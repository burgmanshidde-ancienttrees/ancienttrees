// One place the app loads a photograph, because AsyncImage cannot be made
// reliable and this app kept proving it.
//
// Hidde, 2026-08-29: "plaatjes laden weer niet hoe maken we dat stabiel". The
// same complaint on 2026-08-27 was answered by serving the card images off our
// own domain, which removed the CAUSE of the burst (Wikimedia rate-limits: a
// grid of 24 thumbnails came back 13 x HTTP 429). That fix was right and it is
// not enough, for two reasons measured since.
//
// The heroes were deliberately left on Wikimedia, all 337 of them, because a
// hero is one image on one screen and never bursts. True, and a single request
// still fails sometimes, and that is where AsyncImage falls down: it has no
// retry at all. One 429, one dropped connection in a wood, and that view shows
// its placeholder until it is rebuilt from scratch. There is no second attempt,
// ever.
//
// And nothing was ever cached in a way a scroll could use. AsyncImage keeps
// nothing itself, so scrolling a shelf away and back re-requests every card,
// which turns one burst into one burst per pass. URLCache is under it, but the
// system default is 512 KB of memory and it holds compressed bytes, so every
// reappearance also re-decodes.
//
// Convention: this is what SDWebImage and Kingfisher do, and what Apple's own
// AsyncImage documentation says to write when you need more than it gives.
// Neither library is added, because a dependency inside the product needs
// Hidde's yes (hard rule 5) and this is eighty lines.
//
// Four properties, and each one answers a failure that has actually happened:
//
//   RETRY, three attempts with a growing wait, honouring Retry-After when the
//   server sends one. A 429 is a "not now", not a "no".
//   DECODED IN MEMORY, so a photograph already seen reappears with no request
//   and no decode when you scroll back to it.
//   FOUR AT A TIME, so a shelf asks politely rather than opening twenty
//   connections at once. Everything else waits its turn instead of failing.
//   ONE REQUEST PER URL, so the same photograph on a card and in a list is
//   fetched once even when both appear in the same frame.

import SwiftUI
import UIKit

/// Four at a time, and the rest wait rather than fail.
actor ImageGate {
    private let limit: Int
    private var running = 0
    private var waiting: [CheckedContinuation<Void, Never>] = []

    init(limit: Int) { self.limit = limit }

    func acquire() async {
        if running < limit { running += 1; return }
        await withCheckedContinuation { waiting.append($0) }
    }

    /// The slot is handed straight to whoever is next, so `running` only falls
    /// when nobody is waiting for it.
    func release() {
        if waiting.isEmpty { running -= 1 }
        else { waiting.removeFirst().resume() }
    }
}

@MainActor
final class ImageStore {
    static let shared = ImageStore()

    /// Decoded images. Counted in bytes rather than in pictures, because a
    /// hero and a thumbnail are not the same size and a count of 100 means
    /// nothing.
    private let memory: NSCache<NSURL, UIImage> = {
        let c = NSCache<NSURL, UIImage>()
        c.totalCostLimit = 64 * 1024 * 1024
        return c
    }()

    private var inFlight: [URL: Task<UIImage?, Never>] = [:]
    /// EIGHT, not four. Four was set while every card image came from
    /// Wikimedia, which rate-limits a burst into HTTP 429; since 2026-08-27 the
    /// cards are served from our own domain and the only thing a small number
    /// buys there is a slower scroll. Eight is still a third of the burst that
    /// caused the 429s, so the heroes, which are still Wikimedia's, keep their
    /// protection.
    private let gate = ImageGate(limit: 8)

    private init() {}

    /// Somewhere for the bytes to live between launches. URLCache's default on
    /// iOS is 512 KB in memory and a few megabytes on disk, which a hundred
    /// photographs walk straight through. Called once at launch.
    nonisolated static func prepareCache() {
        URLCache.shared = URLCache(memoryCapacity: 16 * 1024 * 1024,
                                   diskCapacity: 256 * 1024 * 1024,
                                   directory: nil)
    }

    /// What is already in hand, with no waiting at all. A view asks this first
    /// so a photograph it has seen appears in the same frame rather than one
    /// after it, which is the flicker on every scroll back.
    func cached(_ url: URL) -> UIImage? { memory.object(forKey: url as NSURL) }

    func image(for url: URL) async -> UIImage? {
        if let hit = cached(url) { return hit }
        if let running = inFlight[url] { return await running.value }
        // Task, not Task.detached: it inherits MainActor, so the two lines
        // that touch the cache below need no hop. The fetch itself is
        // nonisolated and therefore runs off the main thread, which is what
        // keeps a decoding JPEG out of the scroll.
        let task = Task<UIImage?, Never> { [gate] in
            await gate.acquire()
            let image = await Self.fetch(url)
            await gate.release()
            if let image {
                self.memory.setObject(image, forKey: url as NSURL, cost: Self.cost(of: image))
            }
            self.inFlight[url] = nil
            return image
        }
        inFlight[url] = task
        return await task.value
    }

    nonisolated private static func cost(of image: UIImage) -> Int {
        Int(image.size.width * image.scale * image.size.height * image.scale * 4)
    }

    /// Three attempts, then an honest gap. Nothing here is shown to anybody:
    /// a photograph that will not come is the same missing photograph the rest
    /// of this app already knows how to draw around.
    nonisolated private static func fetch(_ url: URL) async -> UIImage? {
        var wait: UInt64 = 600_000_000          // 0.6s, then 1.8s
        for attempt in 1...3 {
            var request = URLRequest(url: url)
            request.timeoutInterval = 20
            // The disk copy is the point of raising URLCache above, so a
            // relaunch on a train draws what it drew yesterday.
            request.cachePolicy = .returnCacheDataElseLoad
            do {
                let (data, response) = try await Net.data(for: request)
                let code = (response as? HTTPURLResponse)?.statusCode ?? 200
                if (200..<300).contains(code) {
                    // Decoded off the main thread and prepared for drawing, so
                    // a shelf does not decode eight JPEGs during a scroll.
                    if let image = UIImage(data: data) {
                        return await image.byPreparingForDisplay() ?? image
                    }
                    return nil
                }
                // A 4xx that is not a rate limit will say the same thing three
                // times, so stop asking.
                guard code == 429 || code >= 500 else { return nil }
                if let after = (response as? HTTPURLResponse)?
                    .value(forHTTPHeaderField: "Retry-After"), let s = Double(after) {
                    wait = UInt64(min(max(s, 0.5), 5) * 1_000_000_000)
                }
            } catch {
                // No signal, a stall, a dropped connection. Worth another go.
                if Task.isCancelled { return nil }
            }
            guard attempt < 3 else { return nil }
            try? await Task.sleep(nanoseconds: wait)
            wait *= 3
        }
        return nil
    }
}

/// A photograph, with something in its place until it arrives.
///
/// The same shape as AsyncImage on purpose, so the call sites read the way they
/// already did. What differs is everything above: the retry, the cache and the
/// queue.
struct TreePhoto<Placeholder: View>: View {
    let url: URL?
    var contentMode: ContentMode = .fill
    @ViewBuilder var placeholder: () -> Placeholder

    @State private var image: UIImage?
    /// Which url the picture in hand belongs to. Rows are reused as a list
    /// scrolls, and without this a recycled row shows the previous tree's
    /// photograph until the new one lands.
    @State private var shown: URL?

    var body: some View {
        Group {
            if let image, shown == url {
                // AN EMPTY BOX WITH THE PICTURE LAID OVER IT, which is what
                // AsyncImage did for us and a plain Image does not.
                //
                // A `.fill` image proposes the width its own picture wants, so
                // a 4:3 photograph in a 375 point row measures 468 and hangs 46
                // points off each edge. It LOOKS right, because whatever is
                // around it clips; the layout gate reads the frame and calls it
                // clipped, which it is. Caught by appfit on the tree page and
                // the pin picker the first time this view was built, and it is
                // the same fault TreeCard's own comment records.
                Color.clear.overlay {
                    Image(uiImage: image).resizable().aspectRatio(contentMode: contentMode)
                }
                .clipped()
                // DECORATIVE, which is both true and what keeps the layout gate
                // honest. A photograph with no words in it tells VoiceOver
                // nothing it cannot get from the name and the story beside it,
                // so hiding it removes a stop that announced "Image" and no
                // more. TreeCard's own card image was marked this way on the
                // same reasoning and for the same second effect: a `.fill`
                // image reports the size its picture wants rather than the box
                // it is clipped to, and appfit reads frames, so the tree page's
                // hero measured 468 points on a 375 point screen while looking
                // exactly right. A shelf is exempt from that check for the same
                // reason: overflow nobody can see is not a fault.
                .accessibilityHidden(true)
            } else {
                placeholder()
            }
        }
        .task(id: url) {
            guard let url else { image = nil; shown = nil; return }
            if let hit = ImageStore.shared.cached(url) {
                image = hit; shown = url
                return
            }
            image = nil
            shown = nil
            let loaded = await ImageStore.shared.image(for: url)
            // The view may have been handed a different tree while that ran.
            guard url == self.url else { return }
            image = loaded
            shown = loaded == nil ? nil : url
        }
    }
}
