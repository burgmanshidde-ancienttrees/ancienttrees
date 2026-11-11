package app.ancienttrees.map

import android.graphics.Matrix
import android.graphics.Path
import android.graphics.RectF
import androidx.core.graphics.PathParser

/**
 * A species silhouette as the iPhone draws it (Kit/SVGPath.swift, SpeciesShape):
 * every part of the shape in ONE path, filled in one colour. The iPhone reads only
 * each part's `d` and its ellipses, so the website's 45 percent back layers and its
 * rotate/translate never reach the screen there: a wingnut's back crown, drawn
 * half-transparent here, read as a second "weeping" crown beside the iPhone's
 * single round one (visual review 2026-11-11). Flat, one tone, everywhere.
 */
object SpeciesPath {
    private val cache = HashMap<String, Path>()

    /** The shape's parts as one path in the 40 by 40 box the website draws in. */
    @Synchronized
    fun of(shape: String): Path = cache.getOrPut(shape) {
        val out = Path()
        for (part in SpeciesIcons.icons[shape].orEmpty()) {
            when (part) {
                is SpeciesIcons.Part.Shape ->
                    runCatching { PathParser.createPathFromPathData(part.d) }.getOrNull()?.let { out.addPath(it) }
                is SpeciesIcons.Part.Oval ->
                    out.addOval(RectF(part.left, part.top, part.right, part.bottom), Path.Direction.CW)
            }
        }
        out
    }

    /**
     * The path scaled to fit a box `w` by `h` (by its smaller side, over 40) and
     * centred on its OWN bounds there, as SpeciesShape.path(in:) does.
     */
    fun fitted(shape: String, w: Float, h: Float): Path {
        val s = minOf(w, h) / 40f
        val p = Path(of(shape))
        p.transform(Matrix().apply { setScale(s, s) })
        val b = RectF()
        @Suppress("DEPRECATION") p.computeBounds(b, true)
        p.transform(Matrix().apply { setTranslate(w / 2 - b.centerX(), h / 2 - b.centerY()) })
        return p
    }
}
