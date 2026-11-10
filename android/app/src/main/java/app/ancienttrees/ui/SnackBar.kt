// THE ONE-LINE CONFIRMATION at the bottom of the screen, ported from the iPhone's
// SnackBar (Screens/SaveHeart.swift) and Navigator.Snack (Hidde, 2026-10-10: "when
// pressing the bookmark sign a confirmation ... this tree was added to want to
// visit list would be nice"). Airbnb's "Saved to ...", Material's acknowledgement:
// one line, non-modal, gone by itself after four seconds, at most one action.
// Removing something you can get back is done at once and offers Undo.

package app.ancienttrees.ui

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.compositionLocalOf
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay

/** What the bar says and what its one action does (Navigator.Snack). */
data class Snack(
    val text: String,
    val icon: ImageVector = Sym.BookmarkFill,
    /** "View": My trees on Want to visit. */
    val onView: (() -> Unit)? = null,
    /** "Undo": puts back what was just removed. */
    val onUndo: (() -> Unit)? = null,
    val id: Long = System.nanoTime(),
)

/** Any screen posts a snack through this; the app root draws it. */
val LocalSnack = compositionLocalOf<(Snack) -> Unit> { {} }

val SignedInIcon: ImageVector = Sym.CheckCircleFill

@Composable
fun SnackBar(snack: Snack?, lift: Dp, viewLabel: String, undoLabel: String, dismiss: () -> Unit, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    LaunchedEffect(snack?.id) {
        if (snack == null) return@LaunchedEffect
        delay(4000)
        dismiss()
    }
    AnimatedVisibility(
        visible = snack != null,
        enter = slideInVertically { it } + fadeIn(),
        exit = slideOutVertically { it } + fadeOut(),
        modifier = modifier,
    ) {
        val s = snack ?: return@AnimatedVisibility
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            modifier = Modifier
                .padding(horizontal = 16.dp)
                .padding(bottom = lift)
                .fillMaxWidth()
                .defaultMinSize(minHeight = 52.dp)
                .shadow(14.dp, RoundedCornerShape(14.dp), ambientColor = Color.Black.copy(alpha = 0.16f), spotColor = Color.Black.copy(alpha = 0.16f))
                .background(brand.surface, RoundedCornerShape(14.dp))
                .border(1.dp, brand.hairline, RoundedCornerShape(14.dp))
                .padding(start = 16.dp, end = 8.dp)
                .testTag("snack"),
        ) {
            Icon(s.icon, null, tint = brand.moss, modifier = Modifier.size(20.dp))
            Text(s.text, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = brand.ink, maxLines = 2, modifier = Modifier.weight(1f))
            s.onUndo?.let { undo ->
                SnackAction(undoLabel, "snack-undo") { dismiss(); undo() }
            }
            s.onView?.let { view ->
                SnackAction(viewLabel, "snack-view") { dismiss(); view() }
            }
        }
    }
}

@Composable
private fun SnackAction(label: String, tag: String, onClick: () -> Unit) {
    Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier.defaultMinSize(minWidth = 44.dp, minHeight = 44.dp).clickable(onClick = onClick).padding(horizontal = 8.dp).testTag(tag),
    ) {
        Text(label, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = Brand.colors.moss)
    }
}

