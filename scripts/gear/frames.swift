// frames.swift - read a screen recording as a series of images.
//
// Hidde, 2026-08-19: "kun je trouwens met alltrails ook met een screenrecording
// werken?" Not directly: video is not something I can watch. Frames are, and a
// recording carries what screenshots cannot, which is the INTERACTION: what a
// sheet does between closed and open, where a transition starts, what happens
// on a tap. For copying another product's behaviour that is the difference
// between guessing and looking.
//
// macOS ships AVFoundation and a Swift compiler and this machine has neither
// ffmpeg nor Homebrew, so this needs nothing installed.
//
//   swiftc -O scripts/gear/frames.swift -o /tmp/frames
//   /tmp/frames ~/Desktop/alltrails.mov /tmp/at 12
//
// Then the PNGs in /tmp/at are readable one by one. Twelve frames covers a
// thirty second recording well; ask for more when the thing you care about is
// a fast transition.
//
// Verified 2026-08-19 against a synthetic clip: six frames from three seconds,
// each a visibly different moment.

// Pull evenly spaced frames out of a screen recording, so a video can be read
// as a series of images. macOS ships AVFoundation and a Swift compiler; it
// ships no ffmpeg and this machine has no Homebrew, so this is the route that
// needs nothing installed.
import AVFoundation
import AppKit

let args = CommandLine.arguments
guard args.count >= 3 else {
    print("usage: frames <video> <outdir> [count]"); exit(1)
}
let url = URL(fileURLWithPath: args[1])
let outDir = URL(fileURLWithPath: args[2], isDirectory: true)
let count = args.count > 3 ? (Int(args[3]) ?? 12) : 12

let asset = AVURLAsset(url: url)
let seconds = CMTimeGetSeconds(asset.duration)
guard seconds.isFinite, seconds > 0 else { print("no readable duration"); exit(1) }

try? FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)

let gen = AVAssetImageGenerator(asset: asset)
gen.appliesPreferredTrackTransform = true
// A screen recording is mostly still; without tolerances the generator snaps
// to keyframes and hands back the same frame several times.
gen.requestedTimeToleranceBefore = .zero
gen.requestedTimeToleranceAfter = .zero
// Frames come out at recording resolution, which for a phone recording is
// enormous; cap the long edge so a reader gets a legible image, not a wall.
gen.maximumSize = CGSize(width: 1000, height: 1000)

print(String(format: "duration %.1fs, writing %d frames", seconds, count))
var written = 0
for i in 0..<count {
    let t = seconds * (Double(i) + 0.5) / Double(count)
    let time = CMTime(seconds: t, preferredTimescale: 600)
    do {
        let cg = try gen.copyCGImage(at: time, actualTime: nil)
        let rep = NSBitmapImageRep(cgImage: cg)
        guard let data = rep.representation(using: .png, properties: [:]) else { continue }
        let out = outDir.appendingPathComponent(String(format: "frame-%02d.png", i + 1))
        try data.write(to: out)
        written += 1
        print(String(format: "  %.1fs -> %@", t, out.lastPathComponent))
    } catch {
        print(String(format: "  %.1fs failed: %@", t, "\(error)"))
    }
}
print("\(written) frame(s) written to \(outDir.path)")
