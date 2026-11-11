// Every text in the app goes through here, so it sets in Inter tracked as the
// iPhone tracks SF Pro (Hidde, 2026-11-10: "waarom zijn alle lettertypes en
// iconen anders maak het zo veel hetzelfde"). scripts/android_parity.py fails a
// file that imports Material's Text instead.

package app.ancienttrees.ui

import androidx.compose.foundation.text.InlineTextContent
import androidx.compose.material3.LocalTextStyle
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.TextLayoutResult
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.LineHeightStyle
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.em
import androidx.compose.ui.unit.isSpecified
import androidx.compose.ui.unit.sp

/**
 * The letter spacing that sets a line of Inter as wide as SF Pro sets it on the
 * iPhone, in em, by size and weight. Measured 2026-11-10 against the Mac's SF Pro
 * (its own tracking table plus its optical sizes) over a line of tree-page copy:
 * Inter's regular is as wide as SF's text cut before tracking, so at regular this
 * is SF's own tracking (+0.006 em at 11, -0.025 at 17); each 100 of weight adds
 * about 0.0054 em, because SF widens with weight more than Inter does.
 */
private val REGULAR_EM = floatArrayOf(
    // 9 .. 28 sp
    0.0197f, 0.0129f, 0.0070f, 0.0011f, -0.0047f, -0.0096f, -0.0145f, -0.0184f, -0.0242f, -0.0260f,
    -0.0278f, -0.0355f, -0.0389f, -0.0423f, -0.0437f, -0.0452f, -0.0453f, -0.0452f, -0.0452f, -0.0454f,
)

fun sfTracking(size: TextUnit, weight: FontWeight?): TextUnit {
    val sp = if (size.isSpecified && size.type == androidx.compose.ui.unit.TextUnitType.Sp) size.value else 17f
    val x = (sp - 9f).coerceIn(0f, (REGULAR_EM.size - 1).toFloat())
    val i = x.toInt().coerceAtMost(REGULAR_EM.size - 2)
    val base = REGULAR_EM[i] + (REGULAR_EM[i + 1] - REGULAR_EM[i]) * (x - i)
    val w = (weight ?: FontWeight.Normal).weight
    return (base + 0.0054f * (w - 400) / 100f).em
}

// A style built from scratch (TextStyle(shadow = ...)) carries no family, and
// Compose would fall back to Roboto: such a text sets in Inter too.
private fun spacing(letterSpacing: TextUnit, fontSize: TextUnit, fontWeight: FontWeight?, fontFamily: FontFamily?, style: TextStyle): TextUnit {
    if (letterSpacing.isSpecified) return letterSpacing
    if (style.letterSpacing.isSpecified) return style.letterSpacing
    val family = fontFamily ?: style.fontFamily
    if (family != null && family != TextFace) return TextUnit.Unspecified // Gabarito keeps its own spacing
    return sfTracking(if (fontSize.isSpecified) fontSize else style.fontSize, fontWeight ?: style.fontWeight)
}

/**
 * SwiftUI's line, for text that wraps. The iPhone puts the text style's leading
 * (Apple's type ramp: 13 on 18, 15 on 20, 16 on 21, 17 on 22...) between lines
 * and none after the last: six lines of 17 measure 5 x 22 + 20.3 = 130.3, and
 * sixteen of 16 measure 15 x 21 + 19.1 = 334.1, both exactly what SweepFrames
 * reads (data/ios-frames.json, 2026-11-11). Compose, given no line height, set
 * Inter's own (16 on 19.4) and the intro came out 25 shorter; given one, it adds
 * the leading after the last line too. So: the ramp's leading where the call
 * sets none, the glyphs at the top of each line as UIKit sets them, and the last
 * line's extra trimmed. One line keeps exactly its font's height.
 */
private fun swiftLeading(size: TextUnit): TextUnit {
    if (!size.isSpecified || size.type != androidx.compose.ui.unit.TextUnitType.Sp) return TextUnit.Unspecified
    return when (size.value) {
        11f -> 13.sp; 12f -> 16.sp; 13f -> 18.sp; 15f -> 20.sp; 16f -> 21.sp; 17f -> 22.sp
        20f -> 25.sp; 22f -> 28.sp; 28f -> 34.sp; 34f -> 41.sp
        else -> TextUnit.Unspecified
    }
}

private val SWIFT_LINES = LineHeightStyle(LineHeightStyle.Alignment.Top, LineHeightStyle.Trim.LastLineBottom)

private fun lines(lineHeight: TextUnit, fontSize: TextUnit, fontFamily: FontFamily?, style: TextStyle): Pair<TextUnit, TextStyle> {
    val family = fontFamily ?: style.fontFamily
    if (family != null && family != TextFace) return lineHeight to style // Gabarito keeps its own lines
    val h = when {
        lineHeight.isSpecified -> lineHeight
        style.lineHeight.isSpecified -> style.lineHeight
        else -> swiftLeading(if (fontSize.isSpecified) fontSize else style.fontSize)
    }
    if (!h.isSpecified) return lineHeight to style
    return h to style.copy(lineHeightStyle = style.lineHeightStyle ?: SWIFT_LINES)
}

/** A text field's style: Inter at SF's tracking. */
fun sfStyle(
    fontSize: TextUnit = 17.sp,
    color: Color = Color.Unspecified,
    fontWeight: FontWeight = FontWeight.Normal,
    textAlign: TextAlign = TextAlign.Unspecified,
) = TextStyle(
    color = color,
    fontSize = fontSize,
    fontWeight = fontWeight,
    fontFamily = TextFace,
    letterSpacing = sfTracking(fontSize, fontWeight),
    textAlign = textAlign,
)

@Composable
fun Text(
    text: String,
    modifier: Modifier = Modifier,
    color: Color = Color.Unspecified,
    fontSize: TextUnit = TextUnit.Unspecified,
    fontStyle: FontStyle? = null,
    fontWeight: FontWeight? = null,
    fontFamily: FontFamily? = null,
    letterSpacing: TextUnit = TextUnit.Unspecified,
    textDecoration: TextDecoration? = null,
    textAlign: TextAlign? = null,
    lineHeight: TextUnit = TextUnit.Unspecified,
    overflow: TextOverflow = TextOverflow.Clip,
    softWrap: Boolean = true,
    maxLines: Int = Int.MAX_VALUE,
    minLines: Int = 1,
    onTextLayout: ((TextLayoutResult) -> Unit)? = null,
    style: TextStyle = LocalTextStyle.current,
) {
    val (lh, st) = lines(lineHeight, fontSize, fontFamily, style)
    androidx.compose.material3.Text(
        text = text, modifier = modifier, color = color, fontSize = fontSize, fontStyle = fontStyle,
        fontWeight = fontWeight, fontFamily = fontFamily ?: style.fontFamily ?: TextFace,
        letterSpacing = spacing(letterSpacing, fontSize, fontWeight, fontFamily, style),
        textDecoration = textDecoration, textAlign = textAlign, lineHeight = lh, overflow = overflow,
        softWrap = softWrap, maxLines = maxLines, minLines = minLines, onTextLayout = onTextLayout, style = st,
    )
}

@Composable
fun Text(
    text: AnnotatedString,
    modifier: Modifier = Modifier,
    color: Color = Color.Unspecified,
    fontSize: TextUnit = TextUnit.Unspecified,
    fontStyle: FontStyle? = null,
    fontWeight: FontWeight? = null,
    fontFamily: FontFamily? = null,
    letterSpacing: TextUnit = TextUnit.Unspecified,
    textDecoration: TextDecoration? = null,
    textAlign: TextAlign? = null,
    lineHeight: TextUnit = TextUnit.Unspecified,
    overflow: TextOverflow = TextOverflow.Clip,
    softWrap: Boolean = true,
    maxLines: Int = Int.MAX_VALUE,
    minLines: Int = 1,
    inlineContent: Map<String, InlineTextContent> = mapOf(),
    onTextLayout: (TextLayoutResult) -> Unit = {},
    style: TextStyle = LocalTextStyle.current,
) {
    val (lh, st) = lines(lineHeight, fontSize, fontFamily, style)
    androidx.compose.material3.Text(
        text = text, modifier = modifier, color = color, fontSize = fontSize, fontStyle = fontStyle,
        fontWeight = fontWeight, fontFamily = fontFamily ?: style.fontFamily ?: TextFace,
        letterSpacing = spacing(letterSpacing, fontSize, fontWeight, fontFamily, style),
        textDecoration = textDecoration, textAlign = textAlign, lineHeight = lh, overflow = overflow,
        softWrap = softWrap, maxLines = maxLines, minLines = minLines, inlineContent = inlineContent,
        onTextLayout = onTextLayout, style = st,
    )
}
