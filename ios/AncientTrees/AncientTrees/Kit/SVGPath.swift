// A small SVG path parser, because the species silhouettes are the one thing our
// map has that AllTrails' does not and they are worth carrying over exactly.
//
// Scope is deliberately the commands our own icon set actually uses, measured
// rather than guessed: M m L l H h V v C c S s A a Z z, plus <ellipse>. Anything
// else is skipped rather than approximated, because a wrong curve on a tree
// silhouette is worse than a missing one.

import SwiftUI

enum SVG {
    /// Turn one icon fragment into a Path in a 40x40 box, the viewBox the
    /// website draws these in.
    static func path(_ fragment: String) -> Path {
        var path = Path()
        for d in datas(in: fragment, tag: "path") { append(d, to: &path) }
        for e in ellipses(in: fragment) {
            path.addEllipse(in: CGRect(x: e.cx - e.rx, y: e.cy - e.ry,
                                       width: e.rx * 2, height: e.ry * 2))
        }
        return path
    }

    private static func datas(in s: String, tag: String) -> [String] {
        var out: [String] = []
        var rest = Substring(s)
        while let open = rest.range(of: "<\(tag) ") {
            rest = rest[open.upperBound...]
            // Whichever comes FIRST, not whichever is non-nil. `<path d="…"`
            // has no space before d, so `?? ` picked up the ` d="` of a LATER
            // tag and silently skipped this path: the cedar drew one tier of
            // three. Every icon with a bare `<path d=` lost paths this way.
            let spaced = rest.range(of: " d=\"")
            let bare = rest.range(of: "d=\"")
            let candidates = [spaced, bare].compactMap { $0 }
            guard let dRange = candidates.min(by: { $0.lowerBound < $1.lowerBound }),
                  let close = rest[dRange.upperBound...].firstIndex(of: "\"") else { continue }
            out.append(String(rest[dRange.upperBound..<close]))
        }
        return out
    }

    private struct Ellipse { let cx, cy, rx, ry: CGFloat }

    private static func ellipses(in s: String) -> [Ellipse] {
        var out: [Ellipse] = []
        var rest = Substring(s)
        while let open = rest.range(of: "<ellipse") {
            rest = rest[open.upperBound...]
            let end = rest.firstIndex(of: ">") ?? rest.endIndex
            let tag = String(rest[..<end])
            func attr(_ n: String) -> CGFloat {
                guard let r = tag.range(of: "\(n)=\"") else { return 0 }
                let after = tag[r.upperBound...]
                let v = after.prefix { $0 != "\"" }
                return CGFloat(Double(v) ?? 0)
            }
            out.append(Ellipse(cx: attr("cx"), cy: attr("cy"),
                               rx: attr("rx"), ry: attr("ry")))
        }
        return out
    }

    private static func append(_ d: String, to path: inout Path) {
        var cursor = CGPoint.zero
        var start = CGPoint.zero
        var lastControl: CGPoint?
        var i = d.startIndex
        var command: Character = "M"

        func nums(_ count: Int) -> [CGFloat] {
            var out: [CGFloat] = []
            while out.count < count {
                while i < d.endIndex, d[i] == " " || d[i] == "," { i = d.index(after: i) }
                var s = ""
                if i < d.endIndex, d[i] == "-" || d[i] == "+" { s.append(d[i]); i = d.index(after: i) }
                while i < d.endIndex, d[i].isNumber || d[i] == "." {
                    // a second dot starts the next number: "1.5.5" is 1.5 then .5
                    if d[i] == ".", s.contains(".") { break }
                    s.append(d[i]); i = d.index(after: i)
                }
                guard let v = Double(s) else { return out }
                out.append(CGFloat(v))
            }
            return out
        }

        while i < d.endIndex {
            if d[i].isLetter { command = d[i]; i = d.index(after: i) }
            let rel = command.isLowercase
            func pt(_ v: [CGFloat], _ o: Int = 0) -> CGPoint {
                rel ? CGPoint(x: cursor.x + v[o], y: cursor.y + v[o + 1])
                    : CGPoint(x: v[o], y: v[o + 1])
            }
            switch Character(command.lowercased()) {
            case "m":
                let v = nums(2); guard v.count == 2 else { return }
                cursor = pt(v); start = cursor; path.move(to: cursor)
                command = rel ? "l" : "L"
            case "l":
                let v = nums(2); guard v.count == 2 else { return }
                cursor = pt(v); path.addLine(to: cursor)
            case "h":
                let v = nums(1); guard v.count == 1 else { return }
                cursor.x = rel ? cursor.x + v[0] : v[0]; path.addLine(to: cursor)
            case "v":
                let v = nums(1); guard v.count == 1 else { return }
                cursor.y = rel ? cursor.y + v[0] : v[0]; path.addLine(to: cursor)
            case "c":
                let v = nums(6); guard v.count == 6 else { return }
                let c1 = pt(v, 0), c2 = pt(v, 2), end = pt(v, 4)
                path.addCurve(to: end, control1: c1, control2: c2)
                lastControl = c2; cursor = end
            case "s":
                let v = nums(4); guard v.count == 4 else { return }
                let c1 = lastControl.map { CGPoint(x: 2 * cursor.x - $0.x, y: 2 * cursor.y - $0.y) } ?? cursor
                let c2 = pt(v, 0), end = pt(v, 2)
                path.addCurve(to: end, control1: c1, control2: c2)
                lastControl = c2; cursor = end
            case "a":
                let v = nums(7); guard v.count == 7 else { return }
                let end = rel ? CGPoint(x: cursor.x + v[5], y: cursor.y + v[6])
                              : CGPoint(x: v[5], y: v[6])
                arc(&path, from: cursor, to: end, rx: v[0], ry: v[1],
                    rotation: v[2], largeArc: v[3] != 0, sweep: v[4] != 0)
                cursor = end
            case "z":
                path.closeSubpath(); cursor = start
            default:
                i = d.endIndex
            }
            if Character(command.lowercased()) != "c" && Character(command.lowercased()) != "s" {
                lastControl = nil
            }
        }
    }

    /// Endpoint-parameterised arc to centre form, per the SVG spec's appendix.
    /// Our icons use arcs only for the small round fruit on plane and wingnut,
    /// but a wrong one is very visible at card size.
    private static func arc(_ path: inout Path, from p0: CGPoint, to p1: CGPoint,
                            rx: CGFloat, ry: CGFloat, rotation: CGFloat,
                            largeArc: Bool, sweep: Bool) {
        guard rx != 0, ry != 0 else { path.addLine(to: p1); return }
        var rx = abs(rx), ry = abs(ry)
        let phi = rotation * .pi / 180
        let dx2 = (p0.x - p1.x) / 2, dy2 = (p0.y - p1.y) / 2
        let x1 = cos(phi) * dx2 + sin(phi) * dy2
        let y1 = -sin(phi) * dx2 + cos(phi) * dy2
        var lambda = (x1 * x1) / (rx * rx) + (y1 * y1) / (ry * ry)
        if lambda > 1 { let s = sqrt(lambda); rx *= s; ry *= s; lambda = 1 }
        let sign: CGFloat = largeArc == sweep ? -1 : 1
        let num = max(0, rx * rx * ry * ry - rx * rx * y1 * y1 - ry * ry * x1 * x1)
        let den = rx * rx * y1 * y1 + ry * ry * x1 * x1
        let co = sign * sqrt(den == 0 ? 0 : num / den)
        let cxp = co * rx * y1 / ry, cyp = -co * ry * x1 / rx
        let cx = cos(phi) * cxp - sin(phi) * cyp + (p0.x + p1.x) / 2
        let cy = sin(phi) * cxp + cos(phi) * cyp + (p0.y + p1.y) / 2
        func angle(_ ux: CGFloat, _ uy: CGFloat) -> CGFloat { atan2(uy, ux) }
        let theta = angle((x1 - cxp) / rx, (y1 - cyp) / ry)
        var delta = angle((-x1 - cxp) / rx, (-y1 - cyp) / ry) - theta
        if !sweep, delta > 0 { delta -= 2 * .pi }
        if sweep, delta < 0 { delta += 2 * .pi }
        // Approximate with a transformed ellipse arc.
        let m = CGAffineTransform(translationX: cx, y: cy)
            .rotated(by: phi)
            .scaledBy(x: rx, y: ry)
        var sub = Path()
        sub.addArc(center: .zero, radius: 1, startAngle: .radians(theta),
                   endAngle: .radians(theta + delta), clockwise: delta < 0)
        path.addPath(sub, transform: m)
    }
}

/// A species silhouette, drawn at any size.
struct SpeciesMark: View {
    let species: String
    var color: Color = .white

    var body: some View {
        GeometryReader { geo in
            let s = min(geo.size.width, geo.size.height) / 40
            SVG.path(SpeciesIcons.fragment(for: species))
                .applying(CGAffineTransform(scaleX: s, y: s))
                .fill(color)
                .frame(width: geo.size.width, height: geo.size.height, alignment: .center)
        }
    }
}
