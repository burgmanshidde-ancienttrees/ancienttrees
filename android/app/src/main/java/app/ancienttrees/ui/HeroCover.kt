// The frame the app opens on, ported from ios Screens/HeroCover.swift and the
// cover block in ContentView.swift: a tree, the promise, and then out of the
// way. It leaves on its own after 2.4 seconds (Hidde, 2026-08-30: 1.4 was gone
// before the seven words could be read), fades in 0.4, and any tap takes it
// away at once; only on a cold start. The photograph is Heroes' pick for this
// launch, the same one Discover's stock hero wears.

package app.ancienttrees.ui

import android.content.Context
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Shadow
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R

/**
 * Heroes.swift: three photographs, a different one every launch. Which was shown
 * last is a device setting (data/cross-device.json hero.index.v1).
 */
internal object Heroes {
    private val names = listOf(R.drawable.hero_1, R.drawable.hero_2, R.drawable.hero_3)
    /** The credit a licence obliges us to show; none for CC0 or Unsplash. */
    private val credits = mapOf(2 to "Photo: Eric Kilby, CC BY-SA 2.0")
    private var current: Int? = null

    /** The one for this launch, resolved once so a redraw cannot swap it mid-scroll. */
    fun pick(context: Context): Int {
        current?.let { return it }
        val prefs = context.getSharedPreferences("device", Context.MODE_PRIVATE)
        val next = (prefs.getInt("hero.index.v1", 0) + 1) % names.size
        prefs.edit().putInt("hero.index.v1", next).apply()
        current = next
        return next
    }

    fun image(i: Int) = names[i]
    fun credit(i: Int) = credits[i]
}

@Composable
fun HeroCover(dismiss: () -> Unit) {
    val context = LocalContext.current
    val i = remember { Heroes.pick(context) }
    val shadow = Shadow(Color.Black.copy(alpha = 0.4f), Offset(0f, 2f), 20f)
    Box(
        Modifier
            .fillMaxSize()
            .background(Color.Black)
            .clickable(interactionSource = remember { MutableInteractionSource() }, indication = null, onClick = dismiss)
            .semantics { contentDescription = "Trees worth the walk, wherever you are" },
    ) {
        Image(painterResource(Heroes.image(i)), null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())
        // Dark from 60 percent down, only behind the words (2026-10-14).
        Box(
            Modifier.fillMaxSize().background(
                Brush.verticalGradient(0.6f to Color.Transparent, 0.84f to Color.Black.copy(alpha = 0.45f), 1f to Color.Black.copy(alpha = 0.68f)),
            ),
        )
        Column(
            verticalArrangement = Arrangement.spacedBy(2.dp),
            modifier = Modifier.align(Alignment.BottomStart).fillMaxWidth().padding(start = 24.dp, end = 24.dp, bottom = 110.dp),
        ) {
            Text(stringResource(R.string.discover_hero_1), style = TextStyle(shadow = shadow), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 30.sp, color = Color.White)
            Text(stringResource(R.string.discover_hero_2), style = TextStyle(shadow = shadow), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 30.sp, color = Brand.colors.gold)
        }
        Heroes.credit(i)?.let {
            Text(it, fontSize = 11.sp, color = Color.White.copy(alpha = 0.7f), modifier = Modifier.align(Alignment.BottomStart).padding(start = 24.dp, bottom = 44.dp))
        }
    }
}
