// The App Store's "more", ported from ios Screens/ExpandableText.swift: the text
// folded to a number of lines, and where it was cut a moss "more" at the end of
// the last line behind a short fade. A tap anywhere on the text opens it in
// place; a text that fits gets no button at all.

package app.ancienttrees.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import app.ancienttrees.R

@Composable
fun ExpandableText(text: AnnotatedString, lines: Int, style: TextStyle, modifier: Modifier = Modifier) {
    val brand = Brand.colors
    var expanded by remember(text) { mutableStateOf(false) }
    var cut by remember(text) { mutableStateOf(false) }
    Box(
        modifier
            .fillMaxWidth()
            .clickable(
                enabled = cut && !expanded,
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
            ) { expanded = true },
    ) {
        Text(
            text,
            style = style,
            maxLines = if (expanded) Int.MAX_VALUE else lines,
            onTextLayout = { if (!expanded) cut = it.hasVisualOverflow },
            modifier = Modifier.fillMaxWidth(),
        )
        if (cut && !expanded) {
            Row(Modifier.align(Alignment.BottomEnd).height(IntrinsicSize.Min)) {
                Box(
                    Modifier
                        .width(44.dp)
                        .fillMaxHeight()
                        .background(Brush.horizontalGradient(listOf(brand.ground.copy(alpha = 0f), brand.ground))),
                )
                Text(
                    stringResource(R.string.more),
                    style = style.copy(fontWeight = FontWeight.SemiBold, color = brand.moss),
                    modifier = Modifier.background(brand.ground).padding(start = 2.dp),
                )
            }
        }
    }
}

@Composable
fun ExpandableText(text: String, lines: Int, style: TextStyle, modifier: Modifier = Modifier) =
    ExpandableText(AnnotatedString(text), lines, style, modifier)
