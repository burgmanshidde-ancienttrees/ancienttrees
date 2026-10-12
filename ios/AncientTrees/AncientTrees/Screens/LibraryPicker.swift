// Choosing a photograph you already have, and finding out where it was taken.
//
// Hidde, 2026-08-28: "wat als ik een mooie foto op mn fotorol heb staan en die
// boom wil ik toevoegen en ik weet waar die staat." He could not. The collect
// flow took the position from CoreLocation at the moment of the shutter, which
// is right for a tree you are standing in front of and useless for one you
// photographed last spring.
//
// Convention: iNaturalist. The camera roll is the ordinary route there, not an
// exception, and the date, time and location are read from the photograph
// itself; anything missing or misread is corrected by the person afterwards. A
// photograph with no location is never refused, it is simply incomplete.
// CONVENTIONS.md carries the entry and its sources.
//
// Convention: Apple. PHPickerViewController is the picker, and to learn where a
// photograph was taken it has to be built with PHPickerConfiguration(photoLibrary:)
// so the result carries an assetIdentifier. The location then comes off the
// PHAsset. UIImagePickerController, which the camera path still uses and should,
// hands back a bare UIImage with every scrap of metadata gone.
//
// NO PERMISSION IS ASKED, since 2026-10-12. It used to ask for read access to
// the whole library to read the coordinate off the PHAsset, and somebody who
// answered "Limited" was asked to select more photos again every time a new
// one was taken (Hidde: "why can't I just give full access to photos I have to
// allow everytime for the new photos"). The picker runs outside the app and
// needs no permission, and it hands over the file with its own location and
// date unless the person switches location off in the picker's Options. That
// is the iNaturalist and Google Maps behaviour: choose, and nothing is asked.
// A library that WAS authorised before still gets the asset read, which is
// right even for a file whose GPS block was stripped.
//
// SEVERAL AT ONCE (Hidde, 2026-10-12: "I'm not able to add multiple photos at
// once"). The first one chosen is the tree's picture and the rest are its
// further photographs, the same split the tree page's "More photographs" row
// uses. Each is decoded straight to a downsampled image, never at full size,
// because four 48 megapixel photographs held as full bitmaps is how a picker
// runs a phone out of memory.

import CoreLocation
import ImageIO
import Photos
import PhotosUI
import SwiftUI
import UniformTypeIdentifiers

struct LibraryPicker: UIViewControllerRepresentable {

    struct Picked {
        var image: UIImage
        /// Nil when the photograph does not say, which is ordinary: a
        /// screenshot, a download, anything forwarded through a messenger, or
        /// a phone with location off for the camera.
        var coordinate: CLLocationCoordinate2D?
        var taken: Date?
        /// Further photographs chosen with this one, in the order chosen.
        var extras: [UIImage] = []
    }

    /// How many may be chosen at once. One for the sign, several for a tree.
    var limit: Int = 1
    var onPicked: (Picked?) -> Void
    @Environment(\.dismiss) private var dismiss

    func makeUIViewController(context: Context) -> PHPickerViewController {
        var config = PHPickerConfiguration(photoLibrary: .shared())
        config.filter = .images
        config.selectionLimit = limit
        config.selection = .ordered
        // The original file rather than a transcoded copy, so what EXIF there
        // is survives the trip when we have to fall back to reading it.
        config.preferredAssetRepresentationMode = .current
        let p = PHPickerViewController(configuration: config)
        p.delegate = context.coordinator
        return p
    }

    func updateUIViewController(_ c: PHPickerViewController, context: Context) {}

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    /// WHERE THE COORDINATE COMES FROM, as a decision rather than a line buried
    /// in the delegate, because there are three answers and only one of them
    /// can be produced on a machine with no photo library.
    ///
    /// The asset wins: it is the library's own record and it is right even for
    /// a photograph whose file has been stripped. EXIF is the fallback for the
    /// case where the asset cannot be read, which is a refused library. Neither
    /// is an error when it comes back empty.
    static func coordinate(assetLocation: CLLocation?,
                           exif: CLLocationCoordinate2D?) -> CLLocationCoordinate2D? {
        if let l = assetLocation { return l.coordinate }
        return exif
    }

    /// A coordinate out of an image file's own GPS block. Nil for the many
    /// photographs that carry none, and nil for a malformed one.
    static func exifCoordinate(in properties: [CFString: Any]) -> CLLocationCoordinate2D? {
        guard let gps = properties[kCGImagePropertyGPSDictionary] as? [CFString: Any],
              let lat = gps[kCGImagePropertyGPSLatitude] as? Double,
              let lng = gps[kCGImagePropertyGPSLongitude] as? Double
        else { return nil }
        let north = (gps[kCGImagePropertyGPSLatitudeRef] as? String ?? "N") == "N"
        let east = (gps[kCGImagePropertyGPSLongitudeRef] as? String ?? "E") == "E"
        // 0,0 is in the Atlantic and is what a cleared GPS block looks like.
        if lat == 0 && lng == 0 { return nil }
        return CLLocationCoordinate2D(latitude: north ? lat : -lat,
                                      longitude: east ? lng : -lng)
    }

    final class Coordinator: NSObject, PHPickerViewControllerDelegate {
        let parent: LibraryPicker
        init(_ p: LibraryPicker) { parent = p }

        func picker(_ picker: PHPickerViewController, didFinishPicking results: [PHPickerResult]) {
            guard let result = results.first else {
                parent.onPicked(nil)
                parent.dismiss()
                return
            }
            let rest = Array(results.dropFirst())
            Task {
                var picked = await Self.read(result)
                // One at a time rather than in parallel: each is a decode of
                // a large file, and running four at once is the memory spike
                // this file exists to avoid.
                var more: [UIImage] = []
                for r in rest {
                    if let img = await Self.read(r)?.image { more.append(img) }
                }
                picked?.extras = more
                await MainActor.run {
                    parent.onPicked(picked)
                    parent.dismiss()
                }
            }
        }

        static func read(_ result: PHPickerResult) async -> Picked? {
            let file = await fileContents(result.itemProvider)
            var image = file.image
            if image == nil { image = await loadImage(result.itemProvider) }
            guard let image else { return nil }
            var assetLocation: CLLocation?
            var taken: Date?
            // Only a library already authorised in full: touching PHAsset
            // otherwise raises the very prompt this picker no longer needs.
            if PHPhotoLibrary.authorizationStatus(for: .readWrite) == .authorized,
               let id = result.assetIdentifier {
                let assets = PHAsset.fetchAssets(withLocalIdentifiers: [id], options: nil)
                if let asset = assets.firstObject {
                    assetLocation = asset.location
                    taken = asset.creationDate
                }
            }
            var exif: CLLocationCoordinate2D?
            if assetLocation == nil || taken == nil {
                exif = exifCoordinate(in: file.properties)
                if taken == nil { taken = exifDate(in: file.properties) }
            }
            return Picked(image: image,
                          coordinate: coordinate(assetLocation: assetLocation, exif: exif),
                          taken: taken)
        }

        private static func loadImage(_ provider: NSItemProvider) async -> UIImage? {
            guard provider.canLoadObject(ofClass: UIImage.self) else { return nil }
            return await withCheckedContinuation { cont in
                provider.loadObject(ofClass: UIImage.self) { object, _ in
                    cont.resume(returning: object as? UIImage)
                }
            }
        }

        /// The file's own metadata block AND the picture, downsampled while
        /// it is decoded, from one read of the file. Done inside the closure
        /// because loadFileRepresentation deletes its file the moment the
        /// closure returns. 2400 pixels is what Sightings keeps at most
        /// (1600) with room to spare, and decoding straight to that size
        /// never holds the full bitmap in memory.
        private static func fileContents(_ provider: NSItemProvider) async
            -> (image: UIImage?, properties: [CFString: Any]) {
            await withCheckedContinuation { cont in
                _ = provider.loadFileRepresentation(forTypeIdentifier: UTType.image.identifier) { url, _ in
                    guard let url,
                          let src = CGImageSourceCreateWithURL(url as CFURL, nil)
                    else { cont.resume(returning: (nil, [:])); return }
                    let props = CGImageSourceCopyPropertiesAtIndex(src, 0, nil)
                        as? [CFString: Any] ?? [:]
                    let opts: [CFString: Any] = [
                        kCGImageSourceCreateThumbnailFromImageAlways: true,
                        kCGImageSourceCreateThumbnailWithTransform: true,
                        kCGImageSourceShouldCacheImmediately: true,
                        kCGImageSourceThumbnailMaxPixelSize: 2400,
                    ]
                    let cg = CGImageSourceCreateThumbnailAtIndex(src, 0, opts as CFDictionary)
                    cont.resume(returning: (cg.map { UIImage(cgImage: $0) }, props))
                }
            }
        }

        private static func exifDate(in properties: [CFString: Any]) -> Date? {
            guard let exif = properties[kCGImagePropertyExifDictionary] as? [CFString: Any],
                  let text = exif[kCGImagePropertyExifDateTimeOriginal] as? String
            else { return nil }
            let f = DateFormatter()
            f.dateFormat = "yyyy:MM:dd HH:mm:ss"
            return f.date(from: text)
        }
    }
}
