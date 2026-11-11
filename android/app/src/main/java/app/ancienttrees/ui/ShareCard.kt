// A picture of a tree you added, made to be posted somewhere else: the twin of
// ios Kit/ShareCard.swift (review 2026-11-11: Android shared only the link).
//
// CONVENTION: Strava (CONVENTIONS.md "Sharing something you made that has no
// page"): share an IMAGE with the facts and our mark on it. The iPhone hands the
// card and the unlisted link to the share sheet together, so Instagram takes the
// card and Messages takes both; so does this.
//
// 4:5 and 1080 wide, the iPhone's size: your photograph filling the card (or the
// canopy green with the species mark, never a grey placeholder), a dark gradient
// from 62 % down, the name in the brand face at 76, species and day at 34, and
// ancienttrees.app at 30 in the corner, 64 in from the edges.

package app.ancienttrees.ui

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.LinearGradient
import android.graphics.Paint
import android.graphics.RectF
import android.graphics.Shader
import android.text.Layout
import android.text.StaticLayout
import android.text.TextPaint
import android.text.TextUtils
import androidx.core.content.res.ResourcesCompat
import androidx.core.graphics.PathParser
import app.ancienttrees.R
import app.ancienttrees.map.SpeciesIcons
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

object ShareCard {
    const val WIDTH = 1080
    const val HEIGHT = 1350
    private const val PAD = 64f

    /** The card, never null: a tree whose photograph has gone missing still gets one, with its species mark. */
    fun render(context: Context, photo: Bitmap?, name: String, species: String?, date: Date): Bitmap {
        val out = Bitmap.createBitmap(WIDTH, HEIGHT, Bitmap.Config.ARGB_8888)
        val c = Canvas(out)
        if (photo != null) {
            // aspectRatio(.fill): the photograph covers the card, centred, cropped.
            val scale = maxOf(WIDTH / photo.width.toFloat(), HEIGHT / photo.height.toFloat())
            val w = photo.width * scale
            val h = photo.height * scale
            c.drawBitmap(photo, null, RectF((WIDTH - w) / 2f, (HEIGHT - h) / 2f, (WIDTH + w) / 2f, (HEIGHT + h) / 2f),
                Paint(Paint.FILTER_BITMAP_FLAG))
        } else {
            c.drawColor(0xFF3A5222.toInt())
            drawMark(c, species.orEmpty(), 560f, (WIDTH - 560f) / 2f, (HEIGHT - 560f) / 2f - 80f)
        }
        // From below the middle, so the photograph stays the thing shared.
        val shade = Paint().apply {
            shader = LinearGradient(0f, HEIGHT * 0.62f, 0f, HEIGHT.toFloat(), 0x00000000, 0xBF000000.toInt(), Shader.TileMode.CLAMP)
        }
        c.drawRect(0f, HEIGHT * 0.62f, WIDTH.toFloat(), HEIGHT.toFloat(), shade)

        val brandBold = ResourcesCompat.getFont(context, R.font.gabarito_bold)
        val brandRegular = ResourcesCompat.getFont(context, R.font.gabarito_regular)
        val white85 = 0xD9FFFFFF.toInt()
        val inner = (WIDTH - 2 * PAD).toInt()

        // The bottom line: species and day on the left, our mark on the right.
        val markPaint = TextPaint(Paint.ANTI_ALIAS_FLAG).apply { typeface = brandBold; textSize = 30f; color = white85 }
        val metaPaint = TextPaint(Paint.ANTI_ALIAS_FLAG).apply { typeface = brandRegular; textSize = 34f; color = white85 }
        val mark = "ancienttrees.app"
        val markWidth = markPaint.measureText(mark)
        val baseline = HEIGHT - PAD - metaPaint.descent()
        c.drawText(mark, WIDTH - PAD - markWidth, baseline, markPaint)
        val day = SimpleDateFormat("d MMMM yyyy", Locale.getDefault()).format(date)
        val meta = listOfNotNull(species?.takeIf { it.isNotEmpty() }, day).joinToString(" · ")
        val metaFit = TextUtils.ellipsize(meta, metaPaint, inner - markWidth - 16f, TextUtils.TruncateAt.END).toString()
        c.drawText(metaFit, PAD, baseline, metaPaint)

        // The name above it, at most three lines, smaller rather than cut (minimumScaleFactor 0.6).
        val namePaint = TextPaint(Paint.ANTI_ALIAS_FLAG).apply { typeface = brandBold; color = 0xFFFFFFFF.toInt() }
        var size = 76f
        var layout: StaticLayout
        while (true) {
            namePaint.textSize = size
            layout = StaticLayout.Builder.obtain(name, 0, name.length, namePaint, inner)
                .setAlignment(Layout.Alignment.ALIGN_NORMAL).setMaxLines(3).setEllipsize(TextUtils.TruncateAt.END).build()
            if (layout.lineCount <= 3 && layout.getEllipsisCount(layout.lineCount - 1) == 0 || size <= 76f * 0.6f) break
            size -= 4f
        }
        val metaTop = baseline + metaPaint.ascent()
        c.save()
        c.translate(PAD, metaTop - 14f - layout.height)
        layout.draw(c)
        c.restore()
        return out
    }

    /** SpeciesMark on the platform canvas, white at 22 %, as the iPhone's empty card draws it. */
    private fun drawMark(c: Canvas, species: String, side: Float, left: Float, top: Float) {
        val shape = SpeciesIcons.archetype(species.substringBefore("(").trim())
        val parts = SpeciesIcons.icons[shape].orEmpty()
        c.save()
        c.translate(left, top)
        c.scale(side / 40f, side / 40f)
        for (part in parts) {
            val p = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = 0xFFFFFFFF.toInt(); alpha = (255 * 0.22f * part.alpha).toInt() }
            when (part) {
                is SpeciesIcons.Part.Oval -> c.drawOval(RectF(part.left, part.top, part.right, part.bottom), p)
                is SpeciesIcons.Part.Shape -> {
                    val path = runCatching { PathParser.createPathFromPathData(part.d) }.getOrNull() ?: continue
                    val m = android.graphics.Matrix()
                    part.rotate?.let { m.setRotate(it[0], it[1], it[2]) }
                    part.translate?.let { m.setTranslate(it[0], it[1]) }
                    path.transform(m)
                    c.drawPath(path, p)
                }
            }
        }
        c.restore()
    }

    /** The card as a JPEG in the share folder (FileProvider "photos"), for the share sheet. */
    fun file(context: Context, card: Bitmap): File {
        val dir = File(context.cacheDir, "photos").apply { mkdirs() }
        val f = File(dir, "share-card.jpg")
        f.outputStream().use { card.compress(Bitmap.CompressFormat.JPEG, 90, it) }
        return f
    }
}
