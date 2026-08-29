// The launch switchboard. Hidde, 2026-08-26 (DECISIONS.md): the app launches
// free with no reference to Plus anywhere, without walks and without the
// season story, because what is held back is what Plus later introduces, and
// what ships free can never be taken away again.
//
// HIDDEN is the default and the launch state. Nothing is deleted: the walks
// cron keeps planning routes into the feed, the phenology data keeps
// travelling, and every screen behind these flags stays in the build, because
// Plus inherits all of it. The -show-* arguments exist so the screenshot
// sweep, the layout gate and a development build can still open what a user
// cannot; flipping a flag for real users is the Plus introduction, which is
// his call, not a build detail.

import Foundation

public enum Launch {
    /// The walks: shelves, chips and discovery. Deep links (-open=walk, -begin)
    /// stay live regardless, so the UI tests and the sweep keep working.
    public static let walks = ProcessInfo.processInfo.arguments.contains("-show-walks")
    /// The season story: the gold peaking pins and their breathing halo.
    public static let season = ProcessInfo.processInfo.arguments.contains("-show-season")
    /// Every Plus-labelled row and chip.
    public static let plus = ProcessInfo.processInfo.arguments.contains("-show-plus")
    /// The sponsor row in Settings, and with it the only place in the app that
    /// asks for money.
    ///
    /// HIDDEN for 1.0 on Hidde's call (2026-08-29), and the reason is Apple
    /// rather than the sheet, which is finished and honest. An in-app purchase
    /// makes him a trader under the DSA, which publishes his address on the
    /// product page; linking out to the Ko-fi page instead is anti-steering
    /// under 3.1.1, which has been opened up in the US and under the DMA but
    /// only with an entitlement and paperwork that a first submission should
    /// not be carrying. The website keeps its /sponsor page, where none of this
    /// applies and nobody takes a cut, and that is also where the question the
    /// button was built to answer gets measured.
    ///
    /// The sheet itself stays in the build and -sponsor still opens it, so the
    /// screenshot sweep and the layout gate keep seeing it. One line here is
    /// the whole of putting it back.
    public static let sponsor = ProcessInfo.processInfo.arguments.contains("-show-sponsor")

    /// The collect flow's "where does it stand" step. It is otherwise reached
    /// only by choosing a photograph that carries no location of its own, and
    /// a simulator's photo roll carries nothing at all, so without this the
    /// screen would ship having never been looked at. Same reason every other
    /// argument in the sweep exists.
    public static let collectPlace = ProcessInfo.processInfo.arguments.contains("-collect-place")
}
