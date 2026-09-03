// A tree somebody else added, opened from their unlisted link.
//
// Convention: the website's own /t?id= page (site/src/pages/t/index.astro,
// Hidde, 2026-09-02: "kunnen we niet een pagina maken van de boom die wel
// deelbaar is?"). This is that page's app twin, read-only for the same
// reason the website one is: it is somebody else's tree, shown rather than
// editable. Reached from Route.shared(id) when the id is not one this
// device's own Sightings holds; when it is, ContentView's destination(_:_:)
// shows the real, editable TreeDetail instead, because there is no reason to
// give somebody a worse copy of their own page.
//
// WHAT IT DOES NOT SHOW: where the tree is. Hard rule 10 (CLAUDE.md) exists
// because a tree can be harmed by visitors and because somebody's garden is
// nobody's destination, and a tree a person photographed may be either. The
// public `shared_trees` view this reads never carries a coordinate, so there
// is nothing to withhold here by hand; the honesty is enforced upstream.

import SwiftUI

struct SharedTreeView: View {
    let id: UUID

    private enum LoadState {
        case loading, missing
        case found(name: String, species: String?, age: String?,
                   note: String?, photoURL: URL?, takenAt: Date?)
    }
    @State private var state: LoadState = .loading
    @Environment(Navigator.self) private var navigator

    var body: some View {
        ScrollView {
            switch state {
            case .loading:
                ProgressView().padding(.top, 80)
            case .missing:
                ContentUnavailableView("This link does not lead to a tree",
                    systemImage: "link.badge.plus",
                    description: Text("It may have been taken down by the person who shared it."))
                    .padding(.top, 40)
            case .found(let name, let species, let age, let note, let photoURL, let takenAt):
                VStack(alignment: .leading, spacing: 16) {
                    if let photoURL {
                        TreePhoto(url: photoURL, contentMode: .fill) {
                            Rectangle().fill(Brand.surfaceMuted)
                        }
                        .frame(height: 260)
                        .frame(maxWidth: .infinity)
                        .clipShape(.rect(cornerRadius: 18))
                    }
                    Text("A tree someone found")
                        .font(.brand(12, .semibold, relativeTo: .caption))
                        .foregroundStyle(Brand.inkSoft)
                        .textCase(.uppercase)
                    Text(name)
                        .font(.brand(28, .heavy))
                        .foregroundStyle(Brand.ink)
                    let chips = [species, age, takenAt.map { $0.formatted(date: .long, time: .omitted) }]
                        .compactMap { $0 }
                    if !chips.isEmpty {
                        HStack(spacing: 8) {
                            ForEach(chips, id: \.self) { Chip(text: $0) }
                        }
                    }
                    if let note, !note.isEmpty {
                        Text(note)
                            .font(.body)
                            .foregroundStyle(Brand.ink)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                    // NOT "get the app": whoever is reading this already has
                    // it open. The website's CTA is a download pitch because
                    // it has no other place to send a browser; here the same
                    // moment is one tab away.
                    Button {
                        navigator.selectTab = 0
                    } label: {
                        HStack { Spacer()
                            Text("Find the trees near you")
                                .font(.brand(17, .bold))
                            Spacer() }
                            .padding(.vertical, 15)
                            .background(Brand.moss, in: .rect(cornerRadius: 15))
                            .foregroundStyle(.white)
                    }
                    .buttonStyle(.plain)
                    .padding(.top, 8)
                }
                .padding(20)
            }
        }
        .task { await load() }
        .navigationTitle(displayTitle)
        .navigationBarTitleDisplayMode(.inline)
    }

    private var displayTitle: String {
        if case .found(let name, _, _, _, _, _) = state { return name }
        return "A tree"
    }

    private func load() async {
        let rows = await Supa.rows("/rest/v1/shared_trees?select=*&id=eq." + id.uuidString)
        guard let row = rows.first else { state = .missing; return }
        let name = (row["name"] as? String) ?? "A tree"
        let photo = (row["photo"] as? String).map { file in
            URL(string: Supa.url + "/storage/v1/object/public/shared-sightings/" + file)!
        }
        var takenAt: Date?
        if let raw = row["taken_at"] as? String {
            takenAt = ISO8601DateFormatter().date(from: raw)
        }
        state = .found(name: name, species: row["species"] as? String,
                       age: row["age"] as? String, note: row["note"] as? String,
                       photoURL: photo, takenAt: takenAt)
    }
}
