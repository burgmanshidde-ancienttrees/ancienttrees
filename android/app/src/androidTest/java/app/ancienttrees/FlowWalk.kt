// The routes between screens, walked with a finger on the emulator: the Android
// twin of ios AncientTreesUITests/FlowWalk.swift. A screen that looks right but
// cannot be reached, or a gate that leaves you nowhere, only shows up here.
//
//   cd android && ./gradlew connectedDebugAndroidTest
//
// Signed out on purpose: every gate is the server's (hard rule 11), so a phone
// that has never signed in must be asked before it can keep a tree or open the
// camera, and must land back where it was.

package app.ancienttrees

import android.content.Intent
import android.net.Uri
import androidx.compose.ui.test.ExperimentalTestApi
import androidx.compose.ui.test.hasContentDescription
import androidx.compose.ui.test.hasTestTag
import androidx.compose.ui.test.junit4.createEmptyComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performClick
import androidx.test.core.app.ActivityScenario
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.After
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@OptIn(ExperimentalTestApi::class)
@RunWith(AndroidJUnit4::class)
class FlowWalk {
    @get:Rule val rule = createEmptyComposeRule()
    private var scenario: ActivityScenario<MainActivity>? = null

    /** The catalogue reads in seconds on an emulator; every wait allows for it. */
    private val slow = 45_000L

    private fun start(vararg args: String, data: Uri? = null) {
        val intent = Intent(ApplicationProvider.getApplicationContext(), MainActivity::class.java).apply {
            // No opening cover and a fixed place, as the iPhone's sweep stands in Athens.
            putExtra("args", arrayOf("-no-cover", "-at=37.9715,23.7275") + args)
            if (data != null) { action = Intent.ACTION_VIEW; this.data = data }
        }
        scenario = ActivityScenario.launch(intent)
    }

    @After fun close() { scenario?.close() }

    private fun waitFor(tag: String) = rule.waitUntilAtLeastOneExists(hasTestTag(tag), slow)
    private fun gone(tag: String) = rule.waitUntilDoesNotExist(hasTestTag(tag), slow)

    @Test fun theTabsReachEveryPlace() {
        start()
        waitFor("tab-discover")
        rule.onNodeWithTag("tab-discover").performClick()
        rule.waitUntilAtLeastOneExists(hasContentDescription("explore-home"), slow)
        rule.onNodeWithTag("tab-my-trees").performClick()
        waitFor("collection-tab")
        rule.onNodeWithTag("tab-map").performClick()
        gone("collection-tab")
    }

    @Test fun aTreeOpensAndBackLeavesIt() {
        start("-open=tree:ath_004")
        waitFor("tree-page")
        rule.onNodeWithTag("back-to-map").performClick()
        gone("tree-page")
        waitFor("tab-map")
    }

    @Test fun keepingATreeAsksToSignInFirst() {
        start("-open=tree:ath_004")
        waitFor("tree-save")
        rule.onNodeWithTag("tree-save").performClick()
        waitFor("signin-sheet")
    }

    @Test fun theCameraAsksToSignInBeforeTheSheet() {
        start()
        waitFor("tab-collect")
        rule.onNodeWithTag("tab-collect").performClick()
        waitFor("signin-sheet")
    }

    @Test fun aLinkFromTheWebsiteOpensItsTree() {
        start(data = Uri.parse("https://ancienttrees.app/athens/transplanted-olive-of-megali-tou-genous-scholis"))
        waitFor("tree-page")
    }
}
