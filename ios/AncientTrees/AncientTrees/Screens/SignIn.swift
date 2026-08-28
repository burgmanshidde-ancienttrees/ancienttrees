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
    @Environment(\.dismiss) private var dismiss
    @Environment(\.colorScheme) private var scheme

    @State private var address = ""
    @State private var code = ""
    @State private var rawNonce = ""
    @State private var merged: Int?
    @FocusState private var focus: Field?

    private enum Field { case email, code }
    private let brand = Color(red: 0.20, green: 0.35, blue: 0.20)

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
            .padding(.top, 22)
            .padding(.bottom, 26)
        }
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
        .scrollBounceBehavior(.basedOnSize)
        .presentationDetents([.height(660), .large])
        .presentationDragIndicator(.visible)
        // One container with a name, so the layout sweep can measure the
        // sheet on its own rather than together with the screen behind it.
        .accessibilityElement(children: .contain)
        .accessibilityIdentifier("signin-sheet")
    }

    // MARK: - the ask

    private var ask: some View {
        VStack(spacing: 18) {
            header

            SignInWithAppleButton(.continue) { request in
                rawNonce = Self.nonce()
                request.requestedScopes = [.email]
                request.nonce = Self.sha256(rawNonce)
            } onCompletion: { result in
                guard case .success(let auth) = result,
                      let cred = auth.credential as? ASAuthorizationAppleIDCredential,
                      let data = cred.identityToken,
                      let token = String(data: data, encoding: .utf8) else { return }
                Task {
                    await account.signInWithApple(idToken: token, nonce: rawNonce)
                    await finishIfSignedIn()
                }
            }
            .signInWithAppleButtonStyle(scheme == .dark ? .white : .black)
            .frame(height: 52)
            .clipShape(.capsule)

            // Google under Apple, both above the typed route, which is the
            // order every consumer app has settled on: the taps first, the
            // typing second. Both buttons are the provider's own, to the
            // provider's own specification, which is the whole rule.
            GoogleSignInButton {
                Task {
                    await account.signInWithGoogle()
                    await finishIfSignedIn()
                }
            }
            .disabled(account.state == .working)

            HStack(spacing: 12) {
                Rectangle().fill(.quaternary).frame(height: 1)
                Text("or").font(.footnote).foregroundStyle(.secondary)
                Rectangle().fill(.quaternary).frame(height: 1)
            }

            TextField("you@example.com", text: $address)
                .textContentType(.emailAddress)
                .keyboardType(.emailAddress)
                .textInputAutocapitalization(.never)
                .autocorrectionDisabled()
                .submitLabel(.go)
                .focused($focus, equals: .email)
                .onSubmit { Task { await account.sendCode(to: address) } }
                .padding(.horizontal, 16).padding(.vertical, 14)
                .background(Color(.secondarySystemBackground), in: .capsule)

            Button {
                focus = nil
                Task { await account.sendCode(to: address) }
            } label: {
                HStack(spacing: 8) {
                    if account.state == .working { ProgressView().tint(.white) }
                    Text("Email me a code")
                }
                .font(.headline).frame(maxWidth: .infinity).padding(.vertical, 15)
            }
            .buttonStyle(.borderedProminent)
            .tint(brand)
            .clipShape(.capsule)
            .disabled(account.state == .working)

            problemLine
            footer
        }
    }

    // MARK: - the code

    private func codeEntry(_ to: String) -> some View {
        VStack(spacing: 18) {
            VStack(spacing: 8) {
                SpeciesMark(species: "Ginkgo", color: brand).frame(width: 48, height: 48)
                Text("Check your email").font(.title2.bold())
                Text("We sent a six digit code to \(to). Type it here and you are in.")
                    .font(.subheadline).foregroundStyle(.secondary)
                    .multilineTextAlignment(.center)
            }
            .padding(.top, 4)

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
            .buttonStyle(.borderedProminent).tint(brand).clipShape(.capsule)
            .disabled(account.state == .working)

            problemLine

            Button("Send another code") { Task { await account.sendCode(to: to) } }
                .font(.footnote)
            footer
        }
        .onAppear { focus = .code }
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
            dismiss()
        }
    }

    // MARK: - shared pieces

    private var header: some View {
        VStack(spacing: 8) {
            SpeciesMark(species: "Pedunculate Oak", color: brand)
                .frame(width: 52, height: 52)
            Text(reason.headline)
                .font(.title2.bold()).multilineTextAlignment(.center)
            Text(reason.detail)
                .font(.subheadline).foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding(.top, 2)
    }

    @ViewBuilder private var problemLine: some View {
        if let p = account.problem {
            Text(p).font(.footnote).foregroundStyle(.red).multilineTextAlignment(.center)
        }
    }

    /// The privacy line is not small print here, it is part of the offer. The
    /// honest version of it converts better than a vague one, and it is the same
    /// sentence the website has carried since the account track opened.
    private var footer: some View {
        VStack(spacing: 6) {
            // Same correction as Profile's, same day. The "no advertising" and
            // the deletion promise both survive because both are still true;
            // "Nothing else" did not.
            Text("We store your email address and what you collect: the trees you save, the ones you photograph, and where they stand. No advertising, and you can delete the lot from this app.")
                .font(.caption2).foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
            // Both of these were text a finger has to find: "Privacy" measured
            // 37 by 13 points and "Not now" 55 by 17, against Apple's 44 by 44.
            // The words stay the same size; the area around them is the target.
            // The acceptance line every consumer app carries under this button,
            // and the reason it is here rather than on a checkbox: a licence to
            // use what you send is granted by agreeing to terms once, not by
            // answering a question per photograph. Added 2026-08-24 with the
            // terms themselves; the website's sign-in dialog carries the same
            // sentence, because a person who signs in on a laptop and
            // photographs on a phone is one person.
            Text("By continuing you agree to the Terms and the Privacy notice.")
                .font(.caption2).foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
            HStack(spacing: 18) {
                Link("Terms", destination: URL(string: "https://ancienttrees.app/terms")!)
                    .font(.caption2)
                    .frame(minWidth: 44, minHeight: 44)
                    .contentShape(.rect)
                Link("Privacy", destination: URL(string: "https://ancienttrees.app/privacy")!)
                    .font(.caption2)
                    .frame(minWidth: 44, minHeight: 44)
                    .contentShape(.rect)
            }

        }
        .padding(.top, 2)
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
