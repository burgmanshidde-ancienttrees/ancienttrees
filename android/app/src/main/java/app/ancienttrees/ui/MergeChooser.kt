// Merging a tree you added into one of ours, from the ⋯ menu on its page.
// Ported from ios Screens/MergeChooser.swift.
//
// Convention: Google Maps fixes a duplicate place through its report menu
// ("Place is a duplicate"), never through a banner on the place (CONVENTIONS.md,
// "Adding a tree that is already on the map"). Hidde, 2026-10-19, on the box that
// asked on the page itself: "this is hell intrusive flow for how rare it is". So
// it lives in the menu, and this list is shaped like the species one beside it
// (SpeciesChooser): nearest first, search by name. The merge itself is instant
// (Hidde, same day: "let them do it"); the photo review still decides whether the
// photograph shows on our page.
//
// ANDROID-FORCED: the sheet is Material's modal bottom sheet (BarSheet), the
// counterpart of the iPhone's .sheet presentation, as SpeciesChooser's.

package app.ancienttrees.ui

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.feed.CollectRules
import app.ancienttrees.feed.Geo
import app.ancienttrees.feed.SpeciesSearch
import app.ancienttrees.feed.Tree

/** CollectSheet.search: names containing the query, nearest first, eight at most. */
fun mergeSearch(query: String, lat: Double, lng: Double, trees: List<Tree>): List<Tree> {
    val q = SpeciesSearch.fold(query.trim())
    if (q.length < 2) return emptyList()
    return trees.filter { SpeciesSearch.fold(it.name).contains(q) }
        .sortedBy { Geo.km(lat, lng, it.lat, it.lng) }
        .take(8)
}

@Composable
fun MergeChooser(
    catalogue: Catalogue,
    /** Where the tree you added stands. */
    lat: Double,
    lng: Double,
    onMerge: (Tree) -> Unit,
    onClose: () -> Unit,
) {
    val brand = Brand.colors
    var query by remember { mutableStateOf("") }
    var confirming by remember { mutableStateOf<Tree?>(null) }
    // Sorted once, when the sheet opens: every tree times every keystroke froze it.
    val nearest = remember(catalogue, lat, lng) {
        catalogue.trees.map { it to Geo.km(lat, lng, it.lat, it.lng) }.sortedBy { it.second }.take(20).map { it.first }
    }
    val typed = query.trim()
    val rows = if (typed.length >= 2) mergeSearch(typed, lat, lng, catalogue.trees) else nearest
    val none: String = stringResource(R.string.mg_none)
    val footer: (@Composable () -> String)? = if (rows.isEmpty() && typed.length >= 2) ({ none }) else null

    BarSheet(
        title = stringResource(R.string.mg_title),
        onDismiss = onClose,
        leading = stringResource(R.string.cancel) to onClose,
        trailing = null,
        grouped = true,
    ) {
        SearchableList(query, { query = it }, stringResource(R.string.mg_search)) {
            groupedSection(
                header = null,
                headerText = { "" },
                count = rows.size,
                key = { rows[it].id },
                footer = footer,
            ) { i ->
                val t = rows[i]
                val metres = (Geo.km(lat, lng, t.lat, t.lng) * 1000).toInt()
                SpeciesListRow(onClick = { confirming = t }) {
                    Column(Modifier.weight(1f)) {
                        Text(t.name, fontSize = 17.sp, color = brand.ink)
                        Spacer(Modifier.padding(top = 2.dp))
                        Text("${t.commonName} · ${CollectRules.distance(metres)}", fontSize = 13.sp, color = brand.inkSoft)
                    }
                    Spacer(Modifier.width(4.dp))
                }
            }
        }
    }

    confirming?.let { t ->
        BrandSheet(
            icon = Sym.Merge,
            title = stringResource(R.string.mg_confirm_title, t.name),
            message = stringResource(R.string.mg_confirm_body),
            onDismiss = { confirming = null },
            buttons = listOf(
                SheetButton(stringResource(R.string.mg_confirm), SheetKind.PRIMARY) {
                    confirming = null
                    onMerge(t)
                    onClose()
                },
                SheetButton(stringResource(R.string.cancel), SheetKind.QUIET) { confirming = null },
            ),
        )
    }
}
