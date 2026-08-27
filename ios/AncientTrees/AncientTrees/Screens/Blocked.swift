// The people you have blocked, and the way back.
//
// A block you cannot undo is not a setting, it is a trap, and Apple's review
// looks for the undo as well as the block. This is the whole screen: who is on
// the list, and one button each.
//
// It shows a NAME wherever the server can still give one. The block list is
// ids, because that is what survives somebody renaming themselves, so the names
// are fetched when the screen opens. An account that has since been deleted has
// no profile left to fetch, and rather than an empty row it says so, because
// "somebody who is gone" is the honest description of what that block now is.

import SwiftUI

struct BlockedView: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(Account.self) private var account
    @Environment(Profiles.self) private var profiles
    @Environment(Moderation.self) private var moderation

    @State private var people: [Profiles.Profile] = []

    var body: some View {
        NavigationStack {
            List {
                if moderation.blocked.isEmpty {
                    Text("You have not blocked anybody.")
                        .font(.subheadline).foregroundStyle(Brand.inkSoft)
                }
                ForEach(Array(moderation.blocked).sorted(), id: \.self) { id in
                    HStack(spacing: 12) {
                        Text(people.first { $0.user_id == id }?.display_name
                             ?? "Somebody who is no longer here")
                            .font(.callout).foregroundStyle(Brand.ink)
                        Spacer(minLength: 8)
                        Button("Unblock") {
                            guard let s = account.session else { return }
                            Task { await moderation.unblock(id, me: s.userId, token: s.accessToken) }
                        }
                        .font(.subheadline.weight(.semibold))
                        .foregroundStyle(Brand.moss)
                        .buttonStyle(.plain)
                        .frame(minHeight: 44, alignment: .trailing)
                        .contentShape(.rect)
                    }
                }
            }
            .listStyle(.plain)
            .navigationTitle("Blocked people")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Done") { dismiss() }
                }
            }
            .task {
                people = await profiles.byIds(Array(moderation.blocked),
                                              token: account.session?.accessToken)
            }
        }
        .accessibilityIdentifier("blocked-sheet")
    }
}
