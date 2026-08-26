// Sponsoring, inside the app, which means Apple's own purchases and nothing
// else. Hidde asked for it on 2026-08-26 after opening ko-fi.com/ancienttrees
// for the website: "bouw jij de app sponsor actie dan?"
//
// WHY THIS IS NOT JUST A LINK TO KO-FI. App Review's anti-steering rules
// (3.1.1) do not allow an app to send somebody out to an external payment page
// for a digital purchase or a tip, and the registered-nonprofit exception is
// not ours. So the website keeps its Ko-fi page, where nobody takes a cut, and
// the app has this, where Apple takes fifteen percent under the Small Business
// Program. Two routes because the platforms leave no third one, and the person
// paying sees one thing either way: a way to keep this going.
//
// TIPS ARE CONSUMABLE, deliberately. A sponsorship is not an entitlement: it
// unlocks nothing, it can be given again next month, and consumables carry no
// restore obligation because there is nothing to restore. That also keeps this
// clear of Plus, which is a separate decision and still Hidde's.
//
// THE PRICES ARE NOT HERE and cannot be: an in-app purchase's price is set in
// App Store Connect, per product, by the account holder (hard rule 2). This
// file names the product ids and reads back whatever Apple says they cost, in
// the viewer's own currency. Until Hidde creates them, `products` comes back
// empty and the sheet says so rather than showing dead buttons, which is the
// same honest-empty rule the website's SPONSOR_URL follows.

import Foundation
import StoreKit
import Observation

@MainActor
@Observable
public final class Tips {
    /// The ids to create in App Store Connect, as Consumable, under In-App
    /// Purchases. Any price tier works; these three are ordered small to large
    /// and the sheet shows them in the order Apple returns their prices.
    public static let ids = [
        "app.ancienttrees.tip.small",
        "app.ancienttrees.tip.medium",
        "app.ancienttrees.tip.large",
    ]

    public private(set) var products: [Product] = []
    public private(set) var loading = true
    /// Set after a purchase goes through, so the sheet can say thank you
    /// without pretending anything was unlocked.
    public private(set) var thanked = false
    public private(set) var failed = false

    public init() {}

    public func load() async {
        loading = true
        defer { loading = false }
        do {
            let found = try await Product.products(for: Tips.ids)
            products = found.sorted { $0.price < $1.price }
        } catch {
            // No network, or the products do not exist yet. Both mean the same
            // thing to the person looking at the sheet: not today.
            products = []
        }
    }

    public func buy(_ product: Product) async {
        failed = false
        do {
            switch try await product.purchase() {
            case .success(let verification):
                // A consumable still has to be finished, or StoreKit re-serves
                // it on every launch forever.
                if case .verified(let transaction) = verification {
                    await transaction.finish()
                    thanked = true
                }
            case .userCancelled, .pending:
                break
            @unknown default:
                break
            }
        } catch {
            failed = true
        }
    }
}
