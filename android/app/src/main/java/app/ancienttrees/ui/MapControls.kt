// What sits on and under the map: the location-off chip (Apple Maps' pill,
// CONVENTIONS.md "A permission somebody refused"), the my-location button, and
// the list of the trees the map shows (Airbnb's count, the website's explore list).

package app.ancienttrees.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.LocationOff
import androidx.compose.material.icons.filled.MyLocation
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.pluralStringResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.feed.Geo
import app.ancienttrees.feed.Here
import app.ancienttrees.feed.InView
import app.ancienttrees.feed.Tree

@Composable
fun LocationOffChip(refused: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier) {
    Surface(
        shape = RoundedCornerShape(50),
        shadowElevation = 4.dp,
        modifier = modifier.clip(RoundedCornerShape(50)).clickable(onClick = onClick),
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(6.dp),
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
        ) {
            Icon(Icons.Filled.LocationOff, contentDescription = null, modifier = Modifier.size(16.dp))
            Text(stringResource(R.string.location_off), style = MaterialTheme.typography.labelLarge)
            Text("·", color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text(
                stringResource(if (refused) R.string.turn_on_location else R.string.use_my_location),
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary,
            )
        }
    }
}

@Composable
fun MyLocationButton(onClick: () -> Unit, modifier: Modifier = Modifier) {
    Surface(
        shape = CircleShape,
        shadowElevation = 4.dp,
        modifier = modifier.size(48.dp).clip(CircleShape).clickable(onClick = onClick),
    ) {
        Icon(
            Icons.Filled.MyLocation,
            contentDescription = stringResource(R.string.my_location),
            tint = MaterialTheme.colorScheme.primary,
            modifier = Modifier.padding(12.dp),
        )
    }
}

@Composable
fun TreeList(inView: InView, here: Here?, miles: Boolean, onOpen: (Tree) -> Unit) {
    Column(Modifier.fillMaxWidth()) {
        Text(
            pluralStringResource(R.plurals.trees_in_view, inView.total, inView.total),
            fontWeight = FontWeight.Bold,
            fontSize = 16.sp,
            textAlign = TextAlign.Center,
            modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
        )
        LazyColumn(Modifier.fillMaxWidth().navigationBarsPadding()) {
            items(inView.trees, key = { it.id }) { tree ->
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { onOpen(tree) }
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                ) {
                    val photo = tree.photo
                    if (photo != null) {
                        RemoteImage(photo.card, tree.name, Modifier.size(64.dp).clip(RoundedCornerShape(10.dp)))
                        Spacer(Modifier.size(12.dp))
                    }
                    Column(Modifier.weight(1f)) {
                        Text(
                            tree.name,
                            fontFamily = Brand,
                            fontWeight = FontWeight.Bold,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                        )
                        val distance = here?.let { Geo.short(Geo.km(it.lat, it.lng, tree.lat, tree.lng), miles) }
                        Text(
                            listOfNotNull(tree.commonName, distance ?: tree.city).joinToString(" · "),
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                        )
                    }
                }
            }
            if (inView.total > inView.trees.size) {
                item {
                    Text(
                        stringResource(R.string.zoom_for_more),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        textAlign = TextAlign.Center,
                        modifier = Modifier.fillMaxWidth().padding(16.dp),
                    )
                }
            }
            item { Spacer(Modifier.height(16.dp)) }
        }
    }
}
