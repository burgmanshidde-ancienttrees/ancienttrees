// The server, over plain HTTP: the same Supabase endpoints the iPhone calls in
// Kit/Account.swift, so no client library is added to the product.

package app.ancienttrees.account

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

object Supa {
    const val URL_BASE = "https://caimvxiyrtifilimlkqw.supabase.co"
    const val KEY = "sb_publishable_qOTuw-LCejk2VhO2J6aXGQ_6X2O2mgb"

    /** The custom-scheme callback already on Supabase's redirect allow-list for the iPhone. */
    const val CALLBACK = "ancienttrees://auth-callback"

    data class Reply(val code: Int, val body: String) {
        val ok: Boolean get() = code in 200..299
    }

    /** One request with a timeout: a hang costs more than a refusal. Never throws. */
    suspend fun send(
        path: String,
        method: String = "POST",
        token: String? = null,
        body: String? = null,
        prefer: String? = null,
    ): Reply = withContext(Dispatchers.IO) {
        runCatching {
            val c = URL(URL_BASE + path).openConnection() as HttpURLConnection
            c.requestMethod = method
            c.connectTimeout = 20_000
            c.readTimeout = 20_000
            c.setRequestProperty("apikey", KEY)
            c.setRequestProperty("Content-Type", "application/json")
            c.setRequestProperty("Authorization", "Bearer " + (token ?: KEY))
            prefer?.let { c.setRequestProperty("Prefer", it) }
            if (body != null) {
                c.doOutput = true
                c.outputStream.use { it.write(body.toByteArray()) }
            }
            try {
                val code = c.responseCode
                val stream = if (code in 200..299) c.inputStream else c.errorStream
                Reply(code, stream?.bufferedReader()?.use { it.readText() }.orEmpty())
            } finally {
                c.disconnect()
            }
        }.getOrElse { Reply(0, "") }
    }

    suspend fun rows(path: String, token: String): List<JSONObject> {
        val r = send(path, method = "GET", token = token)
        if (!r.ok) return emptyList()
        return runCatching {
            val a = JSONArray(r.body)
            (0 until a.length()).map { a.getJSONObject(it) }
        }.getOrDefault(emptyList())
    }

    suspend fun upsert(path: String, token: String, rows: JSONArray): Boolean =
        send(path, token = token, body = rows.toString(), prefer = "resolution=merge-duplicates,return=minimal").ok

    suspend fun delete(path: String, token: String): Boolean =
        send(path, method = "DELETE", token = token, prefer = "return=minimal").ok
}
