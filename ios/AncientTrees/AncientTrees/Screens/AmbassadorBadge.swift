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
