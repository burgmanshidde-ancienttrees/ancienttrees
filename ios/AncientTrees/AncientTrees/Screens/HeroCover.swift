// The frame the app opens on: a tree, the promise, and then out of the way.
//
// Hidde asked for this four times on 2026-08-29 and I redirected it three, so
// the note in ContentView.swift explains what I had wrong. Short version: an
// iOS launch screen cannot rotate a photograph, a cover the app draws itself
// can, and that is what he meant.
//
// WHAT KEEPS IT HONEST. It is not a splash screen in the sense Apple warns
// about, because it never blocks anybody: it leaves on its own after 1.4
// seconds, a tap anywhere takes it away at once, and the map underneath is
// already loading behind it. Somebody who opens this app may be standing
// outside in the cold.
//
// The photograph is Heroes.current, which is resolved once per launch, so the
// frame you open on is the same one Discover is wearing when you get there.

import SwiftUI

struct HeroCover: View {
    let photo: UIImage
    let dismiss: () -> Void

    var body: some View {
        // A READER FOR THE BOUNDS, then the photograph forced to exactly those
        // bounds and clipped.
        //
        // Two bugs live in this one block and both shipped once. A .fill image
        // is wider than the screen by design, so in a plain ZStack it sets the
        // stack's width and .bottomLeading aligned the words to the
        // photograph's left edge, off screen: the first build read "orth the
        // walk,". And ignoresSafeArea() applied to the image alone left the
        // status bar white and a strip of app showing at the bottom, because
        // the clip that followed it used the safe frame. Sizing from the reader
        // and ignoring the safe area LAST fixes both.
        GeometryReader { geo in
            Image(uiImage: photo)
                .resizable()
                .aspectRatio(contentMode: .fill)
                .frame(width: geo.size.width, height: geo.size.height)
                .clipped()
                .overlay {
                    // Dark from the middle down, so the words sit on the tree's
                    // own shade rather than on a bar laid over it.
                    LinearGradient(colors: [.clear, .black.opacity(0.72)],
                                   startPoint: .center, endPoint: .bottom)
                }
                .overlay(alignment: .bottomLeading) {
                    VStack(alignment: .leading, spacing: 2) {
                        Text("Trees worth the walk,")
                            .foregroundStyle(.white)
                        Text("wherever you are.")
                            .foregroundStyle(Brand.gold)
                    }
                    .font(.brand(30, .bold, relativeTo: .title))
                    .shadow(color: .black.opacity(0.4), radius: 10, y: 2)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(.horizontal, 24)
                    .padding(.bottom, 110)
                }
        }
        .background(Color.black)
        .ignoresSafeArea()
        .contentShape(.rect)
        .onTapGesture(perform: dismiss)
        .accessibilityElement(children: .combine)
        .accessibilityLabel("Trees worth the walk, wherever you are")
        .accessibilityAddTraits(.isButton)
        .accessibilityHint("Tap to continue")
    }
}
