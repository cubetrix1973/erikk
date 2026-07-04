(function () {
  console.log('[services-override] script loaded');

  var HEADINGS = {
    'Marketing Digital': { padTop: false, marginTop: false },
    'Diseño Web': { padTop: true, marginTop: true },
    'Automatizaciones': { padTop: false, marginTop: true },
    "Diseño de App's": { padTop: true, marginTop: true }
  };

  var CLAMP = 'clamp(2rem, 6vw, 5rem)';

  function patch() {
    var changed = false;

    document.querySelectorAll('h1.framer-text, h2.framer-text').forEach(function (h) {
      var cfg = HEADINGS[h.textContent.trim()];
      if (!cfg) return;

      console.log('[services-override] found heading:', JSON.stringify(h.textContent.trim()), h);

      if (h.style.getPropertyValue('font-size') !== CLAMP) {
        h.style.setProperty('--framer-font-size', CLAMP, 'important');
        h.style.setProperty('font-size', CLAMP, 'important');
        changed = true;
      }
      if (cfg.padTop && h.style.getPropertyValue('padding-top') !== '0.3em') {
        h.style.setProperty('padding-top', '0.3em', 'important');
        changed = true;
      }
      if (cfg.marginTop && h.style.getPropertyValue('margin-top') !== '30px') {
        h.style.setProperty('margin-top', '30px', 'important');
        changed = true;
      }

      // The ancestor svg's CSS (.framer-118l9ke etc.) sets white-space:pre,
      // forcing single-line text. At the forced clamp() font-size, "Marketing
      // Digital" is wider than its actual container, and since everything in
      // this svg/foreignObject chain is overflow:visible, the overflow just
      // paints past the box to the right instead of wrapping. Allow wrap.
      if (h.style.getPropertyValue('white-space') !== 'normal') {
        h.style.setProperty('white-space', 'normal', 'important');
        changed = true;
      }

      // Framer wraps each heading in <svg viewBox="0 0 W H"><foreignObject>...
      // svg has width:100%/height:auto, so rendered height derives from the
      // viewBox aspect ratio. Forcing a different font-size makes the real
      // text box no longer match that fixed ratio, so it overflows/clips.
      // Recompute viewBox height to match the actual rendered box.
      var svg = h.closest('svg');
      if (svg && svg.viewBox && svg.viewBox.baseVal) {
        var vb = svg.viewBox.baseVal;
        var rect = h.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0) {
          var newH = Math.round(vb.width * (rect.height / rect.width));
          if (newH !== Math.round(vb.height)) {
            svg.setAttribute('viewBox', '0 0 ' + vb.width + ' ' + newH);
            changed = true;
          }
        }
      }
    });

    return changed;
  }

  // rAF loop — same pattern as antigravity-dom-observer / footer-override
  var stableFrames = 0;
  var maxFrames = 120; // ~2s at 60fps
  function rafLoop() {
    var changed = patch();
    if (changed) {
      stableFrames = 0;
      maxFrames = 120;
    } else {
      stableFrames++;
    }
    if (stableFrames < 20 && maxFrames-- > 0) requestAnimationFrame(rafLoop);
  }
  requestAnimationFrame(rafLoop);

  // setInterval backup — survives Framer hydration
  setInterval(patch, 150);

  // window resize — clamp() is viewport-width-dependent but resize doesn't
  // fire a DOM mutation, so the observer below won't catch it
  window.addEventListener('resize', patch);

  // MutationObserver — react to DOM changes Framer makes after hydration
  var obs = new MutationObserver(function () {
    patch();
    stableFrames = 0;
    maxFrames = 120;
    requestAnimationFrame(rafLoop);
  });

  document.addEventListener('DOMContentLoaded', function () {
    obs.observe(document.documentElement, { childList: true, subtree: true });
    patch();
  });
})();
