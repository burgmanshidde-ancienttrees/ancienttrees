// Every text in the app goes through here, so it sets in Inter tracked as the
// iPhone tracks SF Pro (Hidde, 2026-11-10: "waarom zijn alle lettertypes en
// iconen anders maak het zo veel hetzelfde"). scripts/android_parity.py fails a
// file that imports Material's Text instead.

package app.ancienttrees.ui

import androidx.compose.foundation.text.InlineTextContent
import androidx.compose.material3.LocalTextStyle
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.runtime.getValue
import androidx.compose.ui.text.style.LineBreak
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
 * SwiftUI's line, for text that wraps. Where the Swift sets a text style the
 * iPhone puts that style's leading (Apple's ramp: 16 on 21, 17 on 22...) between
 * lines and none after the last: six lines of .body measure 5 x 22 + 20.3 =
 * 130.3 and sixteen of .callout 15 x 21 + 19.1 = 334.1, exactly what SweepFrames
 * reads (data/ios-frames.json, 2026-11-11). A .system(size:) text has no leading
 * at all, so nothing is guessed from the size: a call that sets a line height
 * gets it between lines only (centred, both ends trimmed: one line keeps its
 * font's height), and a call that sets none keeps Inter's own line. Compose
 * otherwise adds the leading after the last line too.
 */
private val SWIFT_LINES = LineHeightStyle(LineHeightStyle.Alignment.Center, LineHeightStyle.Trim.Both)

private fun lines(lineHeight: TextUnit, fontSize: TextUnit, fontFamily: FontFamily?, style: TextStyle): Pair<TextUnit, TextStyle> {
    val family = fontFamily ?: style.fontFamily
    if (family != null && family != TextFace) return lineHeight to style // Gabarito keeps its own lines
    val h = if (lineHeight.isSpecified) lineHeight else style.lineHeight
    if (!h.isSpecified) return lineHeight to style
    // Always ours: Material's default style carries its own (Center, Trim.None),
    // and left in place it adds the leading after the last line after all.
    return h to style.copy(lineHeightStyle = SWIFT_LINES)
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
    // TextKit's push-out, for every text that may wrap: break greedily, and when
    // a two-line text would end on a single word, take one more word down with it
    // ("...and the / Privacy notice.", "Are you enjoying / Ancient Trees?", "add
    // and / save trees."); a third line keeps its lone word, as the iPhone's
    // refused sheet shows. Measured 2026-11-11. The last two words are tied with
    // a no-break space, so the break stays greedy everywhere else.
    val wraps = softWrap && maxLines >= 2
    var pushed by remember(text) { mutableStateOf(false) }
    val shown = if (wraps && pushed) text.trimEnd().let { t ->
        val i = t.lastIndexOf(' ')
        if (i > 0) t.substring(0, i) + "\u00A0" + t.substring(i + 1) else text
    } else text
    val styled = if (wraps) style.copy(lineBreak = LineBreak.Simple) else style
    val layout: ((TextLayoutResult) -> Unit)? = if (!wraps) onTextLayout else { r ->
        if (!pushed && r.lineCount == 2 && shown === text) {
            val last = text.substring(r.getLineStart(1), r.getLineEnd(1)).trim()
            if (last.isNotEmpty() && ' ' !in last) pushed = true
        }
        onTextLayout?.invoke(r)
    }
    val (lh, st) = lines(lineHeight, fontSize, fontFamily, styled)
    androidx.compose.material3.Text(
        text = shown, modifier = modifier, color = color, fontSize = fontSize, fontStyle = fontStyle,
        fontWeight = fontWeight, fontFamily = fontFamily ?: style.fontFamily ?: TextFace,
        letterSpacing = spacing(letterSpacing, fontSize, fontWeight, fontFamily, style),
        textDecoration = textDecoration, textAlign = textAlign, lineHeight = lh, overflow = overflow,
        softWrap = softWrap, maxLines = maxLines, minLines = minLines, onTextLayout = layout, style = st,
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
    // The same push-out as the plain Text above; a no-break space has the space's
    // length, so the styles and links keep their ranges.
    val wraps = softWrap && maxLines >= 2
    var pushed by remember(text) { mutableStateOf(false) }
    val shown = if (wraps && pushed) {
        val i = text.text.trimEnd().lastIndexOf(' ')
        if (i > 0) androidx.compose.ui.text.buildAnnotatedString {
            append(text.subSequence(0, i)); append("\u00A0"); append(text.subSequence(i + 1, text.length))
        } else text
    } else text
    val layout: (TextLayoutResult) -> Unit = { r ->
        if (wraps && !pushed && r.lineCount == 2 && shown === text) {
            val last = text.text.substring(r.getLineStart(1), r.getLineEnd(1)).trim()
            if (last.isNotEmpty() && ' ' !in last) pushed = true
        }
        onTextLayout(r)
    }
    val (lh, st) = lines(lineHeight, fontSize, fontFamily, if (wraps) style.copy(lineBreak = LineBreak.Simple) else style)
    androidx.compose.material3.Text(
        text = shown, modifier = modifier, color = color, fontSize = fontSize, fontStyle = fontStyle,
        fontWeight = fontWeight, fontFamily = fontFamily ?: style.fontFamily ?: TextFace,
        letterSpacing = spacing(letterSpacing, fontSize, fontWeight, fontFamily, style),
        textDecoration = textDecoration, textAlign = textAlign, lineHeight = lh, overflow = overflow,
        softWrap = softWrap, maxLines = maxLines, minLines = minLines, inlineContent = inlineContent,
        onTextLayout = layout, style = st,
    )
}

/** UIColor.placeholderText: the grey of a text field's prompt (3C3C43 at 30 percent; EBEBF5 at 30 in the dark). */
@androidx.compose.runtime.Composable
fun placeholderGrey(): Color =
    if (Brand.colors.ground.red < 0.5f) Color(0x4DEBEBF5) else Color(0x4D3C3C43)

/**
 * A headline's line breaking as Apple's: greedy, except that a two-line text
 * never ends on one word (TextKit's push-out: "Are you enjoying / Ancient Trees?",
 * while "Ancient Trees works best / with your location turned / on" keeps its
 * lone "on", measured on the iPhone 2026-11-11). Text() does this for every
 * wrapping text now; the marker is kept so a headline says what it is.
 */
@Composable
fun headlineStyle(): TextStyle = LocalTextStyle.current
