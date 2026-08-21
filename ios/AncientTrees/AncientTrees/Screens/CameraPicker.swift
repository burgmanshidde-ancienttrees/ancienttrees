// The camera, wrapped thinly.
//
// UIImagePickerController rather than a hand-built AVCapture screen: the
// system camera is the control every phone owner already knows, and inventing
// a viewfinder is exactly the kind of thing the convention rule forbids.
//
// It falls back to the photo library where there is no camera, which is every
// simulator, so the flow can be built and screenshotted at all.

import SwiftUI
import UIKit

struct CameraPicker: UIViewControllerRepresentable {
    var onPicked: (UIImage?) -> Void
    @Environment(\.dismiss) private var dismiss

    func makeUIViewController(context: Context) -> UIImagePickerController {
        let p = UIImagePickerController()
        p.sourceType = UIImagePickerController.isSourceTypeAvailable(.camera)
            ? .camera : .photoLibrary
        p.delegate = context.coordinator
        return p
    }

    func updateUIViewController(_ c: UIImagePickerController, context: Context) {}

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    final class Coordinator: NSObject, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
        let parent: CameraPicker
        init(_ p: CameraPicker) { parent = p }

        func imagePickerController(_ picker: UIImagePickerController,
                                   didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey: Any]) {
            parent.onPicked(info[.originalImage] as? UIImage)
            parent.dismiss()
        }

        func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
            parent.onPicked(nil)
            parent.dismiss()
        }
    }
}
