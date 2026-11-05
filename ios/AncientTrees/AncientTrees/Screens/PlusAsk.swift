// THE ANCIENT TREES PLUS QUESTION (Hidde, 2026-11-04: "het ziet er eigenlijk
// goed uit zo bouw maar"). Nothing is sold and no price is shown; it asks.
//
// Reference: CONVENTIONS.md, "Where the paywall sits ..." and its 2026-11-04
// addendum. The website draws the same three steps (PlusAsk.astro):
//   1. the OPEN question first, before any option is shown (anchoring);
//   2. ONE choice of four, shuffled per person, "None of these" last;
//   3. "Tell me", the only step that needs an account.
// Two ways in: a row under the ambassador on a city (the map's place header),
// and a row in Settings' Help card. A row, not a card: "a promise belongs in a
// settings row" (Hidde, 2026-08-25, when the old Plus card left Settings).

import SwiftUI

/// The row on a city, the same shape as the ambassador's (AmbassadorBadge.swift):
/// a 32-point circle, the name at 14 bold, one line at 12, a chevron.
struct PlusRow: View {
    let city: String
    @State private var asking = false

    var body: some View {
        // A tap, not a Button: this row sits in the map's sheet header, the
        // handle a thumb raises the sheet by (BottomSheet sheetTap).
        // ONE LINE (Hidde, 2026-11-05, direction C): the second row of the
        // place's white box, under the ambassador; the website's PlusAsk.astro
        // draws the same line.
        // One icon column with the ambassador row above it: 30 wide, 12 to
        // the words, so "Hugo" and this line start at the same x.
        HStack(spacing: 12) {
                Image(systemName: "sparkles")
                    .font(.system(size: 15, weight: .semibold))
                    .foregroundStyle(Brand.moss)
                    .frame(width: 34)
                Text("Help create Ancient Trees Plus")
                    .font(.system(size: 15, weight: .medium))
                    .foregroundStyle(Brand.ink)
                Spacer(minLength: 8)
                Image(systemName: "chevron.right")
                    .font(.caption.weight(.semibold))
                    .foregroundStyle(Brand.inkSoft.opacity(0.6))
            }
            .padding(.horizontal, 14)
            .frame(minHeight: 46)
            .sheetTap {
                Measure.event("plus-open", ["from": "city"])
                asking = true
            }
        .accessibilityIdentifier("plus-row")
        .sheet(isPresented: $asking) { PlusQuestionSheet(city: city, openedFrom: "city") }
    }
}

/// The three steps on the one sheet (Kit/BrandSheet.swift).
struct PlusQuestionSheet: View {
    let city: String
    let openedFrom: String
    enum Step { case idea, choice, thanks, listed }

    @Environment(Account.self) private var account
    @Environment(\.dismiss) private var dismiss
    @State private var step: Step = .idea
    @State private var idea = ""
    /// What "Something else" says (Hidde, 2026-11-05).
    @State private var otherText = ""
    /// Up to two (Hidde, 2026-11-05: "max 2 invullen is goed"); "none" alone.
    @State private var choices: [String] = []
    @State private var order: [(key: String, label: String)] = PlusAnswers.options.shuffled()
    @State private var signingIn = false
    @State private var joining = false

    var body: some View {
        content
            .task {
                // A sheet no argument can open ships unseen (2026-10-10):
                // -pluschoice and -plusthanks open the later steps.
                let args = ProcessInfo.processInfo.arguments
                if args.contains("-pluschoice") { step = .choice }
                if args.contains("-plusthanks") { step = .thanks }
            }
            // Sign in, then back to this step; nothing is pressed for them.
            .sheet(isPresented: $signingIn, onDismiss: { if account.isSignedIn { join() } }) {
                SignInSheet(reason: .feedback)
            }
    }

    @ViewBuilder private var content: some View {
        switch step {
        case .idea:
            BrandSheet(icon: "sparkles", title: "Ancient Trees Plus",
                       message: "We're working on Plus to make Ancient Trees a sustainable platform. What would you like it to do that it doesn't do yet?",
                       // Skip while the field is empty, so leaving it is plainly
                       // allowed (Hidde, 2026-11-05: "ik zou hier wel op vastlopen"),
                       // as the quiet way out; green only once there is
                       // something to send on.
                       buttons: [idea.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
                                 ? .quiet("Skip", id: "plus-next") { step = .choice }
                                 : .primary("Next", id: "plus-next") { step = .choice }],
                       extra: { ideaField })
                .accessibilityIdentifier("plus-sheet")
        case .choice:
            BrandSheet(title: "Which would you want most?", message: "Pick up to two.",
                       buttons: [.primary("Send", id: "plus-send") { send() }],
                       extra: { options })
                .accessibilityIdentifier("plus-sheet")
        case .thanks:
            BrandSheet(icon: "checkmark", title: "Thank you",
                       message: "Want us to tell you when it's here?",
                       buttons: [.primary(joining ? "Sending" : "Tell me", id: "plus-tellme") { tellMe() },
                                 .secondary("No thanks", id: "plus-nothanks") { dismiss() }])
                .accessibilityIdentifier("plus-sheet")
        case .listed:
            BrandSheet(icon: "checkmark", title: "You're on the list",
                       buttons: [.primary("Done", id: "plus-done") { dismiss() }])
                .accessibilityIdentifier("plus-sheet")
        }
    }

    /// The note field's numbers (TreeDetail.swift, noteFields).
    private var ideaField: some View {
        ZStack(alignment: .topLeading) {
            TextEditor(text: $idea)
                .font(.system(size: 16))
                .scrollContentBackground(.hidden)
                .frame(minHeight: 104)
                .padding(.horizontal, 10).padding(.vertical, 8)
                .background(Brand.surfaceMuted, in: .rect(cornerRadius: 14))
                .accessibilityIdentifier("plus-idea")
            if idea.isEmpty {
                Text("I'd like to…")
                    .font(.system(size: 16))
                    .foregroundStyle(Brand.inkSoft.opacity(0.7))
                    .padding(.horizontal, 15).padding(.vertical, 16)
                    .allowsHitTesting(false)
            }
        }
        .padding(.top, 20)
    }

    private var options: some View {
        VStack(spacing: 8) {
            ForEach(order, id: \.key) { o in optionRow(o.key, o.label) }
            // SOMETHING ELSE, then a field (Hidde, 2026-11-05: "de optie
            // something else en dat iemand dan kan gaan typen"): a survey's
            // "Other, please specify", as Google Forms draws it; the field
            // appears only once it is ticked. It counts as one of the two.
            optionRow("other", "Something else")
            if choices.contains("other") {
                TextField("What would you want?", text: $otherText, axis: .vertical)
                    .font(.system(size: 16))
                    .lineLimit(1...4)
                    .padding(.horizontal, 14).padding(.vertical, 12)
                    .background(Brand.surfaceMuted, in: .rect(cornerRadius: 14))
                    .accessibilityIdentifier("plus-other-text")
            }
            optionRow("none", "None of these", quiet: true)
        }
        .padding(.top, 20)
    }

    private func optionRow(_ key: String, _ label: String, quiet: Bool = false) -> some View {
        let on = choices.contains(key)
        let full = !on && choices.count >= 2 && key != "none" && !choices.contains("none")
        return Button { toggle(key) } label: {
            HStack(spacing: 12) {
                Image(systemName: on ? "checkmark.circle.fill" : "circle")
                    .font(.system(size: 20))
                    .foregroundStyle(on ? Brand.moss : Brand.inkSoft.opacity(0.5))
                Text(label)
                    .font(.system(size: 15))
                    .foregroundStyle(quiet ? Brand.inkSoft : Brand.ink)
                    .multilineTextAlignment(.leading)
                    .fixedSize(horizontal: false, vertical: true)
                Spacer(minLength: 0)
            }
            .padding(.horizontal, 14).padding(.vertical, 13)
            .background(on ? Brand.surfaceMuted : .clear, in: .rect(cornerRadius: 14))
            .overlay(RoundedRectangle(cornerRadius: 14).strokeBorder(on ? Brand.ink : Brand.inkSoft.opacity(0.2)))
            .contentShape(.rect)
        }
        .buttonStyle(.plain)
        .opacity(full ? 0.45 : 1)
        .disabled(full)
        .accessibilityAddTraits(on ? .isSelected : [])
        .accessibilityIdentifier("plus-option-\(key)")
    }

    /// "None of these" stands alone: ticking it clears the others, ticking
    /// another clears it; at two the rest wait greyed out (as the website).
    private func toggle(_ key: String) {
        if let i = choices.firstIndex(of: key) { choices.remove(at: i); return }
        if key == "none" { choices = ["none"]; return }
        choices.removeAll { $0 == "none" }
        if choices.count < 2 { choices.append(key) }
    }

    private func send() {
        guard !choices.isEmpty else { return }
        let picked = choices, shown = order.map(\.key)
        let text = idea, city = city, from = openedFrom
        let other = picked.contains("other") ? otherText : ""
        Measure.event("plus-answer", ["choice": picked.joined(separator: ",")])
        Task { await PlusAnswers.answer(choices: picked, idea: text, other: other, shownOrder: shown, city: city, openedFrom: from) }
        step = .thanks
    }

    private func tellMe() {
        guard account.isSignedIn else { signingIn = true; return }
        join()
    }

    private func join() {
        joining = true
        Task {
            guard let token = await account.freshToken() else {
                joining = false; signingIn = true; return
            }
            let ok = await PlusAnswers.joinWaitlist(token: token)
            joining = false
            if ok { Measure.event("plus-tellme"); step = .listed }
        }
    }
}
