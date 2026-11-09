// The Airbnb rule in numbers (CLAUDE.md, "Maps draw pins the Airbnb way"): the
// same as site/src/lib/map.ts and ios TreeMap.swift. PinRulesTest holds them equal
// to the website's.

package app.ancienttrees.map

object PinRules {
    const val PIN_SIZE = 38f
    const val PIN_DISTANCE = 40f
    const val FAR_ZOOM = 6.5f
    const val FAR_PIN_DISTANCE = 90f
    const val MINI_RADIUS = 3f
    const val WORLD_MIN_ZOOM = 1.5

    /** Half the room two pin centres must keep beyond the pin itself. */
    fun padding(distance: Float): Float = (distance - PIN_SIZE) / 2

    /** Which tree gets the full pin where two collide, lower first: a photograph, then readers' saves. */
    fun priority(hasPhoto: Boolean, saves: Int): Int =
        (if (hasPhoto) 0 else 100_000) - saves.coerceIn(0, 99_999)
}
