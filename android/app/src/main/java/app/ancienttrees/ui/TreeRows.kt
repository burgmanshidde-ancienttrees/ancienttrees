// The pieces of a place's list, ported from ios Screens/TreeRow.swift and
// TreeCard.swift (direction C, Hidde 2026-11-05: "i like option c"): the
// Highlights shelf of photograph cards, then every tree as a compact row with a
// small square on the left, a tree without a photograph drawn as the pale moss
// tint with its species in it. Plus the tapped pin's card (TreePlaceSheet.swift).

package app.ancienttrees.ui

import androidx.compose.ui.platform.testTag
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
import androidx.compose.material3.Icon
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
import androidx.compose.ui.res.stringResource
import app.ancienttrees.R
import app.ancienttrees.feed.Tree
import app.ancienttrees.map.SpeciesIcons
import app.ancienttrees.map.SpeciesPath

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
    // One path, one colour, centred on its own bounds (SpeciesShape): the iPhone
    // never draws the website's half-transparent back layers.
    Canvas(modifier) {
        drawPath(SpeciesPath.fitted(shape, size.width, size.height).asComposePath(), color)
    }
}

/**
 * "Silky Oak · 100 years" (TreeMetaLine.swift): three texts 5 apart, the dot in
 * the tertiary shade of the line's colour, 13 everywhere (the iPhone's own .font(13)
 * inside wins over the card's 12 outside). The name gives way first, so a long
 * species truncates and the age stays whole: "Eastern Cape Giant C... · 300 years".
 */
@Composable
fun TreeMetaLine(tree: Tree, @Suppress("UNUSED_PARAMETER") size: Int = 13, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    val age = tree.cardAge
    // One line to a screen reader, as before: "Silky Oak · 100 years".
    Row(modifier.semantics(mergeDescendants = true) { }, horizontalArrangement = Arrangement.spacedBy(5.dp), verticalAlignment = Alignment.CenterVertically) {
        Text(
            tree.commonName,
            fontSize = 13.sp,
            color = brand.inkSoft,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.weight(1f, fill = false),
        )
        if (age != null) {
            Text("·", fontSize = 13.sp, color = brand.inkSoft.copy(alpha = brand.inkSoft.alpha * 0.3f), maxLines = 1)
            Text(age, fontSize = 13.sp, color = brand.inkSoft, maxLines = 1, softWrap = false)
        }
    }
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
    val label = if (on) stringResource(R.string.saved_tap_remove, tree.name) else stringResource(R.string.save_tree, tree.name)
    Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier
            .size(44.dp)
            .clickable(interactionSource = remember { MutableInteractionSource() }, indication = androidx.compose.foundation.LocalIndication.current, role = Role.Button) { marks.onSave(tree) }
            .semantics { contentDescription = label },
    ) {
        if (onPhoto) {
            // 15 semibold in a 0.38 black disc, padded 9 (SaveHeart .onPhoto): 20 dp, a 35 disc.
            Box(Modifier.size(35.dp).background(Color.Black.copy(alpha = 0.38f), CircleShape), contentAlignment = Alignment.Center) {
                Icon(if (on) Sym.BookmarkFillSemibold else Sym.BookmarkSemibold, null, tint = Color.White, modifier = Modifier.size(20.dp))
            }
        } else {
            Icon(
                if (on) Sym.BookmarkFill else Sym.Bookmark,
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
        Icon(Sym.CheckCircleFill, null, tint = brand.canopy, modifier = Modifier.size(13.dp))
        Text(stringResource(R.string.seen_it_done), fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = brand.canopy)
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
            .clickable(interactionSource = remember { MutableInteractionSource() }, indication = androidx.compose.foundation.LocalIndication.current, onClick = onOpen)
            // The walks find a tree card by this, as FlowWalk.swift's firstCard does.
            .testTag("tree-card")
            .padding(vertical = 10.dp),
    ) {
        Box(Modifier.size(64.dp)) {
            Box(Modifier.fillMaxSize().clip(RoundedCornerShape(10.dp)).background(brand.mossTint), contentAlignment = Alignment.Center) {
                val photo = tree.photo
                if (photo != null) {
                    // A row's thumbnail waits on the moss tint (TreeRow.swift:68).
                    RemoteImage(photo.card, null, Modifier.fillMaxSize(), fallback = { Box(Modifier.fillMaxSize().background(Brand.colors.mossTint)) })
                } else {
                    SpeciesMark(tree.species, brand.moss, Modifier.size(30.dp))
                }
            }
            if (tree.id in marks.collected) {
                Box(
                    Modifier.align(Alignment.BottomEnd).offset(4.dp, 4.dp).size(18.dp).background(Color.White, CircleShape),
                    contentAlignment = Alignment.Center,
                ) {
                    Icon(Sym.CheckCircleFill, stringResource(R.string.seen_it_done), tint = brand.canopy, modifier = Modifier.size(18.dp))
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
            .clickable(interactionSource = remember { MutableInteractionSource() }, indication = androidx.compose.foundation.LocalIndication.current, onClick = onOpen)
            .testTag("tree-card"),
    ) {
        Box(Modifier.size(220.dp, 150.dp).clip(RoundedCornerShape(12.dp)).background(leafTile())) {
            // Over the leaf tile, which is its placeholder (TreeRow.swift:106).
            tree.photo?.let { RemoteImage(it.card, null, Modifier.fillMaxSize(), placeholder = false) }
            Box(Modifier.align(Alignment.TopEnd).padding(2.dp)) { SaveMark(tree, onPhoto = true) }
            if (tree.id in marks.collected) Box(Modifier.align(Alignment.TopStart).padding(8.dp)) { SeenTag() }
        }
        // .lineLimit(2, reservesSpace: true): two lines held, the name wrapped at
        // words. The old trailing "\n" made a third line Compose had to ellipsize,
        // and it clipped "The Twin Planes of the El|even" mid-word (2026-11-11).
        Text(
            tree.name,
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
 * A tree of yours on the map list's Collected shelf (MineTile, TreeRow.swift):
 * your photograph in the highlight's frame, the Seen tag, its name and the
 * species when you gave one. No "Your tree" line (Hidde, 2026-11-06).
 */
@Composable
fun MineTile(s: app.ancienttrees.account.OwnSighting, mine: app.ancienttrees.account.MyTrees, onOpen: () -> Unit) {
    val brand = Brand.colors
    Column(
        Modifier
            .width(220.dp)
            .clickable(interactionSource = remember { MutableInteractionSource() }, indication = androidx.compose.foundation.LocalIndication.current, onClick = onOpen),
    ) {
        Box(Modifier.size(220.dp, 150.dp).clip(RoundedCornerShape(12.dp)).background(brand.surfaceMuted)) {
            OwnPhoto(s, mine, Modifier.fillMaxSize(), maxSide = 600) { Box(Modifier.fillMaxSize().background(brand.surfaceMuted)) }
            Box(Modifier.align(Alignment.TopStart).padding(8.dp)) { SeenTag() }
        }
        Text(
            s.name,
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
        s.species?.takeIf { it.isNotEmpty() }?.let {
            Text(it, fontSize = 12.sp, color = brand.inkSoft, maxLines = 1, modifier = Modifier.padding(top = 3.dp))
        }
    }
}

/**
 * TreeCard.swift, built to the AllTrails shape: the photograph 190 high (or the
 * species drawn on the leaf tile with "No photograph yet"), the bookmark top
 * right, the Collected tag top left, and under it the name and one meta line.
 * Rounded 14 with its own hairline, and the tap area is the card and nothing more.
 * [showText] off: the tapped pin's card in the map sheet, whose header already
 * says the name (TreePlaceSheet). [uniformTitle]: two lines kept for the name
 * in a shelf, so a row of cards ends level.
 */
@Composable
fun TreeCard(
    tree: Tree,
    onOpen: () -> Unit,
    modifier: Modifier = Modifier,
    showHeart: Boolean = true,
    showText: Boolean = true,
    uniformTitle: Boolean = false,
) {
    val brand = Brand.colors
    val marks = LocalTreeMarks.current
    val shape = RoundedCornerShape(14.dp)
    Column(
        modifier
            .fillMaxWidth()
            .clip(shape)
            .background(brand.surface)
            .border(1.dp, brand.hairline, shape)
            .clickable(interactionSource = remember { MutableInteractionSource() }, indication = androidx.compose.foundation.LocalIndication.current, onClick = onOpen),
    ) {
        Box(Modifier.fillMaxWidth().height(190.dp).background(leafTile())) {
            val photo = tree.photo
            if (photo != null) {
                // The leaf tile with a white spinner until it lands (TreeCard.swift:116);
                // the spinner in Android's own shape (Airbnb's line).
                RemoteImage(photo.card, null, Modifier.fillMaxSize(), fallback = {
                    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        androidx.compose.material3.CircularProgressIndicator(color = Color.White, strokeWidth = 2.dp, modifier = Modifier.size(24.dp))
                    }
                })
            } else {
                // VStack(spacing: 8): the mark, the name and the note all 8 apart (TreeCard.swift noPhoto).
                Column(Modifier.align(Alignment.Center), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    SpeciesMark(tree.species, Color.White.copy(alpha = 0.9f), Modifier.size(66.dp))
                    Text(tree.commonName, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = Color.White)
                    Text(stringResource(R.string.no_photo_yet), fontSize = 11.sp, color = Color.White.copy(alpha = 0.75f))
                }
            }
            if (showHeart) Box(Modifier.align(Alignment.TopEnd).padding(6.dp)) { SaveMark(tree, onPhoto = true) }
            if (tree.id in marks.collected) Box(Modifier.align(Alignment.TopStart).padding(10.dp)) { SeenTag() }
        }
        if (showText) PlainText {
            Column(Modifier.padding(horizontal = 12.dp, vertical = 10.dp), verticalArrangement = Arrangement.spacedBy(5.dp)) {
                Text(
                    tree.name,
                    fontFamily = BrandFace,
                    fontWeight = FontWeight.Bold,
                    fontSize = 17.sp,
                    lineHeight = 21.sp,
                    color = brand.ink,
                    maxLines = if (uniformTitle) 2 else 3,
                    minLines = if (uniformTitle) 2 else 1,
                    overflow = TextOverflow.Ellipsis,
                )
                TreeMetaLine(tree, size = 12)
            }
        }
    }
}

/** A tapped pin's card (TreePlaceBody): the TreeCard with no text, on the sheet's 16 point edges. */
@Composable
fun TreePlaceBody(tree: Tree, onOpen: () -> Unit) {
    TreeCard(tree, onOpen, Modifier.padding(horizontal = 16.dp), showText = false)
}
