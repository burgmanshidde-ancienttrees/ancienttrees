// Signing in with Google, without Google's SDK.
//
// Hidde said to build it on 2026-08-20, which is the yes hard rule 5 needs: an
// identity provider is a third party in the product. What that rule is actually
// protecting against is a dependency that can break the app while nobody is
// looking, and this deliberately avoids one. There is no GoogleSignIn package
// here. ASWebAuthenticationSession ships with iOS, opens Google's own page in a
// system sheet the app cannot read, and hands back the callback URL. If Google
// changed everything tomorrow, the worst case is a button that says it did not
// work.
//
// It also means the app never sees a password and never sees a Google session,
// which is the whole point of doing it this way rather than in a WebView.
//
// The callback scheme does NOT need registering in Info.plist, which is the
// usual reason people reach for the SDK. ASWebAuthenticationSession intercepts
// its own callbackURLScheme in process. What it DOES need is Supabase's redirect
// allow-list to contain ancienttrees://auth-callback, which is Hidde's, and
// until it is there Supabase quietly redirects to the website instead. So a
// missing token is reported as "not switched on yet" rather than as a mystery.

import Foundation
import AuthenticationServices

@MainActor
public enum OAuth {
    public static let callbackScheme = "ancienttrees"
    static let callback = "ancienttrees://auth-callback"

    /// Runs the sheet and returns the fragment Supabase puts on the callback,
    /// or nil if the person cancelled or nothing came back.
    public static func run(provider: String) async -> [String: String]? {
        let url = URL(string: Supa.url
            + "/auth/v1/authorize?provider=\(provider)"
            + "&redirect_to=\(callback.addingPercentEncoding(withAllowedCharacters: .alphanumerics) ?? callback)")!

        let anchor = PresentationAnchor()
        return await withCheckedContinuation { (c: CheckedContinuation<[String: String]?, Never>) in
            let session = ASWebAuthenticationSession(url: url,
                                                     callbackURLScheme: callbackScheme) { callbackURL, _ in
                guard let callbackURL else { c.resume(returning: nil); return }
                c.resume(returning: fragment(of: callbackURL))
            }
            session.presentationContextProvider = anchor
            // The person may already be signed into Google in Safari, and using
            // that is the entire speed advantage over typing an address.
            session.prefersEphemeralWebBrowserSession = false
            if !session.start() { c.resume(returning: nil) }
        }
    }

    /// Supabase returns its tokens in the URL fragment, the same shape the
    /// website's magic link uses.
    static func fragment(of url: URL) -> [String: String] {
        var out: [String: String] = [:]
        let raw = (url.fragment ?? "").isEmpty ? (url.query ?? "") : (url.fragment ?? "")
        for pair in raw.split(separator: "&") {
            let kv = pair.split(separator: "=", maxSplits: 1)
            guard kv.count == 2 else { continue }
            out[String(kv[0])] = String(kv[1]).removingPercentEncoding ?? String(kv[1])
        }
        return out
    }

    /// ASWebAuthenticationSession needs a window to hang the sheet on.
    final class PresentationAnchor: NSObject, ASWebAuthenticationPresentationContextProviding {
        func presentationAnchor(for session: ASWebAuthenticationSession) -> ASPresentationAnchor {
            let scene = UIApplication.shared.connectedScenes
                .compactMap { $0 as? UIWindowScene }
                .first { $0.activationState == .foregroundActive }
            return scene?.keyWindow ?? ASPresentationAnchor()
        }
    }
}
