// Discover, ported from ios Screens/Home.swift (HomeView), where every ruling
// behind this screen is written beside the code: shelves, not a settings list
// (2026-08-20); every row slides with the next card peeking (2026-10-10); the
// season hero (2026-10-10, 2026-10-13); New from visitors (2026-11-06); the
// order (2026-10-13); the stream at the end that keeps going (2026-10-10); the
// search field that slides away while you read down and comes back the moment
// you scroll up (Quick Return, 2026-10-12). Read the Swift before changing any
// of it here: Android copies the iPhone (DECISIONS.md 2026-11-10).
//
// ANDROID-FORCED DIFFERENCES (data/android-parity.json): Material Symbols for SF
// Symbols, Roboto for SF Pro, the system back, Material's pull-to-refresh spinner.

package app.ancienttrees.ui

import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.activity.compose.BackHandler
import androidx.compose.animation.core.animateIntAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.snapping.rememberSnapFlingBehavior
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.windowInsetsTopHeight
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyListScope
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Icon
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.Shadow
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.input.nestedscroll.NestedScrollConnection
import androidx.compose.ui.input.nestedscroll.NestedScrollSource
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.layout.layout
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.pluralStringResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.account.AmbassadorAsk
import app.ancienttrees.account.NewFromVisitors
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.feed.Geo
import app.ancienttrees.feed.Here
import app.ancienttrees.feed.Record
import app.ancienttrees.feed.Season
import app.ancienttrees.feed.Shelves
import app.ancienttrees.feed.SpeciesCard
import app.ancienttrees.feed.SpeciesSearch
import app.ancienttrees.feed.Tree
import app.ancienttrees.feed.TreeCollection
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.util.Calendar
import java.util.Locale

/** Where a tap on Discover goes that is not Discover's own page (Home.swift's navigator). */
class DiscoverActions(
    val openTree: (Tree) -> Unit,
    /** A city or a country: the map, framed on it (PlaceLink, never a pushed page). */
    val openPlace: (SearchHit) -> Unit,
    /** A species: its own page (Home.swift NavigationLink(Route.species)). */
    val openSpecies: (String) -> Unit,
    /** Somebody's public profile, signed in (Route.person). */
    val openPerson: (String) -> Unit,
    val showMap: () -> Unit,
    /** Your Want to visit list (My trees). */
    val openWantToVisit: () -> Unit,
    /** The camera, as every other entry to it does (navigator.collectNearby). */
    val addTree: () -> Unit,
    /** Sign in, then [then] once the account is in (nudge.require). */
    val signIn: (then: (() -> Unit)?) -> Unit,
    val searching: (Boolean) -> Unit,
    /** A list or a See all, pushed on Discover's stack (Pages.kt). */
    val openPage: (DiscoverPage) -> Unit = {},
)

/** One page pushed on Discover's own stack: a list, or a See all. */
sealed class DiscoverPage {
    data class Collection(val slug: String) : DiscoverPage()
    data class Index(val kind: IndexKind) : DiscoverPage()
}

enum class IndexKind { CITIES, COUNTRIES, SPECIES, OLDEST }

private val TILE_WIDTH = 120.dp
private val TILE_SHAPE = RoundedCornerShape(12.dp)
private val VISITOR_LINE_HEIGHT = 44.dp
private val VISITOR_LINE_ROOM = 28.dp

@Composable
fun treeCount(n: Int): String = pluralStringResource(R.plurals.discover_trees, n, n)

@Composable
fun DiscoverScreen(
    catalogue: Catalogue,
    origin: Here,
    located: Boolean,
    signedIn: Boolean,
    email: String?,
    wantToVisit: Set<String>,
    token: suspend () -> String?,
    refresh: suspend () -> Unit,
    scrollToTop: Int,
    discoverTo: String?,
    act: DiscoverActions,
    /** A collection a link asked for, with a nonce so the same link twice opens it twice. */
    openCollection: Pair<Long, String>? = null,
    /** The places you look after (Profiles.myPlaces): their ambassador row is not yours to see. */
    myPlaces: List<String> = emptyList(),
) {
    val brand = Brand.colors
    val month = remember { Calendar.getInstance().get(Calendar.MONTH) + 1 }
    // Rebuilt when the catalogue changes, and when a fix arrives or moves a long
    // way: a tenth of a degree is about ten kilometres (Home.swift .task(id:)).
    val deck = remember(catalogue.version, located, (origin.lat * 10).toInt(), (origin.lng * 10).toInt()) {
        Shelves.build(catalogue, origin.lat, origin.lng, located, month)
    }
    var visitorRows by remember { mutableStateOf<List<NewFromVisitors.Row>>(emptyList()) }
    LaunchedEffect(signedIn) { visitorRows = NewFromVisitors.load(token()) }
    LaunchedEffect(openCollection) { openCollection?.let { act.openPage(DiscoverPage.Collection(it.second)) } }
    var searching by remember { mutableStateOf(false) }
    LaunchedEffect(searching) { act.searching(searching) }

    val list = rememberLazyListState()
    val scope = rememberCoroutineScope()
    val density = LocalDensity.current
    // QUICK RETURN (Hidde, 2026-10-12): the header slides away reading down and
    // returns on any scroll up; near the top it is always there.
    var headerHidden by remember { mutableStateOf(false) }
    var headerPx by remember { mutableIntStateOf(with(density) { 140.dp.roundToPx() }) }
    val nearTop by remember {
        derivedStateOf { list.firstVisibleItemIndex == 0 && list.firstVisibleItemScrollOffset < headerPx }
    }
    LaunchedEffect(nearTop) { if (nearTop) headerHidden = false }
    val quickReturn = remember {
        object : NestedScrollConnection {
            override fun onPostScroll(consumed: Offset, available: Offset, source: NestedScrollSource): Offset {
                if (consumed.y < -1f && !nearTop) headerHidden = true
                else if (consumed.y > 1f) headerHidden = false
                return Offset.Zero
            }
        }
    }
    val headerShift by animateIntAsState(
        if (headerHidden) -(headerPx + with(density) { 80.dp.roundToPx() }) else 0,
        // .snappy(duration: 0.25) (Home.swift:261).
        Motion.snappy(0.25f),
        label = "header",
    )
    // Tapping Discover while on Discover scrolls back up.
    LaunchedEffect(scrollToTop) {
        if (scrollToTop > 0) {
            list.animateScrollToItem(0)
            headerHidden = false
        }
    }
    // -discoverto=species or -discoverto=tail scrolls there for the sweep.
    LaunchedEffect(discoverTo, deck) {
        val to = discoverTo ?: return@LaunchedEffect
        delay(1500)
        runCatching { list.scrollToItem(keyIndex(deck, visitorRows, catalogue, to)) }
    }

    var refreshing by remember { mutableStateOf(false) }
    Box(Modifier.fillMaxSize().background(brand.ground).semantics { contentDescription = "explore-home" }) {
        PullToRefreshBox(
            isRefreshing = refreshing,
            onRefresh = { scope.launch { refreshing = true; refresh(); refreshing = false } },
            modifier = Modifier.fillMaxSize(),
        ) {
            LazyColumn(
                state = list,
                contentPadding = PaddingValues(top = with(density) { headerPx.toDp() } + 6.dp),
                modifier = Modifier.fillMaxSize().nestedScroll(quickReturn),
            ) {
                discoverContent(
                    deck, catalogue, origin, located, signedIn, wantToVisit, visitorRows, email, token, act, myPlaces,
                    open = act.openPage,
                )
                item(key = "end") { Spacer(Modifier.height(30.dp + 90.dp)) } // clear of the floating tab bar
            }
        }
        // PINNED, sliding away and back (Home.swift safeAreaInset).
        Column(
            verticalArrangement = Arrangement.spacedBy(20.dp),
            modifier = Modifier
                .offset { androidx.compose.ui.unit.IntOffset(0, headerShift) }
                .onSizeChanged { headerPx = it.height }
                .fillMaxWidth()
                .background(brand.ground)
                .statusBarsPadding()
                .padding(horizontal = 16.dp)
                .padding(top = 4.dp, bottom = 10.dp),
        ) {
            Text(
                stringResource(R.string.tab_discover),
                fontFamily = BrandFace,
                fontWeight = FontWeight.Bold,
                fontSize = 32.sp,
                color = brand.ink,
                modifier = Modifier.semantics { heading() },
            )
            SearchField { searching = true }
        }
        // While the header is away, the status bar keeps a solid strip.
        Box(
            Modifier
                .fillMaxWidth()
                .windowInsetsTopHeight(WindowInsets.statusBars)
                .alpha(if (headerHidden) 1f else 0f)
                .background(brand.ground),
        )
    }


    if (searching) {
        MapSearch(
            catalogue = catalogue,
            origin = origin,
            initial = "",
            onPick = { hit ->
                searching = false
                // A PLACE LANDS ON THE MAP, as the map's own search does (2026-11-03).
                when (hit) {
                    is SearchHit.City, is SearchHit.Country, is SearchHit.Place -> act.openPlace(hit)
                    is SearchHit.Species -> act.openSpecies(hit.name)
                    is SearchHit.OneTree -> act.openTree(hit.tree)
                }
            },
            onBack = { searching = false },
        )
    }
}

/** The LazyColumn index of a section, for -discoverto (counted the way discoverContent emits). */
private fun keyIndex(deck: Shelves, rows: List<NewFromVisitors.Row>, c: Catalogue, to: String): Int {
    val keys = ArrayList<String>()
    keys += "discover-top"
    if (deck.best.size >= 3) keys += "best"
    if (rows.count { c.tree(it.treeId) != null } >= NewFromVisitors.MINIMUM) keys += "visitors"
    keys += "cities"
    deck.here?.let { (slug, _) -> if (c.ambassadors(slug).isEmpty() && !c.seated(slug)) keys += "ambassador" }
    if (deck.records.size == 3) keys += "records"
    if (deck.lists.size >= 3) keys += "lists"
    if (deck.countries.isNotEmpty()) keys += "countries"
    keys += "discover-want"
    if (deck.species.isNotEmpty()) keys += "discover-species"
    if (deck.islands.size >= 3) keys += "islands"
    keys += "growing"
    keys += "discover-tail"
    return keys.indexOf("discover-$to").coerceAtLeast(0)
}

/** Home.swift's search field, a button that opens MapSearch. */
@Composable
private fun SearchField(onClick: () -> Unit) {
    val brand = Brand.colors
    Row(
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .fillMaxWidth()
            .height(50.dp)
            // The iPhone's soft drop (black 6%, radius 6, y 2). Android scales a
            // shadow colour down again by its own ambient and spot alpha, so the
            // same visible softness needs stronger numbers here (measured 2026-11-10).
            .shadow(6.dp, CircleShape, ambientColor = Color.Black.copy(alpha = 0.18f), spotColor = Color.Black.copy(alpha = 0.32f))
            .background(brand.surface, CircleShape)
            .border(1.dp, brand.hairline, CircleShape)
            .clip(CircleShape)
            .clickable(onClick = onClick)
            .padding(horizontal = 16.dp)
            .semantics { contentDescription = "explore-search" },
    ) {
        Icon(Sym.SearchSemibold, null, tint = brand.ink, modifier = Modifier.size(22.dp))
        Text(
            stringResource(R.string.discover_search),
            fontSize = 16.sp,
            fontWeight = FontWeight.Medium,
            color = brand.inkSoft,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
        )
    }
}

// MARK: - the page, in Hidde's order (2026-10-13): finding first, your own list
// and the asks after, the index rows last.

private fun LazyListScope.discoverContent(
    deck: Shelves,
    c: Catalogue,
    origin: Here,
    located: Boolean,
    signedIn: Boolean,
    want: Set<String>,
    visitorRows: List<NewFromVisitors.Row>,
    email: String?,
    token: suspend () -> String?,
    act: DiscoverActions,
    myPlaces: List<String>,
    open: (DiscoverPage) -> Unit,
) {
    fun tag(t: Tree): String = tagFor(t, origin, located)

    block("discover-top", first = true) { SeasonHeroOrBand(deck, origin) { act.openTree(it) } }

    if (deck.best.size >= 3) {
        block("best") {
            Section(stringResource(R.string.discover_best)) { TileShelf(deck.best, ::tag, act.openTree) }
        }
    }

    // NEW FROM VISITORS (Hidde, 2026-11-06): one tile per tree, the person under it.
    val fresh = visitorRows.mapNotNull { r -> c.tree(r.treeId)?.let { r to it } }
    if (fresh.size >= NewFromVisitors.MINIMUM) {
        block("visitors") {
            Section(stringResource(R.string.discover_visitors)) {
                Shelf(Modifier.trimBottom(VISITOR_LINE_ROOM)) {
                    items(fresh, key = { it.first.sightingId }) { (row, tree) ->
                        Column(verticalArrangement = Arrangement.spacedBy(7.dp)) {
                            Tile(tree, tree.city, Modifier.width(TILE_WIDTH).semantics { contentDescription = "visitor-tile" }) { act.openTree(tree) }
                            VisitorLine(row, signedIn, act)
                        }
                    }
                }
            }
        }
    }

    block("cities") {
        Section(stringResource(R.string.discover_cities), seeAll = { open(DiscoverPage.Index(IndexKind.CITIES)) }) {
            Shelf(Modifier.padding(bottom = 4.dp)) {
                items(deck.cities.take(14), key = { it.slug }) { city ->
                    PlaceCard(city.name, treeCount(city.count), c.faceOfCity(city.slug)) {
                        act.openPlace(SearchHit.City(city.slug, city.name, 0.0, 0.0))
                    }
                }
            }
        }
    }

    // The open seat of the city you are standing in, right after the cities (Hidde, 2026-10-14).
    deck.here?.let { (slug, name) ->
        if (c.ambassadors(slug).isEmpty() && !c.seated(slug)) {
            block("ambassador") {
                AmbassadorWantedRow(name, signedIn, email, token, act, myPlaces, Modifier.padding(horizontal = 16.dp))
            }
        }
    }

    if (deck.records.size == 3) {
        block("records") {
            Section(stringResource(R.string.discover_records)) {
                Shelf {
                    items(deck.records, key = { it.kind.name }) { r ->
                        Tile(r.tree, recordLabel(r), Modifier.width(TILE_WIDTH)) {
                            when (r.kind) {
                                Record.Kind.OLDEST -> open(DiscoverPage.Index(IndexKind.OLDEST))
                                else -> r.collection?.let { open(DiscoverPage.Collection(it)) }
                            }
                        }
                    }
                }
            }
        }
    }

    if (deck.lists.size >= 3) {
        block("lists") {
            Section(stringResource(R.string.discover_lists)) {
                Shelf {
                    items(deck.lists, key = { it.collection.slug }) { l ->
                        Tile(l.face, l.collection.title, Modifier.width(TILE_WIDTH)) { open(DiscoverPage.Collection(l.collection.slug)) }
                    }
                }
            }
        }
    }

    if (deck.countries.isNotEmpty()) {
        block("countries") {
            Section(stringResource(R.string.discover_countries), seeAll = { open(DiscoverPage.Index(IndexKind.COUNTRIES)) }) {
                Shelf(Modifier.padding(bottom = 4.dp)) {
                    items(deck.countries.take(14), key = { it.name }) { k ->
                        PlaceCard(k.name, treeCount(k.count), k.photo) { act.openPlace(SearchHit.Country(k.name)) }
                    }
                }
            }
        }
    }

    // Full or empty, one place, below the finding rows (Hidde, 2026-10-13).
    block("discover-want") {
        val mine = want.mapNotNull { c.tree(it) }.sortedBy { Geo.km(origin.lat, origin.lng, it.lat, it.lng) }
        if (mine.isNotEmpty()) WantToVisitFull(mine, ::tag, act) else WantToVisitEmpty(signedIn, act)
    }

    if (deck.species.isNotEmpty()) {
        block("discover-species") {
            Section(stringResource(R.string.discover_species), seeAll = { open(DiscoverPage.Index(IndexKind.SPECIES)) }) {
                SpeciesRows(deck.species) { act.openSpecies(it) }
            }
        }
    }

    if (deck.islands.size >= 3) {
        block("islands") {
            Section(stringResource(R.string.discover_islands)) {
                Shelf {
                    items(deck.islands.take(6), key = { it.slug }) { isl ->
                        c.faceOfCity(isl.slug)?.let { face ->
                            Tile(face, isl.name, Modifier.width(TILE_WIDTH)) {
                                act.openPlace(SearchHit.City(isl.slug, isl.name, 0.0, 0.0))
                            }
                        }
                    }
                }
            }
        }
    }

    block("growing") { GrowingCard(act.addTree) }

    // DOWN, NOT SIDEWAYS, AND IT DOES NOT END (Hidde, 2026-10-10): a grid of
    // three, nearest first. Only the rows on screen are drawn.
    if (deck.tail.isNotEmpty()) {
        block("discover-tail") {
            ShelfHeader(
                stringResource(if (located) R.string.discover_more_near else R.string.discover_more_trees),
                seeAll = act.showMap,
            )
        }
        val rows = deck.tail.chunked(3)
        items(rows.size, key = { "tail-$it" }) { i ->
            Row(
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                modifier = Modifier.padding(horizontal = 16.dp).padding(top = if (i == 0) 12.dp else 6.dp),
            ) {
                for (t in rows[i]) Tile(t, tag(t), Modifier.weight(1f).semantics { contentDescription = "tree-card" }) { act.openTree(t) }
                repeat(3 - rows[i].size) { Spacer(Modifier.weight(1f)) }
            }
        }
    }
}

/** One block of the page, 30 below the one before (Home.swift's VStack spacing). */
private fun LazyListScope.block(key: String, first: Boolean = false, content: @Composable () -> Unit) {
    item(key = key) {
        Column {
            if (!first) Spacer(Modifier.height(30.dp))
            content()
        }
    }
}

/** The tag on a tree tile: its city, and the distance within a day trip (Hidde, 2026-10-10). */
private fun tagFor(t: Tree, origin: Here, located: Boolean): String {
    if (!located) return t.city
    val d = Geo.km(origin.lat, origin.lng, t.lat, t.lng)
    if (d > 30) return t.city
    return "${t.city} · " + if (d < 10) String.format(Locale.US, "%.1f km", d) else "${Math.round(d)} km"
}

@Composable
private fun recordLabel(r: Record): String = when (r.kind) {
    Record.Kind.OLDEST -> r.label?.let { stringResource(R.string.discover_oldest_age, it) } ?: stringResource(R.string.discover_oldest)
    Record.Kind.THICKEST -> r.label?.let { stringResource(R.string.discover_thickest_m, it) } ?: stringResource(R.string.discover_thickest)
    Record.Kind.TALLEST -> stringResource(R.string.discover_tallest)
}

/** Takes [room] back off the bottom of a view without moving it (SwiftUI's negative padding). */
private fun Modifier.trimBottom(room: Dp): Modifier = layout { measurable, constraints ->
    val p = measurable.measure(constraints)
    val cut = room.roundToPx()
    layout(p.width, (p.height - cut).coerceAtLeast(0)) { p.place(0, 0) }
}

// MARK: - pieces

/** Home.swift section(): a ShelfHeader and its content, 12 apart. */
@Composable
private fun Section(title: String, seeAll: (() -> Unit)? = null, content: @Composable () -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        ShelfHeader(title, seeAll)
        content()
    }
}

/** Style.swift ShelfHeader: the title and See all on one line. */
@Composable
fun ShelfHeader(title: String, seeAll: (() -> Unit)? = null) {
    val brand = Brand.colors
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
    ) {
        Text(
            title,
            fontFamily = BrandFace,
            fontWeight = FontWeight.Bold,
            fontSize = 21.sp,
            color = brand.ink,
            modifier = Modifier.weight(1f).semantics { heading() },
        )
        if (seeAll != null) {
            Row(
                horizontalArrangement = Arrangement.spacedBy(3.dp),
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier
                    .heightIn(min = 44.dp)
                    .padding(start = 8.dp)
                    .clickable(interactionSource = remember { MutableInteractionSource() }, indication = androidx.compose.foundation.LocalIndication.current, onClick = seeAll),
            ) {
                Text(stringResource(R.string.see_all), fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = brand.moss)
                Icon(Sym.ChevronRight, null, tint = brand.moss, modifier = Modifier.size(14.dp))
            }
        }
    }
}

/** EVERY SECTION SLIDES (Hidde, 2026-10-10): one shelf, one gap, one snap, the next card peeking. */
@Composable
private fun Shelf(modifier: Modifier = Modifier, spacing: Dp = 12.dp, content: LazyListScope.() -> Unit) {
    val state = rememberLazyListState()
    LazyRow(
        state = state,
        // .viewAligned: a card's leading edge comes to rest on the 16 margin (Home.swift:516).
        flingBehavior = rememberSnapFlingBehavior(state, androidx.compose.foundation.gestures.snapping.SnapPosition.Start),
        contentPadding = PaddingValues(horizontal = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(spacing),
        verticalAlignment = Alignment.Top,
        modifier = modifier.fillMaxWidth(),
        content = content,
    )
}

@Composable
private fun TileShelf(trees: List<Tree>, tag: (Tree) -> String, onOpen: (Tree) -> Unit, ghosts: Int = 0) {
    val brand = Brand.colors
    Shelf {
        items(trees, key = { it.id }) { t ->
            Tile(t, tag(t), Modifier.width(TILE_WIDTH).semantics { contentDescription = "tree-card" }) { onOpen(t) }
        }
        // Grey bookmark tiles finishing a short row, not tappable (Hidde, 2026-10-12, 2026-10-13).
        items(ghosts) {
            Box(
                Modifier.size(TILE_WIDTH, TILE_WIDTH * 4 / 3).clip(TILE_SHAPE).background(brand.surfaceMuted),
                contentAlignment = Alignment.Center,
            ) { GhostMark() }
        }
    }
}

@Composable
private fun GhostMark() {
    Icon(Sym.Bookmark, null, tint = Brand.colors.inkSoft.copy(alpha = 0.45f), modifier = Modifier.size(26.dp))
}

/** CollectedTile.swift (.ours): a photograph in a 3:4 tile and its tag, nothing else. */
@Composable
private fun Tile(tree: Tree, tag: String, modifier: Modifier = Modifier, onOpen: () -> Unit) {
    val brand = Brand.colors
    Box(
        modifier
            .aspectRatio(3f / 4f)
            .clip(TILE_SHAPE)
            .background(brand.surfaceMuted)
            .clickable(interactionSource = remember { MutableInteractionSource() }, indication = androidx.compose.foundation.LocalIndication.current, onClick = onOpen),
    ) {
        val p = tree.photo
        if (p != null) {
            RemoteImage(p.card, null, Modifier.fillMaxSize())
        } else {
            Text(
                tree.name,
                fontFamily = BrandFace,
                fontWeight = FontWeight.Bold,
                fontSize = 12.sp,
                color = brand.inkSoft,
                textAlign = TextAlign.Center,
                maxLines = 4,
                modifier = Modifier.align(Alignment.Center).padding(8.dp),
            )
        }
        if (tag.isNotEmpty()) TagPill(tag, Modifier.align(Alignment.BottomStart).padding(6.dp))
    }
}

/** THE tag (Hidde, 2026-10-10: white background, green letters). */
@Composable
fun TagPill(text: String, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    Text(
        text,
        fontSize = 10.sp,
        fontWeight = FontWeight.SemiBold,
        color = brand.moss,
        maxLines = 2,
        overflow = TextOverflow.Ellipsis,
        lineHeight = 12.sp,
        modifier = modifier.background(brand.surface, RoundedCornerShape(8.dp)).padding(horizontal = 6.dp, vertical = 3.dp),
    )
}

/** A place: wide, because a place is a landscape (Airbnb's destination row). */
@Composable
private fun PlaceCard(name: String, sub: String, cover: Tree?, onOpen: () -> Unit) {
    Box(
        Modifier
            .size(172.dp, 120.dp)
            .clip(RoundedCornerShape(14.dp))
            .background(leafTile())
            .clickable(interactionSource = remember { MutableInteractionSource() }, indication = androidx.compose.foundation.LocalIndication.current, onClick = onOpen),
    ) {
        val url = cover?.photo?.card
        if (url != null) {
            RemoteImage(url, null, Modifier.fillMaxSize())
        } else {
            SpeciesMark(cover?.species ?: "Pedunculate Oak", Color.White.copy(alpha = 0.85f), Modifier.size(46.dp).align(Alignment.Center))
        }
        Box(Modifier.fillMaxSize().background(Brush.verticalGradient(0.5f to Color.Transparent, 1f to Color.Black.copy(alpha = 0.55f))))
        Column(Modifier.align(Alignment.BottomStart).padding(10.dp), verticalArrangement = Arrangement.spacedBy(1.dp)) {
            Text(name, fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Color.White, maxLines = 1, overflow = TextOverflow.Ellipsis)
            Text(sub, fontSize = 11.sp, color = Color.White.copy(alpha = 0.85f))
        }
    }
}

/** THE SEASON (hero H1), or the stock hero in the rare month nothing on your half peaks. */
@Composable
private fun SeasonHeroOrBand(deck: Shelves, origin: Here, onOpen: (Tree) -> Unit) {
    val s = deck.season
    val url = s?.hero?.photo?.let { it.hero ?: it.thumb ?: it.url }
    if (s == null || url == null) {
        HeroBand()
        return
    }
    val word = stringResource(
        when (s.word) {
            Season.SPRING -> R.string.season_spring
            Season.SUMMER -> R.string.season_summer
            Season.AUTUMN -> R.string.season_autumn
            Season.WINTER -> R.string.season_winter
        },
    )
    val line = stringResource(R.string.discover_season_count, treeCount(s.count)) +
        if (s.near > 0) stringResource(R.string.discover_season_near, s.near) else ""
    val far = Geo.km(origin.lat, origin.lng, s.hero.lat, s.hero.lng) > 30
    val pill = if (far) stringResource(R.string.discover_at_best_in, s.hero.city) else stringResource(R.string.discover_at_best)
    val shadow = Shadow(Color.Black.copy(alpha = 0.3f), Offset(0f, 2f), 12f)
    Box(
        Modifier
            .padding(horizontal = 16.dp)
            .fillMaxWidth()
            .height(240.dp)
            .clip(RoundedCornerShape(14.dp))
            .background(Brand.colors.surfaceMuted)
            .clickable(interactionSource = remember { MutableInteractionSource() }, indication = androidx.compose.foundation.LocalIndication.current) { onOpen(s.hero) }
            .semantics { contentDescription = "discover-season" },
    ) {
        RemoteImage(url, null, Modifier.fillMaxSize())
        Box(Modifier.fillMaxSize().background(Brush.verticalGradient(0.5f to Color.Transparent, 1f to Color.Black.copy(alpha = 0.62f))))
        Column(Modifier.align(Alignment.BottomStart).padding(16.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(
                stringResource(R.string.discover_season_here, word),
                style = TextStyle(shadow = shadow),
                fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 26.sp, color = Color.White,
            )
            Text(
                line,
                style = TextStyle(shadow = shadow),
                fontSize = 15.sp, fontWeight = FontWeight.Medium, color = Color.White.copy(alpha = 0.88f),
            )
        }
        // FAR AWAY, IT SAYS WHERE (Hidde, 2026-10-13).
        TagPill(pill, Modifier.align(Alignment.TopStart).padding(12.dp))
    }
}

@Composable
private fun HeroBand() {
    val context = LocalContext.current
    val i = remember { Heroes.pick(context) }
    val shadow = Shadow(Color.Black.copy(alpha = 0.35f), Offset(0f, 2f), 16f)
    Box(
        Modifier
            .padding(horizontal = 16.dp)
            .fillMaxWidth()
            .height(260.dp)
            .clip(RoundedCornerShape(16.dp))
            .semantics { contentDescription = "Trees worth the walk, wherever you are" },
    ) {
        Image(painterResource(Heroes.image(i)), null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())
        Box(Modifier.fillMaxSize().background(Brush.verticalGradient(0.5f to Color.Transparent, 1f to Color.Black.copy(alpha = 0.62f))))
        Column(Modifier.align(Alignment.BottomStart).padding(16.dp), verticalArrangement = Arrangement.spacedBy(2.dp)) {
            Text(stringResource(R.string.discover_hero_1), style = TextStyle(shadow = shadow), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 26.sp, color = Color.White)
            Text(stringResource(R.string.discover_hero_2), style = TextStyle(shadow = shadow), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 26.sp, color = Brand.colors.gold)
        }
        Heroes.credit(i)?.let {
            Text(it, fontSize = 11.sp, color = Color.White.copy(alpha = 0.7f), modifier = Modifier.align(Alignment.BottomEnd).padding(10.dp))
        }
    }
}

/**
 * Who sent it: a small avatar and the name. A public profile's name shows to
 * everyone; a tap opens the profile, signed out it asks for a sign-in first
 * (Hidde, 2026-11-06). No public profile: "A visitor", not a link. Apple's 44
 * points to tap on a 16 point line, the room hanging below (VISITOR_LINE_ROOM).
 */
@Composable
private fun VisitorLine(r: NewFromVisitors.Row, signedIn: Boolean, act: DiscoverActions) {
    val brand = Brand.colors
    val real = r.authorName
    val name = real ?: stringResource(R.string.discover_a_visitor)
    var m = Modifier.width(TILE_WIDTH).heightIn(min = VISITOR_LINE_HEIGHT)
    if (real != null) {
        m = m.clickable(interactionSource = remember { MutableInteractionSource() }, indication = androidx.compose.foundation.LocalIndication.current) {
            val id = r.authorId
            if (id != null && signedIn) act.openPerson(id) else act.signIn(null)
        }.semantics { contentDescription = "visitor-name" }
    }
    Box(m, contentAlignment = Alignment.TopStart) {
        Row(horizontalArrangement = Arrangement.spacedBy(5.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(Modifier.size(16.dp).clip(CircleShape).background(brand.moss.copy(alpha = 0.15f)), contentAlignment = Alignment.Center) {
                val a = r.authorAvatar
                if (a != null) {
                    RemoteImage(a, null, Modifier.fillMaxSize())
                } else {
                    Text(name.take(1), fontSize = 9.sp, fontWeight = FontWeight.Bold, color = brand.moss)
                }
            }
            Text(name, fontSize = 12.sp, fontWeight = FontWeight.Medium, color = brand.inkSoft, maxLines = 1, overflow = TextOverflow.Ellipsis)
        }
    }
}

/** The sheet's grey pill (Style.swift BrandButtonStyle(prominent: false)): 48 tall, full width. */
@Composable
private fun SecondaryButton(text: String, icon: ImageVector?, modifier: Modifier = Modifier, onClick: () -> Unit) {
    val brand = Brand.colors
    Row(
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically,
        modifier = modifier
            .fillMaxWidth()
            .height(48.dp)
            .clip(CircleShape)
            .background(brand.creamDark)
            .clickable(onClick = onClick),
    ) {
        if (icon != null) {
            Icon(icon, null, tint = brand.ink, modifier = Modifier.size(18.dp))
            Spacer(Modifier.width(8.dp))
        }
        Text(text, fontSize = 16.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
    }
}

/** WANT TO VISIT, with trees: read live from your account (Netflix's My List). */
@Composable
private fun WantToVisitFull(mine: List<Tree>, tag: (Tree) -> String, act: DiscoverActions) {
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        ShelfHeader(stringResource(R.string.want_to_visit), seeAll = act.openWantToVisit)
        TileShelf(mine.take(3), tag, act.openTree, ghosts = maxOf(0, 3 - mine.size))
        // A SHORT LIST STILL INVITES MORE (Hidde, 2026-10-12).
        if (mine.size < 3) {
            SecondaryButton(stringResource(R.string.discover_find_near), Sym.Map, Modifier.padding(horizontal = 16.dp), act.showMap)
        }
    }
}

/** WANT TO VISIT, empty: the row's own shape, and signed out the ask for the account (Hidde, 2026-10-12). */
@Composable
private fun WantToVisitEmpty(signedIn: Boolean, act: DiscoverActions) {
    val brand = Brand.colors
    Column(verticalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.semantics { contentDescription = "discover-favourites-empty" }) {
        ShelfHeader(stringResource(R.string.want_to_visit))
        Shelf {
            items(3) { i ->
                Box(
                    Modifier.size(TILE_WIDTH, TILE_WIDTH * 4 / 3).clip(TILE_SHAPE).background(brand.surfaceMuted),
                    contentAlignment = Alignment.Center,
                ) { if (i == 0) GhostMark() }
            }
        }
        if (signedIn) {
            SecondaryButton(stringResource(R.string.discover_find_near), Sym.Map, Modifier.padding(horizontal = 16.dp), act.showMap)
        } else {
            Text(
                stringResource(R.string.discover_want_signin),
                fontSize = 15.sp,
                color = brand.inkSoft,
                modifier = Modifier.padding(horizontal = 16.dp),
            )
            SecondaryButton(
                stringResource(R.string.sign_in),
                null,
                Modifier.padding(horizontal = 16.dp).semantics { contentDescription = "discover-want-signin" },
            ) { act.signIn(null) }
        }
    }
}

/** THREE ROWS OF SPECIES THAT SCROLL TOGETHER (Hidde, 2026-10-10), dealt across the rows in turn. */
@Composable
private fun SpeciesRows(species: List<SpeciesCard>, onOpen: (String) -> Unit) {
    val rows = (0 until 3).map { r -> species.filterIndexed { i, _ -> i % 3 == r } }
    Column(
        verticalArrangement = Arrangement.spacedBy(8.dp),
        modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()).padding(horizontal = 16.dp),
    ) {
        for (row in rows) {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                for (sp in row) SpeciesPill(sp) { onOpen(sp.name) }
            }
        }
    }
}

@Composable
private fun SpeciesPill(sp: SpeciesCard, onClick: () -> Unit) {
    val brand = Brand.colors
    Row(
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .height(44.dp)
            .background(brand.surface, CircleShape)
            .border(1.dp, brand.hairline, CircleShape)
            .clip(CircleShape)
            .clickable(onClick = onClick)
            .padding(start = 5.dp, end = 12.dp),
    ) {
        Box(Modifier.size(34.dp).clip(CircleShape).background(brand.surfaceMuted)) {
            sp.photo?.photo?.card?.let { RemoteImage(it, null, Modifier.fillMaxSize()) }
        }
        Text(sp.name, fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 14.sp, color = brand.ink, maxLines = 1)
        Text("${sp.count}", fontSize = 13.sp, color = brand.inkSoft, style = TextStyle(fontFeatureSettings = "tnum"))
    }
}

/** THE MAP IS NOT FINISHED, said out loud at the end of the browsing (Hidde, 2026-08-29). */
@Composable
private fun GrowingCard(addTree: () -> Unit) {
    val brand = Brand.colors
    Column(
        verticalArrangement = Arrangement.spacedBy(10.dp),
        modifier = Modifier
            .padding(horizontal = 16.dp)
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(brand.surface)
            .border(1.dp, brand.hairline, RoundedCornerShape(12.dp))
            .padding(16.dp),
    ) {
        Text(stringResource(R.string.discover_growing_title), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 19.sp, color = brand.ink)
        Text(stringResource(R.string.discover_growing_body), fontSize = 15.sp, color = brand.inkSoft)
        SecondaryButton(stringResource(R.string.discover_add_tree), Sym.PhotoCameraFill, onClick = addTree)
    }
}

/**
 * The open seat (AmbassadorBadge.swift AmbassadorWantedRow, look .row): the
 * whole row is the control (Hidde, 2026-10-04), a plain button on a scrolling
 * page (2026-11-08). Signed out it asks for the account first, then the
 * explainer; nothing is sent until Apply.
 */
@Composable
private fun AmbassadorWantedRow(
    place: String,
    signedIn: Boolean,
    email: String?,
    token: suspend () -> String?,
    act: DiscoverActions,
    myPlaces: List<String>,
    modifier: Modifier = Modifier,
) {
    // You look after this place already, so the ask is not yours (AmbassadorBadge.swift isMine).
    if (myPlaces.any { it.equals(place, ignoreCase = true) }) return
    val brand = Brand.colors
    val scope = rememberCoroutineScope()
    var asked by remember { mutableStateOf(false) }
    var sending by remember { mutableStateOf(false) }
    var confirming by remember { mutableStateOf(false) }
    var sent by remember { mutableStateOf(false) }
    var failed by remember { mutableStateOf(false) }
    LaunchedEffect(signedIn) { asked = AmbassadorAsk.asked(place, token()) }
    fun tap() {
        if (!signedIn) act.signIn { confirming = true } else confirming = true
    }
    Row(
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        verticalAlignment = Alignment.CenterVertically,
        modifier = modifier
            .fillMaxWidth()
            .heightIn(min = 44.dp)
            .clickable(enabled = !(asked || sending), onClick = ::tap)
            .semantics { contentDescription = "ambassador-wanted" },
    ) {
        Box(Modifier.size(32.dp), contentAlignment = Alignment.Center) {
            val moss = brand.moss
            Canvas(Modifier.fillMaxSize()) {
                val w = 1.5.dp.toPx()
                drawCircle(
                    moss,
                    radius = size.minDimension / 2 - w / 2,
                    style = Stroke(w, pathEffect = PathEffect.dashPathEffect(floatArrayOf(3.dp.toPx(), 3.dp.toPx()))),
                )
            }
            Icon(Sym.Verified, null, tint = moss, modifier = Modifier.size(16.dp))
        }
        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(1.dp)) {
            Text(stringResource(R.string.discover_ambassador_wanted, place), fontSize = 14.sp, fontWeight = FontWeight.Bold, color = brand.ink)
            if (asked) Text(stringResource(R.string.discover_request_sent), fontSize = 12.sp, color = brand.inkSoft)
        }
        if (!asked) {
            Icon(Sym.ChevronRight, null, tint = brand.inkSoft.copy(alpha = 0.6f), modifier = Modifier.size(18.dp))
        }
    }
    if (confirming) {
        val close = { confirming = false; sent = false }
        // ONE SHEET WITH TWO STEPS (AmbassadorBadge.swift AmbassadorApplySheet on
        // Kit/BrandSheet.swift): the explainer and its one button, then the receipt.
        if (sent) {
            BrandSheet(
                title = stringResource(R.string.discover_amb_sent_title),
                icon = Sym.Check,
                message = stringResource(R.string.discover_amb_sent_body) +
                    (email?.let { stringResource(R.string.discover_amb_write_to, it) } ?: ""),
                onDismiss = close,
                buttons = listOf(SheetButton(stringResource(R.string.discover_done), SheetKind.PRIMARY, action = close)),
            )
        } else {
            BrandSheet(
                title = stringResource(R.string.discover_amb_title, place),
                icon = Sym.Verified,
                message = stringResource(R.string.discover_amb_message),
                points = listOf(
                    stringResource(R.string.discover_amb_p1),
                    stringResource(R.string.discover_amb_p2),
                    stringResource(R.string.discover_amb_p3),
                ),
                onDismiss = close,
                buttons = listOf(
                    SheetButton(stringResource(if (sending) R.string.discover_sending else R.string.discover_apply), SheetKind.PRIMARY) {
                        if (sending) return@SheetButton
                        sending = true
                        scope.launch {
                            // A request needs a LIVE session: no token opens the sign-in first.
                            val t = token()
                            if (t == null) {
                                sending = false
                                confirming = false
                                act.signIn { confirming = true }
                                return@launch
                            }
                            val ok = AmbassadorAsk.request(place, t)
                            sending = false
                            if (ok) {
                                asked = true
                                sent = true
                            } else {
                                confirming = false
                                failed = true
                            }
                        }
                    },
                    SheetButton(stringResource(R.string.discover_not_now), SheetKind.QUIET, action = close),
                ),
            )
        }
    }
    if (failed) {
        // News is the iPhone's snackbar; one line on the one sheet until Android has a shared one.
        BrandSheet(
            title = stringResource(R.string.discover_amb_failed),
            onDismiss = { failed = false },
            buttons = listOf(SheetButton(stringResource(R.string.discover_done), SheetKind.PRIMARY) { failed = false }),
        )
    }
}

// MARK: - the pages behind the shelves

/** A pushed page's top bar: back and an inline title (navigationBarTitleDisplayMode(.inline)). */
@Composable
private fun PageBar(title: String, onBack: () -> Unit) {
    val brand = Brand.colors
    Box(Modifier.fillMaxWidth().statusBarsPadding().height(44.dp)) {
        Box(
            Modifier.align(Alignment.CenterStart).size(44.dp).clickable(onClick = onBack),
            contentAlignment = Alignment.Center,
        ) {
            Icon(
                Sym.ArrowBack,
                stringResource(R.string.back), tint = brand.ink, modifier = Modifier.size(22.dp),
            )
        }
        Text(
            title, fontSize = 17.sp, fontWeight = FontWeight.SemiBold, color = brand.ink, maxLines = 1,
            overflow = TextOverflow.Ellipsis, textAlign = TextAlign.Center,
            modifier = Modifier.align(Alignment.Center).padding(horizontal = 52.dp),
        )
    }
}

/** A Discover page on the stack (Pages.kt): a list, or a See all. */
@Composable
fun DiscoverPageScreen(p: DiscoverPage, catalogue: Catalogue, act: DiscoverActions, onBack: () -> Unit) {
    when (p) {
        is DiscoverPage.Collection -> catalogue.collections.firstOrNull { it.slug == p.slug }?.let { c ->
            CollectionPage(c, catalogue, onBack = onBack, onOpen = act.openTree)
        } ?: Box(Modifier.fillMaxSize().background(Brand.colors.ground))
        is DiscoverPage.Index -> IndexPage(p.kind, catalogue, act, onBack = onBack)
    }
}

/** Home.swift CollectionView: the list's intro, then its trees. */
@Composable
private fun CollectionPage(c: TreeCollection, catalogue: Catalogue, onBack: () -> Unit, onOpen: (Tree) -> Unit) {
    val brand = Brand.colors
    Column(Modifier.fillMaxSize().background(brand.ground)) {
        PageBar(c.title, onBack)
        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(14.dp),
            contentPadding = PaddingValues(top = 6.dp, bottom = 90.dp),
        ) {
            c.intro?.takeIf { it.isNotEmpty() }?.let { intro ->
                item { Text(intro, fontSize = 16.sp, color = brand.inkSoft, modifier = Modifier.padding(horizontal = 16.dp).padding(top = 4.dp)) }
            }
            items(catalogue.treesOf(c), key = { it.id }) { t ->
                TreeCard(t, { onOpen(t) }, Modifier.padding(horizontal = 16.dp))
            }
        }
    }
}

/** IndexPages.swift: the four See all pages, one screen with four kinds of row. */
@Composable
private fun IndexPage(kind: IndexKind, c: Catalogue, act: DiscoverActions, onBack: () -> Unit) {
    val brand = Brand.colors
    var search by remember { mutableStateOf("") }
    fun matches(s: String) = search.isEmpty() || s.lowercase().contains(search.lowercase())
    val title = stringResource(
        when (kind) {
            IndexKind.CITIES -> R.string.discover_index_cities
            IndexKind.COUNTRIES -> R.string.discover_countries
            IndexKind.SPECIES -> R.string.discover_index_species
            IndexKind.OLDEST -> R.string.discover_index_oldest
        },
    )
    Column(Modifier.fillMaxSize().background(brand.ground)) {
        PageBar(title, onBack)
        // .searchable(prompt: "Search"): the field under the title.
        androidx.compose.foundation.text.BasicTextField(
            value = search,
            onValueChange = { search = it },
            singleLine = true,
            textStyle = sfStyle(fontSize = 17.sp, color = brand.ink),
            cursorBrush = androidx.compose.ui.graphics.SolidColor(brand.moss),
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 6.dp).fillMaxWidth(),
            decorationBox = { inner ->
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    modifier = Modifier.fillMaxWidth().height(36.dp).background(brand.surfaceMuted, RoundedCornerShape(10.dp)).padding(horizontal = 8.dp),
                ) {
                    Icon(Sym.Search, null, tint = brand.inkSoft, modifier = Modifier.size(18.dp))
                    Box(Modifier.weight(1f)) {
                        if (search.isEmpty()) Text(stringResource(R.string.discover_index_search), fontSize = 17.sp, color = brand.inkSoft)
                        inner()
                    }
                }
            },
        )
        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(10.dp),
            contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 6.dp, bottom = 80.dp),
        ) {
            when (kind) {
                IndexKind.CITIES -> {
                    val all = c.byCity.map { (slug, ts) -> Triple(slug, ts[0], ts.size) }
                        .filter { matches(it.second.city) || matches(it.second.country) }
                        .sortedByDescending { it.third }
                    items(all, key = { it.first }) { (slug, t, n) ->
                        IndexRow(t.city, t.country, n) { act.openPlace(SearchHit.City(slug, t.city, t.lat, t.lng)) }
                    }
                }
                IndexKind.COUNTRIES -> {
                    val all = c.byCountry.map { (name, ts) -> Triple(name, ts.size, ts.map { it.citySlug }.toSet().size) }
                        .filter { matches(it.first) }
                        .sortedByDescending { it.second }
                    items(all, key = { it.first }) { (name, n, places) ->
                        IndexRow(name, pluralPlaces(places), n) { act.openPlace(SearchHit.Country(name)) }
                    }
                }
                IndexKind.SPECIES -> {
                    val all = c.bySpecies.filter { it.key.isNotEmpty() }.map { it.key to it.value.size }
                        .filter { search.isEmpty() || SpeciesSearch.hit(it.first, c.scientificName(it.first), c.otherNames[it.first].orEmpty(), search) != null }
                        .sortedByDescending { it.second }
                    items(all, key = { it.first }) { (name, n) -> SpeciesIndexRow(name, n) { act.openSpecies(name) } }
                }
                IndexKind.OLDEST -> {
                    val all = c.trees.filter { (it.ageMin ?: 0) > 0 && (matches(it.name) || matches(it.city)) }
                        .sortedByDescending { it.ageMin ?: 0 }.take(120)
                    items(all, key = { it.id }) { t -> TreeCard(t, { act.openTree(t) }, Modifier.padding(bottom = 6.dp)) }
                }
            }
        }
    }
}

@Composable
private fun pluralPlaces(n: Int) = pluralStringResource(R.plurals.discover_places, n, n)

@Composable
private fun IndexRow(title: String, subtitle: String, count: Int, onClick: () -> Unit) {
    val brand = Brand.colors
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 60.dp)
            .clip(RoundedCornerShape(12.dp))
            .background(brand.surface)
            .border(1.dp, brand.hairline, RoundedCornerShape(12.dp))
            .clickable(onClick = onClick)
            .padding(horizontal = 16.dp),
    ) {
        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
            Text(title, fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = brand.ink, maxLines = 1)
            Text(subtitle, fontSize = 12.sp, color = brand.inkSoft, maxLines = 1)
        }
        Text("$count", fontSize = 15.sp, color = brand.inkSoft)
        Icon(Sym.ChevronRight, null, tint = brand.inkSoft.copy(alpha = 0.6f), modifier = Modifier.size(16.dp))
    }
}

@Composable
private fun SpeciesIndexRow(name: String, count: Int, onClick: () -> Unit) {
    val brand = Brand.colors
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 56.dp)
            .clip(RoundedCornerShape(12.dp))
            .background(brand.surface)
            .border(1.dp, brand.hairline, RoundedCornerShape(12.dp))
            .clickable(onClick = onClick)
            .padding(horizontal = 16.dp),
    ) {
        SpeciesMark(name, brand.moss, Modifier.size(30.dp))
        Text(name, fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = brand.ink, maxLines = 1, modifier = Modifier.weight(1f))
        Text("$count", fontSize = 15.sp, color = brand.inkSoft)
        Icon(Sym.ChevronRight, null, tint = brand.inkSoft.copy(alpha = 0.6f), modifier = Modifier.size(16.dp))
    }
}

/** A person's public profile, until the profile screen is ported (data/android-parity.json). */
fun openProfileOnWeb(context: Context, userId: String) {
    val u = Uri.parse("https://ancienttrees.app/profile?u=" + Uri.encode(userId))
    runCatching { context.startActivity(Intent(Intent.ACTION_VIEW, u)) }
}
