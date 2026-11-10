// A photograph from a web address, without an image library (hard list 5).
// Held in memory only and fetched again after a restart.

package app.ancienttrees.ui

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.util.LruCache
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.produceState
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.net.HttpURLConnection
import java.net.URL

private const val MAX_SIDE = 1600

private val memory = object : LruCache<String, Bitmap>(32 * 1024 * 1024) {
    override fun sizeOf(key: String, value: Bitmap) = value.byteCount
}

private fun fetch(url: String): Bitmap? = runCatching {
    val c = URL(url).openConnection() as HttpURLConnection
    c.connectTimeout = 20_000
    c.readTimeout = 30_000
    // Wikimedia refuses a request that does not say who it is.
    c.setRequestProperty("User-Agent", "AncientTrees-Android/0.1 (https://ancienttrees.app)")
    try {
        if (c.responseCode !in 200..299) return@runCatching null
        val bytes = c.inputStream.use { it.readBytes() }
        val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        BitmapFactory.decodeByteArray(bytes, 0, bytes.size, bounds)
        var sample = 1
        while (maxOf(bounds.outWidth, bounds.outHeight) / sample > MAX_SIDE) sample *= 2
        BitmapFactory.decodeByteArray(bytes, 0, bytes.size, BitmapFactory.Options().apply { inSampleSize = sample })
    } finally {
        c.disconnect()
    }
}.getOrNull()

/** Already in memory: the card's copy a tapped card just drew, shown at once by the page. */
fun cachedImage(url: String): Bitmap? = memory.get(url)

/**
 * [fit] fits the picture inside the box (the photo viewer) instead of filling it.
 * Until it lands: [fallback] when given, else the tint, or nothing with [placeholder] off.
 */
@Composable
fun RemoteImage(
    url: String,
    description: String?,
    modifier: Modifier = Modifier,
    fit: Boolean = false,
    placeholder: Boolean = true,
    fallback: (@Composable () -> Unit)? = null,
) {
    val bitmap by produceState<Bitmap?>(memory.get(url), url) {
        if (value == null) {
            value = withContext(Dispatchers.IO) { fetch(url) }?.also { memory.put(url, it) }
        }
    }
    val loaded = bitmap
    if (loaded != null) {
        Image(
            bitmap = loaded.asImageBitmap(),
            contentDescription = description,
            contentScale = if (fit) ContentScale.Fit else ContentScale.Crop,
            modifier = modifier,
        )
    } else if (fallback != null) {
        Box(modifier) { fallback() }
    } else if (placeholder) {
        Box(modifier.background(MaterialTheme.colorScheme.surfaceVariant))
    }
}
