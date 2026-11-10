// The place's white box under a city's Highlights, and the Plus question under
// its trees. Ported from ios Screens/PlaceAmbassadors.swift (PlaceAsksBox,
// PlusUnderBox, PlaceAmbassadors), AmbassadorBadge.swift (AmbassadorWantedRow,
// its `.slim` and `.link` looks, AmbassadorApplySheet), PlusAsk.swift (PlusRow,
// PlusQuestionSheet), Kit/PlusAnswers.swift and Kit/AppSwitches.swift.
//
// DIRECTION C (Hidde, 2026-11-05): one slim white box, the way Google Maps and
// komoot keep a place's people and asks in one block. Its row is the ambassador:
// the named person with a green "Become one too" at the end of their line, or,
// with nobody named, "Become the <place> ambassador". Radius 14, a hairline
// border, rows 46 tall (58 with an avatar), 14 inside the edges. The Plus
// question sits in its own box under the place's trees (2026-11-06).
//
// ANDROID-FORCED: the sheets are Material's modal bottom sheet (BrandSheet).

package app.ancienttrees.ui

import android.content.Context
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.account.AmbassadorAsk
import app.ancienttrees.account.Supa
import app.ancienttrees.feed.Catalogue
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

/** What the box needs from the screen that owns the account (Environment(Account), Navigator, Profiles). */
class PlaceHost(
    val signedIn: Boolean,
    val email: String?,
    val token: suspend () -> String?,
    /** Signed out: the sign-in sheet with [reason]'s words, then [then] once signed in. */
    val signIn: (reason: SignInReason, then: () -> Unit) -> Unit,
    val openPerson: (String) -> Unit,
    /** The places you look after (Profiles.myPlaces), so the ask is never yours. */
    val myPlaces: List<String>,
)

val LocalPlaceHost = staticCompositionLocalOf<PlaceHost?> { null }

/** PlaceAsksBox: the white box with the ambassador row(s). */
@Composable
fun PlaceAsksBox(slug: String, title: String, catalogue: Catalogue, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    Column(
        modifier
            .fillMaxWidth()
            .background(brand.surface, RoundedCornerShape(14.dp))
            .border(1.dp, brand.hairline, RoundedCornerShape(14.dp))
            .testTag("place-asks"),
    ) {
        PlaceAmbassadors(slug, title, catalogue)
    }
}

/** PlusUnderBox: the Plus question in its own box, while the server's switch is on and it is unanswered here. */
@Composable
fun PlusUnderBox(title: String, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    if (!AppSwitches.showPlus(LocalContext.current)) return
    Box(
        modifier
            .fillMaxWidth()
            .background(brand.surface, RoundedCornerShape(14.dp))
            .border(1.dp, brand.hairline, RoundedCornerShape(14.dp)),
    ) { PlusRow(title) }
}

/** PlaceAmbassadors: one view for every place, so the place header can never draw it two ways. */
@Composable
private fun PlaceAmbassadors(slug: String, title: String, catalogue: Catalogue) {
    val brand = Brand.colors
    val named = catalogue.ambassadors(slug)
    if (named.isEmpty()) {
        AmbassadorSeat(title, seated = catalogue.seated(slug), link = false)
    } else {
        named.forEachIndexed { i, a ->
            if (i > 0) Box(Modifier.fillMaxWidth().padding(vertical = 0.dp).background(brand.hairline).heightIn(min = 1.dp, max = 1.dp))
            PersonRow(a.name, a.profile, title, last = i == named.lastIndex)
        }
    }
}

/**
 * The person: initial with the badge, the name, and under it "<place>
 * ambassador · Become one too". The website's numbers (style.css .city-box):
 * avatar 30 with a 13 point letter, name 14 semibold, role 12, 10 apart.
 */
@Composable
private fun PersonRow(name: String, profile: String?, place: String, last: Boolean) {
    val brand = Brand.colors
    val host = LocalPlaceHost.current
    val open = stringResource(R.string.amb_open_profile, name)
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 58.dp)
            .let { m ->
                if (profile != null && host != null) m.clickable(role = Role.Button) { host.openPerson(profile) }.semantics { contentDescription = open }
                else m
            }
            .padding(horizontal = 14.dp)
            .testTag(if (profile != null) "ambassador-profile" else "ambassador-row"),
    ) {
        Box(Modifier.size(30.dp)) {
            Box(Modifier.size(30.dp).background(brand.mossTint, CircleShape), contentAlignment = Alignment.Center) {
                Text(name.trim().take(1).uppercase(), fontSize = 13.sp, fontWeight = FontWeight.Bold, color = brand.moss)
            }
            Icon(
                Sym.VerifiedFill, null, tint = brand.moss,
                modifier = Modifier.align(Alignment.BottomEnd).offset(x = 3.dp, y = 3.dp).size(13.dp).background(brand.surface, CircleShape),
            )
        }
        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(3.dp)) {
            Text(name, fontFamily = BrandFace, fontWeight = FontWeight.SemiBold, fontSize = 14.sp, color = brand.ink)
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    stringResource(R.string.amb_role, place) + if (last) " · " else "",
                    fontFamily = BrandFace, fontSize = 12.sp, color = brand.inkSoft,
                )
                if (last) AmbassadorSeat(place, seated = true, link = true)
            }
        }
        if (profile != null) {
            Icon(Sym.ChevronRight, null, tint = brand.inkSoft.copy(alpha = 0.6f), modifier = Modifier.size(18.dp))
        }
    }
}

/**
 * AmbassadorWantedRow in the box: `.slim` (the seal, "Become the <place>
 * ambassador", a chevron) or `.link` (the green words at the end of the named
 * person's line). Signed out it asks for the account first, then the explainer;
 * nothing is sent until Apply. Not drawn for a place you look after already.
 */
@Composable
private fun AmbassadorSeat(place: String, seated: Boolean, link: Boolean) {
    val brand = Brand.colors
    val host = LocalPlaceHost.current ?: return
    if (host.myPlaces.any { it.equals(place, ignoreCase = true) }) return
    val scope = rememberCoroutineScope()
    var asked by remember { mutableStateOf(false) }
    var sending by remember { mutableStateOf(false) }
    var confirming by remember { mutableStateOf(false) }
    var sent by remember { mutableStateOf(false) }
    var failed by remember { mutableStateOf(false) }
    LaunchedEffect(host.signedIn) { asked = AmbassadorAsk.asked(place, host.token()) }
    fun tap() {
        if (!host.signedIn) host.signIn(SignInReason.Ambassador) { confirming = true } else confirming = true
    }
    val tapMod = Modifier
        .clickable(
            enabled = !(asked || sending),
            role = Role.Button,
            interactionSource = remember { MutableInteractionSource() },
            indication = null,
            onClick = ::tap,
        )
        .testTag("ambassador-wanted")
    if (link) {
        Text(
            stringResource(if (asked) R.string.amb_request_sent else R.string.amb_one_too),
            fontFamily = BrandFace,
            fontWeight = FontWeight.SemiBold,
            fontSize = 12.sp,
            color = if (asked) brand.inkSoft else brand.moss,
            modifier = tapMod.padding(vertical = 4.dp),
        )
    } else {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            modifier = Modifier.fillMaxWidth().heightIn(min = 46.dp).then(tapMod).padding(horizontal = 14.dp),
        ) {
            Icon(Sym.Verified, null, tint = brand.moss, modifier = Modifier.width(18.dp).size(18.dp))
            Text(
                when {
                    asked -> stringResource(R.string.discover_request_sent)
                    seated -> stringResource(R.string.amb_become_a, place)
                    else -> stringResource(R.string.amb_become_the, place)
                },
                fontFamily = BrandFace,
                fontWeight = FontWeight.Medium,
                fontSize = 15.sp,
                color = brand.ink,
                maxLines = 2,
                modifier = Modifier.weight(1f),
            )
            if (!asked) Icon(Sym.ChevronRight, null, tint = brand.inkSoft.copy(alpha = 0.6f), modifier = Modifier.size(18.dp))
        }
    }
    if (confirming) {
        val close = { confirming = false; sent = false }
        if (sent) {
            BrandSheet(
                title = stringResource(R.string.discover_amb_sent_title),
                icon = Sym.Check,
                message = stringResource(R.string.discover_amb_sent_body) +
                    (host.email?.let { stringResource(R.string.discover_amb_write_to, it) } ?: ""),
                onDismiss = close,
                buttons = listOf(SheetButton(stringResource(R.string.discover_done), SheetKind.PRIMARY, action = close)),
            )
        } else {
            BrandSheet(
                title = if (seated) stringResource(R.string.amb_title_seated, place) else stringResource(R.string.discover_amb_title, place),
                icon = Sym.Verified,
                message = stringResource(R.string.discover_amb_message),
                points = listOf(
                    stringResource(R.string.discover_amb_p1),
                    stringResource(R.string.discover_amb_p2),
                    stringResource(R.string.discover_amb_p3),
                ),
                onDismiss = close,
                buttons = listOf(
                    SheetButton(stringResource(if (sending) R.string.discover_sending else R.string.discover_apply), SheetKind.PRIMARY) {
                        if (sending) return@SheetButton
                        sending = true
                        scope.launch {
                            // A request needs a LIVE session: no token opens the sign-in sheet.
                            val t = host.token()
                            if (t == null) {
                                sending = false
                                confirming = false
                                host.signIn(SignInReason.Ambassador) { confirming = true }
                                return@launch
                            }
                            val ok = AmbassadorAsk.request(place, t)
                            sending = false
                            if (ok) {
                                asked = true
                                sent = true
                            } else {
                                confirming = false
                                failed = true
                            }
                        }
                    },
                    SheetButton(stringResource(R.string.discover_not_now), SheetKind.QUIET, action = close),
                ),
            )
        }
    }
    if (failed) {
        // News is the iPhone's snackbar; one line on the one sheet until Android has a shared one.
        BrandSheet(
            title = stringResource(R.string.discover_amb_failed),
            onDismiss = { failed = false },
            buttons = listOf(SheetButton(stringResource(R.string.discover_done), SheetKind.PRIMARY) { failed = false }),
        )
    }
}

// MARK: - Ancient Trees Plus

/**
 * SWITCHES FROM THE SERVER (Kit/AppSwitches.swift): data/app-switches.json sent
 * in /api/version.json as `switches`; until it answers, everything is ON. Whether
 * this install answered is the one flag kept here ("device" in
 * data/cross-device.json, android:device/plus.answered.v1).
 */
object AppSwitches {
    private const val VERSION = "https://ancienttrees.app/api/version.json"
    private const val ANSWERED = "plus.answered.v1"
    var plusAsk by mutableStateOf(true)
        private set
    /** android_review_question: the question before Google Play's review card (ui/ReviewAsk.kt). */
    var reviewQuestion by mutableStateOf(true)
        private set
    private var answered by mutableStateOf<Boolean?>(null)

    private fun prefs(c: Context) = c.applicationContext.getSharedPreferences("device", Context.MODE_PRIVATE)

    fun showPlus(c: Context): Boolean {
        val a = answered ?: prefs(c).getBoolean(ANSWERED, false).also { answered = it }
        return plusAsk && !a
    }

    fun markPlusAnswered(c: Context) {
        answered = true
        prefs(c).edit().putBoolean(ANSWERED, true).apply()
    }

    /** -plusoff draws the app as a switched-off feed would. */
    suspend fun refresh(args: List<String>) {
        if ("-plusoff" in args) {
            plusAsk = false
            return
        }
        val s = withContext(Dispatchers.IO) {
            runCatching {
                val c = URL(VERSION).openConnection() as HttpURLConnection
                c.connectTimeout = 15_000
                c.readTimeout = 15_000
                try {
                    JSONObject(c.inputStream.bufferedReader().use { it.readText() }).optJSONObject("switches")
                } finally {
                    c.disconnect()
                }
            }.getOrNull()
        } ?: return
        plusAsk = s.optBoolean("plus_ask", true)
        reviewQuestion = s.optBoolean("android_review_question", true)
    }
}

/** Kit/PlusAnswers.swift: one anonymous answer, and "Tell me" on an account. */
object PlusAnswers {
    val options = listOf("walks", "offline", "season", "log")

    suspend fun answer(choices: List<String>, idea: String, other: String, shownOrder: List<String>, city: String, openedFrom: String, lang: String) {
        val body = JSONObject()
            .put("surface", "app")
            .put("lang", lang)
            .put("city", city.take(80))
            .put("opened_from", openedFrom)
            .put("choices", JSONArray(choices))
            .put("idea", idea.trim().take(600))
            .put("shown_order", shownOrder.joinToString(","))
            .put("build", "android")
        // Sent only with "Something else", so an answer without it never depends on the column.
        if ("other" in choices) body.put("other_text", other.trim().take(300))
        Supa.send("/rest/v1/plus_answers", token = null, body = body.toString(), prefer = "return=minimal")
    }

    suspend fun joinWaitlist(token: String): Boolean =
        Supa.send("/rest/v1/plus_waitlist", token = token, body = "{}", prefer = "resolution=ignore-duplicates,return=minimal").ok
}

/** PlusRow: an 18 point icon, 10 to the words, 15 medium, a chevron. */
@Composable
private fun PlusRow(city: String) {
    val brand = Brand.colors
    var asking by remember { mutableStateOf(false) }
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 46.dp)
            .clickable(role = Role.Button) {
                app.ancienttrees.account.Measure.event("plus-open", mapOf("from" to "city"))
                asking = true
            }
            .padding(horizontal = 14.dp)
            .testTag("plus-row"),
    ) {
        Icon(Sym.StarShineFill, null, tint = brand.moss, modifier = Modifier.size(18.dp))
        Text(stringResource(R.string.plus_row), fontFamily = BrandFace, fontWeight = FontWeight.Medium, fontSize = 15.sp, color = brand.ink, modifier = Modifier.weight(1f))
        Icon(Sym.ChevronRight, null, tint = brand.inkSoft.copy(alpha = 0.6f), modifier = Modifier.size(18.dp))
    }
    if (asking) PlusQuestionSheet(city, "city") { asking = false }
}

private enum class PlusStep { IDEA, CHOICE, THANKS, LISTED }

/**
 * The three steps on the one sheet (PlusAsk.swift): the OPEN question first,
 * before any option is shown; ONE choice of up to two, shuffled per person,
 * "Something else" last with its own field; then "Tell me", the only step that
 * needs an account.
 */
@Composable
fun PlusQuestionSheet(city: String, openedFrom: String, onDismiss: () -> Unit) {
    val brand = Brand.colors
    val context = LocalContext.current
    val host = LocalPlaceHost.current
    val scope = rememberCoroutineScope()
    var step by remember { mutableStateOf(PlusStep.IDEA) }
    var idea by remember { mutableStateOf("") }
    var otherText by remember { mutableStateOf("") }
    val choices = remember { mutableStateListOf<String>() }
    val order = remember { PlusAnswers.options.shuffled() }
    var joining by remember { mutableStateOf(false) }
    val labels = mapOf(
        "walks" to stringResource(R.string.plus_opt_walks),
        "offline" to stringResource(R.string.plus_opt_offline),
        "season" to stringResource(R.string.plus_opt_season),
        "log" to stringResource(R.string.plus_opt_log),
        "other" to stringResource(R.string.plus_opt_other),
    )
    LaunchedEffect(Unit) {
        // A sheet no argument can open ships unseen: -pluschoice and -plusthanks.
        val args = (context as? android.app.Activity)?.intent?.getStringArrayExtra("args").orEmpty()
        if ("-pluschoice" in args) step = PlusStep.CHOICE
        if ("-plusthanks" in args) step = PlusStep.THANKS
    }
    fun join() {
        val h = host ?: return
        joining = true
        scope.launch {
            val t = h.token()
            if (t == null) {
                joining = false
                h.signIn(SignInReason.Feedback) { join() }
                return@launch
            }
            val ok = PlusAnswers.joinWaitlist(t)
            joining = false
            if (ok) {
                app.ancienttrees.account.Measure.event("plus-tellme")
                step = PlusStep.LISTED
            }
        }
    }
    when (step) {
        PlusStep.IDEA -> BrandSheet(
            title = stringResource(R.string.plus_title),
            icon = Sym.StarShineFill,
            message = stringResource(R.string.plus_message),
            onDismiss = onDismiss,
            // Skip while the field is empty, so leaving it is plainly allowed; green once there is something.
            buttons = listOf(
                if (idea.isBlank()) SheetButton(stringResource(R.string.plus_skip), SheetKind.QUIET) { step = PlusStep.CHOICE }
                else SheetButton(stringResource(R.string.plus_next), SheetKind.PRIMARY) { step = PlusStep.CHOICE },
            ),
        ) {
            NoteField(idea, { idea = it }, stringResource(R.string.plus_idea_hint), minHeight = 104, tag = "plus-idea")
        }
        PlusStep.CHOICE -> BrandSheet(
            title = stringResource(R.string.plus_choice_title),
            message = stringResource(R.string.plus_pick_two),
            onDismiss = onDismiss,
            buttons = listOf(
                SheetButton(stringResource(R.string.plus_send), SheetKind.PRIMARY) {
                    if (choices.isEmpty()) return@SheetButton
                    val picked = choices.toList()
                    val shown = order
                    val text = idea
                    val other = if ("other" in picked) otherText else ""
                    val lang = java.util.Locale.getDefault().language
                    app.ancienttrees.account.Measure.event("plus-answer", mapOf("choice" to picked.joinToString(",")))
                    scope.launch { PlusAnswers.answer(picked, text, other, shown, city, openedFrom, lang) }
                    // Answered here: the rows go once this sheet closes.
                    AppSwitches.markPlusAnswered(context)
                    step = PlusStep.THANKS
                },
            ),
        ) {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.padding(top = 20.dp)) {
                fun toggle(k: String) {
                    if (k in choices) choices.remove(k) else if (choices.size < 2) choices.add(k)
                }
                for (k in order + "other") {
                    val on = k in choices
                    val full = !on && choices.size >= 2
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                        modifier = Modifier
                            .fillMaxWidth()
                            .alpha(if (full) 0.45f else 1f)
                            .background(if (on) brand.surfaceMuted else Color.Transparent, RoundedCornerShape(14.dp))
                            .border(1.dp, if (on) brand.ink else brand.inkSoft.copy(alpha = 0.2f), RoundedCornerShape(14.dp))
                            .clickable(enabled = !full, role = Role.Checkbox) { toggle(k) }
                            .padding(horizontal = 14.dp, vertical = 13.dp)
                            .testTag("plus-option-$k"),
                    ) {
                        Icon(
                            if (on) Sym.CheckCircleFill else Sym.Circle, null,
                            tint = if (on) brand.moss else brand.inkSoft.copy(alpha = 0.5f), modifier = Modifier.size(20.dp),
                        )
                        Text(labels[k].orEmpty(), fontSize = 15.sp, color = brand.ink, modifier = Modifier.weight(1f))
                    }
                }
                if ("other" in choices) {
                    NoteField(otherText, { otherText = it }, stringResource(R.string.plus_other_hint), minHeight = 0, tag = "plus-other-text")
                }
            }
        }
        PlusStep.THANKS -> BrandSheet(
            title = stringResource(R.string.plus_thanks),
            icon = Sym.Check,
            message = stringResource(R.string.plus_tell_q),
            onDismiss = onDismiss,
            buttons = listOf(
                SheetButton(stringResource(if (joining) R.string.plus_sending else R.string.plus_tell_me), SheetKind.PRIMARY) {
                    val h = host ?: return@SheetButton
                    if (!h.signedIn) h.signIn(SignInReason.Feedback) { join() } else join()
                },
                SheetButton(stringResource(R.string.plus_no_thanks), SheetKind.SECONDARY, action = onDismiss),
            ),
        )
        PlusStep.LISTED -> BrandSheet(
            title = stringResource(R.string.plus_listed),
            icon = Sym.Check,
            onDismiss = onDismiss,
            buttons = listOf(SheetButton(stringResource(R.string.plus_done), SheetKind.PRIMARY, action = onDismiss)),
        )
    }
}

/** The note field's numbers (TreeDetail.swift noteFields): 16 point, the muted ground, radius 14. */
@Composable
private fun NoteField(value: String, onChange: (String) -> Unit, hint: String, minHeight: Int, tag: String) {
    val brand = Brand.colors
    BasicTextField(
        value = value,
        onValueChange = onChange,
        textStyle = sfStyle(fontSize = 16.sp, color = brand.ink),
        cursorBrush = SolidColor(brand.moss),
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = if (minHeight > 0) 20.dp else 0.dp)
            .heightIn(min = minHeight.dp)
            .background(brand.surfaceMuted, RoundedCornerShape(14.dp))
            .padding(horizontal = 14.dp, vertical = 12.dp)
            .testTag(tag),
        decorationBox = { inner ->
            Box {
                if (value.isEmpty()) Text(hint, fontSize = 16.sp, color = brand.inkSoft.copy(alpha = 0.7f))
                inner()
            }
        },
    )
}
