// What the centre button is for, before you use it.
//
// It used to explain two verbs at once, because the button did two jobs at
// once. Since 2026-08-22 it does one: ADD a tree we do not have. Claiming a
// tree we DO have moved to Collect, where your collection is, which is the
// confusion Hidde named ("het vreemde is natuurlijk dat de vierde collect
// heet terwijl je bij Spot eigenlijk het daadwerkelijke collect doet").

import SwiftUI

struct AddIntro: View {
    var onStart: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 18) {
            SpotDrawing()
                .frame(height: 180)
                .frame(maxWidth: .infinity)

            Text("Add a tree we do not have")
                .font(.brand(26, .heavy))
                .foregroundStyle(Brand.ink)
                .fixedSize(horizontal: false, vertical: true)

            Text("Photograph any tree you want to keep and it joins your own trees. And if it is a remarkable old one, tell us: we check it, and it can join the map everybody sees.")
                .font(.body)
                .foregroundStyle(Brand.inkSoft)
                .fixedSize(horizontal: false, vertical: true)

            Spacer(minLength: 0)

            Button(action: onStart) {
                HStack { Spacer()
                    Label("Add a tree", systemImage: "camera").font(.brand(17, .bold))
                    Spacer() }
                    .padding(.vertical, 15)
                    .background(Brand.moss, in: .rect(cornerRadius: 15))
                    .foregroundStyle(.white)
            }
            .buttonStyle(.plain)
            .accessibilityIdentifier("add-start")
        }
    }
}

/// A person in front of a tree, drawn rather than photographed.
///
/// Line art on purpose: an illustration explains an idea, and a photograph of
/// a stranger would be a promise about a specific tree.
struct SpotDrawing: View {
    var body: some View {
        Canvas { ctx, size in
            let w = size.width, h = size.height
            let moss = Brand.moss
            let soft = Brand.moss.opacity(0.16)

            var ground = Path()
            ground.move(to: CGPoint(x: w * 0.12, y: h * 0.86))
            ground.addQuadCurve(to: CGPoint(x: w * 0.88, y: h * 0.86),
                                control: CGPoint(x: w * 0.5, y: h * 0.92))
            ctx.stroke(ground, with: .color(Brand.inkSoft.opacity(0.35)), lineWidth: 2)

            for (cx, cy, r) in [(0.60, 0.34, 0.20), (0.74, 0.42, 0.15), (0.48, 0.44, 0.14)] {
                let rect = CGRect(x: w * (cx - r), y: h * (cy - r * w / h * 0.9),
                                  width: w * r * 2, height: w * r * 2 * 0.9)
                ctx.fill(Path(ellipseIn: rect), with: .color(soft))
                ctx.stroke(Path(ellipseIn: rect), with: .color(moss), lineWidth: 2)
            }
            var trunk = Path()
            trunk.move(to: CGPoint(x: w * 0.62, y: h * 0.86))
            trunk.addLine(to: CGPoint(x: w * 0.62, y: h * 0.52))
            ctx.stroke(trunk, with: .color(moss), lineWidth: 2.5)

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

            let cam = CGRect(x: px + 6, y: py - 46, width: 16, height: 22)
            ctx.stroke(Path(roundedRect: cam, cornerRadius: 3), with: .color(Brand.ink), lineWidth: 2)
            var arm = Path()
            arm.move(to: CGPoint(x: px, y: py - 38))
            arm.addLine(to: CGPoint(x: px + 6, y: py - 36))
            ctx.stroke(arm, with: .color(Brand.ink), lineWidth: 2)
        }
    }
}
