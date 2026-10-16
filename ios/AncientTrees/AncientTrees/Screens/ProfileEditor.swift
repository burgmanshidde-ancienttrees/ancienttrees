// Setting the name and the face people see.
//
// The name is the only required field and it is the only one that has to be
// anything: no real name is asked for, no location, no age. That restraint is
// the point rather than a gap. Hidde opened this on 2026-08-26 ("extra
// persoonsgegevens moet gewoon"), and the way to keep an opened door narrow is
// to ask for the least that makes the feature work.
//
// One door opened wider on 2026-10-16: a COUNTRY, for the flag after your name
// (Hidde: "Yes to storing a country per account", after Polarsteps' profile).
// Optional, picked by the person, never guessed from where the phone is.
//
// The photograph is optional and stays optional. It goes to the `avatars`
// bucket under the person's own id, so one person owns one folder and deleting
// the account leaves nothing behind pointing at it.

import SwiftUI
import PhotosUI

struct ProfileEditor: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(Account.self) private var account
    @Environment(Profiles.self) private var profiles

    @State private var name = ""
    @State private var country: String?
    @State private var picked: PhotosPickerItem?
    @State private var preview: UIImage?
    @State private var saving = false
    @State private var failed = false
    @State private var reason: String?

    var body: some View {
        NavigationStack {
            Form {
                Section {
                    HStack(spacing: 16) {
                        ZStack {
                            Circle().fill(Brand.moss.opacity(0.12))
                            if let preview {
                                Image(uiImage: preview).resizable()
                                    .aspectRatio(contentMode: .fill).clipShape(.circle)
                            } else if let url = profiles.me?.avatar_url, let u = URL(string: url) {
                                TreePhoto(url: u) { Color.clear }
                                    .clipShape(.circle)
                            } else {
                                Image(systemName: "person.fill")
                                    .font(.system(size: 22))
                                    .foregroundStyle(Brand.moss.opacity(0.6))
                            }
                        }
                        .frame(width: 64, height: 64)

                        PhotosPicker(selection: $picked, matching: .images) {
                            Text(preview == nil && profiles.me?.avatar_url == nil
                                 ? "Choose a photo" : "Change photo")
                                .frame(minHeight: 44)
                                .contentShape(.rect)
                        }
                    }
                    .padding(.vertical, 4)
                } header: {
                    Text("Your picture")
                } footer: {
                    Text("Optional. People who follow you see it beside your name.")
                }

                Section {
                    TextField("The name people see", text: $name)
                        .textInputAutocapitalization(.words)
                } header: {
                    Text("Your name")
                } footer: {
                    Text("Any name you like. It does not have to be your real one.")
                }

                // The flag after your name. iOS Settings' own shape for a
                // long choice: a row that opens a list (Language & Region).
                Section {
                    Picker("Country", selection: $country) {
                        Text("None").tag(String?.none)
                        ForEach(Self.countries, id: \.code) { c in
                            Text(Self.row(c)).tag(Optional(c.code))
                        }
                    }
                    .pickerStyle(.navigationLink)
                    .accessibilityIdentifier("profile-country")
                } header: {
                    Text("Your country")
                } footer: {
                    Text("Optional. Its flag shows after your name.")
                }

                if failed {
                    VStack(alignment: .leading, spacing: 4) {
                        Text("That did not save. Try again in a moment.")
                        if let reason {
                            Text("What went wrong: \(reason).")
                                .font(.caption)
                        }
                    }
                    .font(.footnote).foregroundStyle(.red)
                }
            }
            .navigationTitle("Your profile")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button(saving ? "Saving" : "Save") { save() }
                        .disabled(saving || name.trimmingCharacters(in: .whitespaces).isEmpty)
                }
            }
            .task {
                name = profiles.me?.display_name ?? ""
                country = profiles.myCountry
            }
            .onChange(of: picked) { _, item in
                guard let item else { return }
                Task {
                    if let data = try? await item.loadTransferable(type: Data.self),
                       let img = UIImage(data: data) {
                        preview = img
                    }
                }
            }
        }
    }

    private func save() {
        guard let s = account.session else { return }
        saving = true
        Task {
            // A TOKEN THAT IS STILL GOOD. This read session.accessToken
            // directly, and those expire after an hour, so saving failed for
            // anybody signed in longer than that: both calls came back 401 and
            // the screen said "that did not save" without knowing why.
            Avatars.lastFailure = nil
            guard let token = await account.freshToken() else {
                // The commonest cause by far, and the one that was silent: a
                // token that has expired and could not be renewed.
                reason = "your sign-in has expired"
                saving = false; failed = true; return
            }
            var url = profiles.me?.avatar_url
            // 512 points is plenty for a face in a 62 point circle, and it
            // turns an eight megapixel camera file into about forty kilobytes.
            if let preview, let jpeg = Sightings.downsized(preview, max: 512) {
                url = await Avatars.upload(jpeg, userId: s.userId, token: token) ?? url
            }
            var ok = await profiles.save(name: name.trimmingCharacters(in: .whitespaces),
                                         avatarURL: url, userId: s.userId, token: token)
            var countryFailed = false
            if ok, country != profiles.myCountry {
                ok = await profiles.saveCountry(country, userId: s.userId, token: token)
                countryFailed = !ok
            }
            saving = false
            if ok { dismiss() } else {
                reason = countryFailed ? "your country would not save"
                    : Avatars.lastFailure.map { "\($0) would not upload" } ?? "the server refused it"
                failed = true
            }
        }
    }

    /// A picker row: the flag, then the country's name.
    static func row(_ c: (code: String, name: String)) -> String {
        [CountryFlag.emoji(c.code), c.name].compactMap { $0 }.joined(separator: "  ")
    }

    /// Every ISO country by its English name, for the picker.
    static let countries: [(code: String, name: String)] = {
        let en = Locale(identifier: "en")
        return Locale.Region.isoRegions
            .map(\.identifier)
            .filter { $0.count == 2 && $0.allSatisfy(\.isLetter) }
            .compactMap { code in en.localizedString(forRegionCode: code).map { (code, $0) } }
            .sorted { $0.1.localizedCaseInsensitiveCompare($1.1) == .orderedAscending }
    }()
}

/// The bucket half. One file per person, at a path only they may write, which
/// is what the storage policies in supabase/profiles.sql enforce.
enum Avatars {
    /// What went wrong on the last attempt, shown on the editor rather than
    /// swallowed. Cleared when a save starts.
    static var lastFailure: String?

    static func upload(_ jpeg: Data, userId: String, token: String) async -> String? {
        // Three deletingLastPathComponent calls used to walk this back up from
        // the submissions table to the project root, with the count of them
        // load-bearing and commented. Supa knows where the project is.
        var r = Supa.request("/storage/v1/object/avatars/\(userId)/avatar.jpg",
                             token: token, body: jpeg)
        r.setValue("image/jpeg", forHTTPHeaderField: "Content-Type")
        r.setValue("true", forHTTPHeaderField: "x-upsert")
        guard let (body, response) = try? await Net.upload(for: r, from: jpeg),
              (200..<300).contains((response as? HTTPURLResponse)?.statusCode ?? 0) else {
            // WHY, not just no. A failure that says nothing is a failure nobody
            // can fix, and this one cost an afternoon of guessing between an
            // expired token, a bucket policy and a size limit (2026-08-27).
            lastFailure = "the picture"
            return nil
        }
        _ = body
        return Supa.url + "/storage/v1/object/public/avatars/\(userId)/avatar.jpg"
    }
}
