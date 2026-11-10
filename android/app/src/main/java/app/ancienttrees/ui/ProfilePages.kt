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
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue

sealed class ProfilePage {
    data object Settings : ProfilePage()
    data object Privacy : ProfilePage()
    data class People(val source: PeopleSource) : ProfilePage()
    data class Person(val userId: String) : ProfilePage()
}

class ProfileRoutes(args: List<String>) {
    val stack = mutableStateListOf<ProfilePage>()
    var editProfile by mutableStateOf("-profile-edit" in args)
    var earlyAdopterSheet by mutableStateOf("-earlyadoptersheet" in args)
    /** -signoutask: Settings opens with its sign-out question up. */
    val askSignOut = "-signoutask" in args

    init {
        if ("-settings" in args) stack.add(ProfilePage.Settings)
        if ("-privacy" in args) {
            if (stack.isEmpty()) stack.add(ProfilePage.Settings)
            stack.add(ProfilePage.Privacy)
        }
        if ("-people" in args) stack.add(ProfilePage.People(PeopleSource.SEARCH))
    }

    val showing: Boolean get() = stack.isNotEmpty()
    fun openSettings() = stack.add(ProfilePage.Settings)
    fun openPeople(source: PeopleSource) = stack.add(ProfilePage.People(source))
    fun openPerson(userId: String) = stack.add(ProfilePage.Person(userId))
    fun back() { if (stack.isNotEmpty()) stack.removeAt(stack.lastIndex) }
    fun clear() = stack.clear()
}

/** The top page of the stack, full screen, and the sheets that ride over any of them. */
@Composable
fun ProfilePages(
    routes: ProfileRoutes,
    settings: SettingsHost,
    people: PeopleHost,
    onEarlyAdopterSeen: () -> Unit,
) {
    when (val top = routes.stack.lastOrNull()) {
        ProfilePage.Settings -> SettingsScreen(settings, onBack = { routes.back() }, askSignOut = routes.askSignOut)
        ProfilePage.Privacy -> PrivacySettingsScreen(
            settings.account, settings.profiles, people.userId,
            onBack = { routes.back() },
            editName = { routes.editProfile = true },
            openPerson = { routes.openPerson(it) },
        )
        is ProfilePage.People -> FindPeopleScreen(people, top.source, onBack = { routes.back() })
        is ProfilePage.Person -> PersonProfileScreen(people, top.userId, onBack = { routes.back() })
        null -> Unit
    }
    if (routes.editProfile) ProfileEditorSheet(settings.account, settings.profiles) { routes.editProfile = false }
    // Every way out counts as seen: Done, the cross, a swipe.
    if (routes.earlyAdopterSheet) EarlyAdopterSheet { routes.earlyAdopterSheet = false; onEarlyAdopterSeen() }
}
