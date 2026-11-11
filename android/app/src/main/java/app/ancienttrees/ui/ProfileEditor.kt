// Setting the name and the face people see, and who may see them: ported from
// ios Screens/ProfileEditor.swift and Screens/PrivacySettings.swift.
//
// The editor: the photograph large and centred with Change photo under it, then
// one card with Name and Country, Cancel and Save in the bar. The picture goes
// to the avatars bucket under the person's own id; the country is optional and
// picked, never guessed from where the phone stands.
//
// Privacy settings: one switch, "Public profile", ON is public. Turning it on
// asks first with the one sheet; turning it off is one tap and asks nothing.

package app.ancienttrees.ui

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import androidx.activity.compose.BackHandler
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.account.Account
import app.ancienttrees.account.Avatars
import app.ancienttrees.account.Collector
import java.io.ByteArrayOutputStream
import app.ancienttrees.account.Profiles
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.util.Locale

@Composable
fun ProfileEditorSheet(account: Account, profiles: Profiles, onDismiss: () -> Unit) {
    val brand = Brand.colors
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var name by remember { mutableStateOf(profiles.me?.displayName.orEmpty()) }
    var country by remember {
        mutableStateOf(profiles.myCountry ?: if (profiles.myFlagHidden) null else Profiles.countryGuess())
    }
    var preview by remember { mutableStateOf<Bitmap?>(null) }
    var jpeg by remember { mutableStateOf<ByteArray?>(null) }
    var saving by remember { mutableStateOf(false) }
    var failed by remember { mutableStateOf<String?>(null) }
    var picking by remember { mutableStateOf(false) }

    val photo = rememberLauncherForActivityResult(ActivityResultContracts.PickVisualMedia()) { uri ->
        if (uri == null) return@rememberLauncherForActivityResult
        scope.launch {
            val raw = withContext(Dispatchers.IO) { runCatching { context.contentResolver.openInputStream(uri)?.use { it.readBytes() } }.getOrNull() }
                ?: return@launch
            // 512 is plenty for a face in a 62 point circle.
            val small = Collector.downsized(raw)?.let { face(it) } ?: return@launch
            jpeg = small
            preview = BitmapFactory.decodeByteArray(small, 0, small.size)
        }
    }

    fun save() {
        val session = account.session ?: run { failed = context.getString(R.string.editor_why_expired); return }
        saving = true
        failed = null
        scope.launch {
            val token = account.fresh()?.accessToken
            if (token == null) {
                saving = false; failed = context.getString(R.string.editor_why_expired); return@launch
            }
            var url = profiles.me?.avatarUrl
            var pictureFailed = false
            jpeg?.let { bytes -> Avatars.upload(bytes, session.userId, token)?.let { url = it } ?: run { pictureFailed = true } }
            var ok = profiles.save(name.trim(), url, session.userId, token)
            var countryFailed = false
            if (ok && (country != profiles.myCountry || (country == null && !profiles.myFlagHidden))) {
                ok = profiles.saveCountry(country, session.userId, token)
                countryFailed = !ok
            }
            saving = false
            if (ok) onDismiss() else failed = context.getString(
                when {
                    countryFailed -> R.string.editor_why_country
                    pictureFailed -> R.string.editor_why_picture
                    else -> R.string.editor_why_server
                },
            )
        }
    }

    BarSheet(
        stringResource(R.string.editor_title), onDismiss,
        leading = stringResource(R.string.cancel) to onDismiss,
        trailing = stringResource(if (saving) R.string.editor_saving else R.string.editor_save) to { save() },
        trailingEnabled = !saving && name.isNotBlank(),
        grouped = true,
    ) {
        Column(
            verticalArrangement = Arrangement.spacedBy(20.dp),
            modifier = Modifier.fillMaxWidth().verticalScroll(rememberScrollState())
                .padding(horizontal = 16.dp).padding(top = 16.dp, bottom = 32.dp).testTag("profile-editor"),
        ) {
            // THE PHOTO LEADS, LARGE AND CENTRED, with Change photo under it.
            Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                Box(Modifier.size(96.dp).clip(CircleShape).background(brand.moss.copy(alpha = 0.12f)), contentAlignment = Alignment.Center) {
                    val p = preview
                    val url = profiles.me?.avatarUrl
                    when {
                        p != null -> Image(p.asImageBitmap(), null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())
                        url != null -> RemoteImage(url, null, Modifier.fillMaxSize(), placeholder = false)
                        else -> Icon(Sym.PersonFill, null, tint = brand.moss.copy(alpha = 0.6f), modifier = Modifier.size(44.dp))
                    }
                }
                Text(
                    stringResource(if (preview == null && profiles.me?.avatarUrl == null) R.string.editor_choose_photo else R.string.editor_change_photo),
                    fontSize = 17.sp, color = brand.moss,
                    modifier = Modifier.heightIn(min = 44.dp).clickable(role = Role.Button) {
                        photo.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
                    }.padding(vertical = 11.dp),
                )
            }
            // One card, each row naming itself with the value on the right, as Apple's contact card.
            // An iOS 26 Form section: corners 26.
            Column(Modifier.fillMaxWidth().brandCard(26.dp)) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.fillMaxWidth().heightIn(min = 48.dp).padding(horizontal = 16.dp),
                ) {
                    Text(stringResource(R.string.editor_name), fontSize = 17.sp, color = brand.ink)
                    Spacer(Modifier.size(16.dp))
                    BasicTextField(
                        value = name,
                        onValueChange = { name = it },
                        singleLine = true,
                        textStyle = sfStyle(fontSize = 17.sp, color = brand.ink, textAlign = TextAlign.End),
                        keyboardOptions = KeyboardOptions(capitalization = KeyboardCapitalization.Words),
                        modifier = Modifier.weight(1f),
                        decorationBox = { inner ->
                            Box(contentAlignment = Alignment.CenterEnd) {
                                if (name.isEmpty()) Text(stringResource(R.string.editor_name_prompt), fontSize = 17.sp, color = placeholderGrey())
                                inner()
                            }
                        },
                    )
                }
                HorizontalDivider(Modifier.padding(start = 16.dp), thickness = 0.5.dp, color = brand.hairline)
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.fillMaxWidth().heightIn(min = 48.dp).clickable(role = Role.Button) { picking = true }
                        .padding(horizontal = 16.dp).testTag("profile-country"),
                ) {
                    Text(stringResource(R.string.editor_country), fontSize = 17.sp, color = brand.ink, modifier = Modifier.weight(1f))
                    Text(country?.let(::countryRow) ?: stringResource(R.string.editor_dont_show), fontSize = 17.sp, color = brand.inkSoft)
                    Icon(Sym.ChevronRight, null, tint = brand.inkSoft.copy(alpha = 0.6f), modifier = Modifier.size(18.dp))
                }
            }
            failed?.let { why ->
                Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text(stringResource(R.string.editor_failed), fontSize = 13.sp, color = Color(0xFFFF3B30))
                    Text(stringResource(R.string.editor_why, why), fontSize = 12.sp, color = Color(0xFFFF3B30))
                }
            }
        }
    }
    if (picking) CountryPicker(country, onPick = { country = it; picking = false }, onDismiss = { picking = false })
}

/** A picker row: the flag, then the country's English name. */
private fun countryRow(code: String): String = listOfNotNull(flagEmoji(code), countryName(code)).joinToString("  ")

/** iOS Settings' long choice: Don't show, then every country by its English name. */
@Composable
private fun CountryPicker(current: String?, onPick: (String?) -> Unit, onDismiss: () -> Unit) {
    val brand = Brand.colors
    val all = remember {
        Locale.getISOCountries().map { it to countryName(it) }.filter { it.second.isNotEmpty() }.sortedBy { it.second.lowercase() }
    }
    BarSheet(stringResource(R.string.editor_country), onDismiss, trailing = stringResource(R.string.done) to onDismiss) {
        LazyColumn(Modifier.fillMaxWidth().height(560.dp)) {
            item { PickRow(stringResource(R.string.editor_dont_show), current == null) { onPick(null) } }
            items(all, key = { it.first }) { (code, _) -> PickRow(countryRow(code), current == code) { onPick(code) } }
        }
    }
    BackHandler(onBack = onDismiss)
}

@Composable
private fun PickRow(label: String, on: Boolean, onClick: () -> Unit) {
    val brand = Brand.colors
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier.fillMaxWidth().heightIn(min = 48.dp).clickable(role = Role.Button, onClick = onClick).padding(horizontal = 20.dp),
    ) {
        Text(label, fontSize = 17.sp, color = brand.ink, modifier = Modifier.weight(1f))
        if (on) Icon(Sym.Check, null, tint = brand.moss, modifier = Modifier.size(18.dp))
    }
}

/** PrivacySettings.swift: the one switch, its line, and a way to see what others see. */
@Composable
fun PrivacySettingsScreen(
    account: Account,
    profiles: Profiles,
    userId: String?,
    onBack: () -> Unit,
    editName: () -> Unit,
    openPerson: (String) -> Unit,
) = PlainText { PrivacyInner(account, profiles, userId, onBack, editName, openPerson) }

@Composable
private fun PrivacyInner(
    account: Account,
    profiles: Profiles,
    userId: String?,
    onBack: () -> Unit,
    editName: () -> Unit,
    openPerson: (String) -> Unit,
) {
    val brand = Brand.colors
    val scope = rememberCoroutineScope()
    var confirming by remember { mutableStateOf(false) }
    val isPublic = profiles.myPublic ?: false
    fun setPublic(on: Boolean) {
        val uid = userId ?: return
        scope.launch {
            val t = account.fresh()?.accessToken ?: return@launch
            profiles.savePublic(on, uid, t)
        }
    }
    Column(Modifier.fillMaxSize().background(brand.ground)) {
        PushedBar(stringResource(R.string.privacy_settings), onBack)
        Column(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.padding(horizontal = 16.dp).padding(top = 6.dp)) {
            Row(
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.fillMaxWidth().brandCard().heightIn(min = 48.dp).padding(horizontal = 16.dp).testTag("profile-public"),
            ) {
                Icon(Sym.Public, null, tint = brand.moss, modifier = Modifier.size(20.dp))
                Text(stringResource(R.string.privacy_public_profile), fontSize = 16.sp, color = brand.ink, modifier = Modifier.weight(1f))
                Switch(
                    checked = isPublic,
                    onCheckedChange = { want ->
                        when {
                            !want -> setPublic(false)
                            // A public profile shows a name, so the name first.
                            profiles.me?.displayName.isNullOrEmpty() -> editName()
                            else -> confirming = true
                        }
                    },
                    colors = SwitchDefaults.colors(checkedTrackColor = brand.moss, checkedThumbColor = Color.White),
                )
            }
            Text(
                stringResource(if (isPublic) R.string.privacy_public_line else R.string.privacy_private_line),
                fontSize = 13.sp, color = brand.inkSoft, modifier = Modifier.padding(horizontal = 16.dp),
            )
            if (isPublic && userId != null) {
                Text(
                    stringResource(R.string.privacy_see_public), fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = brand.moss,
                    modifier = Modifier.heightIn(min = 44.dp).clickable(role = Role.Button) { openPerson(userId) }
                        .padding(horizontal = 16.dp, vertical = 13.dp).testTag("profile-public-open"),
                )
            }
        }
    }
    if (confirming) MakePublicSheet(onYes = { confirming = false; setPublic(true) }, onNo = { confirming = false })
}

/** "Make your profile public?" with what becomes visible: Privacy settings and Find people ask the same. */
@Composable
fun MakePublicSheet(onYes: () -> Unit, onNo: () -> Unit) {
    BrandSheet(
        title = stringResource(R.string.public_ask_title),
        message = stringResource(R.string.public_ask_body),
        icon = Sym.Public,
        points = listOf(
            stringResource(R.string.public_ask_1),
            stringResource(R.string.public_ask_2),
            stringResource(R.string.public_ask_3),
        ),
        onDismiss = onNo,
        buttons = listOf(
            SheetButton(stringResource(R.string.public_ask_yes), SheetKind.PRIMARY, action = onYes),
            SheetButton(stringResource(R.string.public_ask_no), SheetKind.QUIET, action = onNo),
        ),
    )
}

/** 512 on the long side, about forty kilobytes (ProfileEditor.swift Sightings.downsized(max: 512)). */
private suspend fun face(jpeg: ByteArray): ByteArray? = withContext(Dispatchers.Default) {
    runCatching {
        val b = BitmapFactory.decodeByteArray(jpeg, 0, jpeg.size) ?: return@runCatching null
        val side = maxOf(b.width, b.height)
        val s = if (side > 512) 512f / side else 1f
        val small = if (s < 1f) Bitmap.createScaledBitmap(b, (b.width * s).toInt(), (b.height * s).toInt(), true) else b
        ByteArrayOutputStream().use { out -> small.compress(Bitmap.CompressFormat.JPEG, 80, out); out.toByteArray() }
    }.getOrNull()
}
