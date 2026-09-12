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
    var photo: Photo? = nil
    /// The whole set, when the tree has more than one (2026-09-12). Empty means
    /// `photo` alone, so every existing call site is unchanged.
    var photos: [Photo] = []
    /// Which one to open on. A thumbnail must open AT ITS OWN PICTURE; opening
    /// every thumbnail on the first is the fault that makes a strip feel broken.
    var startAt: Int = 0
    let title: String
    @Binding var isPresented: Bool
    /// A photograph on this phone rather than one of ours: your own, of a tree
    /// you stood in front of. Same viewer and same gestures; no credit, since
    /// nobody but you is being shown it.
    var local: UIImage? = nil

    @State private var scale: CGFloat = 1
    @State private var steady: CGFloat = 1
    @State private var offset: CGSize = .zero
    @State private var settled: CGSize = .zero
    @State private var dragDown: CGFloat = 0
    @State private var chrome = true
    /// Set the first time somebody zooms in, and never unset: once the original
    /// has been asked for there is nothing to gain by dropping it again.
    @State private var wantsOriginal = false
    /// Where in the set we are. Set from `startAt` on appear rather than in an
    /// initialiser, so the memberwise one keeps working at every call site.
    @State private var at = 0

    /// The set to page through, and the one photograph on screen. `shown` is
    /// the only thing the picture and the credit read, so they cannot disagree.
    private var set: [Photo] { photos.isEmpty ? (photo.map { [$0] } ?? []) : photos }
    private var shown: Photo? { set.indices.contains(at) ? set[at] : photo }
    private var original: URL? { shown.flatMap { URL(string: $0.url) } }

    /// Wrap, the way every photo viewer does: paging past the end of three
    /// pictures returns to the first rather than dead-ending. Zoom resets with
    /// the page, because arriving at the next photograph already magnified and
    /// panned to a corner of the last one is disorienting.
    private func page(_ by: Int) {
        guard set.count > 1 else { return }
        reset()
        wantsOriginal = false
        withAnimation(.easeInOut(duration: 0.18)) {
            at = ((at + by) % set.count + set.count) % set.count
        }
    }

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
                    VStack(spacing: 6) {
                        // The counter is the affordance, which is how Google
                        // Maps' photo viewer says there is more: no chevrons,
                        // because Apple Photos has none and a swipe is what an
                        // iOS reader already reaches for. It is also the only
                        // thing on screen saying a second picture exists.
                        if set.count > 1 {
                            Text("\(at + 1) of \(set.count)")
                                .font(.caption2.weight(.semibold))
                                .foregroundStyle(.white.opacity(0.9))
                                .accessibilityIdentifier("photo-count")
                        }
                        if let photo = shown, let credit = Photos.credit(photo) {
                            Text(credit)
                                .font(.caption2)
                                .foregroundStyle(.white.opacity(0.85))
                                .multilineTextAlignment(.center)
                                .padding(.horizontal, 20)
                        }
                    }
                    .padding(.bottom, 16)
                }
                .transition(.opacity)
            }
        }
        .statusBarHidden()
        .accessibilityIdentifier("photo-viewer")
        .onAppear { at = set.indices.contains(startAt) ? startAt : 0 }
    }

    @ViewBuilder private var picture: some View {
        ZStack {
            if let local {
                Image(uiImage: local).resizable().aspectRatio(contentMode: .fit)
            } else if let photo = shown {
                TreePhoto(url: photo.full, contentMode: .fit) {
                    ProgressView().tint(.white)
                }
                // Laid OVER the hero rather than replacing it, so the picture
                // never blinks back to a spinner while the big file is on its
                // way.
                if wantsOriginal, let original {
                    TreePhoto(url: original, contentMode: .fit) { Color.clear }
                }
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
                    // Only downward follows the finger. A sideways drag pages
                    // on release rather than sliding, which keeps this a few
                    // lines instead of a second gesture machine fighting zoom.
                    let d = v.translation
                    dragDown = abs(d.width) > abs(d.height) ? 0 : max(0, d.height)
                }
            }
            .onEnded { v in
                if scale > 1 { settled = offset; return }
                let d = v.translation
                // Which gesture it WAS is decided at the end by the axis that
                // moved further, so a slightly crooked swipe still does what
                // the thumb meant. Same rule as the website's lightbox.
                if abs(d.width) > abs(d.height), abs(d.width) > 60, set.count > 1 {
                    withAnimation(.easeOut(duration: 0.2)) { dragDown = 0 }
                    page(d.width < 0 ? 1 : -1)
                } else if d.height > 90 {
                    isPresented = false
                } else {
                    withAnimation(.easeOut(duration: 0.2)) { dragDown = 0 }
                }
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
