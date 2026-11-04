// The map redraws when what a pin shows changed, not only when the set of ids
// did (audit, 2026-11-04).
//
// Until then a catalogue refresh that corrected a coordinate, gave a tree its
// first photograph (photo pins are drawn first where two collide) or fixed a
// name reached the map only after a restart, because the redraw compared ids.
// Your own pins compared ids too, and the route compared only its point count,
// so two walks of the same length kept the first one's line.
//
// The fast path stays where it was (same array, same storage, nothing to do);
// these tests pin the comparison behind it.

import Testing
import Foundation
import CoreLocation
import UIKit
@testable import AncientTrees

@MainActor
struct TheMapRedrawsWhatChanged {

    private static func tree(_ id: String, lat: Double = 52.37, lng: Double = 4.89,
                             name: String = "The Oak", photo: Bool = false) -> Tree {
        let p = photo
            ? """
              {"url":"https://ancienttrees.app/photos/x.jpg","license":"x",
               "attribution":null,"width":1600,"height":1200,
               "thumb":"https://ancienttrees.app/photos/x-500.jpg",
               "hero":"https://ancienttrees.app/photos/x.jpg",
               "credit_required":false,"attribution_short":null,"credit_line":null}
              """
            : "null"
        let json = """
        {"id":"\(id)","name":"\(name)",
         "species":"Pedunculate Oak (Quercus robur)","age":null,
         "age_min":null,"age_max":null,"lat":\(lat),"lng":\(lng),
         "city":"Amsterdam","city_slug":"amsterdam","country":"Netherlands",
         "neighbourhood":null,"access":"","transport":null,
         "precision":"confirmed","best_time":null,"peak":null,"story":"",
         "how_to_recognise":null,"url":"","photo":\(p)}
        """
        return try! JSONDecoder().decode(Tree.self, from: Data(json.utf8))
    }

    private func keys(_ trees: [Tree], collected: Set<String> = [],
                      favourites: Set<String> = []) -> Set<TreeMap.TreeDrawKey> {
        TreeMap.drawKeys(trees, collected: collected, favourites: favourites)
    }

    @Test func theSameTreesDrawTheSame() {
        #expect(keys([Self.tree("a"), Self.tree("b")]) == keys([Self.tree("b"), Self.tree("a")]))
    }

    @Test func aMovedPinRedraws() {
        #expect(keys([Self.tree("a")]) != keys([Self.tree("a", lat: 52.38)]))
    }

    @Test func aFirstPhotographRedraws() {
        #expect(keys([Self.tree("a")]) != keys([Self.tree("a", photo: true)]))
    }

    @Test func aFixedNameRedraws() {
        #expect(keys([Self.tree("a")]) != keys([Self.tree("a", name: "The Elm")]))
    }

    @Test func tickingOffOrSavingRedraws() {
        let t = [Self.tree("a")]
        #expect(keys(t) != keys(t, collected: ["a"]))
        #expect(keys(t) != keys(t, favourites: ["a"]))
        // A tick on a tree this map does not draw changes nothing here.
        #expect(keys(t) == keys(t, collected: ["zzz"]))
    }

    @Test func yourPinRedrawsWhenItMovesOrGetsAPhoto() {
        let id = UUID()
        let still = TreeMap.drawKeys([(id: id, lat: 1, lng: 2, name: "Fig", photo: nil)])
        let moved = TreeMap.drawKeys([(id: id, lat: 1.001, lng: 2, name: "Fig", photo: nil)])
        let shot = TreeMap.drawKeys([(id: id, lat: 1, lng: 2, name: "Fig", photo: UIImage())])
        let again = TreeMap.drawKeys([(id: id, lat: 1, lng: 2, name: "Fig", photo: nil)])
        #expect(still != moved)
        #expect(still != shot)
        #expect(still == again)
    }

    @Test func twoWalksOfTheSameLengthAreTwoLines() {
        let a = [CLLocationCoordinate2D(latitude: 1, longitude: 1),
                 CLLocationCoordinate2D(latitude: 2, longitude: 2)]
        let b = [CLLocationCoordinate2D(latitude: 1, longitude: 1),
                 CLLocationCoordinate2D(latitude: 3, longitude: 3)]
        #expect(TreeMap.sameRoute(a, true, a, true))
        #expect(!TreeMap.sameRoute(a, true, b, true))
        #expect(!TreeMap.sameRoute(a, true, a, false))
        #expect(!TreeMap.sameRoute(a, true, [], true))
    }
}
