package app.ancienttrees

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.feed.CatalogueStore
import app.ancienttrees.feed.Tree
import app.ancienttrees.map.TreeMapView
import app.ancienttrees.ui.AncientTreesTheme
import app.ancienttrees.ui.TreeCard
import app.ancienttrees.ui.TreeScreen

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent { AncientTreesTheme { App() } }
    }
}

@Composable
private fun App() {
    val context = LocalContext.current
    val store = remember { CatalogueStore(context.applicationContext) }
    var catalogue by remember { mutableStateOf<Catalogue?>(null) }
    var selected by remember { mutableStateOf<Tree?>(null) }
    var open by remember { mutableStateOf<Tree?>(null) }

    LaunchedEffect(Unit) {
        catalogue = store.load()
        store.refresh(catalogue?.version)?.let { catalogue = it }
    }

    BackHandler(enabled = open != null || selected != null) {
        if (open != null) open = null else selected = null
    }

    Box(Modifier.fillMaxSize()) {
        // Always composed, so coming back from a tree finds the map where it was.
        TreeMapView(
            trees = catalogue?.trees.orEmpty(),
            selected = selected,
            onSelect = { selected = it },
            modifier = Modifier.fillMaxSize(),
        )
        selected?.let { tree ->
            TreeCard(
                tree = tree,
                onOpen = { open = tree },
                onClose = { selected = null },
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .navigationBarsPadding()
                    .padding(12.dp),
            )
        }
        open?.let { tree -> TreeScreen(tree, onBack = { open = null }) }
    }
}
