// The camera, wrapped thinly.
//
// UIImagePickerController rather than a hand-built AVCapture screen: the
// system camera is the control every phone owner already knows, and inventing
// a viewfinder is exactly the kind of thing the convention rule forbids.
//
// It falls back to the photo library where there is no camera, which is every
// simulator, so the flow can be built and screenshotted at all.

import AVFoundation
import SwiftUI
import UIKit

struct CameraPicker: UIViewControllerRepresentable {
    var onPicked: (UIImage?) -> Void
    @Environment(\.dismiss) private var dismiss

    func makeUIViewController(context: Context) -> UIImagePickerController {
        let p = UIImagePickerController()
        p.sourceType = Self.source(
            cameraAvailable: UIImagePickerController.isSourceTypeAvailable(.camera),
            authorization: AVCaptureDevice.authorizationStatus(for: .video))
        p.delegate = context.coordinator
        return p
    }

    /// WHICH SOURCE, as a decision rather than a line inside makeUIViewController,
    /// because a simulator has no camera and can therefore never run the camera
    /// path at all. Pulled out so all four authorisation states can be tested
    /// on a machine that has no camera to deny.
    ///
    /// The bug this fixes (2026-08-27): the check used to be
    /// isSourceTypeAvailable(.camera) alone, which asks whether the hardware
    /// EXISTS and not whether we may use it. Somebody who had tapped "Don't
    /// Allow" once, months ago, got a black rectangle with a Cancel button and
    /// no word of explanation, on the one screen that is the core act of this
    /// app. Nothing in the simulator could ever have shown that, because a
    /// simulator has no camera and quietly took the other branch every time.
    static func source(cameraAvailable: Bool,
                       authorization: AVAuthorizationStatus) -> UIImagePickerController.SourceType {
        guard cameraAvailable else { return .photoLibrary }
        switch authorization {
        case .authorized:
            return .camera
        case .notDetermined:
            // Presenting the camera is what triggers the system prompt, and
            // that prompt is the right place to ask: the person has just
            // tapped a button that says photograph a tree.
            return .camera
        case .denied, .restricted:
            // Never a black rectangle. The library is a screen that explains
            // itself by looking like the Photos app, and the task can still be
            // finished from it.
            return .photoLibrary
        @unknown default:
            return .photoLibrary
        }
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
