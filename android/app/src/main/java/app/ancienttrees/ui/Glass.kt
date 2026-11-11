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
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Icon
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
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

// ---------------------------------------------------------------- iOS 26 bars
// The visual review of 2026-11-11 (out/parity-feel/visual-review-2026-11-11.md):
// iOS 26 draws a NavigationStack's bar buttons as white capsules with a soft
// shadow (Cancel, Save, Close, Done), its back button in a white circle, and
// fades the content that slides under the bar at the top of a page (the soft
// scroll edge). The shapes are the iPhone's; back keeps Android's arrow.

/** A bar's text button in its capsule: Cancel, Save, Close, Done. */
@Composable
fun BarCapsule(
    label: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    bold: Boolean = false,
    height: androidx.compose.ui.unit.Dp = 44.dp,
) {
    val brand = Brand.colors
    androidx.compose.foundation.layout.Box(
        contentAlignment = androidx.compose.ui.Alignment.Center,
        modifier = modifier
            .height(height)
            .shadow(8.dp, CircleShape, ambientColor = Color.Black.copy(alpha = 0.10f), spotColor = Color.Black.copy(alpha = 0.10f))
            .clip(CircleShape)
            .clickable(enabled = enabled, role = androidx.compose.ui.semantics.Role.Button, onClick = onClick)
            .background(brand.ground, CircleShape)
            .padding(horizontal = 16.dp),
    ) {
        Text(
            label,
            fontSize = 17.sp,
            fontWeight = if (bold) FontWeight.SemiBold else FontWeight.Normal,
            color = brand.moss.copy(alpha = if (enabled) 1f else 0.4f),
            maxLines = 1,
        )
    }
}

/** A pushed page's back button: Android's arrow in iOS 26's white circle. */
@Composable
fun BackCircle(onBack: () -> Unit, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    val label = androidx.compose.ui.res.stringResource(app.ancienttrees.R.string.back)
    androidx.compose.foundation.layout.Box(
        contentAlignment = androidx.compose.ui.Alignment.Center,
        modifier = modifier
            .size(44.dp)
            .shadow(8.dp, CircleShape, ambientColor = Color.Black.copy(alpha = 0.10f), spotColor = Color.Black.copy(alpha = 0.10f))
            .clip(CircleShape)
            .clickable(role = androidx.compose.ui.semantics.Role.Button, onClick = onBack)
            .background(brand.ground, CircleShape)
            .semantics { contentDescription = label },
    ) {
        Icon(Sym.ArrowBack, null, tint = brand.ink, modifier = Modifier.size(22.dp))
    }
}

/**
 * iOS 26's soft scroll edge over the top of a page: what lies under the status
 * bar and the buttons is blurred and lightened, strongest at the top and gone
 * by [height]. Without a blur, the ground fading out over the same height.
 */
@Composable
fun TopEdge(state: HazeState?, modifier: Modifier = Modifier, height: androidx.compose.ui.unit.Dp = 120.dp) {
    val ground = Brand.colors.ground
    val base = modifier.fillMaxWidth().height(height)
    if (state != null && GlassAvailable) {
        androidx.compose.foundation.layout.Box(
            base.hazeEffect(state) {
                backgroundColor = ground
                blurRadius = 16.dp
                noiseFactor = 0f
                tints = listOf(HazeTint(ground.copy(alpha = 0.45f)))
                progressive = dev.chrisbanes.haze.HazeProgressive.verticalGradient(startIntensity = 1f, endIntensity = 0f)
            },
        )
    } else {
        androidx.compose.foundation.layout.Box(
            base.background(
                androidx.compose.ui.graphics.Brush.verticalGradient(
                    0f to ground.copy(alpha = 0.6f),
                    1f to ground.copy(alpha = 0f),
                ),
            ),
        )
    }
}
