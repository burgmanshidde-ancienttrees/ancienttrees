// A tapped tree's card on the map, and the tree's page.

package app.ancienttrees.ui

import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.FavoriteBorder
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import app.ancienttrees.feed.Seasons
import androidx.compose.runtime.setValue
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.feed.Precision
import app.ancienttrees.feed.Tree

@Composable
fun TreeCard(
    tree: Tree,
    distance: String?,
    onOpen: () -> Unit,
    onClose: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Surface(
        shape = RoundedCornerShape(16.dp),
        shadowElevation = 8.dp,
        modifier = modifier.fillMaxWidth().clickable(onClick = onOpen),
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            val photo = tree.photo
            if (photo != null) {
                RemoteImage(photo.card, tree.name, Modifier.size(96.dp))
            }
            Column(Modifier.weight(1f).padding(horizontal = 12.dp, vertical = 10.dp)) {
                Text(
                    tree.name,
                    fontFamily = Brand,
                    fontWeight = FontWeight.Bold,
                    fontSize = 17.sp,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                )
                Text(
                    listOfNotNull(tree.commonName, tree.ageShort).joinToString(" · "),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
                Text(
                    listOfNotNull(tree.city, distance).joinToString(" · "),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
            }
            IconButton(onClick = onClose) {
                Icon(Icons.Filled.Close, contentDescription = stringResource(R.string.close))
            }
        }
    }
}

private fun storyText(tree: Tree): AnnotatedString = AnnotatedString.Builder(tree.story).apply {
    for (run in tree.storyLatin) {
        if (run.last < tree.story.length) {
            addStyle(SpanStyle(fontStyle = FontStyle.Italic), run.first, run.last + 1)
        }
    }
}.toAnnotatedString()

private fun openUrl(context: Context, url: String) {
    try {
        context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
    } catch (_: ActivityNotFoundException) {
        // Nothing on this phone opens a web address; the button then does nothing.
    }
}

/** Walking directions in whichever maps app the phone has. */
private fun directions(context: Context, tree: Tree) = openUrl(
    context,
    "https://www.google.com/maps/dir/?api=1&destination=${tree.lat},${tree.lng}&travelmode=walking",
)

@Composable
fun TreeScreen(
    tree: Tree,
    hearted: Boolean,
    onHeart: () -> Unit,
    onBack: () -> Unit,
    canCollect: Boolean = false,
    collected: Boolean = false,
    collecting: Boolean = false,
    onCollect: () -> Unit = {},
) {
    val context = LocalContext.current
    Box(Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState())) {
            // The lead, or the photograph a season tile chose.
            var shown by remember(tree.id) { mutableIntStateOf(0) }
            val photo = tree.shots.getOrNull(shown) ?: tree.photo
            if (photo != null) {
                RemoteImage(
                    photo.full,
                    tree.name,
                    Modifier.fillMaxWidth().aspectRatio((photo.frame ?: 1.5).toFloat()),
                )
                photo.credit?.let { credit ->
                    val line = stringResource(R.string.photo_credit, credit)
                    val link = photo.creditUrl
                    Text(
                        line,
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        textDecoration = if (link != null) TextDecoration.Underline else null,
                        modifier = Modifier
                            .padding(horizontal = 16.dp, vertical = 6.dp)
                            .then(if (link != null) Modifier.clickable { openUrl(context, link) } else Modifier),
                    )
                }
            } else {
                Spacer(Modifier.statusBarsPadding().height(56.dp))
            }

            Column(
                Modifier.padding(horizontal = 16.dp, vertical = 12.dp).navigationBarsPadding(),
                verticalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Column {
                    Text(
                        tree.name,
                        fontFamily = Brand,
                        fontWeight = FontWeight.Bold,
                        fontSize = 26.sp,
                        lineHeight = 31.sp,
                        color = MaterialTheme.colorScheme.onBackground,
                    )
                    Text(
                        listOfNotNull(tree.commonName, tree.ageShort, tree.city).joinToString(" · "),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }

                // AT ITS BEST NOW: the chip the website and the iPhone show
                // while the tree's one real peak is on.
                val month = remember { java.util.Calendar.getInstance().get(java.util.Calendar.MONTH) + 1 }
                if (tree.atBest(month)) {
                    seasonChip(tree.seasonKey)?.let { chip ->
                        Text(
                            chip,
                            fontWeight = FontWeight.SemiBold,
                            fontSize = 13.sp,
                            color = Color(0xFF10160A),
                            modifier = Modifier
                                .clip(RoundedCornerShape(50))
                                .background(Color(0xFFD9A13F))
                                .padding(horizontal = 10.dp, vertical = 4.dp),
                        )
                    }
                }

                // The one warning this product must never soften.
                if (tree.precision == Precision.APPROXIMATE) {
                    Text(
                        stringResource(R.string.location_approximate),
                        style = MaterialTheme.typography.bodySmall,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.onBackground,
                    )
                }

                // COLLECT IS THE BIG ONE when you are near enough to stand in
                // front of it (the iPhone's tree page); directions otherwise.
                when {
                    collected -> {
                        Text(
                            "\u2713 " + stringResource(R.string.seen_it_done),
                            fontWeight = FontWeight.SemiBold,
                            color = MaterialTheme.colorScheme.primary,
                        )
                        OutlinedButton(onClick = { directions(context, tree) }, modifier = Modifier.fillMaxWidth()) {
                            Text(stringResource(R.string.take_me_there))
                        }
                    }
                    canCollect -> {
                        Button(onClick = onCollect, enabled = !collecting, modifier = Modifier.fillMaxWidth()) {
                            Text(stringResource(R.string.seen_it))
                        }
                        OutlinedButton(onClick = { directions(context, tree) }, modifier = Modifier.fillMaxWidth()) {
                            Text(stringResource(R.string.take_me_there))
                        }
                    }
                    else -> {
                        Button(onClick = { directions(context, tree) }, modifier = Modifier.fillMaxWidth()) {
                            Text(stringResource(R.string.take_me_there))
                        }
                    }
                }

                SeasonsRow(
                    tree = tree,
                    month = month,
                    onShow = { shown = it },
                    onAsk = if (canCollect && !collected) onCollect else null,
                )

                Text(
                    storyText(tree),
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onBackground,
                )

                val lines = listOf(
                    tree.howToRecognise,
                    if (tree.showsAccess) tree.access else "",
                    tree.transport,
                ).map { it.trim() }.filter { it.isNotEmpty() }
                if (lines.isNotEmpty()) {
                    Text(
                        stringResource(R.string.getting_there),
                        fontWeight = FontWeight.Bold,
                        fontSize = 18.sp,
                        color = MaterialTheme.colorScheme.onBackground,
                    )
                    lines.forEach {
                        Text(
                            it,
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onBackground,
                        )
                    }
                }
                Spacer(Modifier.height(16.dp))
            }
        }

        IconButton(
            onClick = onBack,
            modifier = Modifier
                .statusBarsPadding()
                .padding(8.dp)
                .clip(CircleShape)
                .background(Color.Black.copy(alpha = 0.45f)),
        ) {
            Icon(
                Icons.AutoMirrored.Filled.ArrowBack,
                contentDescription = stringResource(R.string.back),
                tint = Color.White,
            )
        }

        // WANT TO GO, top right over the photograph, where Airbnb keeps the
        // heart on a listing. Signed out, it asks to sign in first.
        IconButton(
            onClick = onHeart,
            modifier = Modifier
                .align(Alignment.TopEnd)
                .statusBarsPadding()
                .padding(8.dp)
                .clip(CircleShape)
                .background(Color.Black.copy(alpha = 0.45f)),
        ) {
            Icon(
                if (hearted) Icons.Filled.Favorite else Icons.Filled.FavoriteBorder,
                contentDescription = stringResource(R.string.want_to_go),
                tint = if (hearted) Color(0xFFE0454F) else Color.White,
            )
        }
    }
}

@Composable
private fun seasonChip(key: String?): String? = when (key) {
    "bloom" -> stringResource(R.string.season_chip_bloom)
    "autumn" -> stringResource(R.string.season_chip_autumn)
    "fruit" -> stringResource(R.string.season_chip_fruit)
    "leaves" -> stringResource(R.string.season_chip_leaves)
    "catkins" -> stringResource(R.string.season_chip_catkins)
    "winter" -> stringResource(R.string.season_chip_winter)
    "peak" -> stringResource(R.string.season_chip_peak)
    else -> null
}

@Composable
private fun seasonName(key: String): String = stringResource(
    when (key) {
        "spring" -> R.string.season_spring
        "summer" -> R.string.season_summer
        "autumn" -> R.string.season_autumn
        else -> R.string.season_winter
    },
)

/**
 * Four tiles, one per season: a filled one shows that photograph in the hero, the
 * empty tile of the season it is now asks for one when the person can collect
 * here ([onAsk]); other empty tiles are not buttons.
 */
@Composable
private fun SeasonsRow(tree: Tree, month: Int, onShow: (Int) -> Unit, onAsk: (() -> Unit)?) {
    val tiles = Seasons.tiles(tree)
    if (tiles.isEmpty()) return
    val now = Seasons.now(month, tree.lat)
    val filled = tiles.count { it.first != null }
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Row(verticalAlignment = Alignment.Bottom) {
            Text(stringResource(R.string.seasons_heading), fontFamily = Brand, fontWeight = FontWeight.Bold,
                fontSize = 18.sp, modifier = Modifier.weight(1f))
            Text(stringResource(R.string.seasons_tally, filled), fontSize = 14.sp,
                color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            for (tile in tiles) {
                val shot = tile.first?.let { tree.shots[it] }
                val ask = if (shot == null && tile.key == now) onAsk else null
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(6.dp),
                    modifier = Modifier
                        .weight(1f)
                        .then(
                            when {
                                shot != null -> Modifier.clickable { onShow(tile.first!!) }
                                ask != null -> Modifier.clickable { ask() }
                                else -> Modifier
                            },
                        ),
                ) {
                    val shape = RoundedCornerShape(12.dp)
                    Box(
                        Modifier
                            .fillMaxWidth()
                            .aspectRatio(1f)
                            .clip(shape)
                            .background(
                                if (shot == null && tile.key == now) MaterialTheme.colorScheme.surfaceVariant
                                else MaterialTheme.colorScheme.onSurface.copy(alpha = 0.06f),
                            ),
                        contentAlignment = Alignment.Center,
                    ) {
                        if (shot != null) {
                            RemoteImage(shot.card, seasonName(tile.key), Modifier.fillMaxSize())
                        } else if (tile.key == now) {
                            Text(stringResource(R.string.season_now), fontWeight = FontWeight.Bold, fontSize = 12.sp,
                                color = MaterialTheme.colorScheme.primary)
                        }
                    }
                    Text(seasonName(tile.key), fontWeight = FontWeight.SemiBold, fontSize = 13.sp)
                }
            }
        }
        if (filled == 4) {
            Text("\u2713 " + stringResource(R.string.seasons_all), fontWeight = FontWeight.SemiBold, fontSize = 14.sp,
                color = MaterialTheme.colorScheme.primary)
        }
    }
}
