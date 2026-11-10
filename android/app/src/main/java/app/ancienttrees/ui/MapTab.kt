// The map tab, ported from ios Screens/MapTab.swift, where Hidde's rulings
// behind every choice here are written down: Google Maps' model (points, not
// lines), the sheet always there with the list or the pin you last tapped, the
// search field fixed at the top at every height, four chips that add up, the
// count small and centred under the grip, Highlights then every tree in view
// as a row (direction C), a search that shows only that place until a finger
// moves the map (Airbnb), and the cross that clears it and leaves the map.

package app.ancienttrees.ui

import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.navigationBars
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Map
import androidx.compose.material.icons.filled.NearMe
import androidx.compose.material.icons.filled.PhotoCamera
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.ConfirmationNumber
import androidx.compose.material.icons.outlined.Eco
import androidx.compose.material.icons.outlined.IosShare
import androidx.compose.material.icons.outlined.LocationOff
import androidx.compose.material.icons.outlined.Park
import androidx.compose.material.icons.outlined.Verified
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.layout
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.layout.positionInRoot
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.feed.Geo
import app.ancienttrees.feed.Here
import app.ancienttrees.feed.Tree
import app.ancienttrees.feed.ViewBox
import app.ancienttrees.map.MoveRequest
import app.ancienttrees.map.TreeMapView
import java.util.Calendar
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.roundToInt

/** The four chips (Kit/MapFilters.swift); each changes only itself. */
data class MapFilters(
    val favouritesOnly: Boolean = false,
    val collectedOnly: Boolean = false,
    val species: String? = null,
    val freeOnly: Boolean = false,
) {
    val isOn: Boolean get() = favouritesOnly || collectedOnly || freeOnly || species != null

    fun keeps(t: Tree, collected: Set<String>, favourites: Set<String>): Boolean {
        if (collectedOnly && t.id !in collected) return false
        if (favouritesOnly && t.id !in favourites) return false
        if (freeOnly && t.paidEntry) return false
        if (species != null && t.commonName != species) return false
        return true
    }
}

/** The city or country the map was sent to: the field keeps its name until its cross. */
sealed class FocusPlace {
    data class City(val slug: String) : FocusPlace()
    data class Country(val name: String) : FocusPlace()
}

/** What a search result asks of the map (MapSearch.Hit). */
sealed class SearchHit {
    data class City(val slug: String, val name: String, val lat: Double, val lng: Double) : SearchHit()
    data class Country(val name: String) : SearchHit()
    data class Species(val name: String) : SearchHit()
    data class OneTree(val tree: Tree) : SearchHit()
}

private data class Listed(val tree: Tree, val km: Double)

/** The map tab's own launch arguments (MapTab.swift debug scaffolding). */
data class MapLaunch(
    val sheet: SheetHeight = SheetHeight.PEEK,
    val select: String? = null,
    val search: String? = null,
)

@Composable
fun MapTab(
    catalogue: Catalogue?,
    origin: Here,
    located: Boolean,
    granted: Boolean,
    locationRefused: Boolean,
    signedIn: Boolean,
    launch: MapLaunch,
    showDot: Boolean,
    onUseMyLocation: () -> Unit,
    onNeedsSignIn: (then: () -> Unit) -> Unit,
    onOpen: (Tree) -> Unit,
    onCollect: (Tree) -> Unit,
    onAddTree: () -> Unit,
    onShare: (Tree) -> Unit,
    onSearching: (Boolean) -> Unit,
    raise: Int,
    /** A place, species or tree a tree page sends here, until their own pages are ported. */
    go: Pair<Long, SearchHit>? = null,
) {
    val brand = Brand.colors
    val density = LocalDensity.current
    val marks = LocalTreeMarks.current
    val sheet = remember { SheetState(launch.sheet) }
    var selected by remember { mutableStateOf<Tree?>(null) }
    var before by remember { mutableStateOf<SheetHeight?>(null) }
    var region by remember { mutableStateOf<ViewBox?>(null) }
    var filters by remember { mutableStateOf(MapFilters()) }
    var focusPlace by remember { mutableStateOf<FocusPlace?>(null) }
    var moveTo by remember { mutableStateOf<MoveRequest?>(null) }
    var recentre by remember { mutableIntStateOf(0) }
    var searching by remember { mutableStateOf(launch.search != null) }
    var pickingSpecies by remember { mutableStateOf(false) }
    var searchBottom by remember { mutableFloatStateOf(0f) }
    var chromeBottom by remember { mutableFloatStateOf(0f) }
    val trees = catalogue?.trees.orEmpty()
    val month = remember { Calendar.getInstance().get(Calendar.MONTH) + 1 }

    LaunchedEffect(searching) { onSearching(searching) }
    LaunchedEffect(raise) { if (raise > 0) sheet.height = SheetHeight.HALF }
    LaunchedEffect(catalogue) {
        val c = catalogue ?: return@LaunchedEffect
        launch.select?.let { id -> c.tree(id)?.let { selected = it } }
    }

    // A tapped pin (TreePlaceSheet.swift PinSelection): the card stop while a
    // tree is chosen, the height it had once it is let go; down to peek lets it go.
    LaunchedEffect(selected?.id) {
        if (selected != null) {
            if (before == null) before = sheet.height
            sheet.height = SheetHeight.CARD
        } else {
            before?.let { sheet.height = it }
            before = null
        }
    }
    LaunchedEffect(sheet.height) {
        if (sheet.height == SheetHeight.PEEK && selected != null) {
            before = null
            selected = null
        }
    }
    BackHandler(enabled = selected != null) { selected = null }

    val focus = region?.let { Here((it.south + it.north) / 2, (it.west + it.east) / 2) } ?: origin
    val box = region ?: ViewBox(origin.lat - 0.05, origin.lng - 0.08, origin.lat + 0.05, origin.lng + 0.08)
    val placeTrees = remember(catalogue, focusPlace) {
        when (val p = focusPlace) {
            is FocusPlace.City -> catalogue?.trees(p.slug).orEmpty()
            is FocusPlace.Country -> catalogue?.treesInCountry(p.name).orEmpty()
            null -> emptyList()
        }
    }
    val placeTitle = when (val p = focusPlace) {
        is FocusPlace.City -> placeTrees.firstOrNull()?.city ?: p.slug
        is FocusPlace.Country -> p.name
        null -> ""
    }
    val filtered = remember(trees, filters, marks.collected, marks.saved) {
        if (!filters.isOn) trees else trees.filter { filters.keeps(it, marks.collected, marks.saved) }
    }
    // WHILE A SEARCH HOLDS, ONLY THAT PLACE'S PINS (Hidde, 2026-11-06).
    val mapTrees = remember(filtered, placeTrees, focusPlace) {
        if (focusPlace == null) filtered else placeTrees.map { it.id }.toSet().let { ids -> filtered.filter { it.id in ids } }
    }
    val source = if (focusPlace == null) trees else placeTrees
    val inReach = remember(source, region, focus, filters, marks.collected, marks.saved) {
        if (region == null) {
            source.count { filters.keeps(it, marks.collected, marks.saved) && Geo.km(focus.lat, focus.lng, it.lat, it.lng) <= 6 }
        } else {
            source.count { box.contains(it.lat, it.lng) && filters.keeps(it, marks.collected, marks.saved) }
        }
    }
    val listed = remember(source, box, focus, filters, marks.collected, marks.saved) {
        val near = source
            .filter { box.contains(it.lat, it.lng) && filters.keeps(it, marks.collected, marks.saved) }
            .map { Listed(it, Geo.km(focus.lat, focus.lng, it.lat, it.lng)) }
            .sortedBy { it.km }
            .take(if (focusPlace == null) 60 else 200)
        leadWithAPhotograph(near)
    }
    // THE TREE YOU ARE STANDING IN FRONT OF, measured from the phone, never the
    // camera, and only with a real fix (MapTab.arrival).
    val arrived = remember(trees, origin, located, selected) {
        if (!located || selected != null) null
        else trees.filter { kotlin.math.abs(it.lat - origin.lat) <= 0.12 / 111.0 * 2 }
            .map { it to Geo.km(origin.lat, origin.lng, it.lat, it.lng) }
            .filter { it.second <= 0.12 }
            .minByOrNull { it.second }?.first
    }
    val nothingInView = inReach == 0 && arrived == null && selected == null && !filters.isOn

    fun fly(lat: Double, lng: Double, metres: Double) {
        val dLat = metres / 2 / 111_320.0
        val dLng = metres / 2 / (111_320.0 * cos(lat * PI / 180)).coerceAtLeast(1.0)
        val b = ViewBox(lat - dLat, lng - dLng, lat + dLat, lng + dLng)
        moveTo = MoveRequest(System.nanoTime(), b)
        region = b
    }

    // What a search result does to the map: one function (MapTab.take).
    fun take(hit: SearchHit) {
        focusPlace = when (hit) {
            is SearchHit.City -> FocusPlace.City(hit.slug)
            is SearchHit.Country -> FocusPlace.Country(hit.name)
            else -> null
        }
        // A PLACE RAISES THE LIST ONE STOP, NEVER LOWERS IT (Hidde, 2026-11-04).
        if ((hit is SearchHit.City || hit is SearchHit.Country) && sheet.height == SheetHeight.PEEK) sheet.height = SheetHeight.CARD
        selected = null
        val c = catalogue ?: return
        when (hit) {
            is SearchHit.City -> {
                val ts = c.trees(hit.slug)
                if (ts.isNotEmpty()) {
                    val minLat = ts.minOf { it.lat }
                    val maxLat = ts.maxOf { it.lat }
                    val minLng = ts.minOf { it.lng }
                    val maxLng = ts.maxOf { it.lng }
                    val cLat = (minLat + maxLat) / 2
                    val latM = (maxLat - minLat) * 111_320
                    val lngM = (maxLng - minLng) * 111_320 * cos(cLat * PI / 180)
                    fly(cLat, (minLng + maxLng) / 2, maxOf(1_500.0, minOf(maxOf(latM, lngM) * 1.35, 60_000.0)))
                } else {
                    fly(hit.lat, hit.lng, 6000.0)
                }
            }
            is SearchHit.Country -> {
                val ts = c.treesInCountry(hit.name)
                if (ts.isNotEmpty()) {
                    val f = c.focus(hit.name)
                    val (s, n, w, e) = if (f != null) {
                        listOf(f.south, f.north, f.west, f.east)
                    } else {
                        // The middle 96 percent, so one island cannot pull the frame to sea.
                        val lats = ts.map { it.lat }.sorted()
                        val lngs = ts.map { it.lng }.sorted()
                        val lo = ((ts.size - 1) * 0.02).toInt()
                        val hi = ((ts.size - 1) * 0.98).toInt()
                        listOf(lats[lo], lats[hi], lngs[lo], lngs[hi])
                    }
                    val cLat = (s + n) / 2
                    val latM = (n - s) * 111_320
                    val lngM = (e - w) * 111_320 * cos(cLat * PI / 180)
                    fly(cLat, (w + e) / 2, maxOf(20_000.0, minOf(maxOf(latM, lngM) * 1.15, 6_000_000.0)))
                }
            }
            is SearchHit.Species -> filters = filters.copy(species = hit.name)
            is SearchHit.OneTree -> {
                fly(hit.tree.lat, hit.tree.lng, 1200.0)
                selected = hit.tree
            }
        }
    }

    LaunchedEffect(go) { go?.let { take(it.second) } }

    val stopCoverage = with(density) {
        when (sheet.height) {
            SheetHeight.PEEK -> SheetStops.PEEK.toPx()
            SheetHeight.CARD -> SheetStops.CARD.toPx()
            else -> sheet.halfPx
        }
    }
    val navBottom = WindowInsets.navigationBars.getBottom(density).toFloat()

    Box(Modifier.fillMaxSize()) {
        TreeMapView(
            trees = mapTrees,
            selected = selected,
            onSelect = { selected = it },
            origin = origin,
            located = located,
            dot = showDot,
            recentre = recentre,
            onView = { region = it },
            onUserMove = { if (focusPlace != null) focusPlace = null },
            topCover = chromeBottom,
            bottomCover = minOf(stopCoverage, sheet.halfPx.takeIf { it > 0 } ?: stopCoverage),
            moveTo = moveTo,
            quietSelect = launch.select,
            modifier = Modifier.fillMaxSize().graphicsLayer { translationY = sheet.parallax() },
        )

        // The locate control and the location chip ride the sheet's top edge
        // (TreeMap.recentrePlacement), then the sheet closes over them.
        val place by remember {
            derivedStateOf {
                with(density) {
                    recentrePlacement(
                        coverage = sheet.points,
                        visible = sheet.screen - navBottom,
                        cardPx = SheetStops.CARD.toPx(),
                        minLift = 120.dp.toPx(),
                        gap = 12.dp.toPx(),
                        fade = 60.dp.toPx(),
                    )
                }
            }
        }
        if (!searching) {
            Box(
                Modifier
                    .fillMaxSize()
                    .navigationBarsPadding()
                    .graphicsLayer { alpha = place.second },
            ) {
                if (!located) {
                    LocationOffChip(
                        refused = locationRefused,
                        onClick = onUseMyLocation,
                        modifier = Modifier
                            .align(Alignment.BottomStart)
                            .offset { IntOffset(12.dp.roundToPx(), -place.first.roundToInt()) },
                    )
                }
                RecentreButton(
                    onClick = {
                        if (granted) recentre++ else onUseMyLocation()
                    },
                    modifier = Modifier
                        .align(Alignment.BottomEnd)
                        .padding(end = 12.dp)
                        .offset { IntOffset(0, -place.first.roundToInt()) },
                )
            }
        }

        MapSheet(
            state = sheet,
            fullInset = if (searchBottom > 0) searchBottom + with(density) { 10.dp.toPx() } else 0f,
            cardFits = selected != null,
            header = {
                val t = selected
                if (t == null) {
                    CountStrip(inReach, full = sheet.height == SheetHeight.FULL)
                } else {
                    TreePlaceHeader(t, onShare = { onShare(t) }, onClose = { selected = null })
                }
            },
        ) {
            val t = selected
            if (t != null) {
                TreePlaceBody(t, onOpen = { onOpen(t) })
            } else {
                Column(
                    Modifier.fillMaxWidth().padding(horizontal = 16.dp).padding(bottom = 110.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp),
                ) {
                    if (arrived != null && sheet.height != SheetHeight.PEEK) {
                        ArrivalCard(arrived, collected = arrived.id in marks.collected, onCollect = { onCollect(arrived) })
                    }
                    if (!nothingInView) {
                        PlaceList(listed, inReach, onOpen)
                    }
                    if (nothingInView) {
                        EmptyPlaceCard(onAdd = onAddTree)
                        catalogue?.let { c ->
                            c.trees.minByOrNull { Geo.km(focus.lat, focus.lng, it.lat, it.lng) }?.let { n ->
                                Column {
                                    Eyebrow("Nearest", Modifier.padding(vertical = 6.dp))
                                    PlainResultRow(
                                        name = n.name,
                                        sub = "${far(Geo.km(focus.lat, focus.lng, n.lat, n.lng))} · ${n.city}",
                                        icon = Icons.Outlined.Park,
                                        inset = 0,
                                        onClick = { onOpen(n) },
                                    )
                                }
                            }
                        }
                    } else if (listed.isEmpty()) {
                        val lookingAtYou = region == null || Geo.km(focus.lat, focus.lng, origin.lat, origin.lng) < 3
                        Text(
                            if (lookingAtYou) "No tree of ours within fifty kilometres." else "No tree of ours in view. Try moving the map.",
                            fontSize = 13.sp,
                            color = brand.inkSoft,
                            textAlign = TextAlign.Center,
                            modifier = Modifier.fillMaxWidth().padding(top = 30.dp),
                        )
                    }
                }
            }
        }

        // The field stays where it is at every height; the chips leave with the
        // map as the sheet becomes the page.
        if (!searching) {
            Column(
                Modifier.fillMaxWidth().statusBarsPadding(),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                SearchField(
                    place = if (focusPlace == null) null else placeTitle,
                    onOpen = { searching = true },
                    onClear = {
                        focusPlace = null
                        selected = null
                    },
                    modifier = Modifier.onGloballyPositioned {
                        searchBottom = it.positionInRoot().y + it.size.height
                    },
                )
                FilterRow(
                    filters = filters,
                    onFavourites = {
                        if (!signedIn) onNeedsSignIn { filters = filters.copy(favouritesOnly = true) }
                        else filters = filters.copy(favouritesOnly = !filters.favouritesOnly)
                    },
                    onCollected = {
                        if (!signedIn) onNeedsSignIn { filters = filters.copy(collectedOnly = true) }
                        else filters = filters.copy(collectedOnly = !filters.collectedOnly)
                    },
                    onSpecies = {
                        if (filters.species != null) filters = filters.copy(species = null) else pickingSpecies = true
                    },
                    onFree = { filters = filters.copy(freeOnly = !filters.freeOnly) },
                    modifier = Modifier
                        .graphicsLayer { alpha = 1f - sheet.pageProgress }
                        .onGloballyPositioned { chromeBottom = it.positionInRoot().y + it.size.height },
                )
            }
        }

        // AT FULL HEIGHT ONLY: the way back to the map (Hidde, 2026-08-25).
        AnimatedVisibility(
            visible = sheet.height == SheetHeight.FULL && !searching,
            enter = fadeIn(),
            exit = fadeOut(),
            modifier = Modifier.align(Alignment.BottomCenter).navigationBarsPadding().padding(bottom = 70.dp),
        ) {
            MapPill { sheet.height = SheetHeight.PEEK }
        }

        if (searching && catalogue != null) {
            MapSearch(
                catalogue = catalogue,
                origin = origin,
                initial = launch.search.orEmpty(),
                onPick = {
                    searching = false
                    take(it)
                },
                onBack = { searching = false },
            )
        }
        if (pickingSpecies && catalogue != null) {
            SpeciesPicker(
                catalogue = catalogue,
                nearby = remember(mapTrees) { mapTrees.map { it.commonName }.toSet() },
                selection = filters.species,
                onPick = { filters = MapFilters(species = it) },
                onDismiss = { pickingSpecies = false },
            )
        }
    }
}

/** Editorial.leadWithAPhotograph: a photograph within the first twelve leads the list. */
private fun leadWithAPhotograph(list: List<Listed>): List<Listed> {
    val first = list.firstOrNull() ?: return list
    if (first.tree.photo != null) return list
    val i = list.take(12).indexOfFirst { it.tree.photo != null }
    if (i < 0) return list
    val out = list.toMutableList()
    out.add(0, out.removeAt(i))
    return out
}

/** EmptyPlace.distance: one decimal under ten. */
private fun far(km: Double): String = if (km < 10) String.format(java.util.Locale.ROOT, "%.1f km", km) else "${km.roundToInt()} km"

/** DIRECTION C: Highlights, Collected, then every tree in view as a row. */
@Composable
private fun PlaceList(listed: List<Listed>, inReach: Int, onOpen: (Tree) -> Unit) {
    val marks = LocalTreeMarks.current
    val highlights = remember(listed) {
        listed.filter { it.tree.isHighlight }.sortedBy { it.tree.highlightRank ?: Int.MAX_VALUE }.take(10)
    }
    if (highlights.isNotEmpty()) {
        SheetSectionHead("Highlights")
        Shelf(highlights.map { it.tree }, onOpen)
    }
    val collected = remember(listed, marks.collected) { listed.filter { it.tree.id in marks.collected }.take(10) }
    if (collected.isNotEmpty()) {
        SheetSectionHead("Collected")
        Shelf(collected.map { it.tree }, onOpen)
    }
    if (listed.isNotEmpty()) {
        SheetSectionHead(
            when {
                inReach > listed.size -> "The ${listed.size} nearest"
                listed.size == 1 -> "The one tree"
                else -> "All ${listed.size} trees"
            },
        )
        Column {
            for (hit in listed) TreeRow(hit.tree) { onOpen(hit.tree) }
        }
    }
}

@Composable
private fun Shelf(trees: List<Tree>, onOpen: (Tree) -> Unit) {
    LazyRow(
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        contentPadding = PaddingValues(horizontal = 16.dp),
        modifier = Modifier.fillMaxWidth().padding(bottom = 6.dp).layoutBleed(16.dp),
    ) {
        items(trees, key = { it.id }) { t -> HighlightCard(t) { onOpen(t) } }
    }
}

/** Reaches past the list's own 16 so the shelf runs to the screen's edges. */
private fun Modifier.layoutBleed(by: androidx.compose.ui.unit.Dp): Modifier =
    this.layout { measurable, constraints ->
        val extra = by.roundToPx() * 2
        val p = measurable.measure(constraints.copy(maxWidth = constraints.maxWidth + extra, minWidth = constraints.minWidth + extra))
        layout(constraints.maxWidth, p.height) { p.place(-by.roundToPx(), 0) }
    }

/** The count, small and centred under the grip; its words go at full height, the strip stays. */
@Composable
private fun CountStrip(inReach: Int, full: Boolean) {
    Text(
        if (inReach == 0) "No trees in view" else "$inReach ${if (inReach == 1) "tree" else "trees"}",
        fontFamily = BrandFace,
        fontWeight = FontWeight.Bold,
        fontSize = 16.sp,
        color = Brand.colors.inkSoft,
        textAlign = TextAlign.Center,
        modifier = Modifier.fillMaxWidth().graphicsLayer { alpha = if (full) 0f else 1f }.padding(bottom = 11.dp),
    )
}

/** Apple Maps' place row (TreePlaceHeader): share, the name and its meta, a cross. */
@Composable
internal fun TreePlaceHeader(tree: Tree, onShare: () -> Unit, onClose: () -> Unit) {
    val brand = Brand.colors
    val meta = listOfNotNull(tree.commonName.ifEmpty { null }, tree.ageShort?.ifEmpty { null } ?: tree.cardAge).joinToString(" · ")
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp).offset(y = (-14).dp).padding(bottom = 2.dp),
    ) {
        PlaceCircle(Icons.Outlined.IosShare, "Share ${tree.name}", onShare)
        Column(Modifier.weight(1f), horizontalAlignment = Alignment.CenterHorizontally) {
            Text(
                tree.name,
                fontFamily = BrandFace,
                fontWeight = FontWeight.Bold,
                fontSize = 20.sp,
                lineHeight = 24.sp,
                color = brand.ink,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
                textAlign = TextAlign.Center,
            )
            if (meta.isNotEmpty()) {
                Text(meta, fontSize = 15.sp, color = brand.inkSoft, maxLines = 1, overflow = TextOverflow.Ellipsis)
            }
        }
        PlaceCircle(Icons.Filled.Close, "Close", onClose)
    }
}

@Composable
private fun PlaceCircle(icon: ImageVector, label: String, onClick: () -> Unit) {
    val brand = Brand.colors
    Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier
            .size(38.dp)
            .background(brand.ink.copy(alpha = 0.08f), CircleShape)
            .clickable(role = Role.Button, onClick = onClick)
            .semantics { contentDescription = label },
    ) {
        Icon(icon, null, tint = brand.ink, modifier = Modifier.size(18.dp))
    }
}

/** The floating search field: the whole sentence, or the place you picked and a cross. */
@Composable
private fun SearchField(place: String?, onOpen: () -> Unit, onClear: () -> Unit, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    Box(modifier.padding(horizontal = 16.dp).padding(top = 6.dp)) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            modifier = Modifier
                .fillMaxWidth()
                .height(50.dp)
                .shadow(8.dp, RoundedCornerShape(50), ambientColor = Color.Black.copy(alpha = 0.10f), spotColor = Color.Black.copy(alpha = 0.10f))
                .background(brand.surface, RoundedCornerShape(50))
                .border(1.dp, brand.hairline, RoundedCornerShape(50))
                .clickable(interactionSource = remember { MutableInteractionSource() }, indication = null, onClick = onOpen)
                .padding(horizontal = 16.dp),
        ) {
            Icon(Icons.Filled.Search, null, tint = brand.ink, modifier = Modifier.size(22.dp))
            Text(
                place ?: SEARCH_PLACEHOLDER,
                fontSize = 16.sp,
                fontWeight = FontWeight.Medium,
                color = if (place == null) brand.inkSoft else brand.ink,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
                modifier = Modifier.weight(1f),
            )
            if (place != null) Spacer(Modifier.width(28.dp))
        }
        if (place != null) {
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier
                    .align(Alignment.CenterEnd)
                    .padding(end = 6.dp)
                    .size(44.dp)
                    .clickable(interactionSource = remember { MutableInteractionSource() }, indication = null, onClick = onClear)
                    .semantics { contentDescription = "Clear" },
            ) {
                Box(Modifier.size(24.dp).background(brand.surfaceMuted, CircleShape), contentAlignment = Alignment.Center) {
                    Icon(Icons.Filled.Close, null, tint = brand.inkSoft, modifier = Modifier.size(13.dp))
                }
            }
        }
    }
}

/** The words on every search field (Kit/Search.swift). */
const val SEARCH_PLACEHOLDER = "Search a place, a tree or a species"

@Composable
private fun FilterRow(
    filters: MapFilters,
    onFavourites: () -> Unit,
    onCollected: () -> Unit,
    onSpecies: () -> Unit,
    onFree: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Row(
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        modifier = modifier.fillMaxWidth().horizontalScroll(rememberScrollState()).padding(horizontal = 16.dp),
    ) {
        FilterChip("Want to visit", Icons.Outlined.BookmarkBorder, filters.favouritesOnly, onFavourites)
        FilterChip("Collected", Icons.Outlined.Verified, filters.collectedOnly, onCollected)
        FilterChip(filters.species ?: "Species", Icons.Outlined.Eco, filters.species != null, onSpecies)
        FilterChip("Free to visit", Icons.Outlined.ConfirmationNumber, filters.freeOnly, onFree)
    }
}

/** FilterChip.swift: a 32 point capsule in a 44 point target. */
@Composable
fun FilterChip(label: String, icon: ImageVector?, on: Boolean, onClick: () -> Unit) {
    val brand = Brand.colors
    Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier
            .height(44.dp)
            .clickable(interactionSource = remember { MutableInteractionSource() }, indication = null, role = Role.Button, onClick = onClick)
            .semantics { selected = on },
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(5.dp),
            modifier = Modifier
                .shadow(if (on) 0.dp else 2.dp, RoundedCornerShape(50), ambientColor = Color.Black.copy(alpha = 0.05f), spotColor = Color.Black.copy(alpha = 0.05f))
                .background(if (on) brand.moss else brand.surface, RoundedCornerShape(50))
                .then(if (on) Modifier else Modifier.border(1.dp, brand.hairline, RoundedCornerShape(50)))
                .padding(horizontal = 12.dp, vertical = 8.dp),
        ) {
            if (icon != null) Icon(icon, null, tint = if (on) Color.White else brand.ink, modifier = Modifier.size(13.dp))
            Text(label, fontFamily = BrandFace, fontWeight = FontWeight.Medium, fontSize = 13.sp, color = if (on) Color.White else brand.ink)
        }
    }
}

/** The way back to the map at full height, in the tab bar's own glass. */
@Composable
private fun MapPill(onClick: () -> Unit) {
    val brand = Brand.colors
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp),
        modifier = Modifier
            .heightIn(min = 44.dp)
            .shadow(8.dp, RoundedCornerShape(50), ambientColor = Color.Black.copy(alpha = 0.18f), spotColor = Color.Black.copy(alpha = 0.18f))
            .background(brand.ground.copy(alpha = 0.96f), RoundedCornerShape(50))
            .clickable(role = Role.Button, onClick = onClick)
            .padding(horizontal = 18.dp, vertical = 11.dp),
    ) {
        Icon(Icons.Filled.Map, null, tint = brand.ink, modifier = Modifier.size(18.dp))
        Text("Map", fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 15.sp, color = brand.ink)
    }
}

/** Back to you, north up (RecentreButton): a rounded square, the moss arrow. */
@Composable
internal fun RecentreButton(onClick: () -> Unit, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    Box(
        contentAlignment = Alignment.Center,
        modifier = modifier
            .size(44.dp)
            .shadow(5.dp, RoundedCornerShape(10.dp), ambientColor = Color.Black.copy(alpha = 0.15f), spotColor = Color.Black.copy(alpha = 0.15f))
            .background(brand.ground.copy(alpha = 0.92f), RoundedCornerShape(10.dp))
            .clickable(role = Role.Button, onClick = onClick)
            .semantics { contentDescription = "Back to my location" },
    ) {
        Icon(Icons.Filled.NearMe, null, tint = brand.moss, modifier = Modifier.size(22.dp))
    }
}

/** Only the ASK survives: "Location off · Use my location". */
@Composable
private fun LocationOffChip(refused: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp),
        modifier = modifier
            .height(44.dp)
            .shadow(6.dp, RoundedCornerShape(50), ambientColor = Color.Black.copy(alpha = 0.12f), spotColor = Color.Black.copy(alpha = 0.12f))
            .background(brand.ground.copy(alpha = 0.96f), RoundedCornerShape(50))
            .clickable(role = Role.Button, onClick = onClick)
            .padding(horizontal = 14.dp),
    ) {
        Icon(Icons.Outlined.LocationOff, null, tint = brand.ink, modifier = Modifier.size(16.dp))
        Text("Location off", fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
        Text("·", fontSize = 15.sp, color = brand.inkSoft)
        Text(if (refused) "Turn on location" else "Use my location", fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = brand.moss)
    }
}

/** The moment the whole product exists for, where the person already is. */
@Composable
private fun ArrivalCard(tree: Tree, collected: Boolean, onCollect: () -> Unit) {
    val brand = Brand.colors
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(10.dp),
        modifier = Modifier.fillMaxWidth().background(brand.surfaceMuted, RoundedCornerShape(14.dp)).padding(16.dp),
    ) {
        Text("You are standing in front of", fontSize = 12.sp, color = brand.inkSoft)
        Text(tree.name, fontSize = 20.sp, fontWeight = FontWeight.Bold, color = brand.ink, textAlign = TextAlign.Center)
        Row(
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier
                .fillMaxWidth()
                .background(if (collected) brand.inkSoft else brand.canopy, RoundedCornerShape(50))
                .clickable(role = Role.Button, onClick = onCollect)
                .padding(vertical = 13.dp),
        ) {
            Icon(if (collected) Icons.Outlined.Verified else Icons.Filled.PhotoCamera, null, tint = Color.White, modifier = Modifier.size(16.dp))
            Spacer(Modifier.width(6.dp))
            Text(if (collected) "Collected" else "Photograph to collect", fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = Color.White)
        }
    }
}

/** EmptyPlaceCard: no trees here yet, and the ask to add the first one. */
@Composable
private fun EmptyPlaceCard(onAdd: () -> Unit) {
    val brand = Brand.colors
    Column(
        verticalArrangement = Arrangement.spacedBy(14.dp),
        modifier = Modifier.fillMaxWidth().background(brand.surfaceMuted, RoundedCornerShape(14.dp)).padding(16.dp),
    ) {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Icon(Icons.Outlined.Park, null, tint = brand.inkSoft.copy(alpha = 0.6f), modifier = Modifier.size(24.dp))
            Text("No trees mapped here yet", fontSize = 16.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
            Text("Know an old tree here? Add the first one.", fontSize = 14.sp, color = brand.inkSoft)
        }
        Row(
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier
                .fillMaxWidth()
                .height(48.dp)
                .background(brand.surface, RoundedCornerShape(50))
                .clickable(role = Role.Button, onClick = onAdd),
        ) {
            Icon(Icons.Filled.PhotoCamera, null, tint = brand.ink, modifier = Modifier.size(17.dp))
            Spacer(Modifier.width(6.dp))
            Text("Add a tree", fontSize = 16.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
        }
    }
}

/** EmptyPlaceRow and MapSearch's row: a moss glyph, a bold name, a small line under it. */
@Composable
fun PlainResultRow(
    name: String,
    sub: String,
    icon: ImageVector,
    inset: Int = 16,
    onClick: () -> Unit,
    title: @Composable (() -> Unit)? = null,
    subLine: @Composable (() -> Unit)? = null,
) {
    val brand = Brand.colors
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(14.dp),
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 56.dp)
            .clickable(onClick = onClick)
            .padding(horizontal = inset.dp),
    ) {
        Icon(icon, null, tint = brand.moss, modifier = Modifier.size(22.dp))
        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
            if (title != null) title() else Text(name, fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = brand.ink, maxLines = 1, overflow = TextOverflow.Ellipsis)
            if (subLine != null) subLine() else Text(sub, fontSize = 12.sp, color = brand.inkSoft, maxLines = 1, overflow = TextOverflow.Ellipsis)
        }
    }
}
