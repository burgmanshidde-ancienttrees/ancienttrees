// Signed in for real: the Android twin of ios AncientTreesUITests/SignedInRoundTrip.swift.
// A save goes to the server, survives closing the app, and comes off again, on the
// test account apptest@ancienttrees.app (scripts/test_session.py; ours, never a
// reader, so nothing here is counted). Hidde, 2026-11-10: "can you test with
// actual test accounts".
//
//   python3 scripts/android_walk.py      (makes the session and passes it as AT_SESSION)
//
// Without AT_SESSION the test is skipped, never faked: the fake signed-in state
// cannot write, so it proves nothing about the server.

package app.ancienttrees

import android.content.Intent
import androidx.compose.ui.test.ExperimentalTestApi
import androidx.compose.ui.test.SemanticsMatcher
import androidx.compose.ui.test.hasTestTag
import androidx.compose.ui.test.isSelected
import androidx.compose.ui.test.junit4.createEmptyComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performClick
import androidx.test.core.app.ActivityScenario
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.After
import org.junit.Assume.assumeTrue
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@OptIn(ExperimentalTestApi::class)
@RunWith(AndroidJUnit4::class)
class SignedInRoundTrip {
    @get:Rule val rule = createEmptyComposeRule()
    private var scenario: ActivityScenario<MainActivity>? = null
    private var session = ""
    private val slow = 45_000L

    /** A tree with a photograph in Athens, as the iPhone's round trip uses. */
    private val tree = "ath_004"

    @Before fun session() {
        session = InstrumentationRegistry.getArguments().getString("AT_SESSION").orEmpty()
        assumeTrue("no test-account session (AT_SESSION)", session.isNotEmpty())
    }

    @After fun close() { scenario?.close() }

    private fun open() {
        scenario?.close()
        val intent = Intent(ApplicationProvider.getApplicationContext(), MainActivity::class.java).apply {
            putExtra("args", arrayOf("-no-cover", "-at=37.9715,23.7275", "-open=tree:$tree"))
            putExtra("AT_TEST_SESSION", session)
        }
        scenario = ActivityScenario.launch(intent)
        rule.waitUntilAtLeastOneExists(hasTestTag("tree-save"), slow)
    }

    /** The account's saves arrive a moment after the page: wait for the server's answer. */
    private fun waitSaved(saved: Boolean) {
        val m = hasTestTag("tree-save") and (if (saved) isSelected() else SemanticsMatcher("not selected") {
            it.config.getOrElseNullable(androidx.compose.ui.semantics.SemanticsProperties.Selected) { null } == false
        })
        rule.waitUntilAtLeastOneExists(m, slow)
    }

    @Test fun aSaveReachesTheServerAndComesBack() {
        open()
        // Start from not saved, whatever an earlier run left.
        rule.waitForIdle()
        Thread.sleep(4000)
        val already = rule.onNodeWithTag("tree-save").fetchSemanticsNode().config
            .getOrElseNullable(androidx.compose.ui.semantics.SemanticsProperties.Selected) { null } == true
        if (already) {
            rule.onNodeWithTag("tree-save").performClick()
            waitSaved(false)
            Thread.sleep(2000)
        }

        rule.onNodeWithTag("tree-save").performClick()
        waitSaved(true)
        Thread.sleep(2000)

        // Closed and opened again: the save came back from the server, not from memory.
        open()
        waitSaved(true)

        // And off again, the same way, which is also the clean-up.
        rule.onNodeWithTag("tree-save").performClick()
        waitSaved(false)
        Thread.sleep(2000)
        open()
        waitSaved(false)
    }
}
