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
import androidx.compose.ui.text.font.FontWeight
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
        MaterialTheme(colorScheme = if (dark) Dark else Light, content = content)
    }
}
