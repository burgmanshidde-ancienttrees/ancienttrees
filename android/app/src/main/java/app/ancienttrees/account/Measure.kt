// What people actually do in this app: the iPhone's Kit/Measure.swift, line for line.
//
// THE SAME POSTHOG PROJECT, THE SAME EVENTS, THE SAME PROPERTIES, so one query in
// scripts/posthog.py and the digest counts both phones. `os` says which phone
// ("Android 15" beside "iOS 26"); nothing else tells them apart.
//
// NO SDK, AS ON THE IPHONE. Measure.swift explains why it uses no PostHog
// package: the package brings its own networking and buys session replay and
// feature flags, which we want neither of. What is left is one HTTP POST of a
// JSON object to PostHog's capture endpoint, which is what this file sends, the
// same plain-HTTP way Supa.kt talks to the server. So nothing is added to the
// build (CLAUDE.md hard list 5: fewer is better).
//
// WHAT WE SEND (privacy page, "What the app records"): an event name, the app
// version, the major system version, how this copy was built (`debug` or
// `play`), an install id that is a random UUID made on this phone, whether an
// account is signed in, and while one is, its account id. No email, no name, no
// coordinates, no advertising id. `$process_person_profile: false`, as on the iPhone.
//
// ON THE DEVICE: the install id and the waiting events, under the keys the
// iPhone uses (measure.install.v1, measure.queue.v1), both ruled `device` in
// data/cross-device.json. Neither is something a person did that belongs to an
// account: the id identifies an install on purpose, and the queue exists because
// this app is used in woods without signal, where dropping events would bias the
// numbers towards city centres (Measure.swift's own reason).

package app.ancienttrees.account

import android.content.Context
import android.content.SharedPreferences
import android.content.pm.ApplicationInfo
import android.os.Build
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone
import java.util.UUID

object Measure {

    /** Write-only and public by design (Measure.swift): it can send events in and read nothing out. */
    private const val KEY = "phc_nSwWiqWesJZmLMypTZDaeR3MDpcpBwcMpWRy7eUSUpTm"
    private const val HOST = "https://eu.i.posthog.com/i/v0/e/"

    private const val ID_KEY = "measure.install.v1"
    private const val QUEUE_KEY = "measure.queue.v1"
    private const val QUEUE_CAP = 50

    private val io = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private var prefs: SharedPreferences? = null
    private var enabled = false
    private var version = "?"
    private var build = "play"

    /** Whether an account was signed in when the event happened, and which one (Measure.swift). */
    @Volatile var signedIn = false
    @Volatile var account: String? = null

    /**
     * Once, at launch. THE LINE IS THE EMULATOR, NOT THE BUILD (Measure.swift's
     * simulator rule): every parity shot, flow walk and CI run happens on an
     * emulator and no real person is ever on one, so an emulator stays silent
     * unless `-measure` is among the launch arguments; a real phone measures
     * however it was built, and a debug install says `build: debug`, which the
     * digest leaves out.
     */
    fun start(context: Context, args: List<String>) {
        val app = context.applicationContext
        prefs = app.getSharedPreferences("device", Context.MODE_PRIVATE)
        version = runCatching { app.packageManager.getPackageInfo(app.packageName, 0).versionName }.getOrNull() ?: "?"
        build = if (app.applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE != 0) "debug" else "play"
        enabled = !isEmulator() || "-measure" in args
    }

    internal fun isEmulator(): Boolean =
        Build.FINGERPRINT.startsWith("generic") || Build.FINGERPRINT.contains("emulator") ||
            Build.HARDWARE in setOf("ranchu", "goldfish") || Build.PRODUCT.startsWith("sdk") ||
            Build.MODEL.contains("Emulator") || Build.MODEL.contains("Android SDK built for")

    private val installId: String
        get() {
            val p = prefs ?: return "unknown"
            p.getString(ID_KEY, null)?.let { return it }
            val s = UUID.randomUUID().toString().uppercase()
            p.edit().putString(ID_KEY, s).apply()
            return s
        }

    /** The event as PostHog takes it; pure, so a unit test can hold it to the iPhone's shape. */
    internal fun body(
        name: String,
        props: Map<String, String>,
        distinctId: String,
        version: String,
        osMajor: String,
        build: String,
        signedIn: Boolean,
        account: String?,
        now: Date,
    ): JSONObject {
        val p = JSONObject()
        for ((k, v) in props) p.put(k, v)
        p.put("\$process_person_profile", false)
        p.put("app_version", version)
        p.put("os", "Android $osMajor")
        p.put("build", build)
        p.put("signed_in", if (signedIn) "yes" else "no")
        if (signedIn && account != null) p.put("account", account)
        val iso = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", Locale.US).apply { timeZone = TimeZone.getTimeZone("UTC") }
        return JSONObject()
            .put("api_key", KEY)
            .put("event", name)
            .put("distinct_id", distinctId)
            // Sent explicitly, so an event that waited in the queue is filed under when it happened.
            .put("timestamp", iso.format(now))
            .put("properties", p)
    }

    /** Record one thing somebody did. Never blocks, never retries in the moment, never surfaces an error. */
    fun event(name: String, props: Map<String, String> = emptyMap()) {
        if (!enabled) return
        val b = body(name, props, installId, version, Build.VERSION.RELEASE.substringBefore('.'), build,
            signedIn, account, Date())
        val data = b.toString()
        io.launch { if (!post(data)) enqueue(data) }
    }

    /** At launch, before anything is added: a failure now simply queues again rather than looping. */
    fun flush() {
        if (!enabled) return
        val p = prefs ?: return
        val raw = p.getString(QUEUE_KEY, null) ?: return
        p.edit().remove(QUEUE_KEY).apply()
        val q = runCatching { JSONArray(raw) }.getOrNull() ?: return
        for (i in 0 until q.length()) {
            val data = q.optString(i).takeIf { it.isNotEmpty() } ?: continue
            io.launch { if (!post(data)) enqueue(data) }
        }
    }

    private fun post(data: String): Boolean = runCatching {
        val c = URL(HOST).openConnection() as HttpURLConnection
        c.requestMethod = "POST"
        c.connectTimeout = 20_000
        c.readTimeout = 20_000
        c.doOutput = true
        c.setRequestProperty("Content-Type", "application/json")
        try {
            c.outputStream.use { it.write(data.toByteArray()) }
            c.responseCode in 200..299
        } finally {
            c.disconnect()
        }
    }.getOrDefault(false)

    /** The OLDEST go first when the cap is reached: a week offline keeps this morning, not last Tuesday. */
    @Synchronized
    private fun enqueue(data: String) {
        val p = prefs ?: return
        val q = runCatching { JSONArray(p.getString(QUEUE_KEY, "[]")) }.getOrDefault(JSONArray())
        q.put(data)
        val kept = JSONArray()
        for (i in maxOf(0, q.length() - QUEUE_CAP) until q.length()) kept.put(q.get(i))
        p.edit().putString(QUEUE_KEY, kept.toString()).apply()
    }
}
