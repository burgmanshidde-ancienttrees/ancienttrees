// One species, and every tree of it we map. Ported from ios Screens/Species.swift,
// with SpeciesRowName.swift (the name block of a species row) and Style.swift's
// scientificNameText (the Latin in italics, its rank words upright).
//
// The website has a page per species; this is the app's. Photographed first,
// then nearest (Hidde, 2026-08-25: "put the ones that have a photo on top"), and
// what this kind of tree IS before the list of them (Hidde, 2026-08-26), from
// the paragraph browse.json carries for the species page (Contract F).
//
// ANDROID-FORCED: the pushed page's bar draws Android's back arrow (PushedBar),
// and the system back gesture closes the page.

package app.ancienttrees.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.text.withStyle
import app.ancienttrees.R
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.feed.Geo
import app.ancienttrees.feed.Here
import app.ancienttrees.feed.SpeciesHit
import app.ancienttrees.feed.Tree

/** Style.swift scientificNameText: the Latin in italics, rank words and cultivar names upright. */
fun scientificName(sci: String): AnnotatedString {
    val upright = setOf("x", "×", "subsp.", "ssp.", "var.", "f.", "sp.", "spp.", "cv.", "syn.")
    val words = Regex("['\"‘“][^'\"’”]*['\"’”]|\\S+")
    return buildAnnotatedString {
        var at = 0
        for (m in words.findAll(sci)) {
            append(sci.substring(at, m.range.first))
            val w = m.value
            if (w in upright || w.first() in "'\"‘“") append(w)
            else withStyle(SpanStyle(fontStyle = FontStyle.Italic)) { append(w) }
            at = m.range.last + 1
        }
        append(sci.substring(at))
    }
}

/**
 * SpeciesRowName.swift: the common name on top and the Latin in italics beneath,
 * and when a search found it by another name, that name first (iNaturalist's
 * taxon row and its matched term). [latin] for a row that is not one of ours.
 */
@Composable
fun SpeciesRowName(catalogue: Catalogue, name: String, hit: SpeciesHit = SpeciesHit.Name, latin: String? = null, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    val sci = latin ?: catalogue.scientificName(name)
    val via = (hit as? SpeciesHit.Other)?.via
    Column(modifier, verticalArrangement = Arrangement.spacedBy(2.dp)) {
        Text(name, fontSize = 17.sp, color = brand.ink)
        if (via != null || sci != null) {
            Text(
                buildAnnotatedString {
                    if (via != null) append(via)
                    if (via != null && sci != null) append(" · ")
                    if (sci != null) append(scientificName(sci))
                },
                fontSize = 13.sp,
                color = brand.inkSoft,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
            )
        }
    }
}

/** Species.swift SpeciesView. */
@Composable
fun SpeciesScreen(
    commonName: String,
    catalogue: Catalogue,
    origin: Here,
    onBack: () -> Unit,
    onOpen: (Tree) -> Unit,
) = PlainText {
    val brand = Brand.colors
    // Back is MainActivity's, so a tree opened from this page closes first.
    // Photographed first, then nearest: distance still decides inside each group.
    val trees = remember(catalogue, commonName, origin) {
        catalogue.treesOfSpecies(commonName).sortedWith(
            compareBy<Tree>({ it.photo == null }, { Geo.km(origin.lat, origin.lng, it.lat, it.lng) }),
        )
    }
    val sci = catalogue.scientificName(commonName)
    val intro = catalogue.intro(commonName)
    Column(Modifier.fillMaxSize().background(brand.ground).testTag("species-page")) {
        PushedBar(commonName, onBack)
        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(14.dp),
            contentPadding = PaddingValues(top = 6.dp),
            modifier = Modifier.fillMaxSize(),
        ) {
            item {
                Row(
                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.padding(horizontal = 16.dp).padding(top = 4.dp),
                ) {
                    SpeciesMark(commonName, brand.moss, Modifier.size(44.dp))
                    Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
                        Text(commonName, fontFamily = BrandFace, fontWeight = FontWeight.ExtraBold, fontSize = 20.sp, color = brand.ink)
                        // The scientific name under the common one, in italics: iNaturalist's taxon page.
                        if (sci != null) {
                            Text(scientificName(sci), fontSize = 15.sp, color = brand.inkSoft, modifier = Modifier.testTag("species-scientific"))
                        }
                        Text(stringResource(R.string.sp_on_map, trees.size), fontSize = 13.sp, color = brand.inkSoft)
                    }
                }
            }
            // WHAT THIS KIND OF TREE IS, before the list of them.
            if (!intro.isNullOrEmpty()) {
                item {
                    Text(
                        intro,
                        fontSize = 16.sp,
                        color = brand.ink,
                        modifier = Modifier.padding(horizontal = 16.dp).padding(bottom = 6.dp).testTag("species-intro"),
                    )
                }
            }
            items(trees, key = { it.id }) { t ->
                TreeCard(t, onOpen = { onOpen(t) }, modifier = Modifier.padding(horizontal = 16.dp).testTag("tree-card"))
            }
            item { Spacer(Modifier.height(90.dp)) }
        }
    }
}
