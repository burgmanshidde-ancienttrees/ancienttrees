// Asking for a store review, ported from ios Kit/ReviewPrompt.swift with every
// timing rule it carries:
//
// - Engagement is three different trees LOOKED AT (Hidde, 2026-09-04: "ik denk
//   naar 3 bomen bekeken in de app"), a set of ids rather than a tally, and only
//   trees of our own catalogue. A tree ticked off counts too.
// - Two moments ask: a tree page closing (the pause) and two seconds after a new
//   tick (the payoff). Never from a button, never on launch.
// - Three milestones (3, 10, 25 trees seen), each at most once, at least seven
//   days apart, three asks in the install's lifetime.
// - A plain question first (Hidde, 2026-10-06: "Polarsteps doet dat ook
//   gewoon"): Yes goes to the store, Not really opens the feedback form.
// - After a Yes: silent until a NEWER version and at least 120 days (Hidde,
//   2026-10-20); every milestone counts as fired from then. Not really leaves
//   the later milestones in place.
// - The state is per install ("reviewPrompt.*" in data/cross-device.json),
//   cleared by -reset-collection; -no-review-prompt silences it, -review-ask
//   opens the sheet for the sweep.
//
// The screen that notices only raises `pending`; the ROOT draws the sheet
// (ReviewAskHost), because the screen that notices is usually the one going away.
//
// FORCED ON ANDROID (data/android-parity.json): the iPhone's Yes asks Apple's own
// rating dialog (requestReview). Android has no system rating dialog without
// Google's Play Core review library, a new third-party dependency that needs
// Hidde's yes, and Google's in-app review guidelines forbid asking any question
// before that dialog, which is exactly what the Polarsteps question does. Until
// he decides, Yes opens the app's Play Store page, where the stars are.

package app.ancienttrees.ui

import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import app.ancienttrees.R

/** The decision, with the device's memory behind a tiny interface so tests need no Android. */
class ReviewPrompt(
    private val store: Store,
    private val version: String,
    private val suppressed: Boolean = false,
) {
    interface Store {
        fun strings(key: String): Set<String>
        fun putStrings(key: String, value: Set<String>)
        fun long(key: String): Long?
        fun putLong(key: String, value: Long?)
        fun string(key: String): String?
        fun putString(key: String, value: String?)
    }

    /** Set when a milestone is reached; the root watches it and asks. */
    var pending by mutableStateOf(false)

    private var fired: Set<String>
        get() = store.strings(FIRED)
        set(v) = store.putStrings(FIRED, v)
    private var last: Long?
        get() = store.long(LAST)
        set(v) = store.putLong(LAST, v)
    private var seen: Set<String>
        get() = store.strings(SEEN)
        set(v) = store.putStrings(SEEN, v)

    val seenCount: Int get() = seen.size

    /** Record that a tree page was opened; stops once the last milestone is behind us. */
    fun saw(treeId: String) {
        val ceiling = MILESTONES.last().second
        val s = seen
        if (s.size >= ceiling) return
        seen = s + treeId
    }

    /** Called at a pause. Raises `pending` when a new milestone is reached and allowed. */
    fun consider(now: Long = System.currentTimeMillis()): Boolean {
        if (suppressed) return false
        val yesVersion = store.string(YES_VERSION)
        val yesDate = store.long(YES_DATE)
        if (yesVersion != null && yesDate != null) {
            if (!asksAgainAfterYes(yesVersion, yesDate, version, now)) return false
            store.putString(YES_VERSION, null)
            store.putLong(YES_DATE, null)
            last = now
            pending = true
            return true
        }
        val name = milestone(seen.size, fired, last, now) ?: return false
        fired = fired + name
        last = now
        pending = true
        return true
    }

    /** A Yes quiets the asking until a newer version, at least 120 days on. */
    fun answeredYes(now: Long = System.currentTimeMillis()) {
        fired = MILESTONES.map { it.first }.toSet()
        store.putString(YES_VERSION, version)
        store.putLong(YES_DATE, now)
    }

    fun reset() {
        store.putStrings(FIRED, emptySet()); store.putLong(LAST, null); store.putStrings(SEEN, emptySet())
        store.putString(YES_VERSION, null); store.putLong(YES_DATE, null)
    }

    companion object {
        // The iPhone's keys, so data/cross-device.json names the same thing on both phones.
        const val FIRED = "reviewPrompt.fired.v2"
        const val LAST = "reviewPrompt.last.v2"
        const val SEEN = "reviewPrompt.seen.v1"
        const val YES_VERSION = "reviewPrompt.yes.v1.version"
        const val YES_DATE = "reviewPrompt.yes.v1.date"
        const val MAX_ASKS = 3
        const val QUIET_DAYS = 7.0
        const val YES_QUIET_DAYS = 120.0
        private const val DAY = 86_400_000.0

        /** Ordered so the first unfired, met threshold wins. */
        val MILESTONES = listOf("first" to 3, "second" to 10, "third" to 25)

        fun milestone(total: Int, fired: Set<String>, last: Long?, now: Long,
                      maxAsks: Int = MAX_ASKS, quietDays: Double = QUIET_DAYS): String? {
            if (fired.size >= maxAsks) return null
            if (last != null && (now - last) < quietDays * DAY) return null
            return MILESTONES.firstOrNull { total >= it.second && it.first !in fired }?.first
        }

        fun asksAgainAfterYes(yesVersion: String, yesDate: Long, version: String, now: Long,
                              quietDays: Double = YES_QUIET_DAYS): Boolean =
            version != yesVersion && (now - yesDate) >= quietDays * DAY

        /** The device store: SharedPreferences "device", as the cover's hero index. */
        fun on(context: Context, args: List<String>): ReviewPrompt {
            val p = context.applicationContext.getSharedPreferences("device", Context.MODE_PRIVATE)
            val store = object : Store {
                override fun strings(key: String) = p.getStringSet(key, emptySet()).orEmpty().toSet()
                override fun putStrings(key: String, value: Set<String>) = p.edit().putStringSet(key, value).apply()
                override fun long(key: String) = if (p.contains(key)) p.getLong(key, 0) else null
                override fun putLong(key: String, value: Long?) =
                    p.edit().apply { if (value == null) remove(key) else putLong(key, value) }.apply()
                override fun string(key: String) = p.getString(key, null)
                override fun putString(key: String, value: String?) =
                    p.edit().apply { if (value == null) remove(key) else putString(key, value) }.apply()
            }
            val version = runCatching { context.packageManager.getPackageInfo(context.packageName, 0).versionName }.getOrNull().orEmpty()
            return ReviewPrompt(store, version, suppressed = "-no-review-prompt" in args).also {
                if ("-reset-collection" in args) it.reset()
            }
        }
    }
}

/**
 * ReviewAsk (the ViewModifier on the iPhone's root): the question as THE ONE
 * SHEET, Yes in green, Not really in grey; Not really opens the feedback form
 * once the question has gone.
 */
@Composable
fun ReviewAskHost(prompt: ReviewPrompt, args: List<String>, onFeedback: () -> Unit) {
    val context = LocalContext.current
    var asking by remember { mutableStateOf(false) }
    // -review-ask: the sheet without a finger, a beat after launch as on the iPhone.
    LaunchedEffect(Unit) {
        if ("-review-ask" in args) {
            kotlinx.coroutines.delay(1000)
            prompt.pending = true
        }
    }
    LaunchedEffect(prompt.pending) {
        if (prompt.pending) {
            prompt.pending = false
            asking = true
        }
    }
    if (!asking) return
    BrandSheet(
        icon = Icons.Outlined.FavoriteBorder,
        title = stringResource(R.string.review_title),
        message = stringResource(R.string.review_message),
        onDismiss = { asking = false },
        buttons = listOf(
            SheetButton(stringResource(R.string.review_yes), SheetKind.PRIMARY) {
                prompt.answeredYes()
                asking = false
                openStorePage(context)
            },
            SheetButton(stringResource(R.string.review_no), SheetKind.SECONDARY) {
                asking = false
                onFeedback()
            },
        ),
    )
}

/** The app's page on Google Play: the Play Store app, else the web page. */
fun openStorePage(context: Context) {
    val id = context.packageName
    val market = Intent(Intent.ACTION_VIEW, Uri.parse("market://details?id=$id")).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    runCatching { context.startActivity(market) }.onFailure {
        runCatching {
            context.startActivity(
                Intent(Intent.ACTION_VIEW, Uri.parse("https://play.google.com/store/apps/details?id=$id")).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK),
            )
        }
    }
}
