// Getting somebody walking, in the maps app they actually use. Ported from ios
// Kit/Directions.swift and the root sheet in ContentView.swift (DirectionsAsk).
//
// The iPhone asks ONCE which maps app (Hidde, 2026-08-28: "90% van de mensen
// hebben die app"), remembers the answer on the device ("directions.app",
// data/cross-device.json: what is installed on this phone stays on this phone),
// and Settings is where somebody changes their mind. The question is presented
// from the root of the app, so the three buttons that start a walk (tree page,
// pushed map, walk mode) can never ask differently. Same here: walk() only
// raises DirectionsAsk.pending and the root draws the one sheet.
//
// No custom scheme for Google: the https link is Google's own published way in
// (developers.google.com/maps/documentation/urls/get-started), opening the app
// when it is there and the browser when it is not, so every path ends with a map.
//
// FORCED ON ANDROID (data/android-parity.json): Apple Maps does not exist here.
// Its place in the question is "Another maps app", which hands the spot to
// Android's own chooser through a geo: link, the system's documented way to
// reach whatever maps apps the phone has (Waze, OsmAnd, Organic Maps, ...).
// Waze stays out of the iPhone's list because it has only a custom scheme; on
// Android it answers geo: like every maps app, so it is reachable through that.

package app.ancienttrees.ui

import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import app.ancienttrees.R

object Directions {
    /** The maps apps we can open. Directions.MapsApp, with Apple's place taken by the system's chooser. */
    enum class MapsApp(val raw: String) {
        GOOGLE("google"), OTHER("other");

        fun label(context: Context): String = context.getString(
            when (this) {
                GOOGLE -> R.string.directions_google
                OTHER -> R.string.directions_other
            },
        )

        companion object {
            fun from(raw: String?): MapsApp? = entries.firstOrNull { it.raw == raw }
        }
    }

    private const val KEY = "directions.app"
    private fun prefs(c: Context) = c.applicationContext.getSharedPreferences("device", Context.MODE_PRIVATE)

    /** The remembered answer, or null while nobody has been asked yet. */
    fun preferred(c: Context): MapsApp? = MapsApp.from(prefs(c).getString(KEY, null))
    fun setPreferred(c: Context, app: MapsApp) = prefs(c).edit().putString(KEY, app.raw).apply()

    /** The walking route in Google Maps, the iPhone's own link. */
    fun googleUrl(lat: Double, lng: Double) =
        "https://www.google.com/maps/dir/?api=1&destination=$lat,$lng&travelmode=walking"

    /** The spot for any maps app: geo: with the place as the query, so the app drops a pin there. */
    fun geoUri(lat: Double, lng: Double, name: String?): String {
        val label = name?.takeIf { it.isNotBlank() }?.let { "(" + Uri.encode(it) + ")" }.orEmpty()
        return "geo:$lat,$lng?q=$lat,$lng$label"
    }

    /** Opens the remembered app, or asks first (at the root, see DirectionsAskHost). */
    fun walk(context: Context, lat: Double, lng: Double, name: String? = null) {
        val chosen = preferred(context)
        if (chosen != null) open(context, chosen, lat, lng, name)
        else DirectionsAsk.pending = DirectionsAsk.Pending(lat, lng, name)
    }

    fun open(context: Context, app: MapsApp, lat: Double, lng: Double, name: String? = null) {
        val intent = when (app) {
            MapsApp.GOOGLE -> Intent(Intent.ACTION_VIEW, Uri.parse(googleUrl(lat, lng)))
            MapsApp.OTHER -> Intent.createChooser(
                Intent(Intent.ACTION_VIEW, Uri.parse(geoUri(lat, lng, name))),
                context.getString(R.string.directions_title),
            )
        }.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        try {
            context.startActivity(intent)
        } catch (_: ActivityNotFoundException) {
            // No maps app and no browser: fall back to the web route, which every phone opens.
            runCatching { context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(googleUrl(lat, lng))).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)) }
        }
    }
}

/** The one place a pending "which maps app" question lives (DirectionsAsk.shared). */
object DirectionsAsk {
    data class Pending(val lat: Double, val lng: Double, val name: String?)

    /** Set by Directions.walk when nothing is remembered yet; -directions opens it for the sweep. */
    var pending by mutableStateOf<Pending?>(null)

    fun answer(context: Context, app: Directions.MapsApp) {
        val p = pending ?: return
        Directions.setPreferred(context, app)
        pending = null
        Directions.open(context, app, p.lat, p.lng, p.name)
    }
}

/**
 * The root's sheet (ContentView.swift): THE ONE SHEET, equal choices so every
 * button is grey; the cross and a swipe are the cancel.
 */
@Composable
fun DirectionsAskHost() {
    val context = LocalContext.current
    if (DirectionsAsk.pending == null) return
    BrandSheet(
        title = stringResource(R.string.directions_title),
        message = stringResource(R.string.directions_message),
        onDismiss = { DirectionsAsk.pending = null },
        buttons = Directions.MapsApp.entries.map { app ->
            SheetButton(app.label(context), SheetKind.SECONDARY) { DirectionsAsk.answer(context, app) }
        },
    )
}
