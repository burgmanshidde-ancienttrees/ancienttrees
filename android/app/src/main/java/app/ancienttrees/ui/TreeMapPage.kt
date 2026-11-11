// ONE TREE ON A WHOLE MAP, without leaving the page you were reading: the twin
// of ios Screens/TreeMapPage.swift (Route.treeMap; audit 2026-11-10 row 14).
//
// Hidde, 2026-08-26: expand only the map of where the tree stands, "in een
// eigen subpagina met een backbutton terug naar de detailpagina". Expanding used
// to switch to the Map tab and drop the tree page; a pushed page keeps the
// trail, and back is the way out. The neighbours within 1.5 km show too; this
// tree stays the selected pin, and a neighbour's tap opens its own page on the
// same stack.

package app.ancienttrees.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.clickable
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import app.ancienttrees.R
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.feed.Here
import app.ancienttrees.feed.Tree
import app.ancienttrees.map.MoveRequest
import app.ancienttrees.map.TreeMapView

@Composable
fun TreeMapPage(tree: Tree, catalogue: Catalogue, onBack: () -> Unit, onOpen: (Tree) -> Unit) {
    val brand = Brand.colors
    val context = LocalContext.current
    val take = stringResource(R.string.take_me_there)
    // This tree and whatever else of ours stands within a walk of it.
    val nearby = remember(tree.id, catalogue) {
        listOf(tree) + catalogue.nearest(tree.lat, tree.lng, limit = 12, withinKm = 1.5)
            .map { it.first }.filter { it.id != tree.id }
    }
    val opening = remember(tree.id) { MoveRequest(1L, boxAround(tree.lat, tree.lng, 600.0)) }
    Column(Modifier.fillMaxSize().background(brand.ground).testTag("tree-map-page")) {
        PushedBar(tree.name, onBack) {
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier
                    .size(44.dp)
                    .clip(CircleShape)
                    .clickable(role = Role.Button) { walkTo(context, tree.lat, tree.lng) }
                    .semantics { contentDescription = take },
            ) {
                Icon(Sym.TurnUpRight, null, tint = brand.moss, modifier = Modifier.size(22.dp))
            }
        }
        TreeMapView(
            trees = nearby,
            selected = tree,
            // A neighbour opens its own page, pushed on this same stack.
            onSelect = { t -> if (t != null && t.id != tree.id) onOpen(t) },
            origin = Here(tree.lat, tree.lng),
            located = true,
            dot = false,
            recentre = 0,
            onView = { },
            moveTo = opening,
            modifier = Modifier.fillMaxWidth().weight(1f),
        )
    }
}
