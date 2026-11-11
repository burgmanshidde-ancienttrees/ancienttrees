// My trees: the game, and the only tab that is about you rather than about trees.
// Ported from ios Screens/Collect.swift (CollectView) and Screens/CollectedTile.swift.
// Every ruling behind an order, a size or a word is written beside it in the
// Swift; this file names the Swift piece each part copies.
//
// The map under the sheet is the same live map the map tab draws, and the sheet
// is the same component (MapWithSheet, Hidde 2026-08-26: "je wilt deze interactie
// als component hebben en overal hetzelfde hebben"). Everything shown comes from
// the account and is held in memory only (hard rule 11; account/MyTrees.kt).

package app.ancienttrees.ui

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.util.LruCache
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.wrapContentHeight
import androidx.compose.ui.layout.layout
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.navigationBars
import androidx.activity.compose.BackHandler
import app.ancienttrees.R
import app.ancienttrees.account.MyTrees
import app.ancienttrees.account.OwnSighting
import app.ancienttrees.account.Saves
import app.ancienttrees.account.SentTip
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.feed.Geo
import app.ancienttrees.feed.Here
import app.ancienttrees.feed.Tree
import app.ancienttrees.feed.ViewBox
import app.ancienttrees.map.MoveRequest
import app.ancienttrees.map.TreeMapView
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlin.math.roundToInt

/** Where the page sends you; the screens behind them belong to MainActivity. */
class MyTreesActions(
    val openTree: (Tree) -> Unit,
    val openMine: (String) -> Unit,
    val signIn: () -> Unit,
    val settings: () -> Unit,
    val editProfile: () -> Unit,
    val findPeople: () -> Unit,
    val followList: (followers: Boolean) -> Unit,
    val showMap: () -> Unit,
)

/** CollectView.TreesLane: two lanes, not three (Hidde, 2026-08-24). */
enum class TreesLane { SEEN, WANT }

/** CollectView.TimelineItem: My trees as one list over time. */
private sealed class TimelineItem(val key: String, val date: Long) {
    class Mine(val s: OwnSighting) : TimelineItem("m:" + s.id, s.date)
    class Sent(val t: SentTip) : TimelineItem("s:" + t.id, t.sentAt ?: Long.MIN_VALUE)
    class Ours(val t: Tree, at: Long) : TimelineItem("t:" + t.id, at)
}

@Composable
fun MyTreesScreen(
    catalogue: Catalogue,
    origin: Here,
    located: Boolean,
    granted: Boolean,
    signedIn: Boolean,
    email: String?,
    saves: Saves,
    mine: MyTrees,
    actions: MyTreesActions,
    initialSheet: SheetHeight = SheetHeight.HALF,
    initialLane: TreesLane = TreesLane.SEEN,
    onUseMyLocation: () -> Unit = {},
) {
    PlainText {
        MyTreesInner(catalogue, origin, located, granted, signedIn, email, saves, mine, actions, initialSheet, initialLane, onUseMyLocation)
    }
}

@Composable
private fun MyTreesInner(
    catalogue: Catalogue,
    origin: Here,
    located: Boolean,
    granted: Boolean,
    signedIn: Boolean,
    email: String?,
    saves: Saves,
    mine: MyTrees,
    actions: MyTreesActions,
    initialSheet: SheetHeight,
    initialLane: TreesLane,
    onUseMyLocation: () -> Unit,
) {
    val density = LocalDensity.current
    // -sheet=full opens the sheet as the page (the Polarsteps transition).
    val sheet = remember { SheetState(initialSheet) }
    // OPENS ON YOUR OWN TREES, not on the wishlist (Hidde, 2026-08-26).
    var lane by remember { mutableStateOf(initialLane) }
    // The country chip, nil for all of them (Hidde, 2026-10-09).
    var country by remember { mutableStateOf<String?>(null) }
    var selected by remember { mutableStateOf<Tree?>(null) }
    var before by remember { mutableStateOf<SheetHeight?>(null) }
    var recentre by remember { mutableIntStateOf(0) }

    // SIGNED OUT, THE PAGE KEEPS ITS SHAPE AND LOSES ITS CONTENTS (Hidde, 2026-08-29).
    val shows = signedIn
    val ownTrees = if (shows) mine.yoursOnly else emptyList()
    val byTree = remember(catalogue) { catalogue.trees.associateBy { it.id } }
    val visited = if (shows) saves.collectedAt.entries.sortedByDescending { it.value }.mapNotNull { byTree[it.key] } else emptyList()
    val wishlist = if (shows) saves.heartedAt.entries.sortedByDescending { it.value }.mapNotNull { byTree[it.key] } else emptyList()

    // nearestTree: the tree of ours a find of yours is placed by, worked out ONCE per find.
    val placeOf = remember(mine.version, catalogue) {
        mine.all.associate { s ->
            s.id to (s.treeId?.let { byTree[it] } ?: catalogue.nearest(s.lat, s.lng, 1, 50.0).firstOrNull()?.first)
        }
    }
    val countryOfCity = remember(catalogue) {
        val m = HashMap<String, String>()
        for (t in catalogue.trees) if (t.city !in m) m[t.city] = t.country
        m
    }
    fun countryOf(i: TimelineItem): String? = when (i) {
        is TimelineItem.Ours -> i.t.country
        is TimelineItem.Mine -> placeOf[i.s.id]?.country
        is TimelineItem.Sent -> countryOfCity[i.t.city]
    }
    fun cityOf(i: TimelineItem): String? = when (i) {
        is TimelineItem.Ours -> i.t.city
        is TimelineItem.Mine -> placeOf[i.s.id]?.city
        is TimelineItem.Sent -> i.t.city
    }
    // TICKED TREES ONLY (Hidde, 2026-10-10): a photograph alone does not put one of ours here.
    val timeline = run {
        val items = ArrayList<TimelineItem>()
        if (shows) {
            ownTrees.forEach { items.add(TimelineItem.Mine(it)) }
            mine.sent.forEach { items.add(TimelineItem.Sent(it)) }
            val seen = HashSet<String>()
            for ((id, at) in saves.collectedAt) {
                val t = byTree[id] ?: continue
                if (seen.add(t.id)) items.add(TimelineItem.Ours(t, at))
            }
        }
        items.sortedByDescending { it.date }
    }

    // A tapped pin (TreePlaceSheet.swift PinSelection), as on the map tab.
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
    BackHandler(enabled = selected == null && sheet.height == SheetHeight.FULL) { sheet.height = SheetHeight.HALF }

    // centreOfYours and spanOfYours: the map opens on your collection, or where you are.
    val points = visited.map { it.lat to it.lng } + ownTrees.map { it.lat to it.lng }
    val centre = if (points.isEmpty()) origin else Here(points.map { it.first }.average(), points.map { it.second }.average())
    val span = if (!shows || points.isEmpty()) 3000.0 else {
        val m = maxOf(
            (points.maxOf { it.first } - points.minOf { it.first }) * 111_000,
            (points.maxOf { it.second } - points.minOf { it.second }) * 111_000 * 0.62,
        )
        maxOf(m * 1.4, 1200.0)
    }
    val frame = remember(centre.lat, centre.lng, span) {
        val dLat = span / 2 / 111_320.0
        val dLng = span / 2 / (111_320.0 * kotlin.math.cos(Math.toRadians(centre.lat))).coerceAtLeast(1.0)
        MoveRequest(System.nanoTime(), ViewBox(centre.lat - dLat, centre.lng - dLng, centre.lat + dLat, centre.lng + dLng))
    }
    val ownAsTrees = remember(mine.version, shows) { ownTrees.associate { s -> s.asTree().id to s } }
    val mapTrees = visited + ownAsTrees.values.map { it.asTree() }
    val navBottom = WindowInsets.navigationBars.getBottom(density).toFloat()

    Box(Modifier.fillMaxSize().background(Brand.colors.ground).testTag("collection-tab")) {
        TreeMapView(
            trees = mapTrees,
            selected = selected,
            onSelect = { selected = it },
            origin = centre,
            located = located,
            dot = granted,
            recentre = recentre,
            onView = {},
            moveTo = frame,
            bottomCover = with(density) { if (sheet.height == SheetHeight.PEEK) SheetStops.PEEK.toPx() else sheet.halfPx },
            modifier = Modifier.fillMaxSize().graphicsLayer { translationY = sheet.parallax() },
        )

        // The locate control rides the sheet's top edge, then the sheet closes over it.
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
        Box(Modifier.fillMaxSize().navigationBarsPadding().graphicsLayer { alpha = place.second }) {
            RecentreButton(
                onClick = { if (granted) recentre++ else onUseMyLocation() },
                modifier = Modifier
                    .align(Alignment.BottomEnd)
                    .padding(end = 12.dp)
                    .offset { IntOffset(0, -place.first.roundToInt()) },
            )
        }

        MapSheet(
            state = sheet,
            cardFits = selected != null,
            pageClose = { sheet.height = SheetHeight.HALF },
            header = {
                val t = selected
                if (t != null) {
                    TreePlaceHeader(t, onShare = {}, onClose = { selected = null })
                } else {
                    Box(Modifier.padding(horizontal = 20.dp).padding(bottom = 12.dp)) {
                        WhoYouAre(signedIn, email, mine, actions)
                    }
                }
            },
        ) {
            val t = selected
            if (t != null) {
                val own = ownAsTrees[t.id]
                TreePlaceBody(t, onOpen = { if (own != null) actions.openMine(own.id) else actions.openTree(t) })
            } else {
                Column(
                    Modifier.fillMaxWidth().padding(horizontal = 20.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp),
                ) {
                    // YOUR OWN TREES COUNT AS HAVING STARTED.
                    val nothing = visited.isEmpty() && wishlist.isEmpty() && ownTrees.isEmpty() && mine.sent.isEmpty()
                    if (shows && nothing) Mission(catalogue, origin, located, wishlist, saves, actions)
                    if (!shows || !nothing) {
                        LanePicker(lane) {
                            lane = it
                            country = null
                        }
                        LaneContent(
                            lane = lane,
                            shows = shows,
                            timeline = timeline,
                            wishlist = wishlist,
                            country = country,
                            onCountry = { country = it },
                            countryOf = ::countryOf,
                            cityOf = ::cityOf,
                            mine = mine,
                            actions = actions,
                        )
                    }
                    Spacer(Modifier.height(24.dp))
                }
            }
        }

        // POLARSTEPS' GEAR: it never leaves, and fills in as the list becomes the page.
        SettingsGear(sheet.pageProgress, actions.settings, Modifier.align(Alignment.TopEnd).statusBarsPadding().padding(end = 16.dp)) // at the safe top, as the Swift's floating slot
    }
}

@Composable
private fun SettingsGear(progress: Float, onClick: () -> Unit, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    val label = stringResource(R.string.mt_settings)
    Box(
        modifier
            .size(44.dp)
            .clip(CircleShape)
            .clickable(role = Role.Button, onClick = onClick)
            // The ripple stays inside the shape (Airbnb's line, 2026-11-10).
            .background(brand.surface, CircleShape)
            .semantics { contentDescription = label },
        contentAlignment = Alignment.Center,
    ) {
        Icon(Sym.SettingsMedium, null, tint = brand.ink, modifier = Modifier.size(24.dp).graphicsLayer { alpha = 1f - progress })
        Icon(Sym.SettingsFillMedium, null, tint = brand.ink, modifier = Modifier.size(24.dp).graphicsLayer { alpha = progress })
    }
}

// MARK: - the header (whoYouAre, whoRow)

/**
 * Your profile as the server holds it (account/Profiles.kt) and whether the
 * early-adopter tag shows, provided by MainActivity; the demo seed's MyProfile
 * stands in when nothing is provided.
 */
class MyHeader(
    val profiles: app.ancienttrees.account.Profiles,
    val earlyAdopter: Boolean,
    val openPlace: (slug: String, name: String) -> Unit,
)

val LocalMyHeader = androidx.compose.runtime.staticCompositionLocalOf<MyHeader?> { null }

@Composable
private fun WhoYouAre(signedIn: Boolean, email: String?, mine: MyTrees, actions: MyTreesActions) {
    val header = LocalMyHeader.current
    val p = header?.profiles
    // YOUR TAGS ON THEIR OWN ROW, under the whole header (Collect.swift whoYouAre, spacing 12).
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        WhoRow(signedIn, email, mine, actions, p)
        val places = p?.myPlaces.orEmpty()
        val early = header?.earlyAdopter == true
        if (signedIn && (places.isNotEmpty() || early)) {
            // Collect.swift: .frame(minHeight: 44).padding(.vertical, -9.5), 44 to hit
            // and the pill's own height to lay out; at 44 the tags sat 9 lower.
            Row(
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier
                    .layout { m, c ->
                        val pl = m.measure(c)
                        val t = 9.5.dp.roundToPx()
                        layout(pl.width, (pl.height - 2 * t).coerceAtLeast(0)) { pl.place(0, -t) }
                    }
                    .heightIn(min = 44.dp),
            ) {
                AmbassadorBadge(places, size = 13, open = { a -> header?.openPlace?.invoke(a.placeSlug, a.placeName) })
                if (early) EarlyAdopterBadge(13)
            }
        }
    }
}

@Composable
private fun WhoRow(signedIn: Boolean, email: String?, mine: MyTrees, actions: MyTreesActions, p: app.ancienttrees.account.Profiles?) {
    val brand = Brand.colors
    val demo = mine.profile
    val me = if (p != null) {
        MyProfileView(
            p.me?.displayName?.takeIf { it.isNotEmpty() } ?: demo?.displayName,
            p.me?.avatarUrl ?: demo?.avatarUrl,
            p.myCountry ?: demo?.country,
            if (p.me != null || demo == null) p.followers else demo.followers,
            if (p.me != null || demo == null) p.following else demo.following,
        )
    } else {
        demo?.let { MyProfileView(it.displayName, it.avatarUrl, it.country, it.followers, it.following) }
    }
    val tap = remember { MutableInteractionSource() }
    Row(verticalAlignment = Alignment.CenterVertically) {
        Row(Modifier.weight(1f), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
            // THE PHOTO OPENS THE SAME EDITOR AS THE NAME (Hidde, 2026-09-27).
            val photoLabel = stringResource(if (signedIn) R.string.mt_change_photo else R.string.sign_in)
            Box(
                Modifier
                    .size(60.dp)
                    .clip(CircleShape)
                    .background(brand.moss.copy(alpha = 0.12f))
                    .clickable(interactionSource = tap, indication = androidx.compose.foundation.LocalIndication.current, role = Role.Button) {
                        if (signedIn) actions.editProfile() else actions.signIn()
                    }
                    .semantics { contentDescription = photoLabel },
                contentAlignment = Alignment.Center,
            ) {
                val avatar = if (signedIn) me?.avatarUrl else null
                val initial = (if (signedIn) (me?.displayName ?: email) else null)?.firstOrNull()
                when {
                    avatar != null -> RemoteImage(avatar, null, Modifier.fillMaxSize(), placeholder = false)
                    initial != null -> Text(
                        initial.uppercase(),
                        fontFamily = BrandFace,
                        fontWeight = FontWeight.Black,
                        fontSize = 24.sp,
                        color = brand.moss,
                    )
                    else -> Icon(Sym.PersonFill, null, tint = brand.moss.copy(alpha = 0.6f), modifier = Modifier.size(28.dp))
                }
            }
            Column {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    val name = if (signedIn) {
                        me?.displayName ?: email?.substringBefore("@") ?: stringResource(R.string.mt_your_trees)
                    } else {
                        stringResource(R.string.mt_your_trees)
                    }
                    val nameLabel = stringResource(if (signedIn) R.string.mt_edit_profile else R.string.sign_in)
                    Text(
                        name,
                        fontFamily = BrandFace,
                        fontWeight = FontWeight.Bold,
                        fontSize = 22.sp,
                        lineHeight = 26.sp,
                        color = brand.ink,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis,
                        // Collect.swift: a 44 frame to hit, .padding(.vertical, -8) to lay
                        // out, the name centred in it. Laid out at its own 26 the counts
                        // and badges below sat higher than on the iPhone.
                        modifier = Modifier
                            .weight(1f, fill = false)
                            .layout { m, c ->
                                val p = m.measure(c)
                                val t = 8.dp.roundToPx()
                                layout(p.width, (p.height - 2 * t).coerceAtLeast(0)) { p.place(0, -t) }
                            }
                            .widthIn(min = 44.dp)
                            .heightIn(min = 44.dp)
                            .wrapContentHeight(Alignment.CenterVertically)
                            .clickable(interactionSource = tap, indication = androidx.compose.foundation.LocalIndication.current, role = Role.Button) {
                                if (signedIn) actions.editProfile() else actions.signIn()
                            }
                            .semantics { contentDescription = nameLabel },
                    )
                    // YOUR FLAG AFTER YOUR NAME, Polarsteps' round flag (Hidde, 2026-10-16).
                    if (signedIn) me?.country?.let { CountryFlag(it) }
                }
                if (signedIn) {
                    Row(horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                        Count(me?.followers ?: 0, stringResource(R.string.mt_followers)) { actions.followList(true) }
                        Count(me?.following ?: 0, stringResource(R.string.mt_following)) { actions.followList(false) }
                    }
                } else {
                    Text(stringResource(R.string.mt_signin_prompt), fontSize = 12.sp, color = brand.inkSoft)
                }
            }
        }
        // FIND PEOPLE BESIDE THE NAME (Hidde, 2026-10-01): the gear's twin.
        if (signedIn) {
            val label = stringResource(R.string.mt_find_people)
            Box(
                Modifier
                    .offset(x = 4.dp)
                    .size(44.dp)
                    .clip(CircleShape)
                    .clickable(role = Role.Button, onClick = actions.findPeople)
                    // The ripple stays inside the shape (Airbnb's line, 2026-11-10).
                    .background(brand.surface, CircleShape)
                    .semantics { contentDescription = label },
                contentAlignment = Alignment.Center,
            ) {
                Icon(Sym.PersonAddMedium, null, tint = brand.ink, modifier = Modifier.size(24.dp))
            }
        }
    }
}

private data class MyProfileView(val displayName: String?, val avatarUrl: String?, val country: String?, val followers: Int, val following: Int)

/** "12 followers": the number in ink and semibold, the word soft, 44 to hit. */
@Composable
private fun Count(n: Int, word: String, onClick: () -> Unit) {
    val brand = Brand.colors
    Text(
        buildAnnotatedString {
            withStyle(SpanStyle(fontWeight = FontWeight.SemiBold, color = brand.ink)) { append("$n") }
            append(" $word")
        },
        fontSize = 15.sp,
        color = brand.inkSoft,
        maxLines = 1,
        // Collect.swift: .frame(minHeight: 44) to hit, .padding(.vertical, -12) to
        // lay out, so the counts take 20 and the badges follow close under them.
        // At 30 everything below sat 10 lower than on the iPhone.
        modifier = Modifier
            .layout { m, c ->
                val p = m.measure(c)
                val t = 12.dp.roundToPx()
                layout(p.width, (p.height - 2 * t).coerceAtLeast(0)) { p.place(0, -t) }
            }
            .heightIn(min = 44.dp)
            .wrapContentHeight(Alignment.CenterVertically)
            .clickable(interactionSource = remember { MutableInteractionSource() }, indication = androidx.compose.foundation.LocalIndication.current, role = Role.Button, onClick = onClick),
    )
}

// MARK: - the lanes

/** lanePicker: underlined tabs on the page's left edge, plain words, no counts. */
@Composable
private fun LanePicker(lane: TreesLane, onPick: (TreesLane) -> Unit) {
    val brand = Brand.colors
    Box(Modifier.fillMaxWidth()) {
        Box(Modifier.align(Alignment.BottomStart).fillMaxWidth().height(1.dp).background(brand.hairline))
        Row(horizontalArrangement = Arrangement.spacedBy(24.dp)) {
            LaneTab(stringResource(R.string.mt_collected), lane == TreesLane.SEEN) { onPick(TreesLane.SEEN) }
            LaneTab(stringResource(R.string.want_to_visit), lane == TreesLane.WANT) { onPick(TreesLane.WANT) }
        }
    }
}

@Composable
private fun LaneTab(title: String, on: Boolean, onClick: () -> Unit) {
    val brand = Brand.colors
    val moss = brand.moss
    Text(
        title,
        fontSize = 16.sp,
        fontWeight = FontWeight.SemiBold,
        color = if (on) brand.ink else brand.inkSoft,
        maxLines = 1,
        modifier = Modifier
            .clickable(interactionSource = remember { MutableInteractionSource() }, indication = androidx.compose.foundation.LocalIndication.current, role = Role.Tab, onClick = onClick)
            .semantics { selected = on }
            // The 2 point moss line under the chosen word, on the hairline.
            .drawBehind { if (on) drawRect(moss, Offset(0f, size.height - 2.dp.toPx()), Size(size.width, 2.dp.toPx())) }
            .padding(vertical = 12.dp),
    )
}

@Composable
private fun LaneContent(
    lane: TreesLane,
    shows: Boolean,
    timeline: List<TimelineItem>,
    wishlist: List<Tree>,
    country: String?,
    onCountry: (String?) -> Unit,
    countryOf: (TimelineItem) -> String?,
    cityOf: (TimelineItem) -> String?,
    mine: MyTrees,
    actions: MyTreesActions,
) {
    val brand = Brand.colors
    Column(Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        if (!shows) {
            SignedOutLane(lane, actions.signIn)
            return@Column
        }
        val shots = mine.newestShotByTree
        if (lane == TreesLane.SEEN) {
            val countries = timeline.mapNotNull(countryOf).groupingBy { it }.eachCount().toList()
                .sortedWith(compareByDescending<Pair<String, Int>> { it.second }.thenBy { it.first })
            CountryChips(countries, timeline.size, country, onCountry)
            val shown = if (country == null) timeline else timeline.filter { countryOf(it) == country }
            if (timeline.isEmpty()) {
                Text(stringResource(R.string.mt_collected_empty), fontSize = 15.sp, color = brand.inkSoft, modifier = Modifier.padding(top = 4.dp))
            } else {
                // THREE ACROSS, Instagram's profile grid, Discover's rounded tiles.
                Grid(Modifier.padding(top = 2.dp), shown.map { item ->
                    @Composable {
                        when (item) {
                            is TimelineItem.Mine -> CollectedTile(cityOf(item), Modifier.clickable { actions.openMine(item.s.id) }) {
                                OwnPhoto(item.s, mine, Modifier.fillMaxSize()) { Named(item.s.name) }
                            }
                            is TimelineItem.Sent -> CollectedTile(item.t.city) { Named(item.t.title) }
                            is TimelineItem.Ours -> CollectedTile(item.t.city, Modifier.clickable { actions.openTree(item.t) }.semantics { contentDescription = item.t.name }) {
                                OursPicture(item.t, shots[item.t.id], mine)
                            }
                        }
                    }
                })
            }
        } else {
            val countries = wishlist.groupingBy { it.country }.eachCount().toList()
                .sortedWith(compareByDescending<Pair<String, Int>> { it.second }.thenBy { it.first })
            CountryChips(countries, wishlist.size, country, onCountry)
            val list = wishlist.filter { country == null || it.country == country }
            if (list.isEmpty()) {
                WantEmpty(actions.showMap)
            } else {
                // THE SAME GRID as Collected (Hidde, 2026-10-09).
                val tiles: List<@Composable () -> Unit> = list.map { t ->
                    @Composable {
                        CollectedTile(t.city, Modifier.clickable { actions.openTree(t) }.semantics { contentDescription = t.name }) {
                            OursPicture(t, shots[t.id], mine)
                        }
                    }
                }
                // A SHORT LIST STILL INVITES MORE (Hidde, 2026-10-12): ghost tiles finish the row.
                val ghosts: List<@Composable () -> Unit> =
                    if (country == null && list.size < 3) List(3 - list.size) { @Composable { WantGhost(Modifier.clip(TILE)) } } else emptyList()
                Grid(Modifier, tiles + ghosts)
                if (country == null && list.size < 3) WantInvite(actions.showMap)
            }
        }
    }
}

private val TILE = RoundedCornerShape(12.dp)

/** LazyVGrid, three flexible columns 6 apart, in a list that already scrolls. */
@Composable
private fun Grid(modifier: Modifier, tiles: List<@Composable () -> Unit>) {
    Column(modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        for (row in tiles.chunked(3)) {
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                for (tile in row) Box(Modifier.weight(1f)) { tile() }
                repeat(3 - row.size) { Spacer(Modifier.weight(1f)) }
            }
        }
    }
}

/** The country chips, only when there is more than one country to choose between. */
@Composable
private fun CountryChips(countries: List<Pair<String, Int>>, total: Int, country: String?, onCountry: (String?) -> Unit) {
    if (countries.size <= 1) return
    Row(
        Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()).padding(horizontal = 1.dp).offset(y = (-6).dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        FilterChip(stringResource(R.string.mt_all, total), null, country == null) { onCountry(null) }
        for ((name, n) in countries) {
            FilterChip("$name $n", null, country == name) { onCountry(if (country == name) null else name) }
        }
    }
}

/** CollectedTile: a photograph in a 3:4 tile, its city on a tag, nothing else. */
@Composable
private fun CollectedTile(city: String?, modifier: Modifier = Modifier, picture: @Composable () -> Unit) {
    Box(
        Modifier
            .fillMaxWidth()
            .aspectRatio(3f / 4f)
            .clip(TILE)
            .then(modifier),
    ) {
        picture()
        if (!city.isNullOrEmpty()) TagPill(city, Modifier.align(Alignment.BottomStart).padding(6.dp))
    }
}

/** A tree of ours: your newest photograph of it, else ours, else its name. */
@Composable
private fun OursPicture(t: Tree, ownShot: OwnSighting?, mine: MyTrees) {
    val brand = Brand.colors
    when {
        ownShot != null -> OwnPhoto(ownShot, mine, Modifier.fillMaxSize()) { Box(Modifier.fillMaxSize().background(brand.surfaceMuted)) }
        t.photo != null -> RemoteImage(t.photo.card, null, Modifier.fillMaxSize(), fallback = { Box(Modifier.fillMaxSize().background(brand.surfaceMuted)) })
        else -> Named(t.name)
    }
}

/** A tree with no photograph still gets its square: its name on the muted ground. */
@Composable
private fun Named(name: String) {
    val brand = Brand.colors
    Box(Modifier.fillMaxSize().background(brand.surfaceMuted).padding(8.dp), contentAlignment = Alignment.Center) {
        Text(
            name,
            fontFamily = BrandFace,
            fontWeight = FontWeight.Bold,
            fontSize = 12.sp,
            color = brand.inkSoft,
            textAlign = TextAlign.Center,
            maxLines = 4,
            overflow = TextOverflow.Ellipsis,
        )
    }
}

/** wantGhost: one empty tile in the grid's shape, a wash of ink and a bookmark. */
@Composable
private fun WantGhost(modifier: Modifier = Modifier, mark: Boolean = true) {
    val brand = Brand.colors
    Box(modifier.fillMaxWidth().aspectRatio(3f / 4f).background(brand.ink.copy(alpha = 0.06f)), contentAlignment = Alignment.Center) {
        if (mark) Icon(Sym.Bookmark, null, tint = brand.inkSoft.copy(alpha = 0.6f), modifier = Modifier.size(26.dp))
    }
}

/** wantEmpty: Discover's own empty row, three ghosts 2 apart, then the way to the map. */
@Composable
private fun WantEmpty(showMap: () -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
        Row(horizontalArrangement = Arrangement.spacedBy(2.dp)) {
            for (i in 0 until 3) Box(Modifier.weight(1f)) { WantGhost(mark = i == 0) }
        }
        WantInvite(showMap)
    }
}

/** wantInvite: "Find trees near you", bordered, 50 high, to the map tab. */
@Composable
private fun WantInvite(showMap: () -> Unit) {
    val brand = Brand.colors
    Row(
        Modifier
            .fillMaxWidth()
            .height(50.dp)
            .clip(RoundedCornerShape(12.dp))
            .background(brand.surface)
            .border(1.dp, brand.ink.copy(alpha = 0.22f), RoundedCornerShape(12.dp))
            .clickable(role = Role.Button, onClick = showMap),
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Icon(Sym.Map, null, tint = brand.ink, modifier = Modifier.size(18.dp))
        Spacer(Modifier.width(8.dp))
        Text(stringResource(R.string.discover_find_near), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = brand.ink)
    }
}

/** signedOutLane: what the lane is FOR, and the one green control that opens it. */
@Composable
private fun SignedOutLane(lane: TreesLane, signIn: () -> Unit) {
    val brand = Brand.colors
    Column(Modifier.padding(top = 4.dp).padding(bottom = TabBar.floatDepth), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        Text(
            stringResource(if (lane == TreesLane.WANT) R.string.discover_want_signin else R.string.mt_signin_collect),
            fontSize = 15.sp,
            color = brand.inkSoft,
        )
        Box(
            Modifier
                .fillMaxWidth()
                .height(48.dp)
                .clip(CircleShape)
                .clickable(role = Role.Button, onClick = signIn)
                // The ripple stays inside the shape (Airbnb's line, 2026-11-10).
                .background(brand.moss, CircleShape),
            contentAlignment = Alignment.Center,
        ) {
            Text(stringResource(R.string.sign_in), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = brand.surface)
        }
    }
}

// MARK: - day zero: a mission, not a score

/** missionTitle: the distance only when we know where you are. */
@Composable
private fun Mission(catalogue: Catalogue, origin: Here, located: Boolean, wishlist: List<Tree>, saves: Saves, actions: MyTreesActions) {
    val brand = Brand.colors
    val t = remember(catalogue, origin, located, wishlist) {
        val heart = if (located) wishlist.minByOrNull { Geo.km(origin.lat, origin.lng, it.lat, it.lng) } else wishlist.firstOrNull()
        heart ?: catalogue.trees.asSequence()
            .filter { it.id !in saves.hearts && it.id !in saves.collected && it.photo != null }
            .minByOrNull { Geo.km(origin.lat, origin.lng, it.lat, it.lng) }
    }
    if (t != null) {
        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            val km = Geo.km(origin.lat, origin.lng, t.lat, t.lng)
            val far = if (km < 1) "${(km * 1000).toInt()} m" else String.format(java.util.Locale.ROOT, "%.1f km", km)
            Text(
                if (located) stringResource(R.string.mt_first_tree, far) else stringResource(R.string.mt_start_with),
                fontFamily = BrandFace,
                fontWeight = FontWeight.Bold,
                fontSize = 24.sp,
                lineHeight = 29.sp,
                color = brand.ink,
            )
            Text(stringResource(R.string.mt_mission_body), fontSize = 15.sp, color = brand.inkSoft)
            TreeCard(t, onOpen = { actions.openTree(t) })
            SheetButtonView(SheetButton(stringResource(R.string.mt_show_way), SheetKind.SECONDARY, Sym.TurnUpRight) { actions.openTree(t) })
        }
    } else {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text(stringResource(R.string.mt_no_trees), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 24.sp, color = brand.ink)
            Text(stringResource(R.string.mt_no_trees_body), fontSize = 15.sp, color = brand.inkSoft)
        }
    }
}

// MARK: - your own photographs (OwnThumb)

private val ownPhotos = object : LruCache<String, Bitmap>(24 * 1024 * 1024) {
    override fun sizeOf(key: String, value: Bitmap) = value.byteCount
}

/**
 * OwnThumb: one of your own photographs, fetched with your token and decoded off
 * the main thread; the tile is drawn at once on the muted ground and the picture
 * arrives a moment later. Memory only (hard rule 11).
 */
@Composable
fun OwnPhoto(s: OwnSighting, mine: MyTrees, modifier: Modifier = Modifier, maxSide: Int = 900, none: @Composable () -> Unit) {
    val brand = Brand.colors
    s.demo?.let {
        StandIn(it, modifier)
        return
    }
    val path = s.photo
    if (path == null) {
        Box(modifier) { none() }
        return
    }
    val key = "$path@$maxSide"
    val bitmap by produceState(ownPhotos.get(key), key) {
        if (value == null) {
            val bytes = mine.photoBytes(path)
            value = bytes?.let { b ->
                withContext(Dispatchers.Default) {
                    val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
                    BitmapFactory.decodeByteArray(b, 0, b.size, bounds)
                    var sample = 1
                    while (maxOf(bounds.outWidth, bounds.outHeight) / sample > maxSide * 2) sample *= 2
                    BitmapFactory.decodeByteArray(b, 0, b.size, BitmapFactory.Options().apply { inSampleSize = sample })
                }
            }?.also { ownPhotos.put(key, it) }
        }
    }
    val b = bitmap
    if (b != null) {
        Image(b.asImageBitmap(), null, contentScale = ContentScale.Crop, modifier = modifier)
    } else {
        Box(modifier.background(brand.surfaceMuted))
    }
}

/** Sightings.stand_in: the drawn photograph -mine-demo uses, sky, crown and trunk. */
@Composable
private fun StandIn(i: Int, modifier: Modifier) {
    Canvas(modifier) {
        // The 600 by 800 drawing, filled into the frame as a photograph would be.
        val scale = maxOf(size.width / 600f, size.height / 800f)
        val dx = (size.width - 600f * scale) / 2
        val dy = (size.height - 800f * scale) / 2
        fun x(v: Float) = dx + v * scale
        fun y(v: Float) = dy + v * scale
        drawRect(if (i == 0) Color(0.72f, 0.83f, 0.90f) else Color(0.86f, 0.87f, 0.80f))
        drawOval(Color(0.29f, 0.42f, 0.20f), Offset(x(-60f), y(60f)), Size(720f * scale, 520f * scale))
        drawRect(Color(0.36f, 0.27f, 0.19f), Offset(x(265f), y(460f)), Size(70f * scale, 340f * scale))
    }
}
