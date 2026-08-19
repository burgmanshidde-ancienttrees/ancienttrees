// Where the catalogue comes from, and the reason the app works with no signal.
//
// The bundled copy is the floor, not a cache: a fresh install on a plane still
// has all 1377 trees. The network only ever REPLACES it with something newer,
// and if that never happens the app is still complete.

import Foundation
import Observation

@Observable
public final class CatalogueStore {
    public private(set) var catalogue: Catalogue?
    public private(set) var loadError: String?

    public init() {}

    /// Read the copy that shipped inside the app. Synchronous and fast enough:
    /// 2.5 MB of JSON decodes in well under a second, and doing it off the main
    /// actor would buy a spinner nobody needs to see.
    public func loadBundled() {
        guard let t = Bundle.main.url(forResource: "trees", withExtension: "json"),
              let w = Bundle.main.url(forResource: "walks", withExtension: "json") else {
            loadError = "the bundled catalogue is missing from the app"
            return
        }
        do {
            let dec = JSONDecoder()
            let tf = try dec.decode(TreeFeed.self, from: Data(contentsOf: t))
            let wf = try dec.decode(WalkFeed.self, from: Data(contentsOf: w))
            var sp: [Species] = []
            if let s = Bundle.main.url(forResource: "species", withExtension: "json") {
                sp = (try? dec.decode(SpeciesFeed.self, from: Data(contentsOf: s)))?.species ?? []
            }
            catalogue = Catalogue(trees: tf.trees, walks: wf.walks,
                                  species: sp, version: tf.version)
        } catch {
            loadError = "the bundled catalogue would not decode: \(error)"
        }
    }
}
