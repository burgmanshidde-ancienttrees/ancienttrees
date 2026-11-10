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
) = androidx.compose.material3.Text(
    text = text, modifier = modifier, color = color, fontSize = fontSize, fontStyle = fontStyle,
    fontWeight = fontWeight, fontFamily = fontFamily ?: style.fontFamily ?: TextFace,
    letterSpacing = spacing(letterSpacing, fontSize, fontWeight, fontFamily, style),
    textDecoration = textDecoration, textAlign = textAlign, lineHeight = lineHeight, overflow = overflow,
    softWrap = softWrap, maxLines = maxLines, minLines = minLines, onTextLayout = onTextLayout, style = style,
)

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
) = androidx.compose.material3.Text(
    text = text, modifier = modifier, color = color, fontSize = fontSize, fontStyle = fontStyle,
    fontWeight = fontWeight, fontFamily = fontFamily ?: style.fontFamily ?: TextFace,
    letterSpacing = spacing(letterSpacing, fontSize, fontWeight, fontFamily, style),
    textDecoration = textDecoration, textAlign = textAlign, lineHeight = lineHeight, overflow = overflow,
    softWrap = softWrap, maxLines = maxLines, minLines = minLines, inlineContent = inlineContent,
    onTextLayout = onTextLayout, style = style,
)
