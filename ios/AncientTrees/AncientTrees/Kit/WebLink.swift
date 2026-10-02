// A web address of ours, turned into a screen.
//
// Convention: Universal Links the way AllTrails and Google Maps use them. A
// link to a trail or a place opens the app when it is installed and the page
// when it is not, and the same link is shared either way. The association file
// on the website (site/public/.well-known/apple-app-site-association) says
// which paths iOS hands to the app; scripts/qa.py refuses a route on the site
// that is neither claimed there nor excluded, so a new page type has to decide.
//
// Hidde, 2026-10-02: "I have the app but whenever clicking it opens the website
// but it should prefer app open if there." Until then the file claimed only
// /t, /auth and /open, so every tree and city link went to Safari by design.
//
// PURE on purpose: the parser takes closures for what the catalogue knows, so
// AncientTreesTests/WebLinkTests.swift can prove every path shape without a
// catalogue, and ContentView passes the live one.
import Foundation

public enum WebLink {
    public enum Target: Equatable {
        case route(Route)
        /// /explore: the map tab itself, which is not a Route.
        case map
        /// The home page, an unknown path, or a page the app has no screen for.
        case none
    }

    public struct Lookup {
        /// "/paris/turkey-oak-of-square-rene-le-gall" -> "par_033"
        public var treeId: (String) -> String?
        public var isCity: (String) -> Bool
        /// A country page slug -> the country's name as the feed spells it.
        public var countryName: (String) -> String?
        /// A species page slug -> the common name Route.species expects.
        public var speciesName: (String) -> String?

        public init(treeId: @escaping (String) -> String?, isCity: @escaping (String) -> Bool,
                    countryName: @escaping (String) -> String?, speciesName: @escaping (String) -> String?) {
            self.treeId = treeId; self.isCity = isCity
            self.countryName = countryName; self.speciesName = speciesName
        }

        public static let empty = Lookup(treeId: { _ in nil }, isCity: { _ in false },
                                         countryName: { _ in nil }, speciesName: { _ in nil })

        public init(catalogue cat: Catalogue?) {
            guard let cat else { self = .empty; return }
            self.init(
                treeId: { path in
                    let parts = path.split(separator: "/").map(String.init)
                    guard let city = parts.first else { return nil }
                    return cat.trees(inCity: city).first(where: { $0.url == path })?.id
                },
                isCity: { !cat.trees(inCity: $0).isEmpty },
                countryName: { slug in cat.countriesWithTrees.keys.first(where: { WebLink.slugify($0) == slug }) },
                speciesName: { slug in cat.speciesNames.first(where: { WebLink.slugify($0) == slug }) })
        }
    }

    /// The seven translated sites live under a prefix; the screens are the same.
    public static let languages: Set<String> = ["de", "es", "fr", "it", "nl", "pt", "ja"]

    public static func parse(_ comps: URLComponents, lookup: Lookup) -> Target {
        var parts = comps.path.split(separator: "/").map(String.init).filter { !$0.isEmpty }
        // A shared sighting, the first link this app ever claimed (2026-09-03).
        if parts.first == "t" {
            guard let idStr = comps.queryItems?.first(where: { $0.name == "id" })?.value,
                  let id = UUID(uuidString: idStr) else { return .none }
            return .route(.shared(id))
        }
        if let first = parts.first, languages.contains(first) { parts.removeFirst() }
        guard let first = parts.first else { return .none }
        switch first {
        case "explore":
            return .map
        case "species":
            guard parts.count == 2, let name = lookup.speciesName(parts[1]) else { return .none }
            return .route(.species(name))
        case "collections":
            guard parts.count == 2 else { return .none }
            return .route(.collection(parts[1]))
        default:
            break
        }
        // /<city>/<tree>, and /<city>/<question page> falls back to the city.
        if parts.count >= 2, let id = lookup.treeId("/" + parts[0] + "/" + parts[1]) {
            return .route(.tree(id))
        }
        if lookup.isCity(first) { return .route(.city(first)) }
        if let name = lookup.countryName(first) { return .route(.country(name)) }
        return .none
    }

    /// The website's slug rules (site/src/lib/slug.ts): lower case, apostrophes
    /// dropped, a leading "the " dropped, accents folded away, anything that is
    /// not a letter or digit becomes one hyphen.
    public static func slugify(_ name: String) -> String {
        var s = name.lowercased().replacingOccurrences(of: "'", with: "").replacingOccurrences(of: "\u{2019}", with: "")
        if s.hasPrefix("the ") { s = String(s.dropFirst(4)) }
        s = s.folding(options: [.diacriticInsensitive, .widthInsensitive], locale: nil)
        var out = ""
        var hyphen = false
        for ch in s.unicodeScalars {
            if (ch.value >= 97 && ch.value <= 122) || (ch.value >= 48 && ch.value <= 57) {
                out.unicodeScalars.append(ch); hyphen = false
            } else if ch.value < 128 {
                if !hyphen && !out.isEmpty { out.append("-"); hyphen = true }
            }
        }
        while out.hasSuffix("-") { out.removeLast() }
        return out
    }
}
