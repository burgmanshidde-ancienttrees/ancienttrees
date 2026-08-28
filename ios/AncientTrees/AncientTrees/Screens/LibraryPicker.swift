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
// WHY WE ASK FOR PERMISSION AT ALL, since the picker itself needs none: the
// asset is where the coordinate and the date live, and reading it needs
// authorisation. So we ask when somebody taps the button that says choose a
// photograph, which is the moment the prompt explains itself, and we present
// the picker whatever they answer. Refused simply means we have to ask them
// where the tree is, which is a question they can answer.

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
    }

    var onPicked: (Picked?) -> Void
    @Environment(\.dismiss) private var dismiss

    func makeUIViewController(context: Context) -> PHPickerViewController {
        var config = PHPickerConfiguration(photoLibrary: .shared())
        config.filter = .images
        config.selectionLimit = 1
        // The original file rather than a transcoded copy, so what EXIF there
        // is survives the trip when we have to fall back to reading it.
        config.preferredAssetRepresentationMode = .current
        let p = PHPickerViewController(configuration: config)
        p.delegate = context.coordinator
        return p
    }

    func updateUIViewController(_ c: PHPickerViewController, context: Context) {}

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    /// Ask before presenting. Called by whoever is about to show this picker,
    /// not by the picker itself, because the prompt belongs to the tap.
    static func askForLibrary() async {
        guard PHPhotoLibrary.authorizationStatus(for: .readWrite) == .notDetermined else { return }
        _ = await PHPhotoLibrary.requestAuthorization(for: .readWrite)
    }

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
            Task {
                let picked = await Self.read(result)
                await MainActor.run {
                    parent.onPicked(picked)
                    parent.dismiss()
                }
            }
        }

        static func read(_ result: PHPickerResult) async -> Picked? {
            guard let image = await loadImage(result.itemProvider) else { return nil }
            var assetLocation: CLLocation?
            var taken: Date?
            if let id = result.assetIdentifier {
                let assets = PHAsset.fetchAssets(withLocalIdentifiers: [id], options: nil)
                if let asset = assets.firstObject {
                    assetLocation = asset.location
                    taken = asset.creationDate
                }
            }
            var exif: CLLocationCoordinate2D?
            if assetLocation == nil || taken == nil {
                let props = await fileProperties(result.itemProvider)
                exif = exifCoordinate(in: props)
                if taken == nil { taken = exifDate(in: props) }
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

        /// The file's own metadata block. Copied to a temporary url first
        /// because loadFileRepresentation deletes its file the moment the
        /// closure returns, and reading a CGImageSource is not instant.
        private static func fileProperties(_ provider: NSItemProvider) async -> [CFString: Any] {
            await withCheckedContinuation { cont in
                _ = provider.loadFileRepresentation(forTypeIdentifier: UTType.image.identifier) { url, _ in
                    guard let url,
                          let src = CGImageSourceCreateWithURL(url as CFURL, nil),
                          let props = CGImageSourceCopyPropertiesAtIndex(src, 0, nil)
                            as? [CFString: Any]
                    else { cont.resume(returning: [:]); return }
                    cont.resume(returning: props)
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
