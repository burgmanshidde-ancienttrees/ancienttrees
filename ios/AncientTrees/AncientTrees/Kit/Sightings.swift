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
// PHOTOGRAPHS STAY ON THE PHONE UNTIL YOU SIGN IN, and that is the whole of
// what this file does: it is the on-device store and it uploads nothing.
//
// This paragraph said "nothing here is uploaded, no bucket, no table, no
// personal data on our side" until 2026-08-28, and by then that was false at
// the level a reader of this file would care about: SightingSync.push, called
// from ContentView on every change, sends the photograph to the sightings
// bucket and a row carrying user_id, lat, lng, note and taken_at. The storage
// question Hidde was supposed to open had been opened and this comment never
// heard. It was found while filling in Apple's privacy questionnaire, which is
// a declaration in his name, so a stale comment was one step from a false
// legal answer.
//
// Offering a tree to the PLATFORM is still a separate, deliberate step through
// the submissions channel. Syncing your own sightings to your own account is
// not that, and the privacy page now says so.

import Foundation
import Observation
import UIKit

/// Main-actor isolated, like every store the root holds. See Account.swift for
/// why: SwiftUI already reads these from the main actor, so the annotation
/// costs nothing at runtime and makes a background write a compiler error
/// instead of a data race nobody can reproduce.
@MainActor
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

        /// When the account last took a copy of this, photograph and all.
        ///
        /// It exists to answer one question and only that one: may this be
        /// dropped from the phone when nobody is signed in. A sighting the
        /// server has can always come back; one it has never seen cannot come
        /// back from anywhere. Optional so a file written before 2026-08-29
        /// still decodes, and nil means the honest thing, which is that we do
        /// not know it arrived.
        var syncedAt: Date?

        /// The id this sighting wears wherever the app talks about TREES: the
        /// heart on its page saves under it, so anything asking whether you
        /// hearted your own tree has to ask with this exact string. Written
        /// once here rather than at each site that spells out the prefix.
        var treeKey: String { "mine:" + id.uuidString }

        /// What you typed, without any Latin you put in brackets, so the map's
        /// species filter compares like with like.
        var commonName: String? {
            guard let s = species, !s.isEmpty else { return nil }
            return Tree.commonName(of: s)
        }
    }

    private(set) var all: [Sighting] = []

    /// Where a change goes after it has been written here. Set once by the root
    /// (ContentView), which is the only place that knows about an account, so
    /// this file keeps knowing nothing about the network.
    static var syncOne: ((Sighting) -> Void)?
    static var syncGone: ((UUID) -> Void)?

    /// Documents/sightings on a phone. A test passes its own throwaway
    /// directory instead, because these tests are ABOUT losing trees and two of
    /// them sharing a folder would read each other's collection, or worse,
    /// the collection of whoever is using the simulator.
    nonisolated static var defaultFolder: URL {
        let d = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("sightings", isDirectory: true)
        try? FileManager.default.createDirectory(at: d, withIntermediateDirectories: true)
        return d
    }

    private let folder: URL
    private var index: URL { folder.appendingPathComponent("index.json") }

    nonisolated private static func ensure(_ d: URL) {
        try? FileManager.default.createDirectory(at: d, withIntermediateDirectories: true)
    }

    init(folder: URL? = nil) {
        self.folder = folder ?? Self.defaultFolder
        // The directory has to exist before anything reads or writes in it.
        // It used to be recreated on every access, because `folder` was a
        // computed property that made it each time; now that it is stored once,
        // making it is explicit, and it has to happen again after a reset wipes
        // it or every later write fails silently.
        Self.ensure(self.folder)
        if ProcessInfo.processInfo.arguments.contains("-reset-collection") {
            try? FileManager.default.removeItem(at: self.folder)
            Self.ensure(self.folder)
        } else {
            load()
        }
        // AFTER the reset rather than instead of it: the two arguments are
        // used together all the time (start clean, then put these two in), and
        // the first version returned early so the seed never ran.
        seedDemo()
    }

    /// Two of your own trees, with a photograph each, behind -mine-demo.
    ///
    /// The same debug scaffolding as -collected= and -people-demo, and it fills
    /// the same kind of gap: a tree you added yourself needs a photograph on a
    /// device to exist at all, so its pin and its card had never been in a
    /// screenshot. A picture drawn here is not a real photograph, and it does
    /// not need to be: what is being looked at is whether a photograph fits the
    /// pin, keeps its shape and reads against a map.
    private func seedDemo() {
        let args = ProcessInfo.processInfo.arguments
        guard args.contains("-mine-demo"), all.isEmpty else { return }
        var lat = 52.3731, lng = 4.8922
        if let at = args.first(where: { $0.hasPrefix("-at=") })?.dropFirst(4) {
            let parts = at.split(separator: ",")
            if parts.count == 2, let a = Double(parts[0]), let b = Double(parts[1]) {
                lat = a; lng = b
            }
        }
        for (i, name) in ["The oak on my street", "The lime by the water"].enumerated() {
            let made = record(treeId: nil, name: name,
                              lat: lat + 0.004 * Double(i + 1), lng: lng + 0.006 * Double(i + 1),
                              image: Self.stand_in(i))
            // A FIXED id, so -open=mine: can address one. A tree of yours was
            // the last screen in this app no launch argument could open, which
            // is the definition this file already uses for a screen that ships
            // unlooked at.
            rename(made.id, to: Self.demoIDs[i])
        }
    }

    /// The two ids `-mine-demo` always creates, so `-open=mine:<id>` can open
    /// one from a launch argument.
    static let demoIDs = [
        UUID(uuidString: "00000000-0000-0000-0000-0000000000a1")!,
        UUID(uuidString: "00000000-0000-0000-0000-0000000000a2")!,
    ]

    /// Debug scaffolding only: give a just-recorded sighting a known id.
    private func rename(_ old: UUID, to new: UUID) {
        guard let i = all.firstIndex(where: { $0.id == old }) else { return }
        var row = all[i]
        // The photograph is filed under the old id, so it moves with the row.
        let folderOld = folder.appendingPathComponent(old.uuidString + ".jpg")
        let folderNew = folder.appendingPathComponent(new.uuidString + ".jpg")
        try? FileManager.default.moveItem(at: folderOld, to: folderNew)
        row = Sighting(id: new, treeId: row.treeId, name: row.name, note: row.note,
                       species: row.species, age: row.age, lat: row.lat, lng: row.lng,
                       date: row.date, photo: row.photo == nil ? nil : new.uuidString + ".jpg",
                       status: row.status)
        all[i] = row
        persist()
    }

    /// A stand-in photograph: bands of green over brown, which at pin size
    /// reads as a canopy over a trunk without pretending to be a real tree.
    private static func stand_in(_ i: Int) -> UIImage {
        let size = CGSize(width: 600, height: 800)
        return UIGraphicsImageRenderer(size: size).image { ctx in
            let sky = i == 0 ? UIColor(red: 0.72, green: 0.83, blue: 0.90, alpha: 1)
                             : UIColor(red: 0.86, green: 0.87, blue: 0.80, alpha: 1)
            sky.setFill(); ctx.fill(CGRect(origin: .zero, size: size))
            UIColor(red: 0.29, green: 0.42, blue: 0.20, alpha: 1).setFill()
            ctx.cgContext.fillEllipse(in: CGRect(x: -60, y: 60, width: 720, height: 520))
            UIColor(red: 0.36, green: 0.27, blue: 0.19, alpha: 1).setFill()
            ctx.fill(CGRect(x: 265, y: 460, width: 70, height: 340))
        }
    }

    // MARK: - reading

    /// Newest first, which is how anybody looks at their own photographs.
    var newestFirst: [Sighting] { all.sorted { $0.date > $1.date } }

    /// Only the ones nobody else has: your own finds, the second layer on the
    /// map.
    var yoursOnly: [Sighting] { newestFirst.filter { $0.treeId == nil } }

    func forTree(_ id: String) -> Sighting? { all.first { $0.treeId == id } }

    /// Whether this phone already holds it, asked by the sync before pulling a
    /// row down. The id is the phone's own, so the same sighting on two phones
    /// is one thing rather than two.
    func has(_ id: UUID) -> Bool { all.contains { $0.id == id } }

    /// Take a sighting that came back from the account, with its photograph if
    /// the account had one. Deliberately does NOT push: this is the way in, and
    /// a pull that wrote straight back would be a loop.
    func adopt(_ sighting: Sighting, image: UIImage?) {
        guard !has(sighting.id) else { return }
        var made = sighting
        if let image, let data = Self.downsized(image) {
            let file = made.id.uuidString + ".jpg"
            try? data.write(to: folder.appendingPathComponent(file))
            made.photo = file
        }
        all.append(made)
        persist()
    }

    func image(_ s: Sighting) -> UIImage? {
        guard let f = s.photo else { return nil }
        return UIImage(contentsOfFile: folder.appendingPathComponent(f).path)
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
        Tree(id: s.treeKey,
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
    /// `date` is when the PHOTOGRAPH was taken, not when it was filed. They
    /// were the same thing until 2026-08-28, when a photograph could first
    /// come off the camera roll: one taken last spring belongs in your trees
    /// under last spring, or the log quietly rewrites your own history. It
    /// falls back to now, which is right for the camera path and for a
    /// photograph whose file no longer says.
    @discardableResult
    func record(treeId: String?, name: String, note: String = "",
                lat: Double, lng: Double, image: UIImage?,
                date: Date = Date(), status: Status = .mine) -> Sighting {
        var s = Sighting(treeId: treeId, name: name, note: note,
                         lat: lat, lng: lng, date: date, photo: nil, status: status)
        if let image, let data = Self.downsized(image) {
            let file = s.id.uuidString + ".jpg"
            try? data.write(to: folder.appendingPathComponent(file))
            s.photo = file
        }
        all.append(s)
        persist()
        // TO THE ACCOUNT AS WELL, if there is one. Hidde, 2026-08-27: "niemand
        // wil een backup my trees knop, je wilt gewoon dat dit automatisch goed
        // gaat." Signed out this does nothing and the app behaves as it did.
        Self.syncOne?(s)
        return s
    }

    func setStatus(_ id: UUID, _ status: Status) {
        guard let i = all.firstIndex(where: { $0.id == id }) else { return }
        all[i].status = status
        persist()
        Self.syncOne?(all[i])
    }

    /// The account has this one now, photograph and all.
    ///
    /// Written from the sync, never guessed. It is not persisted through
    /// `Self.syncOne` on purpose: telling the server that we know it has the
    /// row would be a second write for nothing.
    func markSynced(_ id: UUID, at when: Date = Date()) {
        guard let i = all.firstIndex(where: { $0.id == id }) else { return }
        all[i].syncedAt = when
        persist()
    }

    /// EVERYTHING, off this phone, when nobody is signed in.
    ///
    /// Hidde, 2026-08-29: "je kunt niks toevoegen zonder in te loggen dus als
    /// je uitgelogd bent moet je dus ook niks meer zien, geen favoriet, geen
    /// boom, geen foto toegevoegd, niks."
    ///
    /// The first version of this kept anything the account had not confirmed
    /// holding, which was the right shape for one hour: adding a tree without
    /// an account was still possible then, and such a tree existed nowhere
    /// else. Requiring sign-in to add removed the case, and the exception
    /// outlived its reason by about twenty minutes. Worse, it was the reason he
    /// still saw his own trees after installing: nothing on a phone from before
    /// today carries a stamp, so the exception covered the whole collection.
    ///
    /// NOTHING IS DESTROYED. A sighting the account has confirmed goes for
    /// good, photograph and all, because signing in brings it back. One it has
    /// not is moved to `pending.json` and its photograph is left where it is:
    /// off the map, out of the lists, out of every count, and restored by
    /// `restorePending()` on the next sign-in. A picture somebody took under a
    /// tree is not recoverable by signing back in, so it is not deleted on a
    /// maybe.
    func forgetLocally() {
        guard !all.isEmpty else { return }
        let unsent = all.filter { $0.syncedAt == nil }
        for s in all where s.syncedAt != nil {
            if let f = s.photo {
                try? FileManager.default.removeItem(at: folder.appendingPathComponent(f))
            }
        }
        if !unsent.isEmpty {
            // Added to whatever is already parked, so two sign-outs in a row
            // cannot drop the first one's trees.
            let held = readPending() + unsent.filter { u in !readPending().contains { $0.id == u.id } }
            if let d = try? JSONEncoder().encode(held) { try? d.write(to: pending) }
        }
        all = []
        persist()
    }

    /// What was parked at the last sign-out, back on the phone.
    ///
    /// Called on sign-in before the sync runs, so the push that follows carries
    /// these too and the account finally gets the copy it never had.
    func restorePending() {
        let held = readPending()
        guard !held.isEmpty else { return }
        for s in held where !all.contains(where: { $0.id == s.id }) { all.append(s) }
        all.sort { $0.date > $1.date }
        persist()
        try? FileManager.default.removeItem(at: pending)
    }

    private var pending: URL { folder.appendingPathComponent("pending.json") }

    private func readPending() -> [Sighting] {
        guard let d = try? Data(contentsOf: pending),
              let rows = try? JSONDecoder().decode([Sighting].self, from: d) else { return [] }
        return rows
    }

    func remove(_ id: UUID) {
        guard let i = all.firstIndex(where: { $0.id == id }) else { return }
        if let f = all[i].photo {
            try? FileManager.default.removeItem(at: folder.appendingPathComponent(f))
        }
        let gone = all[i].id
        all.remove(at: i)
        persist()
        Self.syncGone?(gone)
    }

    // MARK: - the pieces

    /// 1600 points on the long edge at 0.8 quality: about 300 KB, which is a
    /// photograph worth keeping and a file worth uploading on the day that
    /// question is opened. A phone camera's original is ten times that and
    /// nothing on this screen is better for it.
    nonisolated static func downsized(_ image: UIImage, max: CGFloat = 1600) -> Data? {
        let side = Swift.max(image.size.width, image.size.height)
        guard side > max else { return image.jpegData(compressionQuality: 0.8) }
        let scale = max / side
        let size = CGSize(width: image.size.width * scale, height: image.size.height * scale)
        // SCALE 1, and without this line the whole function was decoration.
        //
        // UIGraphicsImageRenderer draws at the SCREEN's scale unless told
        // otherwise, which is 3 on every modern iPhone. So asking it for 1600
        // points produced a 4800 pixel image and a file of several megabytes,
        // nine times the pixels this function exists to avoid and nine times
        // what the comment above claims. Nobody noticed because the picture
        // looked right; it was the bytes that were wrong. Found by the first
        // test ever written for it (2026-08-27), and it matters more now than
        // it did last week, because these photographs go to the account.
        let format = UIGraphicsImageRendererFormat.default()
        format.scale = 1
        let r = UIGraphicsImageRenderer(size: size, format: format)
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
        // KEEP THE BYTES, THEN CARRY ON. The first version of this refused to
        // write for the rest of the session whenever salvage came back empty,
        // which protects the file and leaves somebody with an app that cannot
        // record a tree ever again. Copying the original aside protects it just
        // as well and costs nothing, so writing is only refused in the one case
        // where the copy itself failed and the original is still the only copy
        // there is.
        // ASK WHETHER THESE BYTES ARE KEPT, not whether the name is taken.
        //
        // This used to be fileExists(), which answers yes to a directory, to an
        // empty file, and above all to a copy of a DIFFERENT earlier breakage.
        // A file that broke twice in two different ways then kept the first set
        // of bytes and quietly wrote over the second, which is the one case
        // where somebody has already lost trees once and is about to lose the
        // rest (found by the first test written for this, 2026-08-27).
        //
        // Three steps, in this order, and the order is the whole thing:
        //   1. these exact bytes are already saved, so there is nothing to do
        //   2. the name is free, so use it
        //   3. the name is taken by something else, so take a name of our own
        //      rather than write over somebody's only copy
        let fm = FileManager.default
        let copy = folder.appendingPathComponent("index-unreadable.json")
        var kept = (try? Data(contentsOf: copy)) == d
        if !kept, !fm.fileExists(atPath: copy.path) {
            kept = (try? d.write(to: copy)) != nil
        }
        if !kept {
            var n = 2
            while n < 50 {
                let alt = folder.appendingPathComponent("index-unreadable-\(n).json")
                if let existing = try? Data(contentsOf: alt) {
                    if existing == d { kept = true; break }       // already have these
                    n += 1
                    continue
                }
                if fm.fileExists(atPath: alt.path) { n += 1; continue }
                kept = (try? d.write(to: alt)) != nil
                break
            }
        }
        all = Self.salvage(d)
        unreadable = all.isEmpty && !kept
        findOrphans()
        // Only rewrite the index once something was actually recovered, and
        // the copy above survives either way.
        if !all.isEmpty { persist() }
    }

    /// Read the file as plain JSON and build what each row allows, filling in
    /// anything missing rather than throwing the row away. A sighting without a
    /// name or a position cannot be placed on a map and is the only kind
    /// dropped here.
    nonisolated private static func salvage(_ data: Data) -> [Sighting] {
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
        let files = (try? FileManager.default.contentsOfDirectory(atPath: folder.path)) ?? []
        orphanPhotos = files.filter { $0.hasSuffix(".jpg") && !known.contains($0) }.sorted()
    }

}
