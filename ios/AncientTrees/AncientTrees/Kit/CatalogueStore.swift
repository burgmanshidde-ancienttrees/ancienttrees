// Where the catalogue comes from, and the reason the app works with no signal.
//
// The bundled copy is the floor, not a cache: a fresh install on a plane still
// has every tree. The network only ever REPLACES it with something newer, and if
// that never happens the app is still complete.
//
// The replacing half was written in Sync.swift on 2026-08-19 and then never
// called by anything, which nobody noticed until the app was walked through on
// 2026-08-20. The consequence was quiet and total: a tree the night runs added
// could not reach a phone without a new build going through App Store review,
// on a project whose whole shape is that the data changes every single day and
// the app is just a reader of it. /api/version.json exists precisely so that
// checking costs a few dozen bytes. Now something calls it.
//
// Three rules in the code below, each of them a way of not making things worse:
//
// 1. A FAILED REFRESH IS A NON-EVENT. No error, no banner, no red. The whole
//    point of holding the catalogue on disk is that a plane, a forest or a dead
//    connection changes nothing about what the app can do.
// 2. THE DOWNLOAD IS ALL OR NOTHING. Trees, walks and species are fetched into
//    memory first and only written once all three decoded. A half-written
//    catalogue on disk is the one state that could break a fresh launch, and it
//    is the state a dropped connection produces if you write as you go.
// 3. THE BUNDLED COPY IS NEVER DELETED. Whatever happens to the downloaded one,
//    there is always a complete catalogue to fall back to.

import Foundation
import Observation

@Observable
public final class CatalogueStore {
    public private(set) var catalogue: Catalogue?
    public private(set) var loadError: String?
    public private(set) var isRefreshing = false
    /// Set when a refresh actually swapped the catalogue, so a screen can say
    /// so once rather than guessing.
    public private(set) var lastAdded: Int?

    public init() {}

    // MARK: - loading

    /// Read the newest catalogue on disk, which is the downloaded one if there
    /// is one and the bundled one otherwise.
    public func loadBundled() {
        if let c = decode(from: Self.downloadDirectory) {
            catalogue = c
            return
        }
        guard let b = Self.bundleURLs else {
            loadError = "the bundled catalogue is missing from the app"
            return
        }
        do {
            catalogue = try decode(trees: Data(contentsOf: b.trees),
                                   walks: Data(contentsOf: b.walks),
                                   species: b.species.flatMap { try? Data(contentsOf: $0) },
                                   browse: b.browse.flatMap { try? Data(contentsOf: $0) })
        } catch {
            loadError = "the bundled catalogue would not decode: \(error)"
        }
    }

    // MARK: - refreshing

    /// Ask the cheap endpoint whether the copy we hold is stale, and replace it
    /// if so. Safe to call on every launch and from a pull to refresh.
    public func refresh() async {
        guard !isRefreshing else { return }
        isRefreshing = true
        defer { isRefreshing = false }

        let outcome = await Sync.check(localVersion: catalogue?.version) { url in
            try await URLSession.shared.data(from: url).0
        }
        guard case .updated = outcome else { return }

        // Rule 2: everything decodes before anything is written.
        let speciesData = await fetch(Feed.species)
        let browseData = await fetch(Feed.browse)
        guard let treeData = await fetch(Feed.trees),
              let walkData = await fetch(Feed.walks),
              let fresh = try? decode(trees: treeData, walks: walkData,
                                      species: speciesData, browse: browseData)
        else { return }

        let before = catalogue?.trees.count ?? 0
        write(trees: treeData, walks: walkData, species: speciesData, browse: browseData)
        catalogue = fresh
        lastAdded = max(0, fresh.trees.count - before)
    }

    private func fetch(_ url: URL) async -> Data? {
        var r = URLRequest(url: url)
        r.timeoutInterval = 30      // a hang costs more than a refusal
        return try? await URLSession.shared.data(for: r).0
    }

    // MARK: - disk

    private static var downloadDirectory: URL? {
        guard let base = try? FileManager.default.url(for: .applicationSupportDirectory,
                                                      in: .userDomainMask,
                                                      appropriateFor: nil, create: true)
        else { return nil }
        return base.appending(path: "catalogue", directoryHint: .isDirectory)
    }

    private static var bundleURLs: (trees: URL, walks: URL, species: URL?, browse: URL?)? {
        guard let t = Bundle.main.url(forResource: "trees", withExtension: "json"),
              let w = Bundle.main.url(forResource: "walks", withExtension: "json") else { return nil }
        return (t, w,
                Bundle.main.url(forResource: "species", withExtension: "json"),
                Bundle.main.url(forResource: "browse", withExtension: "json"))
    }

    private func decode(from dir: URL?) -> Catalogue? {
        guard let dir,
              let t = try? Data(contentsOf: dir.appending(path: "trees.json")),
              let w = try? Data(contentsOf: dir.appending(path: "walks.json")) else { return nil }
        let s = try? Data(contentsOf: dir.appending(path: "species.json"))
        let b = try? Data(contentsOf: dir.appending(path: "browse.json"))
        return try? decode(trees: t, walks: w, species: s, browse: b)
    }

    private func decode(trees: Data, walks: Data, species: Data?, browse: Data?) throws -> Catalogue {
        let dec = JSONDecoder()
        let tf = try dec.decode(TreeFeed.self, from: trees)
        let wf = try dec.decode(WalkFeed.self, from: walks)
        let sp = species.flatMap { try? dec.decode(SpeciesFeed.self, from: $0) }?.species ?? []
        let co = browse.flatMap { try? dec.decode(BrowseFeed.self, from: $0) }?.collections ?? []
        return Catalogue(trees: tf.trees, walks: wf.walks, species: sp,
                         collections: co, version: tf.version)
    }

    private func write(trees: Data, walks: Data, species: Data?, browse: Data?) {
        guard let dir = Self.downloadDirectory else { return }
        try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
        // .atomic so a kill mid-write leaves the previous file rather than half
        // a file, which is the same reasoning as rule 2 one level down.
        try? trees.write(to: dir.appending(path: "trees.json"), options: .atomic)
        try? walks.write(to: dir.appending(path: "walks.json"), options: .atomic)
        if let species {
            try? species.write(to: dir.appending(path: "species.json"), options: .atomic)
        }
        if let browse {
            try? browse.write(to: dir.appending(path: "browse.json"), options: .atomic)
        }
    }
}
