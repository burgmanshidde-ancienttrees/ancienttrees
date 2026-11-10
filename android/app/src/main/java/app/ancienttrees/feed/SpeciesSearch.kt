// How a typed word finds a species, the twin of ios Kit/SpeciesSearch.swift: the
// common name first, then the Latin, then any other name it goes by, then a
// near miss of one letter for words of five letters or more.

package app.ancienttrees.feed

import java.text.Normalizer

sealed class SpeciesHit(val rank: Int) : Comparable<SpeciesHit> {
    object Name : SpeciesHit(0)
    object Latin : SpeciesHit(1)
    class Other(val via: String) : SpeciesHit(2)
    object Nearly : SpeciesHit(3)

    override fun compareTo(other: SpeciesHit): Int = rank.compareTo(other.rank)
}

object SpeciesSearch {
    private val MARKS = Regex("\\p{Mn}+")

    /** Case and accents folded, as Swift's folding(.caseInsensitive, .diacriticInsensitive). */
    fun fold(s: String): String =
        MARKS.replace(Normalizer.normalize(s, Normalizer.Form.NFD), "").lowercase().trim()

    private fun words(folded: String): List<String> =
        folded.split(' ', '-', '(', '\'').filter { it.isNotEmpty() }

    fun startsAWord(name: String, q: String): Boolean {
        val n = fold(name)
        return n.startsWith(q) || words(n).any { it.startsWith(q) }
    }

    fun nearlyStartsAWord(name: String, q: String): Boolean {
        if (q.length < 5) return false
        return words(fold(name)).any { w ->
            listOf(q.length - 1, q.length, q.length + 1).any { len ->
                len > 0 && len <= w.length && editDistance(q, w.substring(0, len), 1) <= 1
            }
        }
    }

    private fun editDistance(a: String, b: String, limit: Int): Int {
        if (kotlin.math.abs(a.length - b.length) > limit) return limit + 1
        if (a.isEmpty() || b.isEmpty()) return maxOf(a.length, b.length)
        var prev = IntArray(b.length + 1) { it }
        for (i in 1..a.length) {
            val cur = IntArray(b.length + 1)
            cur[0] = i
            for (j in 1..b.length) {
                cur[j] = minOf(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + if (a[i - 1] == b[j - 1]) 0 else 1)
            }
            prev = cur
        }
        return prev[b.length]
    }

    fun hit(common: String, latin: String?, other: List<String>, q: String): SpeciesHit? {
        if (q.isEmpty()) return SpeciesHit.Name
        if (startsAWord(common, q)) return SpeciesHit.Name
        if (latin != null && startsAWord(latin, q)) return SpeciesHit.Latin
        other.firstOrNull { startsAWord(it, q) }?.let { return SpeciesHit.Other(it) }
        if (nearlyStartsAWord(common, q)) return SpeciesHit.Nearly
        if (latin != null && nearlyStartsAWord(latin, q)) return SpeciesHit.Nearly
        other.firstOrNull { nearlyStartsAWord(it, q) }?.let { return SpeciesHit.Other(it) }
        return null
    }
}

/** The species among [commons] a query finds, best kind of hit first, then their own order. */
fun Catalogue.filterSpecies(commons: List<String>, query: String): List<Pair<String, SpeciesHit>> {
    val q = SpeciesSearch.fold(query)
    return commons.mapIndexedNotNull { i, c ->
        SpeciesSearch.hit(c, scientificName(c), otherNames[c].orEmpty(), q)?.let { Triple(i, c, it) }
    }.sortedWith(compareBy<Triple<Int, String, SpeciesHit>>({ it.third.rank }, { it.first })).map { it.second to it.third }
}

/**
 * Kinds of tree we know by name and do not map yet, matching [query]
 * (Catalogue.unmappedSpecies): the same hit order, a genus first when it ties.
 */
fun Catalogue.unmappedSpecies(query: String, limit: Int = 8): List<Pair<SpeciesNameRow, SpeciesHit>> {
    val q = SpeciesSearch.fold(query)
    if (q.length < 2) return emptyList()
    return directory.mapIndexedNotNull { i, r ->
        // A genus we already map ("Oak (Quercus sp.)") is a row above.
        if (r.isMapped || treesOfSpecies(r.c).isNotEmpty()) return@mapIndexedNotNull null
        SpeciesSearch.hit(r.c, r.l, r.a, q)?.let { Triple(i, r, it) }
    }.sortedWith(
        compareBy<Triple<Int, SpeciesNameRow, SpeciesHit>>({ it.third.rank }, { !it.second.isGenus }, { it.first }),
    ).take(limit).map { it.second to it.third }
}
