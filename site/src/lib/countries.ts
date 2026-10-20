// The countries a person can pick for the flag after their name (Hidde,
// 2026-10-16: "Yes to storing a country per account"; Polarsteps' profile is
// the reference). One ISO 3166 two-letter code per country, the same codes the
// app lists from Locale.Region.isoRegions and profiles.country stores.
//
// The flags are flag-icons 7.2.3 (MIT, site/public/flags/LICENSE.txt), the
// square files copied unchanged into site/public/flags/<code>.svg; only the
// one flag a page shows is ever loaded. Never draw a flag by hand.
export const COUNTRY_CODES = [
  "AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AQ", "AR", "AS", "AT", "AU", "AW", "AX", "AZ",
  "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BL", "BM", "BN", "BO", "BQ", "BR", "BS",
  "BT", "BV", "BW", "BY", "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CI", "CK", "CL", "CM", "CN",
  "CO", "CR", "CU", "CV", "CW", "CX", "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC", "EE",
  "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK", "FM", "FO", "FR", "GA", "GB", "GD", "GE", "GF",
  "GG", "GH", "GI", "GL", "GM", "GN", "GP", "GQ", "GR", "GS", "GT", "GU", "GW", "GY", "HK", "HM",
  "HN", "HR", "HT", "HU", "ID", "IE", "IL", "IM", "IN", "IO", "IQ", "IR", "IS", "IT", "JE", "JM",
  "JO", "JP", "KE", "KG", "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KY", "KZ", "LA", "LB", "LC",
  "LI", "LK", "LR", "LS", "LT", "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MF", "MG", "MH", "MK",
  "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW", "MX", "MY", "MZ", "NA",
  "NC", "NE", "NF", "NG", "NI", "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA", "PE", "PF",
  "PG", "PH", "PK", "PL", "PM", "PN", "PR", "PS", "PT", "PW", "PY", "QA", "RE", "RO", "RS", "RU",
  "RW", "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ", "SK", "SL", "SM", "SN", "SO", "SR",
  "SS", "ST", "SV", "SX", "SY", "SZ", "TC", "TD", "TF", "TG", "TH", "TJ", "TK", "TL", "TM", "TN",
  "TO", "TR", "TT", "TV", "TW", "TZ", "UA", "UG", "UM", "US", "UY", "UZ", "VA", "VC", "VE", "VG",
  "VI", "VN", "VU", "WF", "WS", "XK", "YE", "YT", "ZA", "ZM", "ZW",
];

/** Every country by its English name, for the picker; built once at build time. */
export function countryOptions(): { code: string; name: string }[] {
  const names = new Intl.DisplayNames(["en"], { type: "region" });
  return COUNTRY_CODES
    .map((code) => ({ code, name: names.of(code) ?? code }))
    .sort((a, b) => a.name.localeCompare(b.name, "en"));
}

export const flagUrl = (code: string) => `/flags/${code.toLowerCase()}.svg`;

// A FLAG BY DEFAULT (Hidde, 2026-10-20: "bij polarsteps heb ik de vlag zonder
// ooit actief nederland te hebben aangevinkt"). Until you choose, your flag is
// the country you appear to be in; "Don't show" at the top of the picker turns
// it off for good (profiles.flag_hidden, supabase/profiles.sql). The app reads
// the phone's region; the website reads the computer's time zone, because a
// browser's language says nothing reliable (many Dutch browsers run en-US).
// Only a profile row that exists is written: a row needs a name first.
//
// window.atCountryGuess() -> "NL" or ""; window.atSettleCountry(sb, key, token,
// uid) -> Promise of { country, hidden, guess }, writing the guess once.
// tz-country.json is the system zone.tab (time zone -> ISO country).
import TZ_COUNTRY from "./tz-country.json";

export const COUNTRY_JS = `
<script>
(function() {
  var TZ = ${JSON.stringify(TZ_COUNTRY)};
  window.atCountryGuess = function() {
    try { return TZ[Intl.DateTimeFormat().resolvedOptions().timeZone] || ''; } catch (e) { return ''; }
  };
  window.atSettleCountry = function(SB, KEY, token, uid) {
    var h = { 'apikey': KEY, 'Authorization': 'Bearer ' + token };
    var guess = window.atCountryGuess();
    function plain() {
      // A database without flag_hidden yet: the flag as stored, no default.
      return fetch(SB + '/rest/v1/profiles?select=country&user_id=eq.' + encodeURIComponent(uid), { headers: h })
        .then(function(r) { return r.ok ? r.json() : null; })
        .then(function(rows) { return { country: (rows && rows[0] && rows[0].country) || '', hidden: false, guess: '' }; });
    }
    return fetch(SB + '/rest/v1/profiles?select=country,flag_hidden&user_id=eq.' + encodeURIComponent(uid), { headers: h })
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(rows) {
        if (!rows) return plain();
        var row = rows[0];
        if (!row) return { country: '', hidden: false, guess: guess };
        if (row.country) return { country: row.country, hidden: false, guess: guess };
        if (row.flag_hidden || !guess) return { country: '', hidden: !!row.flag_hidden, guess: guess };
        return fetch(SB + '/rest/v1/profiles?user_id=eq.' + encodeURIComponent(uid), {
          method: 'PATCH',
          headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
          body: JSON.stringify({ country: guess })
        }).then(function(r) { return { country: r.ok ? guess : '', hidden: false, guess: guess }; });
      }).catch(function() { return { country: '', hidden: false, guess: '' }; });
  };
})();
</script>`;
