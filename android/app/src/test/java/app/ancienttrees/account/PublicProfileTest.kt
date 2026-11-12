package app.ancienttrees.account

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * public_profile()'s answer with and without supabase/approved-on-profiles.sql
 * (2026-11-12): a profile without `approved` and `own` still opens, with empty
 * lists (PublicProfileTests.swift on the iPhone).
 */
class PublicProfileTest {
    private val before = """
        {"user_id":"u1","display_name":"Marieke","avatar_url":null,"country":"NL",
         "created_at":"2026-09-01","followers":3,"following":1,"ambassador":[],
         "visited":["brn_001","brn_002"],"saves":["brn_003"]}
    """.trimIndent()

    private val after = """
        {"user_id":"u1","display_name":"Marieke","avatar_url":null,"country":"NL",
         "created_at":"2026-09-01","followers":3,"following":1,"ambassador":["Baarn"],
         "visited":["brn_001","brn_002"],"saves":["brn_003"],
         "approved":["brn_001"],
         "own":[{"id":"6f1a2b3c-4d5e-4f60-8a71-92b3c4d5e6f7","name":"","species":"Pedunculate Oak (Quercus robur)",
                 "photo":"u1/6F1A2B3C-4D5E-4F60-8A71-92B3C4D5E6F7.jpg","lat":52.21,"lng":5.28},
                {"id":"not-a-uuid","name":"Lime","species":null,"photo":null,"lat":null,"lng":null}]}
    """.trimIndent()

    @Test fun withoutTheNewKeysTheListsAreEmpty() {
        val p = Profiles.parsePublicProfile(before)
        assertNotNull(p)
        assertEquals(listOf("brn_001", "brn_002"), p!!.visited)
        assertEquals(emptyList<String>(), p.approved)
        assertEquals(emptyList<Profiles.OwnTree>(), p.own)
    }

    @Test fun withTheNewKeysApprovedAndOwnDecode() {
        val p = Profiles.parsePublicProfile(after)!!
        assertEquals(listOf("brn_001"), p.approved)
        assertEquals(2, p.own.size)
        val oak = p.own[0]
        assertEquals("Pedunculate Oak", oak.title)
        assertTrue(oak.opens)
        assertEquals("https://ancienttrees.app/t?id=6f1a2b3c-4d5e-4f60-8a71-92b3c4d5e6f7", oak.url)
        assertEquals(Supa.URL_BASE + "/storage/v1/object/public/shared-sightings/u1/6F1A2B3C-4D5E-4F60-8A71-92B3C4D5E6F7.jpg", oak.photoUrl)
        assertEquals(52.21, oak.lat!!, 0.0)
        val lime = p.own[1]
        assertEquals("Lime", lime.title)
        assertFalse(lime.opens)
        assertNull(lime.photoUrl)
        assertNull(lime.lat)
    }

    @Test fun aMalformedOwnListNeverHidesTheProfile() {
        val p = Profiles.parsePublicProfile(before.replace("\"saves\":[\"brn_003\"]", "\"saves\":[\"brn_003\"],\"own\":\"oops\",\"approved\":null"))!!
        assertEquals(emptyList<Profiles.OwnTree>(), p.own)
        assertEquals(emptyList<String>(), p.approved)
    }
}
