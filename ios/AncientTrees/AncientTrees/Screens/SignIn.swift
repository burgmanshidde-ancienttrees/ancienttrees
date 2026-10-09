// The one sign-in surface, presented as a sheet from wherever the moment
// happened rather than as a destination somebody has to go and find.
//
// The shape is read off the products people already know, per the convention
// rule: Apple's own button first at full width, a hairline "or", then a single
// email field. AllTrails, Airbnb and Google Maps all put the one-tap identity
// above the typed one, and they are right about the order for the same reason
// every time. On a phone, typing an address, leaving for Mail and finding the
// way back is four chances to give up, and one Face ID tap is none.
//
// Two things this screen refuses to do, both learned from watching our own
// website's dialog:
//
// There is ONE job here. The web version offers "Email me a sign-in link", then
// "More options", then "Get the app", and "More options" leads to a page with
// exactly the same single option on it. Three buttons at the moment of decision
// is not generosity, it is a fork in a road somebody was already walking down.
//
// And the copy names the tree. "The Last Elm of Stationsplein is ticked off" is
// a sentence about something that just happened to you; "Create an account" is a
// sentence about us. The name sits in the line underneath rather than in the
// headline, because at title size a long name runs the whole width of a phone.

import SwiftUI
import AuthenticationServices
import CryptoKit

struct SignInSheet: View {
    let reason: SignInReason
    let localCount: Int

    @Environment(Account.self) private var account
    @Environment(Saved.self) private var saved
    @Environment(Nudge.self) private var nudge
    @Environment(\.dismiss) private var dismiss
    @Environment(\.colorScheme) private var scheme

    @State private var address = ""
    @State private var code = ""
    @State private var rawNonce = ""
    @State private var merged: Int?
    /// The sheet stands as tall as what it holds, measured (the add sheet's
    /// fix of 2026-09-28), so no fixed number leaves a gap to explain.
    @State private var askHeight: CGFloat = 470
    @FocusState private var focus: Field?

    private enum Field { case email, code }
    /// The green this screen presses in, and the deeper one it FILLS with. They
    /// used to be one fixed value written out here, which is fine in daylight
    /// and wrong twice over in the dark: a mid green as text on a near-black
    /// ground is 2.5:1, and a filled button needs a green that white still
    /// reads on. Brand carries both and each follows the appearance.
    private let brand = Brand.moss
    private let brandFill = Brand.canopy

    /// iOS 26 draws a sheet as a floating card; iOS 18 runs it to the edge.
    /// See the comment on FlushBottomOnFloatingSheet below.
    private static var floating: Bool {
        if #available(iOS 26, *) { return true } else { return false }
    }
    /// The home indicator's room, 34 on most phones and 0 on the SE: the same
    /// reading TabBar.bottomGap takes.
    private static var bottomInset: CGFloat {
        UIApplication.shared.connectedScenes
            .compactMap { ($0 as? UIWindowScene)?.keyWindow?.safeAreaInsets.bottom }
            .first ?? 0
    }

    var body: some View {
        ScrollView {
            VStack(spacing: 18) {
                switch account.state {
                case .signedIn: done
                case .codeSent(let to): codeEntry(to)
                default: ask
                }
            }
            .padding(.horizontal, 22)
            .padding(.top, 28)
            .padding(.bottom, Self.floating ? 28 : 16)
            .onGeometryChange(for: CGFloat.self) { $0.size.height } action: { askHeight = max(320, $0) }
        }
        // THE BLANK BAND UNDER THE FINE PRINT, which Hidde read as the sheet
        // being out of true three times (2026-10-01 "the vertical alignments
        // once again feels off", 2026-10-08, 2026-10-09). Measured on the 17
        // Pro: 30pt above the icon, 46pt below the last line. A .height detent
        // is the height ABOVE the bottom safe area: the system adds the
        // home-indicator inset (34pt) to the sheet on top of it, and whatever
        // we pad, that inset is laid out empty under our content. Ignoring the
        // safe area alone does not help, it only lets the content reach into
        // a band the sheet is still too tall for (tried first, measured 63pt
        // of blank). So on iOS 26, where the sheet is a floating card whose
        // bottom edge already sits above the indicator, the detent is the
        // content MINUS that inset and the content fills the card: 28 above
        // the icon, 28 below the last line. On iOS 18 the sheet is flush to
        // the screen edge and the inset is the indicator's own room, kept.
        .modifier(FlushBottomOnFloatingSheet())
        // A cross in the corner rather than a "Not now" at the bottom (Hidde,
        // 2026-08-24). A sheet is dismissed by its corner everywhere, and a
        // worded refusal at the end of the offer makes declining feel like an
        // answer you owe rather than a thing you close.
        .overlay(alignment: .topTrailing) {
            Button { dismiss() } label: {
                Image(systemName: "xmark")
                    .font(.system(size: 15, weight: .semibold))
                    .foregroundStyle(.secondary)
                    .frame(width: 44, height: 44)
                    .contentShape(.rect)
            }
            .accessibilityLabel("Close")
        }
        // A CLOSED SHEET LEAVES NOTHING ARMED. Swiping this away is an answer,
        // and the save it was going to finish should not land on the next
        // sign-in an hour later. `done` has already settled and cleared by the
        // time this runs, so the two cannot both fire.
        .onDisappear { nudge.settle(ranThrough: false) }
        .scrollBounceBehavior(.basedOnSize)
        // 660 was measured against a sheet carrying the typed email route as
        // well. With that hidden for 1.0 (Launch.emailSignIn) the same height
        // left nearly half the sheet empty under the two buttons, which reads
        // as a screen that failed to load rather than a short one. The height
        // follows what is actually on it.
        .presentationDetents([.height(askHeight - (Self.floating ? Self.bottomInset : 0)), .large])
        // SOLID, not the system's glass: on a glass sheet the page behind
        // showed through the email button as a green blur (2026-10-01).
        .presentationBackground(Color(.systemBackground))
        .presentationDragIndicator(.visible)
        // One container with a name, so the layout sweep can measure the
        // sheet on its own rather than together with the screen behind it.
        .accessibilityElement(children: .contain)
        .accessibilityIdentifier("signin-sheet")
    }

    // MARK: - the ask

    /// THE SHAPE OF AllTrails' AND Airbnb's SHEET (Hidde, 2026-10-01: "do we
    /// need this text underneath? less is more", "where is email smart link
    /// login?", "the vertical alignments once again feels off"). A title and
    /// a line, three sign-in buttons of one size and one spacing, then one
    /// line linking the terms. Email is a third button that opens its field,
    /// rather than a field always on show below an "or".
    private var ask: some View {
        VStack(alignment: .leading, spacing: 24) {
            header

            // 8 between the buttons, Apple's minimum, after 12 read as three
            // separate offers rather than one stack (Hidde, 2026-10-09: "the
            // buttons should be closer to each other vertically").
            VStack(spacing: 8) {
                SignInWithAppleButton(.continue) { request in
                    rawNonce = Self.nonce()
                    // The name as well, which Apple gives ONCE, on the first
                    // authorisation, and only if asked (2026-10-02).
                    request.requestedScopes = [.fullName, .email]
                    request.nonce = Self.sha256(rawNonce)
                } onCompletion: { result in
                    guard case .success(let auth) = result,
                          let cred = auth.credential as? ASAuthorizationAppleIDCredential,
                          let data = cred.identityToken,
                          let token = String(data: data, encoding: .utf8) else { return }
                    let given = [cred.fullName?.givenName, cred.fullName?.familyName]
                        .compactMap { $0 }.joined(separator: " ")
                    Task {
                        await account.signInWithApple(idToken: token, nonce: rawNonce)
                        account.noteProviderName(given)
                        await finishIfSignedIn()
                    }
                }
                .signInWithAppleButtonStyle(scheme == .dark ? .white : .black)
                .frame(height: 52)
                .clipShape(.capsule)

                GoogleSignInButton {
                    Task {
                        await account.signInWithGoogle()
                        await finishIfSignedIn()
                    }
                }
                .disabled(account.state == .working)

                if Launch.emailSignIn { emailRoute }
            }

            problemLine
            footer
        }
    }

    @State private var emailOpen = false

    /// The third way in, closed until asked for.
    @ViewBuilder private var emailRoute: some View {
        if !emailOpen {
            Button {
                withAnimation(.snappy) { emailOpen = true }
                focus = .email
            } label: {
                Label("Continue with email", systemImage: "envelope")
                    .font(.system(size: 19, weight: .medium))
                    .foregroundStyle(Brand.ink)
                    .frame(maxWidth: .infinity).frame(height: 52)
                    .background(Color(.systemBackground), in: .capsule)
                    .overlay { Capsule().strokeBorder(Color(.separator), lineWidth: 1) }
                    .contentShape(.capsule)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("signin-email")
        } else {
            TextField("you@example.com", text: $address)
                .textContentType(.emailAddress)
                .keyboardType(.emailAddress)
                .textInputAutocapitalization(.never)
                .autocorrectionDisabled()
                .submitLabel(.go)
                .focused($focus, equals: .email)
                .onSubmit { Task { await account.sendCode(to: address) } }
                .padding(.horizontal, 18).frame(height: 52)
                .background(Color(.secondarySystemBackground), in: .capsule)

            Button {
                focus = nil
                Task { await account.sendCode(to: address) }
            } label: {
                HStack(spacing: 8) {
                    if account.state == .working { ProgressView().tint(.white) }
                    Text(Launch.emailCode ? "Email me a code" : "Email me a sign-in link")
                }
                .font(.headline).foregroundStyle(.white)
                .frame(maxWidth: .infinity).frame(height: 52)
                .background(brand, in: .capsule)
            }
            .buttonStyle(.plain)
            .disabled(account.state == .working || !address.contains("@"))
        }
    }


    private func codeEntry(_ to: String) -> some View {
        VStack(spacing: 18) {
            VStack(spacing: 8) {
                SpeciesMark(species: "Ginkgo", color: brand).frame(width: 48, height: 48)
                Text("Check your email").font(.title2.bold())
                Text(Launch.emailCode
                     ? "We sent a six digit code to \(to). Type it here and you are in."
                     : "We sent a sign-in link to \(to). Tap it and you come back here, signed in. It works once and lasts fifteen minutes.")
                    .font(.subheadline).foregroundStyle(.secondary)
                    .multilineTextAlignment(.center)
            }
            .padding(.top, 4)

            // The digits only where the mail actually carries digits. See
            // Launch.emailCode: with the built-in sender it carries a link, and
            // a field asking for six numbers that are nowhere in the mail is
            // the exact fault Hidde hit on 2026-08-30 ("je hoort digits te
            // krijgen maar ik krijg een magic link").
            if Launch.emailCode {
            TextField("123456", text: $code)
                .keyboardType(.numberPad)
                .textContentType(.oneTimeCode)
                .multilineTextAlignment(.center)
                .font(.title2.monospacedDigit().weight(.semibold))
                .focused($focus, equals: .code)
                .padding(.vertical, 14)
                .background(Color(.secondarySystemBackground), in: .capsule)
                .onChange(of: code) { _, new in
                    if new.filter(\.isNumber).count == 6 {
                        Task {
                            await account.verify(code: new, email: to)
                            await finishIfSignedIn()
                        }
                    }
                }

            Button {
                Task { await account.verify(code: code, email: to) ; await finishIfSignedIn() }
            } label: {
                HStack(spacing: 8) {
                    if account.state == .working { ProgressView().tint(.white) }
                    Text("Sign in")
                }
                .font(.headline).frame(maxWidth: .infinity).padding(.vertical, 15)
            }
            .buttonStyle(.borderedProminent).tint(brandFill).clipShape(.capsule)
            .disabled(account.state == .working)
            }

            problemLine

            Button(Launch.emailCode ? "Send another code" : "Send another link") {
                Task { await account.sendCode(to: to) }
            }
                .font(.footnote)
            footer
        }
        .onAppear { if Launch.emailCode { focus = .code } }
    }

    // MARK: - done

    /// SIGNED IN MEANS DONE. No congratulation screen (Hidde, 2026-08-25: "i
    /// dont think this screen adds anything just skip it).
    ///
    /// It said "Your 8 trees are in your account. They are on the website too"
    /// over a button called "Back to the trees", which is a page whose only
    /// content is a claim about something that already happened and a way to
    /// leave. Every app people use closes the sheet and returns them to what
    /// they were doing; the trees being kept is what the sheet PROMISED, and
    /// delivering a promise does not need its own screen.
    ///
    /// The merge still runs, because that is the part that does something: it
    /// pulls back what the account already held. A brief spinner while it does,
    /// and then the sheet is gone.
    private var done: some View {
        VStack(spacing: 14) {
            ProgressView()
                .padding(.vertical, 30)
                .accessibilityLabel("Signing you in")
        }
        .task {
            await finishIfSignedIn()
            // AND THEN THE THING THEY CAME HERE TO DO. A gate turns a tap into
            // a sign-in, and until now it swallowed the tap: press the heart
            // signed out, sign in, and land back on the tree with it unsaved.
            nudge.settle(ranThrough: true)
            dismiss()
        }
    }

    // MARK: - shared pieces

    /// No glyph above the headline (Hidde, 2026-10-09: "maybe the tree should
    /// be next to the title or just gone ... it feels a mess"). The reference
    /// this sheet is read off, AllTrails' and Airbnb's, is a title, a line and
    /// the buttons; the oak mark was a leftover from an earlier shape and sat
    /// alone at the top left with nothing to belong to.
    private var header: some View {
        VStack(alignment: .leading, spacing: 8) {
            // The brand's display face and ink, as every other heading in the
            // app and the website's dialog (Hidde, 2026-10-08: "the design of
            // the overlay to login is a bit off"). It was the system bold in
            // system colours, the one heading in the app that did not look
            // like ours.
            Text(reason.headline)
                .font(.brand(26, .bold, relativeTo: .title2))
                .foregroundStyle(Brand.ink)
                .multilineTextAlignment(.leading)
                .fixedSize(horizontal: false, vertical: true)
            Text(reason.detail)
                .font(.subheadline).foregroundStyle(Brand.inkSoft)
                .multilineTextAlignment(.leading)
                .fixedSize(horizontal: false, vertical: true)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(.top, 2)
    }

    @ViewBuilder private var problemLine: some View {
        if let p = account.problem {
            Text(p).font(.footnote).foregroundStyle(.red).multilineTextAlignment(.leading)
                .frame(maxWidth: .infinity, alignment: .leading)
        }
    }

    /// The privacy line is not small print here, it is part of the offer. The
    /// honest version of it converts better than a vague one, and it is the same
    /// sentence the website has carried since the account track opened.
    /// One line, links inline, which is what every reference sheet carries
    /// under its buttons. The paragraph about what we store went on
    /// 2026-10-01 (Hidde: "do we need this text underneath? less is more");
    /// the privacy notice the line links to says it in full.
    private var footer: some View {
        Text("By continuing you agree to the [Terms](https://ancienttrees.app/terms) and the [Privacy notice](https://ancienttrees.app/privacy).")
            .font(.footnote).foregroundStyle(.secondary)
            .tint(brand)
            .multilineTextAlignment(.leading)
            .frame(maxWidth: .infinity, alignment: .leading)
    }

    private func finishIfSignedIn() async {
        guard account.isSignedIn, merged == nil else { return }
        merged = await CloudSync.merge(account: account, saved: saved)
    }

    // MARK: - Apple's nonce

    private static func nonce(_ length: Int = 32) -> String {
        let chars = Array("0123456789ABCDEFGHIJKLMNOPQRSTUVXYZabcdefghijklmnopqrstuvwxyz-._")
        var out = ""
        for _ in 0..<length {
            out.append(chars[Int.random(in: 0..<chars.count)])
        }
        return out
    }

    private static func sha256(_ input: String) -> String {
        SHA256.hash(data: Data(input.utf8)).map { String(format: "%02x", $0) }.joined()
    }
}


/// See the comment at its use in SignInSheet.body: on the floating sheet of
/// iOS 26 the bottom safe-area inset is empty space, on the edge-to-edge
/// sheet of iOS 18 it is where the home indicator lives.
private struct FlushBottomOnFloatingSheet: ViewModifier {
    func body(content: Content) -> some View {
        if #available(iOS 26, *) {
            content.ignoresSafeArea(.container, edges: .bottom)
        } else {
            content
        }
    }
}
