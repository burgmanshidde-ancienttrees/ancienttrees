// Walks you made yourself.
//
// Hidde, 2026-08-24, naming it as one of the four things the app is for: "ik
// wil een nieuwe wandelroute maken incl mijn bomen en kunnen delen."
//
// TWO KINDS OF WALK, and the difference decides everything about how they are
// stored and addressed. OURS are computed: a script groups the trees that stand
// near each other, so adding a tree tonight can split a walk, move its start
// and change its generated name. YOURS is a decision a person made, and it does
// not move when we publish anything. That is why ours live at a city's address
// (/[city]/walks) and why one of yours can later have a permanent one of its
// own, and it is why this file exists at all rather than reusing Walk.
//
// ON THE PHONE, for now. Sharing needs a row on a server, which is a table
// holding somebody's data and therefore Hidde's yes under the accounts rule.
// Making and keeping does not, so making and keeping ships first and finds out
// whether anybody wants this at all.
//
// STOPS ARE IDS OR SIGHTINGS. A stop is one of ours (a tree id) or one only you
// have (a sighting id), because the whole point is that you can be standing in
// front of something we have never mapped and put it in your walk anyway.
import Foundation
import Observation
import CoreLocation

@Observable
final class MyWalks {

    struct Stop: Codable, Hashable, Sendable, Identifiable {
        /// Ours, when it is one of ours.
        var treeId: String?
        /// Yours, when only you have it. Exactly one of the two is set.
        var sightingId: UUID?
        var lat: Double
        var lng: Double
        var name: String

        var id: String { treeId ?? sightingId?.uuidString ?? "\(lat),\(lng)" }
        var coordinate: CLLocationCoordinate2D { .init(latitude: lat, longitude: lng) }
    }

    struct Walk: Codable, Hashable, Sendable, Identifiable {
        var id: UUID = UUID()
        var name: String
        var stops: [Stop]
        var madeAt: Date = Date()
        /// The routed shape, [lng, lat], fetched ONCE when the walk is saved
        /// rather than on every tap: a tap that waits for a server feels worse
        /// than a straight line, and one call per walk is what a community
        /// routing service is for. Nil means nobody has walked it for us and
        /// the line is the order rather than the path, which the map already
        /// draws dashed and says out loud.
        var shape: [[Double]]?
        var km: Double
        var minutes: Int

        var count: Int { stops.count }
    }

    private(set) var all: [Walk] = []

    private static var file: URL {
        let d = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        return d.appendingPathComponent("my-walks.json")
    }

    init() { load() }

    func walk(_ id: UUID) -> Walk? { all.first { $0.id == id } }

    func save(_ w: Walk) {
        if let i = all.firstIndex(where: { $0.id == w.id }) {
            all[i] = w
        } else {
            all.insert(w, at: 0)
        }
        persist()
    }

    func remove(_ id: UUID) {
        all.removeAll { $0.id == id }
        persist()
    }

    private func persist() {
        guard let d = try? JSONEncoder().encode(all) else { return }
        try? d.write(to: Self.file, options: .atomic)
    }

    private func load() {
        guard let d = try? Data(contentsOf: Self.file),
              let w = try? JSONDecoder().decode([Walk].self, from: d) else { return }
        all = w
    }
}

// MARK: - the straight line, and the real one

extension MyWalks {

    /// Kilometres along the stops in the order they are in. Used while
    /// building, where it has to answer instantly and be honest that it is the
    /// crow's distance rather than the walk's.
    static func straightKm(_ stops: [Stop]) -> Double {
        guard stops.count > 1 else { return 0 }
        var total = 0.0
        for (a, b) in zip(stops, stops.dropFirst()) {
            let l1 = CLLocation(latitude: a.lat, longitude: a.lng)
            let l2 = CLLocation(latitude: b.lat, longitude: b.lng)
            total += l1.distance(from: l2)
        }
        return total / 1000
    }

    /// A rough walking time from a distance. 4.5 km/h, the same figure
    /// scripts/route_walks.py falls back to, so an estimate here and one on the
    /// website do not disagree about the same walk.
    static func minutes(forKm km: Double) -> Int { Int((km / 4.5) * 60) }
}
