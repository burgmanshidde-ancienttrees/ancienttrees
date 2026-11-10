// The map's search page, ported from ios Screens/MapSearch.swift: a full screen
// over everything, the field with a back arrow, four lanes once two letters are
// typed (Top results, Places, Species, Trees), and before that the trees near you
// and the places worth a trip. Places are countries and our cities (popularity
// first), species match by name, Latin or any other name, trees by a word of
// their name from four letters. The typed part of a name is drawn heavier.
//
// Not yet here (data/android-parity.json "search"): Recent searches (signed in,
// kept on the server) and the town lookup for places we have no trees in.

package app.ancienttrees.ui

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Cancel
import androidx.compose.material.icons.outlined.Apartment
import androidx.compose.material.icons.outlined.Eco
import androidx.compose.material.icons.outlined.Park
import androidx.compose.material.icons.outlined.Public
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.feed.Geo
import app.ancienttrees.feed.Here
import app.ancienttrees.feed.SpeciesHit
import app.ancienttrees.feed.SpeciesSearch
import app.ancienttrees.feed.Tree
import app.ancienttrees.feed.filterSpecies

private enum class Lane(val label: String) { TOP("Top results"), PLACES("Places"), SPECIES("Species"), TREES("Trees") }

private data class CityRow(val slug: String, val name: String, val country: String, val count: Int, val lat: Double, val lng: Double)
private data class CountryRow(val name: String, val count: Int, val cities: Int)
private data class PlaceRow(val id: String, val name: String, val sub: String, val icon: ImageVector, val hit: SearchHit)

/** SearchIndex: built once per catalogue. */
private class SearchIndex(c: Catalogue) {
    val cities: List<CityRow> = c.byCity.map { (slug, ts) ->
        CityRow(slug, ts[0].city, ts[0].country, ts.size, ts.sumOf { it.lat } / ts.size, ts.sumOf { it.lng } / ts.size)
    }.sortedWith(compareByDescending<CityRow> { c.popularity(it.slug) }.thenByDescending { it.count })
    val countries: List<CountryRow> = c.byCountry.map { (name, ts) ->
        CountryRow(name, ts.size, ts.map { it.citySlug }.toSet().size)
    }.sortedByDescending { it.count }
    val folded: List<Pair<Tree, String>> = c.trees.map { it to fold(it.name) }

    fun treesNamed(q: String): List<Tree> = folded.filter { it.second.startsWith(q) || it.second.contains(" $q") }.map { it.first }
}

private fun fold(s: String) = SpeciesSearch.fold(s)
private fun treesLabel(n: Int) = if (n == 1) "1 tree" else "$n trees"

@Composable
fun MapSearch(
    catalogue: Catalogue,
    origin: Here,
    initial: String,
    onPick: (SearchHit) -> Unit,
    onBack: () -> Unit,
) {
    val brand = Brand.colors
    var query by remember { mutableStateOf(initial) }
    var lane by remember { mutableStateOf(Lane.TOP) }
    val index = remember(catalogue) { SearchIndex(catalogue) }
    val focus = remember { FocusRequester() }
    LaunchedEffect(Unit) { runCatching { focus.requestFocus() } }
    BackHandler(onBack = onBack)

    Column(
        Modifier
            .fillMaxSize()
            .background(brand.ground)
            .statusBarsPadding()
            .imePadding()
            .semantics { contentDescription = "map-search" },
    ) {
        // The field: a back arrow, the words, a clear button once there is text.
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            modifier = Modifier
                .padding(horizontal = 16.dp)
                .padding(top = 6.dp, bottom = 10.dp)
                .fillMaxWidth()
                .height(54.dp)
                .shadow(6.dp, RoundedCornerShape(50), ambientColor = Color.Black.copy(alpha = 0.06f), spotColor = Color.Black.copy(alpha = 0.06f))
                .background(brand.surface, RoundedCornerShape(50))
                .border(1.dp, brand.hairline, RoundedCornerShape(50))
                .padding(horizontal = 6.dp),
        ) {
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier.size(44.dp).clickable(onClick = onBack).semantics { contentDescription = "Back to the map" },
            ) { Icon(Icons.AutoMirrored.Filled.ArrowBack, null, tint = brand.ink, modifier = Modifier.size(22.dp)) }
            Box(Modifier.weight(1f)) {
                if (query.isEmpty()) Text(SEARCH_PLACEHOLDER, fontSize = 17.sp, fontWeight = FontWeight.Medium, color = brand.inkSoft, maxLines = 1)
                BasicTextField(
                    value = query,
                    onValueChange = { query = it },
                    singleLine = true,
                    textStyle = TextStyle(fontSize = 17.sp, fontWeight = FontWeight.Medium, color = brand.ink),
                    cursorBrush = SolidColor(brand.ink),
                    keyboardOptions = KeyboardOptions(autoCorrectEnabled = false, imeAction = ImeAction.Search),
                    modifier = Modifier.fillMaxWidth().focusRequester(focus),
                )
            }
            if (query.isNotEmpty()) {
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier.size(44.dp).clickable { query = "" }.semantics { contentDescription = "Clear" },
                ) { Icon(Icons.Filled.Cancel, null, tint = brand.inkSoft, modifier = Modifier.size(20.dp)) }
            }
        }
        if (query.length >= 2) {
            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()).padding(horizontal = 16.dp).padding(bottom = 6.dp),
            ) {
                for (l in Lane.entries) {
                    val on = lane == l
                    Box(Modifier.height(44.dp).clickable { lane = l }, contentAlignment = Alignment.Center) {
                        Text(
                            l.label,
                            fontSize = 14.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = if (on) Color.White else brand.ink,
                            modifier = Modifier
                                .background(if (on) brand.canopy else brand.surface, RoundedCornerShape(50))
                                .then(if (on) Modifier else Modifier.border(1.dp, brand.hairline, RoundedCornerShape(50)))
                                .padding(horizontal = 14.dp, vertical = 9.dp),
                        )
                    }
                }
            }
        }
        Box(Modifier.fillMaxWidth().height(0.5.dp).background(brand.hairline))
        LazyColumn(Modifier.fillMaxWidth().weight(1f)) {
            if (query.length < 2) {
                val near = catalogue.trees
                    .filter { Geo.km(origin.lat, origin.lng, it.lat, it.lng) <= 100 }
                    .sortedWith(compareBy<Tree>({ it.photo == null }, { Geo.km(origin.lat, origin.lng, it.lat, it.lng) }))
                    .take(4)
                if (near.isNotEmpty()) {
                    item { Head("Near you") }
                    for (t in near) item { ResultRow(t.name, "${t.commonName} · ${t.city}", Icons.Outlined.Park, query) { onPick(SearchHit.OneTree(t)) } }
                }
                item { Head("Places worth a trip") }
                for (c in index.cities.take(6)) {
                    item {
                        ResultRow(c.name, "${c.country} · ${treesLabel(c.count)}", Icons.Outlined.Apartment, query) {
                            onPick(SearchHit.City(c.slug, c.name, c.lat, c.lng))
                        }
                    }
                }
            } else {
                val r = rank(catalogue, index, query, lane, origin)
                val showPlaces = lane == Lane.TOP || lane == Lane.PLACES
                val showSpecies = lane == Lane.TOP || lane == Lane.SPECIES
                val showTrees = lane == Lane.TOP || lane == Lane.TREES
                val ours = r.places.isEmpty() && r.species.isEmpty() && r.trees.isEmpty()
                val empty = (!showPlaces || r.places.isEmpty()) && (!showSpecies || r.species.isEmpty()) && (!showTrees || r.trees.isEmpty())
                if (ours && showPlaces) {
                    item { Note("Nothing matches “$query”. Check the spelling, or try a town nearby.") }
                } else if (empty) {
                    item { Note("Nothing under ${lane.label.lowercase()}. Try Top results.") }
                }
                if (showPlaces && r.places.isNotEmpty()) {
                    if (lane == Lane.TOP) item { Head("Places") }
                    for (p in r.places) item { ResultRow(p.name, p.sub, p.icon, query) { onPick(p.hit) } }
                }
                if (showSpecies && r.species.isNotEmpty()) {
                    if (lane == Lane.TOP) item { Head("Species") }
                    for ((s, hit) in r.species) {
                        item {
                            SpeciesResultRow(catalogue, s, hit, query) { onPick(SearchHit.Species(s)) }
                        }
                    }
                }
                if (showTrees && r.trees.isNotEmpty()) {
                    if (lane == Lane.TOP) item { Head("Trees") }
                    for (t in r.trees) item { ResultRow(t.name, "${t.commonName} · ${t.city}", Icons.Outlined.Park, query) { onPick(SearchHit.OneTree(t)) } }
                }
            }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}

private class Ranked(val places: List<PlaceRow>, val species: List<Pair<String, SpeciesHit>>, val trees: List<Tree>)

private fun rank(c: Catalogue, idx: SearchIndex, query: String, lane: Lane, origin: Here): Ranked {
    val q = fold(query)
    if (q.length < 2) return Ranked(emptyList(), emptyList(), emptyList())
    val places = ArrayList<PlaceRow>()
    for (k in idx.countries) {
        if (fold(k.name).startsWith(q)) {
            places.add(PlaceRow("k:" + k.name, k.name, "${treesLabel(k.count)} in ${k.cities} ${if (k.cities == 1) "place" else "places"}", Icons.Outlined.Public, SearchHit.Country(k.name)))
        }
    }
    fun startsAWord(name: String) = name.startsWith(q) || name.contains(" $q")
    for (city in idx.cities) {
        val n = fold(city.name)
        val other = c.aka(city.slug).any { startsAWord(fold(it)) }
        if (startsAWord(n) || fold(city.country).startsWith(q) || n.contains(q) || other) {
            places.add(PlaceRow("c:" + city.slug, city.name, "${city.country} · ${treesLabel(city.count)}", Icons.Outlined.Apartment, SearchHit.City(city.slug, city.name, city.lat, city.lng)))
        }
    }
    val species = c.filterSpecies(c.speciesNames, query)
    var trees: List<Tree> = emptyList()
    if (q.length >= 4 || lane == Lane.TREES) {
        trees = idx.treesNamed(q).sortedWith(compareBy<Tree>({ it.photo == null }, { Geo.km(origin.lat, origin.lng, it.lat, it.lng) }))
    }
    if (lane != Lane.TOP) return Ranked(places.take(40), species.take(40), trees.take(40))
    val p = places.take(6)
    val s = species.take(if (p.isEmpty()) 6 else 2)
    val room = maxOf(0, 8 - p.size - s.size)
    return Ranked(p, s, trees.take(minOf(room, if (p.isEmpty()) 5 else 2)))
}

@Composable
private fun Head(text: String) {
    Eyebrow(text, Modifier.padding(horizontal = 16.dp).padding(top = 18.dp, bottom = 6.dp))
}

@Composable
private fun Note(text: String) {
    Text(text, fontSize = 15.sp, color = Brand.colors.inkSoft, modifier = Modifier.padding(horizontal = 16.dp).padding(top = 24.dp))
}

/** The typed part heavier: bold name, black for what matches. */
private fun highlighted(name: String, query: String): AnnotatedString {
    val q = fold(query)
    val f = fold(name)
    val at = if (q.length >= 2) f.indexOf(q) else -1
    return buildAnnotatedString {
        if (at < 0 || at + q.length > name.length || f.length != name.length) {
            withStyle(SpanStyle(fontWeight = FontWeight.Bold)) { append(name) }
            return@buildAnnotatedString
        }
        withStyle(SpanStyle(fontWeight = FontWeight.Bold)) { append(name.substring(0, at)) }
        withStyle(SpanStyle(fontWeight = FontWeight.Black)) { append(name.substring(at, at + q.length)) }
        withStyle(SpanStyle(fontWeight = FontWeight.Bold)) { append(name.substring(at + q.length)) }
    }
}

@Composable
private fun ResultRow(name: String, sub: String, icon: ImageVector, query: String, onClick: () -> Unit) {
    val brand = Brand.colors
    PlainResultRow(
        name = name,
        sub = sub,
        icon = icon,
        onClick = onClick,
        title = {
            Text(highlighted(name, query), fontFamily = BrandFace, fontSize = 16.sp, color = brand.ink, maxLines = 1, overflow = TextOverflow.Ellipsis)
        },
    )
}

/** A species: its name, then how it was found, the Latin in italics, and the count. */
@Composable
private fun SpeciesResultRow(c: Catalogue, name: String, hit: SpeciesHit, query: String, onClick: () -> Unit) {
    val brand = Brand.colors
    val count = treesLabel(c.treesOfSpecies(name).size)
    val sci = c.scientificName(name)
    val via = (hit as? SpeciesHit.Other)?.via
    PlainResultRow(
        name = name,
        sub = "",
        icon = Icons.Outlined.Eco,
        onClick = onClick,
        title = {
            Text(highlighted(name, query), fontFamily = BrandFace, fontSize = 16.sp, color = brand.ink, maxLines = 1, overflow = TextOverflow.Ellipsis)
        },
        subLine = {
            Text(
                buildAnnotatedString {
                    if (via != null) append("$via · ")
                    if (sci != null) {
                        withStyle(SpanStyle(fontStyle = FontStyle.Italic)) { append(sci) }
                        append(" · ")
                    }
                    append(count)
                },
                fontSize = 12.sp,
                color = brand.inkSoft,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
            )
        },
    )
}
