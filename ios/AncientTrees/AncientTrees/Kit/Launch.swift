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

    /// The typed email route on the sign-in sheet.
    ///
    /// HIDDEN FOR 1.0, and for a reason outside our own code. It calls
    /// /auth/v1/otp and verifies six digits, which is right, but WHAT ARRIVES is
    /// decided by Supabase's Magic Link template, and that template can only be
    /// edited on a project with custom SMTP. Without it the mail carries a link
    /// to the website instead of a code, so the field asks for something the
    /// mail never contains (Hidde, 2026-08-30: "je hoort digits te krijgen maar
    /// ik krijg een magic link met een link naar de site").
    ///
    /// Custom SMTP is a third party in the product and therefore his call under
    /// hard rule 5, and he said no for now: "geen zin in nieuw ding kunnen we
    /// ook zonder magic link." We can: Apple needs no mail and no service at
    /// all, and Google needs only a provider switch he was already going to
    /// flip. A signed-out person on iOS always has an Apple ID.
    ///
    /// NOTHING IS DELETED, the same rule the flags above run on. sendCode,
    /// verify and the whole code screen stay in the build and -show-email still
    /// opens them, so the sweep and the layout gate keep seeing the screen. The
    /// day SMTP exists this is one line back.
    ///
    /// The WEBSITE is untouched and keeps its magic link. It has no Apple
    /// button, so removing it there would leave Google alone, and it already
    /// lives with the built-in mail service's few-per-hour limit today.
    public static let emailSignIn = ProcessInfo.processInfo.arguments.contains("-show-email")

    /// The collect flow's "where does it stand" step. It is otherwise reached
    /// only by choosing a photograph that carries no location of its own, and
    /// a simulator's photo roll carries nothing at all, so without this the
    /// screen would ship having never been looked at. Same reason every other
    /// argument in the sweep exists.
    public static let collectPlace = ProcessInfo.processInfo.arguments.contains("-collect-place")
}
