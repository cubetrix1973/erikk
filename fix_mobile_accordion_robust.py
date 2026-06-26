import glob

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # We want to replace the old script or inject the new one.
    # Let's remove any previous fixMobileAccordion scripts first.
    import re
    content = re.sub(r'<script>\s*\(function\(\)\s*\{\s*function fixMobileAccordion\(\).*?</script>', '', content, flags=re.DOTALL)

    robust_logic = """<script>
(function() {
  function fixMobileAccordion() {
     // Do absolutely nothing on desktop width
     if (window.innerWidth >= 1280) {
         return;
     }
     // Encontrar todos los elementos que contengan "UTILITY PAGES" o "CMS" o "PAGES" in the menu
     var allEls = document.querySelectorAll('*');
     var targetLeafs = [];
     for (var i = 0; i < allEls.length; i++) {
         var el = allEls[i];
         if (el.children.length === 0) {
             var text = (el.textContent || '').trim().toUpperCase();
             if (text === 'UTILITY PAGES') {
                 targetLeafs.push(el);
             }
         }
     }
     
     for (var j = 0; j < targetLeafs.length; j++) {
         var parent = targetLeafs[j].parentNode;
         var safetyCounter = 0;
         while (parent && parent.tagName !== 'BODY' && safetyCounter < 10) {
             // Si el padre tiene entre 4 y 15 hijos, asumimos que es el contenedor de la lista del menú
             if (parent.children.length >= 4 && parent.children.length <= 15) {
                 // IGNORAR SI ES PARTE DEL FOOTER
                 var isFooter = false;
                 var tempP = parent;
                 while (tempP && tempP.tagName !== 'BODY') {
                     if (tempP.tagName === 'FOOTER' || (tempP.className && typeof tempP.className === 'string' && (tempP.className.toLowerCase().indexOf('footer') !== -1 || tempP.className.toLowerCase().indexOf('socials') !== -1))) {
                         isFooter = true;
                         break;
                     }
                     tempP = tempP.parentNode;
                 }
                 if (isFooter) {
                     parent = parent.parentNode;
                     safetyCounter++;
                     continue;
                 }

                 var hasHome = false;
                 for (var k = 0; k < parent.children.length; k++) {
                     var childTxt = (parent.children[k].textContent || '').toUpperCase();
                     if (childTxt.indexOf('HOME') !== -1) {
                         hasHome = true; break;
                     }
                 }
                 
                 if (hasHome) {
                     // Hemos encontrado el acordeón del menú móvil
                     parent.style.display = 'flex';
                     parent.style.flexDirection = 'column';
                     
                     for (var c = 0; c < parent.children.length; c++) {
                         var child = parent.children[c];
                         var txt = (child.textContent || '').toUpperCase();
                         
                         if (txt.indexOf('HOME') !== -1 && txt.indexOf('UTILITY') === -1) {
                             child.style.display = 'none';
                         } else if (txt.indexOf('UTILITY') !== -1) {
                             child.style.display = 'none';
                         } else if (txt.indexOf('NOSOTROS') !== -1 || txt.indexOf('ABOUT') !== -1) {
                             child.style.order = '1';
                             child.style.display = 'block';
                         } else if (txt.indexOf('SERVICIOS') !== -1 || txt.indexOf('SERVICES') !== -1) {
                             child.style.order = '2';
                             child.style.display = 'block';
                         } else if (txt.indexOf('PROYECTOS') !== -1 || txt.indexOf('WORK') !== -1 || txt.indexOf('JOBS') !== -1) {
                             child.style.order = '3';
                             child.style.display = 'block';
                             // Forzar href a work.html para el enlace
                             var link = child.querySelector('a');
                             if (link) link.setAttribute('href', 'work.html');
                         } else if (txt.indexOf('BLOG') !== -1 || txt.indexOf('NEWS') !== -1) {
                             child.style.order = '4';
                             child.style.display = 'block';
                             var link = child.querySelector('a');
                             if (link) link.setAttribute('href', 'news.html');
                         } else if (txt.indexOf('HABLEMOS') !== -1 || txt.indexOf('CONTACT') !== -1) {
                             child.style.order = '5';
                             child.style.display = 'block';
                             child.style.marginTop = '20px'; // Espacio antes del botón
                         } else {
                             // Ocultar cualquier otro elemento (páginas individuales, etc.)
                             child.style.display = 'none';
                         }
                     }
                     break; // Paramos de subir en el árbol
                 }
             }
             parent = parent.parentNode;
             safetyCounter++;
         }
     }
  }
  
  // Ejecutar el parche de forma continua para que pise siempre al React
  setInterval(fixMobileAccordion, 50);
})();
</script>
"""
    if "fixMobileAccordion" not in content:
        content = content.replace("</body>", robust_logic + "</body>")

    with open(filepath, 'w') as f:
        f.write(content)
        print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
