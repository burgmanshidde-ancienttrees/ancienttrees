// One tree, and the two actions that matter under it: ported from ios
// Screens/TreeDetail.swift, line by line, for the trees of ours. Every ruling
// behind a size, an order or a word is written beside it in the Swift; this file
// names the Swift piece each part copies so the two can be read side by side.
//
// Not here yet, because the screens they lead to are other sessions' (listed in
// data/android-parity.json): a tree of your own (`mine`, My trees), the place
// pin picker, the city, country and species pages, the library route of Collect.

package app.ancienttrees.ui

import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxHeight
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
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.DirectionsWalk
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.automirrored.outlined.HelpOutline
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.ConfirmationNumber
import androidx.compose.material.icons.filled.Eco
import androidx.compose.material.icons.filled.OpenInFull
import androidx.compose.material.icons.filled.PhotoCamera
import androidx.compose.material.icons.filled.ThumbUp
import androidx.compose.material.icons.filled.Tram
import androidx.compose.material.icons.filled.TurnRight
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material.icons.outlined.Cancel
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.EditNote
import androidx.compose.material.icons.outlined.Feedback
import androidx.compose.material.icons.outlined.IosShare
import androidx.compose.material.icons.outlined.LocationCity
import androidx.compose.material.icons.outlined.LocationOff
import androidx.compose.material.icons.outlined.PhotoCamera
import androidx.compose.material.icons.outlined.Public
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.layout
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.zIndex
import app.ancienttrees.R
import app.ancienttrees.account.Account
import app.ancienttrees.account.MyVotes
import app.ancienttrees.account.Submission
import app.ancienttrees.account.TreeNotes
import app.ancienttrees.account.VoteCounts
import app.ancienttrees.feed.Geo
import app.ancienttrees.feed.Here
import app.ancienttrees.feed.Precision
import app.ancienttrees.feed.Seasons
import app.ancienttrees.feed.Tree
import kotlinx.coroutines.launch
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import java.time.format.FormatStyle
import kotlin.math.roundToInt

/** What the page needs from the screen that owns the account and the map. */
class TreePageActions(
    val onBack: () -> Unit,
    val onHeart: () -> Unit,
    /** Collect: sign in first, then the camera (the app's one collect route on Android). */
    val onCollect: () -> Unit,
    val onShare: () -> Unit,
    /** A place, a species or the tree itself on the map (until those pages are ported). */
    val onGo: (SearchHit) -> Unit,
    /** Signed out: the sign-in sheet, then [then] once signed in. */
    val onNeedsSignIn: (then: () -> Unit) -> Unit,
)

/** The blue the pin's own ticket mark wears (TreeDetail.ticketBlue). */
private val TicketBlue = Color(0.18f, 0.42f, 0.66f)

/** Sightings.metres: 2.4, 3.15, 6. */
fun metres(cm: Int): String {
    var s = String.format(java.util.Locale.ROOT, "%.2f", cm / 100.0)
    while (s.endsWith("0")) s = s.dropLast(1)
    if (s.endsWith(".")) s = s.dropLast(1)
    return s
}

/** TreeDetail.placeDistrict: the district for the line under the name, or null. */
fun placeDistrict(neighbourhood: String, city: String): String? {
    var n = neighbourhood.trim()
    val bracket = n.indexOf('(')
    if (bracket >= 0) n = n.substring(0, bracket).trim()
    if (n.isEmpty() || n.length > 28) return null
    if (n.equals(city, ignoreCase = true)) return null
    return n
}

/** TreeDetail.staysNear: Collect within 200 m, and it gives way again only past 250 m. */
fun staysNear(was: Boolean, km: Double?): Boolean {
    val d = km ?: return false
    return d <= 0.2 || (was && d <= 0.25)
}

/** The distance in the big button: 50 m steps, then one decimal, then whole km. */
fun farLabel(km: Double): String = when {
    km < 1 -> "${((km * 1000 / 50).roundToInt() * 50)} m"
    km < 10 -> String.format(java.util.Locale.ROOT, "%.1f km", km)
    else -> "${km.roundToInt()} km"
}

/** Models.swift storyText: the scientific names in italics. */
fun storyText(tree: Tree): AnnotatedString = AnnotatedString.Builder(tree.story).apply {
    for (run in tree.storyLatin) {
        if (run.last < tree.story.length) addStyle(SpanStyle(fontStyle = FontStyle.Italic), run.first, run.last + 1)
    }
}.toAnnotatedString()

private fun openUrl(context: Context, url: String) {
    try {
        context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
    } catch (_: ActivityNotFoundException) {
        // Nothing on this phone opens a web address; the button then does nothing.
    }
}

/**
 * Directions.walk: walking directions to the tree. The iPhone asks once whether
 * Apple or Google Maps; Android has no Apple Maps and the system opens the maps
 * app the person chose as theirs (data/android-parity.json, forced).
 */
fun walkTo(context: Context, lat: Double, lng: Double) =
    openUrl(context, "https://www.google.com/maps/dir/?api=1&destination=$lat,$lng&travelmode=walking")

/** Pulls a view up by [top] and lets the next one in by [bottom], as SwiftUI's negative padding does. */
private fun Modifier.pull(top: Dp, bottom: Dp): Modifier = layout { m, c ->
    val p = m.measure(c)
    val t = top.roundToPx()
    val b = bottom.roundToPx()
    layout(p.width, (p.height - t - b).coerceAtLeast(0)) { p.place(0, -t) }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun TreeDetail(
    tree: Tree,
    account: Account,
    signedIn: Boolean,
    /** Where the phone is, only from a real fix (kmAway in the Swift). */
    fix: Here?,
    hearted: Boolean,
    collected: Boolean,
    votes: MyVotes,
    counts: VoteCounts,
    actions: TreePageActions,
    openPhotoAtStart: Boolean = false,
) {
    val brand = Brand.colors
    val context = LocalContext.current
    val scroll = rememberScrollState()
    var showingMap by remember(tree.id) { mutableStateOf(false) }
    var viewerAt by remember(tree.id) { mutableStateOf(if (openPhotoAtStart && tree.photo != null) 0 else -1) }
    var reportOpening by remember(tree.id) { mutableStateOf<String?>(null) }
    var choosingCollect by remember(tree.id) { mutableStateOf(false) }
    val pager = rememberPagerState { tree.shots.size + 1 }
    val shotAt = pager.currentPage
    val kmAway = fix?.let { Geo.km(it.lat, it.lng, tree.lat, tree.lng) }
    var nearTree by remember(tree.id) { mutableStateOf(false) }
    LaunchedEffect(kmAway) { nearTree = staysNear(nearTree, kmAway) }
    LaunchedEffect(Unit) { counts.loadOnce() }
    LaunchedEffect(signedIn) { votes.load(if (signedIn) account.fresh()?.accessToken else null) }

    fun startAddPhoto() = actions.onCollect()
    fun openCollectChoice() {
        if (!signedIn) actions.onNeedsSignIn { choosingCollect = true } else choosingCollect = true
    }

    BoxWithConstraints(Modifier.fillMaxSize().background(brand.ground)) {
        val pageW = maxWidth
        val pageH = maxHeight
        // heroHeight: the lead's shape across the page, stopped at 60 percent of the screen.
        val frame = tree.photo?.frame
        val heroHeight = if (frame != null && frame > 0) minOf(pageW / frame.toFloat(), pageH * 0.6f) else 300.dp

        Column(Modifier.fillMaxSize().verticalScroll(scroll)) {
            // THE PAGE SLIDES OVER THE PHOTOGRAPH: the hero keeps half the scroll.
            Box(Modifier.zIndex(0f).graphicsLayer { translationY = scroll.value * 0.5f }) {
                Hero(
                    tree = tree,
                    heroHeight = heroHeight,
                    showingMap = showingMap,
                    pager = pager,
                    onToggleMap = { showingMap = !showingMap },
                    onOpenPhoto = { viewerAt = it },
                    onFullMap = { actions.onGo(SearchHit.OneTree(tree)) },
                    onAddPhoto = { startAddPhoto() },
                )
            }
            Column(
                verticalArrangement = Arrangement.spacedBy(28.dp),
                modifier = Modifier
                    .zIndex(1f)
                    .fillMaxWidth()
                    .background(brand.ground, RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp))
                    .padding(horizontal = 20.dp)
                    .padding(top = 20.dp),
            ) {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    // THE PHOTOGRAPH'S FOOTER LINE CARRIES THE ADD.
                    if (!showingMap && tree.photo != null) {
                        Row(Modifier.fillMaxWidth().pull(12.dp, 4.dp), horizontalArrangement = Arrangement.End) {
                            val onAdd = shotAt >= tree.shots.count()
                            Box(Modifier.graphicsLayer { alpha = if (onAdd) 0f else 1f }) {
                                AddPhotoPill(enabled = !onAdd) { startAddPhoto() }
                            }
                        }
                    }
                    Header(tree, votes, counts, signedIn, account, actions)
                    FactsBlock(tree, actions, onPlace = { reportOpening = context.getString(R.string.opening_pin) })
                }
                SeasonsRow(tree, onOpen = { viewerAt = it }, onAdd = { startAddPhoto() })
                ExpandableText(
                    storyText(tree),
                    lines = 6,
                    style = TextStyle(fontSize = 17.sp, lineHeight = 22.sp, color = brand.ink),
                )
                NotesSection(tree, account, signedIn, actions)
                GettingThere(tree)
                WorthItView(tree, account, signedIn, votes, actions)
                DiscoverMore(tree, actions)
                CreditLine(tree, shotAt)
                Spacer(Modifier.height(90.dp).navigationBarsPadding())
            }
        }

        TopButtons(
            tree = tree,
            onBack = actions.onBack,
            onShare = actions.onShare,
            onReport = { reportOpening = it },
        )

        ActionBar(
            tree = tree,
            standingHere = nearTree,
            kmAway = kmAway,
            collected = collected,
            hearted = hearted,
            onDirections = { walkTo(context, tree.lat, tree.lng) },
            onCollect = { openCollectChoice() },
            onHeart = actions.onHeart,
            modifier = Modifier.align(Alignment.BottomCenter),
        )
    }

    if (viewerAt >= 0) PhotoViewer(tree.shots, viewerAt) { viewerAt = -1 }
    reportOpening?.let { opening ->
        ReportSheet(tree, opening, account, signedIn, actions) { reportOpening = null }
    }
    if (choosingCollect) {
        BrandSheet(
            icon = if (collected) Icons.Filled.Verified else Icons.Outlined.PhotoCamera,
            title = if (collected) stringResource(R.string.collected_title, tree.name) else stringResource(R.string.collect_title, tree.name),
            message = if (collected) null else stringResource(R.string.collect_lead),
            onDismiss = { choosingCollect = false },
            buttons = listOf(
                SheetButton(stringResource(R.string.collect_camera), SheetKind.PRIMARY, Icons.Outlined.PhotoCamera) {
                    choosingCollect = false
                    actions.onCollect()
                },
            ),
        )
    }
}

// MARK: - The hero

@Composable
private fun Hero(
    tree: Tree,
    heroHeight: Dp,
    showingMap: Boolean,
    pager: androidx.compose.foundation.pager.PagerState,
    onToggleMap: () -> Unit,
    onOpenPhoto: (Int) -> Unit,
    onFullMap: () -> Unit,
    onAddPhoto: () -> Unit,
) {
    val brand = Brand.colors
    val photo = tree.photo
    val noTap = remember { MutableInteractionSource() }
    when {
        showingMap -> Box(
            Modifier
                .fillMaxWidth()
                .height(heroHeight)
                .clickable(interactionSource = noTap, indication = null, onClick = onFullMap),
        ) {
            MapInset(tree.lat, tree.lng, side = null, height = heroHeight, modifier = Modifier.fillMaxSize())
            // THE SAME CONTROL, POINTING THE OTHER WAY: the photograph's thumbnail.
            val back = stringResource(R.string.show_photo_again)
            Box(
                Modifier
                    .align(Alignment.BottomEnd)
                    .padding(10.dp)
                    .size(72.dp)
                    .shadow(4.dp, RoundedCornerShape(10.dp))
                    .clip(RoundedCornerShape(10.dp))
                    .background(brand.surfaceMuted)
                    .border(2.dp, Color.White.copy(alpha = 0.9f), RoundedCornerShape(10.dp))
                    .clickable(role = Role.Button, onClick = onToggleMap)
                    .semantics { contentDescription = back },
                contentAlignment = Alignment.Center,
            ) {
                if (photo != null) {
                    RemoteImage(photo.card, null, Modifier.fillMaxSize(), fallback = { Box(Modifier.fillMaxSize().background(brand.surfaceMuted)) })
                } else {
                    SpeciesMark(tree.species, brand.inkSoft.copy(alpha = 0.5f), Modifier.size(30.dp))
                }
            }
            val full = stringResource(R.string.open_full_map)
            Box(
                Modifier
                    .align(Alignment.BottomStart)
                    .padding(10.dp)
                    .size(44.dp)
                    .background(brand.ground.copy(alpha = 0.92f), CircleShape)
                    .clickable(role = Role.Button, onClick = onFullMap)
                    .semantics { contentDescription = full },
                contentAlignment = Alignment.Center,
            ) {
                Icon(Icons.Filled.OpenInFull, null, tint = brand.ink, modifier = Modifier.size(16.dp))
            }
        }
        photo != null -> Box(Modifier.fillMaxWidth().height(heroHeight)) {
            HorizontalPager(pager, Modifier.fillMaxSize()) { i ->
                if (i < tree.shots.size) {
                    val shot = tree.shots[i]
                    // THE CARD'S PICTURE FIRST, the sharp one when it lands.
                    RemoteImage(
                        shot.full,
                        null,
                        Modifier
                            .fillMaxSize()
                            .clickable(interactionSource = noTap, indication = null) { onOpenPhoto(i) },
                        fallback = {
                            val have = cachedImage(shot.card)
                            if (have != null) {
                                androidx.compose.foundation.Image(
                                    have.asImageBitmap(),
                                    null,
                                    contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                                    modifier = Modifier.fillMaxSize(),
                                )
                            } else if (i == 0) {
                                HeroFallback(tree)
                            } else {
                                Box(Modifier.fillMaxSize().background(brand.surfaceMuted))
                            }
                        },
                    )
                } else {
                    AddPhotoPage(onAddPhoto)
                }
            }
            PageDots(count = tree.shots.size, at = pager.currentPage, modifier = Modifier.align(Alignment.BottomCenter).padding(bottom = 12.dp))
            val label = stringResource(R.string.show_on_map)
            Box(
                Modifier
                    .align(Alignment.BottomEnd)
                    .padding(10.dp)
                    .clickable(role = Role.Button, onClick = onToggleMap)
                    .semantics { contentDescription = label },
            ) {
                MapInset(tree.lat, tree.lng, side = 56.dp)
            }
        }
        else -> Box(
            // NO PHOTOGRAPH: THE MAP IS THE PICTURE.
            Modifier
                .fillMaxWidth()
                .height(300.dp)
                .clickable(interactionSource = noTap, indication = null, onClick = onFullMap),
        ) {
            MapInset(tree.lat, tree.lng, side = null, height = 300.dp, modifier = Modifier.fillMaxSize())
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .padding(horizontal = 20.dp)
                    .padding(bottom = 14.dp)
                    .shadow(8.dp, RoundedCornerShape(14.dp), ambientColor = Color.Black.copy(alpha = 0.12f), spotColor = Color.Black.copy(alpha = 0.12f))
                    .background(brand.surface.copy(alpha = 0.94f), RoundedCornerShape(14.dp))
                    .padding(horizontal = 14.dp, vertical = 12.dp),
            ) {
                Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
                    Text(stringResource(R.string.no_photo_yet), fontSize = 14.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
                    Text(stringResource(R.string.no_photo_first), fontSize = 13.sp, color = brand.inkSoft)
                }
                AddPhotoButton(onAddPhoto)
            }
        }
    }
}

@Composable
private fun HeroFallback(tree: Tree) {
    val brand = Brand.colors
    Column(
        Modifier.fillMaxSize().background(brand.surfaceMuted),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(10.dp, Alignment.CenterVertically),
    ) {
        SpeciesMark(tree.species, brand.inkSoft.copy(alpha = 0.35f), Modifier.size(64.dp))
        Text(stringResource(R.string.no_photo_yet), fontSize = 12.sp, color = brand.inkSoft)
    }
}

/** pageDots: one per page, the add page included; white on a photograph, ink on the grey add page. */
@Composable
private fun PageDots(count: Int, at: Int, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    val onAdd = at >= count
    Row(modifier, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
        for (i in 0..count) {
            val c = if (onAdd) (if (i == at) brand.inkSoft else brand.ink.copy(alpha = 0.25f)) else Color.White.copy(alpha = if (i == at) 1f else 0.55f)
            Box(
                Modifier
                    .size(7.dp)
                    .then(if (onAdd) Modifier else Modifier.shadow(1.dp, CircleShape, ambientColor = Color.Black.copy(alpha = 0.35f), spotColor = Color.Black.copy(alpha = 0.35f)))
                    .background(c, CircleShape),
            )
        }
    }
}

/** addPhotoPage: the hero's last page, the ask where the photographs are. */
@Composable
private fun AddPhotoPage(onAdd: () -> Unit) {
    val brand = Brand.colors
    Column(
        Modifier.fillMaxSize().background(brand.surfaceMuted).padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Icon(Icons.Outlined.PhotoCamera, null, tint = brand.inkSoft.copy(alpha = 0.45f), modifier = Modifier.padding(bottom = 4.dp).size(32.dp))
        Spacer(Modifier.height(6.dp))
        Text(stringResource(R.string.your_photo_here), fontSize = 17.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
        Spacer(Modifier.height(6.dp))
        Text(
            stringResource(R.string.your_photo_here_sub),
            fontSize = 14.sp,
            color = brand.inkSoft,
            textAlign = TextAlign.Center,
            modifier = Modifier.widthIn(max = 250.dp),
        )
        Spacer(Modifier.height(16.dp))
        Box(
            Modifier
                .heightIn(min = 44.dp)
                .background(brand.surface, CircleShape)
                .border(1.dp, brand.hairline, CircleShape)
                .clickable(role = Role.Button, onClick = onAdd)
                .padding(horizontal = 18.dp),
            contentAlignment = Alignment.Center,
        ) {
            Text(stringResource(R.string.add_a_photo), fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = brand.moss)
        }
    }
}

/** addPhotoButton: on a tree with no photograph, the moss capsule in the map's card. */
@Composable
private fun AddPhotoButton(onClick: () -> Unit) {
    val brand = Brand.colors
    val label = stringResource(R.string.add_photo_label)
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp),
        modifier = Modifier
            .heightIn(min = 44.dp)
            .background(brand.moss, CircleShape)
            .clickable(role = Role.Button, onClick = onClick)
            .semantics { contentDescription = label }
            .padding(horizontal = 14.dp),
    ) {
        Icon(Icons.Filled.PhotoCamera, null, tint = brand.onMoss, modifier = Modifier.size(16.dp))
        Text(stringResource(R.string.add_a_photo), fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = brand.onMoss)
    }
}

/** addPhotoRow: Google Maps' tonal pill, 36 high, with a 44 point touch target. */
@Composable
private fun AddPhotoPill(enabled: Boolean, onClick: () -> Unit) {
    val brand = Brand.colors
    val label = stringResource(R.string.add_photo_label)
    Box(
        Modifier
            .heightIn(min = 44.dp)
            .clickable(enabled = enabled, role = Role.Button, interactionSource = remember { MutableInteractionSource() }, indication = null, onClick = onClick)
            .semantics { contentDescription = label },
        contentAlignment = Alignment.Center,
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(6.dp),
            modifier = Modifier.height(36.dp).background(brand.mossTint, CircleShape).padding(horizontal = 14.dp),
        ) {
            Icon(Icons.Outlined.PhotoCamera, null, tint = brand.moss, modifier = Modifier.size(16.dp))
            Text(stringResource(R.string.add_a_photo), fontSize = 14.sp, fontWeight = FontWeight.SemiBold, color = brand.moss)
        }
    }
}

// MARK: - The bar over the photograph

/**
 * Back on the left; share and report together on the right, one capsule, as
 * iOS 26 groups a trailing pair. The glass is the ground at 92 percent
 * (data/android-parity.json, forced).
 */
@Composable
private fun TopButtons(tree: Tree, onBack: () -> Unit, onShare: () -> Unit, onReport: (String) -> Unit) {
    val brand = Brand.colors
    val glass = brand.ground.copy(alpha = 0.92f)
    var menu by remember { mutableStateOf(false) }
    Row(
        Modifier.fillMaxWidth().statusBarsPadding().padding(horizontal = 16.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        val back = stringResource(R.string.back)
        Box(
            Modifier
                .size(44.dp)
                .shadow(2.dp, CircleShape)
                .background(glass, CircleShape)
                .clickable(role = Role.Button, onClick = onBack)
                .semantics { contentDescription = back },
            contentAlignment = Alignment.Center,
        ) {
            Icon(Icons.AutoMirrored.Filled.ArrowBack, null, tint = brand.ink, modifier = Modifier.size(20.dp))
        }
        Spacer(Modifier.weight(1f))
        Row(
            Modifier.height(44.dp).shadow(2.dp, CircleShape).background(glass, CircleShape),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            val share = stringResource(R.string.share_tree)
            Box(
                Modifier.size(48.dp, 44.dp).clickable(role = Role.Button, onClick = onShare).semantics { contentDescription = share },
                contentAlignment = Alignment.Center,
            ) {
                Icon(Icons.Outlined.IosShare, null, tint = brand.ink, modifier = Modifier.size(20.dp))
            }
            val report = stringResource(R.string.report_problem)
            Box {
                Box(
                    Modifier.size(48.dp, 44.dp).clickable(role = Role.Button) { menu = true }.semantics { contentDescription = report },
                    contentAlignment = Alignment.Center,
                ) {
                    Icon(Icons.Outlined.Feedback, null, tint = brand.ink, modifier = Modifier.size(20.dp))
                }
                DropdownMenu(expanded = menu, onDismissRequest = { menu = false }, containerColor = brand.surface) {
                    val items = listOf(
                        Triple(R.string.menu_wrong, R.string.opening_wrong, Icons.Outlined.Feedback),
                        Triple(R.string.menu_pin, R.string.opening_pin, Icons.Outlined.LocationOff),
                        Triple(R.string.menu_which, R.string.opening_which, Icons.AutoMirrored.Outlined.HelpOutline),
                        Triple(R.string.menu_gone, R.string.opening_gone, Icons.Outlined.Cancel),
                    )
                    for ((label, opening, icon) in items) {
                        val opens = stringResource(opening)
                        DropdownMenuItem(
                            text = { Text(stringResource(label), color = brand.ink, fontSize = 16.sp) },
                            trailingIcon = { Icon(icon, null, tint = brand.ink, modifier = Modifier.size(20.dp)) },
                            onClick = {
                                menu = false
                                onReport(opens)
                            },
                        )
                    }
                }
            }
        }
    }
}

// MARK: - Name, place, facts

@Composable
private fun Header(tree: Tree, votes: MyVotes, counts: VoteCounts, signedIn: Boolean, account: Account, actions: TreePageActions) {
    val brand = Brand.colors
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text(
            tree.name,
            fontFamily = BrandFace,
            fontWeight = FontWeight.Bold,
            fontSize = 30.sp,
            lineHeight = 35.sp,
            color = brand.ink,
            modifier = Modifier.semantics { heading() },
        )
        // summaryLine: "District, City" (the city the link) · the thumb.
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            val district = placeDistrict(tree.neighbourhood, tree.city)
            val see = stringResource(R.string.see_every_tree_in, tree.city)
            Row(Modifier.heightIn(min = 44.dp).weight(1f, fill = false), verticalAlignment = Alignment.CenterVertically) {
                if (district != null) {
                    Text(
                        "$district, ",
                        fontSize = 15.sp,
                        color = brand.inkSoft,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.weight(1f, fill = false),
                    )
                }
                Text(
                    tree.city,
                    fontSize = 15.sp,
                    color = brand.ink,
                    textDecoration = TextDecoration.Underline,
                    maxLines = 1,
                    modifier = Modifier
                        .heightIn(min = 44.dp)
                        .clickable(role = Role.Button, interactionSource = remember { MutableInteractionSource() }, indication = null) {
                            actions.onGo(SearchHit.City(tree.citySlug, tree.city, tree.lat, tree.lng))
                        }
                        .semantics { contentDescription = see }
                        .wrapCentreVertically(),
                )
            }
            Text("·", fontSize = 15.sp, color = brand.inkSoft)
            WorthItButton(tree, votes, counts, signedIn, account, actions)
        }
    }
}

/** A text in a 44 point tall box, its line centred. */
private fun Modifier.wrapCentreVertically(): Modifier = layout { m, c ->
    val p = m.measure(c.copy(minHeight = 0))
    val h = maxOf(p.height, c.minHeight)
    layout(p.width, h) { p.place(0, (h - p.height) / 2) }
}

/** WorthItButton, compact: the thumb beside the place, and the count once there is one. */
@Composable
private fun WorthItButton(tree: Tree, votes: MyVotes, counts: VoteCounts, signedIn: Boolean, account: Account, actions: TreePageActions) {
    val brand = Brand.colors
    val scope = rememberCoroutineScope()
    val cast = votes.vote(tree.id) == "up"
    val label = if (cast) stringResource(R.string.worth_cast, tree.name) else stringResource(R.string.worth_ask, tree.name)
    fun send(why: String) = scope.launch {
        Submission.feedback(tree.city, Submission.treeField(tree.id, tree.name), why, account.fresh()?.accessToken)
    }
    fun tap() {
        if (cast) {
            send("vote undone: worth it")
            counts.record(tree.id, "up", "")
            votes.setVote(tree.id, "")
        } else {
            counts.record(tree.id, votes.vote(tree.id), "up")
            votes.setVote(tree.id, "up")
            send("worth it")
        }
    }
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(4.dp),
        modifier = Modifier
            .heightIn(min = 44.dp)
            .widthIn(min = 44.dp)
            .clickable(role = Role.Button, interactionSource = remember { MutableInteractionSource() }, indication = null) {
                if (!signedIn) actions.onNeedsSignIn { } else tap()
            }
            .semantics { contentDescription = label },
    ) {
        val tint = if (cast) brand.moss else brand.ink
        Icon(if (cast) Icons.Filled.ThumbUp else Icons.Outlined.ThumbUp, null, tint = tint, modifier = Modifier.size(15.dp))
        counts.up(tree.id)?.let { n ->
            Text("$n", fontSize = 15.sp, color = tint, textDecoration = TextDecoration.Underline)
        }
    }
}

/** factsBlock: the two columns, the location line, the ticket band, in one bordered card. */
@Composable
private fun FactsBlock(tree: Tree, actions: TreePageActions, onPlace: () -> Unit) {
    val brand = Brand.colors
    val shape = RoundedCornerShape(14.dp)
    Column(
        Modifier
            .fillMaxWidth()
            .clip(shape)
            .background(brand.surface, shape)
            .border(1.dp, brand.hairline, shape),
    ) {
        Columns(tree, actions)
        if (tree.precision == Precision.APPROXIMATE) LocationLine(onPlace)
        if (tree.paidEntry) TicketBand(tree)
    }
}

@Composable
private fun Hairline() = Box(Modifier.fillMaxWidth().height(1.dp).background(Brand.colors.hairline))

@Composable
private fun FactColumn(label: String, modifier: Modifier = Modifier, value: @Composable () -> Unit) {
    Column(modifier, verticalArrangement = Arrangement.spacedBy(2.dp)) {
        Text(label, fontSize = 13.sp, color = Brand.colors.inkSoft)
        value()
    }
}

@Composable
private fun FactValue(text: String, color: Color = Brand.colors.ink) {
    Text(
        text,
        fontFamily = BrandFace,
        fontWeight = FontWeight.Bold,
        fontSize = 19.sp,
        lineHeight = 23.sp,
        color = color,
        maxLines = 1,
        overflow = TextOverflow.Ellipsis,
    )
}

@Composable
private fun Columns(tree: Tree, actions: TreePageActions) {
    val brand = Brand.colors
    val showsGirth = tree.girthCm != null
    Column(Modifier.padding(top = 12.dp, bottom = 4.dp).padding(horizontal = 16.dp)) {
        Row(Modifier.height(IntrinsicSize.Min)) {
            // ageColumn: the bare number under "Years old", else the first clause under "Age".
            val lo = tree.ageMin
            val ageNumber = if (lo != null && lo > 0) {
                val hi = tree.ageMax
                if (hi != null && hi > lo) "$lo-$hi" else "$lo"
            } else {
                null
            }
            val shortAge = tree.age?.let { raw ->
                val first = raw.split(',', ';', '(').first().trim()
                if (first.length > 24) stringResource(R.string.age_see_story) else first
            } ?: stringResource(R.string.age_not_recorded)
            FactColumn(
                stringResource(if (ageNumber != null) R.string.years_old else R.string.age),
                Modifier.weight(1f).padding(end = 16.dp),
            ) { FactValue(ageNumber ?: shortAge) }
            Box(Modifier.width(1.dp).height(44.dp).background(brand.hairline))
            Box(Modifier.weight(1f).padding(start = 16.dp)) {
                if (showsGirth) {
                    FactColumn(stringResource(R.string.girth)) { FactValue(stringResource(R.string.girth_value, metres(tree.girthCm!!))) }
                } else {
                    SpeciesColumn(tree, actions)
                }
            }
        }
        if (showsGirth) {
            Column(Modifier.fillMaxWidth().padding(top = 0.dp)) {
                Hairline()
                Box(Modifier.padding(top = 10.dp)) { SpeciesColumn(tree, actions) }
            }
        }
    }
}

@Composable
private fun SpeciesColumn(tree: Tree, actions: TreePageActions) {
    val brand = Brand.colors
    val label = stringResource(R.string.species_see_all, tree.commonName)
    Box(
        Modifier
            .fillMaxWidth()
            .heightIn(min = 44.dp)
            .clickable(role = Role.Button, interactionSource = remember { MutableInteractionSource() }, indication = null) {
                actions.onGo(SearchHit.Species(tree.commonName))
            }
            .semantics { contentDescription = label },
    ) {
        FactColumn(stringResource(R.string.species)) {
            // Common name only, and the chevron that says the species page is one tap away.
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(
                    tree.commonName,
                    fontFamily = BrandFace,
                    fontWeight = FontWeight.Bold,
                    fontSize = 19.sp,
                    lineHeight = 23.sp,
                    color = brand.moss,
                    maxLines = 2,
                    modifier = Modifier.weight(1f, fill = false),
                )
                Icon(Icons.AutoMirrored.Filled.KeyboardArrowRight, null, tint = brand.moss, modifier = Modifier.size(16.dp))
            }
        }
    }
}

/** locationLine: only when the pin is approximate, and the ask is in it. */
@Composable
private fun LocationLine(onPlace: () -> Unit) {
    val brand = Brand.colors
    val label = stringResource(R.string.location_approx_label)
    val lead = stringResource(R.string.location_approx_short)
    val ask = stringResource(R.string.show_us_where)
    Column(Modifier.padding(bottom = 4.dp)) {
        Hairline()
        Box(
            Modifier
                .fillMaxWidth()
                .heightIn(min = 44.dp)
                .clickable(role = Role.Button, onClick = onPlace)
                .semantics { contentDescription = label }
                .padding(horizontal = 16.dp),
            contentAlignment = Alignment.CenterStart,
        ) {
            Text(
                buildAnnotatedString {
                    withStyle(SpanStyle(fontWeight = FontWeight.SemiBold)) { append("$lead ") }
                    withStyle(SpanStyle(color = brand.moss, textDecoration = TextDecoration.Underline)) { append(ask) }
                },
                fontSize = 13.sp,
                lineHeight = 18.sp,
                color = brand.ink,
            )
        }
    }
}

/** ticketBand: the blue kept, standing on its own inside the block. */
@Composable
private fun TicketBand(tree: Tree) {
    val brand = Brand.colors
    Column {
        Hairline()
        Row(
            Modifier.fillMaxWidth().background(TicketBlue.copy(alpha = 0.10f)).padding(horizontal = 16.dp, vertical = 12.dp),
            horizontalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Icon(Icons.Filled.ConfirmationNumber, null, tint = TicketBlue, modifier = Modifier.padding(top = 1.dp).size(16.dp))
            Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
                Text(stringResource(R.string.ticket_needed), fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
                if (tree.access.isNotEmpty()) Text(tree.access, fontSize = 13.sp, color = brand.ink)
            }
        }
    }
}

// MARK: - Seasons

@Composable
private fun seasonName(key: String): String = stringResource(
    when (key) {
        "spring" -> R.string.season_spring
        "summer" -> R.string.season_summer
        "autumn" -> R.string.season_autumn
        else -> R.string.season_winter
    },
)

/** seasonsRow: four tiles, each season's first photograph, the empty one of now asking. */
@Composable
private fun SeasonsRow(tree: Tree, onOpen: (Int) -> Unit, onAdd: () -> Unit) {
    val brand = Brand.colors
    val tiles = Seasons.tiles(tree)
    if (tiles.isEmpty()) return
    val month = remember { java.util.Calendar.getInstance().get(java.util.Calendar.MONTH) + 1 }
    val now = Seasons.now(month, tree.lat)
    val filled = tiles.count { it.first != null }
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Row(verticalAlignment = Alignment.Bottom) {
            Text(stringResource(R.string.seasons_heading), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 18.sp, color = brand.ink, modifier = Modifier.weight(1f))
            Text(stringResource(R.string.seasons_tally, filled), fontSize = 14.sp, fontWeight = FontWeight.Medium, color = brand.inkSoft)
        }
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            for (tile in tiles) {
                val name = seasonName(tile.key)
                val at = tile.first
                val shape = RoundedCornerShape(12.dp)
                if (at != null) {
                    val label = stringResource(R.string.season_photo, name, at + 1, tree.shots.size)
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(6.dp),
                        modifier = Modifier.weight(1f).clickable(role = Role.Button) { onOpen(at) }.semantics { contentDescription = label },
                    ) {
                        Box(
                            Modifier
                                .fillMaxWidth()
                                .aspectRatio(1f)
                                .then(
                                    if (tile.lead) {
                                        Modifier.drawBehind {
                                            val inset = -3.dp.toPx()
                                            drawRoundRect(
                                                brand.moss,
                                                topLeft = Offset(inset, inset),
                                                size = androidx.compose.ui.geometry.Size(size.width - 2 * inset, size.height - 2 * inset),
                                                cornerRadius = androidx.compose.ui.geometry.CornerRadius(15.dp.toPx()),
                                                style = androidx.compose.ui.graphics.drawscope.Stroke(2.dp.toPx()),
                                            )
                                        }
                                    } else {
                                        Modifier
                                    },
                                ),
                        ) {
                            RemoteImage(tree.shots[at].card, null, Modifier.fillMaxSize().clip(shape))
                            if (tile.count > 1) {
                                Box(
                                    Modifier
                                        .align(Alignment.TopEnd)
                                        .padding(6.dp)
                                        .heightIn(min = 22.dp)
                                        .widthIn(min = 22.dp)
                                        .background(Color.Black.copy(alpha = 0.55f), CircleShape)
                                        .padding(horizontal = 6.dp),
                                    contentAlignment = Alignment.Center,
                                ) {
                                    Text("${tile.count}", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = Color.White)
                                }
                            }
                        }
                        Text(name, fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
                    }
                } else {
                    val isNow = tile.key == now
                    val label = stringResource(R.string.season_add, name)
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(6.dp),
                        modifier = Modifier.weight(1f).clickable(role = Role.Button, onClick = onAdd).semantics { contentDescription = label },
                    ) {
                        Box(
                            Modifier.fillMaxWidth().aspectRatio(1f).background(if (isNow) brand.mossTint else brand.surfaceMuted, shape),
                            contentAlignment = Alignment.Center,
                        ) {
                            if (isNow) {
                                Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(3.dp)) {
                                    Icon(Icons.Outlined.PhotoCamera, null, tint = brand.moss, modifier = Modifier.size(22.dp))
                                    Text(stringResource(R.string.season_now), fontSize = 12.sp, fontWeight = FontWeight.Bold, color = brand.moss)
                                }
                            } else {
                                Icon(Icons.Filled.Add, null, tint = brand.inkSoft.copy(alpha = 0.7f), modifier = Modifier.size(22.dp))
                            }
                        }
                        Text(
                            name,
                            fontSize = 13.sp,
                            fontWeight = if (isNow) FontWeight.Bold else FontWeight.Medium,
                            color = if (isNow) brand.moss else brand.inkSoft,
                        )
                    }
                }
            }
        }
        if (filled == 4) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.padding(top = 2.dp)) {
                Icon(Icons.Filled.Check, null, tint = brand.moss, modifier = Modifier.size(16.dp))
                Text(stringResource(R.string.seasons_all), fontSize = 14.sp, fontWeight = FontWeight.SemiBold, color = brand.moss)
            }
        }
    }
}

// MARK: - From people who stood here

@Composable
private fun NotesSection(tree: Tree, account: Account, signedIn: Boolean, actions: TreePageActions) {
    val brand = Brand.colors
    val notes = remember(tree.id) { TreeNotes() }
    val scope = rememberCoroutineScope()
    var writing by remember { mutableStateOf(false) }
    var text by remember { mutableStateOf("") }
    var saving by remember { mutableStateOf(false) }
    var failed by remember { mutableStateOf(false) }
    var me by remember { mutableStateOf<Pair<String?, Boolean>?>(null) }
    LaunchedEffect(tree.id, signedIn) {
        val s = if (signedIn) account.fresh() else null
        notes.load(tree.id, s?.accessToken)
        me = s?.let { session ->
            app.ancienttrees.account.Supa.rows("/rest/v1/profiles?select=display_name,public&user_id=eq.${session.userId}", session.accessToken)
                .firstOrNull()?.let { (it.optString("display_name").ifEmpty { null }) to it.optBoolean("public", false) }
        }
    }
    if (notes.gone) return
    fun open() {
        text = notes.mine?.body.orEmpty()
        failed = false
        writing = true
    }
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text(
            stringResource(R.string.notes_title),
            fontFamily = BrandFace,
            fontWeight = FontWeight.Bold,
            fontSize = 18.sp,
            color = brand.ink,
            modifier = Modifier.semantics { heading() },
        )
        val here = notes.here(tree.id)
        notes.mine?.let { m ->
            NoteCard(m.body, m.date, stringResource(R.string.notes_your), initial = me?.first?.firstOrNull(), mine = true)
        }
        for (n in here) {
            NoteCard(n.body, n.date, n.authorName ?: stringResource(R.string.notes_visitor), initial = n.authorName?.firstOrNull(), mine = false, avatar = n.authorAvatar)
        }
        if (here.isEmpty() && notes.mine == null) {
            Column(
                Modifier
                    .fillMaxWidth()
                    .background(brand.surfaceMuted, RoundedCornerShape(14.dp))
                    .padding(horizontal = 16.dp)
                    .padding(top = 20.dp, bottom = 16.dp),
                verticalArrangement = Arrangement.spacedBy(4.dp),
            ) {
                Icon(Icons.Outlined.ChatBubbleOutline, null, tint = brand.inkSoft.copy(alpha = 0.45f), modifier = Modifier.padding(bottom = 6.dp).size(24.dp))
                Text(stringResource(R.string.notes_none), fontSize = 16.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
                Text(stringResource(R.string.notes_none_sub), fontSize = 14.sp, color = brand.inkSoft)
                Box(Modifier.padding(top = 10.dp)) {
                    NoteButton(onGrey = true, edit = false) { if (!signedIn) actions.onNeedsSignIn { open() } else open() }
                }
            }
        } else {
            Box(Modifier.padding(top = 2.dp)) {
                NoteButton(onGrey = false, edit = notes.mine != null) { if (!signedIn) actions.onNeedsSignIn { open() } else open() }
            }
        }
    }
    if (writing) {
        val named = me?.takeIf { it.second }?.first
        BrandSheet(
            title = stringResource(R.string.note_sheet_title),
            message = tree.name,
            onDismiss = { writing = false },
            footnote = if (failed) stringResource(R.string.note_failed) else null,
            buttons = buildList {
                add(
                    SheetButton(stringResource(if (notes.mine == null) R.string.note_add else R.string.note_save), SheetKind.PRIMARY) {
                        val body = text.trim()
                        if (body.isEmpty() || saving) return@SheetButton
                        saving = true
                        scope.launch {
                            val token = account.fresh()?.accessToken
                            val ok = token != null && notes.save(tree.id, body, token)
                            saving = false
                            if (ok) writing = false else failed = true
                        }
                    },
                )
                if (notes.mine != null) {
                    add(
                        SheetButton(stringResource(R.string.note_delete), SheetKind.DESTRUCTIVE_QUIET) {
                            if (saving) return@SheetButton
                            saving = true
                            scope.launch {
                                val token = account.fresh()?.accessToken
                                val ok = token != null && notes.delete(tree.id, token)
                                saving = false
                                if (ok) writing = false else failed = true
                            }
                        },
                    )
                }
                add(SheetButton(stringResource(R.string.cancel), SheetKind.QUIET) { writing = false })
            },
        ) {
            Column(Modifier.fillMaxWidth().padding(top = 16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Box(
                    Modifier
                        .fillMaxWidth()
                        .heightIn(min = 120.dp)
                        .background(brand.surfaceMuted, RoundedCornerShape(14.dp))
                        .padding(horizontal = 15.dp, vertical = 16.dp),
                ) {
                    BasicTextField(
                        value = text,
                        onValueChange = { text = it },
                        enabled = !saving,
                        textStyle = TextStyle(fontSize = 16.sp, color = brand.ink),
                        cursorBrush = SolidColor(brand.moss),
                        modifier = Modifier.fillMaxWidth(),
                    )
                    if (text.isEmpty()) {
                        Text(stringResource(R.string.note_placeholder), fontSize = 16.sp, color = brand.inkSoft.copy(alpha = 0.7f))
                    }
                }
                Text(stringResource(R.string.note_examples), fontSize = 13.sp, color = brand.inkSoft)
                Text(
                    if (named != null) stringResource(R.string.note_shown_as, named) else stringResource(R.string.note_shown_visitor),
                    fontSize = 13.sp,
                    color = brand.inkSoft,
                )
            }
        }
    }
}

@Composable
private fun NoteCard(body: String, date: java.time.Instant, name: String, initial: Char?, mine: Boolean, avatar: String? = null) {
    val brand = Brand.colors
    val day = remember(date) {
        DateTimeFormatter.ofLocalizedDate(FormatStyle.MEDIUM).withZone(ZoneId.systemDefault()).format(date)
    }
    Column(
        Modifier
            .fillMaxWidth()
            .background(if (mine) brand.mossTint else brand.surfaceMuted, RoundedCornerShape(14.dp))
            .padding(horizontal = 14.dp, vertical = 12.dp),
        verticalArrangement = Arrangement.spacedBy(6.dp),
    ) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Box(
                Modifier.size(28.dp).clip(CircleShape).background(if (mine || initial != null) brand.moss else brand.creamDark),
                contentAlignment = Alignment.Center,
            ) {
                when {
                    avatar != null -> RemoteImage(avatar, null, Modifier.fillMaxSize(), placeholder = false)
                    initial != null -> Text(initial.uppercase(), fontFamily = BrandFace, fontWeight = FontWeight.Black, fontSize = 12.sp, color = brand.onMoss)
                    else -> Icon(Icons.Filled.Eco, null, tint = brand.moss, modifier = Modifier.size(14.dp))
                }
            }
            Text(name, fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = brand.ink, maxLines = 1, modifier = Modifier.weight(1f))
            Text(day, fontSize = 12.sp, color = brand.inkSoft)
        }
        Text(body, fontSize = 16.sp, lineHeight = 22.sp, color = brand.ink)
    }
}

@Composable
private fun NoteButton(onGrey: Boolean, edit: Boolean, onClick: () -> Unit) {
    val brand = Brand.colors
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp),
        modifier = Modifier
            .heightIn(min = 44.dp)
            .background(if (onGrey) brand.surface else Color.Transparent, CircleShape)
            .border(1.dp, brand.hairline, CircleShape)
            .clickable(role = Role.Button, onClick = onClick)
            .padding(horizontal = 18.dp),
    ) {
        Icon(Icons.Outlined.EditNote, null, tint = brand.ink, modifier = Modifier.size(18.dp))
        Text(stringResource(if (edit) R.string.note_edit else R.string.note_write), fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
    }
}

// MARK: - Getting there, something's wrong, discover more, credit

@Composable
private fun GettingThere(tree: Tree) {
    val brand = Brand.colors
    val rows = listOfNotNull(
        tree.howToRecognise.trim().ifEmpty { null }?.let { it to Icons.Outlined.Visibility },
        tree.access.trim().takeIf { it.isNotEmpty() && !tree.paidEntry && !Tree.accessPlainFree(it) }?.let { it to Icons.AutoMirrored.Filled.DirectionsWalk },
        tree.transport.trim().ifEmpty { null }?.let { it to Icons.Filled.Tram },
    )
    if (rows.isEmpty()) return
    Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
        Text(stringResource(R.string.getting_there), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 18.sp, color = brand.ink, modifier = Modifier.semantics { heading() })
        for ((text, icon) in rows) {
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Box(Modifier.width(22.dp).padding(top = 1.dp), contentAlignment = Alignment.TopCenter) {
                    Icon(icon, null, tint = brand.moss, modifier = Modifier.size(17.dp))
                }
                ExpandableText(text, lines = 2, style = TextStyle(fontSize = 15.sp, lineHeight = 20.sp, color = brand.ink))
            }
        }
    }
}

private data class Ask(val reason: String, val label: Int, val question: Int, val hint: Int)

private val ASKS = listOf(
    Ask("dead or gone", R.string.report_dead, R.string.ask_dead_q, R.string.ask_dead_hint),
    Ask("wrong location", R.string.report_location, R.string.ask_location_q, R.string.ask_location_hint),
    Ask("could not tell which tree", R.string.report_which, R.string.ask_which_q, R.string.ask_which_hint),
    Ask("could not reach it", R.string.report_reach, R.string.ask_reach_q, R.string.ask_reach_hint),
    Ask("on the map twice", R.string.report_twice, R.string.ask_twice_q, R.string.ask_twice_hint),
    Ask("something else", R.string.report_else, R.string.ask_else_q, R.string.ask_else_hint),
)

/** WorthItView: "Something's wrong", its six chips, and the one question after. */
@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun WorthItView(tree: Tree, account: Account, signedIn: Boolean, votes: MyVotes, actions: TreePageActions) {
    val brand = Brand.colors
    val scope = rememberCoroutineScope()
    var open by remember { mutableStateOf(false) }
    var detail by remember { mutableStateOf("") }
    fun send(verdict: String, reason: String) = scope.launch {
        Submission.feedback(tree.city, Submission.treeField(tree.id, tree.name), "$verdict: $reason", account.fresh()?.accessToken)
    }
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text(
            stringResource(R.string.something_wrong),
            fontSize = 13.sp,
            fontWeight = FontWeight.SemiBold,
            color = brand.inkSoft,
            textDecoration = TextDecoration.Underline,
            modifier = Modifier
                .pull(13.dp, 13.dp)
                .heightIn(min = 44.dp)
                .clickable(role = Role.Button, interactionSource = remember { MutableInteractionSource() }, indication = null) { open = !open }
                .wrapCentreVertically(),
        )
        if (open) {
            Text(stringResource(R.string.whats_wrong), fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
            FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                for (a in ASKS) {
                    SmallBordered(stringResource(a.label)) {
                        if (!signedIn) {
                            actions.onNeedsSignIn { }
                        } else {
                            votes.markReported(tree.id, a.reason)
                            detail = ""
                            open = false
                            send("report", a.reason)
                        }
                    }
                }
            }
        }
        if (votes.hasReported(tree.id) && !open) {
            val sent = votes.hasDetailed(tree.id)
            Text(stringResource(if (sent) R.string.report_thanks_more else R.string.report_thanks), fontSize = 13.sp, color = brand.inkSoft)
            val ask = ASKS.firstOrNull { it.reason == votes.reason(tree.id) }
            if (!sent && ask != null) {
                Text(stringResource(ask.question), fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
                Box(
                    Modifier
                        .fillMaxWidth()
                        .heightIn(min = 60.dp)
                        .border(1.dp, brand.hairline, RoundedCornerShape(6.dp))
                        .padding(8.dp),
                ) {
                    BasicTextField(
                        value = detail,
                        onValueChange = { detail = it },
                        textStyle = TextStyle(fontSize = 17.sp, color = brand.ink),
                        cursorBrush = SolidColor(brand.moss),
                        modifier = Modifier.fillMaxWidth(),
                    )
                    if (detail.isEmpty()) Text(stringResource(ask.hint), fontSize = 17.sp, color = brand.inkSoft.copy(alpha = 0.6f))
                }
                val ready = detail.trim().isNotEmpty()
                SmallBordered(stringResource(R.string.send), enabled = ready) {
                    if (!signedIn) {
                        actions.onNeedsSignIn { }
                    } else {
                        send("report detail", detail.trim().take(1000))
                        votes.markDetailed(tree.id)
                    }
                }
            }
        }
    }
}

/** The system's small bordered button (.bordered, .small): a tinted capsule. */
@Composable
private fun SmallBordered(label: String, enabled: Boolean = true, onClick: () -> Unit) {
    val brand = Brand.colors
    Box(
        Modifier
            .heightIn(min = 28.dp)
            .background(brand.moss.copy(alpha = if (enabled) 0.12f else 0.06f), CircleShape)
            .clickable(enabled = enabled, role = Role.Button, onClick = onClick)
            .padding(horizontal = 11.dp, vertical = 5.dp),
        contentAlignment = Alignment.Center,
    ) {
        Text(label, fontSize = 15.sp, color = if (enabled) brand.moss else brand.inkSoft.copy(alpha = 0.5f))
    }
}

/** discoverMore: the city and the country, as wrapping chips. */
@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun DiscoverMore(tree: Tree, actions: TreePageActions) {
    val brand = Brand.colors
    Column(Modifier.padding(top = 4.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text(stringResource(R.string.discover_more), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 18.sp, color = brand.ink, modifier = Modifier.semantics { heading() })
        FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            DiscoverChip(tree.city, Icons.Outlined.LocationCity) { actions.onGo(SearchHit.City(tree.citySlug, tree.city, tree.lat, tree.lng)) }
            if (tree.country.isNotEmpty()) {
                DiscoverChip(tree.country, Icons.Outlined.Public) { actions.onGo(SearchHit.Country(tree.country)) }
            }
        }
    }
}

@Composable
private fun DiscoverChip(title: String, icon: ImageVector, onClick: () -> Unit) {
    val brand = Brand.colors
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp),
        modifier = Modifier
            .heightIn(min = 44.dp)
            .background(brand.moss.copy(alpha = 0.10f), CircleShape)
            .clickable(role = Role.Button, onClick = onClick)
            .padding(horizontal = 14.dp, vertical = 8.dp),
    ) {
        Icon(icon, null, tint = brand.ink, modifier = Modifier.size(14.dp))
        Text(title, fontSize = 15.sp, fontWeight = FontWeight.Medium, color = brand.ink, maxLines = 2)
    }
}

/** The credit, the last line on the page and only where the licence asks for it. */
@Composable
private fun CreditLine(tree: Tree, shotAt: Int) {
    val brand = Brand.colors
    val context = LocalContext.current
    val p = tree.shots.getOrNull(shotAt) ?: tree.photo ?: return
    val c = p.credit ?: return
    val link = p.creditUrl
    Text(
        stringResource(R.string.photo_credit, c),
        fontSize = 10.sp,
        color = brand.inkSoft.copy(alpha = 0.45f),
        maxLines = 1,
        overflow = TextOverflow.Ellipsis,
        modifier = if (link != null) Modifier.clickable { openUrl(context, link) } else Modifier,
    )
}

// MARK: - The bar

/** barCircle: 52, the surface, a hairline; the moss tint when it is on. */
@Composable
private fun BarCircle(icon: ImageVector, label: String, on: Boolean = false, tint: Color = Brand.colors.moss, onClick: () -> Unit) {
    val brand = Brand.colors
    Box(
        Modifier
            .size(52.dp)
            .background(if (on) brand.moss.copy(alpha = 0.12f) else brand.surface, CircleShape)
            .border(1.dp, if (on) brand.moss else brand.hairline, CircleShape)
            .clickable(role = Role.Button, onClick = onClick)
            .semantics { contentDescription = label },
        contentAlignment = Alignment.Center,
    ) {
        Icon(icon, null, tint = tint, modifier = Modifier.size(22.dp))
    }
}

/** BrandButtonStyle: the primary capsule, 48 high, as wide as the bar allows. */
@Composable
private fun BigButton(label: String, icon: ImageVector, modifier: Modifier = Modifier, onClick: () -> Unit) {
    val brand = Brand.colors
    Row(
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically,
        modifier = modifier
            .height(48.dp)
            .background(brand.moss, CircleShape)
            .clickable(role = Role.Button, onClick = onClick),
    ) {
        Icon(icon, null, tint = brand.onMoss, modifier = Modifier.size(18.dp))
        Spacer(Modifier.width(8.dp))
        Text(label, fontSize = 16.sp, fontWeight = FontWeight.SemiBold, color = brand.onMoss, maxLines = 1)
    }
}

@Composable
private fun ActionBar(
    tree: Tree,
    standingHere: Boolean,
    kmAway: Double?,
    collected: Boolean,
    hearted: Boolean,
    onDirections: () -> Unit,
    onCollect: () -> Unit,
    onHeart: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val brand = Brand.colors
    Column(modifier.fillMaxWidth().background(brand.ground)) {
        Box(Modifier.fillMaxWidth().height(0.5.dp).background(brand.hairline))
        Row(
            Modifier.fillMaxWidth().padding(horizontal = 20.dp).padding(top = 10.dp, bottom = 8.dp).navigationBarsPadding(),
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            val collectLabel = stringResource(if (collected) R.string.seen_it_done else R.string.seen_it)
            val collectIcon = if (collected) Icons.Filled.Verified else Icons.Outlined.PhotoCamera
            val take = stringResource(R.string.take_me_there)
            if (standingHere) {
                BigButton(collectLabel, collectIcon, Modifier.weight(1f), onCollect)
                BarCircle(Icons.Filled.TurnRight, take, onClick = onDirections)
            } else {
                BigButton(
                    if (kmAway != null) stringResource(R.string.take_me_there_far, farLabel(kmAway)) else take,
                    Icons.Filled.TurnRight,
                    Modifier.weight(1f),
                    onDirections,
                )
                BarCircle(collectIcon, collectLabel, on = collected, onClick = onCollect)
            }
            // SaveHeart, inBar.
            val save = if (hearted) stringResource(R.string.saved_tap_remove, tree.name) else stringResource(R.string.save_tree, tree.name)
            BarCircle(
                if (hearted) Icons.Filled.Bookmark else Icons.Outlined.BookmarkBorder,
                save,
                tint = if (hearted) brand.moss else brand.inkSoft,
                onClick = onHeart,
            )
        }
    }
}

// MARK: - The report form (Contribute.swift, about one tree)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun ReportSheet(tree: Tree, opening: String, account: Account, signedIn: Boolean, actions: TreePageActions, onDismiss: () -> Unit) {
    val brand = Brand.colors
    val scope = rememberCoroutineScope()
    var where by remember { mutableStateOf("") }
    var why by remember { mutableStateOf(opening + "\n") }
    var sending by remember { mutableStateOf(false) }
    var sent by remember { mutableStateOf(false) }
    var failed by remember { mutableStateOf(false) }
    LaunchedEffect(Unit) { if (!signedIn) actions.onNeedsSignIn { } }
    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true),
        containerColor = brand.surfaceMuted,
    ) {
        Column(Modifier.fillMaxWidth().padding(horizontal = 16.dp).padding(bottom = 24.dp).navigationBarsPadding()) {
            Row(Modifier.fillMaxWidth().height(44.dp), verticalAlignment = Alignment.CenterVertically) {
                Text(
                    stringResource(if (sent) R.string.done else R.string.cancel),
                    fontSize = 17.sp,
                    color = brand.moss,
                    modifier = Modifier.clickable(role = Role.Button, onClick = onDismiss),
                )
                Text(
                    stringResource(if (sent) R.string.sent_title else R.string.tell_us),
                    fontSize = 17.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = brand.ink,
                    textAlign = TextAlign.Center,
                    modifier = Modifier.weight(1f),
                )
                Spacer(Modifier.width(56.dp))
            }
            Spacer(Modifier.height(12.dp))
            val group = Modifier.fillMaxWidth().background(brand.surface, RoundedCornerShape(10.dp)).padding(horizontal = 16.dp, vertical = 11.dp)
            if (sent) {
                Column(group, verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Icon(Icons.Filled.Verified, null, tint = brand.moss, modifier = Modifier.size(20.dp))
                        Text(stringResource(R.string.thank_you), fontSize = 17.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
                    }
                    Text(stringResource(R.string.we_read_every_tip), fontSize = 13.sp, color = brand.inkSoft)
                }
            } else if (!signedIn) {
                Column(group, verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(stringResource(R.string.report_needs_account), fontSize = 13.sp, color = brand.inkSoft)
                    Text(
                        stringResource(R.string.sign_in),
                        fontSize = 16.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = brand.moss,
                        modifier = Modifier.clickable(role = Role.Button) { actions.onNeedsSignIn { } },
                    )
                }
            } else {
                Text(stringResource(R.string.about_this_tree).uppercase(), fontSize = 13.sp, color = brand.inkSoft, modifier = Modifier.padding(start = 16.dp, bottom = 6.dp))
                Column(group, verticalArrangement = Arrangement.spacedBy(3.dp)) {
                    Text(tree.name, fontSize = 16.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
                    Text(tree.city, fontSize = 13.sp, color = brand.inkSoft)
                }
                Spacer(Modifier.height(20.dp))
                Box(group) {
                    BasicTextField(where, { where = it }, textStyle = TextStyle(fontSize = 17.sp, color = brand.ink), cursorBrush = SolidColor(brand.moss), modifier = Modifier.fillMaxWidth())
                    if (where.isEmpty()) Text(stringResource(R.string.where_really), fontSize = 17.sp, color = brand.inkSoft.copy(alpha = 0.6f))
                }
                Spacer(Modifier.height(20.dp))
                Box(group.heightIn(min = 110.dp)) {
                    BasicTextField(why, { why = it }, textStyle = TextStyle(fontSize = 17.sp, color = brand.ink), cursorBrush = SolidColor(brand.moss), modifier = Modifier.fillMaxWidth())
                    if (why.isEmpty()) Text(stringResource(R.string.what_should_we_know), fontSize = 17.sp, color = brand.inkSoft.copy(alpha = 0.6f))
                }
                Text(stringResource(R.string.nobody_sees), fontSize = 13.sp, color = brand.inkSoft, modifier = Modifier.padding(start = 16.dp, top = 6.dp, end = 16.dp))
                Spacer(Modifier.height(20.dp))
                val ready = !sending && why.isNotEmpty()
                Box(
                    group.clickable(enabled = ready, role = Role.Button) {
                        sending = true
                        scope.launch {
                            val ok = Submission.correction(tree.city, tree.name, where, why, tree.url, account.fresh()?.accessToken)
                            sending = false
                            if (ok) sent = true else failed = true
                        }
                    },
                    contentAlignment = Alignment.Center,
                ) {
                    Text(
                        stringResource(if (sending) R.string.sending else R.string.send),
                        fontSize = 17.sp,
                        color = if (ready) brand.moss else brand.inkSoft.copy(alpha = 0.5f),
                    )
                }
                if (failed) Text(stringResource(R.string.note_failed), fontSize = 13.sp, color = brand.dangerText, modifier = Modifier.padding(top = 6.dp))
            }
        }
    }
}
