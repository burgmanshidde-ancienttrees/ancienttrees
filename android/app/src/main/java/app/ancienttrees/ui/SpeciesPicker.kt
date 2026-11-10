// The Species chip's sheet, ported from ios Screens/SpeciesPicker.swift: what is
// on the map now first, then by how many trees; a search that finds a species by
// any of its names, the matched name and the Latin under each row
// (SpeciesRowName.swift); "Any species" while one is chosen; a tap picks, a tap
// on the chosen one clears it (Hidde, 2026-08-25). The whole row is the button.
//
// The same inset-grouped List and floating search field as SpeciesChooser.kt.
// ANDROID-FORCED: Material's modal bottom sheet for the iPhone's .sheet.

package app.ancienttrees.ui

import androidx.compose.foundation.layout.size
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
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
import app.ancienttrees.feed.SpeciesHit
import app.ancienttrees.feed.filterSpecies

@Composable
fun SpeciesPicker(
    catalogue: Catalogue,
    nearby: Set<String>,
    selection: String?,
    onPick: (String?) -> Unit,
    onDismiss: () -> Unit,
) {
    val brand = Brand.colors
    var query by remember { mutableStateOf("") }
    // Counted ONCE, when the sheet opens (Hidde, 2026-08-24: "de app loopt vast").
    val index = remember(catalogue) {
        catalogue.bySpecies.map { it.key to it.value.size }
            .sortedWith(compareBy<Pair<String, Int>>({ it.first !in nearby }, { -it.second }, { it.first }))
    }
    val counts = remember(index) { index.toMap() }
    val rows: List<Pair<String, SpeciesHit>> = remember(index, query) {
        val q = query.trim()
        if (q.isEmpty()) index.map { it.first to SpeciesHit.Name } else catalogue.filterSpecies(index.map { it.first }, q)
    }
    BarSheet(
        title = stringResource(R.string.sp_picker_title),
        onDismiss = onDismiss,
        leading = stringResource(R.string.close) to onDismiss,
        trailing = null,
        grouped = true,
    ) {
        SearchableList(query, { query = it }, stringResource(R.string.sp_which)) {
            val any = selection != null
            groupedSection(
                header = null,
                headerText = { "" },
                count = rows.size + if (any) 1 else 0,
                key = { i -> if (any && i == 0) "any" else rows[i - if (any) 1 else 0].first },
            ) { i ->
                if (any && i == 0) {
                    SpeciesListRow(onClick = { onPick(null); onDismiss() }) {
                        Text(stringResource(R.string.sp_any), fontSize = 17.sp, color = brand.moss)
                    }
                    return@groupedSection
                }
                val (name, hit) = rows[i - if (any) 1 else 0]
                SpeciesListRow(onClick = {
                    onPick(if (selection == name) null else name)
                    onDismiss()
                }) {
                    SpeciesMark(name, brand.moss, Modifier.size(26.dp))
                    SpeciesRowName(catalogue, name, hit, modifier = Modifier.weight(1f))
                    if (selection == name) Icon(Icons.Filled.Check, null, tint = brand.moss, modifier = Modifier.size(20.dp))
                    else Text("${counts[name] ?: 0}", fontSize = 15.sp, color = brand.inkSoft)
                }
            }
        }
    }
}
