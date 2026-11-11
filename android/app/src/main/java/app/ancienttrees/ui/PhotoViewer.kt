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
import androidx.compose.animation.core.tween
import androidx.compose.foundation.layout.BoxWithConstraints
import kotlinx.coroutines.launch
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
import app.ancienttrees.R
import app.ancienttrees.feed.Photo
import kotlin.math.abs

@Composable
fun PhotoViewer(photos: List<Photo>, startAt: Int, onClose: () -> Unit) {
    if (photos.isEmpty()) return
    // A FULL-SCREEN COVER, as .fullScreenCover (TreeDetail.swift:577-585): it slides
    // up from the bottom over the page, and down again however it is closed.
    val scope = androidx.compose.runtime.rememberCoroutineScope()
    val rise = remember { androidx.compose.animation.core.Animatable(0f) }
    var closing by remember { mutableStateOf(false) }
    fun close() {
        if (closing) return
        closing = true
        scope.launch {
            rise.animateTo(0f, Motion.push())
            onClose()
        }
    }
    // In the app's own window, not a Dialog: a Dialog is a second window that
    // appears late, so its first half-second of motion was never seen.
    Box(Modifier.fillMaxSize()) {
        BackHandler { close() }
        // .statusBarHidden(): the photograph has the whole screen, for as long as it is open.
        val view = androidx.compose.ui.platform.LocalView.current
        androidx.compose.runtime.DisposableEffect(Unit) {
            val w = (view.context as? android.app.Activity)?.window
            val bars = w?.let { androidx.core.view.WindowCompat.getInsetsController(it, view) }
            bars?.hide(androidx.core.view.WindowInsetsCompat.Type.statusBars())
            onDispose { bars?.show(androidx.core.view.WindowInsetsCompat.Type.statusBars()) }
        }
        androidx.compose.runtime.LaunchedEffect(Unit) { rise.animateTo(1f, Motion.push()) }
        var at by remember { mutableIntStateOf(startAt.coerceIn(0, photos.size - 1)) }
        var scale by remember { mutableFloatStateOf(1f) }
        var offset by remember { mutableStateOf(Offset.Zero) }
        var dragDown by remember { mutableFloatStateOf(0f) }
        var chrome by remember { mutableStateOf(true) }
        var wantsOriginal by remember { mutableStateOf(false) }
        // PhotoViewer.swift's timings: snap back 0.2 s ease-out, double-tap zoom
        // 0.2 s ease-in-out, a page 0.18 s ease-in-out, the chrome 0.15 s.
        fun snapBack() {
            scope.launch {
                androidx.compose.animation.core.animate(dragDown, 0f, animationSpec = tween(200, easing = Motion.EaseOut)) { v, _ -> dragDown = v }
            }
        }
        fun zoomTo(target: Float) {
            val from = scale
            val fromOffset = offset
            scope.launch {
                androidx.compose.animation.core.animate(0f, 1f, animationSpec = tween(200, easing = Motion.EaseInOut)) { f, _ ->
                    scale = from + (target - from) * f
                    if (target == 1f) offset = fromOffset * (1f - f)
                }
            }
        }
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
        BoxWithConstraints(
            Modifier
                .fillMaxSize()
                .graphicsLayer { translationY = (1f - rise.value) * size.height }
                .background(Color.Black.copy(alpha = 1f - minOf(dragDown / 400f, 0.6f))),
        ) {
            Box(
                Modifier
                    .fillMaxSize()
                    .pointerInput(at, photos.size) {
                        detectTapGestures(
                            onDoubleTap = {
                                if (scale > 1f) zoomTo(1f) else { zoomTo(2.5f); wantsOriginal = true }
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
                                        snapBack()
                                        page(if (total.x < 0) 1 else -1)
                                    }
                                    // Down far enough: the cover goes down from where the finger left it.
                                    total.y > 90 * density -> close()
                                    else -> snapBack()
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
                androidx.compose.animation.Crossfade(
                    targetState = at,
                    animationSpec = tween(180, easing = Motion.EaseInOut),
                    label = "photo-page",
                ) { i ->
                    val p = photos[i]
                    Box(Modifier.fillMaxSize()) {
                        // Until it lands: the white spinner on black (TreePhoto's ProgressView().tint(.white)).
                        RemoteImage(p.full, null, layer, fit = true, fallback = {
                            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                                androidx.compose.material3.CircularProgressIndicator(color = Color.White, strokeWidth = 2.dp, modifier = Modifier.size(28.dp))
                            }
                        })
                        if (wantsOriginal && i == at) RemoteImage(p.url, null, layer, fit = true, placeholder = false)
                    }
                }
            }
            androidx.compose.animation.AnimatedVisibility(
                visible = chrome,
                enter = androidx.compose.animation.fadeIn(tween(150, easing = Motion.EaseInOut)),
                exit = androidx.compose.animation.fadeOut(tween(150, easing = Motion.EaseInOut)),
                modifier = Modifier.fillMaxSize(),
            ) { Box(Modifier.fillMaxSize()) {
                val close = stringResource(R.string.close)
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier
                        .align(Alignment.TopEnd)
                        .statusBarsPadding()
                        .padding(horizontal = 8.dp)
                        .size(44.dp)
                        .clip(CircleShape)
                        .clickable(role = Role.Button) { close() }
                        // The ripple stays inside the shape (Airbnb's line, 2026-11-10).
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
            } }
        }
    }
}
