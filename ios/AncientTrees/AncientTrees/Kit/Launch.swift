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
    /// The WEBSITE is untouched and keeps its magic link, and it lives with the
    /// built-in sender's few-per-hour limit. The sentence that stood here also
    /// said the site "has no Apple button", which stopped being true on
    /// 2026-09-12 when Hidde asked why not; it has one now, behind
    /// APPLE_SIGNIN in site-config.ts.
    ///
    /// AND THE BLOCKER ABOVE HAS A WAY ROUND IT, chosen by him the same day
    /// over paying for SMTP. The mail keeps its link; what changed is where the
    /// link LANDS. sendCode now asks Supabase to come back to
    /// ancienttrees.app/auth, which the site's apple-app-site-association
    /// lists, so iOS can hand the whole URL to this app and
    /// Account.signInFromLink spends the refresh token in its fragment. When
    /// iOS does not (a universal link is only reliable on a TAP, and this one
    /// arrives at the end of a server redirect), the page signs the person in
    /// on the website instead, which is the same account.
    ///
    /// So this flag is no longer waiting on a purchase, it is waiting on a
    /// TEST: the chain cannot be verified from a build, only from a phone with
    /// a real mail in it. It stays false until somebody taps one.
    public static let emailSignIn = ProcessInfo.processInfo.arguments.contains("-show-email")

    /// The SIX DIGIT half of the typed email route.
    ///
    /// Separate from `emailSignIn` since 2026-09-12, because the two stopped
    /// being the same question. `emailSignIn` asks whether the typed route is
    /// offered at all; this asks what ARRIVES when it is. Supabase's built-in
    /// sender mails a link and its template cannot be edited without custom
    /// SMTP, so the code screen asks for digits that are not in the mail. The
    /// link route (Account.signInFromLink, /auth in the site's AASA) needs no
    /// digits and no SMTP, so it is what the sent screen describes.
    ///
    /// NOTHING IS DELETED, the same rule every flag here runs on: the field,
    /// the Sign in button and Account.verify(code:) all stay in the build, and
    /// the day custom SMTP exists this is one line back rather than a rebuild.
    public static let emailCode = ProcessInfo.processInfo.arguments.contains("-show-email-code")

    /// The collect flow's "where does it stand" step. It is otherwise reached
    /// only by choosing a photograph that carries no location of its own, and
    /// a simulator's photo roll carries nothing at all, so without this the
    /// screen would ship having never been looked at. Same reason every other
    /// argument in the sweep exists.
    public static let collectPlace = ProcessInfo.processInfo.arguments.contains("-collect-place")

    /// The collect flow's "which one is it" step, for the same reason as the
    /// one above and with the same cost if it is missing: it is reached only by
    /// photographing a tree while standing within eighty metres of two of ours,
    /// which a simulator cannot do, so the screen shipped having never been
    /// looked at once. It is also the screen Hidde could not read in Nara.
    public static let collectIdentify = ProcessInfo.processInfo.arguments.contains("-collect-identify")

    /// The payoff screen, which is the one Hidde photographed and objected to
    /// on 2026-09-07 and which nothing had ever measured, for the same reason
    /// as the two above: it comes after a camera a simulator does not have.
    public static let collectTicked = ProcessInfo.processInfo.arguments.contains("-collect-ticked")

    /// The "is this the one" comparison, added 2026-09-07 on Hidde's sketch of
    /// the flow. Same reason as its three neighbours: it lives behind a camera.
    public static let collectCompare = ProcessInfo.processInfo.arguments.contains("-collect-compare")
}
