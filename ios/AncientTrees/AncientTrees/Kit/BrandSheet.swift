import SwiftUI
import UIKit

// THE ONE SHEET (Hidde, 2026-10-10: "get your act together in designing al
// these overlays ... make it a component or something").
//
// Convention: our own sign-in sheet, which is the one overlay measured against
// AllTrails' (CONVENTIONS.md, "The shape of a sign-in sheet", and "One sheet
// for every overlay"): a sheet from the bottom, our handle 12 down, a grey
// close cross in the corner, everything centred, 24 at the sides, a 56 tile
// when the sheet starts something, a 26 point headline, one or two grey
// sentences, and buttons 48 tall with round ends. The audit that produced this
// found 27 small overlays in the app built from four green buttons, three reds,
// five top paddings, fixed heights that cut buttons off, and system alerts that
// looked like a different app. Every one of them is this view now, and
// scripts/sheetcheck.py refuses an .alert, a .confirmationDialog or a .sheet
// whose content is not on its list, so the next overlay is this one too.
//
// The website draws the same sheet from components/Sheet.astro and the
// .at-sheet styles in style.css: same order, same four kinds of button.

/// One button on a sheet. Four kinds and no more: green is the one thing we
/// hope you do (at most one per sheet), grey the other choices, red removes or
/// deletes something, quiet is the polite way out ("Not now").
struct SheetButton: Identifiable {
    enum Kind { case primary, secondary, destructive, destructiveQuiet, quiet }
    let id = UUID()
    let label: String
    var systemImage: String? = nil
    var kind: Kind = .secondary
    var identifier: String? = nil
    let action: () -> Void

    static func primary(_ label: String, _ systemImage: String? = nil, id: String? = nil,
                        action: @escaping () -> Void) -> SheetButton {
        SheetButton(label: label, systemImage: systemImage, kind: .primary, identifier: id, action: action)
    }
    static func secondary(_ label: String, _ systemImage: String? = nil, id: String? = nil,
                          action: @escaping () -> Void) -> SheetButton {
        SheetButton(label: label, systemImage: systemImage, kind: .secondary, identifier: id, action: action)
    }
    static func destructive(_ label: String, id: String? = nil,
                            action: @escaping () -> Void) -> SheetButton {
        SheetButton(label: label, kind: .destructive, identifier: id, action: action)
    }
    static func destructiveQuiet(_ label: String, id: String? = nil,
                                 action: @escaping () -> Void) -> SheetButton {
        SheetButton(label: label, kind: .destructiveQuiet, identifier: id, action: action)
    }
    static func quiet(_ label: String, id: String? = nil,
                      action: @escaping () -> Void) -> SheetButton {
        SheetButton(label: label, kind: .quiet, identifier: id, action: action)
    }
}

/// The four kinds, drawn. 48 tall with round ends, the sign-in sheet's pills.
struct SheetButtonStyle: ButtonStyle {
    let kind: SheetButton.Kind

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: kind == .quiet ? 15 : 16, weight: .semibold))
            .foregroundStyle(foreground)
            .frame(maxWidth: .infinity)
            .frame(height: kind == .quiet ? 44 : 48)
            .background(background, in: .capsule)
            .contentShape(.capsule)
            .opacity(configuration.isPressed ? 0.8 : 1)
            .animation(.easeOut(duration: 0.12), value: configuration.isPressed)
    }

    private var foreground: Color {
        switch kind {
        case .primary: Brand.onMoss
        case .secondary: Brand.ink
        case .destructive: .white
        case .destructiveQuiet: Brand.dangerText
        case .quiet: Brand.inkSoft
        }
    }
    private var background: Color {
        switch kind {
        case .primary: Brand.moss
        case .secondary, .destructiveQuiet: Brand.creamDark
        case .destructive: Brand.danger
        case .quiet: .clear
        }
    }
}

/// The sheet itself. Put it inside `.sheet { }` and nothing else: it sizes
/// itself to what it holds, draws the handle and the cross, and closes on a
/// swipe, a tap on the cross, or any button.
struct BrandSheet<Extra: View>: View {
    var icon: String? = nil
    let title: String
    var message: String? = nil
    var points: [String] = []
    let buttons: [SheetButton]
    var footnote: String? = nil
    /// Anything a sheet needs between the words and the buttons (a field to
    /// type DELETE into). Rarely used, and never another set of buttons.
    @ViewBuilder var extra: () -> Extra
    var onClose: (() -> Void)? = nil

    @Environment(\.dismiss) private var dismiss
    @State private var height: CGFloat = 320

    var body: some View {
        ScrollView {
            VStack(spacing: 0) {
                if let icon {
                    Image(systemName: icon)
                        .font(.system(size: 24, weight: .semibold))
                        .foregroundStyle(Brand.moss)
                        .frame(width: 56, height: 56)
                        .background(Brand.mossTint, in: .rect(cornerRadius: 14, style: .continuous))
                        .padding(.bottom, 16)
                        .accessibilityHidden(true)
                }
                Text(title)
                    .font(.brand(26, .bold, relativeTo: .title2))
                    .foregroundStyle(Brand.ink)
                    .multilineTextAlignment(.center)
                    .fixedSize(horizontal: false, vertical: true)
                    // Clear of the cross in the corner on a long headline.
                    .padding(.horizontal, 18)
                    .accessibilityAddTraits(.isHeader)
                if let message {
                    Text(message)
                        .font(.system(size: 15))
                        .foregroundStyle(Brand.inkSoft)
                        .multilineTextAlignment(.center)
                        .fixedSize(horizontal: false, vertical: true)
                        .padding(.top, 8)
                }
                if !points.isEmpty {
                    VStack(alignment: .leading, spacing: 10) {
                        ForEach(points, id: \.self) { p in
                            HStack(alignment: .firstTextBaseline, spacing: 10) {
                                Image(systemName: "checkmark")
                                    .font(.system(size: 14, weight: .bold))
                                    .foregroundStyle(Brand.moss)
                                    .accessibilityHidden(true)
                                Text(p)
                                    .font(.system(size: 15))
                                    .foregroundStyle(Brand.ink)
                                    .fixedSize(horizontal: false, vertical: true)
                            }
                        }
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(.top, 18)
                }
                extra()
                VStack(spacing: 12) {
                    ForEach(buttons) { b in
                        Button(action: b.action) {
                            if let s = b.systemImage {
                                Label(b.label, systemImage: s)
                            } else {
                                Text(b.label)
                            }
                        }
                        .buttonStyle(SheetButtonStyle(kind: b.kind))
                        .accessibilityIdentifier(b.identifier ?? "")
                    }
                }
                .padding(.top, 22)
                if let footnote {
                    Text(footnote)
                        .font(.footnote)
                        .foregroundStyle(Brand.inkSoft)
                        .multilineTextAlignment(.center)
                        .fixedSize(horizontal: false, vertical: true)
                        .padding(.top, 14)
                }
            }
            .padding(.horizontal, 24)
            // 36: the handle drawn 12 down and 5 tall, then air.
            .padding(.top, 36)
            .padding(.bottom, BrandSheetFit.floating ? 28 : 16)
            .onGeometryChange(for: CGFloat.self) { $0.size.height } action: { height = max(200, $0) }
        }
        .scrollBounceBehavior(.basedOnSize)
        .modifier(BrandSheetFit())
        .overlay(alignment: .topTrailing) { SheetCloseButton { (onClose ?? { dismiss() })() } }
        // Fits what it holds, and can always be dragged to full height, so
        // large text never cuts a button off (the 2026-10-10 audit found three
        // fixed heights doing exactly that).
        .presentationDetents([.height(height - (BrandSheetFit.floating ? BrandSheetFit.bottomInset : 0)), .large])
        .brandSheetHandle()
        .presentationBackground(Color(.systemBackground))
    }
}

extension BrandSheet where Extra == EmptyView {
    init(icon: String? = nil, title: String, message: String? = nil, points: [String] = [],
         buttons: [SheetButton], footnote: String? = nil, onClose: (() -> Void)? = nil) {
        self.icon = icon; self.title = title; self.message = message; self.points = points
        self.buttons = buttons; self.footnote = footnote; self.extra = { EmptyView() }
        self.onClose = onClose
    }
}

/// Apple's close button: a small grey circle with the cross in it, 30 drawn
/// and 48 to hit, inset from the corner. The sign-in sheet's, shared.
struct SheetCloseButton: View {
    let action: () -> Void
    var body: some View {
        Button(action: action) {
            Image(systemName: "xmark")
                .font(.system(size: 13, weight: .bold))
                .foregroundStyle(.secondary)
                .frame(width: 30, height: 30)
                .background(Brand.surfaceMuted, in: .circle)
                // 48 to hit, not 44: at 44 the sheet's own top edge took two
                // points off it and appfit measured 42 (2026-10-10). The drawn
                // circle stays where the sign-in sheet's sits.
                .frame(width: 48, height: 48)
                .contentShape(.rect)
        }
        .buttonStyle(.plain)
        .padding(.top, 8)
        .padding(.trailing, 10)
        .accessibilityLabel("Close")
        .accessibilityIdentifier("sheet-close")
    }
}

/// On the floating sheet of iOS 26 the bottom safe-area inset is empty space
/// under the card; on the edge-to-edge sheet of iOS 18 it is where the home
/// indicator lives. The full reasoning is at its first use, SignIn.swift.
struct BrandSheetFit: ViewModifier {
    static var floating: Bool {
        if #available(iOS 26, *) { return true } else { return false }
    }
    static var bottomInset: CGFloat {
        UIApplication.shared.connectedScenes
            .compactMap { ($0 as? UIWindowScene)?.keyWindow?.safeAreaInsets.bottom }
            .first ?? 0
    }
    func body(content: Content) -> some View {
        if #available(iOS 26, *) {
            content.ignoresSafeArea(.container, edges: .bottom)
        } else {
            content
        }
    }
}
