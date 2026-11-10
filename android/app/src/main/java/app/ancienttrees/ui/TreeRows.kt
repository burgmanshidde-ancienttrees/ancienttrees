// The pieces of a place's list, ported from ios Screens/TreeRow.swift and
// TreeCard.swift (direction C, Hidde 2026-11-05: "i like option c"): the
// Highlights shelf of photograph cards, then every tree as a compact row with a
// small square on the left, a tree without a photograph drawn as the pale moss
// tint with its species in it. Plus the tapped pin's card (TreePlaceSheet.swift).

package app.ancienttrees.ui

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.compositionLocalOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asComposePath
import androidx.compose.ui.graphics.drawscope.scale
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.graphics.PathParser
import app.ancienttrees.feed.Tree
import app.ancienttrees.map.SpeciesIcons

/** What a tree's marks read and what the bookmark does, from the screen that owns the account. */
data class TreeMarks(
    val saved: Set<String> = emptySet(),
    val collected: Set<String> = emptySet(),
    val onSave: (Tree) -> Unit = {},
)

val LocalTreeMarks = compositionLocalOf { TreeMarks() }

/** Style.swift's leafTile: the photograph's stand-in, moss to sage, top left to bottom right. */
@Composable
fun leafTile(): Brush {
    val dark = Brand.colors.ground.red < 0.5f
    return Brush.linearGradient(
        if (dark) listOf(Color(0xFF2A3A1C), Color(0xFF1E2A16)) else listOf(Color(0xFF3A5222), Color(0xFF597A4D)),
    )
}

/** The species silhouette (SpeciesMark), from the same shapes the pins draw. */
@Composable
fun SpeciesMark(species: String, color: Color, modifier: Modifier = Modifier) {
    val shape = remember(species) { SpeciesIcons.archetype(species.substringBefore("(").trim()) }
    val parts = SpeciesIcons.icons[shape].orEmpty()
    Canvas(modifier) {
        scale(size.width / 40f, size.height / 40f, pivot = androidx.compose.ui.geometry.Offset.Zero) {
            for (part in parts) {
                val c = color.copy(alpha = color.alpha * part.alpha)
                when (part) {
                    is SpeciesIcons.Part.Oval -> drawOval(
                        c,
                        topLeft = androidx.compose.ui.geometry.Offset(part.left, part.top),
                        size = androidx.compose.ui.geometry.Size(part.right - part.left, part.bottom - part.top),
                    )
                    is SpeciesIcons.Part.Shape -> {
                        val p = runCatching { PathParser.createPathFromPathData(part.d) }.getOrNull() ?: continue
                        val m = android.graphics.Matrix()
                        part.rotate?.let { m.setRotate(it[0], it[1], it[2]) }
                        part.translate?.let { m.setTranslate(it[0], it[1]) }
                        p.transform(m)
                        drawPath(p.asComposePath(), c)
                    }
                }
            }
        }
    }
}

/** "Silky Oak" or "Silky Oak · 100 years". */
@Composable
fun TreeMetaLine(tree: Tree, size: Int = 13, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    val age = tree.cardAge
    Text(
        if (age != null) "${tree.commonName}  ·  $age" else tree.commonName,
        fontSize = size.sp,
        color = brand.inkSoft,
        maxLines = 1,
        overflow = TextOverflow.Ellipsis,
        modifier = modifier,
    )
}

/** "Highlights", "All 58 trees": the list's section heads. */
@Composable
fun SheetSectionHead(title: String) {
    Text(
        title,
        fontFamily = BrandFace,
        fontWeight = FontWeight.Bold,
        fontSize = 19.sp,
        color = Brand.colors.ink,
        modifier = Modifier.fillMaxWidth().padding(top = 6.dp).semantics { heading() },
    )
}

/** The small eyebrow heading (Style.swift .eyebrow, uppercase, tracked). */
@Composable
fun Eyebrow(text: String, modifier: Modifier = Modifier) {
    Text(
        text.uppercase(),
        fontFamily = BrandFace,
        fontWeight = FontWeight.Bold,
        fontSize = 11.sp,
        letterSpacing = 0.8.sp,
        color = Brand.colors.inkSoft,
        modifier = modifier,
    )
}

/** The bookmark on a card (SaveHeart): over a photograph, or bare at the end of a row. */
@Composable
fun SaveMark(tree: Tree, onPhoto: Boolean) {
    val marks = LocalTreeMarks.current
    val on = tree.id in marks.saved
    val brand = Brand.colors
    val label = if (on) "Saved ${tree.name}. Tap to remove" else "Save ${tree.name}"
    Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier
            .size(44.dp)
            .clickable(interactionSource = remember { MutableInteractionSource() }, indication = null, role = Role.Button) { marks.onSave(tree) }
            .semantics { contentDescription = label },
    ) {
        if (onPhoto) {
            Box(Modifier.size(33.dp).background(Color.Black.copy(alpha = 0.38f), CircleShape), contentAlignment = Alignment.Center) {
                Icon(if (on) Icons.Filled.Bookmark else Icons.Outlined.BookmarkBorder, null, tint = Color.White, modifier = Modifier.size(17.dp))
            }
        } else {
            Icon(
                if (on) Icons.Filled.Bookmark else Icons.Outlined.BookmarkBorder,
                null,
                tint = if (on) brand.moss else brand.inkSoft,
                modifier = Modifier.size(22.dp),
            )
        }
    }
}

/** The white "Collected" tag on a photograph (SeenTag). */
@Composable
fun SeenTag() {
    val brand = Brand.colors
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(4.dp),
        modifier = Modifier
            .shadow(2.dp, RoundedCornerShape(50))
            .background(Color.White, RoundedCornerShape(50))
            .border(1.dp, Color.Black.copy(alpha = 0.06f), RoundedCornerShape(50))
            .padding(horizontal = 10.dp, vertical = 5.dp),
    ) {
        Icon(Icons.Filled.CheckCircle, null, tint = brand.canopy, modifier = Modifier.size(13.dp))
        Text("Collected", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = brand.canopy)
    }
}

/** One tree in "All trees". */
@Composable
fun TreeRow(tree: Tree, onOpen: () -> Unit) {
    val brand = Brand.colors
    val marks = LocalTreeMarks.current
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .fillMaxWidth()
            .clickable(interactionSource = remember { MutableInteractionSource() }, indication = null, onClick = onOpen)
            .padding(vertical = 10.dp),
    ) {
        Box(Modifier.size(64.dp)) {
            Box(Modifier.fillMaxSize().clip(RoundedCornerShape(10.dp)).background(brand.mossTint), contentAlignment = Alignment.Center) {
                val photo = tree.photo
                if (photo != null) {
                    RemoteImage(photo.card, null, Modifier.fillMaxSize())
                } else {
                    SpeciesMark(tree.species, brand.moss, Modifier.size(30.dp))
                }
            }
            if (tree.id in marks.collected) {
                Box(
                    Modifier.align(Alignment.BottomEnd).offset(4.dp, 4.dp).size(18.dp).background(Color.White, CircleShape),
                    contentAlignment = Alignment.Center,
                ) {
                    Icon(Icons.Filled.CheckCircle, "Collected", tint = brand.canopy, modifier = Modifier.size(18.dp))
                }
            }
        }
        Spacer(Modifier.width(12.dp))
        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(
                tree.name,
                fontFamily = BrandFace,
                fontWeight = FontWeight.Bold,
                fontSize = 16.sp,
                color = brand.ink,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
                lineHeight = 20.sp,
            )
            TreeMetaLine(tree)
        }
        Spacer(Modifier.width(4.dp))
        SaveMark(tree, onPhoto = false)
    }
    Box(Modifier.fillMaxWidth().height(1.dp).background(brand.hairline))
}

/** One card on the Highlights shelf. */
@Composable
fun HighlightCard(tree: Tree, onOpen: () -> Unit) {
    val brand = Brand.colors
    val marks = LocalTreeMarks.current
    Column(
        Modifier
            .width(220.dp)
            .clickable(interactionSource = remember { MutableInteractionSource() }, indication = null, onClick = onOpen),
    ) {
        Box(Modifier.size(220.dp, 150.dp).clip(RoundedCornerShape(12.dp)).background(leafTile())) {
            tree.photo?.let { RemoteImage(it.card, null, Modifier.fillMaxSize()) }
            Box(Modifier.align(Alignment.TopEnd).padding(2.dp)) { SaveMark(tree, onPhoto = true) }
            if (tree.id in marks.collected) Box(Modifier.align(Alignment.TopStart).padding(8.dp)) { SeenTag() }
        }
        Text(
            tree.name + "\n",
            fontFamily = BrandFace,
            fontWeight = FontWeight.Bold,
            fontSize = 15.sp,
            color = brand.ink,
            maxLines = 2,
            minLines = 2,
            overflow = TextOverflow.Ellipsis,
            lineHeight = 19.sp,
            modifier = Modifier.padding(top = 8.dp),
        )
        TreeMetaLine(tree, size = 12, modifier = Modifier.padding(top = 3.dp))
    }
}

/**
 * A tapped pin's card (TreePlaceBody: TreeCard with no text): the photograph
 * 190 high, rounded 14, a hairline round it, the bookmark and the Collected tag.
 */
@Composable
fun TreePlaceBody(tree: Tree, onOpen: () -> Unit) {
    val brand = Brand.colors
    val marks = LocalTreeMarks.current
    val shape = RoundedCornerShape(14.dp)
    Box(
        Modifier
            .padding(horizontal = 16.dp)
            .fillMaxWidth()
            .height(190.dp)
            .clip(shape)
            .background(leafTile())
            .border(1.dp, brand.hairline, shape)
            .clickable(interactionSource = remember { MutableInteractionSource() }, indication = null, onClick = onOpen),
    ) {
        val photo = tree.photo
        if (photo != null) {
            RemoteImage(photo.card, null, Modifier.fillMaxSize())
        } else {
            Column(Modifier.align(Alignment.Center), horizontalAlignment = Alignment.CenterHorizontally) {
                SpeciesMark(tree.species, Color.White.copy(alpha = 0.9f), Modifier.size(66.dp))
                Spacer(Modifier.height(8.dp))
                Text(tree.commonName, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = Color.White)
                Text("No photograph yet", fontSize = 11.sp, color = Color.White.copy(alpha = 0.75f))
            }
        }
        Box(Modifier.align(Alignment.TopEnd).padding(6.dp)) { SaveMark(tree, onPhoto = true) }
        if (tree.id in marks.collected) Box(Modifier.align(Alignment.TopStart).padding(10.dp)) { SeenTag() }
    }
}

