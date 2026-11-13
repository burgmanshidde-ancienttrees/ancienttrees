// A photograph from a web address, without an image library (hard list 5): the
// twin of ios Kit/TreePhoto.swift's ImageStore (audit 2026-11-10, row 10).
//
// - On disk between launches: Android's own HTTP cache (HttpResponseCache, part
//   of the platform), 256 MB as URLCache is on the iPhone, read the way
//   .returnCacheDataElseLoad reads it, so a relaunch on a train draws what it
//   drew yesterday instead of grey tiles.
// - In memory: 64 MB of decoded pictures, counted in bytes.
// - One download per address, however many cards ask for it at once.
// - Eight at a time; the one photograph a screen is about (the tree page's
//   hero) skips the queue (urgent).
// - Three attempts, 0.6 s then 1.8 s apart, honouring Retry-After (0.5 to
//   5 s); a 4xx that is not a rate limit is not asked again.
// - Decoded off the main thread and prepared for drawing.

package app.ancienttrees.ui

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.http.HttpResponseCache
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
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Deferred
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.async
import kotlinx.coroutines.delay
import kotlinx.coroutines.sync.Semaphore
import kotlinx.coroutines.sync.withPermit
import java.io.File
import java.net.HttpURLConnection
import java.net.URL

private const val MAX_SIDE = 1600

private val memory = object : LruCache<String, Bitmap>(64 * 1024 * 1024) {
    override fun sizeOf(key: String, value: Bitmap) = value.byteCount
}

object ImageStore {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private val inFlight = HashMap<String, Deferred<Bitmap?>>()
    private val gate = Semaphore(8)

    /** Somewhere for the bytes to live between launches (ImageStore.prepareCache). Once, at launch. */
    fun prepareCache(context: Context) {
        if (HttpResponseCache.getInstalled() != null) return
        runCatching { HttpResponseCache.install(File(context.cacheDir, "photos-http"), 256L * 1024 * 1024) }
    }

    suspend fun image(url: String, urgent: Boolean = false): Bitmap? {
        memory.get(url)?.let { return it }
        val job = synchronized(inFlight) {
            inFlight.getOrPut(url) {
                scope.async {
                    val b = if (urgent) fetch(url) else gate.withPermit { fetch(url) }
                    b?.also { memory.put(url, it) }
                }.also { d -> d.invokeOnCompletion { synchronized(inFlight) { inFlight.remove(url) } } }
            }
        }
        return job.await()
    }

    private suspend fun fetch(url: String): Bitmap? {
        var wait = 600L
        for (attempt in 1..3) {
            var retryAfter: Long? = null
            val outcome: Result<Bitmap?> = runCatching {
                val c = URL(url).openConnection() as HttpURLConnection
                c.connectTimeout = 20_000
                c.readTimeout = 20_000
                c.useCaches = true
                // The disk copy whatever its age, else the network (.returnCacheDataElseLoad).
                c.addRequestProperty("Cache-Control", "max-stale=" + Int.MAX_VALUE)
                // Wikimedia refuses a request that does not say who it is.
                c.setRequestProperty("User-Agent", "AncientTrees-Android/0.1 (https://ancienttrees.app)")
                try {
                    val code = c.responseCode
                    if (code in 200..299) {
                        val bytes = c.inputStream.use { it.readBytes() }
                        return decode(bytes)
                    }
                    // A 4xx that is not a rate limit will say the same thing three times.
                    if (code != 429 && code < 500) return null
                    c.getHeaderField("Retry-After")?.toDoubleOrNull()?.let {
                        retryAfter = (it.coerceIn(0.5, 5.0) * 1000).toLong()
                    }
                    null
                } finally {
                    c.disconnect()
                }
            }
            // No signal, a stall, a dropped connection, or a 429 / 5xx: worth another go.
            if (outcome.isSuccess && outcome.getOrNull() != null) return outcome.getOrNull()
            if (attempt == 3) return null
            delay(retryAfter ?: wait)
            wait *= 3
        }
        return null
    }

    private fun decode(bytes: ByteArray): Bitmap? {
        val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        BitmapFactory.decodeByteArray(bytes, 0, bytes.size, bounds)
        var sample = 1
        while (maxOf(bounds.outWidth, bounds.outHeight) / sample > MAX_SIDE) sample *= 2
        return BitmapFactory.decodeByteArray(bytes, 0, bytes.size, BitmapFactory.Options().apply { inSampleSize = sample })
            ?.also { it.prepareToDraw() }
    }
}

/** Already in memory: the card's copy a tapped card just drew, shown at once by the page. */
fun cachedImage(url: String): Bitmap? = memory.get(url)

/**
 * [fit] fits the picture inside the box (the photo viewer) instead of filling it.
 * [urgent] skips the download queue: the photograph the screen is about.
 * Until it lands: [fallback] when given, else the tint, or nothing with [placeholder] off.
 */
@Composable
fun RemoteImage(
    url: String,
    description: String?,
    modifier: Modifier = Modifier,
    fit: Boolean = false,
    placeholder: Boolean = true,
    urgent: Boolean = false,
    fallback: (@Composable () -> Unit)? = null,
    /** Loaded when [url] gives nothing (TreePhoto's `fallback` on iOS): a shared
     *  tile's small copy not made yet falls back to the full one (2026-11-13). */
    orElse: String? = null,
) {
    val bitmap by produceState<Bitmap?>(memory.get(url), url) {
        // A recycled row never shows the previous tree's picture.
        value = memory.get(url)
        if (value == null) value = ImageStore.image(url, urgent)
        if (value == null && orElse != null) value = memory.get(orElse) ?: ImageStore.image(orElse, urgent)
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
        // The iPhone's placeholder grey, Brand.surfaceMuted (#F2F2F2; TreePhoto { Brand.surfaceMuted }).
        Box(modifier.background(Brand.colors.surfaceMuted))
    }
}
