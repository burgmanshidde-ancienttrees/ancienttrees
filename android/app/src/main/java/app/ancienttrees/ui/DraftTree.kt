// A tree only you have, still being added: its own page as a draft, with Save at
// the foot. Ported from ios Screens/TreeDetail.swift where `mine` is a draft
// (Hidde, 2026-09-26: the form before the page "asks the same info", so the page
// is the form; CONVENTIONS.md, "Adding a tree: straight to its page"), its
// FieldEditor, and Screens/SpeciesChooser.swift.
//
// The draft lives in memory until Save (data/cross-device.json: unsent drafts
// are the device's); Save sends it to the account and to us as a tree.

package app.ancienttrees.ui

import android.graphics.BitmapFactory
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.outlined.AddCircleOutline
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Text
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

@Composable
fun DraftTree(
    draft: Collector.Draft,
    catalogue: Catalogue,
    onSave: (Collector.Draft, String?) -> Unit,
    onDiscard: () -> Unit,
) {
    val brand = Brand.colors
    var name by remember { mutableStateOf(draft.name) }
    var named by remember { mutableStateOf(false) }
    var age by remember { mutableStateOf("") }
    var girth by remember { mutableStateOf<Int?>(null) }
    var species by remember { mutableStateOf("") }
    var story by remember { mutableStateOf("") }
    var editing by remember { mutableStateOf<Field?>(null) }
    var choosingSpecies by remember { mutableStateOf(false) }
    var confirmingDiscard by remember { mutableStateOf(false) }
    val nearest = remember { CollectRules.nearestTree(draft.lat, draft.lng, catalogue.trees) }
    val city = nearest?.first?.city

    BackHandler { confirmingDiscard = true }

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
                    city?.let { Text(it, fontSize = 15.sp, color = brand.ink, textDecoration = TextDecoration.Underline) }
                    Facts(age, girth, species, onAge = { editing = Field.AGE }, onGirth = { editing = Field.GIRTH }, onSpecies = { choosingSpecies = true })
                }
                if (story.isEmpty()) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.heightIn(min = 44.dp).clickable(role = Role.Button) { editing = Field.STORY },
                    ) {
                        Icon(Icons.Outlined.AddCircleOutline, null, tint = brand.moss, modifier = Modifier.size(18.dp))
                        Spacer(Modifier.width(5.dp))
                        Text(stringResource(R.string.cf_special), fontSize = 15.sp, color = brand.moss)
                    }
                } else {
                    Text(story, fontSize = 17.sp, lineHeight = 22.sp, color = brand.ink, modifier = Modifier.clickable { editing = Field.STORY })
                }
                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text(stringResource(R.string.cf_more_photos), fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 15.sp, color = brand.ink)
                    if (draft.extras.isNotEmpty()) {
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            for (e in draft.extras) {
                                val b = remember(e) { BitmapFactory.decodeByteArray(e, 0, e.size) }
                                if (b != null) {
                                    Image(b.asImageBitmap(), null, contentScale = ContentScale.Crop, modifier = Modifier.size(84.dp).clip(RoundedCornerShape(11.dp)))
                                }
                            }
                        }
                    }
                }
                Spacer(Modifier.height(90.dp))
            }
        }

        // The back circle, top left, which asks before anything is thrown away.
        val back = stringResource(R.string.cf_back)
        Box(
            contentAlignment = Alignment.Center,
            modifier = Modifier
                .statusBarsPadding()
                .padding(start = 16.dp, top = 8.dp)
                .size(40.dp)
                .shadow(3.dp, CircleShape)
                .background(brand.ground, CircleShape)
                .clickable(role = Role.Button) { confirmingDiscard = true }
                .semantics { contentDescription = back }
                .testTag("draft-back"),
        ) {
            Icon(Icons.AutoMirrored.Filled.ArrowBack, null, tint = brand.ink, modifier = Modifier.size(20.dp))
        }

        // SAVE, on a tree still being added: the bar at the foot.
        Column(Modifier.align(Alignment.BottomCenter).fillMaxWidth().background(brand.ground)) {
            HorizontalDivider(color = brand.hairline)
            SheetButtonView(
                SheetButton(stringResource(R.string.cf_save_tree), SheetKind.PRIMARY, Icons.Filled.Check) {
                    onSave(
                        draft.copy(
                            name = name,
                            note = story,
                            species = species.ifEmpty { null },
                            age = age.ifEmpty { null },
                            girthCm = girth,
                        ),
                        city,
                    )
                },
                Modifier.padding(horizontal = 20.dp, vertical = 10.dp).navigationBarsPadding().testTag("draft-save"),
            )
        }
    }

    editing?.let { f ->
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
                Icon(Icons.Outlined.AddCircleOutline, null, tint = brand.moss, modifier = Modifier.size(15.dp))
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
    ModalBottomSheet(onDismissRequest = onCancel, sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true), containerColor = brand.ground) {
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
                    textStyle = TextStyle(fontSize = 17.sp, color = brand.ink),
                    cursorBrush = SolidColor(brand.moss),
                    modifier = Modifier.fillMaxWidth().focusRequester(focus),
                )
                if (text.isEmpty()) Text(prompt, fontSize = 17.sp, color = brand.inkSoft)
            }
            hint?.let { Text(it, fontSize = 13.sp, color = brand.inkSoft) }
        }
    }
}

/** SpeciesChooser.swift: the list, ordered by what grows around you, and searchable. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun SpeciesChooser(catalogue: Catalogue, nearby: List<String>, current: String, onPick: (String) -> Unit, onClose: () -> Unit) {
    val brand = Brand.colors
    var query by remember { mutableStateOf("") }
    val index = remember(catalogue) {
        val near = nearby.toSet()
        catalogue.bySpecies.filterKeys { it.isNotEmpty() }.map { it.key to it.value.size }
            .sortedWith(compareBy<Pair<String, Int>>({ it.first !in near }, { -it.second }, { it.first }))
    }
    val counts = remember(index) { index.toMap() }
    val typed = query.trim()
    val rows = if (typed.isEmpty()) index.map { it.first } else catalogue.filterSpecies(index.map { it.first }, typed).map { it.first }
    val mayTypeOwn = typed.length >= 3 && rows.none { CollectRules.fold(it) == CollectRules.fold(typed) }
    ModalBottomSheet(onDismissRequest = onClose, sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true), containerColor = brand.ground) {
        Column(Modifier.fillMaxWidth().fillMaxSize()) {
            Row(Modifier.fillMaxWidth().padding(horizontal = 8.dp), verticalAlignment = Alignment.CenterVertically) {
                Text(stringResource(R.string.cf_close), fontSize = 17.sp, color = brand.moss, modifier = Modifier.clickable(role = Role.Button, onClick = onClose).padding(8.dp))
                Text(stringResource(R.string.cf_kind_q), fontSize = 17.sp, fontWeight = FontWeight.SemiBold, color = brand.ink, modifier = Modifier.weight(1f), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                Spacer(Modifier.width(60.dp))
            }
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.padding(16.dp).fillMaxWidth().heightIn(min = 44.dp).background(brand.surfaceMuted, RoundedCornerShape(12.dp)).padding(horizontal = 12.dp),
            ) {
                Icon(Icons.Outlined.Search, null, tint = brand.inkSoft, modifier = Modifier.size(20.dp))
                Spacer(Modifier.width(8.dp))
                Box(Modifier.weight(1f)) {
                    BasicTextField(query, { query = it }, singleLine = true, textStyle = TextStyle(fontSize = 17.sp, color = brand.ink), cursorBrush = SolidColor(brand.moss), modifier = Modifier.fillMaxWidth())
                    if (query.isEmpty()) Text(stringResource(R.string.cf_kind_search), fontSize = 17.sp, color = brand.inkSoft)
                }
            }
            LazyColumn(Modifier.fillMaxWidth().weight(1f).navigationBarsPadding()) {
                if (typed.isEmpty() && nearby.isNotEmpty()) {
                    item { Text(stringResource(R.string.cf_near_first), fontSize = 13.sp, color = brand.inkSoft, modifier = Modifier.padding(horizontal = 20.dp, vertical = 6.dp)) }
                }
                items(rows) { n ->
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.fillMaxWidth().heightIn(min = 48.dp).clickable { onPick(n) }.padding(horizontal = 20.dp),
                    ) {
                        SpeciesMark(n, brand.moss, Modifier.size(26.dp))
                        Spacer(Modifier.width(12.dp))
                        Text(n, fontSize = 17.sp, color = brand.ink, modifier = Modifier.weight(1f))
                        if (n.equals(current.substringBefore("(").trim(), ignoreCase = true)) {
                            Icon(Icons.Filled.Check, null, tint = brand.moss)
                        } else {
                            Text("${counts[n] ?: 0}", fontSize = 15.sp, color = brand.inkSoft)
                        }
                    }
                }
                if (mayTypeOwn) {
                    item {
                        Column(Modifier.padding(horizontal = 20.dp, vertical = 8.dp)) {
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                modifier = Modifier.fillMaxWidth().heightIn(min = 48.dp).clickable { onPick(typed) },
                            ) {
                                Icon(Icons.Outlined.AddCircleOutline, null, tint = brand.moss, modifier = Modifier.size(26.dp))
                                Spacer(Modifier.width(12.dp))
                                Text(stringResource(R.string.cf_use_typed, typed), fontSize = 17.sp, color = brand.ink)
                            }
                            Text(stringResource(R.string.cf_use_typed_foot), fontSize = 13.sp, color = brand.inkSoft)
                        }
                    }
                }
            }
        }
    }
}
