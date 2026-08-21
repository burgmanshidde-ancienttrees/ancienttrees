// What Spot is, before you use it.
//
// The centre button opened straight into a list of nearby trees, which is
// the right screen for somebody who already knows what the button does and a
// riddle for everybody else (Hidde, 2026-08-21: "als je die opent moeten er
// gewoon wat uitleg staan").
//
// So the sheet opens tall, with a drawing, two sentences and two buttons: the
// thing you are here to do, and the other thing you might be here to do.

import SwiftUI

struct SpotIntro: View {
    let nearbyCount: Int
    var onCollect: () -> Void
    var onSuggest: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 18) {
            SpotDrawing()
                .frame(height: 190)
                .frame(maxWidth: .infinity)

            Text("Collect a tree by photographing it")
                .font(.brand(26, .heavy))
                .foregroundStyle(Brand.ink)
                .fixedSize(horizontal: false, vertical: true)

            Text("Stand in front of it, take the picture, and it joins your collection with the day and the place. Found one we do not have? Suggest it and we will look at it for the map.")
                .font(.body)
                .foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)

            Spacer(minLength: 0)

            Button(action: onCollect) {
                HStack { Spacer()
                    Label(nearbyCount > 0 ? "Collect a tree near me" : "Photograph a tree",
                          systemImage: "camera")
                        .font(.brand(17, .bold))
                    Spacer() }
                    .padding(.vertical, 15)
                    .background(Brand.moss, in: .rect(cornerRadius: 15))
                    .foregroundStyle(.white)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("spot-collect")

            Button(action: onSuggest) {
                HStack { Spacer()
                    Text("Suggest a new tree").font(.brand(16, .bold))
                    Spacer() }
                    .padding(.vertical, 13)
                    .background(Brand.surfaceMuted, in: .rect(cornerRadius: 15))
                    .foregroundStyle(Brand.ink)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("spot-suggest")
        }
    }
}

/// A person in front of a tree, drawn rather than photographed.
///
/// Line art on purpose: an illustration explains an idea, and a photograph of
/// a stranger would be a promise about a specific tree. Kept to a few strokes
/// so it reads at a glance and cannot be mistaken for a picture of something
/// real.
struct SpotDrawing: View {
    var body: some View {
        Canvas { ctx, size in
            let w = size.width, h = size.height
            let moss = Brand.moss
            let soft = Brand.moss.opacity(0.16)

            // The ground
            var ground = Path()
            ground.move(to: CGPoint(x: w * 0.12, y: h * 0.86))
            ground.addQuadCurve(to: CGPoint(x: w * 0.88, y: h * 0.86),
                                control: CGPoint(x: w * 0.5, y: h * 0.92))
            ctx.stroke(ground, with: .color(Brand.inkSoft.opacity(0.35)), lineWidth: 2)

            // The canopy: three overlapping rounds, the way anybody draws a tree
            for (cx, cy, r) in [(0.60, 0.34, 0.20), (0.74, 0.42, 0.15), (0.48, 0.44, 0.14)] {
                let rect = CGRect(x: w * (cx - r), y: h * (cy - r * w / h * 0.9),
                                  width: w * r * 2, height: w * r * 2 * 0.9)
                ctx.fill(Path(ellipseIn: rect), with: .color(soft))
                ctx.stroke(Path(ellipseIn: rect), with: .color(moss), lineWidth: 2)
            }
            // The trunk
            var trunk = Path()
            trunk.move(to: CGPoint(x: w * 0.62, y: h * 0.86))
            trunk.addLine(to: CGPoint(x: w * 0.62, y: h * 0.52))
            ctx.stroke(trunk, with: .color(moss), lineWidth: 2.5)

            // The person, small enough that the tree is the subject
            let px = w * 0.30, py = h * 0.86
            ctx.stroke(Path(ellipseIn: CGRect(x: px - 9, y: py - 62, width: 18, height: 18)),
                       with: .color(Brand.ink), lineWidth: 2)
            var body = Path()
            body.move(to: CGPoint(x: px, y: py - 44))
            body.addLine(to: CGPoint(x: px, y: py - 18))
            body.move(to: CGPoint(x: px, y: py - 18))
            body.addLine(to: CGPoint(x: px - 8, y: py))
            body.move(to: CGPoint(x: px, y: py - 18))
            body.addLine(to: CGPoint(x: px + 8, y: py))
            ctx.stroke(body, with: .color(Brand.ink), lineWidth: 2)

            // The phone, held up towards the tree
            let cam = CGRect(x: px + 6, y: py - 46, width: 16, height: 22)
            ctx.stroke(Path(roundedRect: cam, cornerRadius: 3), with: .color(Brand.ink), lineWidth: 2)
            var arm = Path()
            arm.move(to: CGPoint(x: px, y: py - 38))
            arm.addLine(to: CGPoint(x: px + 6, y: py - 36))
            ctx.stroke(arm, with: .color(Brand.ink), lineWidth: 2)
        }
    }
}
