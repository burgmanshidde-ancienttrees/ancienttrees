// The sheet over the map, ported from ios Screens/BottomSheet.swift and
// MapWithSheet.swift, where every ruling behind these numbers is written down.
//
// An overlay in the screen rather than a presentation, so the tab bar stays
// visible under it (Google Maps). Stops: peek 168, card 400 (or the fitted
// height of one tapped tree), half 52 percent, full, and on the map tab's results
// list (build 42, Airbnb's way) the bar below them: the grip and the count, with
// the tab bar gone; there, full is the page under the search field, with no grip
// and no count. THE ARBITRATION is the
// iPhone's: below full height the sheet moves and the list does not scroll; at
// full the list scrolls; at full with the list at its top, dragging down moves
// the sheet again. A drag cancels the tap it started on (UIScrollView's rule,
// which Compose's scrollable gives for free). At peek the content is a preview:
// a tap raises the sheet to half and opens nothing. A drag starts after 18 points
// (DragGesture(minimumDistance: 18)); on release the flick is projected and the
// nearest stop taken (predictedEndTranslation, Designing Fluid Interfaces, WWDC18).
//
// ANDROID-FORCED: no system material blur, so the sheet is the ground at 96
// percent (data/android-parity.json "Glass behind floating bars").

package app.ancienttrees.ui

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.spring
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Icon
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.foundation.gestures.awaitEachGesture
import androidx.compose.foundation.gestures.awaitFirstDown
import androidx.compose.foundation.gestures.detectVerticalDragGestures
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBars
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.SideEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.nestedscroll.NestedScrollConnection
import androidx.compose.ui.input.nestedscroll.NestedScrollSource
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.input.pointer.PointerEventPass
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.Velocity
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import kotlin.math.abs

enum class SheetHeight { BAR, PEEK, CARD, HALF, FULL }

object SheetStops {
    /** Until the header has been measured (SheetHeight.bar's fallback). */
    val BAR = 80.dp
    val PEEK = 168.dp
    val CARD = 400.dp
    const val HALF = 0.52f

    /** A spring of 0.28 seconds, SwiftUI's .spring(duration: 0.28). */
    val motion = spring<Float>(dampingRatio = 1f, stiffness = 503f)
}

/**
 * The live state of one sheet, readable by whatever rides it: [points] is the
 * height drawn this frame (drag and spring included), [pageProgress] 0 at the
 * half stop and 1 at the top.
 */
class SheetState(initial: SheetHeight) {
    var height by mutableStateOf(initial)
    var points by mutableFloatStateOf(0f)
    var pageProgress by mutableFloatStateOf(0f)
    /** The full screen height in px, so riders can compute their own places. */
    var screen by mutableFloatStateOf(0f)
    /** The half stop in px, for the map's parallax. */
    var halfPx by mutableFloatStateOf(0f)
}

/**
 * [fullInset]: px from the top of the screen where the full sheet stops, for a
 * screen with a field fixed over the top (the map tab's search, Google Maps).
 * [cardFits]: the card stop is exactly as tall as the content (a tapped pin).
 * [barDepth]: the room kept at the end of the list for the floating tab bar.
 */
@Composable
fun MapSheet(
    state: SheetState,
    modifier: Modifier = Modifier,
    fullInset: Float = 0f,
    cardFits: Boolean = false,
    locked: Boolean = false,
    barDepth: Dp = TabBar.floatDepth,
    /**
     * BottomSheet's pageClose: on a root screen whose sheet reaches the top (no
     * fixed field, so [fullInset] 0), the sheet grows a status-bar strip as it
     * rises and the grabber turns into Polarsteps' chevron-down, which sends it
     * back to half. Null keeps the plain grabber (the map tab).
     */
    pageClose: (() -> Unit)? = null,
    /** BottomSheet's sheetResults (build 42): the bar stop, and full as the page under the field. */
    results: Boolean = false,
    header: @Composable () -> Unit,
    content: @Composable () -> Unit,
) {
    val density = LocalDensity.current
    val scope = rememberCoroutineScope()
    val top = WindowInsets.statusBars.getTop(density).toFloat()
    val bottom = WindowInsets.navigationBars.getBottom(density).toFloat()
    val scroll = rememberScrollState()
    var headerBottom by remember { mutableFloatStateOf(0f) }
    var contentHeight by remember { mutableFloatStateOf(0f) }
    var headerHeight by remember { mutableFloatStateOf(0f) }
    val anim = remember { Animatable(-1f) }
    val brand = Brand.colors
    // DragGesture(minimumDistance: 18): Compose's touch slop is already behind us
    // when a drag arrives, so what is left of the 18 is held back here.
    val slop = androidx.compose.ui.platform.LocalViewConfiguration.current.touchSlop
    val holdBack = with(density) { 18.dp.toPx() } - slop

    BoxWithConstraints(modifier.fillMaxSize()) {
        val total = constraints.maxHeight.toFloat()
        val visible = total - bottom - top
        val page = visible + top - (if (results) 0f else fullInset)
        val barPx = with(density) { (barDepth + 8.dp).toPx() }
        val halfPts = visible * SheetStops.HALF
        val isLocked = locked || cardFits
        // THE IPHONE'S STOPS STAND ON ITS 34 HOME INDICATOR, the floating tab bar on
        // the screen's edge (26 up on both). Over Android's 24 gesture bar the same
        // stop put the sheet's content 10 nearer the tab bar (map-bar's count, the
        // map's Highlights; 2026-11-12), so the fixed stops take the difference.
        // Three-button navigation is taller than 34: nothing is added there.
        val homeLift = with(density) { (34.dp.toPx() - bottom).coerceAtLeast(0f) }
        fun stop(s: SheetHeight): Float = when (s) {
            // The grip and the count: BottomSheet's own sum, 44 + the header + 6.
            SheetHeight.BAR -> with(density) {
                if (headerHeight > 0) 44.dp.toPx() + headerHeight + 6.dp.toPx() + homeLift else SheetStops.BAR.toPx() + homeLift
            }
            SheetHeight.PEEK -> with(density) { SheetStops.PEEK.toPx() } + homeLift
            // The fitted card counts from the floating bar's depth, which is measured
            // from the edge already (map-pin's place row within 1 of the iPhone's).
            SheetHeight.CARD ->
                if (cardFits && contentHeight > 0) minOf(headerBottom + contentHeight + barPx, halfPts)
                else with(density) { SheetStops.CARD.toPx() } + homeLift
            SheetHeight.HALF -> halfPts
            SheetHeight.FULL -> page
        }
        val target = stop(state.height)
        val latestTarget by rememberUpdatedState(target)
        // Spring to the stop whenever it changes (a release, a pin, a search).
        LaunchedEffect(target) {
            if (anim.value < 0) anim.snapTo(target) else anim.animateTo(target, SheetStops.motion)
        }
        val floor = minOf(with(density) { 90.dp.toPx() }, stop(SheetHeight.BAR))
        val h = (if (anim.value < 0) target else anim.value).coerceIn(floor, page)
        SideEffect {
            state.points = h
            state.screen = total
            state.halfPx = halfPts
            state.pageProgress = ((h - halfPts) / maxOf(page - halfPts, 1f)).coerceIn(0f, 1f)
        }

        var dragging by remember { mutableStateOf(false) }
        var held by remember { mutableFloatStateOf(0f) }

        fun settle(velocity: Float) {
            // No drag ever started (under the 18 points): nothing to settle.
            val wasDragging = dragging
            dragging = false
            held = 0f
            if (!wasDragging) return
            // Where the flick would end, not where the finger let go: SwiftUI's
            // predictedEndTranslation, a quarter of a second of the release speed.
            val now = anim.value
            val projected = now - velocity * 0.25f
            // Locked: only down, never up.
            val settled = if (isLocked && projected > now) latestTarget else projected
            val stops = SheetHeight.entries.filter {
                (it != SheetHeight.CARD || cardFits) && (it != SheetHeight.BAR || results)
            }
            val next = stops.minBy { abs(stop(it) - settled) }
            if (next == state.height) {
                scope.launch { anim.animateTo(latestTarget, SheetStops.motion) }
            } else {
                state.height = next
            }
        }

        fun dragBy(dy: Float) {
            var by = dy
            if (!dragging) {
                held += dy
                if (abs(held) < holdBack) return
                dragging = true
                by = held
                held = 0f
            }
            // Locked stops raising, never lowering.
            var next = anim.value - by
            if (isLocked) next = minOf(next, latestTarget)
            scope.launch { anim.snapTo(next.coerceIn(floor, page)) }
        }

        var handingOff by remember { mutableStateOf(false) }
        val connection = remember {
            object : NestedScrollConnection {
                override fun onPreScroll(available: Offset, source: NestedScrollSource): Offset {
                    if (source != NestedScrollSource.UserInput) return Offset.Zero
                    val dy = available.y
                    if (state.height != SheetHeight.FULL || handingOff) {
                        dragBy(-dy)
                        return Offset(0f, dy)
                    }
                    if (dy > 0 && scroll.value == 0) {
                        handingOff = true
                        dragBy(-dy)
                        return Offset(0f, dy)
                    }
                    return Offset.Zero
                }

                override suspend fun onPreFling(available: Velocity): Velocity {
                    if (state.height != SheetHeight.FULL || handingOff) {
                        handingOff = false
                        settle(available.y)
                        return available
                    }
                    return Velocity.Zero
                }

                override suspend fun onPostFling(consumed: Velocity, available: Velocity): Velocity {
                    handingOff = false
                    return Velocity.Zero
                }
            }
        }

        // The sheet becoming the page: the map tab's results list and My trees.
        val progress = if (results || (pageClose != null && fullInset == 0f)) state.pageProgress else 0f
        // Build 42: the grip and the count fold away with the sheet, frame by frame.
        val fold = if (results) state.pageProgress else 0f
        val barPts = stop(SheetHeight.BAR)
        val peekPts = stop(SheetHeight.PEEK)
        val listShown = if (results) ((h - barPts) / maxOf(peekPts - barPts, 1f)).coerceIn(0f, 1f) else 1f
        val lead = if (results) fullInset * fold else top * progress
        val corner = 16.dp * (1f - progress)
        Column(
            Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .height(with(density) { (h + bottom).toDp() })
                .shadow(10.dp, RoundedCornerShape(topStart = corner, topEnd = corner), ambientColor = Color.Black.copy(alpha = 0.12f * (1f - progress)), spotColor = Color.Black.copy(alpha = 0.12f * (1f - progress)))
                // The iPhone's regularMaterial over the map reads as a warm light
                // grey (#F4F4F2 measured off its shots, 2026-11-10), not white.
                .background(
                    // OPAQUE AT EVERY HEIGHT and the iPhone's light grey (#F5F6F5
                    // measured at full height, #F4F4F2 over the map, 2026-11-10):
                    // nothing shows through (Hidde: My trees see-through), and the
                    // white discs of the gear and Find people stand out as on iOS.
                    // Over the map the iPhone's material. The map's results list becomes the
                    // plain white page at full (build 42); My trees keeps the grey it measures
                    // at full height (#F5F6F5), where its white circles stand out.
                    androidx.compose.ui.graphics.lerp(
                        androidx.compose.ui.graphics.lerp(brand.ground, brand.surfaceMuted, 0.8f),
                        brand.ground,
                        if (results) progress else 0f,
                    ),
                    RoundedCornerShape(topStart = corner, topEnd = corner),
                )
                .nestedScroll(connection)
                // At peek every finger belongs to the sheet: a still tap raises
                // it to half and opens nothing underneath.
                .pointerInput(Unit) {
                    awaitEachGesture {
                        val down = awaitFirstDown(requireUnconsumed = false, pass = PointerEventPass.Initial)
                        if ((state.height != SheetHeight.PEEK && state.height != SheetHeight.BAR) || isLocked) return@awaitEachGesture
                        var moved = false
                        while (true) {
                            val e = awaitPointerEvent(PointerEventPass.Initial)
                            val c = e.changes.firstOrNull { it.id == down.id } ?: break
                            if ((c.position - down.position).getDistance() > viewConfiguration.touchSlop) moved = true
                            if (!c.pressed) {
                                if (!moved) {
                                    c.consume()
                                    state.height = SheetHeight.HALF
                                }
                                break
                            }
                        }
                    }
                },
        ) {
            // Room for the status bar, or on the results list for the field over the page.
            if (lead > 0f) Spacer(Modifier.height(with(density) { lead.toDp() }))
            // The grabber row: one fixed height, the capsule what you see.
            Box(
                Modifier
                    .fillMaxWidth()
                    .height(44.dp * (1f - fold))
                    .graphicsLayer { alpha = 1f - fold; clip = true }
                    .dragHandle(::dragBy, ::settle),
                contentAlignment = Alignment.TopCenter,
            ) {
                Box(
                    Modifier
                        .padding(top = 10.dp)
                        .size(width = 40.dp, height = 5.dp)
                        .graphicsLayer { alpha = 1f - progress }
                        .background(brand.ink.copy(alpha = 0.18f), RoundedCornerShape(50)),
                )
                if (pageClose != null && progress > 0f) {
                    val back = androidx.compose.ui.res.stringResource(app.ancienttrees.R.string.back_to_map)
                    Box(
                        Modifier
                            .align(Alignment.CenterStart)
                            .padding(start = 12.dp)
                            .size(44.dp)
                            .graphicsLayer { alpha = progress }
                            .clickable(enabled = progress > 0.9f, role = androidx.compose.ui.semantics.Role.Button) { pageClose() }
                            .semantics { contentDescription = back },
                        contentAlignment = Alignment.Center,
                    ) {
                        Box(Modifier.size(36.dp).background(brand.surfaceMuted, CircleShape), contentAlignment = Alignment.Center) {
                            Icon(Sym.KeyboardArrowDown, null, tint = brand.ink, modifier = Modifier.size(22.dp))
                        }
                    }
                }
            }
            Box(
                Modifier
                    .fillMaxWidth()
                    .dragHandle(::dragBy, ::settle)
                    .onSizeChanged {
                        headerBottom = with(density) { 44.dp.toPx() } + it.height
                        // Only while it is whole: the count folds away towards full.
                        if (fold == 0f && it.height > 0) headerHeight = it.height.toFloat()
                    },
            ) { header() }
            Box(
                Modifier
                    .fillMaxWidth()
                    .weight(1f)
                    .verticalScroll(scroll),
            ) {
                Column(Modifier.fillMaxWidth()) {
                    Box(Modifier.fillMaxWidth().graphicsLayer { alpha = listShown }.onSizeChanged { contentHeight = it.height.toFloat() }) { content() }
                    // Room at the end of the list, not a shorter list: content
                    // still passes under the floating bar (contentMargins).
                    Spacer(Modifier.height(barDepth + 8.dp))
                }
            }
        }
        // Back to the top of the list whenever the sheet leaves full height.
        LaunchedEffect(state.height) {
            if (state.height != SheetHeight.FULL && scroll.value != 0) scroll.scrollTo(0)
        }
    }
}

/** The grabber and the header always move the sheet, whatever the list is doing. */
private fun Modifier.dragHandle(drag: (Float) -> Unit, settle: (Float) -> Unit): Modifier =
    this.pointerInput(Unit) {
        val tracker = androidx.compose.ui.input.pointer.util.VelocityTracker()
        detectVerticalDragGestures(
            onDragStart = { tracker.resetTracking() },
            onDragEnd = { settle(tracker.calculateVelocity().y) },
            onDragCancel = { settle(0f) },
        ) { change, dy ->
            tracker.addPosition(change.uptimeMillis, change.position)
            change.consume()
            drag(dy)
        }
    }

/** How far the map moves up as the sheet rises past half (MapWithSheet.parallax). */
fun SheetState.parallax(): Float = -maxOf(0f, points - halfPx) / 2f

/**
 * WHERE THE RECENTRE CONTROL SITS (TreeMap.recentrePlacement): it rides the
 * sheet up to the tallest stop below full, then the sheet closes over it.
 * Returns the lift off the bottom of the visible map in px and the alpha.
 */
fun recentrePlacement(coverage: Float, visible: Float, cardPx: Float, minLift: Float, gap: Float, fade: Float): Pair<Float, Float> {
    val ceiling = maxOf(cardPx, visible * SheetStops.HALF)
    val ride = minOf(coverage, ceiling)
    return maxOf(ride + gap, minLift) to (1f - (coverage - ceiling) / fade).coerceIn(0f, 1f)
}
