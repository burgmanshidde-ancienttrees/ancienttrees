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
    /// why `keeps(_ tree:)` only answers for ours and `keeps(_ sighting:)`
    /// below answers for yours.
    var collectedOnly = false
    /// The other list, beside Collected (Hidde, 2026-08-26: "misschien is het
    /// dan ook logisch om naast collected ook favorites als filter te maken op
    /// je mapscherm"). They are independent lists everywhere else in the app,
    /// so the map showing only one of them was the map disagreeing with My
    /// trees about what you have.
    var favouritesOnly = false

    var isOn: Bool {
        peakingNow || withPhoto || walkable || collectedOnly || favouritesOnly || species != nil
    }

    func keeps(_ t: Tree, month: Int, collected: Set<String> = [],
               favourites: Set<String> = []) -> Bool {
        if collectedOnly, !collected.contains(t.id) { return false }
        if favouritesOnly, !favourites.contains(t.id) { return false }
        if peakingNow, !(t.bestTime?.isNow(month) ?? false) { return false }
        if withPhoto, t.photo == nil { return false }
        if let species, t.commonName != species { return false }
        return true
    }

    /// And the same four questions asked of a tree only YOU have.
    ///
    /// This file used to end by saying the mine layer was somebody else's
    /// problem, and nobody else took it: `sightings.yoursOnly` went to the map
    /// and to the sheet's list straight from the store, so a tree you added
    /// stood there through every filter (Hidde, 2026-08-27: "de boom die ik
    /// zelf heb toegevoegd blijft altijd op de map staan welke filter ik ook
    /// aanzet, terwijl het geen ginkgo is of niet mijn favoriet"). A filter
    /// that trims our pins and keeps yours is the same lie as one that trims
    /// the list and keeps the pins.
    ///
    /// Three of them are answered from the sighting rather than from
    /// `Sightings.asTree`, because the adapter cannot know them:
    ///
    /// - **with a photo** is read off the sighting. Your photograph is a file
    ///   in Documents rather than a url, so the adapted tree carries no photo
    ///   at all, and asking it would hide every tree you own behind the one
    ///   filter they all pass.
    /// - **collected** is always yes. You collect a tree by adding it, which
    ///   is the rule that dissolved the two lists on 2026-08-24, so there is
    ///   nothing to look up.
    /// - **at their best** is always no. Nothing anywhere records that YOUR
    ///   tree peaks this month, and a filter that keeps what it cannot verify
    ///   is the one failure this whole file is written against. Ours behave
    ///   identically: a tree with no `best_time` is hidden by this filter too.
    ///
    /// Favourites needs no special case: the heart on your tree's page saves
    /// under `treeKey`, which is the id the adapted tree already carries.
    func keeps(_ s: Sightings.Sighting, favourites: Set<String> = []) -> Bool {
        if favouritesOnly, !favourites.contains(s.treeKey) { return false }
        if peakingNow { return false }
        if withPhoto, s.photo == nil { return false }
        if let species, s.commonName != species { return false }
        return true
    }

    /// Distance is applied separately because it needs an origin, and the origin
    /// is where the map is looking rather than a property of the tree.
    func keepsDistance(_ km: Double) -> Bool { !walkable || km <= 2 }
}
