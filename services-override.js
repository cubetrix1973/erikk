(function () {
  // spaceTop = margen SUPERIOR aplicado al <svg> contenedor (fuera del
  // overflow:hidden). NO se puede poner padding/margin en el <h1>/<h2>
  // interno: el svg tiene altura fija (viewBox) y overflow:hidden, así que
  // cualquier desplazamiento vertical del texto recorta el titular por abajo.
  var HEADINGS = {
    'Marketing Digital': { spaceTop: '56px' },
    'Diseño Web': { spaceTop: null },
    'Automatizaciones': { spaceTop: null },
    "Diseño de App's": { spaceTop: null }
  };

  var CLAMP = 'clamp(2rem, 6vw, 5rem)';

  function patch() {
    var changed = false;

    document.querySelectorAll('h1.framer-text, h2.framer-text').forEach(function (h) {
      var cfg = HEADINGS[h.textContent.trim()];
      if (!cfg) return;

      // ¿El titular está EN pantalla? El strip de margin/gap de más abajo solo hace
      // falta cuando se ve el solape. Framer VIRTUALIZA las secciones off-screen y
      // re-aplica su margin al re-renderizarlas; quitárselo ahí entra en un ping-pong
      // a 60fps que oscila la altura de la página ~142px. No se nota mientras la
      // sección está fuera de vista... salvo al llegar al final del scroll, donde ese
      // vaivén de altura hace que el scroll (ya al máximo) rebote: el "temblor".
      // Solución: off-screen no tocamos el margin (no se ve, y se corta la pelea).
      var hr = h.getBoundingClientRect();
      var onScreen = hr.bottom > 0 && hr.top < window.innerHeight;

      if (h.style.getPropertyValue('font-size') !== CLAMP) {
        h.style.setProperty('--framer-font-size', CLAMP, 'important');
        h.style.setProperty('font-size', CLAMP, 'important');
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

      // Framer's own runtime bakes a static "avoid layout jump" correction
      // into these elements' inline style: a negative margin-bottom on the
      // svg and a zeroed gap on the section, precomputed at export time from
      // the ORIGINAL (unclamped) text size. It never gets recalculated, so
      // it now yanks the next block (image/card Grid) up into our taller
      // heading, causing the visible overlap. Strip both — the underlying
      // CSS already defines the correct responsive gap once Framer's inline
      // override is gone.
      if (onScreen && svg && svg.style.getPropertyValue('margin-bottom')) {
        svg.style.removeProperty('margin-bottom');
        changed = true;
      }
      var section = h.closest('section');
      if (onScreen && section && section.style.getPropertyValue('gap')) {
        section.style.removeProperty('gap');
        changed = true;
      }

      // Espacio por encima del titular: como margin en el <svg> (fuera del
      // overflow:hidden), sobrescribiendo el margin-top inline que Framer le
      // pone con !important. No tocar el padding/margin del texto interno.
      if (svg && cfg.spaceTop && svg.style.getPropertyValue('margin-top') !== cfg.spaceTop) {
        svg.style.setProperty('margin-top', cfg.spaceTop, 'important');
        changed = true;
      }

      // Un <svg> recorta su contenido por defecto (overflow:hidden del UA).
      // Con line-height:90% la tilde de la Ñ (y los descendentes) sobresalen
      // de la caja de línea y se cortan por arriba. overflow:visible pinta el
      // glifo completo sin alterar el layout (el alto de caja lo sigue dando
      // el viewBox, esto solo afecta al pintado).
      if (svg && svg.style.getPropertyValue('overflow') !== 'visible') {
        svg.style.setProperty('overflow', 'visible', 'important');
        changed = true;
      }

      // El envoltorio "Headline" (div.framer-ufgxw1 / .framer-uops65 /
      // .framer-1o8wztq) tiene overflow:hidden en su CSS. Con line-height:90%
      // la tilde de la Ñ sobresale por ENCIMA del borde superior del <svg>, y
      // ese recorte lo hace el PADRE, no el svg — por eso overflow:visible en
      // el svg no bastaba. Liberar también el envoltorio.
      var wrap = h.closest('[data-framer-name="Headline"]');
      if (wrap && wrap.style.getPropertyValue('overflow') !== 'visible') {
        wrap.style.setProperty('overflow', 'visible', 'important');
        changed = true;
      }
    });

    if (patchLabels()) changed = true;
    return changed;
  }

  // ---- Labels verticales laterales ("DISEÑO WEB", etc.) --------------------
  // Cada sección tiene un label rotado 90° dentro de una columna "Left" que es
  // position:sticky top:32px. El header del sitio queda fijado arriba por el
  // runtime de Framer y tapa/recorta la parte superior del label.
  //
  // IMPORTANTE: el label está anclado por su CENTRO (top:50% + translate(-50%,
  // -50%)), así que su mitad superior se extiende hacia arriba una distancia =
  // media longitud del texto. "MARKETING DIGITAL" es el más largo, por eso con
  // un top fijo su parte de arriba seguía metiéndose bajo el header (se veía
  // "ETING DIG"). No sirve un top único: cada columna hay que empujarla según
  // la altura real de SU label. Medimos, por label, el offset de su borde
  // superior respecto al borde superior de la columna (O = labTop - colTop,
  // constante e independiente del scroll) y fijamos sticky-top de forma que,
  // cuando la columna esté pegada, el borde superior del label caiga por debajo
  // del header: colTop = headerBottom + gap - O.
  var LABEL_GAP = 20; // separación extra bajo el header

  // El header que TAPA los labels NO es el navbar en flujo (position:relative,
  // se va con el scroll) sino un elemento aparte position:fixed que se oculta al
  // bajar y REAPARECE al subir (patrón hide-on-scroll). Como puede reaparecer en
  // cualquier momento, los labels deben despejar SIEMPRE su altura completa, no
  // su posición instantánea. Detectamos ese header fijo por su geometría (fixed,
  // ancho, altura de barra) y usamos su offsetHeight. Se cachea para no escanear
  // el DOM en cada frame; se re-busca si desaparece del árbol.
  var headerEl = null;
  function findFixedHeader() {
    var best = null, bestTop = Infinity;
    document.querySelectorAll('div[class*="-container"]').forEach(function (el) {
      if (getComputedStyle(el).position !== 'fixed') return;
      var r = el.getBoundingClientRect();
      if (r.width > 300 && el.offsetHeight >= 40 && el.offsetHeight <= 200 && r.top < bestTop) {
        bestTop = r.top; best = el;
      }
    });
    return best;
  }
  function headerHeight() {
    if (!headerEl || !headerEl.isConnected) headerEl = findFixedHeader();
    return headerEl ? headerEl.offsetHeight : 0;
  }

  function patchLabels() {
    var hh = headerHeight();
    if (!hh) return false; // header fijo aún no montado

    // ¿Estamos casi al final del scroll? El label de la ÚLTIMA sección se queda
    // atascado bajo el header al agotarse el scroll (el sticky ya se soltó y no
    // puedes bajar más). Solo ahí aplicamos el empuje hacia abajo; fuera de esa
    // zona los labels de las demás secciones deben poder irse hacia arriba con
    // normalidad (si no, se "pegarían" bajo el header al leer otra sección).
    var slack = (document.body.scrollHeight - window.innerHeight) - window.scrollY;
    var nearBottom = slack <= 260;

    var changed = false;
    document.querySelectorAll('div[data-framer-component-type="RichTextContainer"]').forEach(function (rt) {
      if (!/rotate\(90deg\)/.test(rt.style.transform || '')) return;
      // Subir hasta la columna sticky (la "Left" con position:sticky).
      var col = rt.closest('div');
      while (col && getComputedStyle(col).position !== 'sticky') col = col.parentElement;
      if (!col) return;

      // Top NATURAL del label (sin nuestro translateY). El label está centrado
      // (top:50%) en su caja contenedora, que NO tocamos; medir desde ahí hace la
      // referencia invariante al scroll y a nuestro propio empuje -> sin bucle de
      // realimentación. labelH no cambia con el translateY.
      var box = rt.parentElement;
      var boxRect = box.getBoundingClientRect();
      var labelH = rt.getBoundingClientRect().height;
      var natTop = boxRect.top + boxRect.height / 2 - labelH / 2;

      // (1) Fase PEGADA: fijar sticky-top para que, ya pegado, el label despeje el
      // header. O = offset invariante del top natural respecto al top de la columna.
      var O = natTop - col.getBoundingClientRect().top;
      var top = Math.max(Math.round(hh + LABEL_GAP - O), 32) + 'px';
      if (col.style.getPropertyValue('top') !== top) {
        col.style.setProperty('top', top, 'important');
        changed = true;
      }

      // (2) Fase SOLTADA al final de la última sección: el sticky ya no sujeta y
      // el label sube bajo el header. Empujamos hacia abajo con translateY para que
      // la palabra se lea entera. CLAVE: el empuje va en el transform de la COLUMNA,
      // NO del label. Framer re-asserta el transform del label en cada re-render ->
      // ping-pong con nuestro write -> despierta el observer -> temblor. El transform
      // de la columna (como su `top`) sí lo respeta.
      //
      // Anti-realimentación: natTop se mide dentro de la columna, así que YA incluye
      // el empuje aplicado; lo descontamos (applied) para tener la posición natural
      // real. Objetivo = altura COMPLETA del header (hh, no su borde instantáneo):
      // así no salta cuando el header se oculta/reaparece (mismo criterio que fase 1).
      // Acotado a nearBottom y a que el label esté DE VERDAD junto al top
      // (natTopUnshifted >= -labelH); si no, es de otra sección muy por encima.
      var applied = parseFloat(col.dataset.uShift || '0') || 0;
      var natTopUnshifted = natTop - applied;
      var target = hh + LABEL_GAP;
      var want = (nearBottom && natTopUnshifted < target && natTopUnshifted >= -labelH)
        ? Math.max(0, Math.round(target - natTopUnshifted))
        : 0;
      if (want !== applied) {
        // ponytail: asume que Framer no pone transform propio en estas columnas
        // sticky (verificado: none). Si algún día lo hiciera, componer en vez de fijar.
        if (want > 0) col.style.setProperty('transform', 'translateY(' + want + 'px)', 'important');
        else col.style.removeProperty('transform');
        col.dataset.uShift = String(want);
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

  // scroll — el empuje del label soltado (patchLabels fase 2) depende del scroll,
  // que no dispara mutaciones. IMPORTANTE: en scroll solo corremos patchLabels,
  // NO el patch() completo. Los fixes de titulares quitan/ponen margin/gap y
  // recalculan el viewBox, lo que altera la altura de la página; hacerlo en cada
  // frame de scroll provocaba un bucle (cambia altura -> salta scroll -> scroll
  // event -> patch -> ...), visible como un temblor. patchLabels no toca layout.
  var scrollScheduled = false;
  window.addEventListener('scroll', function () {
    if (scrollScheduled) return;
    scrollScheduled = true;
    requestAnimationFrame(function () { scrollScheduled = false; patchLabels(); });
  }, { passive: true });

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
