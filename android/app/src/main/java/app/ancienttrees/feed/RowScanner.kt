// Reads a feed one row at a time, so an 11.5 MB catalogue never becomes one
// tree of JSON objects in memory (org.json over the whole file took seconds and
// about 100 MB on the emulator where the iPhone opens at once). The text is
// walked once by index and each row cut out as its own string, which org.json
// then reads; rows are independent, so they can be read on every core.
// A scanner of our own rather than android.util.JsonReader, which measured
// slower (10 s only to skim the file on the emulator) and does not exist in the
// unit tests on the build machine.

package app.ancienttrees.feed

import java.io.Reader

object RowScanner {

    class Result(val version: String?, val rows: List<String>)

    fun scan(reader: Reader, key: String): Result = scan(reader.readText().toCharArray(), key)

    /**
     * The top-level "version" string and the text of every object in the
     * top-level array named [key]. Anything else in the file is skipped.
     */
    fun scan(c: CharArray, key: String): Result {
        var version: String? = null
        val rows = ArrayList<String>(4096)
        val n = c.size
        var depth = 0
        var i = 0
        // The last string closed at depth 1 (a key or a value), and its span.
        var lastStart = -1
        var lastEnd = -1
        var expectVersion = false
        var inArray = false
        var rowStart = -1
        while (i < n) {
            val ch = c[i]
            if (ch == '"') {
                val start = i + 1
                i++
                while (i < n) {
                    val d = c[i]
                    if (d == '\\') {
                        i += 2
                        continue
                    }
                    if (d == '"') break
                    i++
                }
                if (rowStart < 0 && depth == 1) {
                    lastStart = start
                    lastEnd = i
                    if (expectVersion) {
                        version = String(c, start, i - start)
                        expectVersion = false
                    }
                }
                i++
                continue
            }
            when (ch) {
                ':' -> if (rowStart < 0 && depth == 1) {
                    expectVersion = matches(c, lastStart, lastEnd, "version")
                    inArray = matches(c, lastStart, lastEnd, key)
                }
                '{' -> {
                    if (rowStart < 0 && inArray && depth == 2) rowStart = i
                    depth++
                }
                '[' -> depth++
                '}' -> {
                    depth--
                    if (rowStart >= 0 && depth == 2) {
                        rows.add(String(c, rowStart, i - rowStart + 1))
                        rowStart = -1
                    }
                }
                ']' -> {
                    depth--
                    if (depth == 1) inArray = false
                }
                ',' -> if (depth == 1) {
                    expectVersion = false
                    inArray = false
                }
            }
            i++
        }
        return Result(version, rows)
    }

    private fun matches(c: CharArray, start: Int, end: Int, word: String): Boolean {
        if (start < 0 || end - start != word.length) return false
        for (k in word.indices) if (c[start + k] != word[k]) return false
        return true
    }
}
