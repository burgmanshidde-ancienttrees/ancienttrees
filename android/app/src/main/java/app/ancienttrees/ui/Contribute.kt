// Sending something back, ported from ios Screens/Contribute.swift: one form,
// three ways in.
//
// - About a tree (the tree page's report menu): no picker and no blank Where,
//   the tree's name and place, and only the field we cannot fill: where it really
//   is (Hidde, 2026-08-25). Kind `correction`, page the tree's url.
// - Feedback (Settings' Send feedback, and Not really on the review question;
//   Hidde, 2026-08-26: "vertel ons welke features je zou willen toevoegen"): no
//   picker, no Where, only the idea. Kind `feedback`, page "app-profile".
// - Otherwise (-contribute): the four kinds as rows with a tick, the way a short
//   choice is listed in Settings, then Where: place, tree, where exactly.
//
// THE ACCOUNT IS ASKED FOR BEFORE THE TYPING (Hidde, 2026-09-24): the sign-in
// sheet opens on arrival; dismissed, the form shows the reason and one button and
// no fields (Google Maps' shape, CONVENTIONS.md "Contributing when you are not
// signed in"). Sending stamps the row with the account, the same `submissions`
// table and the same columns as the iPhone (Kit/Submissions.swift), so the
// pipeline cannot tell the phones apart. Nothing is kept on the device.
//
// The iPhone draws this as a Form in a NavigationStack inside a sheet: Cancel at
// the left of an inline title, grouped white rows on grey, footers in grey.

package app.ancienttrees.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.account.Account
import app.ancienttrees.account.Submission
import app.ancienttrees.feed.Tree
import kotlinx.coroutines.launch

/** Submission.Kind: what the row says it is, in the iPhone's order. */
enum class ContributeKind(val raw: String, val label: Int) {
    TREE("tree", R.string.contribute_kind_tree),
    CITY("city", R.string.contribute_kind_city),
    CORRECTION("correction", R.string.contribute_kind_correction),
    FEEDBACK("feedback", R.string.contribute_kind_feedback),
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ContributeSheet(
    account: Account,
    signedIn: Boolean,
    /** Signed out: the sign-in sheet (SignInSheet(reason: .feedback)). */
    onNeedsSignIn: () -> Unit,
    onDismiss: () -> Unit,
    about: Tree? = null,
    opening: String? = null,
    feedbackMode: Boolean = false,
) {
    val brand = Brand.colors
    val scope = rememberCoroutineScope()
    var kind by remember {
        mutableStateOf(
            when {
                about != null -> ContributeKind.CORRECTION
                feedbackMode -> ContributeKind.FEEDBACK
                else -> ContributeKind.CORRECTION
            },
        )
    }
    var city by remember { mutableStateOf(about?.city.orEmpty()) }
    var tree by remember { mutableStateOf(about?.name.orEmpty()) }
    var where by remember { mutableStateOf("") }
    var why by remember { mutableStateOf(opening?.let { it + "\n" }.orEmpty()) }
    var sending by remember { mutableStateOf(false) }
    var sent by remember { mutableStateOf(false) }
    var failed by remember { mutableStateOf(false) }
    // The gate at the entrance, as the website does on arrival.
    LaunchedEffect(Unit) { if (!signedIn) onNeedsSignIn() }

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true),
        containerColor = brand.surfaceMuted,
    ) {
        Column(
            // Full height, as the iPhone's form sheet (the .large detent of a NavigationStack).
            Modifier.fillMaxWidth().fillMaxHeight().testTag("contribute-sheet")
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 16.dp).padding(bottom = 24.dp).navigationBarsPadding().imePadding(),
        ) {
            // The inline bar: Cancel (Done once sent) at the left, the title centred.
            Row(Modifier.fillMaxWidth().height(44.dp), verticalAlignment = Alignment.CenterVertically) {
                Text(
                    stringResource(if (sent) R.string.done else R.string.cancel),
                    fontSize = 17.sp,
                    color = brand.moss,
                    modifier = Modifier.width(72.dp).clickable(role = Role.Button, onClick = onDismiss),
                )
                Text(
                    stringResource(
                        when {
                            sent -> R.string.sent_title
                            feedbackMode -> R.string.feedback_title
                            else -> R.string.tell_us
                        },
                    ),
                    fontSize = 17.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = brand.ink,
                    textAlign = TextAlign.Center,
                    modifier = Modifier.weight(1f),
                )
                Spacer(Modifier.width(72.dp))
            }
            // The Form's own inset under an inline bar.
            Spacer(Modifier.height(48.dp))
            // iOS 26's grouped rows: 52 tall, the group's corners round at 20.
            val group = Modifier.fillMaxWidth().background(brand.surface, RoundedCornerShape(20.dp))
            val cell = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 15.dp)

            @Composable
            fun Header(text: String) = Text(
                text.uppercase(), fontSize = 13.sp, color = brand.inkSoft,
                modifier = Modifier.padding(start = 16.dp, bottom = 6.dp),
            )

            @Composable
            fun Field(value: String, onChange: (String) -> Unit, hint: String, modifier: Modifier = cell) = Box(modifier) {
                BasicTextField(
                    value, onChange,
                    textStyle = sfStyle(fontSize = 17.sp, color = brand.ink),
                    cursorBrush = SolidColor(brand.moss),
                    modifier = Modifier.fillMaxWidth(),
                )
                if (value.isEmpty()) Text(hint, fontSize = 17.sp, color = brand.inkSoft.copy(alpha = 0.6f))
            }

            @Composable
            fun Divider() = HorizontalDivider(Modifier.padding(start = 16.dp), thickness = 0.5.dp, color = brand.hairline)

            when {
                sent -> Column(group.then(cell), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Icon(Sym.VerifiedFill, null, tint = brand.moss, modifier = Modifier.size(20.dp))
                        Text(stringResource(R.string.thank_you), fontSize = 17.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
                    }
                    Text(stringResource(R.string.we_read_every_tip), fontSize = 13.sp, color = brand.inkSoft)
                }
                // Two rows of one section, as the iPhone's Form draws them: the reason, then the button.
                !signedIn -> Column(group) {
                    Text(stringResource(R.string.report_needs_account), fontSize = 13.sp, color = brand.inkSoft, modifier = cell)
                    Divider()
                    Text(
                        stringResource(R.string.sign_in),
                        fontSize = 16.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = brand.moss,
                        modifier = Modifier.fillMaxWidth().heightIn(min = 52.dp)
                            .clickable(role = Role.Button, onClick = onNeedsSignIn).testTag("contribute-signin")
                            .then(cell),
                    )
                }
                else -> {
                    if (about != null) {
                        Header(stringResource(R.string.about_this_tree))
                        Column(group.then(cell), verticalArrangement = Arrangement.spacedBy(3.dp)) {
                            Text(about.name, fontSize = 16.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
                            Text(about.city, fontSize = 13.sp, color = brand.inkSoft)
                        }
                        Spacer(Modifier.height(20.dp))
                        Column(group) { Field(where, { where = it }, stringResource(R.string.where_really)) }
                        Spacer(Modifier.height(20.dp))
                    } else if (!feedbackMode) {
                        // Four choices as four rows with a tick.
                        Column(group) {
                            ContributeKind.entries.forEachIndexed { i, k ->
                                if (i > 0) Divider()
                                Row(
                                    Modifier.fillMaxWidth().heightIn(min = 52.dp)
                                        .clickable(role = Role.RadioButton) { kind = k }
                                        .padding(horizontal = 16.dp).testTag("contribute-kind-${k.raw}"),
                                    verticalAlignment = Alignment.CenterVertically,
                                ) {
                                    Text(stringResource(k.label), fontSize = 17.sp, color = brand.ink, modifier = Modifier.weight(1f))
                                    if (kind == k) Icon(Sym.Check, null, tint = brand.moss, modifier = Modifier.size(18.dp))
                                }
                            }
                        }
                        Spacer(Modifier.height(20.dp))
                        Header(stringResource(R.string.contribute_where))
                        Column(group) {
                            Field(city, { city = it }, stringResource(R.string.contribute_place_or_city))
                            Divider()
                            Field(tree, { tree = it }, stringResource(R.string.contribute_which_tree))
                            Divider()
                            Field(where, { where = it }, stringResource(R.string.contribute_where_exactly))
                        }
                        Spacer(Modifier.height(20.dp))
                    }
                    if (feedbackMode) Header(stringResource(R.string.feedback_header))
                    Column(group) {
                        Field(
                            why, { why = it },
                            stringResource(if (feedbackMode) R.string.feedback_placeholder else R.string.what_should_we_know),
                            cell.heightIn(min = 110.dp),
                        )
                    }
                    Text(
                        stringResource(R.string.nobody_sees), fontSize = 13.sp, color = brand.inkSoft,
                        modifier = Modifier.padding(start = 16.dp, top = 6.dp, end = 16.dp),
                    )
                    Spacer(Modifier.height(20.dp))
                    val ready = !sending && why.isNotEmpty()
                    Row(
                        group.clickable(enabled = ready, role = Role.Button) {
                            sending = true
                            failed = false
                            scope.launch {
                                val ok = Submission.send(
                                    kind = kind.raw, city = city, tree = tree, locationHint = where, why = why,
                                    page = about?.url ?: if (feedbackMode) "app-profile" else null,
                                    token = account.fresh()?.accessToken,
                                )
                                sending = false
                                if (ok) sent = true else failed = true
                            }
                        }.then(cell).testTag("contribute-send"),
                        horizontalArrangement = Arrangement.Center,
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        if (sending) {
                            CircularProgressIndicator(Modifier.size(16.dp), color = brand.inkSoft, strokeWidth = 2.dp)
                            Spacer(Modifier.width(6.dp))
                        }
                        Text(
                            stringResource(if (sending) R.string.sending else R.string.send),
                            fontSize = 17.sp,
                            color = if (ready) brand.moss else brand.inkSoft.copy(alpha = 0.5f),
                        )
                    }
                    if (failed) {
                        Text(
                            stringResource(R.string.note_failed), fontSize = 13.sp, color = brand.dangerText,
                            modifier = Modifier.padding(start = 16.dp, top = 6.dp),
                        )
                    }
                }
            }
        }
    }
}
