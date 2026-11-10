// Collecting one of our trees with a photograph, the iPhone's claim() in
// CollectSheet.swift and its upload in SightingSync.swift: the photograph into
// the sightings bucket (and the shared one, as every sighting is shared from the
// start), a `sightings` row with the tree's id and WHERE THE PHONE STOOD, and a
// `visited` row. Nothing is kept on the phone afterwards.

package app.ancienttrees.account

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Matrix
import androidx.exifinterface.media.ExifInterface
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.ByteArrayInputStream
import java.io.ByteArrayOutputStream
import java.net.HttpURLConnection
import java.net.URL
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone
import java.util.UUID

object Collector {
    /** Within this of the tree the button is offered: the iPhone's widest reach for a pick. */
    const val REACH_KM = 3.0
    private const val MAX_SIDE = 1600

    /** A camera file as a JPEG no longer than 1600 on its long side, upright. */
    suspend fun downsized(raw: ByteArray): ByteArray? = withContext(Dispatchers.Default) {
        runCatching {
            val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
            BitmapFactory.decodeByteArray(raw, 0, raw.size, bounds)
            var sample = 1
            while (maxOf(bounds.outWidth, bounds.outHeight) / (sample * 2) >= MAX_SIDE) sample *= 2
            var bmp = BitmapFactory.decodeByteArray(raw, 0, raw.size, BitmapFactory.Options().apply { inSampleSize = sample })
                ?: return@runCatching null
            val side = maxOf(bmp.width, bmp.height)
            if (side > MAX_SIDE) {
                val s = MAX_SIDE.toFloat() / side
                bmp = Bitmap.createScaledBitmap(bmp, (bmp.width * s).toInt(), (bmp.height * s).toInt(), true)
            }
            val turn = when (ExifInterface(ByteArrayInputStream(raw)).getAttributeInt(
                ExifInterface.TAG_ORIENTATION, ExifInterface.ORIENTATION_NORMAL,
            )) {
                ExifInterface.ORIENTATION_ROTATE_90 -> 90f
                ExifInterface.ORIENTATION_ROTATE_180 -> 180f
                ExifInterface.ORIENTATION_ROTATE_270 -> 270f
                else -> 0f
            }
            if (turn != 0f) {
                bmp = Bitmap.createBitmap(bmp, 0, 0, bmp.width, bmp.height, Matrix().apply { postRotate(turn) }, true)
            }
            ByteArrayOutputStream().use { out ->
                bmp.compress(Bitmap.CompressFormat.JPEG, 80, out)
                out.toByteArray()
            }
        }.getOrNull()
    }

    /** The day as the `visited` table keeps it. */
    fun day(now: Date = Date()): String = SimpleDateFormat("yyyy-MM-dd", Locale.ROOT).format(now)

    fun iso(now: Date = Date()): String =
        SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", Locale.ROOT).apply { timeZone = TimeZone.getTimeZone("UTC") }.format(now)

    /** The sightings row, the same keys the iPhone sends. */
    fun row(userId: String, id: String, treeId: String, name: String, lat: Double, lng: Double, photo: String?, now: Date = Date()): JSONObject =
        JSONObject()
            .put("user_id", userId)
            .put("id", id)
            .put("tree_id", treeId)
            .put("name", name)
            .put("note", "")
            .put("lat", lat)
            .put("lng", lng)
            .put("taken_at", iso(now))
            .put("status", "mine")
            .put("updated_at", iso(now))
            .put("shared", true)
            .put("photo", photo ?: JSONObject.NULL)

    private suspend fun upload(bucket: String, path: String, jpeg: ByteArray, token: String): Boolean =
        withContext(Dispatchers.IO) {
            runCatching {
                val c = URL("${Supa.URL_BASE}/storage/v1/object/$bucket/$path").openConnection() as HttpURLConnection
                c.requestMethod = "POST"
                c.connectTimeout = 20_000
                c.readTimeout = 60_000
                c.doOutput = true
                c.setRequestProperty("apikey", Supa.KEY)
                c.setRequestProperty("Authorization", "Bearer $token")
                c.setRequestProperty("Content-Type", "image/jpeg")
                c.setRequestProperty("x-upsert", "true")
                try {
                    c.outputStream.use { it.write(jpeg) }
                    c.responseCode in 200..299
                } finally {
                    c.disconnect()
                }
            }.getOrDefault(false)
        }

    /**
     * The photograph first, so a row never points at nothing; then the sighting,
     * then the tick. True only when the row and the tick both landed.
     */
    suspend fun collect(account: Account, treeId: String, name: String, jpeg: ByteArray, lat: Double, lng: Double): Boolean {
        val s = account.fresh() ?: return false
        val id = UUID.randomUUID().toString().uppercase()
        val path = "${s.userId}/$id.jpg"
        val stored = upload("sightings", path, jpeg, s.accessToken)
        if (!stored) return false
        upload("shared-sightings", path, jpeg, s.accessToken)
        val landed = Supa.upsert(
            "/rest/v1/sightings?on_conflict=user_id,id",
            s.accessToken,
            JSONArray().put(row(s.userId, id, treeId, name, lat, lng, path)),
        )
        if (!landed) return false
        return Supa.upsert(
            "/rest/v1/visited?on_conflict=user_id,tree_id",
            s.accessToken,
            JSONArray().put(JSONObject().put("user_id", s.userId).put("tree_id", treeId).put("visited_at", day())),
        )
    }
}
