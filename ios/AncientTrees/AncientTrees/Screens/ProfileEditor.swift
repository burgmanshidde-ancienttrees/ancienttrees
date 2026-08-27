// Setting the name and the face people see.
//
// The name is the only required field and it is the only one that has to be
// anything: no real name is asked for, no location, no age. That restraint is
// the point rather than a gap. Hidde opened this on 2026-08-26 ("extra
// persoonsgegevens moet gewoon"), and the way to keep an opened door narrow is
// to ask for the least that makes the feature work.
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
    @State private var picked: PhotosPickerItem?
    @State private var preview: UIImage?
    @State private var saving = false
    @State private var failed = false

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
                                AsyncImage(url: u) { $0.resizable().aspectRatio(contentMode: .fill) }
                                    placeholder: { Color.clear }
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

                if failed {
                    Text("That did not save. Try again in a moment.")
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
            guard let token = await account.freshToken() else {
                saving = false; failed = true; return
            }
            var url = profiles.me?.avatar_url
            // 512 points is plenty for a face in a 62 point circle, and it
            // turns an eight megapixel camera file into about forty kilobytes.
            if let preview, let jpeg = Sightings.downsized(preview, max: 512) {
                url = await Avatars.upload(jpeg, userId: s.userId, token: token) ?? url
            }
            let ok = await profiles.save(name: name.trimmingCharacters(in: .whitespaces),
                                         avatarURL: url, userId: s.userId, token: token)
            saving = false
            if ok { dismiss() } else { failed = true }
        }
    }
}

/// The bucket half. One file per person, at a path only they may write, which
/// is what the storage policies in supabase/profiles.sql enforce.
enum Avatars {
    static func upload(_ jpeg: Data, userId: String, token: String) async -> String? {
        let base = Submission.url.deletingLastPathComponent()
            .deletingLastPathComponent()   // .../rest/v1/submissions -> .../rest
            .deletingLastPathComponent()   // -> project root
        let path = "storage/v1/object/avatars/\(userId)/avatar.jpg"
        var r = URLRequest(url: base.appendingPathComponent(path))
        r.httpMethod = "POST"
        r.setValue(Submission.key, forHTTPHeaderField: "apikey")
        r.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        r.setValue("image/jpeg", forHTTPHeaderField: "Content-Type")
        r.setValue("true", forHTTPHeaderField: "x-upsert")
        r.httpBody = jpeg
        guard let (_, response) = try? await URLSession.shared.upload(for: r, from: jpeg),
              (200..<300).contains((response as? HTTPURLResponse)?.statusCode ?? 0) else {
            return nil
        }
        return base.appendingPathComponent(
            "storage/v1/object/public/avatars/\(userId)/avatar.jpg").absoluteString
    }
}
