// The trees as read, kept as a compact binary file so the next launch does not
// read 11.5 MB of JSON again (seconds on a slow phone, where the iPhone opens at
// once). Our own catalogue only, nobody's data ("device" in
// data/cross-device.json), keyed on the file it was read from: a new download or
// a new app build makes a new key and the snapshot is simply written again.
// Anything unexpected while reading it means "no snapshot", never an error.

package app.ancienttrees.feed

import java.io.BufferedInputStream
import java.io.BufferedOutputStream
import java.io.DataInputStream
import java.io.DataOutputStream
import java.io.File

object Snapshot {
    private const val MAGIC = 0x41545331 // "ATS1"; bump when Tree changes shape.

    fun write(file: File, key: String, version: String, trees: List<Tree>) {
        val tmp = File(file.path + ".tmp")
        runCatching {
            file.parentFile?.mkdirs()
            DataOutputStream(BufferedOutputStream(tmp.outputStream(), 1 shl 16)).use { o ->
                o.writeInt(MAGIC)
                o.str(key)
                o.str(version)
                o.writeInt(trees.size)
                for (t in trees) o.tree(t)
            }
            tmp.renameTo(file)
        }.onFailure { tmp.delete() }
    }

    /** The trees, or null when there is no snapshot for [key]. */
    fun read(file: File, key: String): Pair<String, List<Tree>>? = runCatching {
        if (!file.exists()) return null
        DataInputStream(BufferedInputStream(file.inputStream(), 1 shl 16)).use { i ->
            if (i.readInt() != MAGIC) return null
            if (i.str() != key) return null
            val version = i.str()
            val n = i.readInt()
            val out = ArrayList<Tree>(n)
            repeat(n) { out.add(i.tree()) }
            version to out
        }
    }.getOrNull()

    private fun DataOutputStream.str(s: String) {
        val b = s.toByteArray(Charsets.UTF_8)
        writeInt(b.size)
        write(b)
    }

    private fun DataInputStream.str(): String {
        val b = ByteArray(readInt())
        readFully(b)
        return String(b, Charsets.UTF_8)
    }

    private fun DataOutputStream.opt(s: String?) {
        writeBoolean(s != null)
        if (s != null) str(s)
    }

    private fun DataInputStream.opt(): String? = if (readBoolean()) str() else null

    private fun DataOutputStream.optInt(v: Int?) {
        writeBoolean(v != null)
        if (v != null) writeInt(v)
    }

    private fun DataInputStream.optInt(): Int? = if (readBoolean()) readInt() else null

    private fun DataOutputStream.photo(p: Photo) {
        str(p.url); opt(p.license); opt(p.attribution); opt(p.attributionShort); opt(p.thumb); opt(p.hero)
        writeByte(when (p.creditRequired) { null -> 0; false -> 1; true -> 2 })
        opt(p.creditLine); opt(p.creditUrl)
        writeBoolean(p.frame != null)
        p.frame?.let { writeDouble(it) }
        opt(p.season)
    }

    private fun DataInputStream.photo(): Photo {
        val url = str()
        val license = opt()
        val attribution = opt()
        val short = opt()
        val thumb = opt()
        val hero = opt()
        val credit = when (readByte().toInt()) { 1 -> false; 2 -> true; else -> null }
        val line = opt()
        val curl = opt()
        val frame = if (readBoolean()) readDouble() else null
        return Photo(url, license, attribution, short, thumb, hero, credit, line, curl, frame, opt())
    }

    private fun DataOutputStream.tree(t: Tree) {
        str(t.id); str(t.name); str(t.species); opt(t.age); opt(t.ageShort)
        optInt(t.ageMin); optInt(t.ageMax)
        writeByte(when (t.highlight) { null -> 0; false -> 1; true -> 2 })
        optInt(t.highlightRank)
        writeDouble(t.lat); writeDouble(t.lng)
        str(t.city); str(t.citySlug); str(t.country); str(t.neighbourhood); str(t.access)
        writeBoolean(t.paidEntry)
        str(t.transport); str(t.story)
        writeInt(t.storyLatin.size)
        for (r in t.storyLatin) { writeInt(r.first); writeInt(r.last) }
        str(t.howToRecognise); str(t.url)
        writeBoolean(t.precision == Precision.CONFIRMED)
        writeBoolean(t.photo != null)
        t.photo?.let { photo(it) }
        writeInt(t.saves)
        writeBoolean(t.mini)
        writeInt(t.photos.size)
        for (p in t.photos) photo(p)
        writeBoolean(t.seasonal)
        writeInt(t.bestMonths.size)
        for (m in t.bestMonths) writeInt(m)
        opt(t.seasonKey)
    }

    private fun DataInputStream.tree(): Tree {
        val id = str()
        val name = str()
        val species = str()
        val age = opt()
        val ageShort = opt()
        val ageMin = optInt()
        val ageMax = optInt()
        val highlight = when (readByte().toInt()) { 1 -> false; 2 -> true; else -> null }
        val rank = optInt()
        val lat = readDouble()
        val lng = readDouble()
        val city = str()
        val citySlug = str()
        val country = str()
        val neighbourhood = str()
        val access = str()
        val paid = readBoolean()
        val transport = str()
        val story = str()
        val latin = List(readInt()) { readInt()..readInt() }
        val recognise = str()
        val url = str()
        val precision = if (readBoolean()) Precision.CONFIRMED else Precision.APPROXIMATE
        val photo = if (readBoolean()) photo() else null
        val saves = readInt()
        val mini = readBoolean()
        val photos = List(readInt()) { photo() }
        val seasonal = readBoolean()
        val months = List(readInt()) { readInt() }
        return Tree(
            id = id, name = name, species = species, age = age, ageShort = ageShort,
            ageMin = ageMin, ageMax = ageMax, highlight = highlight, highlightRank = rank,
            lat = lat, lng = lng, city = city, citySlug = citySlug, country = country,
            neighbourhood = neighbourhood, access = access, paidEntry = paid, transport = transport,
            story = story, storyLatin = latin, howToRecognise = recognise, url = url,
            precision = precision, photo = photo, saves = saves, mini = mini, photos = photos,
            seasonal = seasonal, bestMonths = months, seasonKey = opt(),
        )
    }
}
