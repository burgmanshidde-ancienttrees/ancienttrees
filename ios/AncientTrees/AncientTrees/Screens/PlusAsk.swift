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
        Button {
            Measure.event("plus-open", ["from": "city"])
            asking = true
        } label: {
            HStack(spacing: 10) {
                Image(systemName: "sparkles")
                    .font(.system(size: 14, weight: .semibold))
                    .foregroundStyle(Brand.moss)
                    .frame(width: 32, height: 32)
                    .background(Brand.mossTint, in: .circle)
                VStack(alignment: .leading, spacing: 1) {
                    Text("Ancient Trees Plus")
                        .font(.system(size: 14, weight: .bold))
                        .foregroundStyle(Brand.ink)
                    Text("Help us choose what comes next")
                        .font(.system(size: 12))
                        .foregroundStyle(Brand.inkSoft)
                }
                Spacer(minLength: 8)
                Image(systemName: "chevron.right")
                    .font(.caption.weight(.semibold))
                    .foregroundStyle(Brand.inkSoft.opacity(0.6))
            }
            .frame(minHeight: 44)
            .contentShape(.rect)
        }
        .buttonStyle(.plain)
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
    @State private var choice: String?
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
                       message: "We're working on Plus to keep Ancient Trees going. What would make it worth paying for?",
                       buttons: [.primary("Next", id: "plus-next") { step = .choice }],
                       extra: { ideaField })
                .accessibilityIdentifier("plus-sheet")
        case .choice:
            BrandSheet(title: "Which would you want most?",
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
                Text("Anything you'd like")
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
            optionRow("none", "None of these", quiet: true)
        }
        .padding(.top, 20)
    }

    private func optionRow(_ key: String, _ label: String, quiet: Bool = false) -> some View {
        let on = choice == key
        return Button { choice = key } label: {
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
        .accessibilityAddTraits(on ? .isSelected : [])
        .accessibilityIdentifier("plus-option-\(key)")
    }

    private func send() {
        guard let choice else { return }
        let shown = order.map(\.key)
        let text = idea, city = city, from = openedFrom
        Measure.event("plus-answer", ["choice": choice])
        Task { await PlusAnswers.answer(choice: choice, idea: text, shownOrder: shown, city: city, openedFrom: from) }
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
