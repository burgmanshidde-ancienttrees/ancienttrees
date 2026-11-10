// The way back after somebody has already said no, ported from ios
// Screens/PermissionRecovery.swift: the title says what the app cannot do well,
// the body what they are missing, Open Settings, a named second choice, and the
// path to the switch in one line under the buttons.
//
// The path is Android's own (Settings › Apps › Ancient Trees › Permissions ›
// Location), since the iPhone's names a screen Android does not have; Open
// Settings lands on the app's own page there (data/android-parity.json, forced).

package app.ancienttrees.ui

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.provider.Settings
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import app.ancienttrees.R

enum class Permission { LOCATION, CAMERA, PHOTOS }

@Composable
fun PermissionRecovery(permission: Permission, onDismiss: () -> Unit, onDecline: (() -> Unit)? = null) {
    val context = LocalContext.current
    val (title, body, decline, path) = when (permission) {
        Permission.LOCATION -> listOf(R.string.perm_loc_title, R.string.perm_loc_body, R.string.perm_loc_decline, R.string.perm_loc_path)
        Permission.CAMERA -> listOf(R.string.perm_cam_title, R.string.perm_cam_body, R.string.perm_cam_decline, R.string.perm_cam_path)
        Permission.PHOTOS -> listOf(R.string.perm_photos_title, R.string.perm_photos_body, R.string.perm_photos_decline, R.string.perm_photos_path)
    }
    BrandSheet(
        title = stringResource(title),
        message = stringResource(body),
        icon = when (permission) {
            Permission.LOCATION -> Sym.NearMe
            Permission.CAMERA -> Sym.PhotoCamera
            Permission.PHOTOS -> Sym.Image
        },
        footnote = stringResource(path),
        onDismiss = onDismiss,
        buttons = listOf(
            SheetButton(stringResource(R.string.perm_open_settings), SheetKind.PRIMARY) {
                openAppSettings(context)
                onDismiss()
            },
            SheetButton(stringResource(decline), SheetKind.QUIET) {
                onDismiss()
                onDecline?.invoke()
            },
        ),
    )
}

/** The app's own page in the system's Settings. */
fun openAppSettings(context: Context) {
    runCatching {
        context.startActivity(
            Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.fromParts("package", context.packageName, null))
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK),
        )
    }
}
