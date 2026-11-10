// The bottom bar, ported from ios Screens/TabBar.swift, where the rulings live:
// three places in a floating grey capsule (Map, Discover, My trees), the selected
// one with a light pill behind it and a filled glyph, monochrome (Hidde,
// 2026-08-26), and the deed on its own disc beside it, the same height, a camera
// and never a plus, with no word under it (2026-08-24, 2026-08-26).
//
// ANDROID-FORCED DIFFERENCES (listed on the parity page):
// - Glyphs are Material Symbols, the Android counterpart of SF Symbols: map, search,
//   eco (the leaf) and photo_camera. We never draw icons.
// - No system material blur behind the bar: Compose has none for what lies under a
//   view, so the grey glass is the ground at 92 percent with the iPhone's 6 percent
//   ink wash on top.

package app.ancienttrees.ui

import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.requiredSize
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R

object TabBar {
    /** The disc's own 58 plus the gap under it: how deep the bar floats over what is behind it. */
    val floatDepth = 58.dp + 4.dp

    /** The collect deed's tag: not a tab, intercepted, as on the iPhone. */
    const val COLLECT = 3
}

private data class TabItem(val title: Int, val outline: ImageVector, val filled: ImageVector)

/** The iPhone's accessibility identifiers, so the walk names the same controls. */
private val TAB_TAGS = listOf("tab-map", "tab-discover", "tab-my-trees")

private val ITEMS = listOf(
    TabItem(R.string.tab_map, Sym.Map, Sym.MapFill),
    TabItem(R.string.tab_discover, Sym.Search, Sym.Search),
    TabItem(R.string.tab_my_trees, Sym.Eco, Sym.EcoFill),
)

@Composable
fun TabBar(selected: Int, select: (Int) -> Unit, collect: () -> Unit, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    // OPAQUE, measured off the iPhone's shots (2026-11-10): its regularMaterial
    // is frosted to near-opaque, so nothing behind it is legible; Android has no
    // blur, and at 92 percent the rows under the bar read straight through it.
    val glass = brand.ground
    val wash = brand.ink.copy(alpha = 0.14f)
    val edge = Color.White.copy(alpha = 0.25f)
    Row(
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        verticalAlignment = Alignment.CenterVertically,
        // 16, so the first icon lines up with the 20 every page starts its content at.
        modifier = modifier.fillMaxWidth().navigationBarsPadding().padding(horizontal = 16.dp).padding(bottom = 4.dp),
    ) {
        BoxWithConstraints(
            Modifier
                .weight(1f)
                .shadow(10.dp, CircleShape, ambientColor = Color.Black.copy(alpha = 0.10f), spotColor = Color.Black.copy(alpha = 0.10f))
                .background(glass, CircleShape)
                .background(wash, CircleShape)
                .border(0.5.dp, edge, CircleShape)
                .padding(4.dp),
        ) {
            // THE PILL IS ONE VIEW THAT MOVES (Hidde, 2026-08-26): it slides
            // between items rather than fading in and out, as iOS does.
            val itemWidth = (maxWidth - 4.dp * (ITEMS.size - 1)) / ITEMS.size
            val x by animateDpAsState((itemWidth + 4.dp) * selected, tween(280), label = "tab-pill")
            Box(
                Modifier
                    .offset(x = x)
                    .width(itemWidth)
                    .height(50.dp)
                    .shadow(3.dp, CircleShape, ambientColor = Color.Black.copy(alpha = 0.06f), spotColor = Color.Black.copy(alpha = 0.06f))
                    .background(brand.ground, CircleShape),
            )
            Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                ITEMS.forEachIndexed { i, item ->
                    val on = i == selected
                    val title = stringResource(item.title)
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center,
                        modifier = Modifier
                            .width(itemWidth)
                            .height(50.dp)
                            .clickable(
                                interactionSource = remember { MutableInteractionSource() },
                                indication = null,
                                role = Role.Tab,
                            ) { select(i) }
                            .semantics { this.selected = on }
                            .testTag(TAB_TAGS[i]),
                    ) {
                        // SF 21 point in a 24 high frame: a symbol of the set reads as
                        // large as an SF Symbol at four thirds of its point size.
                        Box(Modifier.height(24.dp), contentAlignment = Alignment.Center) {
                            Icon(
                                if (on) item.filled else item.outline,
                                contentDescription = null,
                                tint = if (on) brand.ink else brand.inkSoft.copy(alpha = 0.8f),
                                modifier = Modifier.requiredSize(28.dp),
                            )
                        }
                        Spacer(Modifier.height(3.dp))
                        Text(
                            title,
                            fontSize = 11.sp,
                            fontWeight = if (on) FontWeight.SemiBold else FontWeight.Normal,
                            color = if (on) brand.ink else brand.inkSoft.copy(alpha = 0.8f),
                            maxLines = 1,
                        )
                    }
                }
            }
        }

        // The deed, on its own disc, the same height as the bar. Its glyph sits
        // lower than the tab icons on purpose (Hidde, 2026-09-13): do not "fix" it.
        val collectLabel = stringResource(R.string.collect_a_tree)
        Box(
            contentAlignment = Alignment.Center,
            modifier = Modifier
                .size(58.dp)
                .shadow(10.dp, CircleShape, ambientColor = Color.Black.copy(alpha = 0.10f), spotColor = Color.Black.copy(alpha = 0.10f))
                .background(glass, CircleShape)
                .background(wash, CircleShape)
                .border(0.5.dp, edge, CircleShape)
                .testTag("tab-collect")
                .clickable(role = Role.Button, onClick = collect)
                .semantics { contentDescription = collectLabel },
        ) {
            Icon(Sym.PhotoCameraFillSemibold, contentDescription = null, tint = brand.ink, modifier = Modifier.size(28.dp))
        }
    }
}
