// Where the profile screens open: Settings, Privacy settings, Find people and
// the follow lists, a person's profile, and the sheets over them (the profile
// editor, the early-adopter sheet). One small stack, as the iPhone's Navigator
// pushes Route.settings, .findPeople, .followList and .person.
//
// My trees (Collect.swift, its own session) opens these from its header: the
// gear -> openSettings(), your face -> editProfile = true, the person-with-a-plus
// -> openPeople(SEARCH), the follow counts -> openPeople(FOLLOWERS/FOLLOWING).
// The launch arguments are the sweep's (SweepFrames.swift): -settings, -privacy,
// -signoutask, -people, -profile-edit, -earlyadoptersheet.

package app.ancienttrees.ui

import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue

class ProfileRoutes(args: List<String>, private val nav: Nav) {
    var editProfile by mutableStateOf("-profile-edit" in args)
    var earlyAdopterSheet by mutableStateOf("-earlyadoptersheet" in args)
    /** -signoutask: Settings opens with its sign-out question up. */
    val askSignOut = "-signoutask" in args

    init {
        if ("-settings" in args) nav.push(Page.Settings)
        if ("-privacy" in args) {
            if (nav.top != Page.Settings) nav.push(Page.Settings)
            nav.push(Page.Privacy)
        }
        if ("-people" in args) nav.push(Page.People(PeopleSource.SEARCH))
        // -open=person:<id>: somebody's profile (ContentView's -open=person:, the sweep's Marieke).
        args.firstOrNull { it.startsWith("-open=person:") }?.let { nav.push(Page.Person(it.removePrefix("-open=person:"))) }
    }

    val showing: Boolean get() = nav.top?.isProfile == true
    fun openSettings() = nav.push(Page.Settings)
    fun openPrivacy() = nav.push(Page.Privacy)
    fun openPeople(source: PeopleSource) = nav.push(Page.People(source))
    fun openPerson(userId: String) = nav.push(Page.Person(userId))
    fun back() = nav.pop()
    /** Signed out: no profile page stays open on any tab. */
    fun clear() = nav.removeAll { it.isProfile }
}

/** One profile page on a stack (Pages.kt). */
@Composable
fun ProfilePageScreen(page: Page, routes: ProfileRoutes, settings: SettingsHost, people: PeopleHost) {
    when (page) {
        Page.Settings -> SettingsScreen(settings, onBack = { routes.back() }, askSignOut = routes.askSignOut)
        Page.Privacy -> PrivacySettingsScreen(
            settings.account, settings.profiles, people.userId,
            onBack = { routes.back() },
            editName = { routes.editProfile = true },
            openPerson = { routes.openPerson(it) },
        )
        is Page.People -> FindPeopleScreen(people, page.source, onBack = { routes.back() })
        is Page.Person -> PersonProfileScreen(people, page.userId, onBack = { routes.back() })
        else -> Unit
    }
}

/** The sheets that ride over any page: the profile editor, the early-adopter sheet. */
@Composable
fun ProfileSheets(
    routes: ProfileRoutes,
    settings: SettingsHost,
    onEarlyAdopterSeen: () -> Unit,
) {
    if (routes.editProfile) ProfileEditorSheet(settings.account, settings.profiles) { routes.editProfile = false }
    // Every way out counts as seen: Done, the cross, a swipe.
    if (routes.earlyAdopterSheet) EarlyAdopterSheet { routes.earlyAdopterSheet = false; onEarlyAdopterSeen() }
}
