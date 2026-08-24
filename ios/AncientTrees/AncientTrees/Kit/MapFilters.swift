// What the map is showing, and what it is hiding.
//
// Hidde asked for a map "helemaal lijp met allerlei features" and this is the
// restrained half of that answer. The map is the one screen where every control
// added takes something away from the thing the screen is for, which is why
// Google Maps is so bare, so there are four filters and not eight. They are the
// four questions people actually ask before walking somewhere:
//
//   is it worth going NOW          at their best
//   can I see what I am going to   with a photo
//   can I walk there               within 2 km
//   is it the kind I like          species
//
// The distance one has a second job worth naming: it is the only filter that
// answers "what could I do this afternoon" rather than "what exists", and that
// is the product's own sentence.
//
// Both the pins AND the list obey these. A filter that trims the list while the
// map keeps every pin is a filter that lies to you.

import Foundation

struct MapFilters: Equatable {
    var peakingNow = false
    var withPhoto = false
    var walkable = false
    var species: String?
    /// The ones you have. ONE filter, not two.
    ///
    /// It was two until 2026-08-24, Collected for our trees you had ticked off
    /// and Yours for trees only you had added, sitting side by side on the map
    /// and reading as the same thing. Hidde saw it and gave the rule that
    /// dissolves it rather than relabels it: "je collect de bomen die er zijn
    /// en je collect automatisch een boom als je die toevoegt." A tree you
    /// added is a tree you collected, so there is nothing left to separate.
    ///
    /// Not a property of a tree, so it is applied with the collection passed
    /// in, the same way distance is applied with an origin. Your own trees are
    /// not in the catalogue at all and ride the map's separate layer, which is
    /// why this only has to answer for ours.
    var collectedOnly = false

    var isOn: Bool { peakingNow || withPhoto || walkable || collectedOnly || species != nil }

    func keeps(_ t: Tree, month: Int, collected: Set<String> = []) -> Bool {
        if collectedOnly, !collected.contains(t.id) { return false }
        if peakingNow, !(t.bestTime?.isNow(month) ?? false) { return false }
        if withPhoto, t.photo == nil { return false }
        if let species, t.commonName != species { return false }
        return true
    }

    /// Distance is applied separately because it needs an origin, and the origin
    /// is where the map is looking rather than a property of the tree.
    func keepsDistance(_ km: Double) -> Bool { !walkable || km <= 2 }
}
