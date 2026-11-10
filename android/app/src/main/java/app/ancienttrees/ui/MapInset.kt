// The little map, ported from ios Screens/MapInset.swift: a still picture of the
// map round a tree, the tree a moss dot in a white ring, drawn by MapLibre's own
// snapshotter from the same style as the map tab. A square inset with rounded
// corners, a white edge and a soft shadow in the corner of a photograph; or the
// whole hero, edge to edge, on a tree without one. Cached in memory only.

package app.ancienttrees.ui

import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Paint
import android.util.LruCache
import androidx.compose.foundation.Image
import androidx.compose.foundation.border
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.produceState
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import app.ancienttrees.map.STYLE_DARK
import app.ancienttrees.map.STYLE_LIGHT
import app.ancienttrees.map.zoomFor
import kotlinx.coroutines.delay
import kotlinx.coroutines.suspendCancellableCoroutine
import org.maplibre.android.MapLibre
import org.maplibre.android.camera.CameraPosition
import org.maplibre.android.geometry.LatLng
import org.maplibre.android.snapshotter.MapSnapshotter
import kotlin.coroutines.resume

private val thumbs = object : LruCache<String, Bitmap>(12 * 1024 * 1024) {
    override fun sizeOf(key: String, value: Bitmap) = value.byteCount
}

private suspend fun snapshot(
    context: android.content.Context,
    lat: Double,
    lng: Double,
    widthDp: Float,
    heightDp: Float,
    density: Float,
    metres: Double,
    dark: Boolean,
    moss: Int,
): Bitmap? {
    val key = "$lat,$lng,${widthDp.toInt()},${heightDp.toInt()},${if (dark) "d" else "l"}"
    thumbs.get(key)?.let { return it }
    MapLibre.getInstance(context)
    val options = MapSnapshotter.Options(widthDp.toInt(), heightDp.toInt())
        .withPixelRatio(density)
        .withStyle(if (dark) STYLE_DARK else STYLE_LIGHT)
        .withCameraPosition(
            CameraPosition.Builder()
                .target(LatLng(lat, lng))
                .zoom(zoomFor(metres, lat, widthDp.toDouble()))
                .build(),
        )
        .withLogo(false)
        .withAttribution(false)
    val shot: Bitmap = suspendCancellableCoroutine { cont ->
        val s = MapSnapshotter(context, options)
        cont.invokeOnCancellation { runCatching { s.cancel() } }
        s.start({ snap -> if (cont.isActive) cont.resume(snap.bitmap) }, { _ -> if (cont.isActive) cont.resume(null) })
    } ?: return null
    // The tree: a 5 point moss dot in a 2 point ring of the ground colour.
    val out = shot.copy(Bitmap.Config.ARGB_8888, true)
    val c = Canvas(out)
    val cx = out.width / 2f
    val cy = out.height / 2f
    val r = 5 * density
    val p = Paint(Paint.ANTI_ALIAS_FLAG)
    p.color = if (dark) 0xFF0D0F0C.toInt() else android.graphics.Color.WHITE
    c.drawCircle(cx, cy, r + 2 * density, p)
    p.color = moss
    c.drawCircle(cx, cy, r, p)
    thumbs.put(key, out)
    return out
}

/**
 * [side] null: the whole box, [height] tall, edge to edge (the tree page's map hero).
 * Otherwise a [side] square with rounded corners and a white edge.
 */
@Composable
fun MapInset(lat: Double, lng: Double, side: Dp? = 72.dp, height: Dp = 72.dp, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val density = LocalDensity.current.density
    val dark = isSystemInDarkTheme()
    val brand = Brand.colors
    val moss = (if (dark) brand.moss else brand.canopy).toArgb()
    BoxWithConstraints(if (side != null) modifier.size(side) else modifier) {
        val w = side?.value ?: maxWidth.value
        val h = side?.value ?: height.value
        val image by produceState<Bitmap?>(null, lat, lng, w, h, dark) {
            // The page lands first; the picture follows (MapInset.swift waits 400 ms).
            delay(400)
            value = snapshot(context, lat, lng, w, h, density, if (side == null) 700.0 else 500.0, dark, moss)
        }
        val loaded = image
        if (side != null) {
            val shape = RoundedCornerShape(10.dp)
            Box(
                Modifier
                    .fillMaxSize()
                    .shadow(if (loaded != null) 4.dp else 0.dp, shape, ambientColor = Color.Black.copy(alpha = 0.18f), spotColor = Color.Black.copy(alpha = 0.18f))
                    .clip(shape)
                    .then(if (loaded != null) Modifier.border(2.dp, Color.White.copy(alpha = 0.9f), shape) else Modifier),
            ) {
                loaded?.let { Image(it.asImageBitmap(), null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize()) }
            }
        } else {
            loaded?.let { Image(it.asImageBitmap(), null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize()) }
        }
    }
}
