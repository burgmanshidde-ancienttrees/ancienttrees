package app.ancienttrees

import android.Manifest
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
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.material3.BottomSheetScaffold
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.rememberBottomSheetScaffoldState
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
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.LifecycleEventEffect
import app.ancienttrees.account.Account
import app.ancienttrees.account.Saves
import app.ancienttrees.account.SignIn
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.account.Account
import app.ancienttrees.account.Saves
import app.ancienttrees.account.SignIn
import app.ancienttrees.feed.CatalogueStore
import app.ancienttrees.feed.Geo
import app.ancienttrees.feed.Here
import app.ancienttrees.feed.Nearby
import app.ancienttrees.feed.Tree
import app.ancienttrees.feed.ViewBox
import app.ancienttrees.map.TreeMapView
import app.ancienttrees.ui.AccountButton
import app.ancienttrees.ui.AccountSheet
import app.ancienttrees.ui.AncientTreesTheme
import app.ancienttrees.ui.SignInSheet
import app.ancienttrees.ui.LocationOffChip
import app.ancienttrees.ui.MyLocationButton
import app.ancienttrees.ui.TreeCard
import app.ancienttrees.ui.TreeList
import app.ancienttrees.ui.TreeScreen
import kotlinx.coroutines.launch
import java.util.Locale

class MainActivity : ComponentActivity() {
    /** A sign-in callback (ancienttrees://auth-callback) waiting to be read. */
    private var link by mutableStateOf<Uri?>(null)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        link = intent?.data
        setContent { AncientTreesTheme { App(link, onLinkRead = { link = null }) } }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        link = intent.data
    }
}

private val PEEK = 96.dp

private val LOCATION = arrayOf(Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION)

private fun locationGranted(context: Context) = LOCATION.any {
    ContextCompat.checkSelfPermission(context, it) == PackageManager.PERMISSION_GRANTED
}

private fun openAppSettings(context: Context) {
    context.startActivity(
        Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.fromParts("package", context.packageName, null)),
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun App(link: Uri?, onLinkRead: () -> Unit) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val account = remember { Account(context.applicationContext) }
    val saves = remember { Saves(account) }
    // What somebody was doing when they were asked to sign in, finished when
    // they land ("device" in data/cross-device.json: a pending intent; held in
    // memory only here).
    var pendingHeart by remember { mutableStateOf<Tree?>(null) }
    var asking by remember { mutableStateOf(false) }
    var showAccount by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) { account.restore() }
    LaunchedEffect(link) {
        val uri = link ?: return@LaunchedEffect
        // Read first, cleared after: clearing changes this effect's key and
        // would cancel the sign-in halfway.
        account.handleCallback(uri)
        onLinkRead()
    }
    val signedIn = account.state is SignIn.SignedIn
    LaunchedEffect(signedIn) {
        if (!signedIn) {
            saves.forget()
            return@LaunchedEffect
        }
        asking = false
        saves.load()
        pendingHeart?.let { t ->
            pendingHeart = null
            if (t.id !in saves.hearts) saves.toggle(t.id)
        }
    }
    fun heart(t: Tree) {
        if (signedIn) {
            scope.launch { saves.toggle(t.id) }
        } else {
            pendingHeart = t
            asking = true
        }
    }
    val store = remember { CatalogueStore(context.applicationContext) }
    var catalogue by remember { mutableStateOf<Catalogue?>(null) }
    var selected by remember { mutableStateOf<Tree?>(null) }
    var open by remember { mutableStateOf<Tree?>(null) }
    var box by remember { mutableStateOf<ViewBox?>(null) }
    var here by remember { mutableStateOf<Here?>(null) }
    var recentre by remember { mutableIntStateOf(0) }
    val miles = remember { Geo.milesFor(Locale.getDefault().country) }

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
    LaunchedEffect(Unit) { if (!granted) ask.launch(LOCATION) }
    // Back from Settings with location turned on.
    LifecycleEventEffect(Lifecycle.Event.ON_RESUME) { granted = locationGranted(context) }

    LaunchedEffect(Unit) {
        catalogue = store.load()
        store.refresh(catalogue?.version)?.let { catalogue = it }
    }

    BackHandler(enabled = open != null || selected != null) {
        if (open != null) open = null else selected = null
    }

    val trees = catalogue?.trees.orEmpty()
    val inView = remember(trees, box, here) { Nearby.inView(trees, box, here) }
    val sheet = rememberBottomSheetScaffoldState()

    Box(Modifier.fillMaxSize()) {
        BottomSheetScaffold(
            scaffoldState = sheet,
            sheetPeekHeight = PEEK,
            sheetContent = {
                TreeList(inView, here, miles, onOpen = { open = it })
            },
        ) { inner ->
            Box(Modifier.fillMaxSize()) {
                TreeMapView(
                    trees = trees,
                    selected = selected,
                    onSelect = { selected = it },
                    locationOn = granted,
                    recentre = recentre,
                    onView = { b, h ->
                        box = b
                        if (h != null) here = h
                    },
                    modifier = Modifier.fillMaxSize(),
                )
                if (!granted) {
                    LocationOffChip(
                        refused = refused,
                        onClick = { if (refused) openAppSettings(context) else ask.launch(LOCATION) },
                        modifier = Modifier.align(Alignment.TopCenter).statusBarsPadding().padding(top = 8.dp),
                    )
                }
                // Above the sheet's lowest stop; the sheet covers them as it rises
                // (CONVENTIONS.md, "A my-location control over a bottom sheet").
                Box(Modifier.fillMaxSize().padding(inner).padding(bottom = PEEK)) {
                    if (selected == null) {
                        MyLocationButton(
                            onClick = {
                                if (granted) recentre++ else if (refused) openAppSettings(context) else ask.launch(LOCATION)
                            },
                            modifier = Modifier.align(Alignment.BottomEnd).padding(12.dp),
                        )
                    }
                    selected?.let { tree ->
                        TreeCard(
                            tree = tree,
                            distance = here?.let { Geo.short(Geo.km(it.lat, it.lng, tree.lat, tree.lng), miles) },
                            onOpen = { open = tree },
                            onClose = { selected = null },
                            modifier = Modifier.align(Alignment.BottomCenter).padding(12.dp),
                        )
                    }
                }
            }
        }
        open?.let { tree ->
            TreeScreen(tree, hearted = tree.id in saves.hearts, onHeart = { heart(tree) }, onBack = { open = null })
        }
        if (open == null) {
            AccountButton(
                signedIn = signedIn,
                onClick = { if (signedIn) showAccount = true else asking = true },
                modifier = Modifier.align(Alignment.TopEnd).statusBarsPadding().padding(12.dp),
            )
        }
        if (asking && !signedIn) {
            SignInSheet(account, treeName = pendingHeart?.name, onDismiss = { asking = false; pendingHeart = null })
        }
        if (showAccount && signedIn) {
            AccountSheet(account, saved = saves.hearts.size, onDismiss = { showAccount = false })
        }
    }
}
