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
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
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
fun TreeScreen(tree: Tree, hearted: Boolean, onHeart: () -> Unit, onBack: () -> Unit) {
    val context = LocalContext.current
    Box(Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState())) {
            val photo = tree.photo
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

                // The one warning this product must never soften.
                if (tree.precision == Precision.APPROXIMATE) {
                    Text(
                        stringResource(R.string.location_approximate),
                        style = MaterialTheme.typography.bodySmall,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.onBackground,
                    )
                }

                Button(
                    onClick = { directions(context, tree) },
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Text(stringResource(R.string.take_me_there))
                }

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
