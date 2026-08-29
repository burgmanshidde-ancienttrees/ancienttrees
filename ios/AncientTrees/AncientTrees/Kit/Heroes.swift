// The photograph at the top of Discover, and a different one every time the
// app is opened.
//
// Hidde, 2026-08-29, having picked four out of six candidates: "B D E en F zijn
// heel vet kunnen we die afwisselend tonen als je de app opent", and then, to
// be exact about it: "als in elke keer als je de app opent toon je een andere".
//
// NOT ON THE LAUNCH SCREEN, which is where the words "as you open the app"
// point first. iOS launch screens are static by design and Apple's own
// guidance is that they are not a place for branding or a photograph, because
// they must look like the first frame of the app rather than a poster in front
// of it. Every reference here opens straight into its content: AllTrails,
// komoot and Google Maps all land on the map. So the picture goes where a
// picture belongs, at the top of the browse tab, which is also exactly what
// ancienttrees.app does with its own hero.
//
// IN ORDER RATHER THAN AT RANDOM. Random repeats: on four images a shuffle
// shows you the same one twice in a row a quarter of the time, which is the
// one thing a rotation is supposed to avoid. A counter in UserDefaults steps
// through them, so opening the app four times shows all four.
//
// The photographs are the free Unsplash License, which asks for no visible
// credit. The names are recorded here because hard rule 4 says an attribution
// is kept wherever the licence does not force it onto the page, and because
// the website's own hero lost its photographer for three weeks when the file
// holding that line was deleted.
//
//   hero-1  Colin Lloyd       unsplash.com/photos/U5pP4ugOhFo
//   hero-2  Cheng Shi Song    unsplash.com/photos/Uewfi5cV_-w
//   hero-3  Kaijun Zhu        unsplash.com/photos/GBbLT1HU_IA
//   hero-4  Paul Yong         unsplash.com/photos/XnnDfVLKrL8
//
// They are DECORATION and they are never labelled as a tree we map, which is
// the line hard rule 2 draws: a photograph beside a tree's name is evidence,
// and one of these beside a name would be an invention. There is no name on
// this band for that reason.

import Foundation
import UIKit

public enum Heroes {
    public static let names = ["hero-1", "hero-2", "hero-3", "hero-4"]

    private static let key = "hero.index.v1"

    /// The one for this launch, resolved once so a redraw cannot swap the
    /// picture out from under somebody mid-scroll.
    public static let current: String = {
        let defaults = UserDefaults.standard
        let next = (defaults.integer(forKey: key) + 1) % names.count
        defaults.set(next, forKey: key)
        return names[next]
    }()

    /// LOADED FROM THE BUNDLE, not from the asset catalogue, because that is
    /// where these files actually are: they sit in Heroes/ as ordinary jpgs
    /// and the synchronized group copies them into the bundle root. The first
    /// version of this used `Image("hero-1")`, which asks the asset catalogue,
    /// finds nothing and draws NOTHING AT ALL: the band rendered as a grey
    /// gradient with the words on it and no photograph, and it took a
    /// screenshot to see it because a missing image is not a build error.
    public static var image: UIImage? {
        guard let url = Bundle.main.url(forResource: current, withExtension: "jpg"),
              let data = try? Data(contentsOf: url) else { return nil }
        return UIImage(data: data)
    }
}
