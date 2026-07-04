(function () {
  var NAV_LINKS = [
    { text: 'Nosotros',               href: '/nosotros' },
    { text: 'Servicios',              href: '/servicios' },
    { text: 'Proyectos',              href: '/proyectos' },
    { text: 'Blog',                   href: '/blog' },
    { text: 'Contacto',               href: '/contacto' },
    { text: 'Términos y condiciones', href: '/terminos-y-condiciones' }
  ];

  var LINKEDIN_URL = 'https://www.linkedin.com/company/the-unders';

  var LINK_STYLE = [
    "font-family:'Roboto Mono',monospace",
    "font-size:18px", "font-weight:400", "letter-spacing:2px",
    "text-transform:uppercase", "color:#000000",
    "text-decoration:none", "transition:opacity 0.2s"
  ].join(';');

  function linkedinIcon() {
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28" fill="#000000">'
      + '<path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037'
      + '-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046'
      + 'c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286z'
      + 'M5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065z'
      + 'm1.782 13.019H3.555V9h3.564v11.452z'
      + 'M22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24'
      + 'h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>'
      + '</svg>';
  }

  function buildFooter() {
    var links = NAV_LINKS.map(function (l) {
      return '<a class="ag-footer-link" href="' + l.href + '" style="' + LINK_STYLE + '">' + l.text + '</a>';
    }).join('');

    var linkedin = '<a href="' + LINKEDIN_URL + '" target="_blank" rel="noopener" title="LinkedIn" '
      + 'style="display:inline-flex;">' + linkedinIcon() + '</a>';

    // El tamaño real de la U_ se calcula en patch() a partir del alto medido de
    // .ag-footer-logo-wrap (que con align-items:stretch coincide con el alto del
    // footer), no aquí: al construir este HTML todavía no hay layout que medir.
    return ''
      + '<div class="ag-footer-left" style="flex:1 1 auto;min-width:0;display:flex;'
      + 'flex-direction:column;justify-content:space-between;gap:32px;">'
      +   '<nav class="ag-footer-nav" style="display:flex;flex-direction:column;align-items:flex-start;gap:16px;">'
      +     links
      +   '</nav>'
      +   '<div class="ag-footer-bottom" style="display:flex;flex-direction:column;align-items:flex-start;width:100%;gap:16px;">'
      +     linkedin
      +     '<div style="width:100%;height:1px;background:#000000;"></div>'
      +     '<p style="font-size:12px;letter-spacing:0.5px;color:#000000;margin:0;">© DISEÑADO POR THE U_NDERS</p>'
      +   '</div>'
      + '</div>'
      + '<div class="ag-footer-logo-wrap" style="flex:0 0 38%;min-width:0;display:flex;align-items:center;justify-content:center;overflow:hidden;">'
      +   '<span class="ag-footer-logo" style="font-weight:900;line-height:1;color:#000000;white-space:nowrap;">'
      +   'U<span class="cursor-blink">_</span></span>'
      + '</div>';
  }

  // Sube por los ancestros de un nodo hasta <body> y fuerza overflow:visible
  // (cualquier valor de overflow que no sea "visible" en un ancestro rompe position:sticky)
  function clearOverflowUp(node) {
    for (var a = node.parentElement; a && a !== document.body; a = a.parentElement) {
      var cs = getComputedStyle(a);
      if (cs.overflow !== 'visible' || cs.overflowX !== 'visible' || cs.overflowY !== 'visible') {
        a.style.setProperty('overflow', 'visible', 'important');
      }
    }
  }

  // .ag-section-blog se inyecta como último hijo de <main>, así que su propio contenedor
  // termina justo donde ella termina: no hay "recorrido" de scroll para que sticky se note.
  // La envolvemos en un div más alto que ella misma para darle ese recorrido, y metemos
  // el banner + footer DENTRO de ese mismo div, justo después: así comparten el mismo
  // contexto de apilamiento (stacking context) que el blog sticky y sí se dibujan encima
  // de él en vez de quedar tapados por él (que es lo que pasaba con footer/banner
  // fuera de <main> y el blog dentro: Framer mete "will-change:transform" en varios
  // ancestros, cada uno crea su propio contexto de apilamiento aislado, y el z-index
  // del footer terminaba comparándose contra el nada en vez de contra el del blog).
  function ensureStickyWrap(blog, bannerWrap, footerWrap) {
    var wrap = blog.parentElement;
    if (!wrap || !wrap.classList.contains('ag-sticky-wrap')) {
      wrap = document.createElement('div');
      wrap.className = 'ag-sticky-wrap';
      wrap.style.position = 'relative';
      blog.parentNode.insertBefore(wrap, blog);
      wrap.appendChild(blog);
    }
    if (bannerWrap && bannerWrap.parentElement !== wrap) wrap.appendChild(bannerWrap);
    if (footerWrap && footerWrap.parentElement !== wrap) wrap.appendChild(footerWrap);
    return wrap;
  }

  function sizeStickyWrap(wrap, blog) {
    var runway = window.innerHeight; // recorrido de un alto de pantalla
    wrap.style.height = (blog.offsetHeight + runway) + 'px';
  }

  function injectFooterCSS() {
    if (document.getElementById('ag-cursor-blink-css')) return;
    var style = document.createElement('style');
    style.id = 'ag-cursor-blink-css';
    style.textContent = [
      '@keyframes blink-cursor {',
      '  0%, 100% { opacity: 1; }',
      '  50% { opacity: 0; }',
      '}',
      '.cursor-blink {',
      '  animation: blink-cursor 1s steps(1) infinite;',
      '}',
      // Tablet: enlaces del footer un poco más chicos para que quepan sin desbordar
      '@media (max-width: 1279px) {',
      '  .ag-footer-link { font-size: 15px !important; letter-spacing: 1.5px !important; }',
      '}',
      // Móvil: enlaces más chicos
      '@media (max-width: 809px) {',
      '  .ag-footer-link { font-size: 12px !important; letter-spacing: 1px !important; }',
      '}'
    ].join('\n');
    document.head.appendChild(style);
  }

  function patch() {
    var changed = false;

    injectFooterCSS();

    // 1. Quitar el botón "Get in Touch"/"Contacto" del banner (ahora vive en el footer)
    document.querySelectorAll('.framer-text').forEach(function (el) {
      var t = el.textContent.trim();
      if (t === 'Get in Touch' || t === 'Contacto') {
        var btn = el.closest('a');
        if (btn && btn.style.display !== 'none') {
          btn.style.setProperty('display', 'none', 'important');
          changed = true;
        }
      }
    });

    // 1b. Quitar el heading "HABLEMOS"/"U_NDERS" del banner (redundante con el logo del footer)
    document.querySelectorAll('.framer-ucirrb').forEach(function (el) {
      if (el.style.display !== 'none') {
        el.style.setProperty('display', 'none', 'important');
        changed = true;
      }
    });

    // 2. Fondo del banner CONTACTO → blanco, elevado por encima del blog sticky
    document.querySelectorAll('.framer-WMTT6').forEach(function (el) {
      if (el.style.getPropertyValue('background-color') !== 'rgb(255, 255, 255)') {
        el.style.setProperty('background-color', '#ffffff', 'important');
        changed = true;
      }
      el.style.setProperty('position', 'relative', 'important');
      el.style.setProperty('z-index', '2', 'important');
    });

    // 2b. Cualquier texto blanco restante dentro del banner → negro
    document.querySelectorAll('.framer-WMTT6 .framer-text, .framer-WMTT6 p, .framer-WMTT6 h2, .framer-WMTT6 span')
      .forEach(function (el) {
        var rgb = getComputedStyle(el).color.match(/\d+/g);
        if (rgb && rgb[0] > 200 && rgb[1] > 200 && rgb[2] > 200) {
          el.style.setProperty('color', '#000000', 'important');
          changed = true;
        }
      });

    // 3. Rediseño completo del footer: enlaces + logo, línea + copyright
    document.querySelectorAll('footer.framer-CaFNh').forEach(function (el) {
      if (!el.querySelector('.ag-footer-left')) {
        el.innerHTML = buildFooter();
        changed = true;
      }
      // Móvil: 0.5vh de arriba dejaba el menú NOSOTROS/SERVICIOS/... pegado al
      // borde superior del footer, tapado por lo que hay justo encima al terminar
      // el scroll. Le damos más aire arriba.
      var pad = window.innerWidth <= 809 ? '48px 6vw 3vh'
        : window.innerWidth <= 1279 ? '0.5vh 6vw 3.5vh'
        : '0.5vh 6vw 4vh';
      el.style.setProperty('background-color', '#ffffff', 'important');
      el.style.setProperty('position', 'relative', 'important');
      el.style.setProperty('z-index', '2', 'important');
      el.style.setProperty('padding', pad, 'important');
      el.style.setProperty('will-change', 'transform', 'important');
      el.style.setProperty('transform', 'translateZ(0)', 'important');
      // En móvil el footer (contenido) suele medir menos que una pantalla completa;
      // sin esto queda un hueco debajo de su fondo blanco por el que se asoma el
      // final del blog (texto cortado + botón READ MORE) mientras el sticky reveal
      // todavía está subiendo. Con min-height el fondo blanco tapa toda la pantalla
      // aunque el contenido del footer sea más corto.
      var isMobile = window.innerWidth <= 809;
      if (isMobile) {
        el.style.setProperty('min-height', window.innerHeight + 'px', 'important');
      } else {
        // Si se vio la versión móvil antes en la misma sesión (p. ej. con el
        // selector de dispositivo del navegador) este min-height se queda pegado
        // y agranda de más el footer y la U_ en escritorio si no se limpia aquí.
        el.style.removeProperty('min-height');
      }

      var leftEl = el.querySelector('.ag-footer-left');
      var navEl = el.querySelector('.ag-footer-nav');
      var logoWrap = el.querySelector('.ag-footer-logo-wrap');
      var logoSpan = el.querySelector('.ag-footer-logo');

      if (isMobile) {
        // Diseño solo-móvil: columna centrada, U_ grande arriba y enlaces debajo.
        // El diseño de escritorio (fila, enlaces a la izq., U_ a la altura completa
        // del footer a la der.) no se toca, es el bloque "else" de aquí abajo.
        el.style.setProperty('flex-direction', 'column', 'important');
        el.style.setProperty('align-items', 'center', 'important');
        if (logoWrap) {
          logoWrap.style.setProperty('order', '0', 'important');
          logoWrap.style.setProperty('align-self', 'stretch', 'important');
          logoWrap.style.setProperty('width', 'auto', 'important');
          logoWrap.style.setProperty('height', 'auto', 'important');
        }
        if (leftEl) {
          leftEl.style.setProperty('order', '1', 'important');
          leftEl.style.setProperty('align-items', 'center', 'important');
          leftEl.style.setProperty('justify-content', 'flex-start', 'important');
          leftEl.style.setProperty('flex', '0 0 auto', 'important');
          leftEl.style.setProperty('width', '100%', 'important');
        }
        if (navEl) {
          navEl.style.setProperty('align-items', 'center', 'important');
        }
        // Grande y centrada: limitada solo por el ancho del footer (más un margen
        // para que no toque los bordes), ya que aquí ocupa una fila para ella sola.
        if (logoWrap && logoSpan && logoWrap.offsetWidth > 0) {
          logoSpan.style.setProperty('font-size', (logoWrap.offsetWidth * 0.58) + 'px', 'important');
        }
      } else {
        // Desktop/tablet: sin cambios respecto al diseño ya aprobado. Framer trae
        // flex-flow:column + align-items:flex-start de fábrica (enlaces, logo, etc.
        // apilados); lo pasamos a fila con stretch para que la columna de la
        // izquierda (enlaces+bottom) y la U_ de la derecha compartan el mismo alto.
        el.style.setProperty('flex-direction', 'row', 'important');
        el.style.setProperty('align-items', 'stretch', 'important');
        if (logoWrap) {
          logoWrap.style.removeProperty('order');
          logoWrap.style.removeProperty('align-self');
          logoWrap.style.removeProperty('width');
          logoWrap.style.removeProperty('height');
        }
        if (leftEl) {
          leftEl.style.removeProperty('order');
          leftEl.style.removeProperty('align-items');
          leftEl.style.removeProperty('width');
          // Ojo: justify-content y flex SÍ traían un valor propio (no el default)
          // en el HTML original de buildFooter(); setProperty() lo sobrescribe in
          // situ (no hay "capa" que restaurar con removeProperty), así que si el
          // usuario ve la vista móvil y luego la de escritorio en la misma sesión
          // (p. ej. con el selector de dispositivo del navegador) hay que
          // reafirmarlos explícitamente aquí o se quedan pisados por los valores
          // de móvil para siempre.
          leftEl.style.setProperty('justify-content', 'space-between', 'important');
          leftEl.style.setProperty('flex', '1 1 auto', 'important');
        }
        if (navEl) {
          // Mismo motivo que arriba: valor propio del HTML original, no el default.
          navEl.style.setProperty('align-items', 'flex-start', 'important');
        }
        if (logoWrap && logoSpan && logoWrap.offsetHeight > 0 && logoWrap.offsetWidth > 0) {
          // Limitado por alto Y ancho ("U_" en negrita mide ~1.15x su font-size)
          // para que nunca desborde su columna; *0.85 para que no toque los bordes.
          var logoSize = Math.min(logoWrap.offsetHeight, logoWrap.offsetWidth / 1.15) * 0.85;
          logoSpan.style.setProperty('font-size', logoSize + 'px', 'important');
        }
      }
    });

    // 4. Sticky reveal: .ag-section-blog se queda fija mientras el banner+footer suben y la tapan
    var blog = document.querySelector('.ag-section-blog');
    var footer = document.querySelector('footer.framer-CaFNh');
    var bannerWrap = document.querySelector('.framer-1hmgifw-container');
    var footerWrap = document.querySelector('.framer-s5vdhb-container');
    if (blog && footer) {
      var wrap = ensureStickyWrap(blog, bannerWrap, footerWrap);
      // top negativo = cuánto le sobra al blog respecto a un alto de pantalla. Con
      // top:0 un blog más alto que la pantalla (grid a 1 columna en móvil) se pega
      // apenas su borde superior toca arriba, sin haber dejado ver sus propias
      // tarjetas todavía. Con top:-excess no se pega hasta haber scrolleado ese
      // excedente de forma normal, y al pegarse ya se ve el final del módulo
      // (la vista queda igual que en desktop, donde el blog ya mide <= 1 pantalla).
      var excess = Math.max(0, blog.offsetHeight - window.innerHeight);
      blog.style.setProperty('position', 'sticky', 'important');
      blog.style.setProperty('top', (-excess) + 'px', 'important');
      blog.style.setProperty('z-index', '1', 'important');
      blog.style.setProperty('will-change', 'transform', 'important');
      blog.style.setProperty('transform', 'translateZ(0)', 'important');
      sizeStickyWrap(wrap, blog);
      if (!blog.dataset.agStickyFixed) {
        blog.dataset.agStickyFixed = '1';
        clearOverflowUp(wrap);
        window.addEventListener('resize', function () { sizeStickyWrap(wrap, blog); });
        changed = true;
      }
    }

    return changed;
  }

  // rAF loop — same pattern as antigravity-dom-observer
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
