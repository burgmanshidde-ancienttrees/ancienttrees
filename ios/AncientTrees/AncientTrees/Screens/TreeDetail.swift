// One tree, and the two actions that matter under it.
//
// The action bar is pinned to the bottom and does not scroll away, which is the
// sharpest thing the AllTrails teardown found: their `Begin` is not merely under
// the elevation chart, it is fixed to the bottom of the phone everywhere the
// route exists. `directions` fired zero times on our website, where the button
// lives at the end of a story somebody has to scroll through.

import SwiftUI
import MapKit

struct TreeDetail: View {
    let tree: Tree
    /// Set when this page is showing a tree only YOU have. The same page, with
    /// the fields you have not filled in yet open for you to fill (Hidde,
    /// 2026-08-24: "het is dezelfde boom pagina als onze bomen alleen dan dat
    /// de eindgebruiker de velden kan invullen"). A second screen for your own
    /// trees would drift from this one inside a week.
    var mine: Sightings.Sighting? = nil
    let catalogue: Catalogue
    /// Where the phone thinks it is, for the walking view. Defaults to the
    /// tree itself, which is honest when nobody has given us a location: the
    /// line is then zero long rather than wrong.
    var origin: (lat: Double, lng: Double)? = nil
    @Environment(Saved.self) private var saved
    @Environment(Sightings.self) private var sightings
    @State private var editing: EditableField?
    @Environment(Account.self) private var account
    @Environment(Nudge.self) private var nudge
    @State private var reporting = false
    @State private var walking = false
    @Environment(Navigator.self) private var navigator

    var body: some View {
        ZStack(alignment: .bottom) {
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    hero
                    header
                    facts
                    if tree.precision.needsWarning { approximateNote }
                    // High on the page, under the facts, because it is a
                    // question about the thing the facts just described
                    // (Hidde, 2026-08-21).
                    // Not on your own tree: a vote on whether YOUR tree is
                    // worth the visit is a question to nobody, and the access
                    // and transport lines are ours to research, not blanks for
                    // you to fill about a tree you already stood at.
                    if mine == nil { WorthItView(tree: tree) }
                    story
                    if mine == nil { accessBlock }
                    if mine == nil, tree.photo == nil { offerPhoto }
                    if mine != nil { mineFooter }
                    // "Report a problem" used to sit here and open the generic
                    // contribute form, which greeted somebody who wanted to
                    // report a wrong pin with a picker whose first row reads "A
                    // tree we are missing" and three empty fields asking which
                    // place and which tree (Hidde, 2026-08-25: "die flow loopt
                    // totaal niet"). It was also the second report control on
                    // one page: WorthItView above already carries "Something's
                    // wrong" and the five chips that name what is actually
                    // wrong, which is the flow the website runs and the one a
                    // run can act on. One page, one way to say it.
                    // Last line on the page, and only where the licence asks
                    // for it. CC BY and BY-SA oblige a credit; CC0 and public
                    // domain do not and get none. Moving it here is allowed
                    // ("in any reasonable manner"), removing it is not.
                    if let p = tree.photo, let c = Photos.credit(p) {
                        Text(c)
                            .font(.system(size: 10))
                            .foregroundStyle(Brand.inkSoft.opacity(0.45))
                            .lineLimit(1)
                    }
                    Color.clear.frame(height: 90)   // room for the pinned bar
                }
                .padding(.horizontal, 20)
                .padding(.top, 8)
            }
            actionBar
        }
        .brandGround()
        // The name renders once, in the body's own heading; a second copy in
        // the bar was the "title twice" mess from the findings list.
        .navigationTitle("")
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            // Only ours can be shared: a tree only you have has no address on
            // the web to send anybody to, and inventing one would send them to
            // a 404. It gets a share button the day these get a page.
            if mine == nil {
                    ShareTo(url: URL(string: "https://ancienttrees.app" + tree.url)!,
                        subject: tree.name,
                        message: "\(tree.name), \(tree.city).",
                        label: "Share this tree")
            }
        }
        .sheet(isPresented: $reporting) { ContributeView(about: tree) }
        .sheet(item: $editing) { editor($0) }
        .task {
            // Debug scaffolding, same family as -tab, -select and -collected:
            // simctl cannot tap, and a screen that only exists after a tap is a
            // screen that ships unlooked at.
            if ProcessInfo.processInfo.arguments.contains("-walkto") { walking = true }
        }
        .fullScreenCover(isPresented: $walking) {
            // The tree itself, not its id: a tree you added is not in the
            // catalogue, so looking it up gave an empty walk (2026-08-25).
            WalkMode(walk: Self.oneTreeWalk(tree), only: [tree], catalogue: catalogue,
                     origin: origin ?? (tree.lat, tree.lng))
        }
    }

    /// The photograph, or the species drawn, edge to edge. AllTrails leads every
    /// route with a picture and it is most of why their pages feel like an
    /// invitation rather than a database record.
    ///
    /// The credit sits UNDER it rather than painted across it.
    ///
    /// This is the only place the attribution appears now, which is deliberate:
    /// cards stopped carrying it on 2026-08-20 because a dark chip over the
    /// trunk is the one thing on a card that is not the tree. A CC BY or BY-SA
    /// licence obliges a credit and this is it, in the ordinary place a caption
    /// goes, which is also what every image search and Wikipedia's own apps do.
    @ViewBuilder private var hero: some View {
        if let m = mine, let shot = sightings.image(m) {
            // Your own photograph, from Documents rather than the network. The
            // same empty box with the picture laid over it as below, for the
            // same reason: an unbounded image drags the whole page sideways.
            Color.clear
                .frame(height: 240)
                .overlay {
                    Image(uiImage: shot).resizable().aspectRatio(contentMode: .fill)
                }
                .clipShape(.rect(cornerRadius: 16))
        } else if let p = tree.photo, let url = Photos.thumb(p.url, width: 960) {
            VStack(alignment: .leading, spacing: 6) {
                // AN EMPTY BOX WITH THE PHOTOGRAPH LAID OVER IT, not a
                // photograph with a height. A .fill image asks for the width
                // its own picture wants (a landscape shot 240 points tall asks
                // for about 410) and everything around it grows to match: on a
                // 375 point phone the whole tree page sat 19.5 points to the
                // left, the photograph against the left edge and the heart
                // button hanging off the right. One unbounded image moved every
                // element on the screen, and adding maxWidth did not fix it,
                // because a frame's maximum still yields to the image's ideal.
                // An overlay never takes part in layout at all, which is the
                // only version that cannot do this again.
                Color.clear
                    .frame(height: 240)
                    .overlay {
                        AsyncImage(url: url) { img in
                            img.resizable().aspectRatio(contentMode: .fill)
                        } placeholder: {
                            heroFallback
                        }
                    }
                    .clipped()
                    .clipShape(.rect(cornerRadius: 14))
                    // The way to the map, in the corner a card already trained
                    // people to look at. It replaces the 150 point map card
                    // that used to sit between the facts and the story and
                    // pushed the whole story below the fold.
                    .overlay(alignment: .bottomTrailing) {
                        Button { navigator.showOnMap = tree.id } label: {
                            MapInset(lat: tree.lat, lng: tree.lng).padding(10)
                        }
                        .buttonStyle(.plain)
                        .accessibilityLabel("Show this tree on the map")
                    }

            }
        } else {
            heroFallback.frame(height: 200).clipShape(.rect(cornerRadius: 14))
                .overlay(alignment: .bottomTrailing) {
                    Button { navigator.showOnMap = tree.id } label: {
                        MapInset(lat: tree.lat, lng: tree.lng).padding(10)
                    }
                    .buttonStyle(.plain)
                    .accessibilityLabel("Show this tree on the map")
                }
        }
    }

    /// The tree, and whatever else of ours is within a few streets, because the
    /// second most useful thing after "where is it" is "is it worth the trip on
    /// its own or are there three more round the corner".
    private var nearbyTrees: [Tree] {
        catalogue.nearest(to: tree.lat, tree.lng, limit: 8, withinKm: 0.5).map(\.tree)
    }

    private var heroFallback: some View {
        ZStack {
            LinearGradient(colors: [Color(red: 0.20, green: 0.35, blue: 0.20),
                                    Color(red: 0.36, green: 0.49, blue: 0.31)],
                           startPoint: .topLeading, endPoint: .bottomTrailing)
            VStack(spacing: 10) {
                SpeciesMark(species: tree.species, color: .white.opacity(0.9))
                    .frame(width: 78, height: 78)
                Text("No photograph of this tree yet.")
                    .font(.caption2).foregroundStyle(.white.opacity(0.8))
                    .multilineTextAlignment(.center).padding(.horizontal, 28)
            }
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(tree.name)
                .font(.brand(30, .bold, relativeTo: .largeTitle))
                .foregroundStyle(Brand.ink)
            if tree.species.isEmpty, mine != nil {
                blank("What kind of tree is it?", .species)
            } else {
                Text(tree.species).font(.subheadline).foregroundStyle(Brand.inkSoft)
            }
            // WHERE it is, with the width of the page to say it in.
            //
            // It used to be the middle column of the stat row, where "Plantage,
            // Amsterdam-Centrum" became "Plantage, Amsterdam-C..." A stat row
            // holds numbers: AllTrails puts length, ascent and time in theirs,
            // and a place name is a phrase, not a number.
            if mine != nil {
                // Where YOU stood. No district, no city, because nobody has
                // told us one and inventing it is the one thing a location
                // field may never do.
                Text("Where you photographed it")
                    .font(.subheadline).foregroundStyle(Brand.inkSoft)
            } else {
                Text(place).font(.subheadline).foregroundStyle(Brand.inkSoft)
                    .lineLimit(1)
            }
        }
    }

    private var place: String {
        let n = tree.neighbourhood.trimmingCharacters(in: .whitespaces)
        guard !n.isEmpty else { return tree.city }
        // Many registers write the district as "Amsterdam-Centrum", so adding
        // the city gives "Plantage, Amsterdam-Centrum, Amsterdam".
        return n.localizedCaseInsensitiveContains(tree.city) ? n : "\(n), \(tree.city)"
    }

    /// Four facts with their units labelled, the way AllTrails does it and the
    /// way our own website already does on a tree page.
    /// The number, where the feed has one, so the row holds a figure rather
    /// than a hedged sentence. The full wording is in the story.
    private var shortAge: String {
        if let lo = tree.ageMin, lo > 0 {
            if let hi = tree.ageMax, hi > lo { return "\(lo)-\(hi) years" }
            return "\(lo) years"
        }
        return tree.age ?? (mine != nil ? "Add it" : "not recorded")
    }

    private var facts: some View {
        HStack(alignment: .top, spacing: 0) {
            if mine != nil, tree.age == nil {
                Button { editing = .age } label: { fact("Add it", "Age") }
                    .buttonStyle(.plain)
            } else {
                fact(shortAge, "Age")
            }
            Divider().frame(height: 34)
            fact(tree.precision == .confirmed ? "Exact" : "Approximate", "Pin")
        }
        .padding(.vertical, 14)
        .frame(maxWidth: .infinity)
        .brandCard(14)
    }

    private func fact(_ value: String, _ label: String) -> some View {
        // Leading, not centred: a centred value starts wherever its width
        // puts it, so "up to 1,500 years" sat seven points right of the card
        // edge and the layout gate read it as a drift. The fourteen matches
        // the card's own inset elsewhere on the page.
        VStack(alignment: .leading, spacing: 3) {
            Text(value).font(.brand(14, .bold, relativeTo: .footnote))
                .foregroundStyle(Brand.ink).multilineTextAlignment(.leading)
                .lineLimit(2).minimumScaleFactor(0.8)
            Text(label).font(.caption2).foregroundStyle(Brand.inkSoft)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(.horizontal, 14)
    }

    /// A walk of one, so the mode built for several can carry a single tree.
    ///
    /// A synthesised Walk rather than a second screen: everything Begin does
    /// (your dot, the line, the metres counting down, the tick when you arrive)
    /// is what somebody walking to one tree wants too, and a copy of it would
    /// drift.
    static func oneTreeWalk(_ t: Tree) -> Walk {
        Walk(city: t.city, citySlug: t.citySlug, name: t.name, trees: [t.id],
             count: 1, km: 0, minutes: 0, duration: "", combined: false, shape: nil)
    }

    /// One sheet for every blank, because four sheets that differ by a
    /// placeholder is four places for them to drift apart.
    private func editor(_ field: EditableField) -> some View {
        FieldEditor(field: field,
                    initial: current(field),
                    onSave: { text in
                        guard let m = mine else { return }
                        switch field {
                        case .name: sightings.update(m.id, name: text)
                        case .species: sightings.update(m.id, species: text)
                        case .age: sightings.update(m.id, age: text)
                        case .story: sightings.update(m.id, note: text)
                        }
                        editing = nil
                    },
                    onCancel: { editing = nil })
    }

    private func current(_ field: EditableField) -> String {
        switch field {
        case .name: tree.name
        case .species: tree.species
        case .age: tree.age ?? ""
        case .story: tree.story
        }
    }

    /// A field on your own tree that nobody has filled in yet.
    enum EditableField: String, Identifiable {
        case name, species, age, story
        var id: String { rawValue }

        var prompt: String {
            switch self {
            case .name: "What do you call it?"
            case .species: "What kind of tree is it?"
            case .age: "How old is it, roughly?"
            case .story: "What makes it worth the walk?"
            }
        }

        /// Long answers get room; a species or an age is one line.
        var long: Bool { self == .story }
    }

    /// An empty field, offered rather than hidden. The green says it is
    /// yours to fill; a grey dash would read as missing data on our side.
    private func blank(_ label: String, _ field: EditableField) -> some View {
        Button { editing = field } label: {
            HStack(spacing: 5) {
                Image(systemName: "plus.circle")
                Text(label)
            }
            .font(.subheadline)
            .foregroundStyle(Brand.moss)
            .frame(minHeight: 44)
            .contentShape(.rect)
        }
        .buttonStyle(.plain)
    }

    /// The one warning this product must never soften. An approximate pin that
    /// says so sends somebody to the right park knowing they will have to look;
    /// one that pretends to be exact sends them to a spot where the tree is not.
    private var approximateNote: some View {
        VStack(alignment: .leading, spacing: 8) {
            Label {
                Text("This pin marks the area, not the trunk. You may have to look around once you are there.")
            } icon: {
                Image(systemName: "scope")
            }
            .font(.footnote)
            // The ask belongs here rather than three screens away: the person
            // reading this line is the one person who can answer it, and
            // location is the field this project cannot afford to get wrong.
            Button { reporting = true } label: {
                Text("Help us place this tree")
                    .font(.footnote.weight(.semibold))
                    .foregroundStyle(Brand.moss)
                    .frame(minHeight: 44)
                    .contentShape(.rect)
            }
            .buttonStyle(.plain)
        }
        .padding(12)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color.orange.opacity(0.12), in: .rect(cornerRadius: 10))
    }

    /// Whole, always. It used to stop at six lines behind a "read the whole
    /// story" button, which is a paywall made of nothing: the story IS the
    /// page, and with the map card gone there is room for it (Hidde,
    /// 2026-08-21: "your text can go up, so you can put the whole story there
    /// instead of putting that behind the button").
    private var story: some View {
        Group {
            if tree.story.isEmpty, mine != nil {
                blank("What makes it worth the walk?", .story)
            } else {
                Text(tree.story)
                    .fixedSize(horizontal: false, vertical: true)
            }
        }
    }

    /// What happens to a tree you added, said plainly on its own page.
    ///
    /// There is no CHOICE about it any more (Hidde, 2026-08-24: "hij komt
    /// uberhaupt automatisch bij ons terecht of ze het willen of niet en dan
    /// kiezen wij of die het waard is"), so the honest thing is to say so here
    /// rather than to ask twice.
    @ViewBuilder private var mineFooter: some View {
        if let m = mine {
            HStack(alignment: .top, spacing: 8) {
                Image(systemName: m.status == .published ? "checkmark.seal" : "leaf")
                    .foregroundStyle(Brand.moss)
                Text(m.status == .published
                     ? "This one made the map everybody sees."
                     // His own sentence, verbatim (2026-08-25). What it
                     // replaced said "This tree is yours. We have it too",
                     // which reads as a boast about our own database at the
                     // moment somebody has just given us something, and it
                     // never said what happens next. The reader is the subject
                     // here and the next step is named.
                     : "You've added this tree. We're taking a look at it, and once it's verified, we will add it to our map.")
                    .font(.footnote).foregroundStyle(Brand.inkSoft)
                    .fixedSize(horizontal: false, vertical: true)
            }
            .padding(.top, 2)
        }
    }

    private var accessBlock: some View {
        VStack(alignment: .leading, spacing: 10) {
            Label(tree.access, systemImage: "figure.walk")
            Label(tree.transport, systemImage: "tram.fill")
        }
        .font(.footnote)
        .foregroundStyle(.secondary)
    }

    /// The highest-intent moment there is for this feature: you are on a tree
    /// with no photograph, and 1077 of our 1435 trees are in that state. Asking
    /// here beats a row in settings, and it measures demand for the feature
    /// exactly where somebody would use it.
    private var offerPhoto: some View {
        LockedRow(feature: .photoUpload) {
            HStack(alignment: .top, spacing: 12) {
                SpeciesMark(species: tree.species,
                            color: Color(red: 0.20, green: 0.35, blue: 0.20).opacity(0.55))
                    .frame(width: 34, height: 34)
                VStack(alignment: .leading, spacing: 3) {
                    Text("Nobody has photographed this one")
                        .font(.brand(16, .bold, relativeTo: .subheadline))
                        .foregroundStyle(Brand.ink)
                    Text("If you are standing in front of it, yours could be the picture on this page.")
                        .font(.caption).foregroundStyle(.secondary)
                }
            }
            .padding(.vertical, 4)
        }
        .padding(14)
        .frame(maxWidth: .infinity, alignment: .leading)
        .brandCard(12)
    }

    private var actionBar: some View {
        HStack(spacing: 10) {
            // OUR walking view, not somebody else's app.
            //
            // Hidde, 2026-08-24: "waarom stuurt ie je dan naar een andere app
            // als je in de app kan navigeren." No reason: Begin arrived later
            // and this button never came with it, so a walk kept you and a
            // single tree handed you away. AllTrails draws the same line we do
            // now: in-app for the trail itself, and a hand-off only for
            // street-by-street, which lives one level in.
            Button { walking = true } label: {
                Label("Take me there", systemImage: "location.fill")
            }
            .buttonStyle(BrandButtonStyle())

            SaveHeart(tree: tree, look: .inBar)
        }
        // The same 20 as the page's content above it; at 16 the bar began
        // four points left of every paragraph, which is the drift the layout
        // gate exists to catch.
        .padding(.horizontal, 20)
        .padding(.bottom, 8)
        .padding(.top, 10)
        // Opaque, with a short fade above it. At 96 percent the story showed
        // through the bar as ghost text, which reads as a rendering fault
        // rather than as translucency.
        .background(alignment: .top) {
            VStack(spacing: 0) {
                LinearGradient(colors: [Brand.ground.opacity(0), Brand.ground],
                               startPoint: .top, endPoint: .bottom)
                    .frame(height: 18)
                Brand.ground
            }
            .ignoresSafeArea(edges: .bottom)
        }
    }
}

/// The one editor behind every blank on a tree of your own.
///
/// Deliberately dull: a title, a field, Cancel and Save. Nothing here is a new
/// interaction, because filling in a text field is the most settled thing in
/// software and inventing a version of it would be the third time in one day.
struct FieldEditor: View {
    let field: TreeDetail.EditableField
    let initial: String
    let onSave: (String) -> Void
    let onCancel: () -> Void

    @State private var text: String = ""
    @FocusState private var focused: Bool

    var body: some View {
        NavigationStack {
            VStack(alignment: .leading, spacing: 12) {
                if field.long {
                    TextField(field.prompt, text: $text, axis: .vertical)
                        .lineLimit(4...10)
                        .focused($focused)
                } else {
                    TextField(field.prompt, text: $text)
                        .focused($focused)
                }
                Spacer()
            }
            .padding(16)
            .navigationTitle(field.prompt)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { onCancel() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        onSave(text.trimmingCharacters(in: .whitespacesAndNewlines))
                    }
                }
            }
        }
        .presentationDetents(field.long ? [.medium, .large] : [.height(220)])
        .onAppear { text = initial; focused = true }
    }
}
