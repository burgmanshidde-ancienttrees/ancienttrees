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

    @Environment(Moderation.self) private var moderation

    @State private var query = ""
    @State private var results: [Profiles.Profile] = []
    @State private var followingIds: Set<String> = []
    @State private var searching = false
    /// Who the report-or-block sheet is about. One optional rather than a
    /// boolean and an id, so the sheet cannot be open about nobody.
    @State private var acting: Profiles.Profile?
    @State private var reporting: Profiles.Profile?
    @State private var reported = false

    /// Blocked people go to the BOTTOM rather than out of the list.
    ///
    /// Hidde removed the Blocked people screen on 2026-08-27 ("dat heb ik nog
    /// nooit als optie gezien in een app, haal maar weg"), and he is right that
    /// it is odd furniture on an app this social: Instagram and X have that
    /// list, Google Maps does not, and we are the second kind of app.
    ///
    /// What cannot go with it is the way back. Blocking is the only thing in
    /// this app that cannot be undone, and a block with no undo is a trap
    /// rather than a control. So a blocked person is not hidden from YOUR OWN
    /// search for them: they sit at the end, dimmed, with Unblock where Follow
    /// would be. They are still gone from everywhere else, which is what a
    /// block is for.
    private var visible: [Profiles.Profile] {
        results.filter { !moderation.hides($0.user_id) }
            + results.filter { moderation.hides($0.user_id) }
    }

    var body: some View {
        NavigationStack {
            List {
                if visible.isEmpty && !query.isEmpty && !searching {
                    Text("Nobody by that name yet.")
                        .font(.subheadline).foregroundStyle(Brand.inkSoft)
                } else if visible.isEmpty {
                    Text("Search for somebody by the name they chose.")
                        .font(.subheadline).foregroundStyle(Brand.inkSoft)
                }
                ForEach(visible, id: \.user_id) { p in
                    HStack(spacing: 12) {
                        ZStack {
                            Circle().fill(Brand.moss.opacity(0.12))
                            if let url = p.avatar_url, let u = URL(string: url) {
                                TreePhoto(url: u) { Color.clear }
                                    .clipShape(.circle)
                            } else if let first = p.display_name.first {
                                Text(String(first).uppercased())
                                    .font(.brand(16, .black, relativeTo: .body))
                                    .foregroundStyle(Brand.moss)
                            }
                        }
                        .frame(width: 40, height: 40)

                        Text(p.display_name).font(.callout)
                            .foregroundStyle(moderation.hides(p.user_id) ? Brand.inkSoft : Brand.ink)
                        Spacer(minLength: 8)

                        if moderation.hides(p.user_id) {
                            Button("Unblock") {
                                guard let s = account.session else { return }
                                Task {
                                    guard let t = await account.freshToken() else { return }
                                    await moderation.unblock(p.user_id, me: s.userId, token: t)
                                }
                            }
                            .font(.subheadline.weight(.semibold))
                            .foregroundStyle(Brand.moss)
                            .buttonStyle(.plain)
                            .frame(minWidth: 78, minHeight: 44, alignment: .trailing)
                            .contentShape(.rect)
                            .accessibilityIdentifier("person-unblock")
                        } else {
                            Button(followingIds.contains(p.user_id) ? "Following" : "Follow") {
                                toggle(p)
                            }
                            .font(.subheadline.weight(.semibold))
                            .foregroundStyle(followingIds.contains(p.user_id) ? Brand.inkSoft : Brand.moss)
                            .buttonStyle(.plain)
                            .frame(minWidth: 78, minHeight: 44, alignment: .trailing)
                            .contentShape(.rect)
                        }

                        // THE ELLIPSIS, and it is not decoration. From the
                        // moment somebody can see a name and a picture another
                        // person chose, App Store guideline 1.2 asks for a way
                        // to report it and a way to block them, and a reviewer
                        // checks by looking for exactly this control. Every app
                        // with profiles puts it in the same place: trailing, on
                        // the row or on the profile, opening a short sheet.
                        Button { acting = p } label: {
                            Image(systemName: "ellipsis")
                                .font(.system(size: 15, weight: .semibold))
                                .foregroundStyle(Brand.inkSoft)
                                .frame(width: 44, height: 44)
                                .contentShape(.rect)
                        }
                        .buttonStyle(.plain)
                        .accessibilityLabel("More about \(p.display_name)")
                        .accessibilityIdentifier("person-more")
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
            .confirmationDialog(acting?.display_name ?? "",
                                isPresented: Binding(get: { acting != nil },
                                                     set: { if !$0 { acting = nil } }),
                                titleVisibility: .visible) {
                Button("Report this person") {
                    reporting = acting
                }
                Button(acting.map { moderation.hides($0.user_id) } == true
                       ? "Unblock this person" : "Block this person",
                       role: acting.map { moderation.hides($0.user_id) } == true ? nil : .destructive) {
                    guard let p = acting, let s = account.session else { return }
                    Task {
                        // A token that is still good: see Account.freshToken.
                        guard let t = await account.freshToken() else { return }
                        if moderation.hides(p.user_id) {
                            await moderation.unblock(p.user_id, me: s.userId, token: t)
                        } else {
                            await moderation.block(p.user_id, me: s.userId, token: t)
                        }
                    }
                }
                Button("Cancel", role: .cancel) {}
            } message: {
                Text("Blocking hides them from you, and neither of you follows the other any more.")
            }
            // The reasons, as their own sheet rather than a text field. A field
            // asks somebody to write an essay about an offensive picture; four
            // buttons take one tap, which is what Apple's own report sheets do.
            .confirmationDialog("Why are you reporting this?",
                                isPresented: Binding(get: { reporting != nil },
                                                     set: { if !$0 { reporting = nil } }),
                                titleVisibility: .visible) {
                ForEach(Moderation.Reason.allCases) { r in
                    Button(r.rawValue) { send(r) }
                }
                Button("Cancel", role: .cancel) {}
            }
            .alert("Thank you", isPresented: $reported) {
                Button("OK", role: .cancel) {}
            } message: {
                Text("We look at every report. If you would rather not see this person at all, block them too.")
            }
            .task {
                // Debug scaffolding, the same family as -tab and -signed-in:
                // this list needs a live database with strangers in it, so
                // without three made-up rows the report and block controls
                // cannot be photographed or looked at before they ship, and a
                // control nobody has looked at is exactly what this project
                // keeps promising not to ship.
                if DemoPeople.on { results = DemoPeople.all }
            }
            .task(id: query) {
                if DemoPeople.on { return }
                // A beat before asking, so typing does not fire a request per
                // letter.
                searching = true
                try? await Task.sleep(for: .milliseconds(300))
                if Task.isCancelled { return }
                results = await profiles.search(query, token: await account.freshToken())
                searching = false
            }
        }
        .accessibilityIdentifier("people-sheet")
    }

    /// Send the report, and say so. The row stays where it is: reporting is
    /// not blocking, and doing both silently would take a choice away from the
    /// person who only wanted to flag something.
    private func send(_ reason: Moderation.Reason) {
        guard let p = reporting, let s = account.session else { return }
        Task {
            guard let t = await account.freshToken() else { return }
            _ = await moderation.report(subject: p.user_id, reason: reason.rawValue,
                                        reporter: s.userId, token: t)
            reported = true
        }
    }

    private func toggle(_ p: Profiles.Profile) {
        guard let s = account.session else { return }
        let wasFollowing = followingIds.contains(p.user_id)
        // Move the button first: a follow that waits on a round trip feels
        // broken, and the number beside your name catches up a moment later.
        if wasFollowing { followingIds.remove(p.user_id) } else { followingIds.insert(p.user_id) }
        Task {
            guard let t = await account.freshToken() else { return }
            if wasFollowing {
                await profiles.unfollow(p.user_id, me: s.userId, token: t)
            } else {
                await profiles.follow(p.user_id, me: s.userId, token: t)
            }
        }
    }
}
