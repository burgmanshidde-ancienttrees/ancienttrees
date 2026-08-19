// Distance on the sphere. One implementation, because the Python side learned
// this lesson the expensive way: the same haversine was pasted six times in
// scripts/ with three drifted call signatures and two drifted units before
// scripts/geo.py took over. This is that module for the app.

import Foundation

public enum Geo {
    public static let earthRadiusKm = 6371.0

    /// Great-circle distance in kilometres.
    public static func km(_ a: (lat: Double, lng: Double),
                          _ b: (lat: Double, lng: Double)) -> Double {
        let dLat = (b.lat - a.lat) * .pi / 180
        let dLng = (b.lng - a.lng) * .pi / 180
        let lat1 = a.lat * .pi / 180
        let lat2 = b.lat * .pi / 180
        let h = sin(dLat / 2) * sin(dLat / 2)
              + sin(dLng / 2) * sin(dLng / 2) * cos(lat1) * cos(lat2)
        return 2 * earthRadiusKm * asin(min(1, sqrt(h)))
    }

    /// Walking minutes at 4.5 km/h, the pace the website's walks already assume.
    public static func walkingMinutes(km: Double) -> Int {
        Int((km / 4.5 * 60).rounded())
    }
}

public extension Tree {
    func distanceKm(from lat: Double, _ lng: Double) -> Double {
        Geo.km((lat: lat, lng: lng), (lat: self.lat, lng: self.lng))
    }
}
