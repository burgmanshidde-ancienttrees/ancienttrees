// Your own trees, kept where a lost phone cannot take them.
//
// Hidde, 2026-08-27, after losing his own trees and photographs in Baarn and
// then seeing the backup button built for it: "maar niemand wil een backup my
// trees knop, je wilt gewoon dat dit automatisch goed gaat." A button is a
// thing somebody has to remember on the one day they will not.
//
// The shape is CloudSync's, deliberately, because that one already works and
// the arguments behind it were had once: the merge is a UNION and only on the
// way in, deletes are only ever sent for something the person just deleted and
// never inferred from what is missing on one side, and a failed write is
// swallowed rather than shown, because the local copy is already right and the
// person is standing under a tree.
//
// THE PHOTOGRAPH TRAVELS TOO, and that is the part that changes an old rule
// rather than adding to it. Sightings.swift held that photographs stay on the
// phone, which was right while a sighting was a note to yourself and stopped
// being right the moment one wipe took everything. The bucket is PRIVATE and
// there is no policy anywhere that lets one account read another's, so this
// adds no moderation surface: nobody but you ever sees these.
//
// Signed out, nothing here runs and the app behaves exactly as it did.

import Foundation
import UIKit

@MainActor
enum SightingSync {

    /// Pull what the account holds, fold it into this phone, push the union
    /// back. Called once when a session appears, next to CloudSync.merge.
    static func merge(account: Account, sightings: Sightings) async {
        guard let s = await account.freshSession() else { return }

        let remote = await Supa.rows("/rest/v1/sightings?select=*", token: s.accessToken)
        for row in remote {
            guard let idText = row["id"] as? String, let id = UUID(uuidString: idText),
                  let lat = row["lat"] as? Double, let lng = row["lng"] as? Double
            else { continue }
            if sightings.has(id) { continue }

            var made = Sightings.Sighting(id: id,
                                          treeId: row["tree_id"] as? String,
                                          name: (row["name"] as? String) ?? "A tree you photographed",
                                          note: (row["note"] as? String) ?? "",
                                          species: row["species"] as? String,
                                          age: row["age"] as? String,
                                          lat: lat, lng: lng)
            if let t = row["taken_at"] as? String,
               let d = ISO8601DateFormatter().date(from: t) { made.date = d }
            // It came FROM the account, so the account has it. Without this the
            // first sign-out after a fresh sign-in would keep every pulled
            // tree on the phone, waiting for a push to tell us what we already
            // know.
            made.syncedAt = Date()
            if let st = row["status"] as? String,
               let k = Sightings.Status(rawValue: st) { made.status = k }

            // The picture comes back too, or the row arrives without one and
            // the page says so, which is the same honest gap as a tree of ours
            // that nobody has photographed.
            if let file = row["photo"] as? String,
               let data = await download(file, token: s.accessToken),
               let image = UIImage(data: data) {
                sightings.adopt(made, image: image)
            } else {
                sightings.adopt(made, image: nil)
            }
        }

        await pushAll(account: account, sightings: sightings)
    }

    /// Everything this phone holds, upserted. The one call that makes a
    /// collection made before signing in survive the first sign-in.
    static func pushAll(account: Account, sightings: Sightings) async {
        guard let s = await account.freshSession() else { return }
        await pushAll(session: s, sightings: sightings)
    }

    /// The same, with the session already in hand.
    ///
    /// Signing out needs this. It used to await the account-taking version above
    /// and only then close the door, which meant the button did nothing visible
    /// while every photograph on the phone went up one at a time, and Hidde
    /// pressed it twice (2026-08-30: "sign out lijkt soms wel een lag te hebben
    /// ik druk soms 2 keer voor die t doet"). Taking the session as a value lets
    /// the sign-out clear its state first and let the upload finish behind it:
    /// a token stays valid for its own lifetime whether or not we still hold a
    /// copy in the Keychain.
    static func pushAll(session s: Session, sightings: Sightings) async {
        for sighting in sightings.all {
            await push(session: s, sightings: sightings, sighting: sighting)
        }
    }

    /// One sighting changed. Fire and forget.
    static func push(account: Account, sightings: Sightings,
                            sighting: Sightings.Sighting) async {
        guard let s = await account.freshSession() else { return }
        await push(session: s, sightings: sightings, sighting: sighting)
    }

    static func push(session s: Session, sightings: Sightings,
                     sighting: Sightings.Sighting) async {

        // The photograph first, so a row never points at a file that is not
        // there yet. Uploaded once: the name is the sighting's own id, and a
        // second upload of the same id simply replaces it.
        var stored: String? = nil
        if let image = sightings.image(sighting),
           let data = Sightings.downsized(image) {
            let path = "\(s.userId)/\(sighting.id.uuidString).jpg"
            if await upload(path, data: data, token: s.accessToken) { stored = path }
        }

        var row: [String: Any] = [
            "user_id": s.userId,
            "id": sighting.id.uuidString,
            "name": sighting.name,
            "note": sighting.note,
            "lat": sighting.lat,
            "lng": sighting.lng,
            "taken_at": ISO8601DateFormatter().string(from: sighting.date),
            "status": sighting.status.rawValue,
            "updated_at": ISO8601DateFormatter().string(from: Date()),
        ]
        row["tree_id"] = sighting.treeId
        row["species"] = sighting.species
        row["age"] = sighting.age
        row["photo"] = stored
        let landed = await Supa.post("/rest/v1/sightings?on_conflict=user_id,id",
                                token: s.accessToken, body: [row])
        // ONLY when the photograph went too, where there is one. A row without
        // its picture is not a copy of this sighting, and treating it as one
        // is how somebody signs out and loses the photograph while keeping the
        // pin.
        if landed, stored != nil || sightings.image(sighting) == nil {
            await MainActor.run { sightings.markSynced(sighting.id) }
        }
    }

    /// One sighting deleted here, deleted there. The file goes first for the
    /// same reason it is uploaded first: never leave a row pointing at nothing,
    /// and never leave a file nothing points at.
    static func remove(account: Account, id: UUID) async {
        guard let s = await account.freshSession() else { return }
        await deleteObject("\(s.userId)/\(id.uuidString).jpg", token: s.accessToken)
        await Supa.delete("/rest/v1/sightings?id=eq.\(id.uuidString)", token: s.accessToken)
    }

    // MARK: - plumbing

    private static let bucket = "sightings"

    // rows / post / delete live on Supa now. post still answers whether the row
    // LANDED, which is what forgetting a sighting on sign-out turns on: dropping
    // one we only HOPED had arrived would lose it for good.

    private static func upload(_ path: String, data: Data, token: String,
                               bucket: String = SightingSync.bucket) async -> Bool {
        var r = Supa.request("/storage/v1/object/\(bucket)/\(path)", token: token)
        r.setValue("image/jpeg", forHTTPHeaderField: "Content-Type")
        // Replace rather than refuse when it is already there.
        r.setValue("true", forHTTPHeaderField: "x-upsert")
        r.httpBody = data
        guard let (_, resp) = try? await Net.data(for: r),
              let http = resp as? HTTPURLResponse else { return false }
        return (200..<300).contains(http.statusCode)
    }

    private static func download(_ path: String, token: String) async -> Data? {
        let r = Supa.request("/storage/v1/object/\(bucket)/\(path)", method: "GET", token: token)
        guard let (data, resp) = try? await Net.data(for: r),
              let http = resp as? HTTPURLResponse, (200..<300).contains(http.statusCode)
        else { return nil }
        return data
    }

    /// Every sighting photograph this account has uploaded, deleted.
    ///
    /// Called from Account.deleteAccount() before the account itself goes.
    /// The sighting ROWS cascade off auth.users and need nobody's help; the
    /// JPEGs in the bucket do not, because storage.objects is not reachable
    /// by a foreign key and Supabase refuses a delete against it from SQL.
    /// Until 2026-08-28 only the avatar was cleaned up this way, so deleting
    /// an account left every photograph a person had taken sitting in the
    /// bucket under a path that is literally their user id, while the privacy
    /// page said "Nothing is kept back".
    ///
    /// Unguarded on purpose, the same reasoning as the avatar: if this fails
    /// the account still goes. An orphaned file is a tidy-up job; an account
    /// that will not delete is a broken promise and a rejected app.
    static func purge(userId: String, token: String) async {
        for name in await list(prefix: userId, token: token) {
            await deleteObject("\(userId)/\(name)", token: token)
        }
    }

    private static func deleteObject(_ path: String, token: String) async {
        let r = Supa.request("/storage/v1/object/\(bucket)/\(path)", method: "DELETE", token: token)
        _ = try? await Net.data(for: r)
    }

    private static func list(prefix: String, token: String) async -> [String] {
        let r = Supa.request("/storage/v1/object/list/\(bucket)", token: token,
                             body: ["prefix": prefix, "limit": 200])
        guard let (data, _) = try? await Net.data(for: r),
              let j = try? JSONSerialization.jsonObject(with: data) as? [[String: Any]]
        else { return [] }
        return j.compactMap { $0["name"] as? String }
    }

    // MARK: - sharing one of them

    /// The unlisted page for a tree of yours, made the moment somebody asks
    /// for it and not before.
    ///
    /// Hidde, 2026-09-02: "kunnen we niet een pagina maken van de boom die wel
    /// deelbaar is?" Unlisted was his answer to the question the references
    /// raise (CONVENTIONS.md, "A page for something a person added, and who
    /// may see it"), and it is the whole of what this does: one row is flipped,
    /// one photograph is copied into a public bucket, and the address carries
    /// the sighting's own uuid so nothing else leads to it.
    ///
    /// Nothing is shared by opening a page, only by tapping the button. The
    /// position never travels: `shared_trees` does not select it.
    private static let sharedBucket = "shared-sightings"

    static func publish(_ sighting: Sightings.Sighting, account: Account,
                        sightings: Sightings) async -> URL? {
        guard let s = await account.freshSession() else { return nil }
        // The picture first, so a page never exists pointing at a file that is
        // not there. Same order as push(), and for the same reason.
        if let image = sightings.image(sighting), let data = Sightings.downsized(image) {
            let path = "\(s.userId)/\(sighting.id.uuidString).jpg"
            _ = await upload(path, data: data, token: s.accessToken, bucket: sharedBucket)
        }
        let ok = await Supa.ok(Supa.request(
            "/rest/v1/sightings?user_id=eq.\(s.userId)&id=eq.\(sighting.id.uuidString)",
            method: "PATCH", token: s.accessToken, body: ["shared": true],
            prefer: "return=minimal"))
        guard ok else { return nil }
        await MainActor.run { sightings.setShared(sighting.id, true) }
        return url(for: sighting.id)
    }

    /// Taking it back: the row stops being readable and the public copy goes.
    /// The private one is untouched, so the tree itself is not lost.
    static func unpublish(_ sighting: Sightings.Sighting, account: Account,
                          sightings: Sightings) async {
        guard let s = await account.freshSession() else { return }
        _ = await Supa.ok(Supa.request(
            "/rest/v1/sightings?user_id=eq.\(s.userId)&id=eq.\(sighting.id.uuidString)",
            method: "PATCH", token: s.accessToken, body: ["shared": false],
            prefer: "return=minimal"))
        let r = Supa.request("/storage/v1/object/\(sharedBucket)/\(s.userId)/\(sighting.id.uuidString).jpg",
                             method: "DELETE", token: s.accessToken)
        _ = try? await Net.data(for: r)
        await MainActor.run { sightings.setShared(sighting.id, false) }
    }

    static func url(for id: UUID) -> URL? {
        // /t and not /t/: the site builds in Astro's "file" format, so the page is
        // t.html and GitHub Pages serves it at /t. The trailing slash 404s, which
        // is the kind of thing you only find by asking the live site.
        URL(string: "https://ancienttrees.app/t?id=" + id.uuidString.lowercased())
    }
}
