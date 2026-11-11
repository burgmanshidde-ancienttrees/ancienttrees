// The routes between screens, walked with a finger on the emulator: the Android
// twin of ios AncientTreesUITests/FlowWalk.swift, flow for flow and identifier
// for identifier (review 2026-11-11: the iPhone walked 17 flows, Android 5).
// A screen that looks right but cannot be reached, or a gate that leaves you
// nowhere, only shows up here.
//
//   python3 scripts/android_walk.py          (takes the emulator lock)
//   cd android && ./gradlew connectedDebugAndroidTest
//
// Each flow is a list of steps. After every step the one invariant FlowWalk.swift
// asserts is checked: THERE IS ALWAYS A WAY BACK, a tab bar, a back control, or a
// sheet's own Cancel, Close or Done. Android's system back is not counted: the
// iPhone has none, and a screen whose only exit is a gesture the iPhone lacks is
// not the same screen. The frames go to the app's files (walk/), which
// scripts/android_walk.py pulls into out/android-walk/.

package app.ancienttrees

import android.content.Intent
import android.graphics.Bitmap
import android.net.Uri
import androidx.compose.ui.semantics.SemanticsProperties
import androidx.compose.ui.test.ExperimentalTestApi
import androidx.compose.ui.test.SemanticsMatcher
import androidx.compose.ui.test.SemanticsNodeInteraction
import androidx.compose.ui.test.click
import androidx.compose.ui.test.hasContentDescription
import androidx.compose.ui.test.hasTestTag
import androidx.compose.ui.test.hasText
import androidx.compose.ui.test.junit4.ComposeTestRule
import androidx.compose.ui.test.junit4.createEmptyComposeRule
import androidx.compose.ui.test.onAllNodesWithTag
import androidx.compose.ui.test.onFirst
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onRoot
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollTo
import androidx.compose.ui.test.performTextInput
import androidx.compose.ui.test.performTouchInput
import androidx.compose.ui.test.swipe
import androidx.compose.ui.test.swipeUp
import androidx.test.core.app.ActivityScenario
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.After
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File

/** One thing a person does, and what to call the picture it leaves. */
class Step(val name: String, val act: Walker.() -> Unit)

/** The finger: taps by the iPhone's identifier or label, drags in fractions of the screen. */
@OptIn(ExperimentalTestApi::class)
class Walker(val rule: ComposeTestRule) {
    val slow = 45_000L

    /** A test tag, else the text a person reads, else what a screen reader says: the iPhone's identifier or label. */
    fun named(id: String): SemanticsMatcher = hasTestTag(id) or hasText(id) or hasContentDescription(id)

    fun exists(id: String): Boolean = rule.onAllNodes(named(id)).fetchSemanticsNodes().isNotEmpty()

    /** Tap ONCE IT IS THERE (FlowWalk.swift's tap: a sheet springs, a list fills, a push animates). */
    fun tap(id: String) {
        rule.waitUntilAtLeastOneExists(named(id), slow)
        val node = rule.onAllNodes(named(id)).onFirst()
        runCatching { node.performScrollTo() }
        node.performClick()
        rule.waitForIdle()
    }

    fun waitFor(id: String) = rule.waitUntilAtLeastOneExists(named(id), slow)

    fun type(id: String, text: String) {
        waitFor(id)
        rule.onAllNodes(named(id)).onFirst().performTextInput(text)
        rule.waitForIdle()
    }

    /** A drag in fractions of the screen, so one number works on every phone. */
    fun drag(from: Float, to: Float) {
        rule.onRoot().performTouchInput {
            swipe(androidx.compose.ui.geometry.Offset(width / 2f, height * from), androidx.compose.ui.geometry.Offset(width / 2f, height * to), 400)
        }
        rule.waitForIdle()
    }

    fun swipeUp() {
        rule.onRoot().performTouchInput { swipeUp() }
        rule.waitForIdle()
    }

    /** A tap at a point in fractions of the screen. */
    fun tapAt(x: Float, y: Float) {
        rule.onRoot().performTouchInput { click(androidx.compose.ui.geometry.Offset(width * x, height * y)) }
        rule.waitForIdle()
    }

    /** The page's own back control (FlowWalk.swift's back: the navigation bar's first button). */
    fun back() {
        val m = hasContentDescription("Back") or hasContentDescription("Back to the map") or hasTestTag("back-to-map") or hasTestTag("draft-back")
        rule.waitUntilAtLeastOneExists(m, slow)
        rule.onAllNodes(m).onFirst().performClick()
        rule.waitForIdle()
    }

    /** The first tree card in whatever list is on screen; on the search screen a tree among the results. */
    fun firstCard(): SemanticsNodeInteraction {
        if (exists("Back to the map")) {
            // A lazy list composes only what is on screen, so the trees below the
            // places and species are not there to find: the Trees lane first.
            if (!exists("search-result-tree")) tap("Trees")
            waitFor("search-result-tree")
            return rule.onAllNodesWithTag("search-result-tree").onFirst()
        }
        // A tag on the map's rows and highlights, a description on Discover's tiles.
        waitFor("tree-card")
        return rule.onAllNodes(named("tree-card")).onFirst()
    }

    /** Somewhere to go that is not forward (FlowWalk.swift's hasAWayBack). */
    fun hasAWayBack(): Boolean {
        if (exists("tab-map")) return true
        // The map's list at its count bar hides the tab bar (build 42); the bar is the way back.
        if (exists("sheet-show-list") || exists("map-count")) return true
        for (id in listOf("Back", "Back to the map", "back-to-map", "draft-back", "Cancel", "Close", "Done", "Not now")) {
            if (exists(id)) return true
        }
        // A sheet you drag away: the grabber is the handle and the way out.
        return listOf("spot-sheet", "signin-sheet", "people-sheet", "contribute-sheet").any { exists(it) }
    }
}

@OptIn(ExperimentalTestApi::class)
@RunWith(AndroidJUnit4::class)
class FlowWalk {
    @get:Rule val rule = createEmptyComposeRule()
    private var scenario: ActivityScenario<MainActivity>? = null
    private val walker by lazy { Walker(rule) }

    @After fun close() { scenario?.close() }

    /** The iPhone's launch: Amsterdam unless the flow names its own place, and the first -at wins. */
    private fun start(args: List<String>, data: Uri? = null) {
        val place = if (args.any { it.startsWith("-at=") }) emptyList() else listOf("-at=52.3731,4.8922")
        val intent = Intent(ApplicationProvider.getApplicationContext(), MainActivity::class.java).apply {
            putExtra("args", (place + listOf("-AppleLocale=en_NL", "-reset-collection", "-reset-blocks", "-no-cover", "-no-review-prompt") + args).toTypedArray())
            if (data != null) { action = Intent.ACTION_VIEW; this.data = data }
        }
        scenario?.close()
        scenario = ActivityScenario.launch(intent)
    }

    /** Walk one flow: launch, every step, a frame and the invariant after each. */
    private fun walk(flow: String, args: List<String>, vararg steps: Step) {
        start(args)
        // The catalogue is read before anything exists; the tab bar or a sheet means it is.
        rule.waitUntil(walker.slow) { walker.hasAWayBack() }
        shoot(flow, 0, "launch")
        steps.forEachIndexed { i, step ->
            // A step that fails leaves its frame too: the picture says why.
            try { step.act(walker) } catch (e: Throwable) { shoot(flow, i + 1, step.name + "-FAILED"); throw e }
            // Long enough for a push, a sheet or a spring to land (FlowWalk.swift: 1.2 s).
            Thread.sleep(1200)
            rule.waitForIdle()
            shoot(flow, i + 1, step.name)
            assertTrue("$flow: after \"${step.name}\" there is no tab bar, no back control and nothing to dismiss", walker.hasAWayBack())
        }
    }

    private fun shoot(flow: String, n: Int, name: String) {
        val ctx = InstrumentationRegistry.getInstrumentation().targetContext
        val dir = File(ctx.filesDir, "walk").apply { mkdirs() }
        val shot: Bitmap = InstrumentationRegistry.getInstrumentation().uiAutomation.takeScreenshot() ?: return
        File(dir, "%s__%02d-%s.png".format(flow, n, name)).outputStream().use { shot.compress(Bitmap.CompressFormat.PNG, 90, it) }
    }

    // A signed-in account, because signed out is a different and much shorter app.
    private val signedIn = listOf("-signed-in", "-collected=ams_001,ams_002")

    // MARK: - the flows, in FlowWalk.swift's order

    // The one that was broken: two doors to the profile editor and a way back out of both.
    @Test fun settings() = walk("settings", listOf("-tab=2") + signedIn,
        Step("gear") { tap("mytrees-settings") },
        Step("your-own-card") { tap("profile-signin") },
        Step("cancel-the-editor") { tap("Cancel") },
        Step("back-to-my-trees") { back() },
    )

    // The sheet: raising it from the header moves the sheet rather than opening something.
    @Test fun myTreesSheet() = walk("my-trees-sheet", listOf("-tab=2") + signedIn,
        Step("drag-the-header-up") { drag(0.55f, 0.16f) },
        Step("scroll-the-list") { swipeUp() },
        Step("drag-back-down") { drag(0.22f, 0.75f) },
    )

    // The map's sheet and the page it leads to; a tree page from a tab keeps its back.
    @Test fun mapToATree() = walk("map-to-a-tree", listOf("-tab=0"),
        // A TAP: at peek the sheet takes no taps of its own and one anywhere raises it.
        Step("raise-the-sheet") { tapAt(0.5f, 0.88f) },
        Step("open-the-first-tree") {
            drag(0.6f, 0.1f)
            Thread.sleep(1000)
            firstCard().performClick()
        },
        Step("back-to-the-map") { back() },
    )

    // AIRBNB'S WAY DOWN AND BACK (build 42): the Map pill drops the list to its count
    // bar and the tab bar steps away; a tap on the bar brings both back.
    @Test fun mapPillAndBack() = walk("map-pill-and-back", listOf("-tab=0", "-sheet=full"),
        Step("tap-the-map-pill") {
            tap("map-pill")
            rule.waitUntilDoesNotExist(hasTestTag("tab-map"), slow)
            assertTrue("the Map pill did not bring the list down to its count bar", exists("map-count") || exists("sheet-show-list"))
        },
        Step("tap-the-count-bar") {
            tap(if (exists("sheet-show-list")) "sheet-show-list" else "map-count")
            waitFor("tab-map")
        },
    )

    // The camera in the bar is gated; a gate that leaves you nowhere is worse than none.
    @Test fun collectGate() = walk("collect-gate", listOf("-tab=0"),
        Step("tap-the-camera") { tap("tab-collect"); waitFor("signin-sheet") },
    )

    // WHICH ONE IS IT: compare, come back without committing, pick it, done.
    @Test fun whichOneIsIt() = walk("which-one-is-it", listOf("-collect", "-collect-identify") + signedIn,
        Step("compare-a-candidate") { tap("collect-compare-0") },
        Step("back-to-the-list") { tap("Back to the list") },
        Step("compare-it-again") { tap("collect-compare-0") },
        Step("say-it-is-the-one") { tap("collect-this-is-the-one") },
        Step("done") { tap("collect-done") },
    )

    // ADDING A TREE WE DO NOT MAP: back first and keep editing (a draft lost by one
    // tap is the fault to catch), then save, which leaves the page standing.
    @Test fun addATreeDraft() = walk("add-a-tree-draft", listOf("-collect", "-collect-describe") + signedIn,
        Step("try-to-leave") { tap("draft-back") },
        Step("keep-editing") { tap("Keep editing") },
        Step("save-it") { tap("draft-save") },
        Step("confirmed") { tap("saved-done") },
    )

    // "Add a new tree" from the list ends on the new tree's draft page, near and far.
    @Test fun addNewTreeFromTheList() = walk("add-new-tree-from-the-list", listOf("-collect", "-collect-identify") + signedIn,
        Step("it-is-none-of-these") { tap("collect-none-of-these") },
        Step("the-draft-page") { tap("draft-save") },
    )

    @Test fun addNewTreeFromTheFarList() = walk("add-new-tree-from-the-far-list",
        listOf("-collect", "-collect-identify", "-at=37.4260,-6.0080") + signedIn,
        Step("it-is-none-of-these") { tap("collect-none-of-these") },
        Step("the-draft-page") { tap("draft-save") },
    )

    // A WRONG PIN (Seville, 2026-10-15): the far list offers the closest trees, a tap asks once, it collects.
    @Test fun aTreeWhosePinIsWrong() = walk("a-tree-whose-pin-is-wrong",
        listOf("-collect", "-collect-identify", "-at=37.4260,-6.0080") + signedIn,
        Step("pick-a-far-tree") { tap("collect-candidate-0") },
        Step("say-it-is-the-one") { tap("collect-this-is-the-one") },
        Step("done") { tap("collect-done") },
    )

    // The honest exit, which must never lose a photograph.
    @Test fun notSureWhich() = walk("not-sure-which", listOf("-collect", "-collect-identify") + signedIn,
        Step("say-you-cannot-tell") { tap("collect-not-sure") },
        Step("done") { tap("collect-unsure-done") },
    )

    // FIND PEOPLE: the demo people have no account, so a tap only has to turn the button and stay.
    @Test fun findPeople() = walk("find-people", listOf("-tab=2", "-people", "-people-demo") + signedIn,
        Step("follow-the-first") { tap("person-follow") },
        Step("unfollow-again") { tap("person-follow") },
        Step("back") { back() },
    )

    // MODERATION: the sequence a store reviewer taps.
    @Test fun reportAndBlock() = walk("report-and-block", listOf("-tab=2", "-people", "-people-demo") + signedIn,
        Step("open-the-ellipsis") { tap("person-more") },
        Step("choose-report") { tap("Report this person") },
        Step("pick-a-reason") { tap("An offensive name or picture") },
        Step("close-the-thank-you") { tap("report-thanks-done") },
    )

    // The way in from a search.
    @Test fun searchToATree() = walk("search-to-a-tree", listOf("-search=lis"),
        Step("first-result") { firstCard().performClick() },
        Step("back") { back() },
    )

    // Discover, and the page under it.
    @Test fun discoverToACity() = walk("discover-to-a-city", listOf("-tab=1"),
        Step("scroll-the-feed") { swipeUp() },
        Step("open-something") { firstCard().performClick() },
        Step("back") { back() },
    )

    // The lane picker, reported dead three times on the iPhone before it was pinned.
    @Test fun myTreesLanes() = walk("my-trees-lanes", listOf("-tab=2") + signedIn,
        Step("raise-the-sheet") { drag(0.55f, 0.16f) },
        Step("favourites") { tap("lane-want") },
        Step("back-to-my-trees") { tap("lane-collected") },
    )

    // THE ROUTE TO DELETING AN ACCOUNT (store rule): the tap is the assertion; it stops at Cancel.
    @Test fun deleteAccountRoute() = walk("delete-account-route", listOf("-tab=2", "-settings") + signedIn,
        Step("open-account") { tap("settings-account") },
        Step("type-the-word") { type("delete-confirm-field", "DELETE") },
        Step("delete-asks-first") { tap("delete-confirm-button") },
        Step("cancel") { tap("delete-cancel") },
    )

    // Settings all the way down: sign out asks first rather than acts.
    @Test fun settingsBottom() = walk("settings-bottom", listOf("-tab=2", "-settings") + signedIn,
        Step("scroll-to-the-bottom") { swipeUp(); swipeUp() },
        Step("sign-out-asks-first") { tap("settings-signout") },
        Step("cancel") { tap("signout-cancel") },
    )

    // MARK: - Android's own, kept from the first walk

    @Test fun keepingATreeAsksToSignInFirst() = walk("save-gate", listOf("-open=tree:ams_001"),
        Step("save") { tap("tree-save"); waitFor("signin-sheet") },
    )

    // The fake session acts signed in, as the iPhone's -signed-in does (Account.swift:207):
    // the bookmark fills instead of asking.
    @Test fun aSaveSignedInFillsTheBookmark() = walk("save-signed-in", listOf("-open=tree:ams_001", "-signed-in"),
        Step("save") {
            tap("tree-save")
            rule.waitUntilAtLeastOneExists(hasTestTag("tree-save") and SemanticsMatcher.expectValue(SemanticsProperties.Selected, true), slow)
            assertTrue("signed in, save still asked to sign in", !exists("signin-sheet"))
        },
    )

    // Signed in, the camera opens the collect intro, not the sign-in sheet (FlowWalk's signed-in camera).
    @Test fun theCameraSignedInOpensTheIntro() = walk("camera-signed-in", listOf("-tab=0", "-signed-in"),
        Step("tap-the-camera") {
            tap("tab-collect")
            waitFor("add-start")
            assertTrue("signed in, the camera still asked to sign in", !exists("signin-sheet"))
        },
    )

    // A LIBRARY PHOTOGRAPH THAT DOES NOT SAY WHERE (LibraryPicker.swift, iNaturalist):
    // never refused, it asks where the tree stands. The system picker cannot be
    // driven from a test, so the walk starts on the step it leads to (-collect-place,
    // the sweep's frame) and places the pin.
    @Test fun aLibraryPhotoWithoutAPlaceAsksWhereItStands() = walk("library-photo-no-place",
        listOf("-collect", "-collect-place") + signedIn,
        Step("asks-where-it-stands") { waitFor("Where does it stand?"); waitFor("collect-place-confirm") },
        Step("the-tree-is-here") { tap("collect-place-confirm") },
    )

    @Test fun aLinkFromTheWebsiteOpensItsTree() {
        start(emptyList(), data = Uri.parse("https://ancienttrees.app/athens/transplanted-olive-of-megali-tou-genous-scholis"))
        walker.waitFor("tree-page")
    }
}
