// A tree only you have: ios Screens/TreeDetail.swift with `mine` set, the same
// page as ours with the other half of it drawn (Hidde, 2026-08-24: "het is
// dezelfde boom pagina als onze bomen alleen dan dat de eindgebruiker de velden
// kan invullen"). Your photograph as the hero, the ellipsis menu of what you can
// change, the empty fields offered in green, More photographs, and one action
// in the bar: Share this tree. The pieces it shares with our trees' page come
// from TreeDetail.kt (FactColumn, FactValue, Hairline, BigButton).
//
// Not here yet, each its own screen in data/android-parity.json: "Move the pin"
// (place-pin) and "Merge with another tree" (MergeChooser).

package app.ancienttrees.ui

import android.content.Intent
import androidx.activity.compose.BackHandler
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.MoreHoriz
import androidx.compose.material.icons.outlined.AddCircleOutline
import androidx.compose.material.icons.outlined.CalendarMonth
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Eco
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.IosShare
import androidx.compose.material.icons.outlined.PhotoCamera
import androidx.compose.material.icons.outlined.PhotoLibrary
import androidx.compose.material.icons.outlined.Straighten
import androidx.compose.material.icons.outlined.Verified
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Text
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
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.zIndex
import androidx.core.content.FileProvider
import app.ancienttrees.R
import app.ancienttrees.account.Collector
import app.ancienttrees.account.MyTrees
import app.ancienttrees.account.OwnSighting
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.feed.Geo
import kotlinx.coroutines.launch

/** TreeDetail.EditableField: a field on your own tree. */
enum class EditableField { NAME, AGE, GIRTH, STORY }

/** TreeDetail.minePlace: the nearest city we publish within 30 km, the day-trip boundary. */
fun minePlace(catalogue: Catalogue, lat: Double, lng: Double): Pair<String, String>? {
    val best = catalogue.trees.minByOrNull { Geo.km(lat, lng, it.lat, it.lng) } ?: return null
    if (Geo.km(lat, lng, best.lat, best.lng) > 30) return null
    return best.city to best.citySlug
}

@Composable
fun OwnTree(
    id: String,
    mine: MyTrees,
    catalogue: Catalogue,
    onBack: () -> Unit,
    onCity: (slug: String, name: String) -> Unit,
) {
    PlainText { OwnTreeInner(id, mine, catalogue, onBack, onCity) }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun OwnTreeInner(
    id: String,
    mine: MyTrees,
    catalogue: Catalogue,
    onBack: () -> Unit,
    onCity: (slug: String, name: String) -> Unit,
) {
    val brand = Brand.colors
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    BackHandler(onBack = onBack)
    // The live record, so an edit shows at once.
    val s = mine.byId(id)
    if (s == null) {
        // "That tree is gone" (ContentView .mine).
        Box(Modifier.fillMaxSize().background(brand.ground), contentAlignment = Alignment.Center) {
            Text(stringResource(R.string.ot_gone), fontSize = 17.sp, color = brand.inkSoft)
        }
        return
    }
    val tree = s.asTree()
    var editing by remember { mutableStateOf<EditableField?>(null) }
    var choosingSpecies by remember { mutableStateOf(false) }
    var removing by remember { mutableStateOf(false) }
    var preparing by remember { mutableStateOf(false) }
    var shareFailed by remember { mutableStateOf(false) }
    val place = remember(s.lat, s.lng, catalogue) { minePlace(catalogue, s.lat, s.lng) }

    BoxWithConstraints(Modifier.fillMaxSize().background(brand.ground)) {
        // heroHeight: the photograph's shape across the page, stopped at 60 percent.
        val heroHeight = minOf(maxWidth * (4f / 3f), maxHeight * 0.6f)
        val scroll = rememberScrollState()
        Column(Modifier.fillMaxSize().verticalScroll(scroll)) {
            Box(Modifier.zIndex(0f).graphicsLayer { translationY = scroll.value * 0.5f }) {
                OwnPhoto(s, mine, Modifier.fillMaxWidth().height(heroHeight), maxSide = 1600) {
                    Box(Modifier.fillMaxWidth().height(heroHeight).background(brand.surfaceMuted))
                }
            }
            Column(
                verticalArrangement = Arrangement.spacedBy(28.dp),
                modifier = Modifier
                    .zIndex(1f)
                    .fillMaxWidth()
                    .background(brand.ground, RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp))
                    .padding(horizontal = 20.dp)
                    .padding(top = 20.dp),
            ) {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(
                        tree.name,
                        fontFamily = BrandFace,
                        fontWeight = FontWeight.Bold,
                        fontSize = 30.sp,
                        lineHeight = 35.sp,
                        color = brand.ink,
                        modifier = Modifier.semantics { heading() },
                    )
                    // placeLink: the city near it, tappable, or nothing when none is near.
                    if (place != null) {
                        val see = stringResource(R.string.see_every_tree_in, place.first)
                        Box(Modifier.heightIn(min = 44.dp), contentAlignment = Alignment.CenterStart) {
                            Text(
                                place.first,
                                fontSize = 15.sp,
                                color = brand.ink,
                                textDecoration = TextDecoration.Underline,
                                maxLines = 1,
                                modifier = Modifier
                                    .clickable(role = Role.Button, interactionSource = remember { MutableInteractionSource() }, indication = null) {
                                        onCity(place.second, place.first)
                                    }
                                    .semantics { contentDescription = see },
                            )
                        }
                    }
                    if (s.published) MineStatus()
                    OwnFacts(s, onEdit = { editing = it }, onSpecies = { choosingSpecies = true })
                }
                // story: the blank to fill, or the words you wrote.
                if (s.note.isEmpty()) {
                    Blank(stringResource(R.string.ot_prompt_story)) { editing = EditableField.STORY }
                } else {
                    ExpandableText(
                        androidx.compose.ui.text.AnnotatedString(s.note),
                        lines = 6,
                        style = TextStyle(fontSize = 17.sp, lineHeight = 22.sp, color = brand.ink),
                    )
                }
                MorePhotos(s, mine)
                Spacer(Modifier.height(90.dp).navigationBarsPadding())
            }
        }

        OwnTopButtons(
            onBack = onBack,
            onEdit = { editing = it },
            onSpecies = { choosingSpecies = true },
            onRemove = { removing = true },
        )

        // ONE ACTION, AND IT IS SHARE (Hidde, 2026-09-01): the unlisted page, made on the tap.
        Column(Modifier.align(Alignment.BottomCenter).fillMaxWidth().background(brand.ground)) {
            Box(Modifier.fillMaxWidth().height(0.5.dp).background(brand.hairline))
            Row(Modifier.fillMaxWidth().padding(horizontal = 20.dp).padding(top = 10.dp, bottom = 8.dp).navigationBarsPadding()) {
                BigButton(stringResource(R.string.share_tree), Icons.Outlined.IosShare, Modifier.weight(1f)) {
                    if (preparing) return@BigButton
                    preparing = true
                    scope.launch {
                        val url = mine.publish(s.id)
                        preparing = false
                        if (url == null) {
                            shareFailed = true
                            return@launch
                        }
                        val send = Intent(Intent.ACTION_SEND).apply {
                            type = "text/plain"
                            putExtra(Intent.EXTRA_SUBJECT, tree.name)
                            putExtra(Intent.EXTRA_TEXT, url)
                        }
                        context.startActivity(Intent.createChooser(send, null))
                    }
                }
            }
        }
    }

    editing?.let { field ->
        FieldEditor(
            field = field,
            initial = when (field) {
                EditableField.NAME -> s.name
                EditableField.AGE -> s.age.orEmpty()
                EditableField.GIRTH -> s.girthCm?.let { metres(it) }.orEmpty()
                EditableField.STORY -> s.note
            },
            onCancel = { editing = null },
            onSave = { text ->
                editing = null
                scope.launch {
                    when (field) {
                        EditableField.NAME -> if (text.isNotEmpty()) mine.update(s.id, name = text)
                        EditableField.AGE -> mine.update(s.id, age = text)
                        // Empty clears it; something unreadable keeps what was there.
                        EditableField.GIRTH -> if (text.isEmpty()) mine.update(s.id, girthCm = 0) else girthCm(text)?.let { mine.update(s.id, girthCm = it) }
                        EditableField.STORY -> mine.update(s.id, note = text)
                    }
                }
            },
        )
    }
    if (choosingSpecies) {
        // SpeciesChooser.swift, as the iPhone's own tree names its species.
        SpeciesChooser(
            catalogue = catalogue,
            // nearbySpecies: ordering only, never a claim.
            nearby = remember(s.lat, s.lng) {
                catalogue.trees.filter { Geo.km(s.lat, s.lng, it.lat, it.lng) < 3 && it.commonName.isNotEmpty() }.map { it.commonName }.distinct()
            },
            current = tree.commonName,
            onPick = { picked ->
                val latin = if ('(' in picked) null else catalogue.scientificName(picked)
                scope.launch { mine.update(s.id, species = if (latin != null) "$picked ($latin)" else picked) }
            },
            onClose = { choosingSpecies = false },
        )
    }
    if (removing) {
        BrandSheet(
            title = stringResource(R.string.ot_remove_title, tree.name),
            message = stringResource(R.string.ot_remove_body),
            onDismiss = { removing = false },
            buttons = listOf(
                SheetButton(stringResource(R.string.ot_remove), SheetKind.DESTRUCTIVE) {
                    removing = false
                    scope.launch { mine.remove(s.id) }
                    onBack()
                },
                SheetButton(stringResource(R.string.ot_keep), SheetKind.SECONDARY) { removing = false },
            ),
        )
    }
    // NEWS IS THE SNACKBAR: a failed share says so and leaves.
    if (shareFailed) {
        LaunchedEffect(Unit) {
            kotlinx.coroutines.delay(3000)
            shareFailed = false
        }
        Box(Modifier.fillMaxSize().navigationBarsPadding().padding(bottom = 90.dp), contentAlignment = Alignment.BottomCenter) {
            Text(
                stringResource(R.string.ot_share_failed),
                color = brand.surface,
                fontSize = 15.sp,
                modifier = Modifier.padding(horizontal = 20.dp).background(brand.ink, RoundedCornerShape(12.dp)).padding(14.dp),
            )
        }
    }
}

/** mineStatus: said only once it made the map (Hidde, 2026-10-08, iNaturalist's Research Grade). */
@Composable
private fun MineStatus() {
    val brand = Brand.colors
    Row(
        Modifier.fillMaxWidth().background(brand.moss.copy(alpha = 0.12f), RoundedCornerShape(10.dp)).padding(12.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        Icon(Icons.Outlined.Verified, null, tint = brand.moss, modifier = Modifier.size(20.dp))
        Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
            Text(stringResource(R.string.ot_approved), fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = brand.ink)
            Text(stringResource(R.string.ot_approved_body), fontSize = 13.sp, color = brand.inkSoft)
        }
    }
}

/** factsBlock with your blanks: Age and Girth side by side, Species under them. */
@Composable
private fun OwnFacts(s: OwnSighting, onEdit: (EditableField) -> Unit, onSpecies: () -> Unit) {
    val brand = Brand.colors
    val shape = RoundedCornerShape(14.dp)
    val tree = s.asTree()
    Column(Modifier.fillMaxWidth().clip(shape).background(brand.surface, shape).border(1.dp, brand.hairline, shape)) {
        Column(Modifier.padding(top = 12.dp, bottom = 4.dp).padding(horizontal = 16.dp)) {
            Row(Modifier.height(IntrinsicSize.Min)) {
                Box(Modifier.weight(1f).padding(end = 16.dp)) {
                    val age = s.age
                    if (age == null) {
                        FactColumn(stringResource(R.string.age)) { AddValue(stringResource(R.string.ot_add_age)) { onEdit(EditableField.AGE) } }
                    } else {
                        val first = age.split(',', ';', '(').first().trim()
                        FactColumn(stringResource(R.string.age)) { FactValue(if (first.length > 24) stringResource(R.string.age_see_story) else first) }
                    }
                }
                Box(Modifier.width(1.dp).height(44.dp).background(brand.hairline))
                Box(Modifier.weight(1f).padding(start = 16.dp)) {
                    FactColumn(stringResource(R.string.girth)) {
                        val g = s.girthCm
                        if (g != null) FactValue(stringResource(R.string.girth_value, metres(g)))
                        else AddValue(stringResource(R.string.ot_add_girth)) { onEdit(EditableField.GIRTH) }
                    }
                }
            }
            Column(Modifier.fillMaxWidth()) {
                Hairline()
                Box(Modifier.padding(top = 10.dp)) {
                    // ON YOUR OWN TREE THIS NAMES THE SPECIES, it does not browse to one.
                    FactColumn(stringResource(R.string.species)) {
                        if (tree.species.isEmpty()) {
                            AddValue(stringResource(R.string.ot_add_species), onSpecies)
                        } else {
                            Text(
                                tree.commonName,
                                fontFamily = BrandFace,
                                fontWeight = FontWeight.Bold,
                                fontSize = 19.sp,
                                lineHeight = 23.sp,
                                color = brand.moss,
                                maxLines = 2,
                                modifier = Modifier.clickable(role = Role.Button, onClick = onSpecies),
                            )
                        }
                    }
                }
            }
        }
    }
}

/** addValue: "Add", never "Add it"; the label above names the field. */
@Composable
private fun AddValue(label: String, onClick: () -> Unit) {
    val brand = Brand.colors
    Row(
        Modifier
            .heightIn(min = 44.dp)
            .clickable(role = Role.Button, interactionSource = remember { MutableInteractionSource() }, indication = null, onClick = onClick)
            .semantics { contentDescription = label },
        verticalAlignment = Alignment.Top,
        horizontalArrangement = Arrangement.spacedBy(4.dp),
    ) {
        Icon(Icons.Outlined.AddCircleOutline, null, tint = brand.moss, modifier = Modifier.size(18.dp).padding(top = 2.dp))
        Text(stringResource(R.string.ot_add), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = brand.moss)
    }
}

/** blank: an empty field offered rather than hidden, in green. */
@Composable
private fun Blank(label: String, onClick: () -> Unit) {
    val brand = Brand.colors
    Row(
        Modifier.heightIn(min = 44.dp).clickable(role = Role.Button, onClick = onClick),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(5.dp),
    ) {
        Icon(Icons.Outlined.AddCircleOutline, null, tint = brand.moss, modifier = Modifier.size(18.dp))
        Text(label, fontSize = 15.sp, color = brand.moss)
    }
}

/** morePhotosRow: the further photographs, and an Add photo tile with camera or library. */
@Composable
private fun MorePhotos(s: OwnSighting, mine: MyTrees) {
    val brand = Brand.colors
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var menu by remember { mutableStateOf(false) }
    val shot = remember { java.io.File(context.cacheDir, "photos").apply { mkdirs() }.let { java.io.File(it, "extra.jpg") } }
    val shotUri = remember { FileProvider.getUriForFile(context, context.packageName + ".photos", shot) }
    fun add(bytes: ByteArray?) {
        scope.launch {
            val jpeg = bytes?.let { Collector.downsized(it) } ?: return@launch
            mine.addExtra(s.id, jpeg)
        }
    }
    val camera = rememberLauncherForActivityResult(ActivityResultContracts.TakePicture()) { ok ->
        if (!ok) return@rememberLauncherForActivityResult
        val raw = runCatching { shot.readBytes() }.getOrNull()
        shot.delete()
        add(raw)
    }
    val room = (MyTrees.MAX_EXTRAS - s.extras.size).coerceAtLeast(1)
    val library = rememberLauncherForActivityResult(ActivityResultContracts.PickMultipleVisualMedia(maxOf(2, room))) { uris ->
        for (u in uris.take(room)) add(runCatching { context.contentResolver.openInputStream(u)?.use { it.readBytes() } }.getOrNull())
    }
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text(stringResource(R.string.ot_more_photos), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 15.sp, color = brand.ink)
        Text(stringResource(R.string.ot_more_photos_body), fontSize = 13.sp, color = brand.inkSoft)
        Row(Modifier.horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            for (path in listOfNotNull(s.sign) + s.extras) {
                OwnPhoto(s.copy(photo = path, demo = null), mine, Modifier.size(88.dp).clip(RoundedCornerShape(12.dp)), maxSide = 300) {}
            }
            if (s.extras.size < MyTrees.MAX_EXTRAS) {
                Box {
                    Column(
                        Modifier
                            .size(88.dp)
                            .background(brand.surfaceMuted, RoundedCornerShape(12.dp))
                            .clickable(role = Role.Button) { menu = true },
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(6.dp, Alignment.CenterVertically),
                    ) {
                        Icon(Icons.Filled.Add, null, tint = brand.moss, modifier = Modifier.size(22.dp))
                        Text(stringResource(R.string.ot_add_photo), fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = brand.moss)
                    }
                    DropdownMenu(expanded = menu, onDismissRequest = { menu = false }, containerColor = brand.surface) {
                        DropdownMenuItem(
                            text = { Text(stringResource(R.string.collect_camera), color = brand.ink, fontSize = 16.sp) },
                            trailingIcon = { Icon(Icons.Outlined.PhotoCamera, null, tint = brand.ink) },
                            onClick = {
                                menu = false
                                runCatching { camera.launch(shotUri) }
                            },
                        )
                        DropdownMenuItem(
                            text = { Text(stringResource(R.string.cf_choose), color = brand.ink, fontSize = 16.sp) },
                            trailingIcon = { Icon(Icons.Outlined.PhotoLibrary, null, tint = brand.ink) },
                            onClick = {
                                menu = false
                                library.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
                            },
                        )
                    }
                }
            }
        }
    }
}

/** Back, and the ellipsis menu: the fields you can fill, then Remove, last and marked. */
@Composable
private fun OwnTopButtons(onBack: () -> Unit, onEdit: (EditableField) -> Unit, onSpecies: () -> Unit, onRemove: () -> Unit) {
    val brand = Brand.colors
    val glass = brand.ground.copy(alpha = 0.92f)
    var menu by remember { mutableStateOf(false) }
    Row(
        Modifier.fillMaxWidth().statusBarsPadding().padding(horizontal = 16.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        val back = stringResource(R.string.back)
        Box(
            Modifier.size(44.dp).shadow(2.dp, CircleShape).background(glass, CircleShape)
                .clickable(role = Role.Button, onClick = onBack).semantics { contentDescription = back },
            contentAlignment = Alignment.Center,
        ) {
            Icon(Icons.AutoMirrored.Filled.ArrowBack, null, tint = brand.ink, modifier = Modifier.size(20.dp))
        }
        Spacer(Modifier.weight(1f))
        val more = stringResource(R.string.ot_more)
        Box {
            Box(
                Modifier.size(44.dp).shadow(2.dp, CircleShape).background(glass, CircleShape)
                    .clickable(role = Role.Button) { menu = true }.semantics { contentDescription = more },
                contentAlignment = Alignment.Center,
            ) {
                Box(Modifier.size(24.dp).border(1.6.dp, brand.moss, CircleShape), contentAlignment = Alignment.Center) {
                    Icon(Icons.Filled.MoreHoriz, null, tint = brand.moss, modifier = Modifier.size(18.dp))
                }
            }
            DropdownMenu(expanded = menu, onDismissRequest = { menu = false }, containerColor = brand.surface) {
                @Composable
                fun item(label: Int, icon: androidx.compose.ui.graphics.vector.ImageVector, danger: Boolean = false, go: () -> Unit) =
                    DropdownMenuItem(
                        text = { Text(stringResource(label), color = if (danger) brand.dangerText else brand.ink, fontSize = 16.sp) },
                        trailingIcon = { Icon(icon, null, tint = if (danger) brand.dangerText else brand.ink, modifier = Modifier.size(20.dp)) },
                        onClick = {
                            menu = false
                            go()
                        },
                    )
                item(R.string.ot_change_name, Icons.Outlined.Edit) { onEdit(EditableField.NAME) }
                item(R.string.ot_change_species, Icons.Outlined.Eco) { onSpecies() }
                item(R.string.ot_change_age, Icons.Outlined.CalendarMonth) { onEdit(EditableField.AGE) }
                item(R.string.ot_change_girth, Icons.Outlined.Straighten) { onEdit(EditableField.GIRTH) }
                HorizontalDivider(color = brand.hairline)
                item(R.string.ot_remove_tree, Icons.Outlined.Delete, danger = true) { onRemove() }
            }
        }
    }
}

/** FieldEditor: one sheet for every blank, Cancel and Save at the top, the prompt as its title. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun FieldEditor(field: EditableField, initial: String, onCancel: () -> Unit, onSave: (String) -> Unit) {
    val brand = Brand.colors
    var text by remember { mutableStateOf(initial) }
    val focus = remember { FocusRequester() }
    LaunchedEffect(Unit) { runCatching { focus.requestFocus() } }
    val prompt = stringResource(
        when (field) {
            EditableField.NAME -> R.string.ot_prompt_name
            EditableField.AGE -> R.string.ot_prompt_age
            EditableField.GIRTH -> R.string.ot_prompt_girth
            EditableField.STORY -> R.string.ot_prompt_story
        },
    )
    ModalBottomSheet(
        onDismissRequest = onCancel,
        sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true),
        containerColor = brand.ground,
    ) {
        Column(Modifier.fillMaxWidth().padding(horizontal = 16.dp).padding(bottom = 16.dp).imePadding()) {
            Row(Modifier.fillMaxWidth().height(44.dp), verticalAlignment = Alignment.CenterVertically) {
                Text(stringResource(R.string.cancel), fontSize = 17.sp, color = brand.moss, modifier = Modifier.clickable(role = Role.Button, onClick = onCancel))
                Text(
                    prompt,
                    fontSize = 17.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = brand.ink,
                    maxLines = 1,
                    textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                    modifier = Modifier.weight(1f).padding(horizontal = 8.dp),
                )
                Text(
                    stringResource(R.string.ot_save),
                    fontSize = 17.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = brand.moss,
                    modifier = Modifier.clickable(role = Role.Button) { onSave(text.trim()) },
                )
            }
            Spacer(Modifier.height(12.dp))
            BasicTextField(
                value = text,
                onValueChange = { text = it },
                textStyle = TextStyle(fontSize = 17.sp, color = brand.ink),
                cursorBrush = SolidColor(brand.moss),
                singleLine = field != EditableField.STORY,
                minLines = if (field == EditableField.STORY) 4 else 1,
                keyboardOptions = KeyboardOptions(keyboardType = if (field == EditableField.GIRTH) KeyboardType.Decimal else KeyboardType.Text),
                modifier = Modifier.fillMaxWidth().focusRequester(focus),
                decorationBox = { inner ->
                    Box {
                        if (text.isEmpty()) Text(prompt, fontSize = 17.sp, color = brand.inkSoft.copy(alpha = 0.6f))
                        inner()
                    }
                },
            )
            if (field == EditableField.GIRTH) {
                Spacer(Modifier.height(12.dp))
                Text(stringResource(R.string.ot_girth_hint), fontSize = 13.sp, color = brand.inkSoft)
            }
            Spacer(Modifier.height(24.dp))
        }
    }
}
