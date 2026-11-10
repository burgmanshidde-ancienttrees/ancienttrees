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
import android.provider.Settings
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
import app.ancienttrees.ui.CollectedSheet
import app.ancienttrees.ui.DiscoverActions
import app.ancienttrees.ui.DiscoverScreen
import app.ancienttrees.ui.HeroCover
import app.ancienttrees.ui.SearchHit
import app.ancienttrees.ui.openProfileOnWeb
import app.ancienttrees.ui.SignInSheet
import app.ancienttrees.ui.LocalTreeMarks
import app.ancienttrees.ui.MapLaunch
import app.ancienttrees.ui.MapTab
import app.ancienttrees.ui.TabBar
import app.ancienttrees.ui.TreeMarks
import app.ancienttrees.ui.TreeScreen
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

private fun share(context: Context, t: Tree) {
    if (t.url.isEmpty()) return
    val link = "https://ancienttrees.app" + t.url + (if ('?' in t.url) "&" else "?") +
        "utm_source=share&utm_medium=app&utm_campaign=map_card"
    val send = Intent(Intent.ACTION_SEND).apply {
        type = "text/plain"
        putExtra(Intent.EXTRA_SUBJECT, t.name)
        putExtra(Intent.EXTRA_TEXT, link)
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

private fun openAppSettings(context: Context) {
    context.startActivity(
        Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.fromParts("package", context.packageName, null)),
    )
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
    // What somebody was doing when they were asked to sign in, finished when
    // they land ("device" in data/cross-device.json: a pending intent; held in
    // memory only here).
    var pendingHeart by remember { mutableStateOf<Tree?>(null) }
    var pendingAfterSignIn by remember { mutableStateOf<(() -> Unit)?>(null) }
    var asking by remember { mutableStateOf(false) }
    var showAccount by remember { mutableStateOf(false) }

    val signedIn = account.state is SignIn.SignedIn
    // COLLECT: sign in before the camera, never after the photograph (the
    // iPhone's rule, 2026-10-12). The photograph is proof of presence, so the
    // camera is the only way in; where the phone stood goes with it.
    var pendingCollect by remember { mutableStateOf<Tree?>(null) }
    var collecting by remember { mutableStateOf<Tree?>(null) }
    var collectedNow by remember { mutableStateOf<Tree?>(null) }
    var collectFailed by remember { mutableStateOf(false) }
    val shot = remember {
        java.io.File(context.cacheDir, "photos").apply { mkdirs() }.let { java.io.File(it, "collect.jpg") }
    }
    val shotUri = remember {
        androidx.core.content.FileProvider.getUriForFile(context, context.packageName + ".photos", shot)
    }
    val camera = rememberLauncherForActivityResult(ActivityResultContracts.TakePicture()) { ok ->
        val t = collecting
        val where = here
        if (!ok || t == null || where == null) {
            collecting = null
            return@rememberLauncherForActivityResult
        }
        scope.launch {
            val raw = runCatching { shot.readBytes() }.getOrNull()
            shot.delete()
            val jpeg = raw?.let { Collector.downsized(it) }
            val landed = jpeg != null && Collector.collect(account, t.id, t.name, jpeg, where.lat, where.lng)
            collecting = null
            if (landed) {
                saves.noteCollected(t.id)
                collectedNow = t
            } else {
                collectFailed = true
            }
        }
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
            return@LaunchedEffect
        }
        asking = false
        saves.load()
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
        if (launch.signIn) asking = true
    }
    LaunchedEffect(Unit) {
        val started = android.os.SystemClock.elapsedRealtime()
        catalogue = store.load()
        android.util.Log.i("AncientTrees", "catalogue ${catalogue?.trees?.size} trees in ${android.os.SystemClock.elapsedRealtime() - started} ms")
        store.refresh(catalogue?.version)?.let { catalogue = it }
    }

    BackHandler(enabled = open != null) { open = null }

    // WHERE YOU ARE: a live fix, kept up to date while the app is open, else
    // Dam square, the iPhone's first-launch-anywhere default (ContentView.origin).
    val fix = rememberFix(granted && fixedAt == null)
    LaunchedEffect(fix) { fix?.let { here = it } }
    val origin = here ?: DAM_SQUARE
    val located = here != null
    var raise by remember { mutableIntStateOf(0) }
    var searching by remember { mutableStateOf(false) }
    val trees = catalogue?.trees.orEmpty()
    // The tabs: Map, Discover (Home.swift), and My trees, which opens your lanes
    // until Collect.swift is ported (data/android-parity.json "collection-tab").
    var tab by remember { mutableIntStateOf(if (launch.tab == 1) 1 else 0) }
    // Tapping Discover while on Discover scrolls back up (navigator.scrollToTop).
    var discoverTop by remember { mutableIntStateOf(0) }
    var discoverSearching by remember { mutableStateOf(false) }
    // A place picked on Discover lands on the map (PlaceLink, navigator.searchOnMap).
    var mapPlace by remember { mutableStateOf<Pair<Long, SearchHit>?>(null) }
    BackHandler(enabled = tab == 1 && open == null) { tab = 0 }
    fun nearestTree() {
        val t = trees.minByOrNull { Geo.km(origin.lat, origin.lng, it.lat, it.lng) }
        if (t != null) open = t
    }

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
                onUseMyLocation = { if (refused) openAppSettings(context) else ask.launch(LOCATION) },
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
                place = mapPlace,
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
                        mapPlace = System.nanoTime() to hit
                    },
                    openSpecies = { name ->
                        tab = 0
                        mapPlace = System.nanoTime() to SearchHit.Species(name)
                    },
                    openPerson = { id -> openProfileOnWeb(context, id) },
                    showMap = { tab = 0 },
                    openWantToVisit = { if (signedIn) showAccount = true else asking = true },
                    addTree = { nearestTree() },
                    signIn = { then ->
                        pendingAfterSignIn = then
                        asking = true
                    },
                    searching = { discoverSearching = it },
                ),
            )
        }
        open?.let { tree ->
            val near = here?.let { Geo.km(it.lat, it.lng, tree.lat, tree.lng) <= Collector.REACH_KM } ?: false
            TreeScreen(
                tree,
                hearted = tree.id in saves.hearts,
                onHeart = { heart(tree) },
                onBack = { open = null },
                canCollect = near,
                collected = tree.id in saves.collected,
                collecting = collecting?.id == tree.id,
                onCollect = { collect(tree) },
            )
        }
        if (open == null && !searching && !discoverSearching) {
            TabBar(
                selected = tab,
                select = { i ->
                    when (i) {
                        0 -> tab = 0
                        1 -> if (tab == 1) discoverTop++ else tab = 1
                        2 -> if (signedIn) showAccount = true else asking = true
                        else -> Unit
                    }
                },
                collect = { nearestTree() },
                modifier = Modifier.align(Alignment.BottomCenter),
            )
        }
        if (asking && !signedIn) {
            SignInSheet(
                account,
                treeName = (pendingHeart ?: pendingCollect)?.name,
                onDismiss = { asking = false; pendingHeart = null; pendingCollect = null; pendingAfterSignIn = null },
            )
        }
        androidx.compose.animation.AnimatedVisibility(
            visible = showingCover,
            enter = androidx.compose.animation.EnterTransition.None,
            exit = androidx.compose.animation.fadeOut(androidx.compose.animation.core.tween(400)),
        ) { HeroCover { showingCover = false } }
        collectedNow?.let { t -> CollectedSheet(t.name, onDismiss = { collectedNow = null }) }
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
