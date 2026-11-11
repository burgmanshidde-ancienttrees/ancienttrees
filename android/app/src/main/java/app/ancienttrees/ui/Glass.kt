// THE IPHONE'S FROSTED GROUND (.regularMaterial, iOS 26's glass) behind the
// floating controls: the tab bar and its camera disc (TabBar.swift:158-205) and
// the round buttons over the tree's photograph (TreeDetail.swift:805).
//
// A real backdrop blur, from Haze (dev.chrisbanes.haze 1.7.2, built against the
// Compose 1.10 and Kotlin 2.2.21 this app uses; hard list 5: a library that makes
// the product better is simply used). Haze blurs what a `glassSource` layer drew
// under the control with Android 12's RenderEffect. Below Android 12 there is no
// RenderEffect, so the control keeps the opaque ground it had.
//
// What it cannot blur is the map: MapLibre draws on its own GL surface, which no
// Android view can sample. Over the map tab the bar frosts the sheet under it, and
// where the map itself shows through, the ground's tint carries it.

package app.ancienttrees.ui

import android.os.Build
import androidx.compose.foundation.background
import androidx.compose.runtime.Composable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Shape
import androidx.compose.ui.unit.dp
import dev.chrisbanes.haze.HazeState
import dev.chrisbanes.haze.HazeStyle
import dev.chrisbanes.haze.HazeTint
import dev.chrisbanes.haze.hazeEffect
import dev.chrisbanes.haze.hazeSource

/** Whether this phone can blur what lies behind a view (RenderEffect, API 31). */
val GlassAvailable: Boolean get() = Build.VERSION.SDK_INT >= Build.VERSION_CODES.S

/** The layer the floating tab bar frosts: each tab's root draws into it. */
val LocalBarGlass = staticCompositionLocalOf<HazeState?> { null }

/** Draw this into [state], so a glass control over it can blur it. */
fun Modifier.glassSource(state: HazeState?): Modifier =
    if (state != null && GlassAvailable) this.hazeSource(state) else this

/**
 * The material, clipped to [shape]: a blur of what [state] drew behind, under the
 * ground at [tint] (regularMaterial's milky white over the blur). Without a blur,
 * [fallback] as before.
 */
@Composable
fun Modifier.glass(state: HazeState?, shape: Shape, fallback: Color, tint: Float = GLASS_TINT): Modifier {
    val ground = Brand.colors.ground
    return if (state != null && GlassAvailable) {
        this.clip(shape).hazeEffect(
            state,
            HazeStyle(
                backgroundColor = ground,
                tint = HazeTint(ground.copy(alpha = tint)),
                blurRadius = GLASS_BLUR.dp,
                noiseFactor = 0f,
            ),
        )
    } else {
        this.background(fallback, shape)
    }
}

/** Tuned against the iPhone's tab bar over the same list (out/parity, 2026-11-11). */
const val GLASS_BLUR = 24f
const val GLASS_TINT = 0.72f
