(function () {
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
    });

    return changed;
  }

  // rAF loop — same pattern as antigravity-dom-observer / footer-override
  var stableFrames = 0;
  var maxFrames = 120; // ~2s at 60fps
  function rafLoop() {
    var changed = patch();
    stableFrames = changed ? 0 : stableFrames + 1;
    if (stableFrames < 20 && maxFrames-- > 0) requestAnimationFrame(rafLoop);
  }
  requestAnimationFrame(rafLoop);

  // setInterval backup — survives Framer hydration
  setInterval(patch, 150);

  // MutationObserver — react to DOM changes Framer makes after hydration
  var obs = new MutationObserver(function () {
    patch();
    stableFrames = 0;
    requestAnimationFrame(rafLoop);
  });

  document.addEventListener('DOMContentLoaded', function () {
    obs.observe(document.documentElement, { childList: true, subtree: true });
    patch();
  });
})();
