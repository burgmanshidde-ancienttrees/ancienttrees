// EVERY SHEET LEAVES THE WAY IT CAME (audit 2026-11-10, row 4): on the iPhone a
// sheet whose state goes away slides down (BrandSheet.swift:189 dismiss()); on
// Android taking the sheet out of the composition removed it in one frame,
// scrim and all. So a sheet's own buttons close through LocalSheetClose, which
// slides it down first and then does what the button does.
//
// And the iPhone's handle (Style.swift:318-330, BrandSheetHandle): 36 by 5,
// cream, 12 down, on every sheet, never the system's grey one (row 11).

package app.ancienttrees.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.SheetState
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.remember
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.runtime.withFrameNanos
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch

/** Slide the sheet down, then run what closes it. */
fun interface SheetClose {
    operator fun invoke(then: () -> Unit)
}

/** Outside a sheet the action simply runs. */
val LocalSheetClose = staticCompositionLocalOf { SheetClose { it() } }

@OptIn(ExperimentalMaterial3Api::class)
fun sheetClose(scope: CoroutineScope, state: SheetState, wanted: () -> Boolean) = SheetClose { then ->
    scope.launch {
        state.hide()
        then()
        // Still here and still wanted two frames later: the button changed
        // something inside the sheet rather than closing it, so it comes back up.
        withFrameNanos { }
        withFrameNanos { }
        if (wanted() && !state.isVisible) state.show()
    }
}

/** Whether the sheet's owner still wants it, and how to let it go (see [Lingering]). */
class SheetPresence(val visible: Boolean, val gone: () -> Unit)

val LocalSheetPresence = staticCompositionLocalOf<SheetPresence?> { null }

/**
 * Keeps a sheet on screen after [value] goes away, so it can slide down
 * first: the iPhone's .sheet(item:) going nil. The sheet inside is drawn with
 * the last value it had.
 */
@Composable
fun <T : Any> Lingering(value: T?, content: @Composable (T) -> Unit) {
    var held by remember { mutableStateOf(value) }
    if (value != null && value != held) held = value
    val h = held ?: return
    CompositionLocalProvider(LocalSheetPresence provides SheetPresence(value != null) { held = null }) {
        content(h)
    }
}

/** [Lingering] for a plain condition. */
@Composable
fun LingeringIf(show: Boolean, content: @Composable () -> Unit) =
    Lingering(if (show) Unit else null) { content() }

/**
 * BrandSheetHandle: 36 by 5, cream, 12 from the top. It keeps the 48 points
 * Material's handle took, so no sheet's content moves (each was measured
 * against the iPhone with that room above it).
 */
@Composable
fun BrandSheetHandle(modifier: Modifier = Modifier) {
    Box(
        modifier
            .padding(top = 12.dp, bottom = 31.dp)
            .size(36.dp, 5.dp)
            .background(Brand.colors.creamDark, RoundedCornerShape(50)),
    )
}

/**
 * The app's one modal sheet: Material's, with the iPhone's handle, and with
 * [LocalSheetClose] for everything inside that closes it.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppSheet(
    onDismissRequest: () -> Unit,
    modifier: Modifier = Modifier,
    sheetState: SheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true),
    containerColor: Color = Brand.colors.ground,
    dragHandle: (@Composable () -> Unit)? = { BrandSheetHandle() },
    properties: androidx.compose.material3.ModalBottomSheetProperties = androidx.compose.material3.ModalBottomSheetProperties(),
    content: @Composable ColumnScope.() -> Unit,
) {
    val scope = rememberCoroutineScope()
    val presence = LocalSheetPresence.current
    val wanted by rememberUpdatedState(presence?.visible ?: true)
    val close = remember(sheetState) { sheetClose(scope, sheetState) { wanted } }
    // Its owner let it go: down first, then out of the composition.
    var hidByOwner by remember { mutableStateOf(false) }
    LaunchedEffect(presence?.visible) {
        if (presence != null && !presence.visible) {
            hidByOwner = true
            try {
                sheetState.hide()
            } catch (e: kotlinx.coroutines.CancellationException) {
                throw e
            } catch (_: Exception) {
                // Refused to move: it goes anyway.
            }
            presence.gone()
        } else if (hidByOwner) {
            // Wanted again while it was going: back up.
            hidByOwner = false
            sheetState.show()
        }
    }
    ModalBottomSheet(
        onDismissRequest = onDismissRequest,
        modifier = modifier,
        sheetState = sheetState,
        containerColor = containerColor,
        dragHandle = dragHandle,
        properties = properties,
    ) {
        // A sheet opened from inside this one has its own owner.
        CompositionLocalProvider(LocalSheetClose provides close, LocalSheetPresence provides null) { content() }
    }
}
