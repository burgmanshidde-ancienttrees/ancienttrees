package app.ancienttrees.account

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class AccountTest {

    @Test fun aTokenReplyBecomesASession() {
        val s = Account.parse(
            """{"access_token":"a","refresh_token":"r","expires_in":3600,"user":{"id":"u1","email":"x@y.z"}}""",
            now = 1_000,
        )!!
        assertEquals("a", s.accessToken)
        assertEquals("r", s.refreshToken)
        assertEquals("u1", s.userId)
        assertEquals("x@y.z", s.email)
        assertEquals(3_601_000, s.expiresAt)
    }

    @Test fun aReplyWithoutTokensSignsNobodyIn() {
        assertNull(Account.parse("""{"error":"invalid_grant"}"""))
        assertNull(Account.parse("not json"))
    }

    @Test fun theCallbackFragmentIsRead() {
        val f = Account.fragment("access_token=a%2Bb&refresh_token=r1&expires_in=3600&type=magiclink")
        assertEquals("a+b", f["access_token"])
        assertEquals("r1", f["refresh_token"])
        assertTrue(Account.fragment("").isEmpty())
    }

    @Test fun aSessionGoesStaleAMinuteEarly() {
        val now = System.currentTimeMillis()
        assertTrue(Session("a", "r", now + 120_000, "u", null).isFresh)
        assertTrue(!Session("a", "r", now + 30_000, "u", null).isFresh)
    }

    /** Apple the website's way: Supabase's authorize redirect, back on the iPhone's own callback. */
    @Test fun appleGoesThroughSupabasesRedirectToTheAppsCallback() {
        val u = Account.authorizeUrl("apple")
        assertTrue(u.startsWith(Supa.URL_BASE + "/auth/v1/authorize?provider=apple&"))
        assertTrue(u.endsWith("redirect_to=ancienttrees%3A%2F%2Fauth-callback"))
    }
}
