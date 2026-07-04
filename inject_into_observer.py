import re

with open('/home/dev/projects/erikk/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the test banner and old menu fix scripts
content = content.replace('<div style="position:fixed;top:0;left:0;right:0;background:red;color:white;z-index:99999;font-size:20px;text-align:center;padding:10px">ARCHIVO ACTUALIZADO v1</div>', '')
content = re.sub(r'<style id="menu-fix">.*?</style>', '', content, flags=re.DOTALL)
content = re.sub(r'<script id="menu-fix-js">.*?</script>', '', content, flags=re.DOTALL)
content = re.sub(r'<script id="menu-fix">.*?</script>', '', content, flags=re.DOTALL)

# Add the menu fix INSIDE the existing observer callback and also as a setInterval
# We inject right before the closing of the existing translation IIFE
# The existing observer is:
#   observer.observe(document.documentElement, { childList: true, subtree: true, characterData: true });
# We add our fix function and call it from there

menu_fix_code = """
  // === MENU MOVIL FIX: ocultar HOME, Utility Pages, y reordenar ===
  function fixMobileMenu() {
    // 1. Ocultar Utility Pages usando el atributo data-framer-name
    document.querySelectorAll('[data-framer-name="Utility Pages"]').forEach(function(el) {
      // Subir hasta el Column padre y ocultarlo
      var col = el;
      for (var i = 0; i < 5; i++) {
        if (!col.parentNode) break;
        col = col.parentNode;
        if (col.getAttribute && col.getAttribute('data-framer-name') === 'Column') {
          col.style.setProperty('display', 'none', 'important');
          break;
        }
      }
      el.style.setProperty('display', 'none', 'important');
    });

    // 2. Ocultar la nav de Utility Pages (framer-rcc1qw)
    document.querySelectorAll('nav.framer-rcc1qw').forEach(function(el) {
      el.style.setProperty('display', 'none', 'important');
    });

    // 3. Reordenar: mover work y news de nav CMS a nav Pages y reconstruir
    var navPages = document.querySelector('nav.framer-1a5fctm');
    var navCms   = document.querySelector('nav.framer-2z7mtb');
    if (!navPages || !navCms || navPages.dataset.mfixed) return;

    function getContainer(nav, href) {
      var a = nav.querySelector('a[href="' + href + '"]');
      if (!a) return null;
      var el = a;
      while (el.parentNode !== nav) el = el.parentNode;
      return el;
    }

    var homeEl     = getContainer(navPages, 'index.html');
    var aboutEl    = getContainer(navPages, 'about.html');
    var servicesEl = getContainer(navPages, 'services.html');
    var workEl     = getContainer(navCms, 'work.html');
    var newsEl     = getContainer(navCms, 'news.html');

    if (!aboutEl || !servicesEl || !workEl || !newsEl) return;

    // Ocultar HOME
    if (homeEl) homeEl.style.setProperty('display', 'none', 'important');

    // Reordenar dentro de navPages
    navPages.appendChild(aboutEl);
    navPages.appendChild(servicesEl);
    navPages.appendChild(workEl);
    navPages.appendChild(newsEl);
    navPages.dataset.mfixed = '1';

    // Ocultar columna CMS (ya vaciada)
    var cmsCol = document.querySelector('.framer-4lqmxf');
    if (cmsCol) cmsCol.style.setProperty('display', 'none', 'important');
  }
  // === FIN MENU MOVIL FIX ===
"""

# Inject the fixMobileMenu function before the observer is set up
# Find the MutationObserver setup in the existing script
target = "  var observer = new MutationObserver(function(mutations) {"

# Also modify the observer callback to call fixMobileMenu
new_observer = """  var observer = new MutationObserver(function(mutations) {
    fixMobileMenu();"""

content = content.replace(
    target,
    menu_fix_code + new_observer
)

# Also add a setInterval call after observer.observe to keep checking
target2 = "  observer.observe(document.documentElement, {"
content = content.replace(
    target2,
    "  setInterval(fixMobileMenu, 200);\n  observer.observe(document.documentElement, {"
)

with open('/home/dev/projects/erikk/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. Lines modified.")
