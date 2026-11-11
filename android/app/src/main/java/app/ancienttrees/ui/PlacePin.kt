// Moving a pin, on the map, with a finger. Ported from ios Screens/PlacePin.swift.
//
// Hidde, 2026-08-25: "the easiest would be if you open the map and let someone
// drop / move a pin." THE PIN DOES NOT MOVE, THE MAP DOES (Google Maps' "Move map
// to adjust", Airbnb's location step): PinPicker.kt holds the crosshair. It sends
// a correction through the channel that already exists: kind `correction`, the
// coordinate in `location_hint`, read by a run at rung 1.
//
// Full screen, because the job is to find one trunk on a map. The recentre arrow
// sits above the card, which moves the BUTTON and nothing else: an inset on the
// map would put the pin somewhere other than under the crosshair.
//
// ANDROID-FORCED: the system back gesture is Cancel.

package app.ancienttrees.ui

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.account.Account
import app.ancienttrees.account.Submission
import app.ancienttrees.feed.Geo
import app.ancienttrees.feed.Here
import app.ancienttrees.feed.Precision
import app.ancienttrees.feed.Tree
import kotlinx.coroutines.launch
import java.util.Locale

@Composable
fun PlacePin(
    tree: Tree,
    account: Account,
    signedIn: Boolean,
    onNeedsSignIn: (then: () -> Unit) -> Unit,
    onDismiss: () -> Unit,
) = PlainText {
    val brand = Brand.colors
    val scope = rememberCoroutineScope()
    val density = LocalDensity.current
    var here by remember { mutableStateOf(Here(tree.lat, tree.lng)) }
    var sending by remember { mutableStateOf(false) }
    var sent by remember { mutableStateOf(false) }
    var failed by remember { mutableStateOf(false) }
    var recentre by remember { mutableIntStateOf(0) }
    var barHeight by remember { mutableFloatStateOf(0f) }
    BackHandler(onBack = onDismiss)

    // How far they have moved it, so the button can say something true.
    val movedMetres = (Geo.km(tree.lat, tree.lng, here.lat, here.lng) * 1000).toInt()

    fun send() {
        sending = true
        failed = false
        scope.launch {
            // Six decimals is about 10 cm; a run pastes this straight into the tree's location.
            val hint = String.format(Locale.ROOT, "%.6f, %.6f", here.lat, here.lng)
            val why = "Moved the pin on the map, $movedMetres m from the published position. Our pin was " +
                (if (tree.precision == Precision.CONFIRMED) "marked confirmed" else "marked approximate") + "."
            val ok = Submission.correction(tree.city, tree.name, hint, why, tree.url, account.fresh()?.accessToken)
            sending = false
            if (ok) sent = true else failed = true
        }
    }

    Box(Modifier.fillMaxSize().background(brand.ground).testTag("place-pin")) {
        PinPicker(
            start = Here(tree.lat, tree.lng),
            trees = listOf(tree),
            spanMetres = 300.0,
            onMove = { here = it },
            recentre = recentre,
            modifier = Modifier.fillMaxSize(),
        )

        // The navigation bar: Cancel (Done once sent) and the title, over the map's top.
        // iOS 26's inline bar: 54, its controls in the top 44 (SweepFrames: Cancel
        // a 36 pill at {20, 66}, 4 under the safe area).
        Box(Modifier.fillMaxWidth().background(brand.ground).statusBarsPadding().height(54.dp).padding(bottom = 10.dp)) {
            Text(
                stringResource(if (sent) R.string.pp_done else R.string.pp_cancel),
                fontSize = 17.sp,
                color = brand.moss,
                modifier = Modifier
                    .align(Alignment.CenterStart)
                    .padding(start = 12.dp)
                    .background(brand.surface, RoundedCornerShape(50))
                    .border(1.dp, brand.hairline, RoundedCornerShape(50))
                    .clickable(role = Role.Button, onClick = onDismiss)
                    .padding(horizontal = 14.dp, vertical = 7.7.dp)
                    .testTag("place-pin-cancel"),
            )
            Text(
                stringResource(if (sent) R.string.pp_thanks else R.string.pp_title),
                fontSize = 17.sp,
                fontWeight = FontWeight.SemiBold,
                color = brand.ink,
                modifier = Modifier.align(Alignment.Center),
            )
        }

        // The recentre control rides above the card, never behind it.
        RecentreButton(
            onClick = { recentre++ },
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .navigationBarsPadding()
                .padding(end = 12.dp, bottom = with(density) { barHeight.toDp() } + 12.dp),
        )

        Column(
            verticalArrangement = Arrangement.spacedBy(10.dp),
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .navigationBarsPadding()
                .padding(horizontal = 16.dp)
                .padding(bottom = 16.dp)
                .onGloballyPositioned { barHeight = it.size.height + with(density) { 16.dp.toPx() } }
                .fillMaxWidth()
                .background(brand.surface, RoundedCornerShape(18.dp))
                .padding(16.dp),
        ) {
            if (sent) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Icon(Sym.VerifiedFill, null, tint = brand.ink, modifier = Modifier.size(18.dp))
                    Text(stringResource(R.string.pp_sent), fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
                }
            } else {
                Text(stringResource(R.string.pp_drag), fontSize = 15.sp, color = brand.ink)
                Text(
                    if (movedMetres < 5) stringResource(R.string.pp_zoom) else stringResource(R.string.pp_far, movedMetres),
                    fontSize = 12.sp,
                    color = brand.inkSoft,
                )
                val enabled = !sending && movedMetres >= 5
                Row(
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(48.dp)
                        .background(brand.moss.copy(alpha = if (enabled) 1f else 0.5f), RoundedCornerShape(50)) // disabled: half (iPhone A3B593 over white)
                        .clickable(enabled = enabled, role = Role.Button) {
                            // Signed out: the sign-in sheet, and nothing is sent until they press again.
                            if (!signedIn) onNeedsSignIn { } else send()
                        }
                        .testTag("place-pin-send"),
                ) {
                    if (sending) {
                        CircularProgressIndicator(color = Color.White, strokeWidth = 2.dp, modifier = Modifier.size(16.dp))
                        Box(Modifier.size(6.dp))
                    }
                    Text(
                        stringResource(if (sending) R.string.pp_sending else R.string.pp_send),
                        fontFamily = BrandFace,
                        fontWeight = FontWeight.Bold,
                        fontSize = 16.sp,
                        color = Color.White,
                    )
                }
                if (failed) Text(stringResource(R.string.pp_failed), fontSize = 12.sp, color = Color.Red)
                if (!signedIn) Text(stringResource(R.string.pp_account), fontSize = 11.sp, color = brand.inkSoft)
            }
        }
    }
}
