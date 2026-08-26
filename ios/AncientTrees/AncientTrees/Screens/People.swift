// Finding somebody, and following them.
//
// The button that opens this is the person-with-a-plus beside your own name,
// which is where Polarsteps puts it and where Hidde asked for it (2026-08-26:
// "hoe voeg ik vrienden toe"). Search by the name they chose is the only way
// in, deliberately: there is no browsing of everybody who ever signed up, and
// nothing here reveals an email address.
//
// WHAT FOLLOWING DOES TODAY, said plainly rather than implied: it counts. Your
// followers and following numbers move, and that is all, because saves are
// row-level-secured per person, so one account cannot read another's trees.
// Making collections visible to the people who follow you is one more decision
// about somebody else's data, and it is Hidde's to make rather than mine to
// assume.

import SwiftUI

struct PeopleView: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(Account.self) private var account
    @Environment(Profiles.self) private var profiles

    @State private var query = ""
    @State private var results: [Profiles.Profile] = []
    @State private var followingIds: Set<String> = []
    @State private var searching = false

    var body: some View {
        NavigationStack {
            List {
                if results.isEmpty && !query.isEmpty && !searching {
                    Text("Nobody by that name yet.")
                        .font(.subheadline).foregroundStyle(Brand.inkSoft)
                } else if results.isEmpty {
                    Text("Search for somebody by the name they chose.")
                        .font(.subheadline).foregroundStyle(Brand.inkSoft)
                }
                ForEach(results, id: \.user_id) { p in
                    HStack(spacing: 12) {
                        ZStack {
                            Circle().fill(Brand.moss.opacity(0.12))
                            if let url = p.avatar_url, let u = URL(string: url) {
                                AsyncImage(url: u) { $0.resizable().aspectRatio(contentMode: .fill) }
                                    placeholder: { Color.clear }
                                    .clipShape(.circle)
                            } else if let first = p.display_name.first {
                                Text(String(first).uppercased())
                                    .font(.brand(16, .black, relativeTo: .body))
                                    .foregroundStyle(Brand.moss)
                            }
                        }
                        .frame(width: 40, height: 40)

                        Text(p.display_name).font(.callout).foregroundStyle(Brand.ink)
                        Spacer(minLength: 8)

                        Button(followingIds.contains(p.user_id) ? "Following" : "Follow") {
                            toggle(p)
                        }
                        .font(.subheadline.weight(.semibold))
                        .foregroundStyle(followingIds.contains(p.user_id) ? Brand.inkSoft : Brand.moss)
                        .buttonStyle(.plain)
                        .frame(minWidth: 78, minHeight: 44, alignment: .trailing)
                        .contentShape(.rect)
                    }
                    .padding(.vertical, 2)
                }
            }
            .listStyle(.plain)
            .searchable(text: $query, prompt: "Search people")
            .navigationTitle("Find people")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Done") { dismiss() }
                }
            }
            .task(id: query) {
                // A beat before asking, so typing does not fire a request per
                // letter.
                searching = true
                try? await Task.sleep(for: .milliseconds(300))
                if Task.isCancelled { return }
                results = await profiles.search(query, token: account.session?.accessToken)
                searching = false
            }
        }
        .accessibilityIdentifier("people-sheet")
    }

    private func toggle(_ p: Profiles.Profile) {
        guard let s = account.session else { return }
        let wasFollowing = followingIds.contains(p.user_id)
        // Move the button first: a follow that waits on a round trip feels
        // broken, and the number beside your name catches up a moment later.
        if wasFollowing { followingIds.remove(p.user_id) } else { followingIds.insert(p.user_id) }
        Task {
            if wasFollowing {
                await profiles.unfollow(p.user_id, me: s.userId, token: s.accessToken)
            } else {
                await profiles.follow(p.user_id, me: s.userId, token: s.accessToken)
            }
        }
    }
}
