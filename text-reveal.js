(function () {
  var GRAY = '#cccccc';
  var FLASH = '#ffffff';

  // selector + texto final esperado (evita animar el texto en inglés
  // mientras antigravity-dom-observer todavía no lo tradujo)
  var TARGETS = [
    { selector: '.framer-bblil4 h1.framer-text', text: 'U_NDERS' },
    { selector: '.framer-zm9h0t h2.framer-text', text: 'Servicios' },
    { selector: '.framer-jy9ig2 h2.framer-text, .framer-jy9ig2 p.framer-text', text: 'Proyectos' },
    { selector: '.framer-1gh8q16 h2.framer-text', text: 'Clientes' },
    { selector: '.ag-section-blog h2.framer-text', text: 'Blog' }
  ];

  function splitLetters(el) {
    var frag = document.createDocumentFragment();
    var letters = [];
    // childNodes es una lista viva: hay que copiarla antes de mover nodos,
    // si no, mover un nodo durante el recorrido desplaza los índices y se
    // saltan hermanos (p. ej. "NDERS" desaparecía tras el span de "_").
    var children = Array.prototype.slice.call(el.childNodes);
    children.forEach(function (node) {
      if (node.nodeType === Node.TEXT_NODE) {
        node.textContent.split('').forEach(function (ch) {
          var span = document.createElement('span');
          span.className = 'reveal-letter';
          span.textContent = ch;
          letters.push(span);
          frag.appendChild(span);
        });
      } else if (node.textContent !== '') {
        // (los nodos vacíos, p. ej. un <br> residual de la hidratación de
        // React, no aportan nada visible: se dejan tal cual, sin envolver)
        var wrap = document.createElement('span');
        wrap.className = 'reveal-letter';
        wrap.appendChild(node);
        letters.push(wrap);
        frag.appendChild(wrap);
      } else {
        frag.appendChild(node);
      }
    });
    el.innerHTML = '';
    el.appendChild(frag);
    return letters;
  }

  function playReveal(el, letters, finalColor) {
    gsap.timeline()
      .to(letters, { color: FLASH, duration: 0.2, stagger: 0.045, ease: 'power1.out' }, 0)
      .to(letters, { color: finalColor, duration: 0.45, stagger: 0.045, ease: 'power1.inOut' }, 0.12);
  }

  // Prepara el título (letras separadas, en gris) y lo deja esperando a que
  // entre en el viewport para disparar la animación — no al cargar la
  // página, si no los títulos que están más abajo (Servicios, Proyectos,
  // Clientes, Blog) ya habrían "gastado" su animación fuera de pantalla.
  function prepare(el) {
    el.dataset.revealDone = '1';
    var finalColor = getComputedStyle(el).color;
    var letters = splitLetters(el);
    if (!letters.length) return;
    gsap.set(letters, { color: GRAY });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          io.unobserve(entry.target);
          playReveal(entry.target, letters, finalColor);
        }
      });
    }, { threshold: 0.2 });
    io.observe(el);
  }

  function tick() {
    TARGETS.forEach(function (t) {
      document.querySelectorAll(t.selector).forEach(function (el) {
        if (!el.dataset.revealDone && el.textContent.trim() === t.text) {
          prepare(el);
        }
      });
    });
  }

  function start() {
    if (typeof gsap === 'undefined') { setTimeout(start, 100); return; }
    var tries = 0;
    var iv = setInterval(function () {
      tick();
      if (++tries > 60) clearInterval(iv); // ~9s de margen para las traducciones/inyección del blog
    }, 150);
  }

  // Framer hidrata estos mismos títulos con React; si los tocamos mientras
  // hidrata, la hidratación falla y el título se queda vacío. Esperamos a
  // que asiente (mismo margen que usa antigravity-dom-observer) antes de
  // empezar a mirar el texto.
  function deferredStart() {
    setTimeout(start, 3000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', deferredStart);
  } else {
    deferredStart();
  }
})();
