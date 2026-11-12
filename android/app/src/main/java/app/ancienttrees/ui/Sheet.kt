@file:OptIn(androidx.compose.ui.ExperimentalComposeUiApi::class)

// EVERY SHEET LEAVES THE WAY IT CAME (audit 2026-11-10, row 4): on the iPhone a
// sheet whose state goes away slides down (BrandSheet.swift:189 dismiss()); on
// Android taking the sheet out of the composition removed it in one frame,
// scrim and all. So a sheet's own buttons close through LocalSheetClose, which
// slides it down first and then does what the button does.
//
// And the iPhone's handle (Style.swift:318-330, BrandSheetHandle): 36 by 5,
// cream, 12 down, on every sheet, never the system's grey one (row 11).

package app.ancienttrees.ui

import androidx.compose.ui.graphics.TransformOrigin
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.semantics.testTagsAsResourceId
import androidx.compose.ui.semantics.semantics
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.navigationBars
import androidx.compose.foundation.layout.tappableElement
import androidx.compose.foundation.layout.only
import androidx.compose.foundation.layout.WindowInsetsSides
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.SheetState
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.remember
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.runtime.withFrameNanos
import androidx.compose.ui.Modifier
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.gestures.awaitFirstDown
import androidx.compose.foundation.gestures.awaitEachGesture
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.layout
import androidx.compose.ui.layout.onPlaced
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch

/** Slide the sheet down, then run what closes it. */
fun interface SheetClose {
    operator fun invoke(then: () -> Unit)
}

/** Outside a sheet the action simply runs. */
val LocalSheetClose = staticCompositionLocalOf { SheetClose { it() } }

@OptIn(ExperimentalMaterial3Api::class)
fun sheetClose(scope: CoroutineScope, state: SheetState, wanted: () -> Boolean) = SheetClose { then ->
    scope.launch {
        state.hide()
        then()
        // Still here and still wanted two frames later: the button changed
        // something inside the sheet rather than closing it, so it comes back up.
        withFrameNanos { }
        withFrameNanos { }
        if (wanted() && !state.isVisible) state.show()
    }
}

/** Whether the sheet's owner still wants it, and how to let it go (see [Lingering]). */
class SheetPresence(val visible: Boolean, val gone: () -> Unit)

val LocalSheetPresence = staticCompositionLocalOf<SheetPresence?> { null }

/**
 * Keeps a sheet on screen after [value] goes away, so it can slide down
 * first: the iPhone's .sheet(item:) going nil. The sheet inside is drawn with
 * the last value it had.
 */
@Composable
fun <T : Any> Lingering(value: T?, content: @Composable (T) -> Unit) {
    var held by remember { mutableStateOf(value) }
    if (value != null && value != held) held = value
    val h = held ?: return
    CompositionLocalProvider(LocalSheetPresence provides SheetPresence(value != null) { held = null }) {
        content(h)
    }
}

/** [Lingering] for a plain condition. */
@Composable
fun LingeringIf(show: Boolean, content: @Composable () -> Unit) =
    Lingering(if (show) Unit else null) { content() }

/**
 * BrandSheetHandle: 36 by 5, cream, 12 from the top. It keeps the 48 points
 * Material's handle took, so no sheet's content moves (each was measured
 * against the iPhone with that room above it).
 */
@Composable
fun BrandSheetHandle(modifier: Modifier = Modifier) {
    Box(
        modifier
            .padding(top = 12.dp, bottom = 31.dp)
            .size(36.dp, 5.dp)
            .background(Brand.colors.creamDark, RoundedCornerShape(50))
            // Seen by scripts/android_spacing.py, which measures every sheet's X and
            // first element from it as the iPhone's 'Sheet Grabber' (a sheet is its
            // own window; AppSheet exports its tags, as MainActivity does the app's).
            .testTag("sheet-grabber"),
    )
}

/**
 * The app's one modal sheet: Material's, with the iPhone's handle, and with
 * [LocalSheetClose] for everything inside that closes it.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppSheet(
    onDismissRequest: () -> Unit,
    modifier: Modifier = Modifier,
    sheetState: SheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true),
    containerColor: Color = Brand.colors.ground,
    dragHandle: (@Composable () -> Unit)? = { BrandSheetHandle() },
    properties: androidx.compose.material3.ModalBottomSheetProperties = androidx.compose.material3.ModalBottomSheetProperties(),
    /**
     * iOS 26's fitted sheet: a card inset from the edges with every corner round
     * (row 13). Measured off the iPhone's sign-in sheet (out/parity/ios/signin.png,
     * 1206 px = 402 pt): 8 in from each side, 10 above the bottom, corners 28 at
     * the top and 36 at the bottom. A full-height sheet stays edge to edge, as
     * the .large detent does.
     */
    floating: Boolean = true,
    /**
     * THE SECOND STOP, iOS's .large (BrandSheet.swift:193, SignIn.swift:148): the
     * sheet opens at its fitted height and a drag up grows it to the full height,
     * rubber-banding past it; release settles on the nearer stop. A drag down from
     * the fitted height is still Material's own, which dismisses. Audit row 12.
     */
    grows: Boolean = false,
    content: @Composable ColumnScope.() -> Unit,
) {
    val scope = rememberCoroutineScope()
    val growth = remember { SheetGrowth() }
    val density = androidx.compose.ui.platform.LocalDensity.current
    // How far up the sheet has grown, 0 at the fitted height and 1 at full.
    val frac = if (grows) growth.fraction else 0f
    val presence = LocalSheetPresence.current
    val wanted by rememberUpdatedState(presence?.visible ?: true)
    val close = remember(sheetState) { sheetClose(scope, sheetState) { wanted } }
    // Its owner let it go: down first, then out of the composition.
    var hidByOwner by remember { mutableStateOf(false) }
    LaunchedEffect(presence?.visible) {
        if (presence != null && !presence.visible) {
            hidByOwner = true
            try {
                sheetState.hide()
            } catch (e: kotlinx.coroutines.CancellationException) {
                throw e
            } catch (_: Exception) {
                // Refused to move: it goes anyway.
            }
            presence.gone()
        } else if (hidByOwner) {
            // Wanted again while it was going: back up.
            hidByOwner = false
            sheetState.show()
        }
    }
    // The gesture bar's height (navigation bar minus anything tappable in it): the
    // floating card stands over it as iOS 26's stands over the home indicator.
    val insetDensity = androidx.compose.ui.platform.LocalDensity.current
    val gestureOnly = (WindowInsets.navigationBars.getBottom(insetDensity) -
        WindowInsets.tappableElement.getBottom(insetDensity)).coerceAtLeast(0)
    // The full height's top: under the status bar with 10 of air, as .large stops.
    // The card is drawn down by the gesture bar, so it may grow that much taller.
    growth.topClear = WindowInsets.statusBars.getTop(density) + with(density) { 10.dp.toPx() } - gestureOnly
    ModalBottomSheet(
        onDismissRequest = onDismissRequest,
        // SCALED, NOT NARROWED (visual review 2026-11-11): iOS 26 lays the fitted
        // sheet out at the screen's full width and draws it smaller, so it stands
        // 8 in from each side with everything in it about 4 percent smaller: the
        // review-ask tile measures 53 for its 56, the sign-in title 258 for the
        // 271 Core Text sets at 26 pt, while titles outside a sheet match to 1 dp.
        // Laid out narrower, as before, the same words wrapped elsewhere and the
        // type read 4 to 5 percent big. 10 above the bottom, as measured.
        // A sheet is its own window, out of reach of MainActivity's
        // testTagsAsResourceId: set here, every sheet's tags reach UI Automator.
        // Set only on the handle, it exported nothing on the sign-in sheet, whose
        // content never set it, and the measurer found no grabber (2026-11-12).
        // Growing to .large the floating card goes edge to edge, as iOS 26's does.
        modifier = if (floating) modifier.semantics { testTagsAsResourceId = true }.graphicsLayer {
            val s = (size.width - 16.dp.toPx() * (1f - frac)) / size.width
            scaleX = s
            scaleY = s
            transformOrigin = TransformOrigin(0.5f, 1f)
            // 10 above the screen's edge, as measured on the iPhone, over the gesture
            // bar: the sheet's window stops on the navigation bar, so it comes down
            // by the bar's height (its foot stood 31.6 up, the last button 58 against
            // the iPhone's 35; android_spacing.py, 2026-11-12).
            translationY = -10.dp.toPx() * (1f - frac) + gestureOnly
        } else modifier.semantics { testTagsAsResourceId = true },
        shape = if (floating) RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp, bottomStart = 36.dp * (1f - frac), bottomEnd = 36.dp * (1f - frac))
        else RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp),
        sheetState = sheetState,
        containerColor = containerColor,
        dragHandle = dragHandle,
        properties = properties,
        // The iPhone's dimming is light: white under it reads #D6D6DA, Material's 32
        // percent black reads #A8A8A8 (review 2026-11-11, row 124).
        scrimColor = Color.Black.copy(alpha = 0.16f),
        // iOS 26's floating sheet ignores the bottom safe area (BrandSheetFit,
        // ignoresSafeArea(.container, edges: .bottom)): its last button stands its
        // own 28 above the card's foot. Material padded the content by the
        // navigation bar on top of that, and with the card scaled about its foot
        // the button stood 80 to 142 above the screen's edge against the iPhone's
        // 35 (android_spacing.py). Only what can be tapped is kept clear: three-
        // button navigation, never the gesture bar.
        contentWindowInsets = {
            if (floating) WindowInsets.tappableElement.only(WindowInsetsSides.Bottom)
            else androidx.compose.material3.BottomSheetDefaults.windowInsets
        },
    ) {
        // A sheet opened from inside this one has its own owner.
        CompositionLocalProvider(LocalSheetClose provides close, LocalSheetPresence provides null) {
            if (grows) {
                androidx.compose.foundation.layout.Column(growth.modifier(scope)) { content() }
            } else {
                content()
            }
        }
    }
}

/**
 * The fitted sheet's growth toward the full height (AppSheet `grows`): the
 * content is laid out at its own height and the sheet reports that plus [extra],
 * so Material's sheet rises with it; the drag is read before the content's own
 * gestures, and only once it has travelled past the touch slop, so taps pass.
 */
class SheetGrowth {
    private val extra = androidx.compose.animation.core.Animatable(0f)
    private var room by androidx.compose.runtime.mutableFloatStateOf(1f)
    private var placed: androidx.compose.ui.layout.LayoutCoordinates? = null
    /** Kept clear above the full height: the status bar and 10 of air, as .large stops. */
    var topClear by androidx.compose.runtime.mutableFloatStateOf(0f)

    /** 0 at the fitted height, 1 at the full height. */
    val fraction: Float get() = (extra.value / room).coerceIn(0f, 1f)

    /** UIKit's rubber band past the full height: a third of the finger's travel, tapering. */
    private fun band(raw: Float): Float {
        if (raw <= room) return raw
        val over = raw - room
        return room + (1f - 1f / (over * 0.55f / room + 1f)) * room * 0.18f
    }

    fun modifier(scope: kotlinx.coroutines.CoroutineScope): Modifier = Modifier
        .layout { measurable, constraints ->
            // Bounded: the content may scroll, and a scroll refuses an endless height.
            val p = measurable.measure(constraints.copy(minHeight = 0))
            // The full height: the window under the status bar and 10 of air, as .large.
            val full = (constraints.maxHeight - topClear.toInt()).coerceAtLeast(p.height)
            room = (full - p.height).toFloat().coerceAtLeast(1f)
            val h = (p.height + band(extra.value).coerceAtLeast(0f)).toInt().coerceAtMost(constraints.maxHeight - topClear.toInt())
            layout(p.width, h) { p.place(0, 0) }
        }
        .onPlaced { placed = it }
        .pointerInput(Unit) {
            val slop = viewConfiguration.touchSlop
            awaitEachGesture {
                val down = awaitFirstDown(requireUnconsumed = false, pass = androidx.compose.ui.input.pointer.PointerEventPass.Initial)
                val tracker = androidx.compose.ui.input.pointer.util.VelocityTracker()
                // The finger in the window, not on the content: the content this
                // listens on moves up as the sheet grows, so its own positions read an
                // upward flick as a downward one (2026-11-12, v +2931 for a flick up).
                fun windowY(at: androidx.compose.ui.geometry.Offset): Float =
                    placed?.takeIf { it.isAttached }?.localToWindow(at)?.y ?: at.y
                val startY = windowY(down.position)
                var lastY = startY
                tracker.addPosition(down.uptimeMillis, androidx.compose.ui.geometry.Offset(0f, startY))
                var travelled = 0f
                var engaged = false
                // Where the finger has the sheet, kept here: each move's snap is launched,
                // and reading extra back before the last one landed lost travel (a drag
                // of 600 down from the full height moved it 375).
                var at = extra.value
                while (true) {
                    val e = awaitPointerEvent(androidx.compose.ui.input.pointer.PointerEventPass.Initial)
                    val c = e.changes.firstOrNull { it.id == down.id } ?: break
                    val y = windowY(c.position)
                    val dy = y - lastY
                    lastY = y
                    travelled += dy
                    // The lift's own sample counts, or a short flick reads as slow.
                    tracker.addPosition(c.uptimeMillis, androidx.compose.ui.geometry.Offset(0f, y))
                    if (!engaged) {
                        // Lifted before the slop: a tap, the content's.
                        if (!c.pressed || kotlin.math.abs(travelled) < slop) {
                            if (!c.pressed) break else continue
                        }
                        // Up, or down while grown: the growth's. Down at the fitted height:
                        // Material's own drag, which dismisses.
                        engaged = travelled < 0 || at > 0f
                        if (!engaged) break
                        // From where the finger went down, as a pan's translation counts.
                        at = (at - travelled).coerceAtLeast(0f)
                    } else {
                        // Every move, the lift's included: its step is part of the travel.
                        at = (at - dy).coerceAtLeast(0f)
                    }
                    c.consume()
                    val next = at
                    scope.launch { extra.snapTo(next) }
                    if (!c.pressed) break
                }
                if (engaged) {
                    val v = tracker.calculateVelocity().y
                    // Where the flick would end (predictedEndTranslation), then the nearer stop.
                    val projected = at - v * 0.25f
                    val target = if (projected > room / 2f) room else 0f
                    scope.launch {
                        extra.animateTo(target, androidx.compose.animation.core.spring(dampingRatio = 1f, stiffness = 503f), -v)
                    }
                }
            }
        }
}
