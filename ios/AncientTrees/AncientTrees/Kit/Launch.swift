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

    /// The collect flow's "where does it stand" step. It is otherwise reached
    /// only by choosing a photograph that carries no location of its own, and
    /// a simulator's photo roll carries nothing at all, so without this the
    /// screen would ship having never been looked at. Same reason every other
    /// argument in the sweep exists.
    public static let collectPlace = ProcessInfo.processInfo.arguments.contains("-collect-place")
}
