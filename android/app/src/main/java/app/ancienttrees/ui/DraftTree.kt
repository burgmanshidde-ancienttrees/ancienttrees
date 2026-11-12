// A tree only you have, still being added: its own page as a draft, with Save at
// the foot. Ported from ios Screens/TreeDetail.swift where `mine` is a draft
// (Hidde, 2026-09-26: the form before the page "asks the same info", so the page
// is the form; CONVENTIONS.md, "Adding a tree: straight to its page"), its
// FieldEditor, and Screens/SpeciesChooser.swift.
//
// The draft lives in memory until Save (data/cross-device.json: unsent drafts
// are the device's); Save sends it to the account and to us as a tree, and the
// page then stays as your tree (OwnTree.kt) with Share at the foot.

package app.ancienttrees.ui



import app.ancienttrees.account.Submission

import app.ancienttrees.feed.Geo

import app.ancienttrees.feed.Tree

import android.graphics.BitmapFactory
import androidx.activity.compose.BackHandler
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.platform.LocalContext
import androidx.core.content.FileProvider
import app.ancienttrees.account.Account
import app.ancienttrees.account.MyTrees
import kotlinx.coroutines.launch
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.VerticalDivider
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.account.Collector
import app.ancienttrees.feed.Catalogue
import app.ancienttrees.feed.CollectRules
import app.ancienttrees.feed.filterSpecies

private enum class Field { NAME, AGE, GIRTH, STORY }

/** Sightings.girthCm(parsing:): metres as typed ("4.2", "4,2 m"), to centimetres. */
fun girthCm(text: String): Int? =
    text.replace(",", ".").replace(Regex("[^0-9.]"), "").toDoubleOrNull()?.takeIf { it > 0 && it < 50 }?.let { (it * 100).toInt() }

/**
 * [account] and [mine] given: Save sends the tree here and, once the account
 * holds it, THE PAGE STAYS AS YOUR TREE with Share at the foot (TreeDetail's
 * `live`: "a draft that is saved on this page turns into a saved tree on this
 * page without being opened again"), under the "Added to your trees" sheet.
 * Without them Save hands the draft to [onSave] and the page closes, as before.
 * [onDiscard] also closes the saved page. [onCity] makes the city a link.
 */
@Composable
fun DraftTree(
    draft: Collector.Draft,
    catalogue: Catalogue,
    onSave: (Collector.Draft, String?) -> Unit,
    onDiscard: () -> Unit,
    account: Account? = null,
    mine: MyTrees? = null,
    onCity: ((slug: String, name: String) -> Unit)? = null,
    /** Merged into one of ours (MergeChooser): the tick and "Trees merged" are the root's. */
    onMerged: ((Tree) -> Unit)? = null,
) {
    val brand = Brand.colors
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var name by remember { mutableStateOf(draft.name) }
    var named by remember { mutableStateOf(false) }
    var age by remember { mutableStateOf("") }
    var girth by remember { mutableStateOf<Int?>(null) }
    var species by remember { mutableStateOf("") }
    var story by remember { mutableStateOf("") }
    var extras by remember { mutableStateOf(draft.extras) }
    var editing by remember { mutableStateOf<Field?>(null) }
    var choosingSpecies by remember { mutableStateOf(false) }
    var confirmingDiscard by remember { mutableStateOf(false) }
    var removing by remember { mutableStateOf(false) }
    var placing by remember { mutableStateOf(false) }
    var merging by remember { mutableStateOf(false) }
    var saving by remember { mutableStateOf(false) }
    var saveFailed by remember { mutableStateOf(false) }
    var savedId by remember { mutableStateOf<String?>(null) }
    var savedName by remember { mutableStateOf<String?>(null) }
    // placeLink: the nearest city we publish within 30 km, as on your saved tree.
    val place = remember(draft.lat, draft.lng, catalogue) { minePlace(catalogue, draft.lat, draft.lng) }
    val city = place?.first

    // SAVED: the same page, now your tree, read from the account.
    val saved = savedId?.let { id -> mine?.takeIf { it.byId(id) != null } }
    if (saved != null) {
        OwnTree(savedId!!, saved, catalogue, onBack = onDiscard, onCity = { slug, n -> onCity?.invoke(slug, n) })
        savedName?.let { n ->
            BrandSheet(
                icon = Sym.VerifiedFill,
                // The name under the title, not in it: "You added A tree in
                // Amsterdam" reads wrong. No "with your photograph".
                title = stringResource(R.string.cf_added_title),
                message = n,
                onDismiss = { savedName = null },
                buttons = listOf(SheetButton(stringResource(R.string.cf_done), SheetKind.PRIMARY, tag = "saved-done") { savedName = null }),
            )
        }
        return
    }

    fun save() {
        val d = draft.copy(name = name, note = story, species = species.ifEmpty { null }, age = age.ifEmpty { null },
            girthCm = girth, extras = extras)
        if (account == null || mine == null) {
            onSave(d, city)
            return
        }
        if (saving) return
        saving = true
        scope.launch {
            val ok = Collector.saveDraft(account, d, city)
            if (ok) mine.keepStandIn(d)
            if (ok) mine.load(force = true)
            saving = false
            when {
                ok && mine.byId(d.id) != null -> { savedId = d.id; savedName = d.name }
                ok -> onDiscard()
                else -> saveFailed = true
            }
        }
    }

    // A FURTHER PHOTOGRAPH (morePhotosRow): camera or your photos, kept with the draft.
    val shotFile = remember { java.io.File(context.cacheDir, "photos").apply { mkdirs() }.let { java.io.File(it, "draft-extra.jpg") } }
    val shotUri = remember { FileProvider.getUriForFile(context, context.packageName + ".photos", shotFile) }
    fun addExtra(raw: ByteArray?) {
        scope.launch {
            val jpeg = raw?.let { Collector.downsized(it) } ?: return@launch
            if (extras.size < Collector.MAX_EXTRAS) extras = extras + jpeg
        }
    }
    val extraCamera = rememberLauncherForActivityResult(ActivityResultContracts.TakePicture()) { ok ->
        if (!ok) return@rememberLauncherForActivityResult
        val raw = runCatching { shotFile.readBytes() }.getOrNull()
        shotFile.delete()
        addExtra(raw)
    }
    val room = (Collector.MAX_EXTRAS - extras.size).coerceAtLeast(1)
    val extraLibrary = rememberLauncherForActivityResult(ActivityResultContracts.PickMultipleVisualMedia(maxOf(2, Collector.MAX_EXTRAS))) { uris ->
        for (u in uris.take(room)) addExtra(runCatching { context.contentResolver.openInputStream(u)?.use { it.readBytes() } }.getOrNull())
    }

    BackHandler { if (!saving) confirmingDiscard = true }

    Box(Modifier.fillMaxSize().background(brand.ground)) {
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState())) {
            val bmp = remember(draft.jpeg) {
                draft.jpeg?.takeIf { it.size > 1 }?.let { BitmapFactory.decodeByteArray(it, 0, it.size) }
            }
            // heroHeight: the photograph's shape across the page, at most 60 percent of the screen.
            val screen = androidx.compose.ui.platform.LocalConfiguration.current
            val heroH = remember(bmp, screen) {
                val w = screen.screenWidthDp.toFloat()
                val ratio = bmp?.let { it.width.toFloat() / it.height } ?: 1f
                minOf(w / ratio, screen.screenHeightDp * 0.6f).dp
            }
            Box(Modifier.fillMaxWidth().height(heroH)) {
                if (bmp != null) {
                    Image(bmp.asImageBitmap(), null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())
                }
            }
            Column(
                verticalArrangement = Arrangement.spacedBy(28.dp),
                modifier = Modifier.padding(horizontal = 20.dp).padding(top = 20.dp),
            ) {
                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text(
                        name,
                        fontFamily = BrandFace,
                        fontWeight = FontWeight.ExtraBold,
                        fontSize = 28.sp,
                        lineHeight = 33.sp,
                        color = brand.ink,
                        modifier = Modifier.clickable(role = Role.Button) { editing = Field.NAME },
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
                                modifier = if (onCity == null) Modifier else Modifier
                                    .clickable(role = Role.Button, interactionSource = remember { MutableInteractionSource() }, indication = androidx.compose.foundation.LocalIndication.current) {
                                        onCity(place.second, place.first)
                                    }
                                    .semantics { contentDescription = see }
                                    .testTag("draft-city"),
                            )
                        }
                    }
                    Facts(age, girth, species, onAge = { editing = Field.AGE }, onGirth = { editing = Field.GIRTH }, onSpecies = { choosingSpecies = true })
                }
                if (story.isEmpty()) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.heightIn(min = 44.dp).clickable(role = Role.Button) { editing = Field.STORY },
                    ) {
                        Icon(Sym.AddCircle, null, tint = brand.moss, modifier = Modifier.size(18.dp))
                        Spacer(Modifier.width(5.dp))
                        Text(stringResource(R.string.cf_special), fontSize = 15.sp, color = brand.moss)
                    }
                } else {
                    Text(story, fontSize = 17.sp, lineHeight = 22.sp, color = brand.ink, modifier = Modifier.clickable { editing = Field.STORY })
                }
                // morePhotosRow: up to three further photographs, the sign among
                // them, and the Add photo tile with camera or your photos.
                Column(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.testTag("more-photos")) {
                    Text(stringResource(R.string.cf_more_photos), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 15.sp, color = brand.ink)
                    Text(stringResource(R.string.ot_more_photos_body), fontSize = 13.sp, color = brand.inkSoft)
                    var tileMenu by remember { mutableStateOf(false) }
                    Row(Modifier.horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                        for (e in extras) {
                            val b = remember(e) { BitmapFactory.decodeByteArray(e, 0, e.size) }
                            if (b != null) {
                                Image(b.asImageBitmap(), null, contentScale = ContentScale.Crop, modifier = Modifier.size(88.dp).clip(RoundedCornerShape(12.dp)))
                            }
                        }
                        if (extras.size < Collector.MAX_EXTRAS) {
                            Box {
                                Column(
                                    Modifier
                                        .size(88.dp)
                                        .background(brand.surfaceMuted, RoundedCornerShape(12.dp))
                                        .clickable(role = Role.Button) { tileMenu = true }
                                        .testTag("add-extra-photo"),
                                    horizontalAlignment = Alignment.CenterHorizontally,
                                    verticalArrangement = Arrangement.spacedBy(6.dp, Alignment.CenterVertically),
                                ) {
                                    Icon(Sym.Add, null, tint = brand.moss, modifier = Modifier.size(22.dp))
                                    Text(stringResource(R.string.ot_add_photo), fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = brand.moss)
                                }
                                DropdownMenu(expanded = tileMenu, onDismissRequest = { tileMenu = false }, containerColor = brand.surface) {
                                    DropdownMenuItem(
                                        text = { Text(stringResource(R.string.collect_camera), color = brand.ink, fontSize = 16.sp) },
                                        trailingIcon = { Icon(Sym.PhotoCamera, null, tint = brand.ink) },
                                        onClick = {
                                            tileMenu = false
                                            runCatching { extraCamera.launch(shotUri) }
                                        },
                                    )
                                    DropdownMenuItem(
                                        text = { Text(stringResource(R.string.cf_choose), color = brand.ink, fontSize = 16.sp) },
                                        trailingIcon = { Icon(Sym.PhotoLibrary, null, tint = brand.ink) },
                                        onClick = {
                                            tileMenu = false
                                            extraLibrary.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
                                        },
                                    )
                                }
                            }
                        }
                    }
                }
                Spacer(Modifier.height(90.dp))
            }
        }

        // The back circle, which asks before anything is thrown away, and the
        // ellipsis menu your saved tree carries: the fields you can fill, then
        // Remove, last and marked (TreeDetail's mine-menu, drafts included).
        DraftTopButtons(
            onBack = { if (!saving) confirmingDiscard = true },
            onEdit = { editing = it },
            onSpecies = { choosingSpecies = true },
            onRemove = { removing = true },
            onMovePin = { placing = true },
            onMerge = if (account != null && onMerged != null) ({ merging = true }) else null,
        )

        // SAVE, on a tree still being added: the bar at the foot. After it the
        // page stays and this becomes Share (OwnTree above).
        Column(Modifier.align(Alignment.BottomCenter).fillMaxWidth().background(brand.ground)) {
            HorizontalDivider(color = brand.hairline)
            SheetButtonView(
                SheetButton(stringResource(if (saving) R.string.cf_adding else R.string.cf_save_tree), SheetKind.PRIMARY, Sym.Check) { save() },
                Modifier.padding(horizontal = 20.dp, vertical = 10.dp).navigationBarsPadding().testTag("draft-save"),
            )
        }
    }
    if (saveFailed) CollectFailedSheet(onDismiss = { saveFailed = false })
    // MOVE THE PIN (TreeDetail's mine-menu): the same full-screen map as on ours.
    if (placing && account != null) {
        PlacePin(
            tree = draftTree(draft, name, species),
            account = account,
            signedIn = true,
            onNeedsSignIn = { },
            onDismiss = { placing = false },
        )
    }
    // MERGE WITH ANOTHER TREE (TreeDetail.merge): the photographs go to that tree
    // of ours and it is ticked, instantly; further than 400 m it is also the pin
    // correction CollectSheet.reportPin sends.
    if (merging && account != null) {
        MergeChooser(
            catalogue = catalogue,
            lat = draft.lat,
            lng = draft.lng,
            onMerge = { t ->
                scope.launch {
                    val jpeg = draft.jpeg
                    val ok = if (jpeg != null) {
                        Collector.collect(account, t.id, t.name, jpeg, draft.lat, draft.lng, extras, draft.taken)
                    } else {
                        Collector.tick(account, t.id)
                    }
                    val metres = (Geo.km(draft.lat, draft.lng, t.lat, t.lng) * 1000).toInt()
                    if (ok && metres > 400) {
                        Submission.correction(
                            t.city, t.name,
                            String.format(java.util.Locale.ROOT, "%.6f, %.6f (%s)", draft.lat, draft.lng, draft.fixNote.ifEmpty { "where the person's own tree stands" }),
                            "A tree the person added, merged into this one $metres m from the published position. " +
                                "Our pin was ${if (t.precision == app.ancienttrees.feed.Precision.CONFIRMED) "marked confirmed" else "marked approximate"}.",
                            t.url, account.fresh()?.accessToken,
                        )
                    }
                    if (ok) onMerged?.invoke(t) else saveFailed = true
                }
            },
            onClose = { merging = false },
        )
    }
    if (removing) {
        BrandSheet(
            title = stringResource(R.string.ot_remove_title, name),
            message = stringResource(R.string.ot_remove_body),
            onDismiss = { removing = false },
            buttons = listOf(
                SheetButton(stringResource(R.string.ot_remove), SheetKind.DESTRUCTIVE) {
                    removing = false
                    onDiscard()
                },
                SheetButton(stringResource(R.string.ot_keep), SheetKind.SECONDARY) { removing = false },
            ),
        )
    }

    Lingering(editing) { f ->
        FieldEditor(
            prompt = stringResource(
                when (f) {
                    Field.NAME -> R.string.cf_q_name
                    Field.AGE -> R.string.cf_q_age
                    Field.GIRTH -> R.string.cf_q_girth
                    Field.STORY -> R.string.cf_special
                },
            ),
            hint = if (f == Field.GIRTH) stringResource(R.string.cf_girth_hint) else null,
            initial = when (f) {
                Field.NAME -> name
                Field.AGE -> age
                Field.GIRTH -> girth?.let { String.format(java.util.Locale.ROOT, "%.1f", it / 100.0) }.orEmpty()
                Field.STORY -> story
            },
            long = f == Field.STORY,
            onSave = { text ->
                when (f) {
                    Field.NAME -> if (text.isNotEmpty()) { name = text; named = true }
                    Field.AGE -> age = text
                    Field.GIRTH -> girth = if (text.isEmpty()) null else girthCm(text) ?: girth
                    Field.STORY -> story = text
                }
                editing = null
            },
            onCancel = { editing = null },
        )
    }
    if (choosingSpecies) {
        SpeciesChooser(
            catalogue = catalogue,
            nearby = CollectRules.nearby(draft.lat, draft.lng, catalogue.trees).map { it.commonName },
            current = species,
            onPick = { picked ->
                species = picked
                // Sightings.fallbackName: "Oak in Nara" the moment a species is known.
                if (!named) {
                    val kind = picked.substringBefore("(").trim()
                    name = draft.place?.let { "$kind $it" } ?: kind
                }
                choosingSpecies = false
            },
            onClose = { choosingSpecies = false },
        )
    }
    if (confirmingDiscard) {
        BrandSheet(
            title = stringResource(R.string.cf_discard_title),
            message = stringResource(R.string.cf_discard_body),
            onDismiss = { confirmingDiscard = false },
            buttons = listOf(
                SheetButton(stringResource(R.string.cf_discard), SheetKind.DESTRUCTIVE) {
                    confirmingDiscard = false
                    onDiscard()
                },
                SheetButton(stringResource(R.string.cf_keep_editing), SheetKind.SECONDARY) { confirmingDiscard = false },
            ),
        )
    }
}

/** OwnTree's top row on a draft: back that asks, and the ⋯ menu (TreeDetail's mine-menu). */
@Composable
private fun DraftTopButtons(
    onBack: () -> Unit,
    onEdit: (Field) -> Unit,
    onSpecies: () -> Unit,
    onRemove: () -> Unit,
    onMovePin: () -> Unit,
    onMerge: (() -> Unit)?,
) {
    val brand = Brand.colors
    var menu by remember { mutableStateOf(false) }
    Row(
        // At the top of the safe area, as the iPhone's toolbar (BackButton {16, 62}).
        Modifier.fillMaxWidth().statusBarsPadding().padding(horizontal = 16.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        val back = stringResource(R.string.cf_back)
        Box(
            Modifier.size(44.dp).softDisc()
                .clickable(role = Role.Button, onClick = onBack).semantics { contentDescription = back }.testTag("draft-back"),
            contentAlignment = Alignment.Center,
        ) {
            Icon(Sym.ArrowBack, null, tint = brand.moss, modifier = Modifier.size(20.dp))
        }
        Spacer(Modifier.weight(1f))
        val more = stringResource(R.string.ot_more)
        Box {
            Box(
                Modifier.size(44.dp).softDisc()
                    .clickable(role = Role.Button) { menu = true }.semantics { contentDescription = more }.testTag("mine-menu"),
                contentAlignment = Alignment.Center,
            ) {
                Box(Modifier.size(24.dp).border(1.6.dp, brand.moss, CircleShape), contentAlignment = Alignment.Center) {
                    Icon(Sym.MoreVert, null, tint = brand.moss, modifier = Modifier.size(22.dp)) // overflow: Android's form
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
                item(R.string.ot_change_name, Sym.Edit) { onEdit(Field.NAME) }
                item(R.string.ot_change_species, Sym.Leaf) { onSpecies() }
                item(R.string.ot_change_age, Sym.CalendarMonth) { onEdit(Field.AGE) }
                item(R.string.ot_change_girth, Sym.Straighten) { onEdit(Field.GIRTH) }
                item(R.string.ot_move_pin, Sym.PinDrop) { onMovePin() }
                // A draft is neither ours nor folded into ours yet, so it may merge.
                if (onMerge != null) item(R.string.ot_merge, Sym.Merge) { onMerge() }
                HorizontalDivider(color = brand.hairline)
                item(R.string.ot_remove_tree, Sym.Delete, danger = true) { onRemove() }
            }
        }
    }
}

/** The bordered block, labels on top: Age and Girth side by side, Species under them. */
@Composable
private fun Facts(age: String, girth: Int?, species: String, onAge: () -> Unit, onGirth: () -> Unit, onSpecies: () -> Unit) {
    val brand = Brand.colors
    Column(
        Modifier
            .padding(top = 10.dp)
            .fillMaxWidth()
            .border(1.dp, brand.hairline, RoundedCornerShape(14.dp))
            .padding(horizontal = 16.dp, vertical = 12.dp),
    ) {
        Row(Modifier.height(androidx.compose.foundation.layout.IntrinsicSize.Min)) {
            FactColumn(stringResource(R.string.cf_age), age.ifEmpty { null }, Modifier.weight(1f), onAge)
            VerticalDivider(color = brand.hairline, modifier = Modifier.padding(horizontal = 12.dp))
            FactColumn(stringResource(R.string.cf_girth), girth?.let { metres(it) }, Modifier.weight(1f), onGirth)
        }
        HorizontalDivider(color = brand.hairline, modifier = Modifier.padding(vertical = 10.dp))
        FactColumn(stringResource(R.string.cf_species), species.substringBefore("(").trim().ifEmpty { null }, Modifier.fillMaxWidth(), onSpecies)
    }
}

@Composable
private fun FactColumn(label: String, value: String?, modifier: Modifier, onClick: () -> Unit) {
    val brand = Brand.colors
    Column(modifier.heightIn(min = 44.dp).clickable(role = Role.Button, onClick = onClick), verticalArrangement = Arrangement.spacedBy(2.dp)) {
        Text(label, fontSize = 13.sp, color = brand.inkSoft)
        if (value == null) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Sym.AddCircle, null, tint = brand.moss, modifier = Modifier.size(15.dp))
                Spacer(Modifier.width(4.dp))
                Text(stringResource(R.string.cf_add), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = brand.moss)
            }
        } else {
            Text(value, fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 19.sp, color = brand.ink, maxLines = 2)
        }
    }
}

/** FieldEditor: one sheet for every blank, Cancel and Save over the field. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun FieldEditor(prompt: String, hint: String?, initial: String, long: Boolean, onSave: (String) -> Unit, onCancel: () -> Unit) {
    val brand = Brand.colors
    var text by remember { mutableStateOf(initial) }
    val focus = remember { FocusRequester() }
    LaunchedEffect(Unit) { runCatching { focus.requestFocus() } }
    AppSheet(onDismissRequest = onCancel, containerColor = brand.ground) {
        Column(Modifier.fillMaxWidth().padding(horizontal = 16.dp).padding(bottom = 16.dp).navigationBarsPadding(), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(stringResource(R.string.cf_cancel), fontSize = 17.sp, color = brand.moss, modifier = Modifier.clickable(role = Role.Button, onClick = onCancel).padding(8.dp))
                Text(prompt, fontSize = 17.sp, fontWeight = FontWeight.SemiBold, color = brand.ink, modifier = Modifier.weight(1f), textAlign = androidx.compose.ui.text.style.TextAlign.Center, maxLines = 1)
                Text(stringResource(R.string.cf_save), fontSize = 17.sp, fontWeight = FontWeight.SemiBold, color = brand.moss, modifier = Modifier.clickable(role = Role.Button) { onSave(text.trim()) }.padding(8.dp))
            }
            Box(Modifier.fillMaxWidth().heightIn(min = if (long) 120.dp else 44.dp).background(brand.surfaceMuted, RoundedCornerShape(10.dp)).padding(12.dp)) {
                BasicTextField(
                    value = text,
                    onValueChange = { text = it },
                    singleLine = !long,
                    textStyle = sfStyle(fontSize = 17.sp, color = brand.ink),
                    cursorBrush = SolidColor(brand.moss),
                    modifier = Modifier.fillMaxWidth().focusRequester(focus),
                )
                if (text.isEmpty()) Text(prompt, fontSize = 17.sp, color = brand.inkSoft)
            }
            hint?.let { Text(it, fontSize = 13.sp, color = brand.inkSoft) }
        }
    }
}

/** The draft as a tree, for the pin map (Sightings.asTree). */
private fun draftTree(d: Collector.Draft, name: String, species: String): Tree = Tree(
    id = "mine-" + d.id,
    name = name,
    species = species,
    age = null,
    ageShort = null,
    lat = d.lat,
    lng = d.lng,
    city = d.place.orEmpty(),
    citySlug = "",
    country = "",
    neighbourhood = "",
    access = "",
    paidEntry = false,
    transport = "",
    story = "",
    storyLatin = emptyList(),
    howToRecognise = "",
    url = "",
    precision = app.ancienttrees.feed.Precision.CONFIRMED,
    photo = null,
    saves = 0,
    mini = false,
)

/**
 * The iPhone's toolbar buttons on your own tree and a draft: a white disc with a
 * soft, wide shadow and no edge, the Discover search field's shadow (Compose
 * scales shadow colour down, so these numbers give the iPhone's softness).
 */
@Composable
internal fun Modifier.softDisc(): Modifier = this
    .shadow(6.dp, CircleShape, ambientColor = androidx.compose.ui.graphics.Color.Black.copy(alpha = 0.18f), spotColor = androidx.compose.ui.graphics.Color.Black.copy(alpha = 0.32f))
    .background(Brand.colors.surface, CircleShape)
