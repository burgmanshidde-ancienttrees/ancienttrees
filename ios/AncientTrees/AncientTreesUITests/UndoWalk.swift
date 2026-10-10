import XCTest

/// REMOVING SOMETHING YOU CAN PUT BACK IS DONE AT ONCE, WITH UNDO (Hidde,
/// 2026-10-10: "your suggestion sounds ok"). The collect sheet's "Remove from
/// collected" used to swap the sheet for a red question; now it closes, the
/// snackbar says what happened, and Undo puts the tick back. This walks that
/// path on the tree page: collected, remove, Undo, collected again.
final class UndoWalk: XCTestCase {
    override func setUpWithError() throws {
        continueAfterFailure = false
    }

    func testRemoveFromCollectedOffersUndo() {
        let app = XCUIApplication()
        app.launchArguments = ["-signed-in", "-tab=0", "-open=tree:cph_001",
                               "-collected=cph_001", "-collectsheet", "-at=55.6761,12.5683"]
        app.launch()

        let remove = app.buttons["uncollect"].firstMatch
        XCTAssertTrue(remove.waitForExistence(timeout: 30), "the collected sheet offers no Remove from collected")
        remove.tap()

        let undo = app.buttons["snack-undo"].firstMatch
        XCTAssertTrue(undo.waitForExistence(timeout: 10), "removing did not offer Undo")
        XCTAssertFalse(app.buttons["uncollect-confirm"].exists, "removing still asks a question first")
        undo.tap()

        // Back to collected: the bar's seal opens the collected sheet again,
        // which offers the way back rather than "Collect without a photograph".
        let seal = app.buttons["tree-add-photo-bar"].firstMatch
        XCTAssertTrue(seal.waitForExistence(timeout: 10))
        seal.tap()
        XCTAssertTrue(app.buttons["uncollect"].firstMatch.waitForExistence(timeout: 10),
                      "Undo did not put the tree back in the collection")
    }
}
