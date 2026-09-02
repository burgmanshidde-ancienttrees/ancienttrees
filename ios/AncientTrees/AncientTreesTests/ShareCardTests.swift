// The share card is drawn in code, so nobody sees it unless something looks.
//
// A blank or half-drawn card is the kind of fault that ships silently: the
// button works, the sheet opens, and what leaves the phone is a black
// rectangle with our name on it. These assertions cannot judge whether it is
// any good, which is a session's job with eyes; they check that it exists, is
// the shape it claims, and is not one flat colour.
//
// It also writes the PNG to the test bundle's temporary directory and prints
// the path, so a session can open the thing it just rendered.

import XCTest
import SwiftUI
@testable import AncientTrees

@MainActor
final class ShareCardTests: XCTestCase {

    private func photo() -> UIImage {
        UIGraphicsImageRenderer(size: CGSize(width: 600, height: 800)).image { ctx in
            UIColor(red: 0.72, green: 0.83, blue: 0.90, alpha: 1).setFill()
            ctx.fill(CGRect(x: 0, y: 0, width: 600, height: 800))
            UIColor(red: 0.29, green: 0.42, blue: 0.20, alpha: 1).setFill()
            ctx.cgContext.fillEllipse(in: CGRect(x: -30, y: 60, width: 660, height: 520))
        }
    }

    func testTheCardIsDrawnAtTheSizeItPromises() throws {
        let card = ShareCard.render(photo: photo(), name: "The oak on my street",
                                    species: "Pedunculate Oak", date: Date(timeIntervalSince1970: 1_756_000_000))
        XCTAssertEqual(card.size.width, ShareCard.size.width)
        XCTAssertEqual(card.size.height, ShareCard.size.height)
        try write(card, "share-card.png")
    }

    /// A tree whose photograph has gone missing still gets a card, because a
    /// share button that works on most trees is a control nobody trusts.
    func testACardIsStillDrawnWithoutAPhotograph() throws {
        let card = ShareCard.render(photo: nil, name: "The lime by the water",
                                    species: nil, date: Date(timeIntervalSince1970: 1_756_000_000))
        XCTAssertEqual(card.size.width, ShareCard.size.width)
        try write(card, "share-card-nophoto.png")
    }

    /// Not one flat colour, which is what a card renders as when the content
    /// fails to lay out: ImageRenderer returns a picture either way.
    func testTheCardIsNotBlank() throws {
        let card = ShareCard.render(photo: photo(), name: "The oak on my street",
                                    species: nil, date: Date())
        let cg = try XCTUnwrap(card.cgImage)
        var seen = Set<UInt32>()
        let w = cg.width, h = cg.height
        var pixels = [UInt32](repeating: 0, count: w * h)
        let space = CGColorSpaceCreateDeviceRGB()
        let ctx = try XCTUnwrap(CGContext(data: &pixels, width: w, height: h,
                                          bitsPerComponent: 8, bytesPerRow: w * 4,
                                          space: space,
                                          bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue))
        ctx.draw(cg, in: CGRect(x: 0, y: 0, width: w, height: h))
        for y in stride(from: 0, to: h, by: 20) {
            for x in stride(from: 0, to: w, by: 20) { seen.insert(pixels[y * w + x]) }
        }
        XCTAssertGreaterThan(seen.count, 20, "the card is one flat colour, so nothing drew")
    }

    private func write(_ image: UIImage, _ name: String) throws {
        // SHARE_CARD_OUT lets a session put the picture somewhere it can open
        // it: the app's own temporary directory is inside a container that
        // xcodebuild deletes as the run ends, so the file is gone before
        // anybody can look. Pass it as TEST_RUNNER_SHARE_CARD_OUT.
        let dir = ProcessInfo.processInfo.environment["SHARE_CARD_OUT"]
            .map { URL(fileURLWithPath: $0) } ?? FileManager.default.temporaryDirectory
        let url = dir.appendingPathComponent(name)
        try XCTUnwrap(image.pngData()).write(to: url)
        print("share card written to \(url.path)")
    }
}
