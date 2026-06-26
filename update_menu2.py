import glob

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find the start of the script
    start_idx = content.find('<script>\n(function() {\n  function fixMobileAccordion() {')
    if start_idx == -1:
        start_idx = content.find('<script>\\n(function() {\\n  function fixMobileAccordion() {')
    
    if start_idx != -1:
        end_idx = content.find('</script>', start_idx)
        if end_idx != -1:
            content = content[:start_idx] + content[end_idx + 9:]
    else:
        # Also try to remove any script that contains fixMobileAccordion
        parts = content.split('<script>')
        new_parts = [parts[0]]
        for p in parts[1:]:
            if 'fixMobileAccordion()' in p:
                end_script = p.find('</script>')
                if end_script != -1:
                    new_parts.append(p[end_script+9:])
                else:
                    new_parts.append('<script>' + p)
            else:
                new_parts.append('<script>' + p)
        content = ''.join(new_parts)

    robust_logic = """<script>
(function() {
  function fixMobileAccordion() {
     if (window.innerWidth >= 1280) return;
     
     var allEls = document.querySelectorAll('*');
     
     // 1. Ocultar los contenedores de Utility Pages / CMS / Pages
     for (var i = 0; i < allEls.length; i++) {
         var el = allEls[i];
         if (el.children.length === 0) {
             var text = (el.textContent || '').trim().toUpperCase();
             if (text === 'UTILITY PAGES' || text === 'CMS' || text === 'PAGES') {
                 var parent = el.parentNode;
                 var safetyCounter = 0;
                 while (parent && parent.tagName !== 'BODY' && safetyCounter < 5) {
                     if (parent.className && typeof parent.className === 'string' && parent.className.indexOf('framer-') !== -1) {
                         parent.style.display = 'none';
                         if (parent.nextSibling && parent.nextSibling.tagName === 'NAV') {
                             parent.nextSibling.style.display = 'none';
                         }
                     }
                     parent = parent.parentNode;
                     safetyCounter++;
                 }
             }
         }
     }

     // 2. Encontrar y ordenar el menú principal
     for (var j = 0; j < allEls.length; j++) {
         var parent = allEls[j];
         if (parent.children.length >= 4 && parent.children.length <= 15) {
             var isFooter = false;
             var tempP = parent;
             while (tempP && tempP.tagName !== 'BODY') {
                 if (tempP.tagName === 'FOOTER' || (tempP.className && typeof tempP.className === 'string' && (tempP.className.toLowerCase().indexOf('footer') !== -1 || tempP.className.toLowerCase().indexOf('socials') !== -1))) {
                     isFooter = true;
                     break;
                 }
                 tempP = tempP.parentNode;
             }
             if (isFooter) continue;

             var hasHome = false;
             for (var k = 0; k < parent.children.length; k++) {
                 var childTxt = (parent.children[k].textContent || '').toUpperCase();
                 if (childTxt.indexOf('HOME') !== -1) {
                     hasHome = true; break;
                 }
             }
             
             if (hasHome) {
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
                         var link = child.querySelector('a');
                         if (link) link.setAttribute('href', 'work.html');
                     } else if (txt.indexOf('BLOG') !== -1 || txt.indexOf('NEWS') !== -1) {
                         child.style.order = '4';
                         child.style.display = 'block';
                         var link = child.querySelector('a');
                         if (link) link.setAttribute('href', 'news.html');
                     } else {
                         // Ocultar cualquier otro, incluyendo Contact
                         child.style.display = 'none';
                     }
                 }
                 break; 
             }
         }
     }
  }
  
  setInterval(fixMobileAccordion, 50);
})();
</script>"""

    if "fixMobileAccordion" not in content:
        content = content.replace("</body>", robust_logic + "\n</body>")
        with open(filepath, 'w') as f:
            f.write(content)
            print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
