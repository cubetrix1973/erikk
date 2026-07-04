(function () {
  // Unifica el tamaño de letra de "Proyectos", "Clientes" y "Blog" con el
  // de "Servicios" (la referencia). Algunos de estos títulos son SVG
  // "Fit Text" de Framer: su font-size en CSS no es el tamaño real en
  // pantalla, hay que multiplicarlo por el factor de escala del propio
  // SVG (ancho renderizado / ancho del viewBox) — mismo problema que en
  // el tamaño del hero U_NDERS.
  var REF_SELECTOR = '.framer-zm9h0t h2.framer-text';
  var TARGETS = [
    '.framer-jy9ig2 h2.framer-text, .framer-jy9ig2 p.framer-text', // Proyectos
    '.framer-1gh8q16 h2.framer-text',                              // Clientes
    '.ag-section-blog h2.framer-text'                              // Blog
  ];

  function trueFontSize(el) {
    var raw = parseFloat(getComputedStyle(el).fontSize);
    var svg = el.closest('svg');
    if (!svg) return raw;
    var vb = svg.viewBox && svg.viewBox.baseVal;
    if (!vb || !vb.width) return raw;
    var rect = svg.getBoundingClientRect();
    if (!rect.width) return raw;
    return raw * (rect.width / vb.width);
  }

  function setFontSize(el, px) {
    var svg = el.closest('svg');
    if (svg) {
      // Neutraliza el escalado del SVG (igual que en el hero) para poder
      // fijar un px absoluto sin que el propio SVG lo reescale.
      svg.style.removeProperty('height');
      var rect = svg.getBoundingClientRect();
      if (!rect.width || !rect.height) return;
      svg.setAttribute('viewBox', '0 0 ' + rect.width + ' ' + rect.height);
    }
    el.style.setProperty('--framer-font-size', px + 'px', 'important');
  }

  function apply() {
    var ref = document.querySelector(REF_SELECTOR);
    if (!ref) return;
    var targetPx = trueFontSize(ref);
    if (!targetPx) return;
    TARGETS.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el) {
        setFontSize(el, targetPx);
      });
    });
  }

  function start() {
    apply();
    // El "Fit Text" de Framer trae su propio ResizeObserver que puede
    // recalcular y pisar esto (mismo motivo que en hero-size.js) — hay
    // que seguir reforzándolo, no solo al principio.
    setInterval(apply, 250);

    var resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(apply, 150);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
