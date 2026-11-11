// "YOU ARE 20 M FROM ..." (ios Screens/NearbyBanner.swift; audit 2026-11-10 row
// 24). A banner drops from the top, with a light tap of the phone, when you
// stand within 50 m of a tree with a confirmed pin that you have not collected,
// and goes after eight seconds or a tap on the cross. On that tree's own page a
// tap collects it; anywhere else it opens the page. Each tree is announced once
// a session, and the next one waits for your next steps (ContentView.nearKey).

package app.ancienttrees.ui

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.spring
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.feed.Here
import app.ancienttrees.feed.Precision
import app.ancienttrees.feed.Tree

/** A tree near enough to say so, and how far, rounded to five metres. */
data class Nearby(val tree: Tree, val meters: Int)

/** ContentView.checkNearby: the nearest unannounced, uncollected, confirmed tree within 50 m. */
fun nearbyTree(c: Catalogue, at: Here, collected: Set<String>, announced: Set<String>): Nearby? {
    val hit = c.nearest(at.lat, at.lng, limit = 50, withinKm = 0.05).firstOrNull { (t, _) ->
        t.precision == Precision.CONFIRMED && t.id !in collected && t.id !in announced
    } ?: return null
    val m = maxOf(5, Math.round(hit.second * 1000 / 5).toInt() * 5)
    return Nearby(hit.first, m)
}

/** The banner, dropping in from the top with .spring(duration: 0.35) and leaving the same way. */
@Composable
fun NearbyBanner(shown: Nearby?, onItsPage: Boolean, open: () -> Unit, dismiss: () -> Unit, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    var last by remember { mutableStateOf(shown) }
    if (shown != null) last = shown
    val springy = spring<Float>(dampingRatio = 1f, stiffness = 322f)
    val springyInt = spring<androidx.compose.ui.unit.IntOffset>(dampingRatio = 1f, stiffness = 322f)
    AnimatedVisibility(
        visible = shown != null,
        enter = slideInVertically(springyInt) { -it } + fadeIn(springy),
        exit = slideOutVertically(springyInt) { -it } + fadeOut(springy),
        modifier = modifier,
    ) {
        val n = last ?: return@AnimatedVisibility
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            modifier = Modifier
                .statusBarsPadding()
                .padding(horizontal = 10.dp)
                .padding(top = 6.dp)
                .fillMaxWidth()
                .shadow(16.dp, RoundedCornerShape(20.dp), ambientColor = Color.Black.copy(alpha = 0.2f), spotColor = Color.Black.copy(alpha = 0.2f))
                .background(brand.surface, RoundedCornerShape(20.dp))
                .padding(start = 10.dp, top = 8.dp, bottom = 8.dp)
                .testTag("nearby-banner"),
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                modifier = Modifier.weight(1f).clip(RoundedCornerShape(12.dp)).clickable(role = Role.Button, onClick = open).testTag("nearby-open"),
            ) {
                val photo = n.tree.photo?.card
                Box(Modifier.size(48.dp).clip(RoundedCornerShape(12.dp)).background(brand.surfaceMuted)) {
                    if (photo != null) RemoteImage(photo, null, Modifier.size(48.dp))
                }
                Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(1.dp)) {
                    Text(
                        stringResource(R.string.nearby_title, n.meters, n.tree.name),
                        fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = brand.ink, maxLines = 2,
                    )
                    Text(
                        stringResource(if (onItsPage) R.string.nearby_tap_collect else R.string.nearby_open_collect),
                        fontSize = 13.sp, color = brand.inkSoft,
                    )
                }
            }
            val label = stringResource(R.string.nearby_dismiss)
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier
                    .size(44.dp)
                    .clip(CircleShape)
                    .clickable(role = Role.Button, onClick = dismiss)
                    .semantics { contentDescription = label }
                    .testTag("nearby-dismiss"),
            ) {
                Icon(Sym.Close, null, tint = brand.inkSoft, modifier = Modifier.size(15.dp))
            }
        }
    }
}
