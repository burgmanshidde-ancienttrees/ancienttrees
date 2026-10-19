// Somebody else's profile, when they made it public.
//
// Reference: Polarsteps' profile, and our own My trees (Collect.swift);
// CONVENTIONS.md, "A public profile, and the private switch" (2026-10-19).
// Hidde, 2026-10-19, on the design page: "ja dit ziet er goed uit", and on the
// two lists: "die kunnen gewoon gelijk blijven toch?". So this is My trees as a
// visitor sees it: picture, name and flag, the follow line, Follow where your
// own gear sits, the badges on their own row, then Collected and Want to visit
// as the same underlined tabs over the same three-across grid. The website's
// /profile?u= page is the same screen (site/src/pages/profile.astro).
//
// WHO MAY BE SEEN is the server's answer: public_profile() returns the
// profile only while its owner's Private profile switch is off. Private,
// unknown and unreachable all read the same, Instagram's "This account is
// private" in our words, under the name the person already shows in People.

import SwiftUI

struct PersonProfileView: View {
    let userId: String
    let catalogue: Catalogue

    @Environment(Profiles.self) private var profiles
    @Environment(Account.self) private var account

    private enum Lane { case seen, want }
    @State private var lane: Lane = .seen
    @State private var profile: Profiles.PublicProfile?
    @State private var loaded = false
    @State private var following = false
    @State private var followers = 0
    @State private var earlyAdopter = false
    @State private var signingIn = false
    /// The name the person already shows in People, for the private face.
    @State private var knownName: String?

    private static let tileShape = RoundedRectangle(cornerRadius: 12, style: .continuous)

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                header
                if let p = profile {
                    if !p.ambassador.isEmpty || earlyAdopter {
                        ViewThatFits(in: .horizontal) {
                            HStack(spacing: 6) { tags(p) }
                            VStack(alignment: .leading, spacing: 4) { tags(p) }
                        }
                    }
                    lanePicker
                    grid(p)
                } else if loaded {
                    Label("This profile is private.", systemImage: "lock")
                        .font(.callout).foregroundStyle(Brand.inkSoft)
                        .accessibilityIdentifier("person-private")
                }
            }
            .padding(.horizontal, 16).padding(.top, 8).padding(.bottom, 40)
        }
        .brandGround()
        // No bar title: the name is the header's, and a page that says its
        // own name twice is the "title twice" fault (Profile.swift).
        .navigationBarTitleDisplayMode(.inline)
        .sheet(isPresented: $signingIn) { SignInSheet(reason: .general, localCount: 0) }
        .task { await load() }
    }

    // MARK: - header, My trees' whoRow at the same numbers

    private var header: some View {
        HStack(spacing: 14) {
            ZStack {
                Circle().fill(Brand.moss.opacity(0.12))
                if let url = profile?.avatar_url, let u = URL(string: url) {
                    TreePhoto(url: u) { Color.clear }.clipShape(.circle)
                } else if let first = (profile?.display_name ?? knownName)?.first {
                    Text(String(first).uppercased())
                        .font(.brand(24, .black, relativeTo: .title3))
                        .foregroundStyle(Brand.moss)
                } else {
                    Image(systemName: "person.fill")
                        .font(.system(size: 24)).foregroundStyle(Brand.moss.opacity(0.6))
                }
            }
            .frame(width: 60, height: 60)
            .accessibilityHidden(true)

            VStack(alignment: .leading, spacing: 2) {
                HStack(alignment: .center, spacing: 8) {
                    Text(profile?.display_name ?? knownName ?? "")
                        .font(.brand(22, .bold, relativeTo: .title3))
                        .foregroundStyle(Brand.ink)
                        .lineLimit(1).truncationMode(.middle)
                    CountryFlag(code: profile?.country)
                }
                if profile != nil {
                    Text("**\(followers)** followers   **\(profile?.following ?? 0)** following")
                        .font(.footnote).foregroundStyle(Brand.inkSoft)
                        .lineLimit(1).minimumScaleFactor(0.8)
                }
            }
            Spacer(minLength: 8)
            if profile != nil && account.session?.userId != userId {
                followButton
            }
        }
    }

    /// People's pill, the same drawing (People.swift): filled while it says
    /// Follow, outlined once you do.
    private var followButton: some View {
        Button { toggle() } label: {
            Text(following ? "Following" : "Follow")
                .font(.subheadline.weight(.semibold))
                .foregroundStyle(following ? Brand.ink : .white)
                .padding(.horizontal, 14)
                .frame(minWidth: 96, minHeight: 34)
                .background(following ? Color.clear : Brand.moss, in: .capsule)
                .overlay { if following { Capsule().strokeBorder(Brand.hairline, lineWidth: 1) } }
                .frame(minHeight: 44)
                .contentShape(.rect)
        }
        .buttonStyle(.plain)
        .accessibilityIdentifier("person-profile-follow")
    }

    @ViewBuilder private func tags(_ p: Profiles.PublicProfile) -> some View {
        if !p.ambassador.isEmpty {
            AmbassadorBadge(places: p.ambassador.map {
                Profiles.Ambassador(user_id: p.user_id, place_slug: $0.lowercased(), place_name: $0, public: true)
            }, size: 13).fixedSize()
        }
        if earlyAdopter { EarlyAdopterBadge(size: 13).fixedSize() }
    }

    // MARK: - the two lists, Collect.swift's tabs and grid

    private var lanePicker: some View {
        HStack(spacing: 24) {
            laneTab("Collected", .seen, id: "person-lane-collected")
            laneTab("Want to visit", .want, id: "person-lane-want")
            Spacer(minLength: 0)
        }
        .overlay(alignment: .bottom) { Rectangle().fill(Brand.hairline).frame(height: 1) }
        .accessibilityElement(children: .contain)
    }

    private func laneTab(_ title: String, _ which: Lane, id: String) -> some View {
        let on = lane == which
        return Button { lane = which } label: {
            Text(title)
                .font(.system(size: 16, weight: .semibold))
                .foregroundStyle(on ? Brand.ink : Brand.inkSoft)
                .padding(.vertical, 12)
                .overlay(alignment: .bottom) { Rectangle().fill(on ? Brand.moss : .clear).frame(height: 2) }
                .contentShape(.rect)
        }
        .buttonStyle(.plain)
        .accessibilityAddTraits(on ? [.isSelected] : [])
        .accessibilityIdentifier(id)
    }

    @ViewBuilder private func grid(_ p: Profiles.PublicProfile) -> some View {
        let trees = (lane == .seen ? p.visited : p.saves).compactMap { catalogue.tree($0) }
        if trees.isEmpty {
            Text(lane == .seen ? "No trees collected yet." : "No trees saved yet.")
                .font(.subheadline).foregroundStyle(Brand.inkSoft)
        } else {
            LazyVGrid(columns: Array(repeating: GridItem(.flexible(), spacing: 6), count: 3), spacing: 6) {
                ForEach(trees) { t in
                    SheetLink(route: .tree(t.id)) {
                        CollectedTile(kind: .ours(t), city: t.city).clipShape(Self.tileShape)
                    }
                    .accessibilityIdentifier("tree-card")
                    .accessibilityLabel(t.name)
                }
            }
            .id(lane)
        }
    }

    // MARK: - data

    private func load() async {
        // The sweep's demo people need no token, and asking for one with the
        // fake -signed-in session signs it out, which pops this page.
        let token = DemoPeople.on ? nil : await account.freshToken()
        let p = await profiles.publicProfile(userId, token: token)
        profile = p
        followers = p?.followers ?? 0
        if p == nil {
            knownName = await profiles.byIds([userId], token: token).first?.display_name
                ?? DemoPeople.all.first(where: { $0.user_id == userId })?.display_name
        }
        loaded = true
        if let p { earlyAdopter = await EarlyAdopter.has(createdAt: p.created_at) }
        if let me = account.session?.userId, me != userId, !DemoPeople.on {
            following = await profiles.followingIds(of: me, token: token).contains(userId)
        }
    }

    /// People's toggle: the button moves first and goes back if refused.
    private func toggle() {
        guard let s = account.session else { signingIn = true; return }
        let was = following
        following.toggle()
        followers = max(0, followers + (was ? -1 : 1))
        if DemoPeople.on { return }
        Task {
            guard let t = await account.freshToken() else {
                following = was; followers = max(0, followers + (was ? 1 : -1)); signingIn = true; return
            }
            let ok = was
                ? await profiles.unfollow(userId, me: s.userId, token: t)
                : await profiles.follow(userId, me: s.userId, token: t)
            if !ok { following = was; followers = max(0, followers + (was ? 1 : -1)) }
        }
    }
}
