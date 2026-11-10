// The one sign-in surface, a sheet from wherever the moment happened: ported from
// ios Screens/SignIn.swift and GoogleButton.swift. The app's own icon, a title and
// one line, the sign-in pills of one size 10 apart, a red line when something went
// wrong, and the terms in one line. The cross in the corner closes it.
//
// The iPhone's three pills in its order: the dark "Continue with Apple" first, then
// Google's cream pill, then email. Apple and Google open in a Custom Tab and come
// back on ancienttrees://auth-callback (Account.kt), so no sign-in library is
// added; the iPhone's Apple sheet is Apple's own, which Android does not have.

package app.ancienttrees.ui

import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.LocalContentColor
import androidx.compose.runtime.CompositionLocalProvider
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
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.PathFillType
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.graphics.vector.PathParser
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.LinkAnnotation
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextLinkStyles
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.withLink
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.account.Account
import app.ancienttrees.account.Problem
import app.ancienttrees.account.SignIn
import kotlinx.coroutines.launch

/** Why the sheet opened (Account.swift SignInReason): the headline and the line under it. */
sealed class SignInReason {
    data object General : SignInReason()
    data class KeepTree(val name: String) : SignInReason()
    data object Feedback : SignInReason()
    data object Ambassador : SignInReason()
    data class Follow(val name: String) : SignInReason()
}

@Composable
private fun headline(r: SignInReason): String = when (r) {
    SignInReason.General -> stringResource(R.string.signin_title)
    is SignInReason.KeepTree -> stringResource(R.string.signin_keep)
    SignInReason.Feedback -> stringResource(R.string.signin_feedback)
    SignInReason.Ambassador -> stringResource(R.string.signin_ambassador)
    is SignInReason.Follow -> stringResource(R.string.signin_follow, r.name)
}

@Composable
private fun detail(r: SignInReason): String = when (r) {
    SignInReason.General, is SignInReason.KeepTree -> stringResource(R.string.signin_sub)
    SignInReason.Feedback -> stringResource(R.string.signin_feedback_sub)
    SignInReason.Ambassador -> stringResource(R.string.signin_ambassador_sub)
    is SignInReason.Follow -> stringResource(R.string.signin_follow_sub)
}

@Composable
private fun problemText(p: Problem): String = stringResource(
    when (p) {
        Problem.NOT_AN_EMAIL -> R.string.problem_not_email
        Problem.COULD_NOT_SEND -> R.string.problem_send
        Problem.LINK_USED -> R.string.problem_link
        Problem.GOOGLE_OFF -> R.string.problem_google
        Problem.APPLE_OFF -> R.string.problem_apple
    },
)

/** The older call: a tree's name means the person was keeping that tree. */
@Composable
fun SignInSheet(account: Account, treeName: String?, onDismiss: () -> Unit) =
    SignInSheet(account, if (treeName != null) SignInReason.KeepTree(treeName) else SignInReason.General, onDismiss)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SignInSheet(account: Account, reason: SignInReason, onDismiss: () -> Unit) {
    val brand = Brand.colors
    ModalBottomSheet(
        onDismissRequest = { account.dismissProblem(); onDismiss() },
        sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true),
        // SOLID, not glass, and the system's own ground (SignIn.swift presentationBackground).
        containerColor = brand.ground,
        modifier = Modifier.testTag("signin-sheet"),
    ) {
        PlainText { Box {
            Column(
                verticalArrangement = Arrangement.spacedBy(18.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .verticalScroll(rememberScrollState())
                    .padding(horizontal = 22.dp)
                    .padding(top = 24.dp, bottom = 16.dp)
                    .navigationBarsPadding(),
            ) {
                when (val s = account.state) {
                    is SignIn.LinkSent -> CheckYourEmail(account, s.email)
                    is SignIn.SignedIn -> Box(Modifier.fillMaxWidth().padding(vertical = 30.dp), contentAlignment = Alignment.Center) {
                        CircularProgressIndicator(color = brand.inkSoft)
                    }
                    else -> Ask(account, reason)
                }
            }
            SheetCloseButton({ account.dismissProblem(); onDismiss() }, Modifier.align(Alignment.TopEnd))
        } }
    }
}

/** AllTrails' and Airbnb's sheet: the icon, a title and a line, the pills, the terms. */
@Composable
private fun Ask(account: Account, reason: SignInReason) {
    val context = LocalContext.current
    val brand = Brand.colors
    val scope = rememberCoroutineScope()
    var emailOpen by remember { mutableStateOf(false) }
    var address by remember { mutableStateOf("") }
    val working = account.state is SignIn.Working
    val focus = remember { FocusRequester() }

    Column(verticalArrangement = Arrangement.spacedBy(24.dp)) {
        // THE HEADER: the app's own icon, the brand face at 26, centred.
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(8.dp),
            modifier = Modifier.fillMaxWidth().padding(horizontal = 22.dp).padding(top = 6.dp, bottom = 4.dp),
        ) {
            AppIconTile()
            Spacer(Modifier.height(8.dp))
            Text(
                headline(reason), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 26.sp,
                lineHeight = 31.sp, color = brand.ink, textAlign = TextAlign.Center,
            )
            Text(detail(reason), fontSize = 15.sp, color = brand.inkSoft, textAlign = TextAlign.Center)
        }
        // 10 apart, where Hidde stopped complaining (SignIn.swift, 2026-10-09).
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            // A custom Sign in with Apple button, as the iPhone's (SignIn.swift; Apple's HIG
            // allows their logo, "Continue with Apple", black or white): loud, first.
            SignInPill(stringResource(R.string.signin_apple), loud = true, enabled = !working, tag = "signin-apple",
                mark = { Icon(AppleLogo, null, Modifier.size(18.dp), tint = LocalContentColor.current) }) { account.openApple(context) }
            SignInPill(stringResource(R.string.signin_google), loud = false, enabled = !working, tag = "signin-google",
                mark = { Image(GoogleG, null, Modifier.size(18.dp)) }) { account.openGoogle(context) }
            if (!emailOpen) {
                SignInPill(stringResource(R.string.signin_email), loud = false, enabled = true, tag = "signin-email") {
                    emailOpen = true
                }
            } else {
                LaunchedEffect(Unit) { runCatching { focus.requestFocus() } }
                val send = { scope.launch { account.sendLink(address) }; Unit }
                BasicTextField(
                    value = address,
                    onValueChange = { address = it },
                    singleLine = true,
                    textStyle = sfStyle(fontSize = 17.sp, color = brand.ink),
                    cursorBrush = SolidColor(brand.moss),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email, imeAction = ImeAction.Go, autoCorrectEnabled = false),
                    keyboardActions = KeyboardActions(onGo = { send() }),
                    modifier = Modifier.fillMaxWidth().focusRequester(focus),
                    decorationBox = { inner ->
                        Box(
                            Modifier.fillMaxWidth().height(52.dp).background(brand.surfaceMuted, RoundedCornerShape(50)).padding(horizontal = 18.dp),
                            contentAlignment = Alignment.CenterStart,
                        ) {
                            if (address.isEmpty()) Text(stringResource(R.string.signin_placeholder), fontSize = 17.sp, color = brand.inkSoft.copy(alpha = 0.7f))
                            inner()
                        }
                    },
                )
                val can = !working && '@' in address
                Box(
                    Modifier.fillMaxWidth().height(52.dp).clip(RoundedCornerShape(50)).background(brand.moss.copy(alpha = if (can) 1f else 0.5f))
                        .clickable(enabled = can, role = Role.Button) { send() },
                    contentAlignment = Alignment.Center,
                ) {
                    if (working) CircularProgressIndicator(color = Color.White, strokeWidth = 2.dp, modifier = Modifier.size(18.dp))
                    else Text(stringResource(R.string.signin_send), color = brand.onMoss, fontSize = 17.sp, fontWeight = FontWeight.SemiBold)
                }
            }
        }
        account.problem?.let { Text(problemText(it), fontSize = 13.sp, color = Color(0xFFFF3B30)) }
        Terms()
    }
}

/** The privacy line is part of the offer: one line, links inline, centred. */
@Composable
private fun Terms() {
    val brand = Brand.colors
    val links = TextLinkStyles(SpanStyle(color = brand.moss))
    val text = buildAnnotatedString {
        append(stringResource(R.string.signin_terms_1))
        withLink(LinkAnnotation.Url("https://ancienttrees.app/terms", links)) { append(stringResource(R.string.signin_terms_link)) }
        append(stringResource(R.string.signin_terms_2))
        withLink(LinkAnnotation.Url("https://ancienttrees.app/privacy", links)) { append(stringResource(R.string.signin_privacy_link)) }
        append(stringResource(R.string.signin_terms_3))
    }
    Text(text, fontSize = 13.sp, color = brand.inkSoft, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth())
}

/** "Check your email": the same header as the first step, then Open Gmail or Mail and Send another link. */
@Composable
private fun CheckYourEmail(account: Account, to: String) {
    val context = LocalContext.current
    val brand = Brand.colors
    val scope = rememberCoroutineScope()
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp),
        modifier = Modifier.fillMaxWidth().padding(horizontal = 22.dp).padding(top = 6.dp),
    ) {
        SheetIconTile(Sym.MailFill)
        Spacer(Modifier.height(8.dp))
        Text(
            stringResource(R.string.signin_check_title), fontFamily = BrandFace, fontWeight = FontWeight.Bold,
            fontSize = 26.sp, lineHeight = 31.sp, color = brand.ink, textAlign = TextAlign.Center,
        )
        Text(stringResource(R.string.signin_check_sub), fontSize = 15.sp, color = brand.inkSoft, textAlign = TextAlign.Center)
    }
    account.problem?.let { Text(problemText(it), fontSize = 13.sp, color = Color(0xFFFF3B30)) }
    Column(verticalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.padding(top = 4.dp)) {
        mailApp(context, to)?.let { (label, open) ->
            SheetButtonView(SheetButton(stringResource(label), SheetKind.PRIMARY) { open() })
        }
        SheetButtonView(SheetButton(stringResource(R.string.signin_again), SheetKind.SECONDARY) {
            scope.launch { account.sendLink(to) }
        })
    }
}

/**
 * The mail app to open, chosen by the ADDRESS rather than by what is installed
 * (Hidde, 2026-10-14): a Gmail address opens Gmail, anything else the phone's
 * mail app. Null when nothing on the phone opens mail.
 */
private fun mailApp(context: Context, address: String): Pair<Int, () -> Unit>? {
    val pm = context.packageManager
    val a = address.lowercase()
    if (a.endsWith("@gmail.com") || a.endsWith("@googlemail.com")) {
        pm.getLaunchIntentForPackage("com.google.android.gm")?.let { i ->
            return R.string.signin_open_gmail to { runCatching { context.startActivity(i) } }
        }
    }
    val mail = Intent.makeMainSelectorActivity(Intent.ACTION_MAIN, Intent.CATEGORY_APP_EMAIL).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    if (mail.resolveActivity(pm) != null) return R.string.signin_open_mail to { runCatching { context.startActivity(mail) } }
    return null
}

/** The icon the home screen shows, 56 with radius 14 and a hairline, never a lookalike. */
@Composable
fun AppIconTile() {
    val brand = Brand.colors
    val shape = RoundedCornerShape(14.dp)
    Image(
        painterResource(R.mipmap.ic_launcher), null,
        Modifier.size(56.dp).clip(shape).border(1.dp, brand.ink.copy(alpha = 0.1f), shape),
    )
}

/**
 * GoogleButton.swift's SignInPill: 48 tall, the mark 18 wide at the leading edge
 * 22 in, the words centred on the whole pill in the brand face. Loud is the
 * website's dark pill; quiet is cream.
 */
@Composable
fun SignInPill(
    title: String,
    loud: Boolean,
    enabled: Boolean,
    tag: String,
    mark: (@Composable () -> Unit)? = null,
    onClick: () -> Unit,
) {
    val brand = Brand.colors
    val dark = brand.ground != LightBrand.ground
    val bg = if (loud) (if (dark) Color.White else Color(0xFF1B2416)) else brand.creamDark
    val fg = if (loud) (if (dark) Color.Black else Color.White) else brand.ink
    Box(
        Modifier
            .fillMaxWidth()
            .heightIn(min = 48.dp)
            .clip(RoundedCornerShape(50))
            .background(bg)
            .clickable(enabled = enabled, role = Role.Button, onClick = onClick)
            .testTag(tag),
        contentAlignment = Alignment.Center,
    ) {
        Text(
            title, fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 17.sp, color = fg, maxLines = 1,
            modifier = Modifier.padding(horizontal = 50.dp),
        )
        if (mark != null) Box(Modifier.align(Alignment.CenterStart).padding(start = 22.dp).size(18.dp)) {
            CompositionLocalProvider(LocalContentColor provides fg) { mark() }
        }
    }
}

/** Apple's logo, the same paths the website's Apple button draws (SignInPanel.astro), on a 24 grid. */
private val AppleLogo: ImageVector by lazy {
    fun p(d: String) = PathParser().parsePathString(d).toNodes()
    ImageVector.Builder("AppleLogo", 18.dp, 18.dp, 24f, 24f).apply {
        addPath(p("M17.05 12.04c-.02-2.4 1.96-3.55 2.05-3.6-1.12-1.64-2.86-1.86-3.48-1.89-1.48-.15-2.89.87-3.64.87-.75 0-1.91-.85-3.14-.83-1.61.02-3.1.94-3.93 2.38-1.68 2.91-.43 7.22 1.2 9.58.8 1.16 1.75 2.46 3 2.41 1.21-.05 1.66-.78 3.12-.78 1.46 0 1.87.78 3.14.76 1.3-.02 2.12-1.18 2.91-2.34.92-1.34 1.3-2.64 1.32-2.71-.03-.01-2.53-.97-2.55-3.85z"),
            fill = SolidColor(Color.Black))
        addPath(p("M14.72 4.7c.66-.8 1.11-1.92.99-3.03-.95.04-2.11.63-2.8 1.43-.61.71-1.15 1.85-1.01 2.94 1.07.08 2.15-.54 2.82-1.34z"),
            fill = SolidColor(Color.Black))
    }.build()
}

/** The four-colour G, Google's own asset geometry (GoogleButton.swift), in an 18 x 18 box. */
private val GoogleG: ImageVector by lazy {
    fun p(d: String) = PathParser().parsePathString(d).toNodes()
    ImageVector.Builder("GoogleG", 18.dp, 18.dp, 18f, 18f).apply {
        addPath(p("M17.64 9.2045c0-.6381-.0573-1.2518-.1636-1.8409H9v3.4814h4.8436c-.2086 1.125-.8427 2.0782-1.7959 2.7164v2.2581h2.9087c1.7018-1.5668 2.6836-3.874 2.6836-6.615z"),
            fill = SolidColor(Color(0xFF4285F4)), pathFillType = PathFillType.NonZero)
        addPath(p("M9 18c2.43 0 4.4673-.806 5.9564-2.1805l-2.9087-2.2581c-.8059.54-1.8368.859-3.0477.859-2.344 0-4.3282-1.5831-5.036-3.7104H.9574v2.3318C2.4382 15.9832 5.4818 18 9 18z"),
            fill = SolidColor(Color(0xFF34A853)))
        addPath(p("M3.964 10.71c-.18-.54-.2822-1.1168-.2822-1.71s.1023-1.17.2823-1.71V4.9582H.9573A8.9965 8.9965 0 0 0 0 9c0 1.4523.3477 2.8268.9573 4.0418L3.964 10.71z"),
            fill = SolidColor(Color(0xFFFBBC05)))
        addPath(p("M9 3.5795c1.3214 0 2.5077.4541 3.4405 1.346l2.5813-2.5814C13.4632.8918 11.426 0 9 0 5.4818 0 2.4382 2.0168.9573 4.9582L3.964 7.29C4.6718 5.1627 6.656 3.5795 9 3.5795z"),
            fill = SolidColor(Color(0xFFEA4335)))
    }.build()
}

/** For a link in plain text elsewhere (Settings' rows): open in the browser. */
fun openWeb(context: Context, url: String) {
    runCatching { context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url))) }
}
