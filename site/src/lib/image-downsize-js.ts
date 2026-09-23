// Turning a phone's photograph into something we can send, once.
//
// Extracted from account/settings.astro on 2026-09-23, when a second place
// needed it: a reader adding a photograph of a tree. A second copy of this
// would have drifted inside a fortnight, and the corpus has the scar to prove
// it (a Wikimedia bucket table hand-ported into Swift, asking for a width the
// server does not serve).
//
// UPRIGHT, asked for rather than hoped for. A phone writes the orientation in
// an EXIF tag and leaves the pixels sideways, which is the same trap
// sightings_publish.py rotates out of reader photographs on the other end.
// createImageBitmap is told to apply it; the <img> fallback exists only for a
// browser with no createImageBitmap at all.
//
// The re-encode drops every other EXIF tag with it, including where the
// photograph was taken. That is a real loss and it is the right trade here:
// stripping a stranger's location out of a file they hand us is what a site
// should do by default, and the one place a geotag would have been useful,
// deciding which of two trunks a picture shows, is answered by which page the
// person was standing on when they pressed the button.
export const DOWNSIZE_JS = `
<script>
window.atDownsize = function(file, maxEdge, done) {
  function draw(src, w, h, release) {
    var side = Math.max(w, h), scale = side > maxEdge ? maxEdge / side : 1;
    var c = document.createElement("canvas");
    c.width = Math.round(w * scale);
    c.height = Math.round(h * scale);
    c.getContext("2d").drawImage(src, 0, 0, c.width, c.height);
    if (release) release();
    c.toBlob(function(b) { done(b); }, "image/jpeg", 0.8);
  }
  if (window.createImageBitmap) {
    createImageBitmap(file, { imageOrientation: "from-image" })
      .then(function(bm) { draw(bm, bm.width, bm.height, function() { bm.close(); }); })
      .catch(function() { done(null); });
    return;
  }
  var img = new Image(), url = URL.createObjectURL(file);
  img.onload = function() {
    draw(img, img.naturalWidth, img.naturalHeight, function() { URL.revokeObjectURL(url); });
  };
  img.onerror = function() { URL.revokeObjectURL(url); done(null); };
  img.src = url;
};
</script>
`;
