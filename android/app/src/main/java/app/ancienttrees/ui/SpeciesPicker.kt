// The Species chip's sheet, ported from ios Screens/SpeciesPicker.swift: what is
// on the map now first, then by how many trees; a search that finds a species by
// any of its names; "Any species" while one is chosen; a tap picks or clears.
//
// ANDROID-FORCED: a system sheet on Android is Material's modal bottom sheet, the
// counterpart of the iPhone's .sheet presentation, with the search field at its top.

package app.ancienttrees.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.feed.filterSpecies

@OptIn(ExperimentalMaterial3Api::class)
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
    val index = remember(catalogue, nearby) {
        catalogue.bySpecies.map { it.key to it.value.size }
            .sortedWith(compareBy<Pair<String, Int>>({ it.first !in nearby }, { -it.second }, { it.first }))
    }
    val rows = remember(index, query) {
        val q = query.trim()
        if (q.isEmpty()) index
        else {
            val counts = index.toMap()
            catalogue.filterSpecies(index.map { it.first }, q).map { it.first to (counts[it.first] ?: 0) }
        }
    }
    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true),
        containerColor = brand.ground,
    ) {
        Box(Modifier.fillMaxWidth().padding(horizontal = 16.dp)) {
            Text("Close", color = brand.moss, fontSize = 17.sp, modifier = Modifier.align(Alignment.CenterStart).clickable(onClick = onDismiss))
            Text("Species", fontWeight = FontWeight.SemiBold, fontSize = 17.sp, color = brand.ink, textAlign = TextAlign.Center, modifier = Modifier.align(Alignment.Center))
        }
        Box(
            Modifier
                .padding(16.dp)
                .fillMaxWidth()
                .background(brand.surfaceMuted, RoundedCornerShape(10.dp))
                .border(0.dp, brand.surfaceMuted, RoundedCornerShape(10.dp))
                .padding(horizontal = 12.dp, vertical = 9.dp),
        ) {
            if (query.isEmpty()) Text("Which kind of tree?", color = brand.inkSoft, fontSize = 17.sp)
            BasicTextField(
                value = query,
                onValueChange = { query = it },
                singleLine = true,
                textStyle = TextStyle(fontSize = 17.sp, color = brand.ink),
                cursorBrush = SolidColor(brand.ink),
                modifier = Modifier.fillMaxWidth(),
            )
        }
        LazyColumn(Modifier.fillMaxWidth()) {
            if (selection != null) {
                item {
                    Text(
                        "Any species",
                        color = brand.moss,
                        fontSize = 17.sp,
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { onPick(null); onDismiss() }
                            .padding(horizontal = 16.dp, vertical = 12.dp),
                    )
                }
            }
            items(rows, key = { it.first }) { (name, count) ->
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                    modifier = Modifier
                        .fillMaxWidth()
                        .heightIn(min = 44.dp)
                        .clickable {
                            onPick(if (selection == name) null else name)
                            onDismiss()
                        }
                        .padding(horizontal = 16.dp, vertical = 6.dp),
                ) {
                    SpeciesMark(name, brand.moss, Modifier.size(26.dp))
                    Text(name, fontSize = 17.sp, color = brand.ink, modifier = Modifier.weight(1f))
                    if (selection == name) {
                        Icon(Icons.Filled.Check, null, tint = brand.moss)
                    } else {
                        Text("$count", fontSize = 15.sp, color = brand.inkSoft)
                    }
                }
            }
            item { Spacer(Modifier.heightIn(min = 24.dp)) }
        }
    }
}
