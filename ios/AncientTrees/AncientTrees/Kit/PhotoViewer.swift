// The photograph, full screen, and the one place it is opened.
//
// Convention: Apple Photos and every iOS viewer that copies it, recorded in
// CONVENTIONS.md 2026-09-03. People arrive already trained, so none of this is
// ours to invent: pinch to zoom and pan, double tap to zoom in and out at once,
// drag DOWN to dismiss, single tap to hide the chrome and leave only the
// picture. The one people complain about when it is missing is the drag, which
// is the gesture a thumb reaches for first.
//
// The other half is Wikipedia's Media Viewer, for the same reason the website's
// lightbox follows it: our photographs carry licences that oblige a credit, and
// the credit belongs UNDER the picture in the viewer rather than painted over
// the trunk on a card (Hidde, 2026-08-20).
//
// "Open it fully" means the original file, and that is loaded on ZOOM rather
// than on open. The hero is 1280 and arrives instantly from the cache the card
// already filled; an original can be eight thousand pixels across and several
// megabytes, which is a fine thing to fetch for somebody who has just pinched
// into the bark and a rude thing to fetch for somebody who tapped by accident.
// Both go through TreePhoto, so the retry, the gate and the decoded cache are
// the ones the rest of the app already uses.

import SwiftUI

struct PhotoViewer: View {
    let photo: Photo
    let title: String
    @Binding var isPresented: Bool

    @State private var scale: CGFloat = 1
    @State private var steady: CGFloat = 1
    @State private var offset: CGSize = .zero
    @State private var settled: CGSize = .zero
    @State private var dragDown: CGFloat = 0
    @State private var chrome = true
    /// Set the first time somebody zooms in, and never unset: once the original
    /// has been asked for there is nothing to gain by dropping it again.
    @State private var wantsOriginal = false

    private var original: URL? { URL(string: photo.url) }

    var body: some View {
        ZStack {
            Color.black.ignoresSafeArea()
                .opacity(1 - min(dragDown / 400, 0.6))

            picture
                .scaleEffect(scale)
                .offset(x: offset.width, y: offset.height + dragDown)
                .gesture(magnify)
                .simultaneousGesture(pan)
                .onTapGesture(count: 2) { doubleTap() }
                .onTapGesture { withAnimation(.easeInOut(duration: 0.15)) { chrome.toggle() } }

            if chrome {
                VStack {
                    HStack {
                        Spacer()
                        Button { isPresented = false } label: {
                            Image(systemName: "xmark")
                                .font(.system(size: 15, weight: .semibold))
                                .foregroundStyle(.white)
                                // 44, which is the floor every phone platform
                                // asks of a control and the number appfit reads.
                                .frame(width: 44, height: 44)
                                .background(.black.opacity(0.45), in: Circle())
                        }
                        .accessibilityLabel("Close")
                        .accessibilityIdentifier("photo-close")
                    }
                    .padding(.horizontal, 8)
                    Spacer()
                    if let credit = Photos.credit(photo) {
                        Text(credit)
                            .font(.caption2)
                            .foregroundStyle(.white.opacity(0.85))
                            .multilineTextAlignment(.center)
                            .padding(.horizontal, 20)
                            .padding(.bottom, 16)
                    }
                }
                .transition(.opacity)
            }
        }
        .statusBarHidden()
        .accessibilityIdentifier("photo-viewer")
    }

    @ViewBuilder private var picture: some View {
        ZStack {
            TreePhoto(url: photo.full, contentMode: .fit) {
                ProgressView().tint(.white)
            }
            // Laid OVER the hero rather than replacing it, so the picture never
            // blinks back to a spinner while the big file is on its way.
            if wantsOriginal, let original {
                TreePhoto(url: original, contentMode: .fit) { Color.clear }
            }
        }
    }

    private var magnify: some Gesture {
        MagnifyGesture()
            .onChanged { v in scale = max(1, min(steady * v.magnification, 6)) }
            .onEnded { _ in
                steady = scale
                if scale > 1.2 { wantsOriginal = true }
                if scale <= 1 { reset() }
            }
    }

    private var pan: some Gesture {
        DragGesture()
            .onChanged { v in
                // At rest the drag is the dismissal; zoomed in it is panning,
                // because somebody moving around a trunk must not be thrown out
                // of the viewer for dragging downward.
                if scale > 1 {
                    offset = CGSize(width: settled.width + v.translation.width,
                                    height: settled.height + v.translation.height)
                } else {
                    dragDown = max(0, v.translation.height)
                }
            }
            .onEnded { v in
                if scale > 1 { settled = offset; return }
                if v.translation.height > 90 { isPresented = false }
                else { withAnimation(.easeOut(duration: 0.2)) { dragDown = 0 } }
            }
    }

    private func doubleTap() {
        withAnimation(.easeInOut(duration: 0.2)) {
            if scale > 1 { reset() } else { scale = 2.5; steady = 2.5; wantsOriginal = true }
        }
    }

    private func reset() {
        scale = 1; steady = 1; offset = .zero; settled = .zero
    }
}
