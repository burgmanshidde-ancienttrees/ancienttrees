// The ambassador badge: one person looking after one place.
//
// Convention: komoot's Pioneer badge (CONVENTIONS.md 2026-10-02), a small seal
// beside the name on the person's own profile and contributions, tied to one
// region and earned by what they already did. Google's Local Guides badge is
// the same shape at level 4. Ours is Apple's checkmark.seal.fill (the website
// draws Phosphor's seal-check, its listed twin) in the moss pill the app
// already uses for a person's avatar, with the place's name. On your OWN
// profile it opens the place you look after (Hidde, 2026-10-18: "Baarn
// ambassador ... zou klikbaar moeten zijn"); on somebody else's row it stays
// a label.
//
// Hidde, 2026-10-02: "ambassador idea is perfect lets implement it in both app
// and web." The website draws the same badge beside your name on /account and
// one line under a city's intro, there only with the person's consent to be
// named (AmbassadorLine.astro). The rows come from supabase/ambassadors.sql
// through Profiles.myPlaces and Profiles.placesByUser.
import SwiftUI

struct AmbassadorBadge: View {
    let places: [Profiles.Ambassador]
    /// 12 under a row's name, 13 under the My trees header.
    var size: CGFloat = 12
    /// In a LIST ROW the badge says only the place ("Amsterdam"), because the
    /// row also holds Follow and a menu and the full label truncated to
    /// "Amsterdam a..." on the smallest phone (seen in the sweep, 2026-10-02).
    /// komoot's list rows carry the seal alone; the word "ambassador" belongs
    /// on the person's own header, where there is room for it.
    var compact = false
    /// Set on your own profile: a tap opens the (first) place's page.
    var open: ((Profiles.Ambassador) -> Void)? = nil

    var body: some View {
        if let open, let first = places.first {
            Button { open(first) } label: { pill }
                .buttonStyle(.plain)
                .frame(minHeight: 44)
                .contentShape(.rect)
                .accessibilityHint("Opens \(first.place_name)")
        } else {
            pill
        }
    }

    @ViewBuilder private var pill: some View {
        if !places.isEmpty {
            HStack(spacing: 4) {
                Image(systemName: "checkmark.seal.fill")
                    .font(.system(size: size + 1, weight: .semibold))
                Text(label)
                    .font(.system(size: size, weight: .medium))
                    .lineLimit(1).truncationMode(.tail)
            }
            .foregroundStyle(Brand.moss)
            .padding(.vertical, 3)
            .padding(.leading, 7).padding(.trailing, 9)
            .background(Brand.moss.opacity(0.12), in: .capsule)
            .accessibilityElement(children: .combine)
            .accessibilityLabel(compact ? "\(label) ambassador" : label)
            .accessibilityIdentifier("ambassador-badge")
        }
    }

    /// "Paris ambassador", or "Paris and Lyon ambassador" for the rare person
    /// with two. Never a list longer than that: scarcity is the point.
    private var label: String {
        let names = places.map(\.place_name)
        if compact {
            return names.count == 1 ? names[0] : "\(names[0]) and \(names.count - 1) more"
        }
        switch names.count {
        case 0: return ""
        case 1: return "\(names[0]) ambassador"
        case 2: return "\(names[0]) and \(names[1]) ambassador"
        default: return "\(names[0]), \(names[1]) and \(names.count - 2) more, ambassador"
        }
    }
}

/// The early-adopter tag (Kit/EarlyAdopter.swift, 2026-10-16): the
/// ambassador's pill with its numbers unchanged, in gold rather than moss so
/// the two never read as the same thing, on the same row after it. Hidde
/// chose this as option 1 of five, over Polarsteps' hexagon seal on the photo
/// ("honestly i liked the tag better"). Apple's sparkle; the website draws
/// Phosphor's sparkle, its listed twin. A label, never a button.
struct EarlyAdopterBadge: View {
    var size: CGFloat = 12

    var body: some View {
        HStack(spacing: 4) {
            Image(systemName: "sparkle")
                .font(.system(size: size + 1, weight: .semibold))
            Text("Early adopter")
                .font(.system(size: size, weight: .medium))
                .lineLimit(1)
        }
        .foregroundStyle(Brand.goldInk)
        .padding(.vertical, 3)
        .padding(.leading, 7).padding(.trailing, 9)
        .background(Brand.gold.opacity(0.18), in: .capsule)
        .accessibilityElement(children: .combine)
        .accessibilityIdentifier("early-adopter-badge")
    }
}

/// The flag after your name (Hidde, 2026-10-16), Polarsteps' round flag: the
/// country the person picked in Edit profile, as Apple's own flag emoji
/// clipped to a circle. Nothing when they have not picked one.
struct CountryFlag: View {
    let code: String?
    var size: CGFloat = 20

    var body: some View {
        if let flag = Self.emoji(code), let img = Self.trimmed(flag) {
            // THE FLAG ITSELF, NOT ITS GLYPH BOX (Hidde, 2026-10-19: "the flag
            // is completely misaligned in the round circle"). The emoji's box
            // carries empty space above the flag, so a centred Text left a
            // white crescent top left. Drawn once, cropped to its own pixels,
            // then filled into the circle: Polarsteps' round flag.
            Image(uiImage: img)
                .resizable()
                .scaledToFill()
                .frame(width: size, height: size)
                .clipShape(.circle)
                .overlay(Circle().strokeBorder(.black.opacity(0.08), lineWidth: 1))
                .dynamicTypeSize(.large)
                .accessibilityLabel(Self.name(code) ?? "")
                .accessibilityIdentifier("profile-flag")
        }
    }

    /// The emoji drawn large and cropped to where it has pixels, cached per
    /// flag. Nil if nothing drew (an unknown pair renders as letters, which
    /// still crops to something, so in practice never).
    @MainActor private static var cache: [String: UIImage] = [:]
    @MainActor static func trimmed(_ flag: String) -> UIImage? {
        if let hit = cache[flag] { return hit }
        let font = UIFont.systemFont(ofSize: 96)
        let text = flag as NSString
        let attrs: [NSAttributedString.Key: Any] = [.font: font]
        let box = text.size(withAttributes: attrs)
        let fmt = UIGraphicsImageRendererFormat(); fmt.scale = 1
        let drawn = UIGraphicsImageRenderer(size: box, format: fmt).image { _ in
            text.draw(at: .zero, withAttributes: attrs)
        }
        guard let cg = drawn.cgImage, let crop = opaqueBounds(cg),
              let cut = cg.cropping(to: crop) else { return nil }
        // An inset of a few percent so the waving edge of the flag never
        // shows as a pale rim inside the circle.
        let inset = cut.cropping(to: CGRect(x: 0, y: 0, width: cut.width, height: cut.height)
            .insetBy(dx: CGFloat(cut.width) * 0.06, dy: CGFloat(cut.height) * 0.08)) ?? cut
        let out = UIImage(cgImage: inset)
        cache[flag] = out
        return out
    }

    /// The smallest rectangle holding every pixel that is not transparent.
    private static func opaqueBounds(_ cg: CGImage) -> CGRect? {
        let w = cg.width, h = cg.height
        var px = [UInt8](repeating: 0, count: w * h * 4)
        guard let ctx = CGContext(data: &px, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4,
                                  space: CGColorSpaceCreateDeviceRGB(),
                                  bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) else { return nil }
        ctx.draw(cg, in: CGRect(x: 0, y: 0, width: w, height: h))
        var minX = w, minY = h, maxX = -1, maxY = -1
        for y in 0..<h {
            for x in 0..<w where px[(y * w + x) * 4 + 3] > 24 {
                minX = min(minX, x); maxX = max(maxX, x)
                minY = min(minY, y); maxY = max(maxY, y)
            }
        }
        guard maxX >= minX, maxY >= minY else { return nil }
        return CGRect(x: minX, y: minY, width: maxX - minX + 1, height: maxY - minY + 1)
    }

    /// "NL" to the regional-indicator pair Apple draws as the Dutch flag.
    static func emoji(_ code: String?) -> String? {
        guard let c = code?.uppercased(), c.count == 2,
              c.unicodeScalars.allSatisfy({ ("A"..."Z").contains(Character($0)) }) else { return nil }
        return String(String.UnicodeScalarView(c.unicodeScalars.compactMap {
            Unicode.Scalar(127397 + $0.value)
        }))
    }

    static func name(_ code: String?) -> String? {
        code.flatMap { Locale(identifier: "en").localizedString(forRegionCode: $0) }
    }
}

/// Shown once per account, the first time the profile opens with the badge.
/// The website's sheet says the same (account.astro, early-dialog).
struct EarlyAdopterSheet: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        BrandSheet(
            icon: "sparkle",
            title: "You're an early adopter",
            message: "You are one of the first users of Ancient Trees. This badge is only for them.",
            buttons: [.primary("Done", id: "early-adopter-done") { dismiss() }],
            tint: .gold)
            // One container with a name, as the sign-in sheet carries, so the
            // layout sweep measures the sheet on its own and not against the
            // profile behind it (2026-10-18: "Done" at 24 read as a drift from
            // the profile's 20).
            .accessibilityElement(children: .contain)
            .accessibilityIdentifier("early-adopter-sheet")
    }
}

#Preview {
    VStack(alignment: .leading, spacing: 12) {
        AmbassadorBadge(places: [.init(user_id: "u", place_slug: "paris", place_name: "Paris", public: false)])
        EarlyAdopterBadge()
        CountryFlag(code: "NL")
        AmbassadorBadge(places: [.init(user_id: "u", place_slug: "friedewald", place_name: "Friedewald", public: true),
                                 .init(user_id: "u", place_slug: "bad-homburg", place_name: "Bad Homburg", public: true)], size: 13)
    }
    .padding()
}

/// The ambassador on a city page, komoot's person row (Hidde, 2026-10-03:
/// "follow the design way of komoot"): a 32 point round avatar, the name in
/// bold, one small grey line saying what they are. The website draws the same
/// row under the city intro (AmbassadorLine.astro); the names arrive in the
/// feed, so neither surface decides who is named.
struct AmbassadorRow: View {
    let name: String
    let place: String
    var affiliation: String? = nil

    var body: some View {
        HStack(spacing: 10) {
            Text(String(name.trimmingCharacters(in: .whitespaces).prefix(1)).uppercased())
                .font(.system(size: 14, weight: .bold))
                .foregroundStyle(Brand.moss)
                .frame(width: 32, height: 32)
                .background(Brand.moss.opacity(0.12), in: .circle)
                .overlay(alignment: .bottomTrailing) {
                    Image(systemName: "checkmark.seal.fill")
                        .font(.system(size: 12, weight: .semibold))
                        .foregroundStyle(Brand.moss)
                        .background(Brand.ground, in: .circle)
                        .offset(x: 3, y: 3)
                }
            VStack(alignment: .leading, spacing: 1) {
                Text(name)
                    .font(.system(size: 14, weight: .bold))
                    .foregroundStyle(Brand.ink)
                Text(affiliation.map { "\(place) ambassador · \($0)" } ?? "\(place) ambassador")
                    .font(.system(size: 12))
                    .foregroundStyle(Brand.inkSoft)
            }
        }
        .accessibilityElement(children: .combine)
        .accessibilityIdentifier("ambassador-row")
    }
}

/// The open seat on a city page with nobody named (Hidde, 2026-10-04: "Tokio
/// is looking for an ambassador met een knop"). The same row as AmbassadorRow
/// with a dashed, empty avatar and one button, as the website draws it under
/// the intro (AmbassadorLine.astro). Convention: Google Maps' "Join Local
/// Guides", one tap (CONVENTIONS.md 2026-10-04). Signed out opens the sign-in
/// sheet; signed in writes one request row and says thanks. The badge follows
/// the person's answer to our mail, never the tap.
struct AmbassadorWantedRow: View {
    let place: String

    @Environment(Account.self) private var account
    @State private var asked = false
    @State private var sending = false
    @State private var signingIn = false
    /// Confirm first, then say it arrived (Hidde, 2026-10-05: "ik zou eerder
    /// een pop up verwachten"), as Google Maps' "Join Local Guides" asks for
    /// a yes and then says you are in. ONE SHEET WITH TWO STEPS since
    /// 2026-10-10 (the one-sheet rule, Kit/BrandSheet.swift): the receipt is
    /// the sheet's next step rather than a system alert, the same two steps
    /// the website's sheet draws (AmbassadorLine.astro). A failure is news,
    /// so it is the snackbar.
    @State private var confirming = false
    @State private var sent = false
    @Environment(Navigator.self) private var navigator

    /// THE WHOLE ROW IS THE CONTROL (Hidde, 2026-10-04: "just make the whole
    /// thing clickable instead of adding a huge button"), an iOS list row with
    /// a chevron, as Google Maps draws "Join Local Guides". The website's row
    /// is the same (AmbassadorLine.astro).
    var body: some View {
        Button(action: tap) {
            HStack(spacing: 10) {
                Image(systemName: "checkmark.seal")
                    .font(.system(size: 14, weight: .semibold))
                    .foregroundStyle(Brand.moss)
                    .frame(width: 32, height: 32)
                    .overlay(Circle().strokeBorder(Brand.moss, style: StrokeStyle(lineWidth: 1.5, dash: [3, 3])))
                VStack(alignment: .leading, spacing: 1) {
                    Text("\(place) is looking for an ambassador")
                        .font(.system(size: 14, weight: .bold))
                        .foregroundStyle(Brand.ink)
                        .fixedSize(horizontal: false, vertical: true)
                    Text(asked ? "Request sent." : "Help us improve this list.")
                        .font(.system(size: 12))
                        .foregroundStyle(Brand.inkSoft)
                        .fixedSize(horizontal: false, vertical: true)
                }
                Spacer(minLength: 8)
                if !asked {
                    Image(systemName: "chevron.right")
                        .font(.caption.weight(.semibold))
                        .foregroundStyle(Brand.inkSoft.opacity(0.6))
                }
            }
            .frame(minHeight: 44)
            .contentShape(.rect)
        }
        .buttonStyle(.plain)
        .disabled(asked || sending)
        .accessibilityHint(asked ? "" : "Become the ambassador")
        .accessibilityIdentifier("ambassador-wanted")
        .task(id: account.isSignedIn) {
            // A sheet no argument can open ships unseen: -ambassadorask opens
            // the explainer, -ambassadorsent its receipt (2026-10-10).
            let args = ProcessInfo.processInfo.arguments
            if args.contains("-ambassadorask") || args.contains("-ambassadorsent") {
                sent = args.contains("-ambassadorsent")
                confirming = true
                return
            }
            asked = await Submission.askedToBeAmbassador(city: place, token: await account.freshToken())
        }
        // Sign in, THEN the confirm step (Hidde, 2026-10-07: "it should fire a
        // login screen and after that confirm ambassadorship"). The sheet
        // dismisses itself once the account is in; the tap is finished here
        // rather than swallowed, and nothing is sent until Send request.
        .sheet(isPresented: $signingIn, onDismiss: { if account.isSignedIn { confirming = true } }) {
            SignInSheet(reason: .ambassador, localCount: 0)
        }
        // WHAT THE ROLE IS, BEFORE THE YES (Hidde, 2026-10-08: "add some text
        // in an overlay both app and web that says an ambassador helps make
        // this list as good as possible for city, help with photos info and
        // walks. Apply here"). It was a bare alert with one sentence. Google
        // Maps' Local Guides join sheet is the convention: what you will do,
        // one line each, and one button. The website's dialog carries the
        // same three lines (AmbassadorLine.astro, i18n ambassadorAskPoints).
        .sheet(isPresented: $confirming, onDismiss: { sent = false }) {
            AmbassadorApplySheet(place: place, writeTo: writeTo, sent: $sent, sending: $sending) {
                send()
            }
        }
    }

    private var writeTo: String {
        account.email.map { " We will write to \($0)." } ?? ""
    }

    private func tap() {
        guard account.isSignedIn else { signingIn = true; return }
        confirming = true
    }

    /// A request needs a LIVE session, not just one stored on the phone
    /// (Hidde, 2026-10-06: "i just requested ambassador without being logged
    /// in", then "its not working"). isSignedIn only asks whether a session is
    /// saved; when it has expired and cannot be renewed, freshToken() is nil
    /// and the old code sent the request anyway on the publishable key, which
    /// the database refuses (supabase/postbox-needs-an-account.sql), and then
    /// said nothing at all. Now: no token opens the sign-in sheet, and a send
    /// that fails says so.
    private func send() {
        sending = true
        Task {
            guard let token = await account.freshToken() else {
                sending = false
                signingIn = true
                return
            }
            let ok = await Submission.requestAmbassador(city: place, token: token)
            sending = false
            if ok {
                asked = true
                sent = true
            } else {
                confirming = false
                navigator.snack = .init(text: "Your request did not send. Please try again in a moment.",
                                        symbol: "exclamationmark.circle")
            }
        }
    }
}

/// The ambassador explainer and its one button, then the receipt, on the one
/// sheet (Kit/BrandSheet.swift). The same three lines as the website's sheet,
/// in the same order, as rows rather than bullets on both.
struct AmbassadorApplySheet: View {
    let place: String
    let writeTo: String
    /// Bindings rather than values: a sheet's content can keep the value it
    /// was first drawn with, so the receipt step never appeared (2026-10-10).
    @Binding var sent: Bool
    @Binding var sending: Bool
    let apply: () -> Void
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        if sent {
            BrandSheet(
                icon: "checkmark",
                title: "Request sent",
                message: "We will email you soon with a few questions about the list." + writeTo,
                buttons: [.primary("Done", id: "ambassador-done") { dismiss() }])
        } else {
            BrandSheet(
                icon: "checkmark.seal",
                title: "Become the ambassador for \(place)",
                message: "An ambassador helps make this list as good as it can be.",
                points: ["Add photographs of the trees",
                         "Check the facts and tell us which trees are missing",
                         "Help put together walks past them"],
                buttons: [
                    .primary(sending ? "Sending" : "Apply", id: "ambassador-apply") { if !sending { apply() } },
                    .quiet("Not now") { dismiss() },
                ])
            // No address on this step (Hidde, 2026-10-10: "dont say we will
            // contact email - just only do it at the second overlay once
            // confirmed"): the receipt names it, once there is something to
            // write about.
        }
    }
}
