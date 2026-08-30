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

/// Main-actor isolated, like every store the root holds. See Account.swift for
/// why: SwiftUI already reads these from the main actor, so the annotation
/// costs nothing at runtime and makes a background write a compiler error
/// instead of a data race nobody can reproduce.
@MainActor
@Observable
public final class CatalogueStore {
    public private(set) var catalogue: Catalogue?
    public private(set) var loadError: String?
    public private(set) var isRefreshing = false
    /// Set when a refresh actually swapped the catalogue, so a screen can say
    /// so once rather than guessing.
    public private(set) var lastAdded: Int?

    /// Where a synced catalogue is kept. Application Support on a phone; a
    /// throwaway directory in a test, because these tests are about a download
    /// that no longer fits and must not touch the simulator's real one.
    private let downloads: URL?

    public init(downloads: URL? = nil) {
        self.downloads = downloads ?? Self.defaultDownloadDirectory
    }

    // MARK: - loading

    /// Read the newest catalogue, file by file: the downloaded copy where there
    /// is one, and the bundled copy for anything it does not have.
    ///
    /// An OVERLAY rather than a replacement, and that distinction is a bug this
    /// found rather than a nicety. The first version preferred the download
    /// directory wholesale, which broke the moment a new feed was added: a phone
    /// that had already synced trees, walks and species held a complete-looking
    /// download directory with no browse.json in it, so it showed zero
    /// collections. And it would have stayed that way, because refresh() asks
    /// whether the version changed and the version had not: the phone was up to
    /// date with a file it had never heard of. Falling back per file means a new
    /// feed works on the old download the first time it is asked for.
    /// OFF THE MAIN THREAD, and the reason is the second caller rather than this
    /// one.
    ///
    /// Reading and decoding a few megabytes of JSON is a hundred milliseconds
    /// or two on an older phone. At launch that hides behind the opening cover
    /// and nobody sees it. But refresh() below decodes the same feeds while
    /// somebody is looking at a live map and may be dragging it, and that one
    /// is a stutter in the one interaction this app is made of. Both go through
    /// the same nonisolated worker now, so neither can block a frame.
    ///
    /// Everything that TOUCHES this object still happens on the main actor. The
    /// worker is a pure function of two file locations: it reads, it decodes,
    /// it hands back an answer, and this method is the only thing that assigns.
    public func loadBundled() async {
        let dir = downloads
        let bundle = Self.bundleURLs
        switch await Task.detached(priority: .userInitiated, operation: {
            Self.readAndDecode(dir: dir, bundle: bundle)
        }).value {
        case .ok(let fresh):
            catalogue = fresh
            loadError = nil
        case .fellBackToTheBundle(let fresh):
            catalogue = fresh
            loadError = nil
            // Throw the stale download away. It is a cache of public data,
            // rebuilt by the next refresh, and leaving it means paying this
            // failure on every launch: refresh() asks whether the VERSION
            // changed, and it has not, so nothing would ever replace it.
            if let dir { try? FileManager.default.removeItem(at: dir) }
        case .failed(let why):
            loadError = why
        }
    }

    private enum Loaded {
        case ok(Catalogue)
        case fellBackToTheBundle(Catalogue)
        case failed(String)
    }

    /// The reading and the decoding, with nothing of this object in it, so it
    /// can run anywhere. The rules it keeps are unchanged and are the three at
    /// the top of this file.
    nonisolated private static func readAndDecode(
        dir: URL?, bundle: (trees: URL, walks: URL, species: URL?, browse: URL?)?
    ) -> Loaded {
        func read(_ name: String, _ bundled: URL?) -> Data? {
            if let dir, let d = try? Data(contentsOf: dir.appending(path: "\(name).json")) { return d }
            return bundled.flatMap { try? Data(contentsOf: $0) }
        }

        guard let trees = read("trees", bundle?.trees),
              let walks = read("walks", bundle?.walks) else {
            return .failed("the bundled catalogue is missing from the app")
        }
        do {
            return .ok(try decode(trees: trees,
                                  walks: walks,
                                  species: read("species", bundle?.species),
                                  browse: read("browse", bundle?.browse)))
        } catch {
            // FALL BACK TO THE BUNDLE, which rule 3 at the top of this file has
            // promised since it was written and did not actually do.
            //
            // The fallback above is per FILE and per PRESENCE: a downloaded
            // trees.json that exists is preferred whether or not it can still be
            // read. So a phone that had ever synced, meeting an app update where
            // a model gained a required field, decoded nothing at all and showed
            // an empty app, with a perfect bundled copy sitting beside it and no
            // way out but delete and reinstall. That is the exact shape of an
            // upgrade going wrong, and it would have hit everybody who uses the
            // app rather than a few unlucky ones (2026-08-27).
            guard let bundle,
                  let bt = try? Data(contentsOf: bundle.trees),
                  let bw = try? Data(contentsOf: bundle.walks),
                  let fresh = try? decode(trees: bt, walks: bw,
                                          species: bundle.species.flatMap { try? Data(contentsOf: $0) },
                                          browse: bundle.browse.flatMap { try? Data(contentsOf: $0) })
            else {
                return .failed("the catalogue would not decode: \(error)")
            }
            return .fellBackToTheBundle(fresh)
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
            try await Net.data(from: url).0
        }
        guard case .updated = outcome else { return }

        // Rule 2: everything decodes before anything is written.
        let speciesData = await fetch(Feed.species)
        let browseData = await fetch(Feed.browse)
        guard let treeData = await fetch(Feed.trees),
              let walkData = await fetch(Feed.walks),
              // Decoded off the main thread. This runs while somebody is
              // looking at the map and possibly dragging it.
              let fresh = await Task.detached(priority: .utility, operation: {
                  try? Self.decode(trees: treeData, walks: walkData,
                                   species: speciesData, browse: browseData)
              }).value
        else { return }

        let before = catalogue?.trees.count ?? 0
        write(trees: treeData, walks: walkData, species: speciesData, browse: browseData)
        catalogue = fresh
        lastAdded = max(0, fresh.trees.count - before)
    }

    private func fetch(_ url: URL) async -> Data? {
        var r = URLRequest(url: url)
        r.timeoutInterval = 30      // a hang costs more than a refusal
        return try? await Net.data(for: r).0
    }

    // MARK: - disk

    nonisolated static var defaultDownloadDirectory: URL? {
        guard let base = try? FileManager.default.url(for: .applicationSupportDirectory,
                                                      in: .userDomainMask,
                                                      appropriateFor: nil, create: true)
        else { return nil }
        return base.appending(path: "catalogue", directoryHint: .isDirectory)
    }

    nonisolated private static var bundleURLs: (trees: URL, walks: URL, species: URL?, browse: URL?)? {
        guard let t = Bundle.main.url(forResource: "trees", withExtension: "json"),
              let w = Bundle.main.url(forResource: "walks", withExtension: "json") else { return nil }
        return (t, w,
                Bundle.main.url(forResource: "species", withExtension: "json"),
                Bundle.main.url(forResource: "browse", withExtension: "json"))
    }

    nonisolated private static func decode(trees: Data, walks: Data, species: Data?, browse: Data?) throws -> Catalogue {
        let dec = JSONDecoder()
        let tf = try dec.decode(TreeFeed.self, from: trees)
        let wf = try dec.decode(WalkFeed.self, from: walks)
        let sp = species.flatMap { try? dec.decode(SpeciesFeed.self, from: $0) }?.species ?? []
        let bf = browse.flatMap { try? dec.decode(BrowseFeed.self, from: $0) }
        return Catalogue(trees: tf.trees, walks: wf.walks, species: sp,
                         collections: bf?.collections ?? [],
                         facets: BrowseFacets(feed: bf), version: tf.version)
    }

    private func write(trees: Data, walks: Data, species: Data?, browse: Data?) {
        guard let dir = downloads else { return }
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
