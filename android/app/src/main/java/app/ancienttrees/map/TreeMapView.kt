// The map, on MapLibre, the same engine, style file and tiles as the iPhone and
// the website. Every tree is one feature in a plain source and MapLibre places the
// pins: a symbol layer that may not overlap drops a pin whose box meets one already
// placed, and the dot layer underneath shows where it stood, so no tree is ever gone
// and a tap always opens the tree. Never MapLibre's own clustering.

package app.ancienttrees.map

import app.ancienttrees.ui.Sym

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
import androidx.compose.ui.graphics.asAndroidPath
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
import org.maplibre.android.geometry.LatLngBounds
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.ln
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

internal const val STYLE_LIGHT = "https://ancienttrees.app/assets/map-style.json"
internal const val STYLE_DARK = "https://ancienttrees.app/assets/map-style-dark.json"
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
    var userMoved = false
    var aimed = false
    var aimedCoverage = 0f
    var aimedWithFix = false
    var padTop = 0.0
    var padBottom = 0.0
    /** The last deliberate move and when, so a sheet that rises after it does not undo it. */
    var lastMove: Pair<(MapLibreMap) -> Unit, Long>? = null
    /** The tree the camera last went to. */
    var centred: String? = null

    private var swaps = 0
    private var firstPinsLogged = false

    /**
     * NO FADE DURING THE SWAP (TreeMap.swift performsPlacementTransitions; Hidde,
     * 2026-11-08: "knipperende pins ... de eerste 10 seconde na download"):
     * MapLibre cross-fades symbols over 0.3 s, so the same pins on the same spots
     * dipped once per data swap. Placement transitions are off for the swap and
     * back on once it is drawn, so a pan or zoom still fades pins as before.
     */
    fun redraw() {
        val st = style ?: return
        val swap = ++swaps
        // Only on a style still in charge: MapLibre throws when a transition is set
        // while a newer style loads (caught by the flow walk, 2026-11-11).
        if (st.isFullyLoaded) st.transition = org.maplibre.android.style.layers.TransitionOptions(300, 0, false)
        st.getSourceAs<GeoJsonSource>(SOURCE)?.setGeoJson(collection(trees, spots, spread))
        // THE FIRST PINS, timed from the process start: what a cold start costs a person.
        if (!firstPinsLogged && trees.isNotEmpty()) {
            firstPinsLogged = true
            val since = android.os.SystemClock.elapsedRealtime() - android.os.Process.getStartElapsedRealtime()
            android.util.Log.i("AncientTrees", "first pins ${trees.size} trees at $since ms from process start")
        }
        android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
            if (swap == swaps && style === st && st.isFullyLoaded) {
                st.transition = org.maplibre.android.style.layers.TransitionOptions(300, 0, true)
            }
        }, 350)
    }
}
private val MOSS = Color.rgb(51, 89, 51)

/** Somewhere to GO, with its own token so the same request is applied once (TreeMap moveTo). */
data class MoveRequest(val token: Long, val box: ViewBox)

/**
 * The map tab's map, the twin of ios Screens/TreeMap.swift.
 *
 * [origin] is where the person is, else Dam square (ContentView.origin), and
 * [located] says whether it is a real fix: the opening shot is retaken once when
 * a guess turns into a fix, and never after a finger moved the map
 * (TreeMap.shouldAim). [dot]: the person has said yes, so the blue dot shows.
 * [recentre] counts presses of the locate control: follow the person, north up.
 * [topCover] and [bottomCover] are px of the map hidden under the search field
 * and under the sheet's stop (capped at half): the camera aims into what is left.
 */
@Composable
fun TreeMapView(
    trees: List<Tree>,
    selected: Tree?,
    onSelect: (Tree?) -> Unit,
    origin: Here,
    located: Boolean,
    dot: Boolean,
    recentre: Int,
    onView: (ViewBox) -> Unit,
    modifier: Modifier = Modifier,
    topCover: Float = 0f,
    bottomCover: Float = 0f,
    moveTo: MoveRequest? = null,
    onUserMove: () -> Unit = {},
    /** A selection that should not move the camera (the launch argument). */
    quietSelect: String? = null,
    /** YOUR OWN TREES (TreeMap.setMine): drawn last, on top of ours, each in your photograph. */
    mine: List<app.ancienttrees.account.OwnSighting> = emptyList(),
    minePhoto: suspend (String) -> ByteArray? = { null },
    onMine: (String) -> Unit = {},
) {
    val latestView by rememberUpdatedState(onView)
    val latestUserMove by rememberUpdatedState(onUserMove)
    val context = LocalContext.current
    val lifecycle = LocalLifecycleOwner.current.lifecycle
    val dark = isSystemInDarkTheme()
    val latestSelect by rememberUpdatedState(onSelect)
    val byId = remember(trees) { trees.associateBy { it.id } }
    val latestById by rememberUpdatedState(byId)
    val holder = remember { MapHolder() }
    var ready by remember { mutableStateOf<Pair<MapLibreMap, Style>?>(null) }
    val latestSelected by rememberUpdatedState(selected)
    val latestOnMine by rememberUpdatedState(onMine)

    val mapView = remember {
        MapLibre.getInstance(context)
        MapView(context).also { view ->
            view.onCreate(null)
            view.getMapAsync { map ->
                map.setMinZoomPreference(PinRules.WORLD_MIN_ZOOM)
                // A first paint on the origin, so the map never shows the Atlantic.
                map.moveCamera(CameraUpdateFactory.newLatLngZoom(LatLng(origin.lat, origin.lng), openingZoom()))
                // No logo; the OpenFreeMap credit stays, it is the price of the tiles.
                map.uiSettings.isLogoEnabled = false
                // NO ROTATION (Hidde, 2026-08-25): every label is a name to read.
                map.uiSettings.isRotateGesturesEnabled = false
                map.uiSettings.isCompassEnabled = false
                map.setStyle(styleFromDisk(context, if (dark) STYLE_DARK else STYLE_LIGHT)) { style ->
                    // One image per shape, about fifteen, never one per species.
                    for (shape in SpeciesIcons.icons.keys) {
                        style.addImage(iconName(shape), pinBitmap(context, shape))
                        style.addImage(iconName(shape) + "-t", pinBitmap(context, shape, ticket = true))
                    }
                    for (n in 2..STACK_ICONS) style.addImage(stackName(n), stackBitmap(context, n))
                    installLayers(style)
                    style.addImage(MINE_ICON, minePinBitmap(context))
                    installMine(style)
                    holder.style = style
                    ready = map to style
                }
                // NOT while a tree is selected: the sheet rising would report a
                // region every frame and rebuild the list under a card (2026-10-20).
                map.addOnCameraIdleListener { if (latestSelected == null) latestView(viewBox(map)) }
                map.addOnCameraMoveStartedListener { reason ->
                    if (reason == MapLibreMap.OnCameraMoveStartedListener.REASON_API_GESTURE) {
                        holder.userMoved = true
                        latestUserMove()
                        // A spread stands a fixed number of points from its spot,
                        // so a pinch or a drag folds it back.
                        if (holder.spread != null) {
                            holder.spread = null
                            holder.redraw()
                        }
                    }
                }
                map.addOnMapClickListener { point ->
                    val at = map.projection.toScreenLocation(point)
                    mineAt(map, at, context)?.let { id ->
                        latestOnMine(id)
                        return@addOnMapClickListener true
                    }
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
                    // A pin SELECTS; a tap on the map itself lets the tree go.
                    latestSelect(tree)
                    true
                }
            }
        }
    }

    // Your trees, and each one's own photograph as its pin once it has loaded.
    LaunchedEffect(ready, mine) {
        val style = ready?.second ?: return@LaunchedEffect
        style.getSourceAs<GeoJsonSource>(SOURCE_MINE)?.setGeoJson(mineCollection(mine, emptySet()))
        val drawn = HashSet<String>()
        for (m in mine) {
            val path = m.photo ?: continue
            val bytes = runCatching { minePhoto(path) }.getOrNull() ?: continue
            val bmp = android.graphics.BitmapFactory.decodeByteArray(bytes, 0, bytes.size) ?: continue
            style.addImage(mineIconFor(m.id), photoPinBitmap(context, bmp))
            drawn.add(m.id)
            style.getSourceAs<GeoJsonSource>(SOURCE_MINE)?.setGeoJson(mineCollection(mine, drawn))
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
        val (map, style) = ready ?: return@LaunchedEffect
        (style.getLayer(LAYER_CHOSEN) as? SymbolLayer)?.setFilter(
            Expression.eq(Expression.get(KEY_ID), Expression.literal(selected?.id ?: "")),
        )
        val sel = selected
        if (sel == null) {
            // A tree was just let go: say once what is in view now.
            if (holder.centred != null) latestView(viewBox(map))
            holder.centred = null
            return@LaunchedEffect
        }
        if (holder.centred == sel.id || sel.id == quietSelect) {
            holder.centred = sel.id
            return@LaunchedEffect
        }
        holder.centred = sel.id
        // Centred at the zoom it already had, never zoomed in (Apple Maps leaves
        // the neighbours on screen); only a map zoomed out past a city comes in.
        val zoom = maxOf(map.cameraPosition.zoom, zoomFor(20_000.0))
        val redo: (MapLibreMap) -> Unit = {
            it.animateCamera(CameraUpdateFactory.newLatLngZoom(LatLng(sel.lat, sel.lng), zoom), 300)
        }
        holder.lastMove = redo to System.currentTimeMillis()
        redo(map)
    }

    // THE CONTENT INSET: the camera aims into the strip a person can see,
    // between the field and chips over the top and the sheet under it.
    LaunchedEffect(ready, topCover, bottomCover) {
        val map = ready?.first ?: return@LaunchedEffect
        val h = mapView.height.toFloat()
        val topPx = minOf(topCover, h / 3).toDouble()
        map.moveCamera(CameraUpdateFactory.paddingTo(0.0, topPx, 0.0, bottomCover.toDouble()))
        holder.padTop = topPx
        holder.padBottom = bottomCover.toDouble()
        // The inset change cancels a flight in progress: finish a deliberate one
        // into the new viewport (TreeMap lastMove, four seconds).
        holder.lastMove?.let { (redo, at) ->
            if (System.currentTimeMillis() - at < 4_000) redo(map)
        }
        // AND NOW AIM, with an inset that is finally real (TreeMap.settle).
        if (shouldAim(holder, bottomCover, located)) {
            holder.aimed = true
            holder.aimedCoverage = bottomCover
            holder.aimedWithFix = located
            map.moveCamera(CameraUpdateFactory.newLatLngZoom(LatLng(origin.lat, origin.lng), openingZoom()))
        }
    }
    // A guess turned into a fix: one more shot, unless a finger moved the map.
    LaunchedEffect(ready, located, origin) {
        val map = ready?.first ?: return@LaunchedEffect
        if (shouldAim(holder, bottomCover, located)) {
            holder.aimed = true
            holder.aimedCoverage = bottomCover
            holder.aimedWithFix = located
            map.moveCamera(CameraUpdateFactory.newLatLngZoom(LatLng(origin.lat, origin.lng), openingZoom()))
            latestView(viewBox(map))
        }
    }

    LaunchedEffect(ready, moveTo?.token) {
        val map = ready?.first ?: return@LaunchedEffect
        val m = moveTo ?: return@LaunchedEffect
        // A DELIBERATE MOVE OWNS THE CAMERA, as a finger does.
        holder.userMoved = true
        val redo: (MapLibreMap) -> Unit = { fit(it, m.box, holder, animate = true) }
        holder.lastMove = redo to System.currentTimeMillis()
        redo(map)
    }

    // THE BLUE DOT, only once the person has said yes: switching it on is what
    // would otherwise make the system ask.
    LaunchedEffect(ready, dot) {
        val (map, style) = ready ?: return@LaunchedEffect
        if (dot) startLocation(map, style, context)
    }
    // Back to you, AND north to the top: following, so the map keeps up with
    // every new fix until a finger moves it (Apple Maps' follow mode).
    LaunchedEffect(recentre) {
        val (map, style) = ready ?: return@LaunchedEffect
        if (recentre == 0) return@LaunchedEffect
        if (startLocation(map, style, context)) follow(map)
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

/** The box into the strip between the field and the sheet. */
private fun fit(map: MapLibreMap, box: ViewBox, h: MapHolder, animate: Boolean) {
    val bounds = LatLngBounds.from(box.north, box.east, box.south, box.west)
    val pos = map.getCameraForLatLngBounds(bounds, intArrayOf(0, h.padTop.toInt(), 0, h.padBottom.toInt())) ?: return
    val update = CameraUpdateFactory.newCameraPosition(pos)
    if (animate) map.animateCamera(update, 600) else map.moveCamera(update)
}

/** Three shots at most, never after a finger (TreeMap.shouldAim). */
private fun shouldAim(h: MapHolder, coverage: Float, hasFix: Boolean): Boolean {
    if (h.userMoved) return false
    if (!h.aimed) return true
    if (h.centred != null) return false
    if (hasFix && !h.aimedWithFix) return true
    return kotlin.math.abs(coverage - h.aimedCoverage) > 1 && h.aimedCoverage <= 0
}

/**
 * MapKit's metres across into MapLibre's zoom (TreeMap.zoom(forMeters:)), on
 * 512-point tiles, at the iPhone's defaults (latitude 52, a 375 point width), so
 * both phones open at the same zoom.
 */
fun zoomFor(metres: Double, latitude: Double = 52.0, width: Double = 375.0): Double {
    val perPoint = (40_075_017.0 / 512.0) * cos(latitude * PI / 180)
    return (ln(perPoint * width / maxOf(metres, 1.0)) / ln(2.0)).coerceIn(1.0, 20.0)
}

/** The map tab's first look: four kilometres across. */
private fun openingZoom() = zoomFor(4000.0)

@SuppressLint("MissingPermission")
private fun startLocation(map: MapLibreMap, style: Style, context: Context): Boolean = runCatching {
    val component = map.locationComponent
    if (!component.isLocationComponentActivated) {
        component.activateLocationComponent(
            LocationComponentActivationOptions.builder(context, style).build(),
        )
    }
    component.isLocationComponentEnabled = true
    component.renderMode = RenderMode.NORMAL
    true
}.getOrDefault(false)

private fun follow(map: MapLibreMap) {
    runCatching {
        val component = map.locationComponent
        component.cameraMode = CameraMode.TRACKING
        component.zoomWhileTracking(maxOf(map.cameraPosition.zoom, NEAR_ZOOM))
        if (map.cameraPosition.bearing != 0.0) map.animateCamera(CameraUpdateFactory.bearingTo(0.0))
    }
}

private const val NEAR_ZOOM = 14.0

private fun viewBox(map: MapLibreMap): ViewBox {
    val b = map.projection.visibleRegion.latLngBounds
    return ViewBox(b.latitudeSouth, b.longitudeWest, b.latitudeNorth, b.longitudeEast)
}

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
        addStringProperty("icon", iconName(SpeciesIcons.archetype(t.commonName)) + if (t.paidEntry) "-t" else "")
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
    // Inter Bold, the text face (ui/Theme.kt), never the system's Roboto.
    paint.typeface = androidx.core.content.res.ResourcesCompat.getFont(context, app.ancienttrees.R.font.inter_bold)
    canvas.drawText(n.toString(), centre, centre - (paint.descent() + paint.ascent()) / 2, paint)
    return bitmap
}

private fun iconName(shape: String) = "at-pin-$shape"

/**
 * The iPhone's pin: a moss disc, a white ring, and the species silhouette in
 * white, 20 points tall, so a ginkgo looks like a ginkgo before anyone taps it.
 */
private fun pinBitmap(context: Context, shape: String, ticket: Boolean = false): Bitmap {
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

    // The silhouette flat and white, 20 points, centred on its own bounds
    // (TreeMap.pin + SpeciesGlyph: SpeciesMark in 22, drawn into 20).
    val glyph = 20 * density
    paint.style = Paint.Style.FILL
    paint.color = Color.WHITE
    canvas.save()
    canvas.translate((size - glyph) / 2, (size - glyph) / 2)
    canvas.drawPath(SpeciesPath.fitted(shape, glyph, glyph), paint)
    canvas.restore()
    // A TICKET, bottom left (TreeMap.pin, Hidde 2026-08-24/25): a white disc a
    // little bigger than the collected tick, the system's ticket glyph in a light
    // navy, never the Plus gold. Material's confirmation_number is Android's ticket.
    if (ticket) {
        val b = 17 * density
        val left = 1 * density
        val top = size - b - 1 * density
        paint.alpha = 255
        paint.color = Color.WHITE
        canvas.drawCircle(left + b / 2, top + b / 2, b / 2, paint)
        // ticket.fill at 9 pt bold is about 13 wide and 9.5 tall; the set's ticket
        // fills 83 percent of its box across: a 12 dp box draws it 10 across inside the 17 disc, as the shots show.
        val g = 12 * density
        canvas.save()
        canvas.translate(left + (b - g) / 2, top + (b - g) / 2)
        // The set draws on 0 -960 960 960 (Symbols.kt), and a path taken out of
        // its vector leaves the group's move behind: scale the grid, then move it
        // into view. Scaled as a 24 grid it fell outside the disc, which drew empty
        // (visual review 2026-11-11).
        canvas.scale(g / 960f, g / 960f)
        canvas.translate(0f, 960f)
        paint.color = TICKET_BLUE
        ticketPath()?.let { canvas.drawPath(it, paint) }
        canvas.restore()
    }
    return bitmap
}

private val TICKET_BLUE = Color.rgb(46, 107, 168)

/** The set's confirmation_number glyph as a path on its own grid (0 -960 960 960). */
private fun ticketPath(): android.graphics.Path? = runCatching {
    val out = android.graphics.Path()
    fun add(group: androidx.compose.ui.graphics.vector.VectorGroup) {
        for (child in group) {
            when (child) {
                is androidx.compose.ui.graphics.vector.VectorPath ->
                    out.addPath(androidx.compose.ui.graphics.vector.PathParser().addPathNodes(child.pathData).toPath().asAndroidPath())
                is androidx.compose.ui.graphics.vector.VectorGroup -> add(child)
            }
        }
    }
    add(Sym.ConfirmationNumberFill.root)
    out
}.getOrNull()


// MARK: your own trees (TreeMap.setMine, minePin, photoPin)

private const val SOURCE_MINE = "at-mine"
private const val LAYER_MINE = "at-mine-pins"
private const val MINE_ICON = "at-pin-mine"

private fun mineIconFor(id: String) = "at-pin-mine-$id"

/** The same keys on every feature, as on our own source. */
private fun mineCollection(mine: List<app.ancienttrees.account.OwnSighting>, withPhoto: Set<String>): FeatureCollection =
    FeatureCollection.fromFeatures(
        mine.map { m ->
            Feature.fromGeometry(Point.fromLngLat(m.lng, m.lat)).apply {
                addStringProperty("mine_id", m.id)
                addStringProperty("icon", if (m.id in withPhoto) mineIconFor(m.id) else MINE_ICON)
                addNumberProperty("pr", -1)
            }
        },
    )

/** Placed like every other pin, and first: your own photograph is the one pin that is a picture of the tree. */
private fun installMine(style: Style) {
    style.addSource(GeoJsonSource(SOURCE_MINE, FeatureCollection.fromFeatures(emptyList<Feature>())))
    style.addLayer(
        SymbolLayer(LAYER_MINE, SOURCE_MINE).withProperties(
            PropertyFactory.iconImage(Expression.get("icon")),
            PropertyFactory.iconAllowOverlap(false),
            PropertyFactory.iconIgnorePlacement(false),
            PropertyFactory.iconPadding(PinRules.padding(PinRules.PIN_DISTANCE)),
            PropertyFactory.iconAnchor(Property.ICON_ANCHOR_CENTER),
            PropertyFactory.symbolSortKey(Expression.get("pr")),
        ),
    )
}

private fun mineAt(map: MapLibreMap, at: PointF, context: Context): String? {
    val reach = 22 * context.resources.displayMetrics.density
    val box = RectF(at.x - reach, at.y - reach, at.x + reach, at.y + reach)
    return map.queryRenderedFeatures(box, LAYER_MINE).firstOrNull { it.hasProperty("mine_id") }?.getStringProperty("mine_id")
}

/** A white disc with a moss ring and the broadleaf in moss: a tree of yours with no photograph yet. */
private fun minePinBitmap(context: Context): Bitmap {
    val metrics = context.resources.displayMetrics
    val density = metrics.density
    val size = (PinRules.PIN_SIZE * density).toInt()
    val bitmap = Bitmap.createBitmap(size, size, Bitmap.Config.ARGB_8888)
    bitmap.density = metrics.densityDpi
    val canvas = Canvas(bitmap)
    val c = size / 2f
    val paint = Paint(Paint.ANTI_ALIAS_FLAG)
    paint.color = Color.WHITE
    canvas.drawCircle(c, c, c - 2 * density, paint)
    paint.color = MOSS
    paint.style = Paint.Style.STROKE
    paint.strokeWidth = 3 * density
    canvas.drawCircle(c, c, c - 2.5f * density, paint)
    paint.style = Paint.Style.FILL
    val glyph = 20 * density
    canvas.save()
    canvas.translate((size - glyph) / 2, (size - glyph) / 2)
    canvas.drawPath(SpeciesPath.fitted("broadleaf", glyph, glyph), paint)
    canvas.restore()
    return bitmap
}

/** Your photograph in the disc, filled to the edge, with an ink ring where ours is white. */
private fun photoPinBitmap(context: Context, photo: Bitmap): Bitmap {
    val metrics = context.resources.displayMetrics
    val density = metrics.density
    val size = (PinRules.PIN_SIZE * density).toInt()
    val bitmap = Bitmap.createBitmap(size, size, Bitmap.Config.ARGB_8888)
    bitmap.density = metrics.densityDpi
    val canvas = Canvas(bitmap)
    val c = size / 2f
    val r = c - 2 * density
    val paint = Paint(Paint.ANTI_ALIAS_FLAG)
    paint.color = Color.WHITE
    canvas.drawCircle(c, c, r, paint)
    canvas.save()
    canvas.clipPath(android.graphics.Path().apply { addCircle(c, c, r, android.graphics.Path.Direction.CW) })
    val scale = maxOf(2 * r / photo.width, 2 * r / photo.height)
    val w = photo.width * scale
    val h = photo.height * scale
    canvas.drawBitmap(photo, null, RectF(c - w / 2, c - h / 2, c + w / 2, c + h / 2), paint)
    canvas.restore()
    paint.color = INK
    paint.style = Paint.Style.STROKE
    paint.strokeWidth = 3 * density
    canvas.drawCircle(c, c, c - 2.5f * density, paint)
    return bitmap
}

private val INK = Color.rgb(0x26, 0x30, 0x1E)

/**
 * THE MAP'S STYLE FROM THE COPY ON DISK, refreshed behind it (cold-start
 * measurement 2026-11-12): the style is served for ten minutes (max-age 600),
 * so most launches waited on the network before a single pin could be drawn,
 * 3.7 to 7.7 s from the process start on the emulator. Its sprite, glyph and
 * tile addresses are absolute, so the JSON opens from text as it does from its
 * address. The first launch, with no copy yet, still loads from the address.
 */
internal fun styleFromDisk(context: android.content.Context, url: String): Style.Builder {
    val file = java.io.File(context.filesDir, "map-style/" + url.substringAfterLast('/'))
    val onDisk = runCatching { file.readText() }.getOrNull()?.takeIf { it.trimStart().startsWith("{") }
    // A first launch has no copy yet: the one built into the app, as the site serves it.
    val kept = onDisk ?: runCatching {
        context.assets.open("map-style/" + url.substringAfterLast('/')).bufferedReader().use { it.readText() }
    }.getOrNull()?.takeIf { it.trimStart().startsWith("{") }
    Thread {
        runCatching {
            val c = java.net.URL(url).openConnection() as java.net.HttpURLConnection
            c.connectTimeout = 20_000
            c.readTimeout = 20_000
            try {
                if (c.responseCode in 200..299) {
                    val text = c.inputStream.bufferedReader().use { it.readText() }
                    if (text != onDisk && text.trimStart().startsWith("{")) {
                        file.parentFile?.mkdirs()
                        val tmp = java.io.File(file.path + ".tmp")
                        tmp.writeText(text)
                        tmp.renameTo(file)
                    }
                }
            } finally {
                c.disconnect()
            }
        }
    }.start()
    return if (kept != null) Style.Builder().fromJson(kept) else Style.Builder().fromUri(url)
}
