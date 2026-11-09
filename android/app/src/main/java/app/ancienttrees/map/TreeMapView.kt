// The map, on MapLibre, the same engine, style file and tiles as the iPhone and
// the website. Every tree is one feature in a plain source and MapLibre places the
// pins: a symbol layer that may not overlap drops a pin whose box meets one already
// placed, and the dot layer underneath shows where it stood, so no tree is ever gone
// and a tap always opens the tree. Never MapLibre's own clustering.

package app.ancienttrees.map

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
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
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.compose.LocalLifecycleOwner
import app.ancienttrees.feed.Tree
import org.maplibre.android.MapLibre
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
private const val ICON = "at-pin-default"
private const val KEY_ID = "at_id"
private val TAPPABLE = arrayOf(LAYER_PINS, LAYER_FAR, LAYER_DOTS, LAYER_MINI)
private val MOSS = Color.rgb(51, 89, 51)

@Composable
fun TreeMapView(
    trees: List<Tree>,
    selected: Tree?,
    onSelect: (Tree?) -> Unit,
    modifier: Modifier = Modifier,
) {
    val context = LocalContext.current
    val lifecycle = LocalLifecycleOwner.current.lifecycle
    val dark = isSystemInDarkTheme()
    val latestSelect by rememberUpdatedState(onSelect)
    val byId = remember(trees) { trees.associateBy { it.id } }
    val latestById by rememberUpdatedState(byId)
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
                    style.addImage(ICON, pinBitmap(context))
                    installLayers(style)
                    ready = map to style
                }
                map.addOnMapClickListener { point ->
                    latestSelect(treeAt(map, map.projection.toScreenLocation(point), context, latestById))
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
        val style = ready?.second ?: return@LaunchedEffect
        style.getSourceAs<GeoJsonSource>(SOURCE)?.setGeoJson(collection(trees))
    }

    LaunchedEffect(ready, selected?.id) {
        val style = ready?.second ?: return@LaunchedEffect
        (style.getLayer(LAYER_CHOSEN) as? SymbolLayer)?.setFilter(
            Expression.eq(Expression.get(KEY_ID), Expression.literal(selected?.id ?: "")),
        )
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

/** The same keys on every feature, always: a source with uneven properties has emptied the iPhone's map. */
private fun collection(trees: List<Tree>): FeatureCollection =
    FeatureCollection.fromFeatures(
        trees.map { t ->
            Feature.fromGeometry(Point.fromLngLat(t.lng, t.lat)).apply {
                addStringProperty(KEY_ID, t.id)
                addStringProperty("icon", ICON)
                addNumberProperty("pr", PinRules.priority(t.photo != null, t.saves))
                addBooleanProperty("mini", t.mini)
            }
        },
    )

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
    style.addLayer(pins(LAYER_PINS, PinRules.PIN_DISTANCE).apply { minZoom = PinRules.FAR_ZOOM })
    style.addLayer(pins(LAYER_FAR, PinRules.FAR_PIN_DISTANCE).apply { maxZoom = PinRules.FAR_ZOOM })

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
        .mapNotNull { f -> if (f.hasProperty(KEY_ID)) byId[f.getStringProperty(KEY_ID)] else null }
        .distinctBy { it.id }
        .minByOrNull { t ->
            val p = map.projection.toScreenLocation(LatLng(t.lat, t.lng))
            (p.x - at.x) * (p.x - at.x) + (p.y - at.y) * (p.y - at.y)
        }
}

/** A filled disc with a white ring, 38 points across, the iPhone's default pin. */
private fun pinBitmap(context: Context): Bitmap {
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
    return bitmap
}
