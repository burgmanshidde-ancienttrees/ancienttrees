// A copy of every photograph taken with the app's camera, in your own Photos.
//
// Convention: iNaturalist saves each photograph its camera takes to the camera
// roll by default, and what its users ask for is the opposite of a way in: a
// switch to turn it off, and the location travelling with the copy
// (CONVENTIONS.md 2026-09-11). Hidde, the same day, on finding his Kyoto
// photographs only inside the app: "doe dit maar dit willen mensen".
//
// ADD-ONLY permission, the smallest thing iOS offers: the app can put a picture
// into Photos and never read one back. Refused is not an error. The photograph
// is still recorded in the app; it simply is not copied.

import CoreLocation
import Photos
import UIKit

enum CameraRoll {
    static func keep(_ image: UIImage) {
        guard let data = image.jpegData(compressionQuality: 0.92) else { return }
        // The phone's last fix, which on the camera path is where the shutter
        // fell. UIImagePickerController hands back pixels without the camera's
        // own GPS, so without this the copy would say nowhere.
        let here = CLLocationManager().location
        let lat = here?.coordinate.latitude, lng = here?.coordinate.longitude
        Task.detached(priority: .utility) {
            let status = await PHPhotoLibrary.requestAuthorization(for: .addOnly)
            guard status == .authorized || status == .limited else { return }
            try? await PHPhotoLibrary.shared().performChanges {
                let r = PHAssetCreationRequest.forAsset()
                r.addResource(with: .photo, data: data, options: nil)
                r.creationDate = Date()
                if let lat, let lng { r.location = CLLocation(latitude: lat, longitude: lng) }
            }
        }
    }
}
