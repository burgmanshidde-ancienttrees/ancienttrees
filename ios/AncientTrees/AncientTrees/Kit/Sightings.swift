// Your own trees: what you photographed, where, and when.
//
// The core act of the app, from 2026-08-21 (Hidde: "dat is echt de kern van
// de app... het is hetzelfde als dat je een hike in Strava gaat vastleggen").
// A tap is free and can be done from the sofa; a photograph is evidence and a
// souvenir at once, which is the rare case where the thing that proves you
// were there is the thing you wanted anyway.
//
// TWO LAYERS, and the distinction is his. OURS is the Remarkable Trees map:
// verified, sourced, published. YOURS is every tree you have photographed,
// including ours. A sighting of one of our trees carries its id; a sighting of
// a tree only you have found carries none and is yours alone until you offer
// it and we take it.
//
// PHOTOGRAPHS STAY ON THE PHONE. Nothing here is uploaded: no bucket, no table,
// no personal data on our side and no bill. Offering a tree to the platform
// sends the WORDS through the submissions channel the website already has, and
// the picture waits here until Hidde opens the storage question, which is his
// under the accounts rule and hard rule 5.

import Foundation
import Observation
import UIKit

@Observable
final class Sightings {

    enum Status: String, Codable, Sendable {
        /// Yours, and never offered. The ordinary case.
        case mine
        /// Offered to us, waiting to be looked at.
        case sent
        /// We are checking it.
        case checking
        /// It made the map.
        case published
        /// Not this time. It stays on YOUR map, which is the point.
        case declined

        var label: String {
            switch self {
            case .mine: "Yours"
            case .sent: "Sent to us"
            case .checking: "Being checked"
            case .published: "On the map"
            case .declined: "Not this time"
            }
        }
    }

    struct Sighting: Codable, Identifiable, Hashable, Sendable {
        var id: UUID = UUID()
        /// Our tree, when it is one of ours. Empty when only you have it.
        var treeId: String?
        var name: String
        var note: String = ""
        /// Filled in by you, on the tree's own page, and empty until then.
        var species: String?
        var age: String?
        var lat: Double
        var lng: Double
        var date: Date = Date()
        /// A file in Documents/sightings. Not a path: a phone's container
        /// moves between launches and an absolute path goes stale.
        var photo: String?
        var status: Status = .mine
    }

    private(set) var all: [Sighting] = []

    private static var folder: URL {
        let d = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("sightings", isDirectory: true)
        try? FileManager.default.createDirectory(at: d, withIntermediateDirectories: true)
        return d
    }
    private var index: URL { Self.folder.appendingPathComponent("index.json") }

    init() {
        if ProcessInfo.processInfo.arguments.contains("-reset-collection") {
            try? FileManager.default.removeItem(at: Self.folder)
            return
        }
        load()
    }

    // MARK: - reading

    /// Newest first, which is how anybody looks at their own photographs.
    var newestFirst: [Sighting] { all.sorted { $0.date > $1.date } }

    /// Only the ones nobody else has: your own finds, the second layer on the
    /// map.
    var yoursOnly: [Sighting] { newestFirst.filter { $0.treeId == nil } }

    func forTree(_ id: String) -> Sighting? { all.first { $0.treeId == id } }

    func image(_ s: Sighting) -> UIImage? {
        guard let f = s.photo else { return nil }
        return UIImage(contentsOfFile: Self.folder.appendingPathComponent(f).path)
    }

    // MARK: - editing

    /// Fill in a field on a tree only you have.
    ///
    /// Hidde, 2026-08-24, on where you land after adding one: "het is dezelfde
    /// boom pagina als onze bomen alleen dan dat de eindgebruiker de velden kan
    /// invullen." So a sighting grows the same fields one of ours has, and the
    /// page that renders ours renders it.
    func update(_ id: UUID, name: String? = nil, species: String? = nil,
                age: String? = nil, note: String? = nil, status: Status? = nil) {
        guard let i = all.firstIndex(where: { $0.id == id }) else { return }
        if let status { all[i].status = status }
        if let name, !name.isEmpty { all[i].name = name }
        if let species { all[i].species = species.isEmpty ? nil : species }
        if let age { all[i].age = age.isEmpty ? nil : age }
        if let note { all[i].note = note }
        persist()
    }

    /// The same page ours get, from what you have filled in so far.
    ///
    /// An adapter rather than a second screen: the tree page is 330 lines of
    /// hero, facts, story, access and a directions bar, and a copy of it for
    /// your own trees would drift within a week. Empty strings are honest here
    /// and the page already knows how to show a gap.
    func asTree(_ s: Sighting) -> Tree {
        Tree(id: "mine:" + s.id.uuidString,
             name: s.name,
             species: s.species ?? "",
             age: s.age,
             ageMin: nil,
             ageMax: nil,
             lat: s.lat,
             lng: s.lng,
             city: "",
             citySlug: "",
             country: "",
             neighbourhoodRaw: nil,
             access: "",
             // Your own tree never stands behind a ticket: you were there.
             paidEntryRaw: false,
             transportRaw: nil,
             story: s.note,
             url: "",
             // You photographed it where you stood, which is the one field a
             // tree of yours is never vague about.
             precision: .confirmed,
             photo: nil,
             bestTime: nil,
             peak: nil)
    }

    // MARK: - writing

    /// Records a sighting and returns it. The photograph is written first, so
    /// a crash between the two leaves an orphan file rather than a row
    /// pointing at nothing.
    @discardableResult
    func record(treeId: String?, name: String, note: String = "",
                lat: Double, lng: Double, image: UIImage?,
                status: Status = .mine) -> Sighting {
        var s = Sighting(treeId: treeId, name: name, note: note,
                         lat: lat, lng: lng, photo: nil, status: status)
        if let image, let data = Self.downsized(image) {
            let file = s.id.uuidString + ".jpg"
            try? data.write(to: Self.folder.appendingPathComponent(file))
            s.photo = file
        }
        all.append(s)
        persist()
        return s
    }

    func setStatus(_ id: UUID, _ status: Status) {
        guard let i = all.firstIndex(where: { $0.id == id }) else { return }
        all[i].status = status
        persist()
    }

    func remove(_ id: UUID) {
        guard let i = all.firstIndex(where: { $0.id == id }) else { return }
        if let f = all[i].photo {
            try? FileManager.default.removeItem(at: Self.folder.appendingPathComponent(f))
        }
        all.remove(at: i)
        persist()
    }

    // MARK: - the pieces

    /// 1600 points on the long edge at 0.8 quality: about 300 KB, which is a
    /// photograph worth keeping and a file worth uploading on the day that
    /// question is opened. A phone camera's original is ten times that and
    /// nothing on this screen is better for it.
    static func downsized(_ image: UIImage, max: CGFloat = 1600) -> Data? {
        let side = Swift.max(image.size.width, image.size.height)
        guard side > max else { return image.jpegData(compressionQuality: 0.8) }
        let scale = max / side
        let size = CGSize(width: image.size.width * scale, height: image.size.height * scale)
        let r = UIGraphicsImageRenderer(size: size)
        return r.image { _ in image.draw(in: CGRect(origin: .zero, size: size)) }
            .jpegData(compressionQuality: 0.8)
    }

    private func persist() {
        // NEVER WRITE OVER A FILE WE COULD NOT READ. This is the line that
        // turns a bad launch into permanent loss: load() silently returned
        // nothing, the list showed as empty, and the next thing that touched it
        // wrote that emptiness over the only copy there is.
        //
        // Hidde, 2026-08-27: "ik had ook ooit bomen toegevoegd en foto's in
        // Baarn en die zie ik niet meer, slaan we dit dan wel goed op." Whatever
        // took his, this is how a recoverable problem becomes an unrecoverable
        // one, and it was one `try?` away from happening to anybody.
        guard !unreadable else { return }
        guard let d = try? JSONEncoder().encode(all) else { return }
        try? d.write(to: index)
    }

    /// Set when the file exists and could not be understood. While it is true
    /// nothing overwrites the file, so the data is still there to be salvaged
    /// by a later version rather than gone.
    private(set) var unreadable = false

    /// Photographs on this phone with no row pointing at them. They are named
    /// after the sighting that made them, so they can be counted and shown even
    /// when the index that described them is broken.
    private(set) var orphanPhotos: [String] = []

    private func load() {
        guard let d = try? Data(contentsOf: index) else {
            // No file at all is the ordinary first launch, not a fault.
            findOrphans()
            return
        }
        if let list = try? JSONDecoder().decode([Sighting].self, from: d) {
            all = list
            findOrphans()
            return
        }

        // IT DID NOT DECODE. Keep the bytes before anything else happens to
        // them, then salvage what can be read row by row: one row that a later
        // version wrote differently must not take the other forty with it,
        // which is exactly what decoding the array in one go does.
        let copy = Self.folder.appendingPathComponent("index-unreadable.json")
        if !FileManager.default.fileExists(atPath: copy.path) {
            try? d.write(to: copy)
        }
        all = Self.salvage(d)
        unreadable = all.isEmpty
        findOrphans()
        // Only rewrite the index once something was actually recovered, and
        // the copy above survives either way.
        if !all.isEmpty { persist() }
    }

    /// Read the file as plain JSON and build what each row allows, filling in
    /// anything missing rather than throwing the row away. A sighting without a
    /// name or a position cannot be placed on a map and is the only kind
    /// dropped here.
    private static func salvage(_ data: Data) -> [Sighting] {
        guard let rows = (try? JSONSerialization.jsonObject(with: data)) as? [[String: Any]] else {
            return []
        }
        let iso = ISO8601DateFormatter()
        return rows.compactMap { r in
            guard let lat = r["lat"] as? Double, let lng = r["lng"] as? Double else { return nil }
            var s = Sighting(name: (r["name"] as? String) ?? "A tree you photographed",
                             lat: lat, lng: lng)
            if let id = r["id"] as? String, let u = UUID(uuidString: id) { s.id = u }
            s.treeId = r["treeId"] as? String
            s.note = (r["note"] as? String) ?? ""
            s.species = r["species"] as? String
            s.age = r["age"] as? String
            s.photo = r["photo"] as? String
            // Dates have been written two ways by JSONEncoder over this app's
            // life, as a number of seconds and as a string, and a salvage pass
            // that only understood one of them would date half the collection
            // to 2001.
            if let n = r["date"] as? Double { s.date = Date(timeIntervalSinceReferenceDate: n) }
            else if let t = r["date"] as? String, let d = iso.date(from: t) { s.date = d }
            if let st = r["status"] as? String, let k = Status(rawValue: st) { s.status = k }
            return s
        }
    }

    /// Photographs in the folder that no row mentions. Never deleted: a picture
    /// somebody took of a tree they walked to is the least replaceable thing in
    /// this app, and an index that lost track of it is our fault rather than
    /// theirs.
    private func findOrphans() {
        let known = Set(all.compactMap(\.photo))
        let files = (try? FileManager.default.contentsOfDirectory(atPath: Self.folder.path)) ?? []
        orphanPhotos = files.filter { $0.hasSuffix(".jpg") && !known.contains($0) }.sorted()
    }

    /// Everything this phone holds, as one file somebody can keep. The
    /// photographs are in it, so it is a real backup rather than a list of
    /// names, and it is the answer to "is this saved anywhere" for as long as
    /// these trees live only on the phone.
    func exportArchive() -> URL? {
        let out = FileManager.default.temporaryDirectory
            .appendingPathComponent("my-trees-backup.json")
        var rows: [[String: Any]] = []
        for s in all {
            var r: [String: Any] = ["id": s.id.uuidString, "name": s.name, "note": s.note,
                                    "lat": s.lat, "lng": s.lng,
                                    "date": ISO8601DateFormatter().string(from: s.date),
                                    "status": s.status.rawValue]
            r["treeId"] = s.treeId
            r["species"] = s.species
            r["age"] = s.age
            if let f = s.photo,
               let d = try? Data(contentsOf: Self.folder.appendingPathComponent(f)) {
                r["photo_jpeg_base64"] = d.base64EncodedString()
            }
            rows.append(r)
        }
        guard let d = try? JSONSerialization.data(withJSONObject: rows, options: [.prettyPrinted])
        else { return nil }
        try? d.write(to: out)
        return out
    }

}
