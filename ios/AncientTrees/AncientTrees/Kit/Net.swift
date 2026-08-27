// The one place this app talks to the network.
//
// Written 2026-08-27, and the reason is a question nobody could answer: what
// does this app do in a wood with no bereik? There was no way to find out.
// Eighteen calls to URLSession.shared sat in twelve files, and URLSession.shared
// cannot be taken away from: its configuration is immutable and it ignores a
// registered URLProtocol, which is exactly the seam a test needs. So the whole
// class of failure that a walking app meets most often, no signal, a stalled
// connection, a session three weeks old, was untestable rather than untested.
//
// In a release build this file is a pass-through and nothing else. Net.session
// IS URLSession.shared, the compiler folds it away, and Faults.swift is not
// compiled at all. The interception below exists only in a Debug build, which is
// what the tests run against and what Apple never receives.
//
// The second reason it earns its place: one chokepoint is where a timeout
// belongs. Account sets 20 seconds per request, CatalogueStore 30, and the other
// ten files set none at all, which means the system default of 60 seconds of
// somebody standing under a tree watching a spinner.

import Foundation

public enum Net {

    #if DEBUG
    /// A session carrying the fault protocol. It is installed always and costs
    /// nothing while no fault is armed: FaultProtocol.canInit says no, and the
    /// request goes down the normal stack untouched.
    public static let session: URLSession = {
        let c = URLSessionConfiguration.default
        c.protocolClasses = [FaultProtocol.self] + (c.protocolClasses ?? [])
        c.timeoutIntervalForRequest = 30
        return URLSession(configuration: c)
    }()
    #else
    public static let session = URLSession.shared
    #endif

    public static func data(for r: URLRequest) async throws -> (Data, URLResponse) {
        try await session.data(for: r)
    }

    public static func data(from url: URL) async throws -> (Data, URLResponse) {
        try await session.data(from: url)
    }

    public static func upload(for r: URLRequest, from body: Data) async throws -> (Data, URLResponse) {
        try await session.upload(for: r, from: body)
    }

    public static func dataTask(with r: URLRequest) -> URLSessionDataTask {
        session.dataTask(with: r)
    }
}
