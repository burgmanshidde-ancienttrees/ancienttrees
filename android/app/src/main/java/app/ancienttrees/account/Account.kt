// Who is signed in, decided by the server (hard rule 11). The twin of ios
// Kit/Account.swift: an emailed sign-in link and Google, both landing on
// ancienttrees://auth-callback; sign out tells the server; deletion calls the same
// delete_user() the website and the iPhone call.
//
// The one thing kept on the phone is the session token ("device" in
// data/cross-device.json: a session identifies the device and never travels).
// A stored token signs nobody in by itself: at launch it is spent with the server
// first, and only the server's yes makes the app signed in.

package app.ancienttrees.account

import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import org.json.JSONObject
import java.net.URLEncoder

data class Session(
    val accessToken: String,
    val refreshToken: String,
    val expiresAt: Long,
    val userId: String,
    val email: String?,
) {
    val isFresh: Boolean get() = System.currentTimeMillis() < expiresAt - 60_000
}

sealed class SignIn {
    /** Not known yet: the stored token is still being checked with the server. */
    data object Checking : SignIn()
    data object SignedOut : SignIn()
    data object Working : SignIn()
    data class LinkSent(val email: String) : SignIn()
    data class SignedIn(val email: String?) : SignIn()
}

/** Problems a person can act on, as resource-free codes the screens word. */
enum class Problem { NOT_AN_EMAIL, COULD_NOT_SEND, LINK_USED, GOOGLE_OFF }

class Account(context: Context) {
    private val prefs = context.applicationContext.getSharedPreferences("auth", Context.MODE_PRIVATE)
    private val refreshLock = Mutex()

    var state by mutableStateOf<SignIn>(SignIn.Checking)
        private set
    var problem by mutableStateOf<Problem?>(null)
        private set
    var session: Session? = null
        private set

    // MARK: launch

    /** Spend the stored token with the server; only its yes signs anybody in. */
    suspend fun restore() {
        val stored = prefs.getString(KEY_REFRESH, null)
        if (stored.isNullOrEmpty()) {
            state = SignIn.SignedOut
            return
        }
        val fresh = exchange(stored)
        if (fresh != null) store(fresh) else {
            // Refused or unreachable: signed out until the server says otherwise.
            session = null
            state = SignIn.SignedOut
        }
    }

    // MARK: the emailed link

    suspend fun sendLink(address: String) {
        val clean = address.trim()
        if (!clean.contains("@") || clean.length <= 3) {
            problem = Problem.NOT_AN_EMAIL
            return
        }
        state = SignIn.Working
        problem = null
        val back = URLEncoder.encode(Supa.CALLBACK, "UTF-8")
        val body = JSONObject().put("email", clean).put("create_user", true).toString()
        val r = Supa.send("/auth/v1/otp?redirect_to=$back", body = body)
        if (r.ok) {
            state = SignIn.LinkSent(clean)
        } else {
            state = SignIn.SignedOut
            problem = Problem.COULD_NOT_SEND
        }
    }

    // MARK: Google, in the phone's browser

    fun openGoogle(context: Context) {
        problem = null
        val back = URLEncoder.encode(Supa.CALLBACK, "UTF-8")
        val url = "${Supa.URL_BASE}/auth/v1/authorize?provider=google&redirect_to=$back"
        runCatching {
            context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
        }
    }

    /**
     * The callback from an emailed link or from Google. The refresh token in the
     * fragment is spent with the server rather than trusted, so a made-up link
     * signs nobody in. False for a link that carries no tokens.
     */
    suspend fun handleCallback(uri: Uri): Boolean {
        if (uri.scheme != "ancienttrees" || uri.host != "auth-callback") return false
        val f = fragment(uri.encodedFragment ?: uri.encodedQuery.orEmpty())
        val refresh = f["refresh_token"]
        if (refresh.isNullOrEmpty()) {
            if (f.containsKey("error") || f.containsKey("error_description")) {
                state = SignIn.SignedOut
                problem = Problem.GOOGLE_OFF
            }
            return false
        }
        state = SignIn.Working
        problem = null
        val fresh = exchange(refresh)
        if (fresh == null) {
            state = SignIn.SignedOut
            problem = Problem.LINK_USED
            return false
        }
        store(fresh)
        return true
    }

    // MARK: a token that will still be accepted

    /** Every write goes through here; at most one refresh is ever in flight. */
    suspend fun fresh(): Session? = refreshLock.withLock {
        val s = session ?: return@withLock null
        if (s.isFresh) return@withLock s
        val next = exchange(s.refreshToken)
        if (next != null) store(next) else if (lastRefusal) clear()
        session
    }

    // MARK: leaving

    suspend fun signOut() {
        val s = session
        clear()
        if (s != null) Supa.send("/auth/v1/logout", token = s.accessToken)
    }

    /** The same delete_user() the website and the iPhone call. Saves and visits cascade. */
    suspend fun deleteAccount(): Boolean {
        val s = fresh() ?: return false
        val ok = Supa.send("/rest/v1/rpc/delete_user", token = s.accessToken, body = "{}").ok
        if (ok) clear()
        return ok
    }

    fun dismissProblem() {
        problem = null
        if (state is SignIn.LinkSent || state is SignIn.Working) state = SignIn.SignedOut
    }

    // MARK: inside

    private var lastRefusal = false

    private suspend fun exchange(refresh: String): Session? {
        val r = Supa.send(
            "/auth/v1/token?grant_type=refresh_token",
            body = JSONObject().put("refresh_token", refresh).toString(),
        )
        // A refusal (4xx) means the token is dead; no answer at all is only a bad signal.
        lastRefusal = r.code in 400..499
        return if (r.ok) parse(r.body) else null
    }

    private fun store(s: Session) {
        session = s
        state = SignIn.SignedIn(s.email)
        problem = null
        prefs.edit().putString(KEY_REFRESH, s.refreshToken).apply()
    }

    private fun clear() {
        session = null
        state = SignIn.SignedOut
        prefs.edit().remove(KEY_REFRESH).apply()
    }

    companion object {
        private const val KEY_REFRESH = "session.refresh"

        /** Supabase's token reply; null when it carries no tokens. */
        fun parse(body: String, now: Long = System.currentTimeMillis()): Session? = runCatching {
            val j = JSONObject(body)
            val access = j.optString("access_token")
            val refresh = j.optString("refresh_token")
            if (access.isEmpty() || refresh.isEmpty()) return@runCatching null
            val user = j.optJSONObject("user")
            Session(
                accessToken = access,
                refreshToken = refresh,
                expiresAt = now + j.optLong("expires_in", 3600) * 1000,
                userId = user?.optString("id").orEmpty(),
                email = user?.let { if (it.isNull("email")) null else it.optString("email") },
            )
        }.getOrNull()

        /** "a=1&b=two" from a callback's fragment, decoded. */
        fun fragment(raw: String): Map<String, String> =
            raw.split("&").mapNotNull { pair ->
                val i = pair.indexOf('=')
                if (i <= 0) null else pair.substring(0, i) to java.net.URLDecoder.decode(pair.substring(i + 1), "UTF-8")
            }.toMap()
    }
}
