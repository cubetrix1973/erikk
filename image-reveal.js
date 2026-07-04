(function () {
  // ojo: [data-framer-original-sizes] existe en el HTML estático pero
  // Framer lo borra al hidratar (lo usa una vez para fijar "sizes" y
  // luego lo quita) — hay que engancharse a un atributo que sobrevive.
  var SELECTOR = '[data-framer-background-image-wrapper="true"] img, .ag-blog-card__img-link img';
  var appearAncestors = [];

  // Framer controla estos contenedores con animaciones WAAPI propias
  // (element.animate(), con un "hold" inicial de 10s a opacity:0.001) que
  // ganan incluso a los estilos en línea con !important. Hay que
  // cancelarlas y reforzar el estado "asentado" en cada tick, no solo una
  // vez, porque Framer puede volver a lanzar la animación real más tarde
  // (al entrar en viewport) y nos la pisaría.
  function neutralizeAppearAncestors() {
    appearAncestors.forEach(function (el) {
      var anims = el.getAnimations();
      if (anims.length) anims.forEach(function (a) { a.cancel(); });
      if (el.style.opacity !== '1') el.style.setProperty('opacity', '1', 'important');
      if (el.style.transform !== 'none') el.style.setProperty('transform', 'none', 'important');
    });
  }

  function setupImages() {
    var found = false;
    document.querySelectorAll(SELECTOR).forEach(function (img) {
      if (img.dataset.revealSetup) return;
      img.dataset.revealSetup = '1';
      found = true;

      // Algunas fotos (hero/"About" y "Te acercamos el futuro") viven
      // dentro de un contenedor que Framer anima por su cuenta al entrar
      // en pantalla (fade + deslizamiento propio, data-framer-appear-id).
      // Ese efecto nativo se suma al nuestro y descoordina el barrido;
      // lo neutralizamos dejando el contenedor ya "asentado".
      var appearAncestor = img.closest('[data-framer-appear-id]');
      if (appearAncestor && appearAncestors.indexOf(appearAncestor) === -1) {
        appearAncestors.push(appearAncestor);
      }

      // Destello leve en barrido: la foto ya está visible tal cual, y una
      // franja de luz con degradado recorre de izquierda a derecha. Misma
      // envolvente de opacidad (0.2s de encendido + 0.45s de apagado,
      // arrancando el apagado a los 0.12s) que el flash de las letras en
      // text-reveal.js, para que fotos y títulos se sientan sincronizados;
      // el barrido en sí dura lo mismo que esa envolvente (0.57s).
      var parent = img.parentElement;
      parent.style.overflow = 'hidden';
      var flash = document.createElement('div');
      flash.className = 'reveal-flash';
      flash.style.cssText = 'position:absolute;top:0;left:0;width:35%;height:100%;pointer-events:none;z-index:1;background:linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.85) 50%, rgba(255,255,255,0) 100%);';
      parent.appendChild(flash);

      gsap.set(flash, { opacity: 0, xPercent: -140 });

      var tl = gsap.timeline({
        scrollTrigger: { trigger: img, start: 'top 88%', once: true },
        onComplete: function () { flash.remove(); }
      });
      tl.to(flash, { xPercent: 240, duration: 0.57, ease: 'power1.inOut' }, 0)
        .to(flash, { opacity: 1, duration: 0.2, ease: 'power1.out' }, 0)
        .to(flash, { opacity: 0, duration: 0.45, ease: 'power1.inOut' }, 0.12);
      // Las imágenes con loading="lazy" (tarjetas del Blog) todavía no
      // tienen tamaño real cuando se crea el ScrollTrigger; al cargar,
      // el layout puede moverse y hay que recalcular el punto de disparo.
      if (!img.complete) {
        img.addEventListener('load', function () { ScrollTrigger.refresh(); }, { once: true });
      }
    });
    if (found) ScrollTrigger.refresh();
  }

  function start() {
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
      setTimeout(start, 100);
      return;
    }
    gsap.registerPlugin(ScrollTrigger);
    setupImages();
    // El bloque de Blog se inyecta por JS unos instantes después de cargar
    // la página (footer-override.js); seguimos revisando un rato para
    // engancharle el mismo efecto en cuanto aparece.
    var tries = 0;
    var iv = setInterval(function () {
      setupImages();
      if (++tries > 40) clearInterval(iv);
    }, 200);
    // Esta, en cambio, no se para nunca: Framer puede relanzar su propia
    // animación de aparición en cualquier momento (al hacer scroll hasta
    // el elemento), así que hay que seguir peleándola indefinidamente.
    setInterval(neutralizeAppearAncestors, 200);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
