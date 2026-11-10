// A map you drag under a fixed pin, to say where something is. Ported from ios
// Screens/PinPicker.swift. Convention: Google Maps ("Move map to adjust") and
// Airbnb's location step: the MAP moves under a pin that never moves, so the
// thumb never covers what it aims at. Our trees nearby are drawn for context.

package app.ancienttrees.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Place
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.unit.dp
import app.ancienttrees.feed.Here
import app.ancienttrees.feed.Tree
import app.ancienttrees.feed.ViewBox
import app.ancienttrees.map.MoveRequest
import app.ancienttrees.map.TreeMapView

/** A box [metres] across, centred on [lat],[lng]. */
fun boxAround(lat: Double, lng: Double, metres: Double): ViewBox {
    val dLat = metres / 2 / 111_320.0
    val dLng = dLat / kotlin.math.cos(Math.toRadians(lat)).coerceAtLeast(0.01)
    return ViewBox(lat - dLat, lng - dLng, lat + dLat, lng + dLng)
}

@Composable
fun PinPicker(
    start: Here,
    trees: List<Tree>,
    spanMetres: Double,
    onMove: (Here) -> Unit,
    modifier: Modifier = Modifier,
    /** Presses of a locate control drawn over it (PlacePin's arrow): back to the person. */
    recentre: Int = 0,
) {
    val latest by rememberUpdatedState(onMove)
    val opening = remember { MoveRequest(1L, boxAround(start.lat, start.lng, spanMetres)) }
    Box(modifier) {
        TreeMapView(
            trees = trees,
            selected = null,
            onSelect = { },
            origin = start,
            located = true,
            dot = false,
            recentre = recentre,
            onView = { b -> latest(Here((b.south + b.north) / 2, (b.west + b.east) / 2)) },
            moveTo = opening,
            modifier = Modifier.matchParentSize(),
        )
        // Dead centre, hanging from its point like a map pin: the tip marks the spot.
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier.align(Alignment.Center).offset(y = (-20).dp),
        ) {
            Icon(Icons.Filled.Place, null, tint = Brand.colors.moss, modifier = Modifier.size(38.dp))
            Box(Modifier.offset(y = (-4).dp).size(6.dp).shadow(2.dp, CircleShape).background(Brand.colors.moss, CircleShape))
        }
    }
}
