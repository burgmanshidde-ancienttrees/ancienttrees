package app.ancienttrees.account

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import java.util.Date

/** Android's events in the iPhone's shape (Kit/Measure.swift), so one query counts both phones. */
class MeasureTest {

    private fun body(signedIn: Boolean, account: String?) = Measure.body(
        "tree_opened", mapOf("tree" to "lis_001", "near" to "unknown"), "ABC", "0.1.0", "15", "play",
        signedIn, account, Date(0),
    )

    @Test fun theIphonesKeysAndNoMore() {
        val b = body(signedIn = true, account = "u1")
        assertEquals("tree_opened", b.getString("event"))
        assertEquals("ABC", b.getString("distinct_id"))
        assertEquals("1970-01-01T00:00:00Z", b.getString("timestamp"))
        assertTrue(b.getString("api_key").startsWith("phc_"))
        val p = b.getJSONObject("properties")
        assertEquals(
            setOf("tree", "near", "\$process_person_profile", "app_version", "os", "build", "signed_in", "account"),
            p.keys().asSequence().toSet(),
        )
        assertEquals(false, p.getBoolean("\$process_person_profile"))
        assertEquals("Android 15", p.getString("os"))
        assertEquals("yes", p.getString("signed_in"))
        assertEquals("u1", p.getString("account"))
    }

    @Test fun signedOutSendsNothingAccountShaped() {
        val p = body(signedIn = false, account = "u1").getJSONObject("properties")
        assertEquals("no", p.getString("signed_in"))
        assertFalse(p.has("account"))
    }
}
