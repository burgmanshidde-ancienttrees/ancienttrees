// Never load the original. 278 of our 353 photographs are wider than 1500px and
// one is 8368px across, so a list asking for originals downloads tens of
// megabytes to draw thumbnails. The website solved this in thumbUrl() and
// scripts/qa.py fails its build if any img ships a full-resolution original.
//
// Ported from site/src/lib/images.ts rather than reinvented, and the first
// attempt here proved why: it asked Wikimedia for 800px and every request came
// back 400. Wikimedia has served only fixed thumbnail buckets since 2024, and
// the website had already probed which ones are live (250/330/500/960) and
// written it down. Reading our own code first would have saved the round trip.
//
// SINCE 2026-08-25 THIS IS A FALLBACK, NOT THE PATH. The feed now carries the
// card and hero urls already resolved (Photo.card, Photo.full), so the bucket
// table below only runs for a snapshot bundled before that date. That is the
// general shape CLAUDE.md now states: an answer travels in the feed, a rule
// stays on the server. A bucket table is a rule, and this one had to learn
// Wikimedia's answer twice.

import Foundation

public enum Photos {
    /// The buckets Wikimedia actually serves. 400 and 800 are 400s.
    private static let wikimediaBuckets = [250, 330, 500, 960]

    public static func thumb(_ url: String, width: Int) -> URL? {
        if url.contains("upload.wikimedia.org/wikipedia/commons/"), !url.contains("/thumb/"),
           let marker = url.range(of: "/wikipedia/commons/") {
            let head = String(url[..<marker.lowerBound])
            let tail = String(url[marker.upperBound...])
            let fname = tail.split(separator: "/").last.map(String.init) ?? ""
            let ext = fname.lowercased()
            guard ext.hasSuffix(".jpg") || ext.hasSuffix(".jpeg")
                    || ext.hasSuffix(".png") || ext.hasSuffix(".gif") else {
                return URL(string: url)
            }
            let w = wikimediaBuckets.first { width <= $0 } ?? 960
            return URL(string: "\(head)/wikipedia/commons/thumb/\(tail)/\(w)px-\(fname)")
        }
        if url.contains("inaturalist") {
            for size in ["/original.", "/large.", "/medium."] where url.contains(size) {
                return URL(string: url.replacingOccurrences(
                    of: size, with: width <= 500 ? "/medium." : "/large."))
            }
        }
        return URL(string: url)
    }

    /// CC BY and BY-SA oblige a visible credit. That is the licence's price and
    /// it is never stripped: a photo that cannot carry its credit is replaced,
    /// not shown bare.
    /// The credit, trimmed to what the licence actually asks for.
    ///
    /// CC BY and BY-SA want the author and the terms. The HOST is neither, so
    /// "via Wikimedia Commons" is dropped: it doubled the length of every
    /// credit on the site and told the reader nothing they needed (Hidde,
    /// 2026-08-21, "als de foto referentie subtieler kan"). Where the host is
    /// all we have, it stays, because a photograph with no attributable name
    /// still has to say where it came from.
    public static func credit(_ p: Photo) -> String? {
        guard p.creditRequired else { return nil }
        var who = p.attribution
        if var a = who {
            for host in [", via Wikimedia Commons", " via Wikimedia Commons",
                         ", Wikimedia Commons", ", via Flickr", ", via iNaturalist"] {
                if a.hasSuffix(host) { a = String(a.dropLast(host.count)); break }
            }
            who = a.trimmingCharacters(in: .whitespacesAndNewlines)
            if who?.isEmpty == true { who = p.attribution }
        }
        return [who, p.license].compactMap { $0 }.joined(separator: " · ")
    }
}
