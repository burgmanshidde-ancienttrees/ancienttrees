// Kilometres or miles, and one place that decides.
//
// Added 2026-08-21 with the profile rebuild. Every consumer map app has this
// setting and ours did not, which is fine in the Netherlands and wrong the
// moment somebody in Boston opens it. It defaults to the phone's own locale,
// so almost nobody has to touch it, and it lives in one place so a distance
// cannot be printed in kilometres on one screen and miles on the next.

import Foundation
import SwiftUI

enum DistanceUnit: String, CaseIterable, Identifiable {
    case metric, imperial
    var id: String { rawValue }
    /// "Kilometers", not "Kilometres" (Hidde, 2026-08-25: "waarom staat er in
    /// godsnaam kilometres in het spaans"). It is not Spanish, it is British
    /// English, and that is the more useful finding: the -res spelling is the
    /// one that reads as foreign to a Dutch eye and to an American one at the
    /// same time. Apple's own Settings, iOS Maps and Google Maps all write
    /// Kilometers in a row like this, and it is also the Dutch spelling, so it
    /// looks native to more readers than the version I reached for out of habit.
    ///
    /// The corpus stays British; that is prose about trees. A settings value is
    /// not prose.
    var label: String { self == .metric ? "Kilometers" : "Miles" }
}

@Observable
final class Units {
    private static let key = "distanceUnit"

    /// Told the account when it changes, set once by the root, so this file
    /// keeps knowing nothing about the network.
    static var sync: ((DistanceUnit) -> Void)?

    var unit: DistanceUnit {
        didSet {
            UserDefaults.standard.set(unit.rawValue, forKey: Self.key)
            Self.sync?(unit)
        }
    }

    init() {
        if let raw = UserDefaults.standard.string(forKey: Self.key),
           let u = DistanceUnit(rawValue: raw) {
            unit = u
        } else {
            // The phone already knows. Locale.measurementSystem is the answer
            // Apple itself uses, so the default is right without asking.
            unit = Locale.current.measurementSystem == .metric ? .metric : .imperial
        }
    }

    /// A distance somebody reads on a card or a card-sized line.
    func short(km: Double) -> String {
        switch unit {
        case .metric:
            return km < 1 ? "\(Int((km * 1000).rounded())) m"
                          : String(format: "%.1f km", km)
        case .imperial:
            let miles = km * 0.621371
            return miles < 0.2 ? "\(Int((miles * 5280).rounded())) ft"
                               : String(format: "%.1f mi", miles)
        }
    }

    /// The same thing said in full, for a line that has room.
    func away(km: Double) -> String { short(km: km) + " away" }
}
