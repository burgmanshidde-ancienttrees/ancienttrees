// Your own trees, which is the only thing in this app that exists nowhere else.
//
// A tree of OURS that goes wrong is an edit: the story is in the repository,
// the pin is in a register, the photograph is on Commons. A tree of YOURS is a
// photograph you took while standing somewhere, and if this file loses it, it
// is gone. Hidde lost his own in Baarn on 2026-08-27 and the code made a
// recoverable problem unrecoverable: the loader swallowed every error and
// returned an empty list, and the next write put that emptiness over the only
// copy there is.
//
// The salvage path built that day is the most important code in the app and it
// had no tests at all, which is a strange sentence to be able to write. These
// are they. Most of them are about a file that is WRONG in some way, because
// that is the whole point: the ordinary path was never what took anybody's
// trees.
//
// Every test gets its own throwaway directory. Tests about losing trees that
// share a folder would read each other's collection, or the simulator's.

import Testing
import Foundation
import UIKit
@testable import AncientTrees

/// One test's own sightings folder, removed after it.
private struct Patch {
    let url: URL
    init() {
        url = FileManager.default.temporaryDirectory
            .appendingPathComponent("sightings-test-" + UUID().uuidString)
        try? FileManager.default.createDirectory(at: url, withIntermediateDirectories: true)
    }
    func clean() { try? FileManager.default.removeItem(at: url) }
    var index: URL { url.appendingPathComponent("index.json") }
    var rescued: URL { url.appendingPathComponent("index-unreadable.json") }
    func write(_ text: String) { try? Data(text.utf8).write(to: index) }
    func files() -> [String] {
        ((try? FileManager.default.contentsOfDirectory(atPath: url.path)) ?? []).sorted()
    }
}

/// A real one-pixel image, because record() only writes a file when it can
/// actually encode one.
private func pixel() -> UIImage {
    UIGraphicsImageRenderer(size: CGSize(width: 8, height: 8)).image { c in
        UIColor.green.setFill()
        c.fill(CGRect(x: 0, y: 0, width: 8, height: 8))
    }
}

@Suite(.serialized)
struct WhenTheIndexIsBroken {

    /// The failure that took Hidde's trees, as a test. The promise is not that
    /// index.json is frozen, it is that the ORIGINAL BYTES survive somewhere,
    /// so a later version can still read what this one could not.
    @Test func theOriginalSurvivesEvenAfterTheAppCarriesOnWriting() {
        let p = Patch(); defer { p.clean() }
        p.write("this is not JSON at all")

        let s = Sightings(folder: p.url)
        #expect(s.all.isEmpty)

        // Anything that would normally persist.
        s.record(treeId: nil, name: "A new one", lat: 52.37, lng: 4.89, image: nil)

        let kept = try? String(contentsOf: p.rescued, encoding: .utf8)
        #expect(kept == "this is not JSON at all",
                "the only copy of somebody's trees is gone")
    }

    /// Breaking twice, in two different ways, is the case where somebody has
    /// already lost trees once and is about to lose the rest. Both sets of
    /// bytes have to survive; keeping only the first is the same as keeping
    /// neither, for the person whose second collection went.
    @Test func aSecondBreakageDoesNotWriteOverTheFirstOnesBytes() {
        let p = Patch(); defer { p.clean() }

        p.write("first breakage")
        _ = Sightings(folder: p.url)

        p.write("second breakage, different bytes")
        _ = Sightings(folder: p.url)

        let saved = p.files()
            .filter { $0.hasPrefix("index-unreadable") }
            .compactMap { try? String(contentsOf: p.url.appendingPathComponent($0),
                                      encoding: .utf8) }
        #expect(saved.contains("first breakage"), "the first breakage's bytes are gone")
        #expect(saved.contains("second breakage, different bytes"),
                "the second breakage was written over the first, so those trees are gone")
    }

    /// And the last ditch: when the bytes cannot be kept ANYWHERE, nothing is
    /// written at all, because index.json is once again the only copy there is.
    /// A read-only folder is what that looks like.
    @Test func whenTheBytesCannotBeKeptNothingIsWritten() {
        let p = Patch()
        p.write("this is not JSON at all")
        try? FileManager.default.setAttributes([.posixPermissions: 0o500],
                                               ofItemAtPath: p.url.path)
        defer {
            try? FileManager.default.setAttributes([.posixPermissions: 0o700],
                                                   ofItemAtPath: p.url.path)
            p.clean()
        }

        let s = Sightings(folder: p.url)
        #expect(s.unreadable,
                "the bytes could not be kept anywhere and the app carried on writing anyway")
    }

    /// ONE bad row must not take the other forty with it. Decoding the array in
    /// one go is exactly what does that, which is why salvage reads row by row.
    @Test func oneRowALaterVersionWroteDifferentlyDoesNotTakeTheRest() {
        let p = Patch(); defer { p.clean() }
        // The middle row carries a field this version has never heard of and a
        // status that does not exist, which is what a downgrade looks like.
        p.write("""
        [{"id":"\(UUID().uuidString)","name":"The oak","lat":52.37,"lng":4.89,"date":770000000},
         {"id":"\(UUID().uuidString)","name":"The lime","lat":52.38,"lng":4.90,"date":770000001,
          "mood":"golden","status":"invented"},
         {"id":"\(UUID().uuidString)","name":"The plane","lat":52.39,"lng":4.91,"date":770000002}]
        """)

        let s = Sightings(folder: p.url)
        #expect(s.all.count == 3, "salvage kept \(s.all.count) of 3 trees")
        #expect(s.all.map(\.name).sorted() == ["The lime", "The oak", "The plane"])
        #expect(s.all.first { $0.name == "The lime" }?.status == .mine,
                "an unknown status should fall back, not drop the row")
        #expect(!s.unreadable, "salvage recovered rows, so writing must be allowed again")
    }

    /// A row with no position cannot be put on a map and is the only kind
    /// dropped. A row with no name gets one rather than being thrown away.
    @Test func onlyARowWithNoPositionIsDropped() {
        let p = Patch(); defer { p.clean() }
        p.write("""
        [{"name":"No position","date":770000000},
         {"id":"\(UUID().uuidString)","lat":52.38,"lng":4.90,"date":770000001}]
        """)

        let s = Sightings(folder: p.url)
        #expect(s.all.count == 1, "the wrong number of rows survived")
        #expect(s.all.first?.name.isEmpty == false, "a nameless row came back with no name at all")
    }

    /// JSONEncoder has written dates two ways over this app's life. A salvage
    /// that understood one of them would date half a collection to 2001.
    @Test func bothWaysOfWritingADateSurvive() {
        let p = Patch(); defer { p.clean() }
        p.write("""
        [{"id":"\(UUID().uuidString)","name":"Seconds","lat":52.37,"lng":4.89,"date":770000000},
         {"id":"\(UUID().uuidString)","name":"Text","lat":52.38,"lng":4.90,
          "date":"2024-05-01T10:00:00Z"}]
        """)

        let s = Sightings(folder: p.url)
        let year = Calendar(identifier: .gregorian)
        for one in s.all {
            let y = year.component(.year, from: one.date)
            #expect(y > 2020, "\(one.name) came back dated \(y)")
        }
    }

    /// A photograph whose row is missing is the least replaceable thing here.
    /// It is counted and kept, never quietly deleted.
    @Test func aPhotographWhoseRowIsGoneIsKeptAndCounted() {
        let p = Patch(); defer { p.clean() }
        try? Data("not really a jpeg".utf8)
            .write(to: p.url.appendingPathComponent("orphan.jpg"))
        p.write("[]")

        let s = Sightings(folder: p.url)
        #expect(s.orphanPhotos == ["orphan.jpg"], "an orphaned photograph was not noticed")
        #expect(p.files().contains("orphan.jpg"), "an orphaned photograph was deleted")
    }

    /// No file at all is an ordinary first launch, not a fault, and must not
    /// put the app into the never-write-again state.
    @Test func aFirstLaunchIsNotAFault() {
        let p = Patch(); defer { p.clean() }
        let s = Sightings(folder: p.url)
        #expect(s.all.isEmpty)
        #expect(!s.unreadable, "an empty folder was treated as a broken file")

        s.record(treeId: nil, name: "The first one", lat: 52.37, lng: 4.89, image: nil)
        #expect(Sightings(folder: p.url).all.count == 1, "the first tree did not survive a relaunch")
    }
}

@Suite(.serialized)
struct RecordingATreeOfYourOwn {

    @Test func aPhotographIsWrittenAndComesBack() {
        let p = Patch(); defer { p.clean() }
        let s = Sightings(folder: p.url)

        let made = s.record(treeId: nil, name: "The oak on my street",
                            lat: 52.37, lng: 4.89, image: pixel())

        #expect(made.photo != nil, "no photograph file was written")
        #expect(p.files().contains(made.photo ?? ""), "the file named by the row is not there")
        #expect(s.image(made) != nil, "the photograph could not be read back")
    }

    /// The row and the file go together. An index that keeps pointing at a
    /// deleted picture is how a page ends up with a grey box forever.
    @Test func removingATreeTakesItsPhotographWithIt() {
        let p = Patch(); defer { p.clean() }
        let s = Sightings(folder: p.url)
        let made = s.record(treeId: nil, name: "The lime", lat: 52.37, lng: 4.89, image: pixel())
        let file = made.photo ?? ""

        s.remove(made.id)

        #expect(s.all.isEmpty)
        #expect(!p.files().contains(file), "the photograph outlived the row that named it")
        #expect(Sightings(folder: p.url).all.isEmpty, "it came back after a relaunch")
    }

    /// Filling in a field the app did not know, which is the whole point of a
    /// tree of yours. An empty string clears rather than storing emptiness.
    @Test func fieldsCanBeFilledInAndCleared() {
        let p = Patch(); defer { p.clean() }
        let s = Sightings(folder: p.url)
        let made = s.record(treeId: nil, name: "Unknown", lat: 52.37, lng: 4.89, image: nil)

        s.update(made.id, name: "The plane by the bridge", species: "Platanus", age: "150 years")
        var now = s.all.first
        #expect(now?.name == "The plane by the bridge")
        #expect(now?.species == "Platanus")

        s.update(made.id, species: "")
        now = s.all.first
        #expect(now?.species == nil, "an empty species was stored rather than cleared")
        #expect(now?.age == "150 years", "clearing one field cleared another")
        #expect(now?.name == "The plane by the bridge", "an omitted name overwrote the real one")
    }

    /// The account is told, and only about deliberate changes. A pull that
    /// echoed straight back would be a loop.
    @Test func theAccountHearsAboutAChangeButNotAboutAPull() {
        let p = Patch(); defer { p.clean() }
        var pushed: [String] = []
        var deleted = 0
        Sightings.syncOne = { pushed.append($0.name) }
        Sightings.syncGone = { _ in deleted += 1 }
        defer { Sightings.syncOne = nil; Sightings.syncGone = nil }

        let s = Sightings(folder: p.url)
        let made = s.record(treeId: nil, name: "Pushed", lat: 52.37, lng: 4.89, image: nil)
        s.adopt(Sightings.Sighting(name: "From the account", lat: 52.4, lng: 4.9), image: nil)
        s.remove(made.id)

        #expect(pushed == ["Pushed"], "a row pulled from the account was echoed back: \(pushed)")
        #expect(deleted == 1)
    }

    /// Twice is once. A second merge must not double the collection.
    @Test func adoptingTheSameTreeTwiceKeepsOneOfIt() {
        let p = Patch(); defer { p.clean() }
        let s = Sightings(folder: p.url)
        let one = Sightings.Sighting(name: "The yew", lat: 52.37, lng: 4.89)

        s.adopt(one, image: pixel())
        s.adopt(one, image: pixel())

        #expect(s.all.count == 1, "a second sync duplicated the collection")
    }

    /// Your tree wears the same page ours do, and the one field it is never
    /// vague about is where it is: you were standing there.
    @Test func yourTreeBecomesATreePageWithAConfirmedPin() {
        let p = Patch(); defer { p.clean() }
        let s = Sightings(folder: p.url)
        let made = s.record(treeId: nil, name: "The oak", note: "Enormous.",
                            lat: 52.37, lng: 4.89, image: nil)

        let tree = s.asTree(made)
        #expect(tree.id == "mine:" + made.id.uuidString)
        #expect(tree.name == "The oak")
        #expect(tree.story == "Enormous.")
        #expect(tree.precision == .confirmed, "a tree you stood in front of got a vague pin")
        #expect(tree.paidEntry == false)
    }

    /// A phone camera's original is several megabytes. Keeping that per tree is
    /// how a collection becomes a storage problem.
    @Test func aPhotographIsShrunkBeforeItIsKept() throws {
        // Scale 1, the way a camera hands one over: size in pixels, not points.
        let format = UIGraphicsImageRendererFormat.default()
        format.scale = 1
        let big = UIGraphicsImageRenderer(size: CGSize(width: 4000, height: 3000),
                                          format: format).image { c in
            UIColor.systemGreen.setFill()
            c.fill(CGRect(x: 0, y: 0, width: 4000, height: 3000))
        }

        let data = try #require(Sightings.downsized(big))
        let out = try #require(UIImage(data: data))
        #expect(max(out.size.width, out.size.height) <= 1600,
                "a full sized photograph was kept at \(out.size)")
        // The bytes are the point rather than the dimensions. Before the
        // renderer was pinned to scale 1 this came back at 4800 pixels and
        // several megabytes, on a phone, per tree.
        #expect(data.count < 900_000,
                "a photograph of \(data.count / 1024) KB was kept per tree")
    }
}
