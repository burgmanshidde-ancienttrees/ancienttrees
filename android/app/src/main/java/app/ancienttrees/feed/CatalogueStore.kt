// Where the catalogue comes from, the twin of ios Kit/CatalogueStore.swift, with
// its three rules: a failed refresh is a non-event; a download is all or nothing;
// the bundled copy is the floor and is never touched.
//
// Only OUR catalogue lands on disk ("device" in data/cross-device.json: nobody's
// data, the same on every phone, replaced on the next refresh).

package app.ancienttrees.feed

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.net.HttpURLConnection
import java.net.URL

class CatalogueStore(private val context: Context) {

    private val downloads = File(context.filesDir, "catalogue")

    private fun bundled(name: String): String? =
        runCatching { context.assets.open(name).bufferedReader().use { it.readText() } }.getOrNull()

    /** The downloaded copy where there is one and the bundled one for the rest, per file. */
    private fun read(name: String): String? {
        val f = File(downloads, name)
        if (f.exists()) runCatching { return f.readText() }
        return bundled(name)
    }

    suspend fun load(): Catalogue? = withContext(Dispatchers.Default) {
        try {
            FeedParser.catalogue(read(TREES)!!, read(WALKS)!!, read(SPECIES), read(BROWSE))
        } catch (_: Throwable) {
            // A download that no longer reads would fail on every launch, because
            // the version has not changed and nothing would replace it.
            downloads.deleteRecursively()
            runCatching {
                FeedParser.catalogue(bundled(TREES)!!, bundled(WALKS)!!, bundled(SPECIES), bundled(BROWSE))
            }.getOrNull()
        }
    }

    /** A newer catalogue, or null when there is none or anything went wrong. */
    suspend fun refresh(current: String?): Catalogue? = withContext(Dispatchers.IO) {
        runCatching {
            val remote = FeedParser.version(get("/api/version.json"))
            if (remote == current) return@runCatching null
            val trees = get("/api/$TREES")
            val walks = get("/api/$WALKS")
            val species = runCatching { get("/api/$SPECIES") }.getOrNull()
            val browse = runCatching { get("/api/$BROWSE") }.getOrNull()
            val fresh = FeedParser.catalogue(trees, walks, species, browse)
            // Written only after everything read, each file by rename so a kill
            // mid-write leaves the previous file rather than half a file.
            downloads.mkdirs()
            write(TREES, trees)
            write(WALKS, walks)
            species?.let { write(SPECIES, it) }
            browse?.let { write(BROWSE, it) }
            fresh
        }.getOrNull()
    }

    private fun write(name: String, text: String) {
        val tmp = File(downloads, "$name.tmp")
        tmp.writeText(text)
        tmp.renameTo(File(downloads, name))
    }

    private fun get(path: String): String {
        val c = URL(HOST + path).openConnection() as HttpURLConnection
        c.connectTimeout = 30_000
        c.readTimeout = 30_000
        try {
            check(c.responseCode in 200..299) { "HTTP ${c.responseCode}" }
            return c.inputStream.bufferedReader().use { it.readText() }
        } finally {
            c.disconnect()
        }
    }

    private companion object {
        const val HOST = "https://ancienttrees.app"
        const val TREES = "trees.json"
        const val WALKS = "walks.json"
        const val SPECIES = "species.json"
        const val BROWSE = "browse.json"
    }
}
