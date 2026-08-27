// Three made-up people, for the screens that cannot otherwise be looked at.
//
// Finding somebody and blocking them both need a live database with strangers
// in it, and neither the screenshot sweep nor the flow walk has one. A screen
// no argument can open is a screen that ships unseen, which is the rule this
// project keeps writing down, and a screen that opens EMPTY is the same problem
// wearing a different face: the report and block controls are the two things
// App Store review taps, and until 2026-08-27 neither had ever been in a
// picture.
//
// Behind a launch argument, so nothing here can reach a real build's screen.

import Foundation

public enum DemoPeople {
    public static var on: Bool {
        ProcessInfo.processInfo.arguments.contains("-people-demo")
            || ProcessInfo.processInfo.arguments.contains("-blocked-demo")
    }

    public static let all: [Profiles.Profile] = [
        .init(user_id: "00000000-0000-0000-0000-0000000000a1",
              display_name: "Marieke", avatar_url: nil),
        .init(user_id: "00000000-0000-0000-0000-0000000000a2",
              display_name: "Tom", avatar_url: nil),
        .init(user_id: "00000000-0000-0000-0000-0000000000a3",
              display_name: "Sofia", avatar_url: nil),
    ]
}
