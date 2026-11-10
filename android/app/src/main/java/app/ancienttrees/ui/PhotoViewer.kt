// The photograph, full screen, ported from ios Kit/PhotoViewer.swift (Hidde,
// 2026-09-03: the picture opens at its original size, on web and in the app).
// Black, the picture fitted; pinch or double tap to zoom (the original file is
// fetched once you zoom past 1.2), drag down to close, swipe sideways for the
// next photograph; a tap hides and shows the chrome: the cross top right, and at
// the foot "2 of 5" and the credit.

package app.ancienttrees.ui

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.awaitEachGesture
import androidx.compose.foundation.gestures.awaitFirstDown
import androidx.compose.foundation.gestures.calculatePan
import androidx.compose.foundation.gestures.calculateZoom
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.input.pointer.positionChange
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import app.ancienttrees.R
import app.ancienttrees.feed.Photo
import kotlin.math.abs

@Composable
fun PhotoViewer(photos: List<Photo>, startAt: Int, onClose: () -> Unit) {
    if (photos.isEmpty()) return
    Dialog(
        onDismissRequest = onClose,
        properties = DialogProperties(usePlatformDefaultWidth = false, decorFitsSystemWindows = false),
    ) {
        BackHandler(onBack = onClose)
        // .statusBarHidden(): the photograph has the whole screen.
        val view = androidx.compose.ui.platform.LocalView.current
        androidx.compose.runtime.LaunchedEffect(Unit) {
            (view.parent as? androidx.compose.ui.window.DialogWindowProvider)?.window?.let { w ->
                androidx.core.view.WindowCompat.getInsetsController(w, view)
                    .hide(androidx.core.view.WindowInsetsCompat.Type.statusBars())
            }
        }
        var at by remember { mutableIntStateOf(startAt.coerceIn(0, photos.size - 1)) }
        var scale by remember { mutableFloatStateOf(1f) }
        var offset by remember { mutableStateOf(Offset.Zero) }
        var dragDown by remember { mutableFloatStateOf(0f) }
        var chrome by remember { mutableStateOf(true) }
        var wantsOriginal by remember { mutableStateOf(false) }
        fun reset() {
            scale = 1f; offset = Offset.Zero
        }
        fun page(by: Int) {
            if (photos.size < 2) return
            reset()
            wantsOriginal = false
            at = ((at + by) % photos.size + photos.size) % photos.size
        }
        val shown = photos[at]
        Box(
            Modifier
                .fillMaxSize()
                .background(Color.Black.copy(alpha = 1f - minOf(dragDown / 400f, 0.6f))),
        ) {
            Box(
                Modifier
                    .fillMaxSize()
                    .pointerInput(at, photos.size) {
                        detectTapGestures(
                            onDoubleTap = {
                                if (scale > 1f) reset() else { scale = 2.5f; wantsOriginal = true }
                            },
                            onTap = { chrome = !chrome },
                        )
                    }
                    .pointerInput(at, photos.size) {
                        awaitEachGesture {
                            awaitFirstDown(requireUnconsumed = false)
                            var total = Offset.Zero
                            var pinched = false
                            do {
                                val event = awaitPointerEvent()
                                val zoom = event.calculateZoom()
                                val pan = event.calculatePan()
                                if (event.changes.size > 1 || zoom != 1f) {
                                    pinched = true
                                    scale = (scale * zoom).coerceIn(1f, 6f)
                                }
                                if (scale > 1f) {
                                    offset += pan
                                } else if (!pinched) {
                                    total += pan
                                    dragDown = if (abs(total.x) > abs(total.y)) 0f else maxOf(0f, total.y)
                                }
                                if (scale > 1f || pinched) event.changes.forEach { if (it.positionChange() != Offset.Zero) it.consume() }
                            } while (event.changes.any { it.pressed })
                            if (pinched) {
                                if (scale > 1.2f) wantsOriginal = true
                                if (scale <= 1f) reset()
                            } else if (scale <= 1f) {
                                when {
                                    abs(total.x) > abs(total.y) && abs(total.x) > 60 * density && photos.size > 1 -> {
                                        dragDown = 0f
                                        page(if (total.x < 0) 1 else -1)
                                    }
                                    total.y > 90 * density -> onClose()
                                    else -> dragDown = 0f
                                }
                            }
                        }
                    },
            ) {
                val layer = Modifier.fillMaxSize().graphicsLayer {
                    scaleX = scale
                    scaleY = scale
                    translationX = offset.x
                    translationY = offset.y + dragDown
                }
                RemoteImage(shown.full, null, layer, fit = true)
                if (wantsOriginal) RemoteImage(shown.url, null, layer, fit = true, placeholder = false)
            }
            if (chrome) {
                val close = stringResource(R.string.close)
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier
                        .align(Alignment.TopEnd)
                        .statusBarsPadding()
                        .padding(horizontal = 8.dp)
                        .size(44.dp)
                        .clip(CircleShape)
                        .clickable(role = Role.Button, onClick = onClose)
                        // Pressed dims the fill too (Motion.kt, SheetButtonStyle).
                        .background(Color.Black.copy(alpha = 0.45f), CircleShape)
                        .semantics { contentDescription = close },
                ) {
                    Icon(Sym.Close, null, tint = Color.White, modifier = Modifier.size(20.dp))
                }
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(6.dp),
                    modifier = Modifier.align(Alignment.BottomCenter).fillMaxWidth().navigationBarsPadding().padding(bottom = 16.dp),
                ) {
                    if (photos.size > 1) {
                        Text(
                            stringResource(R.string.photo_count, at + 1, photos.size),
                            fontSize = 11.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = Color.White.copy(alpha = 0.9f),
                        )
                    }
                    shown.credit?.let {
                        Text(
                            it,
                            fontSize = 11.sp,
                            color = Color.White.copy(alpha = 0.85f),
                            textAlign = TextAlign.Center,
                            modifier = Modifier.padding(horizontal = 20.dp),
                        )
                    }
                }
            }
        }
    }
}
