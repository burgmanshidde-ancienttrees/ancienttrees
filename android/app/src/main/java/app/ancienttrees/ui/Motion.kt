// HOW THE IPHONE APP MOVES, in one place (audit 2026-11-10, out/parity-feel/).
//
// Airbnb's line (Hidde, 2026-11-10; CONVENTIONS.md "One app on iPhone and
// Android"): every motion is the iPhone's, the system's reflexes are Android's.
// So the press is Material's ripple clipped to the button's shape and lists
// keep Android's stretch (off over the tree page's hero); what lives here is
// the iPhone's:
//
// - Haptics: exactly three (ContentView.swift:668 light impact when a tree is
//   near, SaveHeart.swift:50 selection on save, MapTab.swift:1020 success when
//   a tree is collected).
// - Springs: SwiftUI's .snappy (CollectSheet.swift) is duration 0.5, bounce
//   0.15; UIKit's push and pop is a critically damped spring of about half a
//   second.

package app.ancienttrees.ui

import android.os.Build
import android.view.HapticFeedbackConstants
import android.view.View
import androidx.compose.animation.core.CubicBezierEasing
import androidx.compose.animation.core.SpringSpec
import androidx.compose.animation.core.spring

object Motion {
    /** SwiftUI's .snappy: duration 0.5, bounce 0.15 (CollectSheet.swift's steps). */
    fun <T> snappy(): SpringSpec<T> = spring(dampingRatio = 0.85f, stiffness = 158f)

    /** UIKit's navigation push and pop: critically damped, about half a second. */
    fun <T> push(): SpringSpec<T> = spring(dampingRatio = 1f, stiffness = 158f)

    /** SwiftUI's .easeOut, for the 0.12 s press and the 0.2 s fades. */
    val EaseOut = CubicBezierEasing(0f, 0f, 0.58f, 1f)
    val EaseInOut = CubicBezierEasing(0.42f, 0f, 0.58f, 1f)
}

// ---------------------------------------------------------------- haptics

/** The iPhone's three (ContentView.swift:668, SaveHeart.swift:50, MapTab.swift:1020). */
object Haptics {
    /** .selection: a save toggled. */
    fun selection(view: View) {
        view.performHapticFeedback(
            if (Build.VERSION.SDK_INT >= 34) HapticFeedbackConstants.SEGMENT_TICK else HapticFeedbackConstants.CLOCK_TICK,
        )
    }

    /** .success: a tree collected. */
    fun success(view: View) {
        view.performHapticFeedback(
            if (Build.VERSION.SDK_INT >= 30) HapticFeedbackConstants.CONFIRM else HapticFeedbackConstants.LONG_PRESS,
        )
    }

    /** .impact(weight: .light): a tree is near. */
    fun light(view: View) {
        view.performHapticFeedback(
            if (Build.VERSION.SDK_INT >= 27) HapticFeedbackConstants.KEYBOARD_TAP else HapticFeedbackConstants.VIRTUAL_KEY,
        )
    }
}
