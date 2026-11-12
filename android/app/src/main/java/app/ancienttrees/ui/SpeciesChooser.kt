// Naming the species of a tree you added yourself. Ported from ios
// Screens/SpeciesChooser.swift: iNaturalist's identify list, ordered by what
// grows around you, searchable by any name a species goes by; kinds of tree we
// know and do not map yet in their own section; and while nothing carries what
// was typed, the tag field's "Use …" row at the foot (a typed string cannot
// group, and hard rule 9 wants one name per species).
//
// The list is the iPhone's inset-grouped List: white sections with hairlines
// inset to the name, a grey ground, and the search field floating at the foot
// (.searchable in a sheet on iOS 26). GroupedSection and SheetSearchField are
// shared with the map's species filter (SpeciesPicker.kt).
//
// ANDROID-FORCED: the sheet is Material's modal bottom sheet (BarSheet), the
// counterpart of the iPhone's .sheet presentation.

package app.ancienttrees.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.RowScope
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBars
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyListScope
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.feed.SpeciesHit
import app.ancienttrees.feed.SpeciesSearch
import app.ancienttrees.feed.filterSpecies
import app.ancienttrees.feed.unmappedSpecies

/** SpeciesChooser.swift. [current] carries the tick; [onPick] gets a name, or "Common (Latin)" for an unmapped row. */
@Composable
fun SpeciesChooser(
    catalogue: Catalogue,
    nearby: List<String>,
    current: String,
    onPick: (String) -> Unit,
    onClose: () -> Unit,
) {
    val brand = Brand.colors
    var query by remember { mutableStateOf("") }
    // Counted once, when the sheet opens (the freeze SpeciesPicker hit on 2026-08-24).
    val index = remember(catalogue) {
        val near = nearby.toSet()
        catalogue.bySpecies.filterKeys { it.isNotEmpty() }.map { it.key to it.value.size }
            .sortedWith(compareBy<Pair<String, Int>>({ it.first !in near }, { -it.second }, { it.first }))
    }
    val counts = remember(index) { index.toMap() }
    val typed = query.trim()
    val rows: List<Pair<String, SpeciesHit>> = remember(index, typed) {
        if (typed.isEmpty()) index.map { it.first to SpeciesHit.Name }
        else catalogue.filterSpecies(index.map { it.first }, typed)
    }
    val notMapped = remember(catalogue, typed) { catalogue.unmappedSpecies(typed) }
    val folded = SpeciesSearch.fold(typed)
    val mayTypeOwn = typed.length >= 3 &&
        rows.none { SpeciesSearch.fold(it.first) == folded } &&
        notMapped.none { SpeciesSearch.fold(it.first.c) == folded }
    fun isCurrent(name: String) = SpeciesSearch.fold(name) == SpeciesSearch.fold(current) ||
        SpeciesSearch.fold(name) == SpeciesSearch.fold(current.substringBefore("(").trim())

    BarSheet(
        title = stringResource(R.string.cf_kind_q),
        onDismiss = onClose,
        leading = stringResource(R.string.close) to onClose,
        trailing = null,
        grouped = true,
    ) {
        SearchableList(query, { query = it }, stringResource(R.string.sp_which)) {
            groupedSection(
                header = if (typed.isEmpty() && nearby.isNotEmpty()) "near" else null,
                headerText = { stringResource(R.string.cf_near_first) },
                count = rows.size,
                key = { rows[it].first },
            ) { i ->
                val (name, hit) = rows[i]
                SpeciesListRow(onClick = { onPick(name); onClose() }) {
                    SpeciesMark(name, brand.moss, Modifier.size(26.dp))
                    SpeciesRowName(catalogue, name, hit, modifier = Modifier.weight(1f))
                    if (isCurrent(name)) Icon(Sym.CheckSemibold, null, tint = brand.moss, modifier = Modifier.size(23.dp))
                    else Text("${counts[name] ?: 0}", fontSize = 15.sp, color = brand.inkSoft)
                }
            }
            if (notMapped.isNotEmpty()) {
                groupedSection(
                    header = "not-mapped",
                    headerText = { stringResource(R.string.sp_not_mapped) },
                    count = notMapped.size,
                    key = { "nm-" + notMapped[it].first.c },
                ) { i ->
                    val (row, hit) = notMapped[i]
                    SpeciesListRow(onClick = { onPick(row.species); onClose() }) {
                        SpeciesMark(row.c, brand.moss, Modifier.size(26.dp))
                        SpeciesRowName(catalogue, row.c, hit, latin = if (row.isGenus) row.l + " sp." else row.l, modifier = Modifier.weight(1f))
                        if (isCurrent(row.species) || isCurrent(row.c)) Icon(Sym.CheckSemibold, null, tint = brand.moss, modifier = Modifier.size(23.dp))
                    }
                }
            }
            if (mayTypeOwn) {
                groupedSection(
                    header = null,
                    headerText = { "" },
                    count = 1,
                    key = { "own" },
                    footer = { stringResource(R.string.cf_use_typed_foot) },
                ) {
                    SpeciesListRow(onClick = { onPick(typed); onClose() }) {
                        Icon(Sym.AddCircle, null, tint = brand.moss, modifier = Modifier.size(26.dp))
                        Text(stringResource(R.string.cf_use_typed, typed), fontSize = 17.sp, color = brand.ink)
                    }
                }
            }
        }
    }
}

/** The list with the search field floating at its foot, over the grey ground. */
@Composable
internal fun ColumnScope.SearchableList(
    query: String,
    onQuery: (String) -> Unit,
    prompt: String,
    content: LazyListScope.() -> Unit,
) {
    Box(Modifier.fillMaxWidth().weight(1f)) {
        LazyColumn(
            Modifier.fillMaxSize().testTag("species-list"),
            contentPadding = androidx.compose.foundation.layout.PaddingValues(bottom = 96.dp),
            content = content,
        )
        // The list fades out behind the floating field, iOS 26's soft scroll edge at
        // the foot (visual review 2026-11-11, row 116).
        Box(
            Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .height(96.dp)
                .background(
                    androidx.compose.ui.graphics.Brush.verticalGradient(
                        0f to Brand.colors.surfaceMuted.copy(alpha = 0f),
                        1f to Brand.colors.surfaceMuted,
                    ),
                ),
        )
        SheetSearchField(query, onQuery, prompt, Modifier.align(Alignment.BottomCenter))
    }
}

/** .searchable on iOS 26 in a sheet: a white capsule floating at the foot. */
@Composable
internal fun SheetSearchField(query: String, onQuery: (String) -> Unit, prompt: String, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    // iOS 26's bottom search capsule: 48 tall, 28 from each side and 28 above the
    // screen's foot (out/parity/side-by-side/species-pick.png, 2026-11-12). This
    // field stands on the navigation bar, so the bar's height comes off the 28;
    // over three-button navigation it keeps 4 above the buttons.
    val nav = with(androidx.compose.ui.platform.LocalDensity.current) {
        androidx.compose.foundation.layout.WindowInsets.navigationBars.getBottom(this).toDp()
    }
    BasicTextField(
        value = query,
        onValueChange = onQuery,
        singleLine = true,
        textStyle = sfStyle(fontSize = 17.sp, color = brand.ink),
        cursorBrush = SolidColor(brand.moss),
        modifier = modifier
            .imePadding()
            .padding(start = 28.dp, end = 28.dp, top = 14.dp, bottom = (28.dp - nav).coerceAtLeast(4.dp))
            .fillMaxWidth()
            .testTag("species-search"),
        decorationBox = { inner ->
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp)
                    .shadow(10.dp, RoundedCornerShape(50), ambientColor = Color.Black.copy(alpha = 0.12f), spotColor = Color.Black.copy(alpha = 0.12f))
                    .background(brand.surface, RoundedCornerShape(50))
                    .padding(horizontal = 16.dp),
            ) {
                Icon(Sym.Search, null, tint = brand.ink, modifier = Modifier.size(20.dp))
                Box(Modifier.weight(1f)) {
                    if (query.isEmpty()) Text(prompt, fontSize = 17.sp, color = brand.inkSoft)
                    inner()
                }
            }
        },
    )
}

/**
 * One inset-grouped section of a List: an optional grey header, white rows in one
 * rounded card with hairlines inset to the name, and an optional footer.
 */
internal fun LazyListScope.groupedSection(
    header: String?,
    headerText: @Composable () -> String,
    count: Int,
    key: (Int) -> Any,
    footer: (@Composable () -> String)? = null,
    row: @Composable (Int) -> Unit,
) {
    if (header != null) {
        item(key = "h-$header") {
            Text(
                headerText(),
                // An iOS 26 inset-grouped section header: 17 semibold.
                fontSize = 17.sp,
                fontWeight = FontWeight.SemiBold,
                color = Brand.colors.inkSoft,
                modifier = Modifier.padding(start = 32.dp, end = 32.dp, top = 6.dp, bottom = 8.dp),
            )
        }
    } else {
        item(key = "gap-${key(0)}") { Spacer(Modifier.height(18.dp)) }
    }
    items(count, key = key) { i ->
        val first = i == 0
        val last = i == count - 1
        val r = 22.dp
        val shape = RoundedCornerShape(
            topStart = if (first) r else 0.dp, topEnd = if (first) r else 0.dp,
            bottomStart = if (last) r else 0.dp, bottomEnd = if (last) r else 0.dp,
        )
        Column(Modifier.padding(horizontal = 16.dp).clip(shape).background(Brand.colors.surface)) {
            row(i)
            // iOS 26's inset-grouped separator: from the name, stopping 32 short of the card's edge.
            if (!last) Box(Modifier.padding(start = 54.dp, end = 32.dp).fillMaxWidth().height(0.5.dp).background(Brand.colors.hairline))
        }
    }
    if (footer != null) {
        item(key = "f-${key(0)}") {
            Text(
                footer(),
                fontSize = 13.sp,
                color = Brand.colors.inkSoft,
                modifier = Modifier.padding(start = 32.dp, end = 32.dp, top = 8.dp),
            )
        }
    }
}

/** The whole row is the button (Hidde, 2026-08-25): mark, name block, then the count or the tick. */
@Composable
internal fun SpeciesListRow(onClick: () -> Unit, minHeight: Dp = 44.dp, content: @Composable RowScope.() -> Unit) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = minHeight)
            .clickable(role = Role.Button, onClick = onClick)
            // iOS 26's List row: 18 above and below (SweepFrames: a name and its Latin
            // line make a 74 point row there; at 11 the rows were 60.5).
            .padding(horizontal = 16.dp, vertical = 18.dp),
        content = content,
    )
}
