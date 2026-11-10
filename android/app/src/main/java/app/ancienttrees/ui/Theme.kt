// The palette of ios Kit/Style.swift.

package app.ancienttrees.ui

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.sp
import app.ancienttrees.R

private val Light = lightColorScheme(
    primary = Color(0xFF4A6B2A),
    onPrimary = Color(0xFFFFFFFF),
    background = Color(0xFFFFFFFF),
    onBackground = Color(0xFF26301E),
    surface = Color(0xFFFFFFFF),
    onSurface = Color(0xFF26301E),
    onSurfaceVariant = Color(0xFF5C6350),
    surfaceVariant = Color(0xFFEDF3E3),
)

private val Dark = darkColorScheme(
    primary = Color(0xFF96B863),
    onPrimary = Color(0xFF10160A),
    background = Color(0xFF1A1D18),
    onBackground = Color(0xFFECEFE4),
    surface = Color(0xFF1A1D18),
    onSurface = Color(0xFFECEFE4),
    onSurfaceVariant = Color(0xFFA7AE9E),
    surfaceVariant = Color(0xFF26301E),
)

/** The display face, Gabarito, as on the iPhone and the website (OFL, android/FONT-LICENSE-OFL.txt). */
val BrandFace = FontFamily(
    Font(R.font.gabarito_regular, FontWeight.Normal),
    Font(R.font.gabarito_medium, FontWeight.Medium),
    Font(R.font.gabarito_bold, FontWeight.Bold),
)

/**
 * The text face: Inter (OFL, android/FONT-LICENSE-INTER-OFL.txt), the open face
 * closest to SF Pro, which Apple licenses for its own platforms only. Every text
 * that is not Gabarito sets in it, tracked as SF tracks (Text.kt).
 */
val TextFace = FontFamily(
    Font(R.font.inter_regular, FontWeight.Normal),
    Font(R.font.inter_medium, FontWeight.Medium),
    Font(R.font.inter_semibold, FontWeight.SemiBold),
    Font(R.font.inter_bold, FontWeight.Bold),
)

/**
 * Material's type scale with Inter in every style and SwiftUI's line: the
 * font's own line height and no added letter spacing (Text.kt adds SF's). The
 * default text is SwiftUI's .body, 17.
 */
private val Type = androidx.compose.material3.Typography().run {
    fun TextStyle.sf() = copy(
        fontFamily = TextFace,
        letterSpacing = TextUnit.Unspecified,
        lineHeight = TextUnit.Unspecified,
    )
    copy(
        displayLarge = displayLarge.sf(), displayMedium = displayMedium.sf(), displaySmall = displaySmall.sf(),
        headlineLarge = headlineLarge.sf(), headlineMedium = headlineMedium.sf(), headlineSmall = headlineSmall.sf(),
        titleLarge = titleLarge.sf(), titleMedium = titleMedium.sf(), titleSmall = titleSmall.sf(),
        bodyLarge = bodyLarge.sf().copy(fontSize = 17.sp), bodyMedium = bodyMedium.sf(), bodySmall = bodySmall.sf(),
        labelLarge = labelLarge.sf(), labelMedium = labelMedium.sf(), labelSmall = labelSmall.sf(),
    )
}

/** The iPhone's Brand palette (BrandColors.kt, generated from Style.swift). */
val LocalBrand = staticCompositionLocalOf { LightBrand }

object Brand {
    val colors: BrandColors
        @Composable get() = LocalBrand.current
}

@Composable
fun AncientTreesTheme(content: @Composable () -> Unit) {
    val dark = isSystemInDarkTheme()
    CompositionLocalProvider(LocalBrand provides if (dark) DarkBrand else LightBrand) {
        MaterialTheme(colorScheme = if (dark) Dark else Light, typography = Type, content = content)
    }
}

/**
 * SwiftUI's text: the font's own line height and no added tracking. Material's
 * body style adds 0.5 sp of letter spacing and a 24 sp line, which made every
 * ported line wider and taller than the iPhone's (tree page parity, 2026-11-10).
 */
@Composable
fun PlainText(content: @Composable () -> Unit) {
    CompositionLocalProvider(
        androidx.compose.material3.LocalTextStyle provides androidx.compose.material3.LocalTextStyle.current.copy(
            lineHeight = androidx.compose.ui.unit.TextUnit.Unspecified,
            letterSpacing = androidx.compose.ui.unit.TextUnit.Unspecified,
        ),
        content = content,
    )
}
