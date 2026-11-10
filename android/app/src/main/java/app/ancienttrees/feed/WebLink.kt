// A link from the website, read the way the iPhone reads it (Kit/WebLink.swift and
// ContentView.open / continued): /t?id= is a shared tree, /profile?u= a person,
// /open?tree= or ?city= continues in the app, a language prefix is dropped,
// /explore is the map, /species/<slug> and /collections/<slug> their pages, a
// tree's own path its page, a city slug its place, a country slug its country.
// Beyond the iPhone: /<city>#tree=<id>, the address the feed gives an app-only tree.

package app.ancienttrees.feed

import android.net.Uri
import java.text.Normalizer

sealed class LinkTarget {
    data class TreeAt(val id: String) : LinkTarget()
    data class City(val slug: String) : LinkTarget()
    data class Country(val name: String) : LinkTarget()
    data class SpeciesAt(val name: String) : LinkTarget()
    data class Collection(val slug: String) : LinkTarget()
    data class Shared(val id: String) : LinkTarget()
    data class Person(val id: String) : LinkTarget()
    data object Map : LinkTarget()
}

object WebLink {
    val LANGUAGES = setOf("de", "es", "fr", "it", "nl", "pt", "ja")
    private val UUID = Regex("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")

    /** What the catalogue knows, so the parser can tell a tree from a city. */
    class Lookup(
        val treeId: (path: String) -> String? = { null },
        val isCity: (slug: String) -> Boolean = { false },
        val countryName: (slug: String) -> String? = { null },
        val speciesName: (slug: String) -> String? = { null },
    ) {
        companion object {
            fun of(c: Catalogue?): Lookup {
                if (c == null) return Lookup()
                return Lookup(
                    treeId = { path ->
                        val city = path.trim('/').substringBefore('/')
                        c.trees(city).firstOrNull { it.url == path }?.id
                    },
                    isCity = { c.trees(it).isNotEmpty() },
                    countryName = { slug -> c.byCountry.keys.firstOrNull { slugify(it) == slug } },
                    speciesName = { slug -> c.speciesNames.firstOrNull { slugify(it) == slug } },
                )
            }
        }
    }

    /** The parts of a link this needs, so a test on the build machine needs no Android. */
    fun parse(path: String, query: Map<String, String>, fragment: String?, lookup: Lookup): LinkTarget? {
        var parts = path.split("/").filter { it.isNotEmpty() }
        if (parts.firstOrNull() == "t") {
            val id = query["id"] ?: return null
            return if (UUID.matches(id)) LinkTarget.Shared(id.lowercase()) else null
        }
        if (parts == listOf("profile")) {
            val u = query["u"] ?: return null
            return if (UUID.matches(u)) LinkTarget.Person(u.lowercase()) else null
        }
        if (parts == listOf("open")) {
            query["tree"]?.takeIf { it.isNotEmpty() }?.let { return LinkTarget.TreeAt(it) }
            query["city"]?.takeIf { it.isNotEmpty() }?.let { return LinkTarget.City(it) }
            return null
        }
        if (parts.firstOrNull() in LANGUAGES) parts = parts.drop(1)
        val first = parts.firstOrNull() ?: return null
        when (first) {
            "explore" -> return LinkTarget.Map
            "species" -> return if (parts.size == 2) lookup.speciesName(parts[1])?.let { LinkTarget.SpeciesAt(it) } else null
            "collections" -> return if (parts.size == 2) LinkTarget.Collection(parts[1]) else null
        }
        // The feed's address of an app-only tree: the city map with its card.
        fragment?.removePrefix("tree=")?.takeIf { fragment.startsWith("tree=") && it.isNotEmpty() }?.let {
            return LinkTarget.TreeAt(it)
        }
        if (parts.size >= 2) lookup.treeId("/" + parts[0] + "/" + parts[1])?.let { return LinkTarget.TreeAt(it) }
        if (lookup.isCity(first)) return LinkTarget.City(first)
        lookup.countryName(first)?.let { return LinkTarget.Country(it) }
        return null
    }

    fun parse(uri: Uri, lookup: Lookup): LinkTarget? {
        if (uri.host != "ancienttrees.app" && uri.host != "www.ancienttrees.app") return null
        val query = uri.queryParameterNames.associateWith { uri.getQueryParameter(it).orEmpty() }
        return parse(uri.path.orEmpty(), query, uri.fragment, lookup)
    }

    /** The website's slugs: lower case, accents folded, "the " dropped, hyphens between words. */
    fun slugify(name: String): String {
        var s = name.lowercase().replace("'", "").replace("’", "")
        if (s.startsWith("the ")) s = s.drop(4)
        s = Normalizer.normalize(s, Normalizer.Form.NFKD).replace(Regex("\\p{M}"), "")
        val out = StringBuilder()
        var hyphen = false
        for (ch in s) {
            if (ch in 'a'..'z' || ch in '0'..'9') {
                out.append(ch); hyphen = false
            } else if (ch.code < 128) {
                if (!hyphen && out.isNotEmpty()) { out.append('-'); hyphen = true }
            }
        }
        return out.toString().trimEnd('-')
    }
}
