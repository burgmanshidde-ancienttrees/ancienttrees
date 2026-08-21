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
    var label: String { self == .metric ? "Kilometres" : "Miles" }
}

@Observable
final class Units {
    private static let key = "distanceUnit"

    var unit: DistanceUnit {
        didSet { UserDefaults.standard.set(unit.rawValue, forKey: Self.key) }
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
