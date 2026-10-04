// The ambassador badge: one person looking after one place.
//
// Convention: komoot's Pioneer badge (CONVENTIONS.md 2026-10-02), a small seal
// beside the name on the person's own profile and contributions, tied to one
// region and earned by what they already did. Google's Local Guides badge is
// the same shape at level 4. Ours is Apple's checkmark.seal.fill (the website
// draws Phosphor's seal-check, its listed twin) in the moss pill the app
// already uses for a person's avatar, with the place's name. It is a label,
// never a button: nothing happens when it is tapped, exactly as on komoot.
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

    var body: some View {
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

#Preview {
    VStack(alignment: .leading, spacing: 12) {
        AmbassadorBadge(places: [.init(user_id: "u", place_slug: "paris", place_name: "Paris", public: false)])
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
                    Text(asked ? "Thanks, we'll write to you." : "Help us improve this list.")
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
            asked = await Submission.askedToBeAmbassador(city: place, token: await account.freshToken())
        }
        .sheet(isPresented: $signingIn) {
            SignInSheet(reason: .feedback, localCount: 0)
        }
    }

    private func tap() {
        guard account.isSignedIn else { signingIn = true; return }
        sending = true
        Task {
            let ok = await Submission.requestAmbassador(city: place, token: await account.freshToken())
            sending = false
            if ok { asked = true }
        }
    }
}
