// A NAVIGATION STACK PER TAB, as the iPhone's (ContentView.swift stack(),
// mapPath / explorePath / collectPath; audit 2026-11-10 rows 1 to 3).
//
// Each tab keeps its own history: open a tree from Discover, switch to the map,
// come back, and the tree is still there with Discover under it. A page slides
// in from the right while the one under it moves a third of the way left, as
// UINavigationController pushes; back slides it out again. The system back
// gesture drags the page with the finger (predictive back, Android 14 and
// later) and lets go of it when the gesture is cancelled, as the iPhone's edge
// swipe does.
//
// A tab that is not on screen stays composed, so its scroll positions and its
// pages are where they were (TabView keeps its tabs alive), but it is not
// placed, so it draws nothing and takes no touches, and its back handlers
// listen to a dispatcher nobody calls.

package app.ancienttrees.ui

import androidx.activity.BackEventCompat
import androidx.activity.OnBackPressedDispatcher
import androidx.activity.OnBackPressedDispatcherOwner
import androidx.activity.compose.LocalOnBackPressedDispatcherOwner
import androidx.activity.compose.PredictiveBackHandler
import androidx.compose.animation.core.Animatable
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.key
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshotFlow
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.layout
import androidx.compose.ui.semantics.clearAndSetSemantics
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.lifecycle.LifecycleOwner
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.launch

/** Where a tap goes (Route.swift), as a value. Trees by id, looked up at drawing time. */
sealed class Page {
    data class TreePage(val id: String) : Page()
    /** One of yours (Route.mine). */
    data class Mine(val id: String) : Page()
    /** Somebody else's tree from its unlisted link (SharedTreeView.swift), read only. */
    data class Shared(val id: String) : Page()
    data class Species(val name: String) : Page()
    /** The map of one tree, pushed on the stack you are on (Route.treeMap). */
    data class TreeMap(val id: String) : Page()
    data class Discover(val page: DiscoverPage) : Page()
    data object Settings : Page()
    data object Privacy : Page()
    data class People(val source: PeopleSource) : Page()
    data class Person(val userId: String) : Page()

    val isProfile: Boolean get() = this is Settings || this is Privacy || this is People || this is Person
}

/** One push. Its own identity, so the same tree pushed twice is two pages. */
class Entry internal constructor(val page: Page, val key: Long)

/** The three stacks and which tab is showing (ContentView.tab, mapPath, explorePath, collectPath). */
class Nav(initialTab: Int) {
    var tab by mutableIntStateOf(initialTab)
    val stacks = List(3) { mutableStateListOf<Entry>() }
    private var next = 0L

    val stack: List<Entry> get() = stacks[tab]
    val top: Page? get() = stacks[tab].lastOrNull()?.page

    fun push(page: Page, onTab: Int = tab) {
        stacks[onTab].add(Entry(page, next++))
    }

    fun pop() {
        val s = stacks[tab]
        if (s.isNotEmpty()) s.removeAt(s.lastIndex)
    }

    /** Back to the tab's root (clearPath). */
    fun clear(onTab: Int) = stacks[onTab].clear()

    /** Take every page matching [what] off every stack (signing out leaves no profile page open). */
    fun removeAll(what: (Page) -> Boolean) = stacks.forEach { s -> s.removeAll { what(it.page) } }
}

/** Laid out but not placed: composed, drawing nothing, taking no touches. */
fun Modifier.placedIf(placed: Boolean): Modifier = layout { m, c ->
    val p = m.measure(c)
    layout(p.width, p.height) { if (placed) p.place(0, 0) }
}

/** A back dispatcher no gesture reaches, for a tab that is off screen. */
@Composable
fun BackOnlyWhen(active: Boolean, content: @Composable () -> Unit) {
    val lifecycle = LocalLifecycleOwner.current
    val deaf = remember(lifecycle) {
        object : OnBackPressedDispatcherOwner, LifecycleOwner by lifecycle {
            override val onBackPressedDispatcher = OnBackPressedDispatcher()
        }
    }
    if (active) content()
    else CompositionLocalProvider(LocalOnBackPressedDispatcherOwner provides deaf, content = content)
}

private class Shown(val entry: Entry, start: Float) {
    /** 0 off to the right, 1 in place. */
    val progress = Animatable(start)
    var leaving by mutableStateOf(false)
}

/**
 * One tab: its root, and the pages pushed over it. [active] is whether this
 * tab is the one on screen; [rootPlaced] keeps the root drawn even when it is
 * not (the map stays under everything, as it does on the iPhone).
 */
@Composable
fun PageStack(
    entries: List<Entry>,
    active: Boolean,
    onPop: () -> Unit,
    rootPlaced: Boolean = active,
    root: @Composable () -> Unit,
    page: @Composable (Page) -> Unit,
) {
    val shown = remember { mutableStateListOf<Shown>().apply { entries.forEach { add(Shown(it, 1f)) } } }
    val scope = rememberCoroutineScope()

    // Follow the stack: a new entry slides in, a gone one slides out and then leaves.
    LaunchedEffect(Unit) {
        snapshotFlow { entries.toList() }.collect { now ->
            val keys = now.map { it.key }.toSet()
            for (s in shown.toList()) {
                if (s.entry.key !in keys && !s.leaving) {
                    s.leaving = true
                    scope.launch {
                        s.progress.animateTo(0f, Motion.push())
                        shown.remove(s)
                    }
                }
            }
            val have = shown.map { it.entry.key }.toSet()
            for (e in now) {
                if (e.key !in have) {
                    val s = Shown(e, 0f)
                    shown.add(s)
                    scope.launch { s.progress.animateTo(1f, Motion.push()) }
                }
            }
        }
    }

    // THE BACK GESTURE: the top page follows it, and comes back if it is cancelled.
    PredictiveBackHandler(enabled = active && entries.isNotEmpty()) { events: Flow<BackEventCompat> ->
        val top = shown.lastOrNull { !it.leaving }
        try {
            events.collect { e -> top?.progress?.snapTo(1f - e.progress) }
            onPop()
        } catch (e: CancellationException) {
            scope.launch { top?.progress?.animateTo(1f, Motion.push()) }
            throw e
        }
    }

    BoxWithConstraints(Modifier.fillMaxSize()) {
        val w = constraints.maxWidth.toFloat()
        val moving = shown.any { it.progress.isRunning }
        // What lies over layer i: the progress of the page above it, if any.
        fun above(i: Int): Float = shown.getOrNull(i + 1)?.progress?.value ?: 0f
        // A layer a page has settled over is out of the accessibility tree, as
        // UIKit's navigation stack takes it out of VoiceOver's: TalkBack read the
        // My trees page under Settings, and ButtonWalk tapped its controls
        // through Settings and found them dead (2026-11-11).
        fun covered(i: Int): Boolean = !moving && above(i) >= 1f

        Box(
            Modifier
                .fillMaxSize()
                .placedIf(rootPlaced || active)
                // Off screen is out of the accessibility tree too: TalkBack never reads a hidden tab.
                // Drawn under another tab (the map stays under everything) is still off
                // screen to TalkBack: only the tab in front is read.
                .then(if (active && !covered(-1)) Modifier else Modifier.clearAndSetSemantics { })
                .graphicsLayer { translationX = -0.3f * w * above(-1) },
        ) {
            root()
            UnderDim { above(-1) }
        }
        shown.forEachIndexed { i, s ->
            key(s.entry.key) {
                Box(
                    Modifier
                        .fillMaxSize()
                        .placedIf(active)
                        .then(if (active && !covered(i)) Modifier else Modifier.clearAndSetSemantics { })
                        .graphicsLayer {
                            translationX = w * (1f - s.progress.value) - 0.3f * w * above(i)
                        }
                        // A page on its way out takes no taps.
                        .then(if (s.leaving) Modifier.pointerInput(Unit) { awaitPointerEventScope { while (true) awaitPointerEvent().changes.forEach { it.consume() } } } else Modifier),
                ) {
                    page(s.entry.page)
                    UnderDim { above(i) }
                }
            }
        }
        // While a page is moving the screen under it takes no taps, as on the iPhone.
        if (moving && active) {
            Box(Modifier.matchParentSize().pointerInput(Unit) {
                awaitPointerEventScope { while (true) awaitPointerEvent().changes.forEach { it.consume() } }
            })
        }
    }
}

/** UIKit's parallax dimming: the page underneath darkens a tenth as the next one covers it. */
@Composable
private fun UnderDim(amount: () -> Float) {
    Box(
        Modifier
            .fillMaxSize()
            .graphicsLayer { alpha = amount() * 0.1f }
            .background(Color.Black),
    )
}
