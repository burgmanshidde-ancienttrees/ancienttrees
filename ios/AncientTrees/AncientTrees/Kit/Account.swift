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
        if let body { r.httpBody = try? JSONSerialization.data(withJSONObject: body) }
        return r
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

    var isFresh: Bool { expiresAt.timeIntervalSinceNow > 300 }
}

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

    public init() { restore() }

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
        let r = Supa.request("/auth/v1/token?grant_type=refresh_token",
                             body: ["refresh_token": s.refreshToken])
        guard let parsed = await Self.send(r) else {
            // A spent or revoked refresh token is a real sign-out. Leaving it in
            // place would show an account screen that cannot save anything.
            signOut()
            return false
        }
        store(parsed)
        return true
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
        guard let (_, resp) = try? await URLSession.shared.data(for: r),
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
        guard let (data, resp) = try? await URLSession.shared.data(for: r),
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
        let r = Supa.request("/rest/v1/rpc/delete_user", token: s.accessToken)
        let ok = (try? await URLSession.shared.data(for: r))
            .flatMap { ($0.1 as? HTTPURLResponse) }
            .map { (200..<300).contains($0.statusCode) } ?? false
        if ok { signOut() }
        return ok
    }

    // MARK: - the one place a token response is read

    private static func send(_ r: URLRequest) async -> Session? {
        guard let (data, resp) = try? await URLSession.shared.data(for: r),
              let http = resp as? HTTPURLResponse, (200..<300).contains(http.statusCode),
              let j = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
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
    public var id: String { headline }

    case general
    case keepTree(String)        // just ticked or saved this one
    case keepCollection(Int)     // has this many and nothing backing them up
    case seasonAlerts

    var headline: String {
        switch self {
        case .general: "Keep your trees"
        // Short on purpose. An earlier version put the tree's name in the
        // headline and "Keep The Last Elm of Stationsplein" ran the full width
        // of the phone at title size, which is a layout that only holds for the
        // short names. The name belongs in the sentence underneath, where it can
        // wrap without breaking anything.
        case .keepTree: "That one is yours"
        case .keepCollection(let n): n == 1 ? "Keep your tree safe" : "Keep your \(n) trees safe"
        case .seasonAlerts: "Be told when a tree near you peaks"
        }
    }

    var detail: String {
        switch self {
        case .general:
            "Right now your collection lives on this phone only. An account keeps it, and puts it on the website too."
        case .keepTree(let name):
            "\(name) is ticked off. That record lives on this phone only, so an account is what keeps it, here and on the website."
        case .keepCollection:
            "They live on this phone only. Lose it, replace it, or reinstall, and they are gone. An account keeps them, and puts them on the website too."
        case .seasonAlerts:
            "We can only tell you about a tree if we know where to reach you."
        }
    }
}
