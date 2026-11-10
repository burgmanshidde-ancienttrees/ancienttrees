// ONE SHEET FOR EVERY QUESTION, ported from ios Kit/BrandSheet.swift (CLAUDE.md,
// "One sheet for every overlay"): an icon tile, the title in the brand face at 26
// centred, one line under it, then capsule buttons 12 apart, a footnote, and the
// grey close circle top right. The sheet itself is Android's modal bottom sheet
// (data/android-parity.json: system sheets are the platform's on both phones).

package app.ancienttrees.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R

/** SheetButton.Kind: what a button in a sheet looks like. */
enum class SheetKind { PRIMARY, SECONDARY, DESTRUCTIVE, DESTRUCTIVE_QUIET, QUIET }

data class SheetButton(
    val label: String,
    val kind: SheetKind = SheetKind.SECONDARY,
    val icon: ImageVector? = null,
    val action: () -> Unit,
)

/** SheetButtonStyle: a capsule the width of the sheet, 48 high (44 for the quiet two). */
@Composable
fun SheetButtonView(b: SheetButton, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    val quiet = b.kind == SheetKind.QUIET || b.kind == SheetKind.DESTRUCTIVE_QUIET
    val fg = when (b.kind) {
        SheetKind.PRIMARY -> brand.onMoss
        SheetKind.SECONDARY -> brand.ink
        SheetKind.DESTRUCTIVE -> Color.White
        SheetKind.DESTRUCTIVE_QUIET -> brand.dangerText
        SheetKind.QUIET -> brand.inkSoft
    }
    val bg = when (b.kind) {
        SheetKind.PRIMARY -> brand.moss
        SheetKind.SECONDARY -> brand.creamDark
        SheetKind.DESTRUCTIVE -> brand.danger
        else -> Color.Transparent
    }
    Row(
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically,
        modifier = modifier
            .fillMaxWidth()
            .height(if (quiet) 44.dp else 48.dp)
            .background(bg, RoundedCornerShape(50))
            .clickable(role = Role.Button, onClick = b.action),
    ) {
        b.icon?.let {
            Icon(it, null, tint = fg, modifier = Modifier.size(18.dp))
            Spacer(Modifier.width(8.dp))
        }
        Text(b.label, color = fg, fontSize = if (quiet) 15.sp else 16.sp, fontWeight = FontWeight.SemiBold)
    }
}

/** SheetIconTile: the glyph on the moss tint, 56 square, radius 14. */
@Composable
fun SheetIconTile(icon: ImageVector, tint: Color? = null, ground: Color? = null) {
    val brand = Brand.colors
    Box(
        Modifier.size(56.dp).background(ground ?: brand.mossTint, RoundedCornerShape(14.dp)),
        contentAlignment = Alignment.Center,
    ) {
        Icon(icon, null, tint = tint ?: brand.moss, modifier = Modifier.size(26.dp))
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BrandSheet(
    title: String,
    onDismiss: () -> Unit,
    buttons: List<SheetButton>,
    icon: ImageVector? = null,
    message: String? = null,
    footnote: String? = null,
    /** BrandSheet.swift `points`: what a choice shows, one checked line each. */
    points: List<String> = emptyList(),
    /** BrandSheet.swift `tint: .gold`, the early-adopter sheet's tile. */
    iconTint: Color? = null,
    iconGround: Color? = null,
    extra: @Composable ColumnScope.() -> Unit = {},
) {
    val brand = Brand.colors
    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true),
        containerColor = brand.ground,
    ) {
        Box {
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                modifier = Modifier
                    .fillMaxWidth()
                    .verticalScroll(rememberScrollState())
                    .padding(horizontal = 24.dp)
                    .padding(top = 12.dp, bottom = 16.dp)
                    .navigationBarsPadding(),
            ) {
                icon?.let {
                    SheetIconTile(it, iconTint, iconGround)
                    Spacer(Modifier.height(16.dp))
                }
                Text(
                    title,
                    fontFamily = BrandFace,
                    fontWeight = FontWeight.Bold,
                    fontSize = 26.sp,
                    lineHeight = 31.sp,
                    color = brand.ink,
                    textAlign = TextAlign.Center,
                    modifier = Modifier.padding(horizontal = 18.dp).semantics { heading() },
                )
                message?.let {
                    Text(
                        it,
                        fontSize = 15.sp,
                        color = brand.inkSoft,
                        textAlign = TextAlign.Center,
                        modifier = Modifier.padding(top = 8.dp),
                    )
                }
                if (points.isNotEmpty()) SheetPoints(points)
                extra()
                Column(
                    verticalArrangement = Arrangement.spacedBy(12.dp),
                    modifier = Modifier.fillMaxWidth().padding(top = 22.dp),
                ) {
                    for (b in buttons) SheetButtonView(b)
                }
                footnote?.let {
                    Text(
                        it,
                        fontSize = 13.sp,
                        color = brand.inkSoft,
                        textAlign = TextAlign.Center,
                        modifier = Modifier.padding(top = 14.dp),
                    )
                }
            }
            SheetCloseButton(onDismiss, Modifier.align(Alignment.TopEnd))
        }
    }
}

/** SheetCloseButton: a 30 point grey circle with the cross, in a 48 point target. */
@Composable
fun SheetCloseButton(onClick: () -> Unit, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    val label = stringResource(R.string.close)
    Box(
        contentAlignment = Alignment.Center,
        modifier = modifier
            .padding(end = 10.dp)
            .size(48.dp)
            .clickable(role = Role.Button, onClick = onClick)
            .semantics { contentDescription = label },
    ) {
        Box(Modifier.size(30.dp).background(brand.surfaceMuted, CircleShape), contentAlignment = Alignment.Center) {
            Icon(Icons.Filled.Close, null, tint = brand.inkSoft, modifier = Modifier.size(15.dp))
        }
    }
}

/** BrandSheet.swift's points: a check in moss and the line, left-aligned under the message. */
@Composable
private fun SheetPoints(points: List<String>) {
    val brand = Brand.colors
    Column(
        verticalArrangement = Arrangement.spacedBy(10.dp),
        modifier = Modifier.fillMaxWidth().padding(top = 18.dp),
    ) {
        for (p in points) {
            Row(verticalAlignment = Alignment.Top) {
                Icon(androidx.compose.material.icons.Icons.Filled.Check, null, tint = brand.moss, modifier = Modifier.size(16.dp).padding(top = 2.dp))
                Spacer(Modifier.width(10.dp))
                Text(p, fontSize = 15.sp, color = brand.ink)
            }
        }
    }
}
