// Decode the REAL feed and assert what it should contain. Run before trusting
// any of this: a model that compiles proves nothing, a model that decodes 1377
// live trees proves the shape.
//
//   swiftc -O Sources/*.swift Checks/main.swift -o /tmp/atkit && /tmp/atkit <dir>

import Foundation

var failures = 0
func check(_ label: String, _ ok: Bool, _ detail: String = "") {
    print(ok ? "  ok   \(label)\(detail.isEmpty ? "" : "  \(detail)")"
             : "  FAIL \(label)  \(detail)")
    if !ok { failures += 1 }
}

let dir = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "/tmp"
let dec = JSONDecoder()

let treeData = try Data(contentsOf: URL(fileURLWithPath: "\(dir)/trees.json"))
let walkData = try Data(contentsOf: URL(fileURLWithPath: "\(dir)/walks.json"))

print("decoding the live feed from \(dir)")
let tf = try dec.decode(TreeFeed.self, from: treeData)
let wf = try dec.decode(WalkFeed.self, from: walkData)

check("every tree decodes", tf.trees.count == tf.count, "\(tf.trees.count) of \(tf.count)")
check("every walk decodes", wf.walks.count == wf.count, "\(wf.walks.count) of \(wf.count)")

// Nullability measured against the live feed on 2026-08-19.
let noAge = tf.trees.filter { $0.age == nil }.count
let withPhoto = tf.trees.filter { $0.photo != nil }.count
let withBest = tf.trees.filter { $0.bestTime != nil }.count
let approx = tf.trees.filter { $0.precision == .approximate }.count
check("3 trees carry no age", noAge == 3, "got \(noAge)")
check("353 carry a photo", withPhoto == 353, "got \(withPhoto)")
check("546 carry a best_time", withBest == 546, "got \(withBest)")
check("458 pins are approximate", approx == 458, "got \(approx)")

// km arrives as int on some walks and double on others; Double must take both.
let kmSum = wf.walks.reduce(0.0) { $0 + $1.km }
check("km decodes as Double whether the JSON says 5 or 5.0", kmSum > 0,
      String(format: "%.1f km across %d walks", kmSum, wf.walks.count))

// An unknown precision must fall to approximate, never to confirmed.
let odd = try dec.decode(Precision.self, from: Data(#""something-new""#.utf8))
check("unknown precision degrades to approximate", odd == .approximate)

let cat = Catalogue(trees: tf.trees, walks: wf.walks, species: [], version: tf.version)

// Dam square, Amsterdam.
let near = cat.nearest(to: 52.3731, 4.8922, limit: 5)
check("nearest returns 5 from the Dam", near.count == 5)
check("nearest is sorted", zip(near, near.dropFirst()).allSatisfy { $0.km <= $1.km })
check("the closest is within 2 km of the Dam", (near.first?.km ?? 99) < 2.0,
      near.first.map { String(format: "%@ at %.2f km", $0.tree.name, $0.km) } ?? "")

// Somewhere with nothing of ours: the middle of the Atlantic.
let empty = cat.nearest(to: 30.0, -40.0, limit: 10)
check("an empty answer is possible rather than a far-away 12th choice", empty.isEmpty)

let ams = cat.walks(inCity: "amsterdam")
check("Amsterdam has walks", !ams.isEmpty, "\(ams.count)")
if let w = ams.first {
    let ts = cat.trees(of: w)
    check("a walk resolves its tree ids", ts.count == w.trees.count,
          "\(w.name): \(ts.count) of \(w.trees.count)")
}

let august = cat.atTheirBest(inMonth: 8)
let november = cat.atTheirBest(inMonth: 11)
check("the season radar differs by month", august.count != november.count,
      "August \(august.count), November \(november.count)")

check("common name drops the binomial",
      tf.trees.first?.commonName == "Wild Service Tree",
      tf.trees.first?.commonName ?? "")

check("walking minutes are sane", Geo.walkingMinutes(km: 4.5) == 60)

print(failures == 0 ? "\nall checks passed" : "\n\(failures) FAILED")
exit(failures == 0 ? 0 : 1)
