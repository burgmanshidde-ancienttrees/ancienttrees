// Settings, ported from ios Screens/Profile.swift: pushed from the gear on My
// trees, in the order every app people know keeps it. Your card, Preferences,
// Help, About, then Account (Sign out, Delete account) last, and the version
// under everything. No screen title in the body: the bar says Settings.
//
// What Android forces (data/android-parity.json): Directions offers Google Maps
// and Another maps app (no Apple Maps on Android, ui/Directions.kt); Rate the app
// opens the Play Store rather than the App Store.

package app.ancienttrees.ui

import android.content.Context
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.RowScope
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.account.Account
import app.ancienttrees.account.Profiles
import app.ancienttrees.feed.Geo
import kotlinx.coroutines.launch

/** Kilometres or miles, a device setting (data/cross-device.json "units"); unset follows the phone's region. */
object Units {
    private fun prefs(c: Context) = c.applicationContext.getSharedPreferences("settings", Context.MODE_PRIVATE)
    fun miles(c: Context): Boolean = prefs(c).getString("units", null)?.let { it == "mi" }
        ?: Geo.milesFor(java.util.Locale.getDefault().country)
    fun set(c: Context, miles: Boolean) = prefs(c).edit().putString("units", if (miles) "mi" else "km").apply()
}

/** What Settings needs from the app around it. */
class SettingsHost(
    val account: Account,
    val profiles: Profiles,
    /** Signed in, by the server's word (or the sweep's -signed-in stand-in). */
    val signedIn: Boolean,
    val email: String?,
    val locationAllowed: Boolean,
    val locationRefused: Boolean,
    val askLocation: () -> Unit,
    val signIn: () -> Unit,
    val editProfile: () -> Unit,
    val openPrivacy: () -> Unit,
    val signedOut: () -> Unit,
    /** Sign in for the feedback form (SignInSheet(reason: .feedback)). */
    val signInForFeedback: () -> Unit = signIn,
    /** The launch arguments: -contribute and -feedback open the form (Profile.swift launchSheet). */
    val args: List<String> = emptyList(),
)

@Composable
fun SettingsScreen(host: SettingsHost, onBack: () -> Unit, askSignOut: Boolean = false) = PlainText {
    SettingsInner(host, onBack, askSignOut)
}

@Composable
private fun SettingsInner(host: SettingsHost, onBack: () -> Unit, askSignOut: Boolean) {
    val brand = Brand.colors
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var refused by remember { mutableStateOf(false) }
    var showingLegal by remember { mutableStateOf(false) }
    var showingDelete by remember { mutableStateOf(false) }
    var confirmingSignOut by remember { mutableStateOf(askSignOut) }
    var signingOut by remember { mutableStateOf(false) }
    var miles by remember { mutableStateOf(Units.miles(context)) }
    var contributing by remember { mutableStateOf("-contribute" in host.args) }
    var givingFeedback by remember { mutableStateOf("-feedback" in host.args) }
    var directionsApp by remember { mutableStateOf(Directions.preferred(context)) }
    // -plusask opens the Plus question here (Profile.swift launchSheet).
    var askingPlus by remember { mutableStateOf("-plusask" in host.args) }
    // "Tell me" signed out: the sign-in sheet, then back to the step (PlusAsk.swift
    // onDismiss). Held only while this screen is open; nothing is pressed for them.
    var afterSignIn by remember { mutableStateOf<(() -> Unit)?>(null) }
    LaunchedEffect(host.signedIn) {
        if (host.signedIn) afterSignIn?.let { afterSignIn = null; it() }
    }

    Column(Modifier.fillMaxSize().background(brand.ground).testTag("settings")) {
        PushedBar(stringResource(R.string.settings), onBack)
        Column(
            verticalArrangement = Arrangement.spacedBy(18.dp),
            modifier = Modifier.fillMaxWidth().verticalScroll(rememberScrollState()).padding(horizontal = 16.dp).padding(top = 6.dp),
        ) {
            Identity(host)

            // PREFERENCES: Distances, Location, Privacy settings.
            Group(stringResource(R.string.settings_preferences)) {
                var menu by remember { mutableStateOf(false) }
                Box {
                    SettingsRow(Sym.Straighten, stringResource(R.string.settings_distances),
                        value = stringResource(if (miles) R.string.units_miles else R.string.units_km),
                        trailing = Sym.UnfoldMore) { menu = true }
                    DropdownMenu(expanded = menu, onDismissRequest = { menu = false }, modifier = Modifier.background(brand.surface)) {
                        for (m in listOf(false, true)) {
                            DropdownMenuItem(
                                text = { Text(stringResource(if (m) R.string.units_miles else R.string.units_km), color = brand.ink) },
                                onClick = { Units.set(context, m); miles = m; menu = false },
                            )
                        }
                    }
                }
                RowDivider(48.dp)
                // DIRECTIONS: which maps app Take me there opens, asked once on the
                // first tap and changed here (Profile.swift, Hidde 2026-08-28). The two
                // apps and nothing else: no "Ask again" (Hidde, 2026-08-29).
                var dirMenu by remember { mutableStateOf(false) }
                Box {
                    SettingsRow(Sym.TurnRight, stringResource(R.string.settings_directions),
                        value = directionsApp?.label(context) ?: stringResource(R.string.directions_ask_each),
                        trailing = Sym.UnfoldMore, tag = "profile-directions") { dirMenu = true }
                    DropdownMenu(expanded = dirMenu, onDismissRequest = { dirMenu = false }, modifier = Modifier.background(brand.surface)) {
                        for (a in Directions.MapsApp.entries) {
                            DropdownMenuItem(
                                text = { Text(a.label(context), color = brand.ink) },
                                onClick = { Directions.setPreferred(context, a); directionsApp = a; dirMenu = false },
                            )
                        }
                    }
                }
                RowDivider(48.dp)
                // LOCATION: On or Off; a tap asks when nothing was asked, opens the
                // recovery sheet after a no, and the system's page when it is on.
                SettingsRow(
                    if (host.locationAllowed) Sym.NearMe else Sym.NearMeDisabled,
                    stringResource(R.string.settings_location),
                    value = stringResource(if (host.locationAllowed) R.string.settings_on else R.string.settings_off),
                    tag = "profile-location",
                ) {
                    when {
                        host.locationAllowed -> openAppSettings(context)
                        host.locationRefused -> refused = true
                        else -> host.askLocation()
                    }
                }
                // PRIVACY SETTINGS, only once the server has said whether the profile is public.
                val isPublic = host.profiles.myPublic
                if (host.signedIn && isPublic != null) {
                    RowDivider(48.dp)
                    SettingsRow(Sym.Lock, stringResource(R.string.privacy_settings),
                        value = stringResource(if (isPublic) R.string.privacy_public else R.string.privacy_only_me),
                        tag = "profile-privacy") { host.openPrivacy() }
                }
            }

            // HELP: feedback and a rating.
            Group(stringResource(R.string.settings_help)) {
                // THE PLUS QUESTION (Profile.swift helpCard; Hidde, 2026-11-04): a
                // row, the way a promise belongs in Settings (2026-08-25), first in
                // Help because it asks for help choosing. The sheet is the city's
                // (PlaceBox.kt PlusQuestionSheet, PlusAsk.swift); the row goes once
                // this install answered or the server's switch is off (AppSwitches).
                if (AppSwitches.showPlus(context)) {
                    SettingsRow(Sym.StarShineFill, stringResource(R.string.plus_title), tag = "profile-plus") {
                        app.ancienttrees.account.Measure.event("plus-open", mapOf("from" to "settings"))
                        askingPlus = true
                    }
                    RowDivider(48.dp)
                }
                SettingsRow(Sym.Chat, stringResource(R.string.settings_feedback), tag = "profile-feedback") {
                    givingFeedback = true
                }
                RowDivider(48.dp)
                LinkRow(Sym.Star, stringResource(R.string.settings_rate), stringResource(R.string.settings_rate_sub)) {
                    openWeb(context, "https://play.google.com/store/apps/details?id=" + context.packageName)
                }
            }

            // ABOUT: Privacy, Terms, Sources.
            Group(stringResource(R.string.settings_about)) {
                LinkRow(Sym.Lock, stringResource(R.string.settings_privacy)) { openWeb(context, "https://ancienttrees.app/privacy") }
                RowDivider(48.dp)
                LinkRow(Sym.Draft, stringResource(R.string.settings_terms)) { openWeb(context, "https://ancienttrees.app/terms") }
                RowDivider(48.dp)
                SettingsRow(Sym.Description, stringResource(R.string.settings_sources)) { showingLegal = true }
            }

            // ACCOUNT: Sign out, then Delete account, grey, opening the screen that explains.
            if (host.signedIn) {
                Group(stringResource(R.string.account)) {
                    PlainRow(stringResource(R.string.sign_out), brand.ink, chevron = false, tag = "settings-signout") { confirmingSignOut = true }
                    RowDivider(16.dp)
                    PlainRow(stringResource(R.string.delete_account), brand.inkSoft, chevron = true, tag = "settings-account") { showingDelete = true }
                }
            }

            Text(
                versionLine(context),
                fontSize = 11.sp, color = brand.inkSoft.copy(alpha = 0.8f), textAlign = TextAlign.Center,
                modifier = Modifier.fillMaxWidth().padding(top = 4.dp).testTag("build-line"),
            )
            Spacer(Modifier.height(80.dp))
        }
    }

    if (refused) PermissionRecovery(Permission.LOCATION, onDismiss = { refused = false })
    if (showingLegal) SourcesSheet { showingLegal = false }
    if (contributing || givingFeedback) {
        ContributeSheet(
            host.account, host.signedIn,
            onNeedsSignIn = host.signInForFeedback,
            onDismiss = { contributing = false; givingFeedback = false },
            feedbackMode = givingFeedback,
        )
    }
    if (askingPlus) {
        CompositionLocalProvider(
            LocalPlaceHost provides PlaceHost(
                signedIn = host.signedIn,
                email = host.email,
                token = { host.account.fresh()?.accessToken },
                signIn = { _, then ->
                    afterSignIn = then
                    host.signInForFeedback()
                },
                openPerson = { },
                myPlaces = emptyList(),
            ),
        ) {
            PlusQuestionSheet(city = "", openedFrom = "settings") { askingPlus = false }
        }
    }
    if (showingDelete) DeleteAccountSheet(host, onDismiss = { showingDelete = false })
    if (confirmingSignOut) {
        BrandSheet(
            title = stringResource(R.string.sign_out_title),
            message = stringResource(R.string.sign_out_body),
            onDismiss = { confirmingSignOut = false },
            buttons = listOf(
                SheetButton(stringResource(R.string.sign_out), SheetKind.DESTRUCTIVE) {
                    confirmingSignOut = false
                    // NOTHING IS AWAITED BEFORE THE DOOR SHUTS (Profile.swift signOutNow).
                    if (!signingOut) {
                        signingOut = true
                        host.profiles.forgetLocally()
                        host.signedOut()
                        scope.launch { host.account.signOut(); signingOut = false }
                    }
                },
                SheetButton(stringResource(R.string.cancel), SheetKind.SECONDARY) { confirmingSignOut = false },
            ),
        )
    }
}

/** Your card: the initial and your name and address, or Sign in with the one prompt line. */
@Composable
private fun Identity(host: SettingsHost) {
    val brand = Brand.colors
    Row(
        horizontalArrangement = Arrangement.spacedBy(14.dp),
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .fillMaxWidth()
            .brandCard()
            .clickable(role = Role.Button) { if (host.signedIn) host.editProfile() else host.signIn() }
            .padding(16.dp)
            .testTag("profile-signin"),
    ) {
        Box(Modifier.size(56.dp).background(brand.surfaceMuted, CircleShape), contentAlignment = Alignment.Center) {
            if (host.signedIn) {
                Text((host.email ?: "?").take(1).uppercase(), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 24.sp, color = brand.moss)
            } else {
                Icon(Sym.Person, null, tint = brand.inkSoft, modifier = Modifier.size(28.dp))
            }
        }
        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(3.dp)) {
            if (host.signedIn) {
                Text(
                    host.profiles.me?.displayName?.takeIf { it.isNotEmpty() } ?: host.email?.substringBefore("@") ?: stringResource(R.string.signed_in),
                    fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 19.sp, color = brand.ink, maxLines = 1, overflow = TextOverflow.Ellipsis,
                )
                host.email?.let { Text(it, fontSize = 13.sp, color = brand.inkSoft, maxLines = 1, overflow = TextOverflow.Ellipsis) }
            } else {
                Text(stringResource(R.string.settings_sign_in), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 18.sp, color = brand.ink)
                // .footnote: its 18 between lines, as the iPhone's two lines (33.7).
                Text(stringResource(R.string.signin_prompt), fontSize = 13.sp, lineHeight = 18.sp, color = brand.inkSoft)
            }
        }
        Icon(Sym.ChevronRight, null, tint = brand.inkSoft.copy(alpha = 0.6f), modifier = Modifier.size(18.dp))
    }
}

/** Style.swift brandCard: surface, radius 12, a one point hairline. */
@Composable
fun Modifier.brandCard(radius: Dp = 12.dp): Modifier {
    val brand = Brand.colors
    val shape = RoundedCornerShape(radius)
    return this.background(brand.surface, shape).border(1.dp, brand.hairline, shape).clip(shape)
}

@Composable
private fun Group(title: String, content: @Composable ColumnScope.() -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Eyebrow(title)
        Column(Modifier.fillMaxWidth().brandCard(), content = content)
    }
}

@Composable
private fun RowDivider(inset: Dp) = HorizontalDivider(Modifier.padding(start = inset), thickness = 0.5.dp, color = Brand.colors.hairline)

/** One settings row, 48 high: the icon 20 wide in moss, the title, a value, the chevron. */
@Composable
private fun SettingsRow(
    icon: ImageVector,
    title: String,
    value: String? = null,
    trailing: ImageVector = Sym.ChevronRight,
    tag: String? = null,
    onClick: () -> Unit,
) {
    val brand = Brand.colors
    RowFrame(onClick, tag) {
        Icon(icon, null, tint = brand.moss, modifier = Modifier.size(20.dp))
        Text(title, fontSize = 16.sp, color = brand.ink, modifier = Modifier.weight(1f))
        value?.let { Text(it, fontSize = 16.sp, color = brand.inkSoft) }
        Icon(trailing, null, tint = brand.inkSoft, modifier = Modifier.size(16.dp))
    }
}

/** A row that leaves the app: the arrow up and to the right, a subtitle when it says why. */
@Composable
private fun LinkRow(icon: ImageVector, title: String, subtitle: String? = null, onClick: () -> Unit) {
    val brand = Brand.colors
    RowFrame(onClick, null, vertical = if (subtitle == null) 0.dp else 10.dp) {
        Icon(icon, null, tint = brand.moss, modifier = Modifier.size(20.dp))
        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
            Text(title, fontSize = 16.sp, color = brand.ink)
            subtitle?.let { Text(it, fontSize = 13.sp, color = brand.inkSoft) }
        }
        Icon(Sym.NorthEast, null, tint = brand.inkSoft.copy(alpha = 0.6f), modifier = Modifier.size(14.dp))
    }
}

@Composable
private fun PlainRow(title: String, color: androidx.compose.ui.graphics.Color, chevron: Boolean, tag: String, onClick: () -> Unit) {
    val brand = Brand.colors
    RowFrame(onClick, tag) {
        Text(title, fontSize = 16.sp, color = color, modifier = Modifier.weight(1f))
        if (chevron) Icon(Sym.ChevronRight, null, tint = brand.inkSoft.copy(alpha = 0.6f), modifier = Modifier.size(16.dp))
    }
}

@Composable
private fun RowFrame(onClick: () -> Unit, tag: String?, vertical: Dp = 0.dp, content: @Composable RowScope.() -> Unit) {
    Row(
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 48.dp)
            .clickable(role = Role.Button, onClick = onClick)
            .padding(horizontal = 16.dp, vertical = vertical)
            .let { if (tag != null) it.testTag(tag) else it },
        content = content,
    )
}

/** A pushed page's bar: back on the left and the title inline in the middle. */
@Composable
fun PushedBar(title: String, onBack: () -> Unit, trailing: (@Composable () -> Unit)? = null) {
    val brand = Brand.colors
    // iOS 26's inline navigation bar is 54 tall, its back button and title in
    // the top 44 (SweepFrames: NavigationBar {0, 62} {402, 54} on profile,
    // species, collection). At 44 every pushed page started 10 higher than on
    // the iPhone (android_spacing.py, 2026-11-11).
    Box(Modifier.fillMaxWidth().statusBarsPadding().height(54.dp)) {
    Box(Modifier.fillMaxWidth().height(44.dp)) {
        Box(
            Modifier.align(Alignment.CenterStart).size(44.dp).clickable(role = Role.Button, onClick = onBack),
            contentAlignment = Alignment.Center,
        ) {
            Icon(Sym.ArrowBack, stringResource(R.string.back), tint = brand.ink, modifier = Modifier.size(22.dp))
        }
        Text(
            title, fontSize = 17.sp, fontWeight = FontWeight.SemiBold, color = brand.ink, maxLines = 1,
            overflow = TextOverflow.Ellipsis, textAlign = TextAlign.Center,
            modifier = Modifier.align(Alignment.Center).padding(horizontal = 52.dp),
        )
        trailing?.let { Box(Modifier.align(Alignment.CenterEnd).padding(end = 8.dp)) { it() } }
    }
    }
}

/** A sheet with a navigation bar: the title in the middle, Done (or a pair) at the ends. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BarSheet(
    title: String,
    onDismiss: () -> Unit,
    leading: Pair<String, () -> Unit>? = null,
    trailing: Pair<String, () -> Unit>?,
    trailingEnabled: Boolean = true,
    /** The large detent with the grouped grey ground, as a Form sheet on the iPhone. */
    grouped: Boolean = false,
    content: @Composable ColumnScope.() -> Unit,
) {
    val brand = Brand.colors
    AppSheet(
        onDismissRequest = onDismiss,
        containerColor = if (grouped) brand.surfaceMuted else brand.ground,
        // The bar is the top of this sheet; the handle sits over it (BrandSheetHandle).
        dragHandle = null,
    ) {
        Column(Modifier.fillMaxWidth().let { if (grouped) it.fillMaxHeight(0.94f) else it }.navigationBarsPadding()) {
            Box(Modifier.fillMaxWidth().height(56.dp)) {
                BrandSheetHandle(Modifier.align(Alignment.TopCenter))
                // Cancel slides the sheet down first (Sheet.kt).
                val close = LocalSheetClose.current
                leading?.let { (label, act) ->
                    Text(label, fontSize = 17.sp, color = brand.moss, modifier = Modifier.align(Alignment.CenterStart)
                        .clickable(role = Role.Button) { close(act) }.padding(horizontal = 16.dp, vertical = 12.dp))
                }
                Text(title, fontSize = 17.sp, fontWeight = FontWeight.SemiBold, color = brand.ink, modifier = Modifier.align(Alignment.Center))
                trailing?.let { (label, act) ->
                    Text(label, fontSize = 17.sp, fontWeight = FontWeight.SemiBold, color = brand.moss,
                        modifier = Modifier.align(Alignment.CenterEnd).alpha(if (trailingEnabled) 1f else 0.4f)
                            .clickable(enabled = trailingEnabled, role = Role.Button, onClick = act).padding(horizontal = 16.dp, vertical = 12.dp))
                }
            }
            val column = this
            PlainText { column.content() }
        }
    }
}

/** Who made the map and the photographs, in the website footer's words. */
@Composable
private fun SourcesSheet(onDismiss: () -> Unit) {
    val brand = Brand.colors
    val context = LocalContext.current
    BarSheet(stringResource(R.string.settings_sources), onDismiss, trailing = stringResource(R.string.done) to onDismiss) {
        Column(verticalArrangement = Arrangement.spacedBy(18.dp), modifier = Modifier.fillMaxWidth().padding(20.dp)) {
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text(stringResource(R.string.sources_map), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 17.sp, color = brand.ink)
                Text(stringResource(R.string.sources_map_body), fontSize = 13.sp, color = brand.inkSoft)
                Text(stringResource(R.string.sources_osm), fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = brand.moss,
                    modifier = Modifier.clickable { openWeb(context, "https://www.openstreetmap.org/copyright") })
            }
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text(stringResource(R.string.sources_photos), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 17.sp, color = brand.ink)
                Text(stringResource(R.string.sources_photos_body), fontSize = 13.sp, color = brand.inkSoft)
            }
            Text(stringResource(R.string.sources_terms), fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = brand.moss,
                modifier = Modifier.clickable { openWeb(context, "https://ancienttrees.app/terms") })
            Spacer(Modifier.height(24.dp))
        }
    }
}

/** What we hold, then the typed second ask (Hidde, 2026-08-31: "met twee keer vragen weet je het zeker"). */
@Composable
private fun DeleteAccountSheet(host: SettingsHost, onDismiss: () -> Unit) {
    val brand = Brand.colors
    val scope = rememberCoroutineScope()
    val focus = LocalFocusManager.current
    var typed by remember { mutableStateOf("") }
    var confirming by remember { mutableStateOf(false) }
    var failed by remember { mutableStateOf(false) }
    val may = typed.trim().uppercase() == "DELETE"
    BarSheet(stringResource(R.string.delete_account), onDismiss, trailing = stringResource(R.string.done) to onDismiss) {
        Column(verticalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.fillMaxWidth().padding(20.dp)) {
            Text(stringResource(R.string.delete_signed_in_as), fontSize = 13.sp, color = brand.inkSoft)
            Text(host.email ?: stringResource(R.string.signed_in), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 20.sp, color = brand.ink)
            Text(stringResource(R.string.delete_keep), fontSize = 13.sp, color = brand.inkSoft)
            Text(stringResource(R.string.delete_hold), fontSize = 13.sp, color = brand.inkSoft)
            Text(stringResource(R.string.delete_other_address), fontSize = 13.sp, color = brand.inkSoft)
            Spacer(Modifier.height(40.dp))
            Text(stringResource(R.string.delete_type), fontSize = 13.sp, color = brand.inkSoft)
            BasicTextField(
                value = typed,
                onValueChange = { typed = it },
                singleLine = true,
                textStyle = sfStyle(fontSize = 16.sp, color = brand.ink),
                keyboardOptions = KeyboardOptions(capitalization = KeyboardCapitalization.Characters, autoCorrectEnabled = false, imeAction = ImeAction.Done),
                // RETURN PUTS THE KEYBOARD AWAY, so the button under it can be reached.
                keyboardActions = KeyboardActions(onDone = { focus.clearFocus() }),
                modifier = Modifier.fillMaxWidth().testTag("delete-confirm-field"),
                decorationBox = { inner ->
                    Box(Modifier.fillMaxWidth().height(48.dp).background(brand.surfaceMuted, RoundedCornerShape(10.dp)).padding(horizontal = 14.dp),
                        contentAlignment = Alignment.CenterStart) {
                        if (typed.isEmpty()) Text("DELETE", fontSize = 16.sp, color = brand.inkSoft.copy(alpha = 0.6f))
                        inner()
                    }
                },
            )
            Box(Modifier.alpha(if (may) 1f else 0.5f).testTag("delete-confirm-button")) {
                SheetButtonView(SheetButton(stringResource(R.string.delete_account), if (may) SheetKind.DESTRUCTIVE else SheetKind.SECONDARY) {
                    if (may) confirming = true
                })
            }
            if (failed) Text(stringResource(R.string.delete_failed), fontSize = 13.sp, color = brand.dangerText)
            Spacer(Modifier.height(16.dp))
        }
    }
    if (confirming) {
        BrandSheet(
            title = stringResource(R.string.delete_title),
            message = stringResource(R.string.delete_body),
            onDismiss = { confirming = false },
            buttons = listOf(
                SheetButton(stringResource(R.string.delete), SheetKind.DESTRUCTIVE) {
                    confirming = false
                    scope.launch {
                        val ok = host.account.deleteAccount()
                        failed = !ok
                        if (ok) { host.profiles.forgetLocally(); host.signedOut(); onDismiss() }
                    }
                },
                SheetButton(stringResource(R.string.cancel), SheetKind.SECONDARY) { confirming = false },
            ),
        )
    }
}

/** "Version 0.1.0 (1)": which build a report came from (Profile.swift buildLine). */
@Composable
private fun versionLine(context: Context): String {
    val info = remember { runCatching { context.packageManager.getPackageInfo(context.packageName, 0) }.getOrNull() }
    @Suppress("DEPRECATION")
    val code = info?.let { if (android.os.Build.VERSION.SDK_INT >= 28) it.longVersionCode.toString() else it.versionCode.toString() } ?: "?"
    return stringResource(R.string.settings_version, info?.versionName ?: "?", code)
}
