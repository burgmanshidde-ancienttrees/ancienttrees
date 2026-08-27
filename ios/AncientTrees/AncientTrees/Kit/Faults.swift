// Making the app fail on purpose, so somebody can watch what it does.
//
// DEBUG ONLY. This whole file is compiled out of a release build, so there is
// nothing here for a reader to reach and nothing to strip before shipping.
//
// WHY IT EXISTS. Every UI test this app had ran the path where everything
// works, and that is not where the complaints after a launch come from. They
// come from a wood with no signal, a hotel wifi that accepts a connection and
// then says nothing, a Supabase that answers 500 for ten minutes, and a session
// somebody left alone for three weeks. None of those could be reached from a
// test, so none of them had ever been looked at once.
//
// TWO WAYS TO USE IT.
//
// A UI test, or a person with a simulator, passes a launch argument:
//     -fault=offline   every request fails, no signal
//     -fault=slow      eight seconds of nothing, then a timeout
//     -fault=server    HTTP 500 on everything
//     -fault=expired   HTTP 401 on everything, which is what a stale session is
//     -fault=garbage   HTTP 200 carrying broken JSON
//
// A unit test arms it in code and can be far more specific, handing a named
// endpoint a canned answer:
//     Faults.stub("/rest/v1/saves", json: [["tree_id": "ams_004"]])
// and afterwards asks what the app actually sent, with Faults.seen.
//
// The rule for both: a request that matches no stub gets a 404 rather than
// reaching the real internet. A test that quietly talks to the live Supabase is
// a test that fails on a train, and worse, one that can write to it.

#if DEBUG

import Foundation

public enum Faults {

    public enum Mode: String, Sendable {
        case offline, slow, server, expired, garbage
    }

    public struct Stub: Sendable {
        /// Matched against the request's full URL as a plain substring. A path
        /// is enough and reads better at the call site than a whole URL.
        let match: String
        let status: Int
        let body: Data
    }

    /// One request the app made while faults were armed, for a test to assert
    /// on afterwards. The body is captured from the stream, because URLSession
    /// converts httpBody to one before a URLProtocol ever sees the request and
    /// reading request.httpBody here returns nil every time.
    public struct Sent: Sendable {
        public let method: String
        public let url: String
        public let body: Data?

        public var text: String { body.flatMap { String(data: $0, encoding: .utf8) } ?? "" }
    }

    // MARK: - state
    //
    // A URLProtocol is created and started off the main thread, so this is
    // touched from two threads at once by definition. A lock rather than an
    // actor: startLoading is synchronous and cannot await.

    private final class Box: @unchecked Sendable {
        let lock = NSLock()
        var mode: Mode?
        var stubs: [Stub] = []
        var seen: [Sent] = []
    }

    private static let box: Box = {
        let b = Box()
        b.mode = launchMode
        return b
    }()

    private static let launchMode: Mode? = {
        guard let a = ProcessInfo.processInfo.arguments
            .first(where: { $0.hasPrefix("-fault=") }) else { return nil }
        return Mode(rawValue: String(a.dropFirst("-fault=".count)))
    }()

    // MARK: - arming

    public static var mode: Mode? {
        get { box.lock.withLock { box.mode } }
        set { box.lock.withLock { box.mode = newValue } }
    }

    /// True while anything is armed. FaultProtocol asks this before claiming a
    /// request, so an unarmed app pays nothing at all for this file existing.
    static var isArmed: Bool {
        box.lock.withLock { box.mode != nil || !box.stubs.isEmpty }
    }

    public static func stub(_ match: String, status: Int = 200, json: Any) {
        let data = (try? JSONSerialization.data(withJSONObject: json)) ?? Data()
        stub(match, status: status, body: data)
    }

    public static func stub(_ match: String, status: Int = 200, body: Data) {
        box.lock.withLock { box.stubs.append(Stub(match: match, status: status, body: body)) }
    }

    /// Everything the app sent since the last reset, oldest first.
    public static var seen: [Sent] { box.lock.withLock { box.seen } }

    public static func sent(to match: String) -> [Sent] {
        seen.filter { $0.url.contains(match) }
    }

    /// Call at the start of every test that arms anything, and at the end.
    /// Leaving a stub behind makes the NEXT test fail somewhere else, which is
    /// the most expensive kind of test failure there is.
    public static func reset() {
        box.lock.withLock {
            box.mode = nil
            box.stubs = []
            box.seen = []
        }
    }

    // MARK: - answering, called from FaultProtocol

    fileprivate static func record(_ s: Sent) {
        box.lock.withLock { box.seen.append(s) }
    }

    fileprivate static func answer(for url: String) -> (mode: Mode?, stub: Stub?) {
        box.lock.withLock {
            (box.mode, box.stubs.first { url.contains($0.match) })
        }
    }
}

/// The interceptor itself. It never performs a request: everything it claims,
/// it answers, which is what stops a test reaching the live database.
final class FaultProtocol: URLProtocol {

    override class func canInit(with request: URLRequest) -> Bool { Faults.isArmed }

    override class func canonicalRequest(for request: URLRequest) -> URLRequest { request }

    override func startLoading() {
        let url = request.url?.absoluteString ?? ""
        Faults.record(Faults.Sent(method: request.httpMethod ?? "GET",
                                  url: url,
                                  body: Self.body(of: request)))

        let (mode, stub) = Faults.answer(for: url)

        if let stub {
            reply(status: stub.status, body: stub.body)
            return
        }

        switch mode {
        case .offline:
            fail(URLError(.notConnectedToInternet))
        case .slow:
            // A stalled connection, not a refused one. The point is the eight
            // seconds: a refusal comes back instantly and the app has no chance
            // to show a spinner that never ends, which is the actual complaint.
            let work = DispatchWorkItem { [weak self] in
                self?.fail(URLError(.timedOut))
            }
            stalled = work
            DispatchQueue.global().asyncAfter(deadline: .now() + 8, execute: work)
        case .server:
            reply(status: 500, body: Data())
        case .expired:
            reply(status: 401, body: Data(#"{"code":401,"message":"JWT expired"}"#.utf8))
        case .garbage:
            reply(status: 200, body: Data("{".utf8))
        case .none:
            // Stubs are armed and none of them matched. Say so out loud rather
            // than letting the request through: a test that reaches the real
            // Supabase passes at a desk and fails on a train.
            reply(status: 404, body: Data(#"{"message":"no stub for this request"}"#.utf8))
        }
    }

    override func stopLoading() {
        stalled?.cancel()
        stalled = nil
    }

    private var stalled: DispatchWorkItem?

    private func reply(status: Int, body: Data) {
        guard let url = request.url,
              let resp = HTTPURLResponse(url: url, statusCode: status,
                                         httpVersion: "HTTP/1.1",
                                         headerFields: ["Content-Type": "application/json"])
        else { return fail(URLError(.badServerResponse)) }
        client?.urlProtocol(self, didReceive: resp, cacheStoragePolicy: .notAllowed)
        client?.urlProtocol(self, didLoad: body)
        client?.urlProtocolDidFinishLoading(self)
    }

    private func fail(_ error: Error) {
        client?.urlProtocol(self, didFailWithError: error)
    }

    /// URLSession turns httpBody into a stream before a URLProtocol sees the
    /// request, so asking for httpBody returns nil however the request was
    /// built. This is the only way to see what was actually posted.
    private static func body(of r: URLRequest) -> Data? {
        if let b = r.httpBody { return b }
        guard let stream = r.httpBodyStream else { return nil }
        stream.open()
        defer { stream.close() }
        var out = Data()
        let size = 4096
        let buffer = UnsafeMutablePointer<UInt8>.allocate(capacity: size)
        defer { buffer.deallocate() }
        while stream.hasBytesAvailable {
            let read = stream.read(buffer, maxLength: size)
            if read <= 0 { break }
            out.append(buffer, count: read)
        }
        return out.isEmpty ? nil : out
    }
}

#endif
