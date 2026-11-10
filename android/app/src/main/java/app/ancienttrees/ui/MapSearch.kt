// The map's search page, ported from ios Screens/MapSearch.swift: a full screen
// over everything, the field with a back arrow, four lanes once two letters are
// typed (Top results, Places, Species, Trees), and before that the trees near you
// and the places worth a trip. Places are countries and our cities (popularity
// first), species match by name, Latin or any other name, trees by a word of
// their name from four letters. The typed part of a name is drawn heavier.
//
// Recent searches (signed in, on the server: account/RecentSearches.kt) sit under
// the empty field. A town we hold no trees in comes from the platform's own
// Geocoder (EmptyPlace.kt) where the iPhone asks MKLocalSearch: the grey card, the
// towns, and the nearest tree we do hold.

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
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.outlined.History
import androidx.compose.material.icons.outlined.PinDrop
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
import androidx.compose.runtime.compositionLocalOf
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import app.ancienttrees.account.RecentSearches
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
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

/** Who is searching: the account's recent searches need a signed-in token (MainActivity provides it). */
data class SearchAccount(
    val signedIn: Boolean = false,
    val token: suspend () -> String? = { null },
    /** `-recentdemo`: three rows so the section can be looked at without signing in. */
    val recentDemo: Boolean = false,
    /** The empty card's Add a tree: the camera flow (navigator.collectNearby). */
    val addTree: () -> Unit = {},
)

val LocalSearchAccount = compositionLocalOf { SearchAccount() }

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
    val who = LocalSearchAccount.current
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val recent = remember { RecentSearches() }
    // Recent searches: the account's newest five, signed in only.
    LaunchedEffect(Unit) {
        if (who.recentDemo) { recent.demo(demoRecent(catalogue, index)); return@LaunchedEffect }
        if (who.signedIn) recent.load(who.token())
    }
    // The geocoder's towns, a beat after the last keystroke, and which query they
    // answer so a stale answer is never shown under a newer one. Not asked when
    // one of OUR places carries the name typed.
    var realPlaces by remember { mutableStateOf<List<RealPlace>>(emptyList()) }
    var answered by remember { mutableStateOf<String?>(null) }
    LaunchedEffect(query) {
        val q = query.trim()
        if (q.length < 2 || oursIsNamed(catalogue, index, q)) { realPlaces = emptyList(); answered = null; return@LaunchedEffect }
        delay(300)
        val found = EmptyPlace.lookup(context, q)
        realPlaces = found
        answered = query
    }
    /** Every pick: recorded on the account (signed in only), then handed on. The
     *  upsert outlives this screen, as the iPhone's own Task does. */
    @OptIn(kotlinx.coroutines.DelicateCoroutinesApi::class)
    fun pick(hit: SearchHit) {
        if (who.signedIn) entryFor(catalogue, index, hit)?.let { e ->
            recent.demo(listOf(e) + recent.rows.filter { it.id != e.id })
            GlobalScope.launch { recent.record(e, who.token()) }
        }
        onPick(hit)
    }

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
                val mine = recentRows(catalogue, index, recent.rows)
                if (mine.isNotEmpty()) {
                    item {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.fillMaxWidth().padding(start = 16.dp, end = 4.dp).padding(top = 6.dp),
                        ) {
                            Eyebrow("Recent", Modifier.weight(1f))
                            Text(
                                "Clear all",
                                fontSize = 14.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = brand.moss,
                                modifier = Modifier
                                    .clickable { scope.launch { recent.clear(who.token()) } }
                                    .padding(12.dp)
                                    .testTag("recent-clear"),
                            )
                        }
                    }
                    for (r in mine) item(key = "recent-" + r.entry.id) {
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().testTag("recent-row")) {
                            Box(Modifier.weight(1f)) {
                                PlainResultRow(r.name, r.sub, Icons.Outlined.History, onClick = { pick(r.hit) }, iconTint = brand.inkSoft)
                            }
                            Box(
                                contentAlignment = Alignment.Center,
                                modifier = Modifier
                                    .padding(end = 2.dp)
                                    .size(44.dp)
                                    .clickable { scope.launch { recent.remove(r.entry, who.token()) } }
                                    .semantics { contentDescription = "Remove ${r.name} from recent" },
                            ) { Icon(Icons.Filled.Close, null, tint = brand.inkSoft, modifier = Modifier.size(18.dp)) }
                        }
                    }
                    item { Box(Modifier.padding(top = 10.dp).fillMaxWidth().height(0.5.dp).background(brand.hairline)) }
                }
                val near = catalogue.trees
                    .filter { Geo.km(origin.lat, origin.lng, it.lat, it.lng) <= 100 }
                    .sortedWith(compareBy<Tree>({ it.photo == null }, { Geo.km(origin.lat, origin.lng, it.lat, it.lng) }))
                    .take(4)
                if (near.isNotEmpty()) {
                    item { Head("Near you") }
                    for (t in near) item { ResultRow(t.name, "${t.commonName} · ${t.city}", Icons.Outlined.Park, query) { pick(SearchHit.OneTree(t)) } }
                }
                item { Head("Places worth a trip") }
                for (c in index.cities.take(6)) {
                    item {
                        ResultRow(c.name, "${c.country} · ${treesLabel(c.count)}", Icons.Outlined.Apartment, query) {
                            pick(SearchHit.City(c.slug, c.name, c.lat, c.lng))
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
                // NOTHING OF OURS, BUT A REAL TOWN (Hidde, 2026-10-25): the ask to add
                // the first tree, the towns, and the nearest tree we hold.
                val town = if (showPlaces) cardTown(catalogue, index, r, query, answered, realPlaces) else null
                if (town != null) {
                    item {
                        Box(Modifier.padding(horizontal = 16.dp).padding(top = 18.dp).testTag("empty-place-card")) {
                            EmptyPlaceCard(place = town.name, onAdd = who.addTree)
                        }
                    }
                    item { Head("Places") }
                    for (pl in listOf(town) + realPlaces.filter { it != town }) item(key = "town-" + pl.id) {
                        Box(Modifier.testTag("empty-place-town")) {
                            PlainResultRow(
                                pl.name,
                                if (pl.country.isEmpty()) "Show on the map" else "${pl.country} · show on the map",
                                Icons.Outlined.PinDrop,
                                onClick = { pick(SearchHit.Place(pl.name, pl.lat, pl.lng)) },
                            )
                        }
                    }
                    EmptyPlace.nearest(catalogue, town.lat, town.lng)?.let { (t, km) ->
                        item { Head("Nearest tree") }
                        item {
                            Box(Modifier.testTag("empty-place-nearest")) {
                                PlainResultRow(t.name, "${EmptyPlace.distance(km)} from ${town.name} · ${t.city}", Icons.Outlined.Park, onClick = { pick(SearchHit.OneTree(t)) })
                            }
                        }
                    }
                } else if (ours && showPlaces && answered == query) {
                    item { Note("Nothing matches “$query”. Check the spelling, or try a town nearby.") }
                } else if (empty && !(ours && showPlaces)) {
                    item { Note("Nothing under ${lane.label.lowercase()}. Try Top results.") }
                }
                if (town == null && showPlaces && r.places.isNotEmpty()) {
                    if (lane == Lane.TOP) item { Head("Places") }
                    for (p in r.places) item { ResultRow(p.name, p.sub, p.icon, query) { pick(p.hit) } }
                }
                if (showSpecies && r.species.isNotEmpty()) {
                    if (lane == Lane.TOP) item { Head("Species") }
                    for ((s, hit) in r.species) {
                        item {
                            SpeciesResultRow(catalogue, s, hit, query) { pick(SearchHit.Species(s)) }
                        }
                    }
                }
                if (showTrees && r.trees.isNotEmpty()) {
                    if (lane == Lane.TOP) item { Head("Trees") }
                    for (t in r.trees) item { ResultRow(t.name, "${t.commonName} · ${t.city}", Icons.Outlined.Park, query) { pick(SearchHit.OneTree(t)) } }
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

/** One of our cities or countries carries exactly this name, in English or another language. */
private fun oursIsNamed(c: Catalogue, idx: SearchIndex, raw: String): Boolean {
    val q = fold(raw)
    if (idx.countries.any { fold(it.name) == q }) return true
    return idx.cities.any { city -> fold(city.name) == q || c.aka(city.slug).any { fold(it) == q } }
}

/**
 * The town the empty card is about, or null for no card (MapSearch.cardTown).
 * When nothing of ours matches, the geocoder's first town. When ours match only in
 * passing, a town known by EXACTLY the name typed still gets its card (Bern), unless
 * one of our places begins with what was typed (barce finds Barcelona, not Barce).
 * Never "no trees" for a place of ours.
 */
private fun cardTown(c: Catalogue, idx: SearchIndex, r: Ranked, query: String, answered: String?, real: List<RealPlace>): RealPlace? {
    if (answered != query || real.isEmpty()) return null
    val towns = real.filter { !oursIsNamed(c, idx, it.name) }
    if (towns.isEmpty()) return null
    if (r.places.isEmpty() && r.species.isEmpty() && r.trees.isEmpty()) return towns[0]
    val q = fold(query.trim())
    if (r.places.any { fold(it.name).startsWith(q) }) return null
    return towns.firstOrNull { fold(it.name) == q }
}

private fun countrySub(k: CountryRow) = "${treesLabel(k.count)} in ${k.cities} ${if (k.cities == 1) "place" else "places"}"

/** What a pick is recorded as (MapSearch.entry(for:)). */
private fun entryFor(c: Catalogue, idx: SearchIndex, hit: SearchHit): RecentSearches.Entry? = when (hit) {
    is SearchHit.City -> RecentSearches.Entry(
        "city", hit.slug, hit.name,
        idx.cities.firstOrNull { it.slug == hit.slug }?.let { "${it.country} · ${treesLabel(it.count)}" }.orEmpty(),
    )
    is SearchHit.Country -> RecentSearches.Entry("country", hit.name, hit.name, idx.countries.firstOrNull { it.name == hit.name }?.let(::countrySub).orEmpty())
    is SearchHit.Species -> RecentSearches.Entry("species", hit.name, hit.name, treesLabel(c.treesOfSpecies(hit.name).size))
    is SearchHit.OneTree -> RecentSearches.Entry("tree", hit.tree.id, hit.tree.name, "${hit.tree.commonName} · ${hit.tree.city}")
    is SearchHit.Place -> RecentSearches.Entry(
        "place", String.format(java.util.Locale.US, "%.4f,%.4f", hit.lat, hit.lng), hit.name, "Show on the map",
    )
}

private class RecentRow(val entry: RecentSearches.Entry, val name: String, val sub: String, val hit: SearchHit)

/** The account's rows read against today's catalogue; a row no longer ours is left out. */
private fun recentRows(c: Catalogue, idx: SearchIndex, rows: List<RecentSearches.Entry>): List<RecentRow> = rows.mapNotNull { e ->
    when (e.kind) {
        "city" -> idx.cities.firstOrNull { it.slug == e.ref }?.let {
            RecentRow(e, it.name, "${it.country} · ${treesLabel(it.count)}", SearchHit.City(it.slug, it.name, it.lat, it.lng))
        }
        "country" -> idx.countries.firstOrNull { it.name == e.ref }?.let { RecentRow(e, it.name, countrySub(it), SearchHit.Country(it.name)) }
        "species" -> if (e.ref in c.speciesNames) {
            val sci = c.scientificName(e.ref)
            val n = treesLabel(c.treesOfSpecies(e.ref).size)
            RecentRow(e, e.ref, if (sci != null) "$sci · $n" else n, SearchHit.Species(e.ref))
        } else null
        "tree" -> c.tree(e.ref)?.let { RecentRow(e, it.name, "${it.commonName} · ${it.city}", SearchHit.OneTree(it)) }
        "place" -> {
            val p = e.ref.split(",").mapNotNull { it.toDoubleOrNull() }
            if (p.size == 2) RecentRow(e, e.label, e.sub.ifEmpty { "Show on the map" }, SearchHit.Place(e.label, p[0], p[1])) else null
        }
        else -> null
    }
}

/** Three rows for `-recentdemo`: Canada, Lisbon and a Lisbon tree, the mock's. */
private fun demoRecent(c: Catalogue, idx: SearchIndex): List<RecentSearches.Entry> {
    val out = ArrayList<RecentSearches.Entry>()
    (idx.countries.firstOrNull { it.name == "Canada" } ?: idx.countries.firstOrNull())?.let { k ->
        entryFor(c, idx, SearchHit.Country(k.name))?.let(out::add)
    }
    (idx.cities.firstOrNull { it.slug == "lisbon" } ?: idx.cities.firstOrNull())?.let { city ->
        entryFor(c, idx, SearchHit.City(city.slug, city.name, city.lat, city.lng))?.let(out::add)
        val ts = c.trees(city.slug)
        (ts.firstOrNull { it.name.contains("dragon", ignoreCase = true) } ?: ts.firstOrNull())?.let { t ->
            entryFor(c, idx, SearchHit.OneTree(t))?.let(out::add)
        }
    }
    return out
}
