// The account, and the two ways into it.
//
// Written 2026-08-20 against the same Supabase project the website has used
// since 2026-07-28, so a person who signed in on ancienttrees.app and then
// installs the app is the same person with the same collection. That is the
// whole reason this exists: an account here is not a new thing to sell, it is
// the answer to "I ticked six trees and then got a new phone".
//
// Three routes in, and the order on screen is deliberate: the taps first, the
// typing second.
//
// 1. SIGN IN WITH APPLE. One Face ID tap, no typing, and the app is never left.
//    On a phone that is the difference between an account and a shrug.
// 2. GOOGLE, added 2026-08-20 on Hidde's yes, through a system sheet rather than
//    Google's SDK. See OAuth.swift for why that matters.
// 3. AN EMAILED CODE, typed back into the app. Not a magic link: a link means
//    leaving the app for Mail and hoping the way back works, which is where the
//    website loses people and where an app loses them worse.
//
// ONE THING THESE THREE DO NOT SHARE, and it is the trap: Supabase folds two
// sign-ins into one account when the verified email matches, so Google on the
// phone and Google on the website are the same person with one collection. But
// Sign in with Apple hands out a private relay address by default, which is a
// DIFFERENT address, so Apple on the phone and Google on the laptop are two
// accounts and the second one looks empty. That is why every screen that shows
// an account shows which address it is: a person who can see
// "someone@privaterelay.appleid.com" can work out what happened, and a person
// who cannot just thinks we lost their trees.
//
// What we store is unchanged from the rule Hidde set when he opened the account
// track (DECISIONS.md 2026-08-14): an email address and a collection, nothing
// else. No name, no profile, no avatar, and nothing about a person renders
// anywhere. Deletion stays end to end through the same delete_user() the
// website calls, because that is the promise that made accounts acceptable.

import Foundation
import Observation

public enum Supa {
    public static let url = "https://caimvxiyrtifilimlkqw.supabase.co"
    public static let key = "sb_publishable_qOTuw-LCejk2VhO2J6aXGQ_6X2O2mgb"

    static func request(_ path: String, method: String = "POST",
                        token: String? = nil, body: Any? = nil,
                        prefer: String? = nil) -> URLRequest {
        var r = URLRequest(url: URL(string: url + path)!)
        r.httpMethod = method
        r.timeoutInterval = 20            // a hang costs more than a refusal
        r.setValue(key, forHTTPHeaderField: "apikey")
        r.setValue("application/json", forHTTPHeaderField: "Content-Type")
        r.setValue("Bearer " + (token ?? key), forHTTPHeaderField: "Authorization")
        if let prefer { r.setValue(prefer, forHTTPHeaderField: "Prefer") }
        // Data passes straight through: Profiles and Moderation encode their
        // rows with JSONEncoder before they get here, and that was the whole
        // reason they had a request builder of their own.
        if let raw = body as? Data { r.httpBody = raw }
        else if let body { r.httpBody = try? JSONSerialization.data(withJSONObject: body) }
        return r
    }

    // MARK: - the four things anybody does with it
    //
    // These lived twice, character for character, as private helpers in
    // CloudSync and SightingSync, and six more files built their own URLRequest
    // rather than calling request() above. That was not merely untidy. Only
    // request() sets a timeout, so Submissions, VoteCounts, Profiles,
    // Moderation and Diagnostics all ran on the system default of sixty
    // seconds: a minute of somebody standing under a tree watching nothing
    // happen, in an app whose whole point is being outside with poor signal.
    //
    // And the copies are where the bugs were. Profiles and ProfileEditor built
    // their URL with appendingPathComponent, which percent-encodes the "?" in
    // "profiles?on_conflict=user_id" into a table name with a question mark in
    // it, so saving a name or a picture had never once worked. request() has
    // always concatenated, which is exactly why saves, visited and sightings
    // were fine all along. One builder means one answer.

    /// A GET returning rows, or an empty list. Nothing here ever throws at the
    /// caller: a failed read of somebody's saves is a non-event, same rule as
    /// the catalogue's failed refresh.
    static func rows(_ path: String, token: String? = nil) async -> [[String: Any]] {
        let r = request(path, method: "GET", token: token)
        guard let (data, _) = try? await Net.data(for: r),
              let j = try? JSONSerialization.jsonObject(with: data) as? [[String: Any]]
        else { return [] }
        return j
    }

    /// An upsert. Returns whether the row actually landed, which matters
    /// wherever we then forget the local copy: dropping something we only HOPED
    /// had arrived loses it for good.
    @discardableResult
    static func post(_ path: String, token: String? = nil, body: Any,
                     prefer: String = "resolution=merge-duplicates,return=minimal") async -> Bool {
        await ok(request(path, token: token, body: body, prefer: prefer))
    }

    @discardableResult
    static func delete(_ path: String, token: String? = nil) async -> Bool {
        await ok(request(path, method: "DELETE", token: token, prefer: "return=minimal"))
    }

    /// Did the server say yes. One reading of a status code, so "did it work"
    /// cannot come to two answers in two files.
    static func ok(_ r: URLRequest) async -> Bool {
        guard let (_, resp) = try? await Net.data(for: r),
              let http = resp as? HTTPURLResponse else { return false }
        return (200..<300).contains(http.statusCode)
    }
}

/// The tokens, kept in the Keychain rather than UserDefaults.
///
/// UserDefaults is fine for a list of tree ids, which is what Saved uses it for.
/// It is not fine for a credential: it sits in a plist inside the app container
/// and it lands in an unencrypted backup. The Keychain costs about thirty lines
/// and removes a whole class of "how did that leak" from a product that holds
/// somebody's email address.
enum TokenStore {
    private static let service = "app.ancienttrees.session"
    private static let account = "supabase"

    static func save(_ data: Data) {
        let q: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
                                kSecAttrService as String: service,
                                kSecAttrAccount as String: account]
        SecItemDelete(q as CFDictionary)
        var add = q
        add[kSecValueData as String] = data
        add[kSecAttrAccessible as String] = kSecAttrAccessibleAfterFirstUnlock
        SecItemAdd(add as CFDictionary, nil)
    }

    static func read() -> Data? {
        let q: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
                                kSecAttrService as String: service,
                                kSecAttrAccount as String: account,
                                kSecReturnData as String: true,
                                kSecMatchLimit as String: kSecMatchLimitOne]
        var out: CFTypeRef?
        guard SecItemCopyMatching(q as CFDictionary, &out) == errSecSuccess else { return nil }
        return out as? Data
    }

    static func clear() {
        SecItemDelete([kSecClass as String: kSecClassGenericPassword,
                       kSecAttrService as String: service,
                       kSecAttrAccount as String: account] as CFDictionary)
    }
}

public struct Session: Codable, Sendable, Equatable {
    public var accessToken: String
    public var refreshToken: String
    public var expiresAt: Date
    public var userId: String
    public var email: String?

    /// Internal until 2026-08-30, when signing out needed to ask it: the
    /// sign-out uploads with the token already in hand rather than refreshing
    /// one first, because a refresh is a network round trip standing between a
    /// person and the door.
    public var isFresh: Bool { expiresAt.timeIntervalSinceNow > 300 }
}

/// MAIN-ACTOR ISOLATED, like every store the app keeps in the root.
///
/// It was not, and it is the one where that hurt: `session` is written by
/// restore(), by three sign-in routes and by refreshIfNeeded(), and the last of
/// those runs from whatever background task happened to ask. Two of them at
/// once is a data race on a class property, which Swift 5 mode compiles without
/// a word. Isolating it costs an await at three call sites and turns the whole
/// class of "I was suddenly signed out" into something the compiler can see.
@MainActor
@Observable
public final class Account {
    public enum State: Equatable {
        case signedOut
        case working
        case codeSent(email: String)
        case signedIn(email: String?)
    }

    public private(set) var state: State = .signedOut
    public private(set) var session: Session?
    /// Shown under the form when something failed, in plain words. Never a
    /// status code: nobody has ever been helped by "HTTP 422".
    public private(set) var problem: String?

    public var isSignedIn: Bool { session != nil }
    public var email: String? { session?.email }

    public init() {
        // Test scaffolding, the same family as -at=, -collected= and -tab:
        // simctl cannot sign in, and since 2026-08-25 saving and ticking need
        // an account, so without this every UI test that ticks a tree measures
        // the sign-in sheet instead of the thing it is testing. A local session
        // with no tokens: isSignedIn is true, and any network call it tries
        // fails as it would for an expired one.
        //
        // It is deliberately not a way to sign in. There is nothing to sign in
        // TO here, no user id that any row could belong to.
        if ProcessInfo.processInfo.arguments.contains("-signed-in") {
            session = Session(accessToken: "", refreshToken: "",
                              expiresAt: .distantFuture,
                              userId: "00000000-0000-0000-0000-000000000000",
                              email: "test@ancienttrees.app")
            state = .signedIn(email: session?.email)
            return
        }
        restore()
    }

    /// A unit test's way in, and only that. It sets the two fields the Keychain
    /// would have restored and touches nothing else, so a test about what
    /// happens to a session left alone for three weeks needs no Keychain, no
    /// network and no real account.
    init(restoring session: Session?) {
        self.session = session
        state = session.map { .signedIn(email: $0.email) } ?? .signedOut
    }

    // MARK: - restoring

    private func restore() {
        guard let d = TokenStore.read(),
              let s = try? JSONDecoder().decode(Session.self, from: d) else { return }
        session = s
        state = .signedIn(email: s.email)
    }

    private func store(_ s: Session) {
        session = s
        state = .signedIn(email: s.email)
        problem = nil
        if let d = try? JSONEncoder().encode(s) { TokenStore.save(d) }
    }

    /// A token that will still be accepted, or nil.
    ///
    /// Every write on somebody's behalf goes through here, because reading
    /// `session?.accessToken` straight out gives you whatever was minted when
    /// they last signed in, and those live an hour. ProfileEditor read it
    /// straight and so saving a name and a picture failed for anybody who had
    /// been signed in longer than that, which is everybody after the first
    /// afternoon (Hidde, 2026-08-27, on his own phone: "foutmelding als ik foto
    /// en naam wil opslaan").
    public func freshToken() async -> String? {
        guard await refreshIfNeeded() else { return nil }
        return session?.accessToken
    }

    /// The whole session, refreshed first. The two-step version of this
    /// (`guard await refreshIfNeeded(), let s = session`) is what CloudSync and
    /// SightingSync each wrote four times, and it reads the property back in a
    /// second statement, which is a gap another task can change the session in.
    public func freshSession() async -> Session? {
        guard await refreshIfNeeded() else { return nil }
        return session
    }

    /// The refresh in flight, so there is never more than one.
    ///
    /// THE REASON IT MATTERS IS THAT A SECOND ONE CAN SIGN SOMEBODY OUT. Launch
    /// asks three times at once: this method directly, and freshToken() from
    /// the profiles load and from the moderation load. All three saw a stale
    /// token, all three posted the SAME refresh token, and Supabase rotates it.
    /// Its reuse window covers a fast network and nothing else: past that the
    /// second answer is a refusal, and a refusal here is read as a real
    /// sign-out and empties the Keychain. So a perfectly good session could be
    /// thrown away by the app asking politely twice, on a slow connection,
    /// which is the shape of every "ik was ineens uitgelogd" that never
    /// reproduces.
    ///
    /// The waiters share one answer instead. Nothing about the outcome changes:
    /// a refusal is still a sign-out, no signal is still not one.
    @ObservationIgnored private var refreshTask: Task<Bool, Never>?

    /// Keep the hour-long access token alive off the refresh token.
    ///
    /// The website shipped without this and it broke exactly as you would
    /// expect: an hour after signing in, saves silently stopped reaching the
    /// account and nothing said so. Doing it here on every launch means the app
    /// never reaches that state.
    @discardableResult
    public func refreshIfNeeded() async -> Bool {
        guard let s = session else { return false }
        if s.isFresh { return true }
        if let running = refreshTask { return await running.value }
        let task = Task { @MainActor [refreshToken = s.refreshToken] in
            // Cleared by the task itself rather than by a waiter: a waiter that
            // clears it can be the slow one, and by then a later caller may
            // already have put a new task in.
            defer { self.refreshTask = nil }
            let r = Supa.request("/auth/v1/token?grant_type=refresh_token",
                                 body: ["refresh_token": refreshToken])
            return self.apply(await Self.refresh(r))
        }
        refreshTask = task
        return await task.value
    }

    /// The verdict, in one place, so the three outcomes cannot drift apart.
    private func apply(_ outcome: Refreshed) -> Bool {
        switch outcome {
        case .ok(let parsed):
            store(parsed)
            return true
        case .rejected:
            // A spent or revoked refresh token is a real sign-out. Leaving it in
            // place would show an account screen that cannot save anything.
            signOut()
            return false
        case .unreachable:
            // NO SIGNAL IS NOT A SIGN-OUT, and it used to be one. Found by the
            // first offline test ever written here (2026-08-27): every failure
            // took the same branch, so opening the app an hour after signing in,
            // in a wood with no bereik, cleared the Keychain and asked the
            // person to sign in again. Which is precisely where this app is
            // meant to be used, and the one place it could not ask them to.
            //
            // Nothing is lost by keeping it. The collection is already correct
            // on the phone, the token is refused by the server anyway if it has
            // really been revoked, and the next launch with a signal tries
            // again and gets a real answer.
            return false
        }
    }

    private enum Refreshed {
        case ok(Session)
        case rejected        // the server answered, and the answer was no
        case unreachable     // nobody answered at all
    }

    private static func refresh(_ r: URLRequest) async -> Refreshed {
        guard let (data, resp) = try? await Net.data(for: r),
              let http = resp as? HTTPURLResponse else { return .unreachable }
        // A 5xx is the server saying it is broken, not that this token is. It
        // belongs with no-signal rather than with a refusal: Supabase having a
        // bad ten minutes must not empty somebody's Keychain, which is the same
        // mistake as the one above wearing a different hat.
        if http.statusCode >= 500 { return .unreachable }
        guard (200..<300).contains(http.statusCode) else { return .rejected }
        guard let parsed = session(from: data) else { return .rejected }
        return .ok(parsed)
    }

    // MARK: - the email route

    public func sendCode(to address: String) async {
        let clean = address.trimmingCharacters(in: .whitespacesAndNewlines)
        guard clean.contains("@"), clean.count > 3 else {
            problem = "That does not look like an email address."
            return
        }
        state = .working
        problem = nil
        let r = Supa.request("/auth/v1/otp",
                             body: ["email": clean, "create_user": true])
        guard let (_, resp) = try? await Net.data(for: r),
              let http = resp as? HTTPURLResponse, (200..<300).contains(http.statusCode) else {
            state = .signedOut
            problem = "We could not send that just now. Try again in a minute."
            return
        }
        state = .codeSent(email: clean)
    }

    public func verify(code: String, email: String) async {
        let clean = code.filter(\.isNumber)
        guard clean.count >= 6 else {
            problem = "That code is six digits."
            return
        }
        state = .working
        problem = nil
        let r = Supa.request("/auth/v1/verify",
                             body: ["email": email, "token": clean, "type": "email"])
        guard let parsed = await Self.send(r) else {
            state = .codeSent(email: email)
            problem = "That code did not work. Check it, or ask for a new one."
            return
        }
        store(parsed)
    }

    // MARK: - the Apple route

    public func signInWithApple(idToken: String, nonce: String) async {
        state = .working
        problem = nil
        let r = Supa.request("/auth/v1/token?grant_type=id_token",
                             body: ["provider": "apple", "id_token": idToken, "nonce": nonce])
        guard let parsed = await Self.send(r) else {
            state = .signedOut
            problem = "Apple sign-in is not switched on yet. Use your email for now."
            return
        }
        store(parsed)
    }

    // MARK: - the Google route

    /// The tokens come back on the callback URL rather than from a token
    /// exchange, because Supabase does the exchange with Google itself. So this
    /// builds the session out of the fragment instead of going through send().
    public func signInWithGoogle() async {
        state = .working
        problem = nil
        guard let f = await OAuth.run(provider: "google") else {
            state = .signedOut
            return                                   // cancelled: not an error
        }
        guard let access = f["access_token"], let refresh = f["refresh_token"] else {
            state = .signedOut
            problem = f["error_description"]?.replacingOccurrences(of: "+", with: " ")
                ?? "Google sign-in is not switched on yet. Use your email for now."
            return
        }
        let expires = Double(f["expires_in"] ?? "3600") ?? 3600
        var session = Session(accessToken: access,
                              refreshToken: refresh,
                              expiresAt: Date().addingTimeInterval(expires),
                              userId: "", email: nil)
        // The callback carries no user, so ask who this is. Without it the
        // account screen cannot say which address you signed in with, which is
        // the one thing that makes an Apple relay address versus a Google
        // address understandable rather than mysterious.
        if let who = await Self.user(accessToken: access) {
            session.userId = who.id
            session.email = who.email
        }
        store(session)
    }

    private static func user(accessToken: String) async -> (id: String, email: String?)? {
        let r = Supa.request("/auth/v1/user", method: "GET", token: accessToken)
        guard let (data, resp) = try? await Net.data(for: r),
              let http = resp as? HTTPURLResponse, (200..<300).contains(http.statusCode),
              let j = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let id = j["id"] as? String else { return nil }
        return (id, j["email"] as? String)
    }

    // MARK: - leaving

    public func signOut() {
        TokenStore.clear()
        session = nil
        state = .signedOut
    }

    /// The promise that made accounts acceptable in the first place, so it calls
    /// the same delete_user() the website calls rather than a second path that
    /// could quietly drift out of step with it. The saves and visited tables
    /// cascade off auth.users, so the collection goes with the row.
    public func deleteAccount() async -> Bool {
        guard await refreshIfNeeded(), let s = session else { return false }
        // THE PROFILE PICTURE FIRST, and from here rather than from the SQL.
        //
        // Everything else this account owns hangs off auth.users with a
        // cascade, so deleting the account takes it. A file in storage does
        // not: storage.objects is not reachable by a cascade and Supabase
        // refuses a delete against it from SQL outright, which broke the whole
        // function for an hour on 2026-08-27 until the deletion test was
        // actually run.
        //
        // Not guarded, deliberately. If this fails, the account still goes: an
        // orphaned image is a tidy-up job, an account that will not delete is a
        // broken promise and a rejected app.
        _ = try? await Net.data(
            for: Supa.request("/storage/v1/object/avatars/\(s.userId)/avatar.jpg",
                              method: "DELETE", token: s.accessToken))
        // And the sighting photographs, which are the same problem and were
        // missed. Their ROWS cascade off auth.users; the JPEGs in the
        // sightings bucket do not, so before 2026-08-28 deleting an account
        // left every picture somebody had taken sitting under a path that is
        // their own user id, while the privacy page promised nothing is kept
        // back. Found while writing that page's missing paragraph.
        await SightingSync.purge(userId: s.userId, token: s.accessToken)
        let r = Supa.request("/rest/v1/rpc/delete_user", token: s.accessToken)
        let ok = (try? await Net.data(for: r))
            .flatMap { ($0.1 as? HTTPURLResponse) }
            .map { (200..<300).contains($0.statusCode) } ?? false
        if ok { signOut() }
        return ok
    }

    // MARK: - the one place a token response is read

    private static func send(_ r: URLRequest) async -> Session? {
        guard let (data, resp) = try? await Net.data(for: r),
              let http = resp as? HTTPURLResponse, (200..<300).contains(http.statusCode)
        else { return nil }
        return session(from: data)
    }

    /// One parser, used by both routes above. It was written twice for a while
    /// and the two copies were already drifting.
    private static func session(from data: Data) -> Session? {
        guard let j = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let access = j["access_token"] as? String,
              let refresh = j["refresh_token"] as? String else { return nil }
        let user = j["user"] as? [String: Any]
        let expires = (j["expires_in"] as? Double) ?? 3600
        return Session(accessToken: access,
                       refreshToken: refresh,
                       expiresAt: Date().addingTimeInterval(expires),
                       userId: (user?["id"] as? String) ?? "",
                       email: user?["email"] as? String)
    }
}

/// Why the sheet opened, which decides its headline.
public enum SignInReason: Equatable, Identifiable {
    /// The one line every passive sign-in prompt uses: the card on My trees,
    /// the row on Settings, the name at the top of the collection. Written
    /// once because it was written three times and they had already drifted
    /// into two different sentences, both of them about our plumbing rather
    /// than about what a person gets (Hidde, 2026-08-29).
    public static let prompt = "Register and sign in to add and save trees."


    public var id: String { headline }

    case general
    case keepTree(String)        // just ticked or saved this one
    case keepCollection(Int)     // has this many and nothing backing them up
    case seasonAlerts
    case feedback                // votes, reports and tips need the account
                                 // that lets us answer (2026-08-21 ruling)

    /// SHALLOW ON PURPOSE (Hidde, 2026-08-29, reading "Sign in to keep your 7
    /// trees" over "Sign in and they follow you": "kijk even naar conventies
    /// wat voor copy je normaal hier zegt, hou het maar wat oppervlakkiger
    /// zodat we niet elke keer als we iets wijzigen die tekst niet meer
    /// klopt").
    ///
    /// Convention, recorded in CONVENTIONS.md: a sign-in sheet says in one
    /// short line what an account is for and stops. Google Maps ("Sign in to
    /// get the most out of Maps"), AllTrails, Airbnb and Apple all do the same
    /// thing, and none of them counts anything or promises a mechanism.
    ///
    /// Two faults in the line he read. It carried a NUMBER, which is a fact
    /// about this moment printed into a sentence, and PRODUCT_COPY.md already
    /// bans that anywhere nothing regenerates it. And "they follow you to the
    /// website and to any phone" describes our sync, which is a promise that
    /// has to stay true through every change we make to it.
    ///
    /// So the copy says what somebody GETS and never how. A line like that
    /// survives a rewrite of everything underneath it.
    var headline: String {
        switch self {
        case .general, .keepCollection: "Sign in to add and save trees"
        // Short on purpose. An earlier version put the tree's name in the
        // headline and "Keep The Last Elm of Stationsplein" ran the full width
        // of the phone at title size, which is a layout that only holds for the
        // short names.
        case .keepTree: "Sign in to keep this one"
        case .seasonAlerts: "Sign in for season alerts"
        case .feedback: "Sign in to have your say"
        }
    }

    var detail: String {
        switch self {
        case .general, .keepCollection, .keepTree:
            "An account keeps what you collect and save."
        case .seasonAlerts:
            "We can only tell you about a tree if we know where to reach you."
        case .feedback:
            "Every vote, correction and tip gets checked and answered, and your account is how the answer reaches you."
        }
    }
}
