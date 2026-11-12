// A tree somebody else added, opened from their unlisted link: the twin of ios
// Screens/SharedTreeView.swift (review 2026-11-11: Android sent the link to the
// website instead).
//
// Convention: the website's own /t?id= page (site/src/pages/t/index.astro). Read
// only, for the same reason the website's is: it is somebody else's tree, shown,
// not editable. A link to a tree this account holds opens its own editable page
// instead (MainActivity), as ContentView's destination does.
//
// WHAT IT DOES NOT SHOW: where the tree is (hard rule 10). The public
// `shared_trees` view never carries a coordinate, so there is nothing to withhold.

package app.ancienttrees.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.account.Supa
import java.text.DateFormat
import java.text.SimpleDateFormat
import java.util.Locale

private sealed class SharedState {
    data object Loading : SharedState()
    data object Missing : SharedState()
    data class Found(
        val name: String,
        val species: String?,
        val age: String?,
        val note: String?,
        val photo: String?,
        val takenAt: java.util.Date?,
    ) : SharedState()
}

/** SharedTreeView.load: one tree by its link's id (shared_tree, 2026-10-19), never the list. */
private suspend fun loadShared(id: String): SharedState {
    val rows = Supa.rows("/rest/v1/rpc/shared_tree?tid=" + id.lowercase(), Supa.KEY)
    val row = rows.firstOrNull() ?: return SharedState.Missing
    fun str(k: String) = if (row.isNull(k) || !row.has(k)) null else row.optString(k).takeIf { it.isNotEmpty() }
    val taken = str("taken_at")?.let { raw ->
        // The day only now ("2026-10-19"); a full timestamp still reads by its day.
        runCatching { SimpleDateFormat("yyyy-MM-dd", Locale.ROOT).parse(raw.take(10)) }.getOrNull()
    }
    return SharedState.Found(
        name = str("name") ?: "A tree",
        species = str("species"),
        age = str("age"),
        note = str("note"),
        photo = str("photo")?.let { Supa.URL_BASE + "/storage/v1/object/public/shared-sightings/" + it },
        takenAt = taken,
    )
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun SharedTreeScreen(id: String, onBack: () -> Unit, onFindNear: () -> Unit) = PlainText {
    val brand = Brand.colors
    var state by remember(id) { mutableStateOf<SharedState>(SharedState.Loading) }
    LaunchedEffect(id) { state = loadShared(id) }
    val title = (state as? SharedState.Found)?.name ?: stringResource(R.string.shared_a_tree)
    Column(Modifier.fillMaxSize().background(brand.ground).testTag("shared-tree")) {
        PushedBar(title, onBack)
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState())) {
            when (val s = state) {
                SharedState.Loading -> Box(Modifier.fillMaxWidth().padding(top = 80.dp), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(color = brand.inkSoft)
                }
                // ContentUnavailableView: the symbol, a title and a line, centred.
                SharedState.Missing -> Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.fillMaxWidth().padding(top = 40.dp).padding(horizontal = 32.dp),
                ) {
                    androidx.compose.material3.Icon(Sym.AddLink, null, tint = brand.inkSoft, modifier = Modifier.padding(bottom = 6.dp))
                    Text(stringResource(R.string.shared_missing), fontSize = 22.sp, fontWeight = FontWeight.Bold, color = brand.ink, textAlign = TextAlign.Center)
                    Text(stringResource(R.string.shared_missing_why), fontSize = 15.sp, color = brand.inkSoft, textAlign = TextAlign.Center)
                }
                is SharedState.Found -> Column(
                    verticalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = Modifier.padding(20.dp),
                ) {
                    if (s.photo != null) {
                        RemoteImage(
                            s.photo, null,
                            Modifier.fillMaxWidth().height(260.dp).clip(RoundedCornerShape(18.dp)).background(brand.surfaceMuted),
                        )
                    }
                    Text(
                        stringResource(R.string.shared_overline).uppercase(), fontSize = 12.sp, fontWeight = FontWeight.SemiBold,
                        color = brand.inkSoft,
                    )
                    Text(s.name, fontFamily = BrandFace, fontWeight = FontWeight.ExtraBold, fontSize = 28.sp, color = brand.ink)
                    val chips = listOfNotNull(s.species, s.age, s.takenAt?.let { DateFormat.getDateInstance(DateFormat.LONG).format(it) })
                    if (chips.isNotEmpty()) {
                        FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            for (c in chips) {
                                Text(
                                    c, fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = brand.ink,
                                    modifier = Modifier.background(brand.surfaceMuted, RoundedCornerShape(50)).padding(horizontal = 10.dp, vertical = 5.dp),
                                )
                            }
                        }
                    }
                    if (!s.note.isNullOrEmpty()) Text(s.note, fontSize = 17.sp, color = brand.ink)
                    // NOT "get the app": whoever reads this already has it open.
                    Box(
                        Modifier.padding(top = 8.dp).fillMaxWidth().clip(RoundedCornerShape(50)).background(brand.moss)
                            .clickable(role = Role.Button, onClick = onFindNear).padding(vertical = 15.dp)
                            .testTag("shared-find-near"),
                        contentAlignment = Alignment.Center,
                    ) {
                        Text(stringResource(R.string.shared_find_near), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 17.sp, color = brand.onMoss)
                    }
                }
            }
        }
    }
}
