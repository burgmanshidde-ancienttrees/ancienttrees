package app.ancienttrees

import android.Manifest
import android.annotation.SuppressLint
import android.location.LocationListener
import android.location.LocationManager
import android.app.Activity
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle

import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.LifecycleEventEffect
import app.ancienttrees.account.Account
import app.ancienttrees.account.Collector
import app.ancienttrees.account.Saves
import app.ancienttrees.account.SignIn
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.feed.CatalogueStore
import app.ancienttrees.feed.Geo
import app.ancienttrees.feed.Here
import app.ancienttrees.feed.Tree
import app.ancienttrees.ui.AccountSheet
import app.ancienttrees.ui.AncientTreesTheme
import app.ancienttrees.ui.CollectFailedSheet
import app.ancienttrees.ui.DiscoverActions
import app.ancienttrees.ui.DiscoverScreen
import app.ancienttrees.ui.HeroCover
import app.ancienttrees.ui.SearchHit
import app.ancienttrees.ui.SignInSheet
import app.ancienttrees.ui.LocalTreeMarks
import app.ancienttrees.ui.MapLaunch
import app.ancienttrees.ui.MapTab
import app.ancienttrees.ui.TabBar
import app.ancienttrees.ui.TreeMarks
import app.ancienttrees.ui.TreeDetail
import app.ancienttrees.ui.TreePageActions
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    /** A sign-in callback (ancienttrees://auth-callback) waiting to be read. */
    private var link by mutableStateOf<Uri?>(null)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        link = intent?.data
        launch = LaunchArgs.from(intent, applicationInfo)
        setContent {
            // A new set of launch arguments starts the screen afresh (debug builds only).
            androidx.compose.runtime.key(launch) {
                AncientTreesTheme { App(link, onLinkRead = { link = null }, launch = launch) }
            }
        }
    }

    /** The parity script's arguments; a start that lands on a running copy brings them here. */
    private var launch by mutableStateOf(LaunchArgs.NONE)

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        link = intent.data
        LaunchArgs.from(intent, applicationInfo).takeIf { it.args.isNotEmpty() }?.let { launch = it }
    }
}

/** Dam square: where the map opens with no fix, as on the iPhone. */
private val DAM_SQUARE = Here(52.3731, 4.8922)

private fun share(context: Context, t: Tree, from: String = "map_card", message: String? = null) {
    if (t.url.isEmpty()) return
    val link = "https://ancienttrees.app" + t.url + (if ('?' in t.url) "&" else "?") +
        "utm_source=share&utm_medium=app&utm_campaign=$from"
    val send = Intent(Intent.ACTION_SEND).apply {
        type = "text/plain"
        putExtra(Intent.EXTRA_SUBJECT, t.name)
        putExtra(Intent.EXTRA_TEXT, if (message != null) "$message $link" else link)
    }
    context.startActivity(Intent.createChooser(send, null))
}

/**
 * The phone's position while the app is open, from the system's own location
 * service (no Play services): network and GPS, the newer fix wins. Held in
 * memory only ("device" rules, data/cross-device.json).
 */
@SuppressLint("MissingPermission")
@Composable
private fun rememberFix(on: Boolean): Here? {
    val context = LocalContext.current
    var fix by remember { mutableStateOf<Here?>(null) }
    DisposableEffect(on) {
        val lm = context.getSystemService(Context.LOCATION_SERVICE) as? LocationManager
        if (!on || lm == null) return@DisposableEffect onDispose { }
        val listener = LocationListener { l -> fix = Here(l.latitude, l.longitude) }
        val providers = listOf(LocationManager.NETWORK_PROVIDER, LocationManager.GPS_PROVIDER).filter {
            runCatching { lm.isProviderEnabled(it) }.getOrDefault(false)
        }
        providers.mapNotNull { runCatching { lm.getLastKnownLocation(it) }.getOrNull() }
            .maxByOrNull { it.time }
            ?.let { fix = Here(it.latitude, it.longitude) }
        for (p in providers) {
            runCatching { lm.requestLocationUpdates(p, 5_000L, 20f, listener, android.os.Looper.getMainLooper()) }
        }
        onDispose { runCatching { lm.removeUpdates(listener) } }
    }
    return fix
}

private val LOCATION = arrayOf(Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION)

private fun locationGranted(context: Context) = LOCATION.any {
    ContextCompat.checkSelfPermission(context, it) == PackageManager.PERMISSION_GRANTED
}

@Composable
private fun App(link: Uri?, onLinkRead: () -> Unit, launch: LaunchArgs = LaunchArgs.NONE) {
    val context = LocalContext.current
    val store = remember { CatalogueStore(context.applicationContext) }
    var catalogue by remember { mutableStateOf<Catalogue?>(null) }
    var selected by remember { mutableStateOf<Tree?>(null) }
    var open by remember { mutableStateOf<Tree?>(null) }
    var here by remember { mutableStateOf<Here?>(launch.at?.let { Here(it.first, it.second) }) }
    val scope = rememberCoroutineScope()
    val account = remember { Account(context.applicationContext) }
    val saves = remember { Saves(account) }
    // My trees' server half (account/MyTrees.kt): your own finds, tips and profile, memory only.
    val myTrees = remember { app.ancienttrees.account.MyTrees(account) }
    // A tree of your own, open (ContentView .mine).
    var openMine by remember { mutableStateOf<String?>(null) }
    var myLane by remember { mutableStateOf(if (launch.laneWant) app.ancienttrees.ui.TreesLane.WANT else app.ancienttrees.ui.TreesLane.SEEN) }
    // The tree page's thumb and reports (WorthIt.swift): memory only.
    val votes = remember { app.ancienttrees.account.MyVotes() }
    val counts = remember { app.ancienttrees.account.VoteCounts() }
    // A place, species or tree a tree page sends to the map.
    var go by remember { mutableStateOf<Pair<Long, SearchHit>?>(null) }
    // What somebody was doing when they were asked to sign in, finished when
    // they land ("device" in data/cross-device.json: a pending intent; held in
    // memory only here).
    var pendingHeart by remember { mutableStateOf<Tree?>(null) }
    var pendingAfterSignIn by remember { mutableStateOf<(() -> Unit)?>(null) }
    var asking by remember { mutableStateOf(false) }
    var showAccount by remember { mutableStateOf(false) }

    val signedIn = account.state is SignIn.SignedIn
    // SIGN-IN AND PROFILE (ProfilePages.kt): settings, people, a person, the editor.
    val profiles = remember { app.ancienttrees.account.Profiles(launch.args) }
    val moderation = remember { app.ancienttrees.ui.Moderation() }
    val routes = remember { app.ancienttrees.ui.ProfileRoutes(launch.args) }
    var signInReason by remember { mutableStateOf<app.ancienttrees.ui.SignInReason?>(null) }
    var recovering by remember { mutableStateOf("-refused" in launch.args) }
    // The early-adopter tag on My trees: the server's created_at against the feed's cutoff
    // (EarlyAdopter.swift); -earlyadopter and -earlyadoptersheet draw it for the sweep.
    var earlyAdopter by remember { mutableStateOf("-earlyadopter" in launch.args || "-earlyadoptersheet" in launch.args) }
    // The sweep's -signed-in stand-in draws the signed-in screens; nothing is sent without a real session.
    val shownSignedIn = signedIn || launch.signedIn
    val myId = account.session?.userId ?: if (launch.signedIn) "00000000-0000-0000-0000-000000000000" else null
    val myEmail = (account.state as? SignIn.SignedIn)?.email ?: if (launch.signedIn) "test@ancienttrees.app" else null
    // COLLECT: sign in before the camera, never after the photograph (the
    // iPhone's rule, 2026-10-12). The photograph is proof of presence, so the
    // camera is the only way in; where the phone stood goes with it.
    var pendingCollect by remember { mutableStateOf<Tree?>(null) }
    var collecting by remember { mutableStateOf<Tree?>(null) }
    var collectFailed by remember { mutableStateOf(false) }
    // THE COLLECT FLOW (CollectSheet.kt), and a tree only you have being added.
    var collectStart by remember { mutableStateOf<app.ancienttrees.ui.CollectStart?>(null) }
    var draft by remember { mutableStateOf<Collector.Draft?>(null) }
    val shot = remember {
        java.io.File(context.cacheDir, "photos").apply { mkdirs() }.let { java.io.File(it, "collect.jpg") }
    }
    val shotUri = remember {
        androidx.core.content.FileProvider.getUriForFile(context, context.packageName + ".photos", shot)
    }
    // From a tree page's own collect sheet: the camera first, then the flow opens
    // at the photograph (TreeDetail.openFlowWithPhoto), the tree already known.
    val camera = rememberLauncherForActivityResult(ActivityResultContracts.TakePicture()) { ok ->
        val t = collecting
        collecting = null
        if (!ok || t == null) return@rememberLauncherForActivityResult
        scope.launch {
            val raw = runCatching { shot.readBytes() }.getOrNull()
            shot.delete()
            val jpeg = raw?.let { Collector.downsized(it) } ?: return@launch
            collectStart = app.ancienttrees.ui.CollectStart(about = t.name, knownTree = t.id, shotIn = jpeg)
        }
    }
    // The same from the library: the flow reads the photograph's own place and date.
    var choosingFor by remember { mutableStateOf<Tree?>(null) }
    val library = rememberLauncherForActivityResult(
        ActivityResultContracts.PickMultipleVisualMedia(1 + Collector.MAX_EXTRAS),
    ) { uris ->
        val t = choosingFor
        choosingFor = null
        if (uris.isEmpty() || t == null) return@rememberLauncherForActivityResult
        scope.launch {
            val p = Collector.read(context, uris.first()) ?: return@launch
            val more = uris.drop(1).mapNotNull { Collector.read(context, it)?.raw?.let { r -> Collector.downsized(r) } }
            collectStart = app.ancienttrees.ui.CollectStart(about = t.name, knownTree = t.id, pickedIn = p, pickedMore = more)
        }
    }
    fun collectFromLibrary(t: Tree) {
        if (!signedIn) {
            pendingAfterSignIn = { collectFromLibrary(t) }
            asking = true
            return
        }
        choosingFor = t
        library.launch(androidx.activity.result.PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
    }
    fun collect(t: Tree) {
        if (!signedIn) {
            pendingCollect = t
            asking = true
            return
        }
        collecting = t
        collectFailed = false
        runCatching { camera.launch(shotUri) }.onFailure { collecting = null }
    }

    fun heart(t: Tree) {
        if (signedIn) {
            scope.launch { saves.toggle(t.id) }
        } else {
            pendingHeart = t
            asking = true
        }
    }
    LaunchedEffect(Unit) { account.restore() }
    LaunchedEffect(link) {
        val uri = link ?: return@LaunchedEffect
        // Read first, cleared after: clearing changes this effect's key and
        // would cancel the sign-in halfway.
        account.handleCallback(uri)
        onLinkRead()
    }
    LaunchedEffect(signedIn) {
        if (!signedIn) {
            saves.forget()
            myTrees.forget()
            if (!launch.signedIn) profiles.forgetLocally()
            return@LaunchedEffect
        }
        scope.launch {
            val t = account.fresh()?.accessToken
            profiles.load(account.session?.userId, t)
            moderation.load(account.session?.userId, t)
            if (t != null) app.ancienttrees.account.EarlyAdopter.status(t)?.let { st ->
                earlyAdopter = st.hasBadge
                if (st.hasBadge && !st.seenSheet) routes.earlyAdopterSheet = true
            }
        }
        asking = false
        saves.load()
        myTrees.load()
        pendingAfterSignIn?.let { f ->
            pendingAfterSignIn = null
            f()
        }
        pendingHeart?.let { t ->
            pendingHeart = null
            if (t.id !in saves.hearts) saves.toggle(t.id)
        }
        pendingCollect?.let { t ->
            pendingCollect = null
            collecting = t
            runCatching { camera.launch(shotUri) }.onFailure { collecting = null }
        }
    }

    // LOCATION, ASKED ON THE FIRST OPEN with no screen of ours in front of it
    // (CONVENTIONS.md, "When the location question is asked", 2026-10-14). Android
    // itself stops asking after a second no, so nothing is remembered here.
    var granted by remember { mutableStateOf(locationGranted(context)) }
    var refused by remember { mutableStateOf(false) }
    val ask = rememberLauncherForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { result ->
        granted = result.values.any { it }
        val activity = context as? Activity
        refused = !granted && activity != null &&
            !ActivityCompat.shouldShowRequestPermissionRationale(activity, Manifest.permission.ACCESS_FINE_LOCATION)
    }
    // THE COVER (HeroCover.swift, ContentView.swift): 2.4 seconds or a tap, cold
    // start only; the location question comes half a second after it has gone.
    var showingCover by remember { mutableStateOf("-no-cover" !in launch.args) }
    LaunchedEffect(Unit) {
        if (showingCover) kotlinx.coroutines.delay(2400)
        showingCover = false
    }
    LaunchedEffect(showingCover) {
        if (showingCover) return@LaunchedEffect
        kotlinx.coroutines.delay(500)
        if (!granted && launch.at == null) ask.launch(LOCATION)
    }
    // Back from Settings with location turned on.
    LifecycleEventEffect(Lifecycle.Event.ON_RESUME) { granted = locationGranted(context) }

    // The parity script's launch arguments: the iPhone's own (LaunchArgs.kt).
    val fixedAt = launch.at
    LaunchedEffect(catalogue) {
        val c = catalogue ?: return@LaunchedEffect
        launch.openTree?.let { id -> c.tree(id)?.let { open = it } }
        if (launch.signIn) {
            // The sweep's -signin is the keep-a-tree sheet, as on the iPhone.
            signInReason = app.ancienttrees.ui.SignInReason.KeepTree("")
            asking = true
        }
        if (launch.collectOpen) collectStart = app.ancienttrees.ui.CollectStart()
        // The sweep's stand-ins for an account (debug builds only, nothing sent).
        if (launch.mineDemo) myTrees.seedDemo(launch.at?.first ?: DAM_SQUARE.lat, launch.at?.second ?: DAM_SQUARE.lng)
        if (launch.collectedIds.isNotEmpty() || launch.savedIds.isNotEmpty()) saves.seed(launch.collectedIds, launch.savedIds)
        launch.openMine?.let { openMine = it }
    }
    LaunchedEffect(Unit) {
        val started = android.os.SystemClock.elapsedRealtime()
        catalogue = store.load()
        android.util.Log.i("AncientTrees", "catalogue ${catalogue?.trees?.size} trees in ${android.os.SystemClock.elapsedRealtime() - started} ms")
        store.refresh(catalogue?.version)?.let { catalogue = it }
    }

    BackHandler(enabled = open != null) { open = null }
    BackHandler(enabled = openMine != null && open == null) { openMine = null }

    // WHERE YOU ARE: a live fix, kept up to date while the app is open, else
    // Dam square, the iPhone's first-launch-anywhere default (ContentView.origin).
    val fix = rememberFix(granted && fixedAt == null)
    LaunchedEffect(fix) { fix?.let { here = it } }
    val origin = here ?: DAM_SQUARE
    val located = here != null
    var raise by remember { mutableIntStateOf(0) }
    var searching by remember { mutableStateOf(false) }
    val trees = catalogue?.trees.orEmpty()
    // The tabs: Map, Discover (Home.swift), and My trees (Collect.swift).
    var tab by remember { mutableIntStateOf(if (launch.tab == 1 || launch.tab == 2) launch.tab!! else 0) }
    // Tapping Discover while on Discover scrolls back up (navigator.scrollToTop).
    var discoverTop by remember { mutableIntStateOf(0) }
    var discoverSearching by remember { mutableStateOf(false) }
    BackHandler(enabled = (tab == 1 || tab == 2) && open == null && openMine == null) { tab = 0 }

    Box(Modifier.fillMaxSize()) {
        CompositionLocalProvider(
            LocalTreeMarks provides TreeMarks(saves.hearts, saves.collected, onSave = { heart(it) }),
        ) {
            MapTab(
                catalogue = catalogue,
                origin = origin,
                located = located,
                granted = granted,
                locationRefused = refused,
                signedIn = signedIn,
                launch = MapLaunch(sheet = launch.sheet, select = launch.select, search = launch.search),
                showDot = granted && fixedAt == null,
                // After a no, the recovery sheet first (PermissionRecovery.swift), then Settings.
                onUseMyLocation = { if (refused) recovering = true else ask.launch(LOCATION) },
                onNeedsSignIn = { then ->
                    pendingAfterSignIn = then
                    asking = true
                },
                onOpen = { open = it },
                onCollect = { collect(it) },
                onAddTree = { open = null },
                onShare = { t -> share(context, t) },
                onSearching = { searching = it },
                raise = raise,
                go = go,
            )
        }
        val cat = catalogue
        if (tab == 1 && cat != null) {
            DiscoverScreen(
                catalogue = cat,
                origin = origin,
                located = located,
                signedIn = signedIn,
                email = (account.state as? SignIn.SignedIn)?.email,
                wantToVisit = saves.hearts,
                token = { if (signedIn) account.fresh()?.accessToken else null },
                refresh = { store.refresh(catalogue?.version)?.let { catalogue = it } },
                scrollToTop = discoverTop,
                discoverTo = launch.args.firstOrNull { it.startsWith("-discoverto=") }?.removePrefix("-discoverto="),
                act = DiscoverActions(
                    openTree = { open = it },
                    openPlace = { hit ->
                        tab = 0
                        go = System.nanoTime() to hit
                    },
                    openSpecies = { name ->
                        tab = 0
                        go = System.nanoTime() to SearchHit.Species(name)
                    },
                    openPerson = { id -> routes.openPerson(id) },
                    showMap = { tab = 0 },
                    openWantToVisit = {
                        myLane = app.ancienttrees.ui.TreesLane.WANT
                        tab = 2
                    },
                    addTree = { collectStart = app.ancienttrees.ui.CollectStart() },
                    signIn = { then ->
                        pendingAfterSignIn = then
                        asking = true
                    },
                    searching = { discoverSearching = it },
                ),
            )
        }
        // MY TREES (Collect.swift). The gear opens Settings, your face the profile
        // editor, the person-with-a-plus Find people, the counts the follow lists.
        if (tab == 2 && cat != null) {
            val mtSignedIn = signedIn || launch.signedIn
            CompositionLocalProvider(
                LocalTreeMarks provides TreeMarks(saves.hearts, saves.collected, onSave = { heart(it) }),
                app.ancienttrees.ui.LocalMyHeader provides app.ancienttrees.ui.MyHeader(
                    profiles = profiles,
                    earlyAdopter = earlyAdopter,
                    openPlace = { slug, name ->
                        val t = cat.trees(slug).firstOrNull()
                        tab = 0
                        go = System.nanoTime() to SearchHit.City(slug, name, t?.lat ?: 0.0, t?.lng ?: 0.0)
                    },
                ),
            ) {
                androidx.compose.runtime.key(myLane) {
                    app.ancienttrees.ui.MyTreesScreen(
                        catalogue = cat,
                        origin = origin,
                        located = located,
                        granted = granted,
                        signedIn = mtSignedIn,
                        email = (account.state as? SignIn.SignedIn)?.email,
                        saves = saves,
                        mine = myTrees,
                        initialSheet = if (launch.sheetFull) app.ancienttrees.ui.SheetHeight.FULL else app.ancienttrees.ui.SheetHeight.HALF,
                        initialLane = myLane,
                        onUseMyLocation = { if (refused) recovering = true else ask.launch(LOCATION) },
                        actions = app.ancienttrees.ui.MyTreesActions(
                            openTree = { open = it },
                            openMine = { openMine = it },
                            signIn = { asking = true },
                            settings = { routes.openSettings() },
                            editProfile = { if (mtSignedIn) routes.editProfile = true else asking = true },
                            findPeople = { routes.openPeople(app.ancienttrees.ui.PeopleSource.SEARCH) },
                            followList = { f -> routes.openPeople(if (f) app.ancienttrees.ui.PeopleSource.FOLLOWERS else app.ancienttrees.ui.PeopleSource.FOLLOWING) },
                            showMap = { tab = 0 },
                        ),
                    )
                }
            }
        }
        openMine?.let { id ->
            if (cat != null) {
                app.ancienttrees.ui.OwnTree(
                    id = id,
                    mine = myTrees,
                    catalogue = cat,
                    onBack = { openMine = null },
                    onCity = { slug, name ->
                        val t = cat.trees(slug).firstOrNull()
                        openMine = null
                        tab = 0
                        go = System.nanoTime() to SearchHit.City(slug, name, t?.lat ?: 0.0, t?.lng ?: 0.0)
                    },
                )
            }
        }
        if (routes.showing || routes.editProfile || routes.earlyAdopterSheet) {
            app.ancienttrees.ui.ProfilePages(
                routes = routes,
                settings = app.ancienttrees.ui.SettingsHost(
                    account = account,
                    profiles = profiles,
                    signedIn = shownSignedIn,
                    email = myEmail,
                    locationAllowed = granted,
                    locationRefused = refused,
                    askLocation = { ask.launch(LOCATION) },
                    signIn = { asking = true },
                    editProfile = { routes.editProfile = true },
                    openPrivacy = { routes.stack.add(app.ancienttrees.ui.ProfilePage.Privacy) },
                    signedOut = { routes.clear() },
                ),
                people = app.ancienttrees.ui.PeopleHost(
                    account = account,
                    profiles = profiles,
                    moderation = moderation,
                    catalogue = catalogue,
                    yourTrees = (saves.hearts + saves.collected).toList(),
                    userId = myId,
                    args = launch.args,
                    signIn = { r -> signInReason = r; asking = true },
                    editName = { routes.editProfile = true },
                    openPerson = { routes.openPerson(it) },
                    openTree = { open = it },
                ),
                onEarlyAdopterSeen = {
                    scope.launch { account.fresh()?.accessToken?.let { app.ancienttrees.account.EarlyAdopter.markSeen(it) } }
                },
            )
        }
        open?.let { tree ->
            CompositionLocalProvider(
                LocalTreeMarks provides TreeMarks(saves.hearts, saves.collected, onSave = { heart(it) }),
            ) {
                TreeDetail(
                    tree = tree,
                    account = account,
                    signedIn = signedIn,
                    fix = if (located) here else null,
                    hearted = tree.id in saves.hearts,
                    collected = tree.id in saves.collected,
                    votes = votes,
                    counts = counts,
                    openPhotoAtStart = launch.photo,
                    actions = TreePageActions(
                        onBack = { open = null },
                        onHeart = { heart(tree) },
                        onCollect = { collect(tree) },
                        onShare = { share(context, tree, "tree", "${tree.name}, ${tree.city}.") },
                        onGo = { hit ->
                            open = null
                            tab = 0
                            go = System.nanoTime() to hit
                        },
                        onNeedsSignIn = { then ->
                            pendingAfterSignIn = then
                            asking = true
                        },
                        onCollectFromLibrary = { collectFromLibrary(tree) },
                        onAddPhoto = {
                            if (signedIn) {
                                collectStart = app.ancienttrees.ui.CollectStart(about = tree.name, addsPhoto = true, knownTree = tree.id)
                            } else {
                                pendingAfterSignIn = { collectStart = app.ancienttrees.ui.CollectStart(about = tree.name, addsPhoto = true, knownTree = tree.id) }
                                asking = true
                            }
                        },
                    ),
                )
            }
        }
        if (recovering) {
            app.ancienttrees.ui.PermissionRecovery(app.ancienttrees.ui.Permission.LOCATION, onDismiss = { recovering = false })
        }
        if (open == null && openMine == null && !searching && !discoverSearching && draft == null && !routes.showing) {
            TabBar(
                selected = tab,
                select = { i ->
                    when (i) {
                        0 -> tab = 0
                        1 -> if (tab == 1) discoverTop++ else tab = 1
                        2 -> tab = 2
                        else -> Unit
                    }
                },
                collect = { collectStart = app.ancienttrees.ui.CollectStart() },
                modifier = Modifier.align(Alignment.BottomCenter),
            )
        }
        if (asking && !signedIn) {
            SignInSheet(
                account,
                reason = signInReason ?: (pendingHeart ?: pendingCollect)?.name?.let { app.ancienttrees.ui.SignInReason.KeepTree(it) }
                    ?: app.ancienttrees.ui.SignInReason.General,
                onDismiss = { asking = false; signInReason = null; pendingHeart = null; pendingCollect = null; pendingAfterSignIn = null },
            )
        }
        androidx.compose.animation.AnimatedVisibility(
            visible = showingCover,
            enter = androidx.compose.animation.EnterTransition.None,
            exit = androidx.compose.animation.fadeOut(androidx.compose.animation.core.tween(400)),
        ) { HeroCover { showingCover = false } }
        collectStart?.let { start ->
            if (cat != null) {
                app.ancienttrees.ui.CollectSheet(
                    catalogue = cat,
                    origin = origin,
                    located = located,
                    host = app.ancienttrees.ui.CollectHost(
                        account = account,
                        signedIn = signedIn || launch.signedIn,
                        collected = saves.collected,
                        votes = votes,
                        counts = counts,
                        needsSignIn = { then -> pendingAfterSignIn = then; asking = true },
                        askLocation = { if (!refused) ask.launch(LOCATION) },
                        send = { job -> scope.launch { if (!job()) collectFailed = true else myTrees.load(force = true) } },
                        ticked = { saves.noteCollected(it) },
                        openDraft = { draft = it },
                        share = { t -> share(context, t, "collect", "${t.name}, ${t.city}.") },
                    ),
                    start = start,
                    launch = launch.collect,
                    onDismiss = { collectStart = null },
                )
            }
        }
        draft?.let { d ->
            if (cat != null) {
                app.ancienttrees.ui.DraftTree(
                    draft = d,
                    catalogue = cat,
                    onSave = { saved, city ->
                        draft = null
                        scope.launch { if (!Collector.saveDraft(account, saved, city)) collectFailed = true else myTrees.load(force = true) }
                    },
                    onDiscard = { draft = null },
                )
            }
        }
        if (collectFailed) CollectFailedSheet(onDismiss = { collectFailed = false })
        if (showAccount && signedIn) {
            val byId = remember(trees) { trees.associateBy { it.id } }
            AccountSheet(
                account,
                hearted = saves.hearts.mapNotNull { byId[it] }.sortedBy { it.name },
                collected = saves.collected.mapNotNull { byId[it] }.sortedBy { it.name },
                onOpen = { showAccount = false; open = it },
                onDismiss = { showAccount = false },
            )
        }
    }
}
