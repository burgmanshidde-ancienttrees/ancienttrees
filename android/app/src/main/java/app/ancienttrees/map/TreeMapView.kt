// The map, on MapLibre, the same engine, style file and tiles as the iPhone and
// the website. Every tree is one feature in a plain source and MapLibre places the
// pins: a symbol layer that may not overlap drops a pin whose box meets one already
// placed, and the dot layer underneath shows where it stood, so no tree is ever gone
// and a tap always opens the tree. Never MapLibre's own clustering.

package app.ancienttrees.map

import android.annotation.SuppressLint
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Matrix
import android.graphics.Paint
import android.graphics.PointF
import android.graphics.RectF
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.navigationBars
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.graphics.PathParser
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.compose.LocalLifecycleOwner
import app.ancienttrees.feed.Here
import app.ancienttrees.feed.Tree
import app.ancienttrees.feed.ViewBox
import org.maplibre.android.MapLibre
import org.maplibre.android.location.LocationComponentActivationOptions
import org.maplibre.android.location.modes.CameraMode
import org.maplibre.android.location.modes.RenderMode
import org.maplibre.android.camera.CameraUpdateFactory
import org.maplibre.android.geometry.LatLng
import org.maplibre.android.maps.MapLibreMap
import org.maplibre.android.maps.MapView
import org.maplibre.android.maps.Style
import org.maplibre.android.style.expressions.Expression
import org.maplibre.android.style.layers.CircleLayer
import org.maplibre.android.style.layers.Property
import org.maplibre.android.style.layers.PropertyFactory
import org.maplibre.android.style.layers.SymbolLayer
import org.maplibre.android.style.sources.GeoJsonSource
import org.maplibre.geojson.Feature
import org.maplibre.geojson.FeatureCollection
import org.maplibre.geojson.Point

private const val STYLE_LIGHT = "https://ancienttrees.app/assets/map-style.json"
private const val STYLE_DARK = "https://ancienttrees.app/assets/map-style-dark.json"
private const val SOURCE = "at-trees"
private const val LAYER_MINI = "at-mini"
private const val LAYER_DOTS = "at-dots"
private const val LAYER_PINS = "at-pins"
private const val LAYER_FAR = "at-pins-far"
private const val LAYER_CHOSEN = "at-chosen"
private const val KEY_ID = "at_id"
private const val LAYER_STACK = "at-stack"
private const val LAYER_SPREAD = "at-spread"
private val TAPPABLE = arrayOf(LAYER_SPREAD, LAYER_STACK, LAYER_PINS, LAYER_FAR, LAYER_DOTS, LAYER_MINI)

/** The pile spread out right now, if any: its spot and where each tree stands. */
private class Spread(val spot: String, val at: Map<String, LatLng>)

/** What the map's listeners read, so they always see the newest trees and spread. */
private class MapHolder {
    var trees: List<Tree> = emptyList()
    var spots: Map<String, List<Tree>> = emptyMap()
    var spread: Spread? = null
    var style: Style? = null

    fun redraw() {
        style?.getSourceAs<GeoJsonSource>(SOURCE)?.setGeoJson(collection(trees, spots, spread))
    }
}
private val MOSS = Color.rgb(51, 89, 51)

/**
 * [locationOn]: the person has said yes, so the blue dot shows and the map goes
 * to them once. [recentre] counts presses of the my-location button.
 * [onView] hears where the map now looks and, when known, where the person is.
 */
@Composable
fun TreeMapView(
    trees: List<Tree>,
    selected: Tree?,
    onSelect: (Tree?) -> Unit,
    locationOn: Boolean,
    recentre: Int,
    onView: (ViewBox, Here?) -> Unit,
    modifier: Modifier = Modifier,
) {
    val latestView by rememberUpdatedState(onView)
    val context = LocalContext.current
    val lifecycle = LocalLifecycleOwner.current.lifecycle
    val dark = isSystemInDarkTheme()
    val latestSelect by rememberUpdatedState(onSelect)
    val byId = remember(trees) { trees.associateBy { it.id } }
    val latestById by rememberUpdatedState(byId)
    val holder = remember { MapHolder() }
    var ready by remember { mutableStateOf<Pair<MapLibreMap, Style>?>(null) }

    val mapView = remember {
        MapLibre.getInstance(context)
        MapView(context).also { view ->
            view.onCreate(null)
            view.getMapAsync { map ->
                map.setMinZoomPreference(PinRules.WORLD_MIN_ZOOM)
                map.moveCamera(CameraUpdateFactory.newLatLngZoom(LatLng(50.0, 10.0), 3.0))
                // No logo; the OpenFreeMap credit stays, it is the price of the tiles.
                map.uiSettings.isLogoEnabled = false
                map.uiSettings.isRotateGesturesEnabled = false
                map.setStyle(Style.Builder().fromUri(if (dark) STYLE_DARK else STYLE_LIGHT)) { style ->
                    // One image per shape, about fifteen, never one per species.
                    for (shape in SpeciesIcons.icons.keys) {
                        style.addImage(iconName(shape), pinBitmap(context, shape))
                    }
                    for (n in 2..STACK_ICONS) style.addImage(stackName(n), stackBitmap(context, n))
                    installLayers(style)
                    holder.style = style
                    ready = map to style
                }
                map.addOnCameraIdleListener { latestView(viewBox(map), here(map)) }
                // A spread stands a fixed number of points from its spot, so a
                // pinch or a drag folds it back.
                map.addOnCameraMoveStartedListener { reason ->
                    if (reason == MapLibreMap.OnCameraMoveStartedListener.REASON_API_GESTURE && holder.spread != null) {
                        holder.spread = null
                        holder.redraw()
                    }
                }
                map.addOnMapClickListener { point ->
                    val at = map.projection.toScreenLocation(point)
                    val stack = stackAt(map, at, context)
                    if (stack != null) {
                        holder.spread = spreadOut(map, stack, holder.spots[stack].orEmpty(), context)
                        holder.redraw()
                        return@addOnMapClickListener true
                    }
                    val tree = treeAt(map, at, context, latestById)
                    if (tree == null && holder.spread != null) {
                        holder.spread = null
                        holder.redraw()
                    }
                    latestSelect(tree)
                    true
                }
            }
        }
    }

    DisposableEffect(lifecycle, mapView) {
        val observer = LifecycleEventObserver { _, event ->
            when (event) {
                Lifecycle.Event.ON_START -> mapView.onStart()
                Lifecycle.Event.ON_RESUME -> mapView.onResume()
                Lifecycle.Event.ON_PAUSE -> mapView.onPause()
                Lifecycle.Event.ON_STOP -> mapView.onStop()
                else -> Unit
            }
        }
        lifecycle.addObserver(observer)
        onDispose {
            lifecycle.removeObserver(observer)
            mapView.onDestroy()
        }
    }

    LaunchedEffect(ready, trees) {
        if (ready == null) return@LaunchedEffect
        holder.trees = trees
        holder.spots = Stacks.spots(trees)
        holder.spread = null
        holder.redraw()
    }

    LaunchedEffect(ready, selected?.id) {
        val style = ready?.second ?: return@LaunchedEffect
        (style.getLayer(LAYER_CHOSEN) as? SymbolLayer)?.setFilter(
            Expression.eq(Expression.get(KEY_ID), Expression.literal(selected?.id ?: "")),
        )
    }

    // THE BLUE DOT, only once the person has said yes: switching it on is what
    // would otherwise make the system ask. The first fix brings the map to them;
    // after that the map is theirs until they press my location.
    var located by remember { mutableStateOf(false) }
    LaunchedEffect(ready, locationOn) {
        val (map, style) = ready ?: return@LaunchedEffect
        if (!locationOn || located) return@LaunchedEffect
        if (startLocation(map, style, context)) {
            located = true
            follow(map)
        }
    }
    LaunchedEffect(recentre) {
        val map = ready?.first ?: return@LaunchedEffect
        if (recentre > 0 && located) follow(map)
    }

    // The credit stands clear of the system's navigation bar.
    val bottomInset = WindowInsets.navigationBars.getBottom(LocalDensity.current)
    LaunchedEffect(ready, bottomInset) {
        val map = ready?.first ?: return@LaunchedEffect
        val margin = (8 * context.resources.displayMetrics.density).toInt()
        map.uiSettings.setAttributionMargins(margin, 0, 0, bottomInset + margin)
    }

    AndroidView(factory = { mapView }, modifier = modifier)
}

private const val NEAR_ZOOM = 14.0

@SuppressLint("MissingPermission")
private fun startLocation(map: MapLibreMap, style: Style, context: Context): Boolean = runCatching {
    val component = map.locationComponent
    component.activateLocationComponent(
        LocationComponentActivationOptions.builder(context, style).build(),
    )
    component.isLocationComponentEnabled = true
    component.renderMode = RenderMode.NORMAL
    true
}.getOrDefault(false)

/** To the person, once: tracking lets go by itself as soon as they pan. */
private fun follow(map: MapLibreMap) {
    runCatching {
        val component = map.locationComponent
        component.cameraMode = CameraMode.TRACKING
        component.zoomWhileTracking(maxOf(map.cameraPosition.zoom, NEAR_ZOOM))
    }
}

private fun viewBox(map: MapLibreMap): ViewBox {
    val b = map.projection.visibleRegion.latLngBounds
    return ViewBox(b.latitudeSouth, b.longitudeWest, b.latitudeNorth, b.longitudeEast)
}

private fun here(map: MapLibreMap): Here? = runCatching {
    val c = map.locationComponent
    if (!c.isLocationComponentActivated || !c.isLocationComponentEnabled) return@runCatching null
    c.lastKnownLocation?.let { Here(it.latitude, it.longitude) }
}.getOrNull()

/**
 * The same keys on every feature, always: a source with uneven properties has
 * emptied the iPhone's map. One feature per spot; the first tree on a shared spot
 * carries the count, unless that pile is the one spread out.
 */
private fun collection(trees: List<Tree>, spots: Map<String, List<Tree>>, spread: Spread?): FeatureCollection {
    val features = ArrayList<Feature>(trees.size)
    for ((spot, group) in spots) {
        if (spread != null && spread.spot == spot) {
            for (t in group) {
                val p = spread.at[t.id] ?: continue
                features.add(feature(t, p.latitude, p.longitude, n = 1, spot = spot, spread = true))
            }
        } else {
            val head = group.first()
            features.add(feature(head, head.lat, head.lng, n = group.size, spot = spot, spread = false))
        }
    }
    return FeatureCollection.fromFeatures(features)
}

private fun feature(t: Tree, lat: Double, lng: Double, n: Int, spot: String, spread: Boolean): Feature =
    Feature.fromGeometry(Point.fromLngLat(lng, lat)).apply {
        addStringProperty(KEY_ID, t.id)
        addStringProperty("icon", iconName(SpeciesIcons.archetype(t.commonName)))
        addStringProperty("stack", if (n > 1) stackName(minOf(n, STACK_ICONS)) else "")
        addStringProperty("spot", spot)
        addNumberProperty("n", n)
        addNumberProperty("pr", PinRules.priority(t.photo != null, t.saves))
        addBooleanProperty("mini", t.mini)
        addBooleanProperty("spread", spread)
    }

private fun installLayers(style: Style) {
    style.addSource(GeoJsonSource(SOURCE, FeatureCollection.fromFeatures(emptyList<Feature>())))

    style.addLayer(
        CircleLayer(LAYER_MINI, SOURCE).withProperties(
            PropertyFactory.circleColor(MOSS),
            PropertyFactory.circleRadius(PinRules.MINI_RADIUS),
            PropertyFactory.circleStrokeColor(Color.WHITE),
            PropertyFactory.circleStrokeWidth(1f),
        ).apply {
            setFilter(Expression.eq(Expression.get("mini"), Expression.literal(true)))
            maxZoom = PinRules.FAR_ZOOM
        },
    )
    style.addLayer(
        CircleLayer(LAYER_DOTS, SOURCE).withProperties(
            PropertyFactory.circleColor(MOSS),
            PropertyFactory.circleRadius(4f),
            PropertyFactory.circleStrokeColor(Color.WHITE),
            PropertyFactory.circleStrokeWidth(1.5f),
        ).apply { minZoom = PinRules.FAR_ZOOM },
    )

    fun pins(id: String, distance: Float) = SymbolLayer(id, SOURCE).withProperties(
        PropertyFactory.iconImage(Expression.get("icon")),
        PropertyFactory.iconAllowOverlap(false),
        PropertyFactory.iconIgnorePlacement(false),
        PropertyFactory.iconPadding(PinRules.padding(distance)),
        PropertyFactory.iconAnchor(Property.ICON_ANCHOR_CENTER),
        PropertyFactory.symbolSortKey(Expression.get("pr")),
    )
    // A pile's first tree is an ordinary pin until STACK_ZOOM, then its bubble.
    val single = Expression.all(
        Expression.eq(Expression.get("spread"), Expression.literal(false)),
        Expression.any(
            Expression.eq(Expression.get("n"), Expression.literal(1)),
            Expression.lt(Expression.zoom(), Expression.literal(Stacks.STACK_ZOOM)),
        ),
    )
    style.addLayer(pins(LAYER_PINS, PinRules.PIN_DISTANCE).apply { minZoom = PinRules.FAR_ZOOM; setFilter(single) })
    style.addLayer(pins(LAYER_FAR, PinRules.FAR_PIN_DISTANCE).apply { maxZoom = PinRules.FAR_ZOOM; setFilter(single) })

    style.addLayer(
        SymbolLayer(LAYER_STACK, SOURCE).withProperties(
            PropertyFactory.iconImage(Expression.get("stack")),
            PropertyFactory.iconAllowOverlap(true),
            PropertyFactory.iconAnchor(Property.ICON_ANCHOR_CENTER),
        ).apply {
            setFilter(
                Expression.all(
                    Expression.gt(Expression.get("n"), Expression.literal(1)),
                    Expression.gte(Expression.zoom(), Expression.literal(Stacks.STACK_ZOOM)),
                ),
            )
        },
    )
    style.addLayer(
        SymbolLayer(LAYER_SPREAD, SOURCE).withProperties(
            PropertyFactory.iconImage(Expression.get("icon")),
            PropertyFactory.iconAllowOverlap(true),
            PropertyFactory.iconAnchor(Property.ICON_ANCHOR_CENTER),
        ).apply { setFilter(Expression.eq(Expression.get("spread"), Expression.literal(true))) },
    )

    style.addLayer(
        SymbolLayer(LAYER_CHOSEN, SOURCE).withProperties(
            PropertyFactory.iconImage(Expression.get("icon")),
            PropertyFactory.iconAllowOverlap(true),
            PropertyFactory.iconAnchor(Property.ICON_ANCHOR_CENTER),
            PropertyFactory.iconSize(1.5f),
        ).apply { setFilter(Expression.eq(Expression.get(KEY_ID), Expression.literal(""))) },
    )
}

/** The nearest tree under a finger, on a full pin or a dot. Null is a tap on the map itself. */
private fun treeAt(map: MapLibreMap, at: PointF, context: Context, byId: Map<String, Tree>): Tree? {
    val reach = 22 * context.resources.displayMetrics.density
    val box = RectF(at.x - reach, at.y - reach, at.x + reach, at.y + reach)
    return map.queryRenderedFeatures(box, *TAPPABLE)
        .filter { f -> f.hasProperty(KEY_ID) && !(f.hasProperty("n") && f.getNumberProperty("n").toInt() > 1 && map.cameraPosition.zoom >= Stacks.STACK_ZOOM) }
        .mapNotNull { f ->
            val tree = byId[f.getStringProperty(KEY_ID)] ?: return@mapNotNull null
            val g = f.geometry() as? Point ?: return@mapNotNull null
            val p = map.projection.toScreenLocation(LatLng(g.latitude(), g.longitude()))
            tree to (p.x - at.x) * (p.x - at.x) + (p.y - at.y) * (p.y - at.y)
        }
        .minByOrNull { it.second }
        ?.first
}

/** The spot of a pile's bubble under a finger, or null. */
private fun stackAt(map: MapLibreMap, at: PointF, context: Context): String? {
    if (map.cameraPosition.zoom < Stacks.STACK_ZOOM) return null
    val reach = 22 * context.resources.displayMetrics.density
    val box = RectF(at.x - reach, at.y - reach, at.x + reach, at.y + reach)
    return map.queryRenderedFeatures(box, LAYER_STACK)
        .firstOrNull { it.hasProperty("spot") }
        ?.getStringProperty("spot")
}

/** Spread a pile round its spot at the zoom it is tapped at. */
private fun spreadOut(map: MapLibreMap, spot: String, trees: List<Tree>, context: Context): Spread? {
    val head = trees.firstOrNull() ?: return null
    val density = context.resources.displayMetrics.density
    val centre = map.projection.toScreenLocation(LatLng(head.lat, head.lng))
    val at = trees.zip(Stacks.spreadOffsets(trees.size)).associate { (t, o) ->
        t.id to map.projection.fromScreenLocation(PointF(centre.x + o.first * density, centre.y + o.second * density))
    }
    return Spread(spot, at)
}

private const val STACK_ICONS = 99

private fun stackName(n: Int) = "at-stack-$n"

/** A pile's bubble: moss, white ring, the count in white, one size whatever the count. */
private fun stackBitmap(context: Context, n: Int): Bitmap {
    val metrics = context.resources.displayMetrics
    val density = metrics.density
    val size = (PinRules.PIN_SIZE * density).toInt()
    val bitmap = Bitmap.createBitmap(size, size, Bitmap.Config.ARGB_8888)
    bitmap.density = metrics.densityDpi
    val canvas = Canvas(bitmap)
    val centre = size / 2f
    val paint = Paint(Paint.ANTI_ALIAS_FLAG)
    paint.color = MOSS
    canvas.drawCircle(centre, centre, centre - 2 * density, paint)
    paint.color = Color.WHITE
    paint.style = Paint.Style.STROKE
    paint.strokeWidth = 3 * density
    canvas.drawCircle(centre, centre, centre - 2.5f * density, paint)
    paint.style = Paint.Style.FILL
    paint.textAlign = Paint.Align.CENTER
    paint.textSize = 15 * density
    paint.isFakeBoldText = true
    canvas.drawText(n.toString(), centre, centre - (paint.descent() + paint.ascent()) / 2, paint)
    return bitmap
}

private fun iconName(shape: String) = "at-pin-$shape"

/**
 * The iPhone's pin: a moss disc, a white ring, and the species silhouette in
 * white, 20 points tall, so a ginkgo looks like a ginkgo before anyone taps it.
 */
private fun pinBitmap(context: Context, shape: String): Bitmap {
    val metrics = context.resources.displayMetrics
    val density = metrics.density
    val size = (PinRules.PIN_SIZE * density).toInt()
    val bitmap = Bitmap.createBitmap(size, size, Bitmap.Config.ARGB_8888)
    // MapLibre reads the bitmap's density, so the pin keeps its size in points.
    bitmap.density = metrics.densityDpi
    val canvas = Canvas(bitmap)
    val centre = size / 2f
    val paint = Paint(Paint.ANTI_ALIAS_FLAG)
    paint.color = MOSS
    canvas.drawCircle(centre, centre, centre - 2 * density, paint)
    paint.color = Color.WHITE
    paint.style = Paint.Style.STROKE
    paint.strokeWidth = 3 * density
    canvas.drawCircle(centre, centre, centre - 2.5f * density, paint)

    val glyph = 20 * density
    paint.style = Paint.Style.FILL
    canvas.save()
    canvas.translate((size - glyph) / 2, (size - glyph) / 2)
    canvas.scale(glyph / 40f, glyph / 40f)
    for (part in SpeciesIcons.icons[shape].orEmpty()) {
        paint.alpha = (part.alpha * 255).toInt()
        when (part) {
            is SpeciesIcons.Part.Oval -> canvas.drawOval(RectF(part.left, part.top, part.right, part.bottom), paint)
            is SpeciesIcons.Part.Shape -> {
                val path = runCatching { PathParser.createPathFromPathData(part.d) }.getOrNull() ?: continue
                val m = Matrix()
                part.rotate?.let { m.setRotate(it[0], it[1], it[2]) }
                part.translate?.let { m.setTranslate(it[0], it[1]) }
                path.transform(m)
                canvas.drawPath(path, paint)
            }
        }
    }
    canvas.restore()
    return bitmap
}
