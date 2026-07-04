(function () {
  'use strict';

  var blog = null, fw = null;
  var docTop = 0, blogH = 0;

  // DELAY: extra px of dark space between blog bottom and footer top.
  // Controls two things:
  //   (a) How long blog is fully visible before footer starts covering it.
  //   (b) Total scroll distance = blogH + DELAY (larger = slower reveal).
  // Currently DELAY = 50% of blogH  →  total travel = 1.5 × blogH.
  // To tune: change only this multiplier (0 = original speed, 1.0 = double).
  var DELAY_FACTOR = 0.5;
  var DELAY = 0;

  function measure() {
    blog.style.transform = '';
    var r = blog.getBoundingClientRect();
    docTop = r.top + window.pageYOffset;
    blogH  = r.height;
    DELAY  = Math.round(blogH * DELAY_FACTOR);
    fw.style.marginTop = DELAY + 'px';  // push footer down by DELAY px
  }

  function onScroll() {
    var offset = window.pageYOffset - docTop;
    if (offset > 0 && offset < blogH + DELAY) {
      // Keep blog visually frozen at viewport top while footer rises over it.
      // transform = offset counteracts exactly how far we've scrolled past docTop.
      blog.style.transform = 'translateY(' + offset + 'px)';
    } else {
      blog.style.transform = '';
    }
  }

  function onResize() {
    if (!blog || !fw) return;
    fw.style.marginTop = '';
    measure();
    onScroll();
  }

  function setup() {
    fw = document.querySelector('.framer-1hmgifw-container');
    if (!blog || !fw) return;

    fw.style.position        = 'relative';
    fw.style.zIndex          = '2';
    fw.style.backgroundColor = 'rgb(17,17,17)';

    measure();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onResize, { passive: true });
    onScroll();
  }

  var attempts = 0;
  var iv = setInterval(function () {
    blog = document.querySelector('.ag-section-blog');
    if (blog && document.querySelector('.framer-1hmgifw-container')) {
      clearInterval(iv);
      requestAnimationFrame(function () { requestAnimationFrame(setup); });
    }
    if (++attempts > 100) clearInterval(iv);
  }, 100);
})();
