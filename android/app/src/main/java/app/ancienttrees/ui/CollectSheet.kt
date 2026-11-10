// Collecting a tree: one action, and we work out which kind it was. Ported line
// by line from ios Screens/CollectSheet.swift and Screens/CollectIntro.swift; the
// reasons live in the Swift comments and are repeated here only where the
// Android code has to make the same choice.
//
// ADD and COLLECT are the same physical act (Hidde, 2026-08-23): one button and
// one camera, and the app resolves the outcome from where the shutter fell.
// The photograph is compulsory: it is proof of presence. Sign in before the
// camera, never after the photograph (2026-10-12).
//
// Steps: intro (take or choose), place (the photograph does not say where),
// identify (which one is it), ticked (you found it), unsure (we will work it
// out), compare (is this the one). A tree only you have goes straight to its own
// page as a draft with Save at the foot (DraftTree.kt).

package app.ancienttrees.ui

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.InlineTextContent
import androidx.compose.foundation.text.appendInlineContent
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Help
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.AddCircle
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Image
import androidx.compose.material.icons.filled.ThumbDown
import androidx.compose.material.icons.filled.ThumbUp
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.PhotoCamera
import androidx.compose.material.icons.outlined.PhotoLibrary
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.Share
import androidx.compose.material.icons.outlined.ThumbDown
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.ModalBottomSheetProperties
import androidx.compose.material3.SheetValue
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringArrayResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.Placeholder
import androidx.compose.ui.text.PlaceholderVerticalAlign
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.account.Account
import app.ancienttrees.account.Collector
import app.ancienttrees.account.MyTrees
import app.ancienttrees.account.MyVotes
import app.ancienttrees.account.OwnSighting
import app.ancienttrees.account.Submission
import app.ancienttrees.account.TreeNotes
import app.ancienttrees.account.VoteCounts
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.feed.CollectRules
import app.ancienttrees.feed.CollectRules.Fix
import app.ancienttrees.feed.Geo
import app.ancienttrees.feed.Here
import app.ancienttrees.feed.Precision
import app.ancienttrees.feed.Tree
import kotlinx.coroutines.launch
import java.util.Date
import java.util.Locale

/** How the sheet was opened: the tree somebody came from, when there is one. */
data class CollectStart(
    /** The tree's name, when the camera was tapped on a tree (CollectIntro.about). */
    val about: String? = null,
    /** Came in from the tree's missing photograph: the sheet is about adding a photo. */
    val addsPhoto: Boolean = false,
    /** The tree whose own page this started from: no "which one is it" list. */
    val knownTree: String? = null,
    /** A photograph that arrives already taken or chosen, from the tree page's own sheet. */
    val shotIn: ByteArray? = null,
    val pickedIn: Collector.Picked? = null,
    /** Further photographs chosen with [pickedIn], already downsized. */
    val pickedMore: List<ByteArray> = emptyList(),
)

/** The sweep's launch arguments for the flow (ios Kit/Launch.swift). */
data class CollectLaunch(
    val place: Boolean = false,
    val identify: Boolean = false,
    val ticked: Boolean = false,
    val voted: Boolean = false,
    val compare: Boolean = false,
    val describe: Boolean = false,
)

private sealed class Stage {
    data object Intro : Stage()
    data object Place : Stage()
    data object Identify : Stage()
    data class Ticked(val id: String) : Stage()
    data object Unsure : Stage()
    data class Compare(val id: String) : Stage()
}

/** Everything the flow asks of the app around it. */
class CollectHost(
    val account: Account,
    val signedIn: Boolean,
    val collected: Set<String>,
    val votes: MyVotes,
    val counts: VoteCounts,
    /** Sign in first, then carry on with what was being done. */
    val needsSignIn: (() -> Unit) -> Unit,
    /** Location is asked at the first photograph, as iNaturalist and Seek do. */
    val askLocation: () -> Unit,
    /** Runs past the sheet's own life; false means it did not reach the account. */
    val send: (suspend () -> Boolean) -> Unit,
    val ticked: (String) -> Unit,
    val openDraft: (Collector.Draft) -> Unit,
    val share: (Tree) -> Unit,
    /** Your own trees (My trees), so a second photograph of one is offered to it. */
    val mine: MyTrees? = null,
    /** Opens your own tree's page (navigator.push = .mine), after a photo joins it. */
    val openMine: (String) -> Unit = {},
)

/**
 * CollectSheet.yoursNear: a tree of yours within [SAME_TREE_METRES] of the
 * photograph, nearest first, at most two. Within 30 metres two photographs are
 * nearly always of the same trunk, the distance the server matches a sighting at
 * (scripts/sightings_inbox.py, MATCH_M). YOUR OWN TREE, PHOTOGRAPHED AGAIN
 * (Hidde, 2026-10-18: "twee losse pins voor twee foto's van 1 boom"): offered
 * first, and picking it adds the photograph to that tree, as Google Maps adds a
 * photo to a place you already put on the map instead of a new place.
 */
fun yoursNear(lat: Double, lng: Double, yours: List<OwnSighting>): List<OwnSighting> =
    yours.map { it to Geo.km(lat, lng, it.lat, it.lng) * 1000 }
        .filter { it.second <= SAME_TREE_METRES }
        .sortedBy { it.second }
        .take(2)
        .map { it.first }

const val SAME_TREE_METRES = 30.0

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CollectSheet(
    catalogue: Catalogue,
    origin: Here,
    located: Boolean,
    host: CollectHost,
    start: CollectStart,
    launch: CollectLaunch,
    onDismiss: () -> Unit,
) {
    val brand = Brand.colors
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val trees = catalogue.trees
    var stage by remember { mutableStateOf<Stage>(Stage.Intro) }
    var fix by remember { mutableStateOf(Fix.DEVICE) }
    var taken by remember { mutableStateOf<Date?>(null) }
    var placing by remember { mutableStateOf<Here?>(null) }
    var shot by remember { mutableStateOf<ByteArray?>(null) }
    var extras by remember { mutableStateOf<List<ByteArray>>(emptyList()) }
    var newFind by remember { mutableStateOf(true) }
    var at by remember { mutableStateOf<Here?>(null) }
    var confirmingDiscard by remember { mutableStateOf(false) }
    var query by remember { mutableStateOf("") }
    var pinReported by remember { mutableStateOf(false) }
    var reading by remember { mutableStateOf(false) }
    val known = start.knownTree?.let { catalogue.byId[it] }

    val here = at ?: origin
    val nothingNear = CollectRules.nearby(here.lat, here.lng, trees).isEmpty()
    val candidates = if (nothingNear) {
        if (query.isBlank()) CollectRules.closest(here.lat, here.lng, trees) else CollectRules.search(query, here.lat, here.lng, trees)
    } else {
        CollectRules.nearby(here.lat, here.lng, trees)
    }
    val ownNear = host.mine?.let { yoursNear(here.lat, here.lng, it.yoursOnly) }.orEmpty()

    val hasWork = when (stage) {
        Stage.Intro, Stage.Unsure, is Stage.Ticked -> false
        else -> shot != null
    }
    val fits = stage is Stage.Ticked || stage == Stage.Unsure || stage is Stage.Compare

    // THE PHOTOGRAPHS AFTER A TICK OF OURS: filed where the phone stood.
    fun claim(t: Tree, image: ByteArray, h: Here) {
        val isNew = t.id !in host.collected
        newFind = isNew
        val more = extras
        val when_ = taken ?: Date()
        extras = emptyList()
        host.ticked(t.id)
        host.send { Collector.collect(host.account, t.id, t.name, image, h.lat, h.lng, more, when_) }
        stage = Stage.Ticked(t.id)
    }

    fun placePhrase(h: Here): String? {
        val near = CollectRules.nearestTree(h.lat, h.lng, trees) ?: return null
        return when (CollectRules.placeKind(near.first.city, near.second)) {
            CollectRules.Near.IN -> context.getString(R.string.cf_in_city, near.first.city)
            CollectRules.Near.NEAR -> context.getString(R.string.cf_near_city, near.first.city)
            null -> null
        }
    }

    // A TREE WE DO NOT HAVE: straight to its own page, as a draft with Save.
    fun startDraft(force: Boolean = false) {
        if (!force && !host.signedIn) {
            host.needsSignIn { }
            return
        }
        val h = at ?: origin
        val place = placePhrase(h)
        val name = if (place != null) context.getString(R.string.cf_a_tree_at, place) else context.getString(R.string.cf_unnamed)
        host.openDraft(
            Collector.Draft(
                id = Collector.newId(), name = name, lat = h.lat, lng = h.lng, jpeg = shot, extras = extras,
                taken = taken ?: Date(), fixNote = fix.note, place = place,
            ),
        )
        extras = emptyList()
        shot = null
        onDismiss()
    }

    fun settle(image: ByteArray, h: Here, source: Fix) {
        shot = image
        at = h
        fix = source
        pinReported = false
        query = ""
        when {
            known != null -> claim(known, image, h)
            CollectRules.nearby(h.lat, h.lng, trees).isEmpty() && CollectRules.closest(h.lat, h.lng, trees).isEmpty() &&
                host.mine?.let { yoursNear(h.lat, h.lng, it.yoursOnly) }.isNullOrEmpty() -> startDraft()
            else -> stage = Stage.Identify
        }
    }

    // The photograph joins the tree you already added, and its page opens.
    fun addToYours(s: OwnSighting) {
        val store = host.mine ?: return
        val images = listOfNotNull(shot) + extras
        host.send {
            var ok = true
            for (img in images) ok = store.addExtra(s.id, img) && ok
            ok
        }
        extras = emptyList()
        shot = null
        onDismiss()
        host.openMine(s.id)
    }

    // THE CAMERA PATH: standing there is the fix, unless the phone has none.
    fun resolve(image: ByteArray) {
        taken = null
        when (val r = CollectRules.route(cameraShot = true, locationKnown = located, photoHasCoordinate = false)) {
            is CollectRules.Route.Settle -> settle(image, origin, r.fix)
            CollectRules.Route.AskForThePin -> {
                if (known != null) {
                    settle(image, Here(known.lat, known.lng), Fix.PLACED)
                } else {
                    shot = image
                    placing = origin
                    stage = Stage.Place
                }
            }
        }
    }

    // THE CAMERA ROLL PATH: the photograph's own coordinate, or we ask.
    fun picked(first: ByteArray, p: Collector.Picked, more: List<ByteArray>) {
        shot = first
        extras = more
        taken = p.taken
        val lat = p.lat
        val lng = p.lng
        if ((lat == null || lng == null) && known != null) {
            settle(first, Here(known.lat, known.lng), Fix.PLACED)
            return
        }
        val r = CollectRules.route(cameraShot = false, locationKnown = located, photoHasCoordinate = lat != null && lng != null)
        if (r is CollectRules.Route.Settle && lat != null && lng != null) {
            settle(first, Here(lat, lng), r.fix)
        } else {
            placing = origin
            stage = Stage.Place
        }
    }

    // The system camera writes into our cache; read, downsized, deleted.
    val file = remember { java.io.File(context.cacheDir, "photos").apply { mkdirs() }.let { java.io.File(it, "collect.jpg") } }
    val fileUri = remember { androidx.core.content.FileProvider.getUriForFile(context, context.packageName + ".photos", file) }
    val camera = rememberLauncherForActivityResult(ActivityResultContracts.TakePicture()) { ok ->
        if (!ok) return@rememberLauncherForActivityResult
        reading = true
        scope.launch {
            val raw = runCatching { file.readBytes() }.getOrNull()
            file.delete()
            val jpeg = raw?.let { Collector.downsized(it) }
            reading = false
            if (jpeg != null) resolve(jpeg)
        }
    }
    val library = rememberLauncherForActivityResult(
        ActivityResultContracts.PickMultipleVisualMedia(1 + Collector.MAX_EXTRAS),
    ) { uris ->
        if (uris.isEmpty()) return@rememberLauncherForActivityResult
        reading = true
        scope.launch {
            val all = uris.mapNotNull { Collector.read(context, it) }
            val first = all.firstOrNull()
            val firstJpeg = first?.let { Collector.downsized(it.raw) }
            val more = all.drop(1).mapNotNull { Collector.downsized(it.raw) }
            reading = false
            if (first != null && firstJpeg != null) picked(firstJpeg, first, more)
        }
    }

    fun openCamera() {
        if (!host.signedIn) {
            host.needsSignIn { }
            return
        }
        if (!located) host.askLocation()
        runCatching { camera.launch(fileUri) }
    }

    fun openLibrary() {
        if (!host.signedIn) {
            host.needsSignIn { }
            return
        }
        library.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
    }

    // THE "I AM NOT SURE" ANSWER: no tick, the photograph and the shortlist go to us.
    fun notSure() {
        if (!host.signedIn) {
            host.needsSignIn { }
            return
        }
        val h = at ?: origin
        val picks = candidates
        val image = shot
        val more = extras
        val id = Collector.newId()
        val name = picks.firstOrNull()?.name ?: context.getString(R.string.cf_unplaced)
        val when_ = taken ?: Date()
        val note = fix.note
        val city = CollectRules.nearestTree(h.lat, h.lng, trees)?.first?.city.orEmpty()
        host.send {
            val ok = Collector.send(host.account, id, null, name, h.lat, h.lng, image, more, when_)
            Submission.correction(
                city, id, String.format(Locale.ROOT, "%.5f, %.5f (%s)", h.lat, h.lng, note),
                "could not tell which tree: " + picks.joinToString("; ") { "${it.name} (${it.id})" },
                "app:collect-unsure", host.account.fresh()?.accessToken,
            )
            ok
        }
        extras = emptyList()
        shot = null
        stage = Stage.Unsure
    }

    // A FAR PICK IS A PIN CORRECTION as well as a find (PlacePin's channel).
    fun reportPin(t: Tree, h: Here) {
        pinReported = true
        val metres = (Geo.km(h.lat, h.lng, t.lat, t.lng) * 1000).toInt()
        val note = fix.note
        scope.launch {
            Submission.correction(
                t.city, t.name, String.format(Locale.ROOT, "%.6f, %.6f (%s)", h.lat, h.lng, note),
                "Collected with a photograph $metres m from the published position, " +
                    "picked from the closest trees because none of ours was pinned within 400 m. " +
                    "Our pin was ${if (t.precision == Precision.CONFIRMED) "marked confirmed" else "marked approximate"}.",
                t.url, host.account.fresh()?.accessToken,
            )
        }
    }

    // The sweep's states, each with a stand-in photograph (a simulator has no camera).
    LaunchedEffect(Unit) {
        val stand = ByteArray(1)
        val first = CollectRules.nearby(origin.lat, origin.lng, trees).firstOrNull()
            ?: CollectRules.closest(origin.lat, origin.lng, trees).firstOrNull()
        when {
            launch.compare && first != null -> { at = origin; shot = stand; stage = Stage.Compare(first.id) }
            launch.ticked && first != null -> {
                at = origin; pinReported = CollectRules.isFar(origin.lat, origin.lng, first); shot = stand
                stage = Stage.Ticked(first.id)
            }
            launch.describe -> { at = origin; shot = null; startDraft(force = true) }
            launch.identify -> { at = origin; shot = stand; stage = Stage.Identify }
            launch.place -> { placing = origin; stage = Stage.Place }
            start.shotIn != null -> resolve(start.shotIn)
            start.pickedIn != null -> Collector.downsized(start.pickedIn.raw)?.let { picked(it, start.pickedIn, start.pickedMore) }
        }
    }

    fun closeTapped() {
        if (hasWork) confirmingDiscard = true else onDismiss()
    }

    // A SWIPE CANNOT THROW IT AWAY EITHER (Hidde, 2026-08-29): with a photograph
    // in hand, every way out goes through the one control that asks.
    val workNow by rememberUpdatedState(hasWork)
    val sheet = rememberModalBottomSheetState(
        skipPartiallyExpanded = true,
        confirmValueChange = { v -> if (v == SheetValue.Hidden && workNow) { confirmingDiscard = true; false } else true },
    )
    ModalBottomSheet(
        onDismissRequest = {
            if (workNow) {
                confirmingDiscard = true
                scope.launch { sheet.show() }
            } else {
                onDismiss()
            }
        },
        sheetState = sheet,
        containerColor = brand.ground,
        properties = ModalBottomSheetProperties(shouldDismissOnBackPress = true),
        modifier = Modifier.testTag("spot-sheet"),
    ) {
        val tall = stage == Stage.Place || stage == Stage.Identify
        Box(if (tall) Modifier.fillMaxHeight() else Modifier) {
            when (val s = stage) {
                Stage.Intro -> CollectIntro(
                    about = start.about,
                    addsPhoto = start.addsPhoto,
                    onStart = { openCamera() },
                    onLibrary = { openLibrary() },
                    onClose = { closeTapped() },
                )
                Stage.Place -> PlaceStep(
                    start = placing ?: origin,
                    trees = trees,
                    onMove = { placing = it },
                    // Never asked is not refused: the first tap asks (RecentreButton.recentre).
                    onLocate = { if (located) true else { host.askLocation(); false } },
                    onConfirm = {
                        val c = placing
                        val image = shot
                        if (c != null && image != null) settle(image, c, Fix.PLACED)
                    },
                    onClose = { closeTapped() },
                )
                Stage.Identify -> IdentifyStep(
                    here = here,
                    located = at != null || located,
                    candidates = candidates,
                    ownNear = ownNear,
                    mine = host.mine,
                    onYours = { addToYours(it) },
                    nothingNear = nothingNear,
                    query = query,
                    onQuery = { query = it },
                    blurb = when {
                        candidates.isEmpty() && ownNear.isNotEmpty() -> stringResource(R.string.cf_blurb_yours)
                        nothingNear -> stringResource(if (query.isBlank()) R.string.cf_blurb_far else R.string.cf_blurb_far_query)
                        candidates.any { it.precision == Precision.APPROXIMATE } -> stringResource(R.string.cf_blurb_rough)
                        fix == Fix.DEVICE -> stringResource(R.string.cf_blurb_device)
                        else -> stringResource(R.string.cf_blurb_photo)
                    },
                    onPick = { t ->
                        if (CollectRules.isFar(here.lat, here.lng, t)) {
                            stage = Stage.Compare(t.id)
                        } else {
                            val image = shot
                            val h = at
                            if (image != null && h != null) claim(t, image, h)
                        }
                    },
                    onCompare = { stage = Stage.Compare(it.id) },
                    onNew = { startDraft() },
                    onNotSure = { notSure() },
                    onClose = { closeTapped() },
                )
                else -> FitStep(onClose = { closeTapped() }) {
                    when (s) {
                        is Stage.Ticked -> catalogue.byId[s.id]?.let { t ->
                            TickedStep(t, newFind, pinReported, host, launch.voted, onDone = onDismiss)
                        }
                        Stage.Unsure -> UnsureStep(onDone = onDismiss)
                        is Stage.Compare -> catalogue.byId[s.id]?.let { t ->
                            CompareStep(
                                t = t,
                                here = here,
                                located = at != null || located,
                                onThis = {
                                    val image = shot
                                    val h = at
                                    if (image != null && h != null) {
                                        if (CollectRules.isFar(h.lat, h.lng, t)) reportPin(t, h)
                                        claim(t, image, h)
                                    }
                                },
                                onBack = { stage = Stage.Identify },
                            )
                        }
                        else -> Unit
                    }
                }
            }
        }
    }

    if (confirmingDiscard) {
        BrandSheet(
            title = stringResource(R.string.cf_discard_title),
            message = stringResource(R.string.cf_discard_body),
            onDismiss = { confirmingDiscard = false },
            buttons = listOf(
                SheetButton(stringResource(R.string.cf_discard), SheetKind.DESTRUCTIVE) {
                    confirmingDiscard = false
                    onDismiss()
                },
                SheetButton(stringResource(R.string.cf_keep_editing), SheetKind.SECONDARY) { confirmingDiscard = false },
            ),
        )
    }
}

// MARK: - The intro (CollectIntro.swift)

@Composable
private fun CollectIntro(
    about: String?,
    addsPhoto: Boolean,
    onStart: () -> Unit,
    onLibrary: () -> Unit,
    onClose: () -> Unit,
) {
    val brand = Brand.colors
    Box {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 20.dp)
                .padding(top = 12.dp, bottom = 8.dp)
                .navigationBarsPadding(),
        ) {
            SheetIconTile(Icons.Outlined.PhotoCamera)
            Spacer(Modifier.height(16.dp))
            SheetTitleText(
                stringResource(
                    when {
                        addsPhoto -> R.string.cf_add_photo
                        about == null -> R.string.cf_add_tree
                        else -> R.string.cf_add_this_tree
                    },
                ),
            )
            Text(
                stringResource(if (addsPhoto) R.string.cf_intro_photo else R.string.cf_intro),
                fontSize = 15.sp,
                color = brand.inkSoft,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(horizontal = 18.dp).padding(top = 8.dp, bottom = 22.dp),
            )
            Column(verticalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.fillMaxWidth()) {
                SheetButtonView(SheetButton(stringResource(R.string.cf_take), SheetKind.PRIMARY, Icons.Outlined.PhotoCamera, onStart), Modifier.testTag("add-start"))
                SheetButtonView(SheetButton(stringResource(R.string.cf_choose), SheetKind.SECONDARY, Icons.Outlined.PhotoLibrary, onLibrary), Modifier.testTag("add-library"))
            }
        }
        SheetCloseButton(onClose, Modifier.align(Alignment.TopEnd).padding(top = 0.dp))
    }
}

@Composable
private fun SheetTitleText(text: String) {
    Text(
        text,
        fontFamily = BrandFace,
        fontWeight = FontWeight.Bold,
        fontSize = 26.sp,
        lineHeight = 31.sp,
        color = Brand.colors.ink,
        textAlign = TextAlign.Center,
        modifier = Modifier.padding(horizontal = 18.dp).semantics { heading() },
    )
}

@Composable
private fun SheetMessageText(text: String) {
    Text(text, fontSize = 15.sp, color = Brand.colors.inkSoft, textAlign = TextAlign.Center, modifier = Modifier.padding(top = 8.dp))
}

@Composable
private fun SheetFootnoteText(text: String) {
    Text(text, fontSize = 13.sp, color = Brand.colors.inkSoft, textAlign = TextAlign.Center, modifier = Modifier.padding(top = 14.dp))
}

/** The one sheet's layout for the steps that answer or ask one thing. */
@Composable
private fun FitStep(onClose: () -> Unit, content: @Composable ColumnScope.() -> Unit) {
    Box {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .fillMaxWidth()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 24.dp)
                .padding(top = 12.dp, bottom = 16.dp)
                .navigationBarsPadding(),
            content = content,
        )
        SheetCloseButton(onClose, Modifier.align(Alignment.TopEnd))
    }
}

@Composable
private fun CloseRow(onClose: () -> Unit) {
    Row(Modifier.fillMaxWidth().padding(horizontal = 2.dp), horizontalArrangement = Arrangement.End) {
        SheetCloseButton(onClose)
    }
}

// MARK: - Where does it stand

@Composable
private fun PlaceStep(
    start: Here,
    trees: List<Tree>,
    onMove: (Here) -> Unit,
    /** True when the map may go to the person; false when it asked instead. */
    onLocate: () -> Boolean,
    onConfirm: () -> Unit,
    onClose: () -> Unit,
) {
    val brand = Brand.colors
    var recentre by remember { mutableIntStateOf(0) }
    Column(Modifier.fillMaxSize()) {
        CloseRow(onClose)
        Column(Modifier.padding(horizontal = 20.dp).padding(bottom = 12.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Text(stringResource(R.string.cf_where), fontFamily = BrandFace, fontWeight = FontWeight.ExtraBold, fontSize = 24.sp, color = brand.ink)
            Text(stringResource(R.string.cf_place_reason), fontSize = 15.sp, color = brand.inkSoft)
        }
        Box(Modifier.fillMaxWidth().weight(1f)) {
            PinPicker(
                start = start,
                trees = CollectRules.nearby(start.lat, start.lng, trees),
                spanMetres = 400.0,
                onMove = onMove,
                modifier = Modifier.fillMaxSize(),
                recentre = recentre,
            )
            // THE LOCATE ARROW, as every TreeMap on the iPhone carries it
            // (TreeMap.showsRecentre): trailing 12, and above the confirm button
            // with the iPhone's 18 points of air (its 120 from the bottom edge
            // less the 102 the button and the home indicator take there).
            RecentreButton(
                onClick = { if (onLocate()) recentre++ },
                modifier = Modifier
                    .align(Alignment.BottomEnd)
                    .navigationBarsPadding()
                    .padding(end = 12.dp, bottom = 86.dp)
                    .testTag("map-recentre"),
            )
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .padding(horizontal = 20.dp)
                    .padding(bottom = 20.dp)
                    .navigationBarsPadding()
                    .fillMaxWidth()
                    .height(48.dp)
                    .background(brand.moss, RoundedCornerShape(50))
                    .clickable(role = Role.Button, onClick = onConfirm)
                    .testTag("collect-place-confirm"),
            ) {
                Text(stringResource(R.string.cf_tree_is_here), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = brand.onMoss)
            }
        }
    }
}

// MARK: - Which one is it

@Composable
private fun IdentifyStep(
    here: Here,
    located: Boolean,
    candidates: List<Tree>,
    ownNear: List<OwnSighting>,
    mine: MyTrees?,
    onYours: (OwnSighting) -> Unit,
    nothingNear: Boolean,
    query: String,
    onQuery: (String) -> Unit,
    blurb: String,
    onPick: (Tree) -> Unit,
    onCompare: (Tree) -> Unit,
    onNew: () -> Unit,
    onNotSure: () -> Unit,
    onClose: () -> Unit,
) {
    val brand = Brand.colors
    Column(Modifier.fillMaxSize()) {
        CloseRow(onClose)
        Column(
            verticalArrangement = Arrangement.spacedBy(20.dp),
            modifier = Modifier
                .fillMaxWidth()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 20.dp)
                .padding(bottom = 32.dp)
                .navigationBarsPadding(),
        ) {
            Text(stringResource(R.string.cf_which), fontFamily = BrandFace, fontWeight = FontWeight.ExtraBold, fontSize = 24.sp, color = brand.ink)
            Text(blurb, fontSize = 15.sp, color = brand.inkSoft)
            if (candidates.isNotEmpty()) {
                val parts = stringResource(R.string.cf_tap_to_compare, "\u0000").split("\u0000")
                Text(
                    buildAnnotatedString {
                        append(parts.first())
                        appendInlineContent("info", "(i)")
                        append(parts.getOrElse(1) { "" })
                    },
                    inlineContent = mapOf(
                        "info" to InlineTextContent(Placeholder(14.sp, 14.sp, PlaceholderVerticalAlign.TextCenter)) {
                            Icon(Icons.Outlined.Info, null, tint = brand.inkSoft, modifier = Modifier.fillMaxSize())
                        },
                    ),
                    fontSize = 13.sp,
                    color = brand.inkSoft,
                )
            }
            if (mine != null) {
                ownNear.forEachIndexed { i, s ->
                    OwnRow(s, here, mine, Modifier.clickable(role = Role.Button) { onYours(s) }.testTag("collect-yours-$i"))
                }
            }
            if (nothingNear) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier
                        .fillMaxWidth()
                        .heightIn(min = 44.dp)
                        .background(brand.surfaceMuted, RoundedCornerShape(14.dp))
                        .padding(horizontal = 12.dp),
                ) {
                    Icon(Icons.Outlined.Search, null, tint = brand.inkSoft, modifier = Modifier.size(20.dp))
                    Spacer(Modifier.width(8.dp))
                    Box(Modifier.weight(1f)) {
                        BasicTextField(
                            value = query,
                            onValueChange = onQuery,
                            singleLine = true,
                            textStyle = TextStyle(fontSize = 16.sp, color = brand.ink),
                            cursorBrush = SolidColor(brand.moss),
                            modifier = Modifier.fillMaxWidth().testTag("collect-search"),
                        )
                        if (query.isEmpty()) Text(stringResource(R.string.cf_search), fontSize = 16.sp, color = brand.inkSoft)
                    }
                }
                if (candidates.isEmpty() && query.trim().length >= 2) {
                    Text(stringResource(R.string.cf_none_called), fontSize = 13.sp, color = brand.inkSoft)
                }
            }
            val compass = stringArrayResource(R.array.cf_compass)
            candidates.forEachIndexed { i, t ->
                Box {
                    CandidateRow(t, here, located, compass, Modifier.clickable(role = Role.Button) { onPick(t) }.testTag("collect-candidate-$i"))
                    val label = stringResource(R.string.cf_compare_named, t.name)
                    Box(
                        contentAlignment = Alignment.Center,
                        modifier = Modifier
                            .align(Alignment.TopEnd)
                            .size(44.dp)
                            .clickable(role = Role.Button) { onCompare(t) }
                            .semantics { contentDescription = label }
                            .testTag("collect-compare-$i"),
                    ) {
                        Icon(Icons.Outlined.Info, null, tint = brand.moss, modifier = Modifier.size(22.dp))
                    }
                }
            }
            HorizontalDivider(color = brand.hairline, modifier = Modifier.padding(vertical = 4.dp))
            ChoiceRow(Icons.Filled.AddCircle, brand.moss, stringResource(R.string.cf_add_new), stringResource(R.string.cf_none_of_these), "collect-none-of-these", onNew)
            if (candidates.isNotEmpty()) {
                ChoiceRow(Icons.AutoMirrored.Filled.Help, brand.inkSoft, stringResource(R.string.cf_not_sure), stringResource(R.string.cf_work_it_out), "collect-not-sure", onNotSure)
            }
        }
    }
}

@Composable
private fun ChoiceRow(icon: androidx.compose.ui.graphics.vector.ImageVector, tint: androidx.compose.ui.graphics.Color, title: String, sub: String, tag: String, onClick: () -> Unit) {
    val brand = Brand.colors
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier.fillMaxWidth().heightIn(min = 44.dp).clickable(role = Role.Button, onClick = onClick).testTag(tag),
    ) {
        Icon(icon, null, tint = tint, modifier = Modifier.size(24.dp))
        Spacer(Modifier.width(10.dp))
        Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
            Text(title, fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = brand.ink)
            Text(sub, fontSize = 13.sp, color = brand.inkSoft)
        }
    }
}

/** ownRow: a tree you added, in the same card as ours: your photograph, its name, how far. */
@Composable
private fun OwnRow(s: OwnSighting, here: Here, mine: MyTrees, modifier: Modifier) {
    val brand = Brand.colors
    Row(
        verticalAlignment = Alignment.Top,
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(14.dp))
            .background(brand.surface)
            .then(modifier)
            .padding(12.dp),
    ) {
        OwnPhoto(s, mine, Modifier.size(56.dp).clip(RoundedCornerShape(11.dp)), maxSide = 168) {
            Box(Modifier.size(56.dp).clip(RoundedCornerShape(11.dp)).background(brand.surfaceMuted))
        }
        Spacer(Modifier.width(12.dp))
        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(3.dp)) {
            Text(OwnSighting.oneLine(s.name), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = brand.ink)
            val metres = (Geo.km(here.lat, here.lng, s.lat, s.lng) * 1000).toInt()
            Text(stringResource(R.string.cf_your_tree_at, CollectRules.distance(metres)), fontSize = 13.sp, color = brand.inkSoft)
        }
        Spacer(Modifier.width(32.dp))
    }
}

/** "Lime · 325 m south": the direction turns a distance into an instruction. */
@Composable
private fun candidateLabel(t: Tree, here: Here, located: Boolean, compass: Array<String>): String {
    if (!located) return t.commonName
    val metres = (Geo.km(here.lat, here.lng, t.lat, t.lng) * 1000).toInt()
    val d = CollectRules.compass(here.lat, here.lng, t.lat, t.lng)
    val dir = if (d >= 0) " " + compass[d] else ""
    return "${t.commonName} · ${CollectRules.distance(metres)}$dir"
}

@Composable
private fun CandidateRow(t: Tree, here: Here, located: Boolean, compass: Array<String>, modifier: Modifier) {
    val brand = Brand.colors
    Row(
        verticalAlignment = Alignment.Top,
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(14.dp))
            .background(brand.surface)
            .then(modifier)
            .padding(12.dp),
    ) {
        val p = t.photo
        Box(Modifier.size(56.dp).clip(RoundedCornerShape(11.dp)).background(brand.surfaceMuted), contentAlignment = Alignment.Center) {
            if (p != null) {
                RemoteImage(p.card, null, Modifier.fillMaxSize())
            } else {
                SpeciesMark(t.commonName, brand.moss, Modifier.fillMaxSize())
            }
        }
        Spacer(Modifier.width(12.dp))
        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(3.dp)) {
            Text(t.name, fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = brand.ink)
            Text(candidateLabel(t, here, located, compass), fontSize = 13.sp, color = brand.inkSoft)
            if (t.howToRecognise.isNotEmpty()) {
                Text(t.howToRecognise, fontSize = 13.sp, color = brand.ink, maxLines = 2, overflow = TextOverflow.Ellipsis)
            } else if (t.precision == Precision.APPROXIMATE) {
                Text(stringResource(R.string.cf_rough_row), fontSize = 13.sp, color = brand.inkSoft)
            }
        }
        Spacer(Modifier.width(32.dp))
    }
}

// MARK: - Is this the one

@Composable
private fun ColumnScope.CompareStep(t: Tree, here: Here, located: Boolean, onThis: () -> Unit, onBack: () -> Unit) {
    val brand = Brand.colors
    val compass = stringArrayResource(R.array.cf_compass)
    SheetTitleText(t.name)
    SheetMessageText(candidateLabel(t, here, located, compass))
    t.photo?.let { p ->
        RemoteImage(p.full, null, Modifier.padding(top = 18.dp).fillMaxWidth().height(220.dp).clip(RoundedCornerShape(14.dp)))
    }
    if (t.howToRecognise.isNotEmpty()) {
        Column(
            verticalArrangement = Arrangement.spacedBy(4.dp),
            modifier = Modifier
                .padding(top = 18.dp)
                .fillMaxWidth()
                .background(brand.surface, RoundedCornerShape(14.dp))
                .padding(14.dp),
        ) {
            Text(stringResource(R.string.cf_how_find), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 13.sp, color = brand.inkSoft)
            Text(t.howToRecognise, fontSize = 15.sp, color = brand.ink)
        }
    }
    if (CollectRules.isFar(here.lat, here.lng, t)) {
        val metres = (Geo.km(here.lat, here.lng, t.lat, t.lng) * 1000).toInt()
        SheetFootnoteText(stringResource(R.string.cf_pin_far, CollectRules.distance(metres)))
    }
    SheetButtonView(SheetButton(stringResource(R.string.cf_this_one), SheetKind.PRIMARY, null, onThis), Modifier.padding(top = 22.dp).testTag("collect-this-is-the-one"))
    SheetButtonView(SheetButton(stringResource(R.string.cf_back_to_list), SheetKind.QUIET, null, onBack), Modifier.padding(top = 12.dp))
    if (t.precision == Precision.APPROXIMATE) {
        SheetFootnoteText(
            stringResource(if (t.photo == null && t.howToRecognise.isEmpty()) R.string.cf_foot_nothing else R.string.cf_foot_rough),
        )
    }
}

// MARK: - Thank you, that helps

@Composable
private fun ColumnScope.UnsureStep(onDone: () -> Unit) {
    SheetIconTile(Icons.AutoMirrored.Filled.Send)
    Spacer(Modifier.height(16.dp))
    SheetTitleText(stringResource(R.string.cf_thanks))
    SheetMessageText(stringResource(R.string.cf_unsure_message))
    SheetButtonView(SheetButton(stringResource(R.string.cf_done), SheetKind.PRIMARY, null, onDone), Modifier.padding(top = 22.dp).testTag("collect-unsure-done"))
    SheetFootnoteText(stringResource(R.string.cf_unsure_foot))
}

// MARK: - You found one of ours

@Composable
private fun ColumnScope.TickedStep(t: Tree, newFind: Boolean, pinReported: Boolean, host: CollectHost, voted: Boolean, onDone: () -> Unit) {
    val brand = Brand.colors
    val scope = rememberCoroutineScope()
    val notes = remember { TreeNotes() }
    var noteText by remember { mutableStateOf("") }
    var sending by remember { mutableStateOf(false) }
    var failed by remember { mutableStateOf(false) }
    LaunchedEffect(t.id) { notes.load(t.id, host.account.fresh()?.accessToken) }

    SheetIconTile(if (newFind) Icons.Filled.Verified else Icons.Filled.Image)
    Spacer(Modifier.height(16.dp))
    SheetTitleText(stringResource(if (newFind) R.string.cf_you_found else R.string.cf_photo_added, t.name))
    val age = CollectRules.ageNeedsOld(t.age)?.let { needs -> if (needs) stringResource(R.string.cf_age_old, t.age!!.trim()) else t.age!!.trim() }
    SheetMessageText(listOfNotNull(t.commonName.ifEmpty { null }, age).joinToString(", "))
    if (pinReported) SheetFootnoteText(stringResource(R.string.cf_pin_thanks))

    val vote = if (voted) "up" else host.votes.vote(t.id)
    WorthTheTripAsk(t, vote, host, Modifier.padding(top = 20.dp))
    if (vote.isNotEmpty() && (notes.mine == null || sending)) {
        Column(Modifier.padding(top = 16.dp).fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Box(
                Modifier
                    .fillMaxWidth()
                    .heightIn(min = 96.dp)
                    .background(brand.surfaceMuted, RoundedCornerShape(14.dp))
                    .padding(horizontal = 15.dp, vertical = 16.dp),
            ) {
                BasicTextField(
                    value = noteText,
                    onValueChange = { noteText = it },
                    textStyle = TextStyle(fontSize = 16.sp, color = brand.ink),
                    cursorBrush = SolidColor(brand.moss),
                    modifier = Modifier.fillMaxWidth().testTag("collect-note-field"),
                )
                if (noteText.isEmpty()) {
                    Text(stringResource(R.string.cf_note_hint), fontSize = 16.sp, color = brand.inkSoft.copy(alpha = 0.7f))
                }
            }
            if (failed) Text(stringResource(R.string.cf_note_failed), fontSize = 13.sp, color = brand.inkSoft)
        }
    }
    val typed = noteText.trim()
    if (typed.isEmpty()) {
        SheetButtonView(SheetButton(stringResource(R.string.cf_done), SheetKind.PRIMARY, null, onDone), Modifier.padding(top = 22.dp).testTag("collect-done"))
    } else {
        SheetButtonView(
            SheetButton(stringResource(if (sending) R.string.cf_adding else R.string.cf_add_note), SheetKind.PRIMARY, null) {
                if (sending) return@SheetButton
                sending = true; failed = false
                scope.launch {
                    val token = host.account.fresh()?.accessToken
                    val ok = token != null && notes.save(t.id, typed.take(1000), token)
                    sending = false
                    if (ok) onDone() else failed = true
                }
            },
            Modifier.padding(top = 22.dp).testTag("collect-note-send"),
        )
    }
    if (t.url.isNotEmpty()) {
        SheetButtonView(
            SheetButton(stringResource(R.string.cf_share), SheetKind.SECONDARY, Icons.Outlined.Share) { host.share(t) },
            Modifier.padding(top = 12.dp).testTag("collect-share"),
        )
    }
}

/** WorthTheTripAsk (Kit/WorthIt.swift): the thumbs stay, the chosen one filled. */
@Composable
private fun WorthTheTripAsk(t: Tree, vote: String, host: CollectHost, modifier: Modifier) {
    val brand = Brand.colors
    val scope = rememberCoroutineScope()
    Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(10.dp), modifier = modifier.testTag("worth-the-trip")) {
        Text(stringResource(R.string.cf_worth), fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            for ((value, label) in listOf("up" to R.string.cf_worth_yes, "down" to R.string.cf_worth_no)) {
                val chosen = vote == value
                val text = stringResource(label)
                val icon = when {
                    value == "up" && chosen -> Icons.Filled.ThumbUp
                    value == "up" -> Icons.Outlined.ThumbUp
                    chosen -> Icons.Filled.ThumbDown
                    else -> Icons.Outlined.ThumbDown
                }
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier
                        .width(64.dp)
                        .height(44.dp)
                        .background(if (chosen) brand.moss.copy(alpha = 0.12f) else brand.surfaceMuted, CircleShape)
                        .clip(CircleShape)
                        .clickable(role = Role.Button) {
                            if (!host.signedIn) { host.needsSignIn { }; return@clickable }
                            if (chosen) return@clickable
                            val before = host.votes.vote(t.id)
                            host.votes.setVote(t.id, value)
                            host.counts.record(t.id, before, if (value == "up") "up" else "")
                            scope.launch {
                                Submission.feedback(t.city, Submission.treeField(t.id, t.name),
                                    if (value == "up") "worth it" else "not worth it", host.account.fresh()?.accessToken)
                            }
                        }
                        .semantics { contentDescription = text }
                        .testTag("worth-the-trip-$value"),
                ) {
                    Icon(icon, null, tint = if (chosen) brand.moss else brand.ink, modifier = Modifier.size(22.dp))
                }
            }
        }
    }
}
