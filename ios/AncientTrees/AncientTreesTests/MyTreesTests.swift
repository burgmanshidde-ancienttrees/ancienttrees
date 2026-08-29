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
import AVFoundation
import CoreLocation
import ImageIO
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

// MARK: - permission refused

/// What the app does when somebody says no.
///
/// A simulator has no camera, so the camera branch could never run there and
/// the black-rectangle bug was invisible to every test and every screenshot
/// this project has ever taken. The decision is a pure function now, which can
/// be asked all four questions on a machine with nothing to deny.
@Suite(.serialized)
struct WhenPermissionIsRefused {

    @Test func aDeniedCameraOpensTheLibraryRatherThanABlackRectangle() {
        #expect(CameraPicker.source(cameraAvailable: true, authorization: .denied)
                == .photoLibrary,
                "a denied camera still presented the camera, which is a black screen with a Cancel button")
        #expect(CameraPicker.source(cameraAvailable: true, authorization: .restricted)
                == .photoLibrary,
                "a restricted camera still presented the camera")
    }

    @Test func anAllowedCameraIsStillTheCamera() {
        #expect(CameraPicker.source(cameraAvailable: true, authorization: .authorized) == .camera)
    }

    /// Never asked is not the same as refused. Presenting the camera is what
    /// raises the system prompt, and the moment somebody has just tapped a
    /// button saying photograph a tree is the right moment to raise it.
    @Test func neverHavingBeenAskedStillAsks() {
        #expect(CameraPicker.source(cameraAvailable: true, authorization: .notDetermined) == .camera)
    }

    /// Every simulator, and any iPad without a rear camera.
    @Test func noCameraAtAllIsTheLibraryWhateverTheAnswerWas() {
        for answer in [AVAuthorizationStatus.authorized, .denied, .notDetermined, .restricted] {
            #expect(CameraPicker.source(cameraAvailable: false, authorization: answer)
                    == .photoLibrary)
        }
    }
}

// MARK: - A photograph you already had

/// Collecting from the camera roll, added 2026-08-28 (Hidde: "wat als ik een
/// mooie foto op mn fotorol heb staan").
///
/// None of this can be tested through the picker itself, because a simulator
/// has no photo library worth the name and PHPickerViewController cannot be
/// driven by a UI test. So the two questions that actually decide where a tree
/// lands are pure functions, on the same principle the camera source decision
/// was pulled out for: when the situation cannot be reproduced on the machine
/// that tests it, make the DECISION testable instead of the situation.
/// SIGNING OUT, which is the state this app spent its first weeks never being in.
///
/// Hidde, 2026-08-29: "als je uitlogt moeten de bomen die je hebt toegevoegd
/// niet meer zichtbaar zijn op de kaart en in de lijsten", and "ik kan ook een
/// boom removen terwijl ik uitgelogd ben dat lijkt me niet de bedoeling".
///
/// The rule has two halves and only testing the first is how the bug it fixes
/// gets replaced by a worse one: everything the account holds goes, and
/// everything the account has never seen stays. A file somebody photographed
/// under a tree while signed out is the only copy of it in the world.
@Suite struct SigningOutForgetsTheCollection {

    /// The whole rule in one line (Hidde, 2026-08-29): "als je uitgelogd bent
    /// moet je dus ook niks meer zien, geen favoriet, geen boom, geen foto
    /// toegevoegd, niks."
    @Test func nothingSurvivesOnScreen() {
        let p = Patch(); defer { p.clean() }
        let s = Sightings(folder: p.url)
        let synced = s.record(treeId: nil, name: "At the account", lat: 52.1, lng: 4.1, image: pixel())
        s.markSynced(synced.id)
        _ = s.record(treeId: nil, name: "Never sent", lat: 52.2, lng: 4.2, image: pixel())

        s.forgetLocally()

        #expect(s.all.isEmpty, "a tree stayed visible on a signed-out phone")
        #expect(s.yoursOnly.isEmpty, "it stayed in the lists the map and Collect read")
        #expect(Sightings(folder: p.url).all.isEmpty, "it came back on the next launch")
    }

    /// A tree the account holds goes for good, because signing in brings it
    /// back from there.
    @Test func aSyncedTreeTakesItsPhotographWithIt() {
        let p = Patch(); defer { p.clean() }
        let s = Sightings(folder: p.url)
        let made = s.record(treeId: nil, name: "The oak on my street",
                            lat: 52.37, lng: 4.89, image: pixel())
        let file = made.photo ?? ""
        s.markSynced(made.id)

        s.forgetLocally()

        #expect(!p.files().contains(file), "its photograph stayed behind")
        s.restorePending()
        #expect(s.all.isEmpty, "a synced tree was parked as if nobody had it")
    }

    /// One the account has never seen is parked, not destroyed, and comes back
    /// on the next sign-in with its picture. A photograph somebody took under a
    /// tree is not recoverable by signing in, so it is never deleted on a maybe.
    @Test func anUnsentTreeIsParkedAndComesBack() {
        let p = Patch(); defer { p.clean() }
        let s = Sightings(folder: p.url)
        let made = s.record(treeId: nil, name: "Photographed with no signal",
                            lat: 52.37, lng: 4.89, image: pixel())
        let file = made.photo ?? ""

        s.forgetLocally()
        #expect(s.all.isEmpty, "it was still on screen while signed out")
        #expect(p.files().contains(file), "its photograph was deleted on a maybe")

        s.restorePending()
        #expect(s.all.map(\.id) == [made.id], "it did not come back on sign-in")
        #expect(s.image(s.all[0]) != nil, "it came back without its photograph")
    }

    /// Two sign-outs in a row must not drop the first one's trees.
    @Test func parkingTwiceKeepsBoth() {
        let p = Patch(); defer { p.clean() }
        let s = Sightings(folder: p.url)
        let first = s.record(treeId: nil, name: "One", lat: 52.1, lng: 4.1, image: nil)
        s.forgetLocally()

        let second = s.record(treeId: nil, name: "Two", lat: 52.2, lng: 4.2, image: nil)
        s.forgetLocally()

        s.restorePending()
        #expect(Set(s.all.map(\.id)) == Set([first.id, second.id]))
    }

    /// A file written before syncedAt existed still decodes, and clears, which
    /// is the case that made him see his own trees after installing.
    @Test func anOlderFileClearsToo() {
        let p = Patch(); defer { p.clean() }
        p.write("""
        [{"id":"00000000-0000-0000-0000-0000000000b1","name":"From an older build",
          "note":"","lat":52.37,"lng":4.89,
          "date":770000000,"status":"mine"}]
        """)

        let s = Sightings(folder: p.url)
        #expect(s.all.count == 1, "an older file stopped decoding")
        #expect(s.all[0].syncedAt == nil)

        s.forgetLocally()
        #expect(s.all.isEmpty, "a tree from before today stayed on a signed-out phone")
        s.restorePending()
        #expect(s.all.count == 1, "and it was not kept anywhere")
    }
}

@Suite struct CameraRollTests {

    @Test func theLibrarysOwnRecordBeatsTheFilesMetadata() {
        let asset = CLLocation(latitude: 52.3731, longitude: 4.8922)
        let exif = CLLocationCoordinate2D(latitude: 41.9028, longitude: 12.4964)

        let got = LibraryPicker.coordinate(assetLocation: asset, exif: exif)

        #expect(got?.latitude == 52.3731,
                "the file's own block won over the library's record")
    }

    /// The case that matters when somebody has refused us the library: the
    /// asset cannot be read, and the file sometimes still says.
    @Test func exifAnswersWhenTheAssetCannot() {
        let exif = CLLocationCoordinate2D(latitude: 41.9028, longitude: 12.4964)
        let got = LibraryPicker.coordinate(assetLocation: nil, exif: exif)
        #expect(got?.latitude == 41.9028)
    }

    /// And neither knowing is ordinary rather than an error. A screenshot, a
    /// download, anything through a messenger.
    @Test func nothingKnowsWhereItWasTaken() {
        #expect(LibraryPicker.coordinate(assetLocation: nil, exif: nil) == nil)
    }

    @Test func gpsBlockIsReadWithItsHemispheres() {
        let south: [CFString: Any] = [
            kCGImagePropertyGPSDictionary: [
                kCGImagePropertyGPSLatitude: 33.9249,
                kCGImagePropertyGPSLatitudeRef: "S",
                kCGImagePropertyGPSLongitude: 18.4241,
                kCGImagePropertyGPSLongitudeRef: "E",
            ] as [CFString: Any]
        ]
        let got = LibraryPicker.exifCoordinate(in: south)
        #expect(got?.latitude == -33.9249, "a southern latitude came back positive")
        #expect(got?.longitude == 18.4241)
    }

    /// Null Island. A cleared GPS block reads as 0,0, which is a real
    /// coordinate in the Atlantic and would put somebody's tree in the sea.
    @Test func aClearedGpsBlockIsNotACoordinate() {
        let zeroed: [CFString: Any] = [
            kCGImagePropertyGPSDictionary: [
                kCGImagePropertyGPSLatitude: 0.0,
                kCGImagePropertyGPSLongitude: 0.0,
            ] as [CFString: Any]
        ]
        #expect(LibraryPicker.exifCoordinate(in: zeroed) == nil)
    }

    @Test func noGpsBlockAtAll() {
        #expect(LibraryPicker.exifCoordinate(in: [:]) == nil)
    }

    /// The log keeps the day the photograph was taken, not the day it was
    /// filed. Without this a photograph from last spring quietly rewrites your
    /// own history to today.
    @Test func theSightingKeepsThePhotographsOwnDate() {
        let p = Patch(); defer { p.clean() }
        let s = Sightings(folder: p.url)
        let lastSpring = Date(timeIntervalSince1970: 1_713_000_000)

        let made = s.record(treeId: nil, name: "The oak I photographed in April",
                            lat: 52.37, lng: 4.89, image: nil, date: lastSpring)

        #expect(made.date == lastSpring)
        #expect(Sightings(folder: p.url).all.first?.date == lastSpring,
                "the date did not survive a relaunch")
    }

    /// The bug Hidde found within an hour of this shipping: he picked a photo
    /// of something standing NEAR one of our trees and was told he had found
    /// that tree. A coordinate off a photograph says where the photographer
    /// stood, and nothing says the subject is a tree at all.
    @Test func onlyStandingThereClaimsATreeWithoutAsking() {
        #expect(CollectSheet.mayClaimWithoutAsking(.device),
                "the camera path should still tick off a confident match")
        #expect(!CollectSheet.mayClaimWithoutAsking(.photo),
                "a photograph off the roll claimed a tree nobody confirmed")
        #expect(!CollectSheet.mayClaimWithoutAsking(.placed),
                "a hand-placed pin claimed a tree nobody confirmed")
    }

    /// The camera path is unchanged and still files under now.
    @Test func withoutADateItIsFiledUnderNow() {
        let p = Patch(); defer { p.clean() }
        let s = Sightings(folder: p.url)
        let made = s.record(treeId: nil, name: "Standing here", lat: 52.37, lng: 4.89, image: nil)
        #expect(abs(made.date.timeIntervalSinceNow) < 5)
    }
}

/// The map's own grid, which decides which trees pile into one bubble.
@Suite struct ClusterGridTests {

    /// The old key was `column * 100_000 + row`, and the row index passes
    /// 100,000 at zoom 13.5. Two cells far apart then shared a key and their
    /// trees were drawn as one bubble at the mean of both, which is a pile of
    /// trees standing where none of them are.
    @Test func cellsFarApartDoNotShareAKeyAtHighZoom() {
        // zoom 14: the world is 512 * 2^14 points across, cells are 60 wide,
        // so indices run to roughly 139,000.
        let cell = 60.0 / (512.0 * pow(2.0, 14.0))

        let a = MapLayers.cellKey(x: 1 * cell, y: 100_000 * cell, cell: cell)
        let b = MapLayers.cellKey(x: 2 * cell, y: 0, cell: cell)

        #expect(a != b, "two cells a long way apart landed in the same bubble")
    }

    @Test func theSameCellAlwaysGivesTheSameKey() {
        let cell = 60.0 / (512.0 * pow(2.0, 9.0))
        // Two points inside one cell, neither on a boundary.
        let a = MapLayers.cellKey(x: 10 * cell + cell / 4, y: 20 * cell + cell / 4, cell: cell)
        let b = MapLayers.cellKey(x: 10 * cell + cell / 2, y: 20 * cell + cell / 2, cell: cell)
        #expect(a == b)
    }

    @Test func neighbouringCellsDiffer() {
        let cell = 60.0 / (512.0 * pow(2.0, 9.0))
        let here = MapLayers.cellKey(x: 10 * cell, y: 20 * cell, cell: cell)
        #expect(here != MapLayers.cellKey(x: 11 * cell, y: 20 * cell, cell: cell))
        #expect(here != MapLayers.cellKey(x: 10 * cell, y: 21 * cell, cell: cell))
    }

    /// A tree you added yourself is one of the numbers (Hidde, 2026-08-29:
    /// "zelfgemaakte bomen moeten gewoon mee clusteren met de getallen als je
    /// uitzoomt"). It used to sit in a source of its own, and a grid can only
    /// group what it is handed, so a city collapsing to one bubble left your
    /// own pin hanging beside it at full size.
    ///
    /// The point of testing the grouping rather than the map: this is the whole
    /// decision, and it can be asked without a simulator, a style or a pixel.
    @Test func yourOwnTreeJoinsThePileBesideIt() {
        // Zoom 6, a continent on the screen: everything in Amsterdam is one
        // pile at this range.
        let cell = 60.0 / (512.0 * pow(2.0, 6.0))
        let ours = [CLLocationCoordinate2D(latitude: 52.3731, longitude: 4.8922),
                    CLLocationCoordinate2D(latitude: 52.3600, longitude: 4.9100)]
        let yours = CLLocationCoordinate2D(latitude: 52.3700, longitude: 4.8800)

        let grouped = MapLayers.groups(of: ours + [yours], cell: cell)

        #expect(grouped.count == 1, "three trees in one city drew more than one bubble")
        #expect(grouped[0].count == 3, "the pile did not count the tree you added")
    }

    /// And it comes back out on its own when the map is close enough, or a
    /// photograph you took would be locked inside a bubble forever.
    @Test func yourOwnTreeStandsAloneWhenTheMapIsClose() {
        let cell = 60.0 / (512.0 * pow(2.0, 15.0))
        let ours = CLLocationCoordinate2D(latitude: 52.3731, longitude: 4.8922)
        let yours = CLLocationCoordinate2D(latitude: 52.3700, longitude: 4.8800)

        let grouped = MapLayers.groups(of: [ours, yours], cell: cell)

        #expect(grouped.count == 2)
        #expect(grouped.allSatisfy { $0.count == 1 })
    }
}
