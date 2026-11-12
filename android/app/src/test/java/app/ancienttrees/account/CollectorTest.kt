package app.ancienttrees.account

import org.junit.Assert.assertEquals
import org.junit.Test
import java.util.Date

class CollectorTest {

    private val noon = Date(1_762_776_000_000) // 2025-11-10 12:00 UTC

    @Test fun theRowCarriesTheIphonesKeysAndWhereThePhoneStood() {
        val r = Collector.row("u1", "ID-1", "lis_001", "The Ajuda Dragon Tree", 38.7, -9.2, "u1/ID-1.jpg", noon)
        assertEquals(
            setOf("user_id", "id", "tree_id", "name", "note", "lat", "lng", "taken_at", "status", "updated_at", "shared", "photo", "client"),
            r.keys().asSequence().toSet(),
        )
        assertEquals("android", r.getString("client"))
        assertEquals("mine", r.getString("status"))
        assertEquals(true, r.getBoolean("shared"))
        assertEquals(38.7, r.getDouble("lat"), 0.0)
        assertEquals("u1/ID-1.jpg", r.getString("photo"))
        assertEquals("2025-11-10T12:00:00Z", r.getString("taken_at"))
    }

    @Test fun theVisitIsADay() {
        assertEquals(10, Collector.day(noon).length)
    }
}
