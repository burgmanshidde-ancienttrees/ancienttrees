// Sending what the collect flow made, ported from ios Kit/SightingSync.swift
// (push), Kit/Sightings.swift (record, commit) and Kit/Submissions.swift (offer):
// the photograph into the sightings bucket (and the shared one, as every sighting
// is shared from the start), the further photographs beside it, a `sightings` row
// with WHERE THE PHONE STOOD, a `visited` row for a tick, and a `submissions` row
// for a tree only you have. Signed in for real (hard rule 11): nothing is kept on
// the phone afterwards, and a draft lives in memory until Save.

package app.ancienttrees.account

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Matrix
import android.net.Uri
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
    private const val MAX_SIDE = 1600

    /** Sightings.maxExtras: further photographs chosen with the first. */
    const val MAX_EXTRAS = 3

    /** A photograph off the phone: its bytes, and what the file itself says. */
    data class Picked(val raw: ByteArray, val lat: Double?, val lng: Double?, val taken: Date?)

    /** A library file read with its own GPS and date, when the picker left them in. */
    suspend fun read(context: Context, uri: Uri): Picked? = withContext(Dispatchers.IO) {
        runCatching {
            val raw = context.contentResolver.openInputStream(uri)?.use { it.readBytes() } ?: return@runCatching null
            val exif = ExifInterface(ByteArrayInputStream(raw))
            val ll = exif.latLong
            val taken = exif.getAttribute(ExifInterface.TAG_DATETIME_ORIGINAL)?.let {
                runCatching { SimpleDateFormat("yyyy:MM:dd HH:mm:ss", Locale.ROOT).parse(it) }.getOrNull()
            }
            Picked(raw, ll?.get(0), ll?.get(1), taken)
        }.getOrNull()
    }

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

    /** The sightings row, the same keys the iPhone sends (SightingSync.push). */
    fun row(
        userId: String,
        id: String,
        treeId: String?,
        name: String,
        lat: Double,
        lng: Double,
        photo: String?,
        now: Date = Date(),
        taken: Date = now,
        status: String = "mine",
        note: String = "",
        species: String? = null,
        extras: List<String> = emptyList(),
        age: String? = null,
        girthCm: Int? = null,
    ): JSONObject =
        JSONObject()
            .put("user_id", userId)
            .put("id", id)
            .put("tree_id", treeId ?: JSONObject.NULL)
            .put("name", name)
            .put("note", note)
            .put("lat", lat)
            .put("lng", lng)
            .put("taken_at", iso(taken))
            .put("status", status)
            .put("updated_at", iso(now))
            .put("shared", true)
            .put("photo", photo ?: JSONObject.NULL)
            .apply {
                if (species != null) put("species", species)
                if (age != null) put("age", age)
                if (girthCm != null) put("girth_cm", girthCm)
                if (extras.isNotEmpty()) put("extra_photos", JSONArray(extras))
            }

    /** Sightings.extraFile: the further photographs beside the first, private like the sign. */
    fun extraPath(userId: String, id: String, n: Int) = "$userId/$id-extra-$n.jpg"

    /** A new sighting's id, upper case as the iPhone's UUID().uuidString writes it. */
    fun newId(): String = UUID.randomUUID().toString().uppercase()

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
     * One sighting to the account, as SightingSync.push sends it: the photograph
     * first, so a row never points at nothing (to the private bucket, and to the
     * shared one because every sighting is shared from the start), the further
     * photographs to the private bucket only, then the row. One retry without
     * `extra_photos`, the least valuable thing in it, as the iPhone does.
     */
    suspend fun send(
        account: Account,
        id: String,
        treeId: String?,
        name: String,
        lat: Double,
        lng: Double,
        jpeg: ByteArray?,
        extras: List<ByteArray> = emptyList(),
        taken: Date = Date(),
        status: String = "mine",
        note: String = "",
        species: String? = null,
        /** The photograph already uploaded, when only the row changes. */
        storedPath: String? = null,
        age: String? = null,
        girthCm: Int? = null,
    ): Boolean {
        val s = account.fresh() ?: return false
        var stored: String? = storedPath
        if (jpeg != null) {
            val path = "${s.userId}/$id.jpg"
            if (!upload("sightings", path, jpeg, s.accessToken)) return false
            stored = path
            upload("shared-sightings", path, jpeg, s.accessToken)
        }
        val extrasStored = extras.mapIndexedNotNull { i, data ->
            val path = extraPath(s.userId, id, i + 1)
            path.takeIf { upload("sightings", it, data, s.accessToken) }
        }
        val full = row(s.userId, id, treeId, name, lat, lng, stored, taken = taken, status = status,
            note = note, species = species, extras = extrasStored, age = age, girthCm = girthCm)
        val url = "/rest/v1/sightings?on_conflict=user_id,id"
        if (Supa.upsert(url, s.accessToken, JSONArray().put(full))) return true
        if (!full.has("extra_photos")) return false
        full.remove("extra_photos")
        return Supa.upsert(url, s.accessToken, JSONArray().put(full))
    }

    /** The tick: one `visited` row, today. */
    suspend fun tick(account: Account, treeId: String): Boolean {
        val s = account.fresh() ?: return false
        return Supa.upsert(
            "/rest/v1/visited?on_conflict=user_id,tree_id",
            s.accessToken,
            JSONArray().put(JSONObject().put("user_id", s.userId).put("tree_id", treeId).put("visited_at", day())),
        )
    }

    /**
     * CollectSheet.claim: the photograph on one of our trees, filed WHERE THE
     * PHONE STOOD, and the tick. True only when the row and the tick both landed.
     */
    suspend fun collect(
        account: Account,
        treeId: String,
        name: String,
        jpeg: ByteArray,
        lat: Double,
        lng: Double,
        extras: List<ByteArray> = emptyList(),
        taken: Date = Date(),
    ): Boolean {
        if (!send(account, newId(), treeId, name, lat, lng, jpeg, extras, taken)) return false
        return tick(account, treeId)
    }

    /**
     * Save pressed on a draft (Sightings.commit, then Submissions.offer): the tree
     * goes to the account, then to us as a `tree` submission from "app:collect",
     * and the row turns `sent` when that landed.
     */
    suspend fun saveDraft(account: Account, d: Draft, city: String?): Boolean {
        if (!send(account, d.id, null, d.name, d.lat, d.lng, d.jpeg, d.extras, d.taken, note = d.note, species = d.species,
                age = d.age, girthCm = d.girthCm)) {
            return false
        }
        val hint = String.format(Locale.ROOT, "%.5f, %.5f (%s)", d.lat, d.lng, d.fixNote)
        val offered = Submission.tree(city.orEmpty(), d.id, hint, d.note, account.fresh()?.accessToken)
        if (offered) {
            val uid = account.fresh()?.userId
            send(account, d.id, null, d.name, d.lat, d.lng, null, taken = d.taken, status = "sent", note = d.note,
                species = d.species, age = d.age, girthCm = d.girthCm, storedPath = if (d.jpeg != null && uid != null) "$uid/${d.id}.jpg" else null)
        }
        return true
    }

    /** A tree only you have, still being added: in memory until Save (Sighting.draft). */
    data class Draft(
        val id: String,
        val name: String,
        val lat: Double,
        val lng: Double,
        val jpeg: ByteArray?,
        val extras: List<ByteArray>,
        val taken: Date,
        val fixNote: String,
        val place: String?,
        val note: String = "",
        val species: String? = null,
        val age: String? = null,
        val girthCm: Int? = null,
    )
}
