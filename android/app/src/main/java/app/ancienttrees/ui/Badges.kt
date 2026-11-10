// The badges a person wears and the flag after their name, ported from ios
// Screens/AmbassadorBadge.swift: the ambassador's moss pill (komoot's Pioneer),
// the early-adopter tag in gold with its one-time sheet, and the round flag.
// Shared by My trees (Collect.swift's header), Find people and a person's profile.

package app.ancienttrees.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.wrapContentSize
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.account.Profiles
import java.util.Locale

/** "Paris ambassador"; in a list row only the place, so Follow and the menu keep their room. */
@Composable
fun ambassadorLabel(places: List<String>, compact: Boolean): String = when {
    places.isEmpty() -> ""
    compact && places.size == 1 -> places[0]
    compact -> stringResource(R.string.badge_and_more, places[0], places.size - 1)
    places.size == 1 -> stringResource(R.string.badge_ambassador_1, places[0])
    places.size == 2 -> stringResource(R.string.badge_ambassador_2, places[0], places[1])
    else -> stringResource(R.string.badge_ambassador_n, places[0], places[1], places.size - 2)
}

/** The moss pill with the seal; on your own profile a tap opens the place. */
@Composable
fun AmbassadorBadge(
    places: List<Profiles.Ambassador>,
    size: Int = 12,
    compact: Boolean = false,
    open: ((Profiles.Ambassador) -> Unit)? = null,
) {
    if (places.isEmpty()) return
    val brand = Brand.colors
    val pill = @Composable {
        Row(
            horizontalArrangement = Arrangement.spacedBy(4.dp),
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier
                .background(brand.moss.copy(alpha = 0.12f), RoundedCornerShape(50))
                .padding(top = 3.dp, bottom = 3.dp, start = 7.dp, end = 9.dp),
        ) {
            Icon(Icons.Filled.Verified, null, tint = brand.moss, modifier = Modifier.size((size + 2).dp))
            Text(
                ambassadorLabel(places.map { it.placeName }, compact), color = brand.moss, fontSize = size.sp,
                fontWeight = FontWeight.Medium, maxLines = 1, overflow = TextOverflow.Ellipsis,
            )
        }
    }
    if (open != null) {
        Box(
            Modifier.heightIn(min = 44.dp).clickable { open(places.first()) },
            contentAlignment = Alignment.CenterStart,
        ) { pill() }
    } else {
        pill()
    }
}

/** The gold tag (Hidde, 2026-10-16: "honestly i liked the tag better"); a label, never a button. */
@Composable
fun EarlyAdopterBadge(size: Int = 12) {
    val brand = Brand.colors
    Row(
        horizontalArrangement = Arrangement.spacedBy(4.dp),
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .wrapContentSize()
            .background(brand.gold.copy(alpha = 0.18f), RoundedCornerShape(50))
            .padding(top = 3.dp, bottom = 3.dp, start = 7.dp, end = 9.dp),
    ) {
        Icon(Icons.Filled.AutoAwesome, null, tint = brand.goldInk, modifier = Modifier.size((size + 1).dp))
        Text(stringResource(R.string.early_adopter), color = brand.goldInk, fontSize = size.sp, fontWeight = FontWeight.Medium, maxLines = 1)
    }
}

/** Shown once per account, the first time My trees opens with the badge (account.astro's early-dialog). */
@Composable
fun EarlyAdopterSheet(onDismiss: () -> Unit) {
    BrandSheet(
        title = stringResource(R.string.early_title),
        message = stringResource(R.string.early_body),
        icon = Icons.Filled.AutoAwesome,
        iconTint = Brand.colors.goldInk,
        iconGround = Brand.colors.gold.copy(alpha = 0.18f),
        onDismiss = onDismiss,
        buttons = listOf(SheetButton(stringResource(R.string.done), SheetKind.PRIMARY, action = onDismiss)),
    )
}

/**
 * The flag after your name, round as Polarsteps draws it. The iPhone fills the
 * circle with the website's flat flag (flag-icons); Android draws the system's
 * flag emoji in the circle (data/android-parity.json, a listed difference).
 */
@Composable
fun CountryFlag(code: String?, size: Int = 20) {
    val emoji = flagEmoji(code) ?: return
    Box(
        Modifier
            .size(size.dp)
            .clip(CircleShape)
            .border(1.dp, Color.Black.copy(alpha = 0.08f), CircleShape),
        contentAlignment = Alignment.Center,
    ) {
        Text(emoji, fontSize = (size * 1.25f).sp, maxLines = 1, softWrap = false)
    }
}

/** "NL" to the regional-indicator pair the system draws as the Dutch flag. */
fun flagEmoji(code: String?): String? {
    val c = code?.uppercase(Locale.ROOT) ?: return null
    if (c.length != 2 || !c.all { it in 'A'..'Z' }) return null
    return c.map { String(Character.toChars(127397 + it.code)) }.joinToString("")
}

/** The country's English name, as the iPhone's picker lists them. */
fun countryName(code: String): String = Locale("", code).getDisplayCountry(Locale.ENGLISH)
