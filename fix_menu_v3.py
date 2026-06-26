import glob
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Clean old scripts
    content = re.sub(r'<script>\s*\(function\(\)\s*\{\s*function fixMobileAccordion\(\).*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style>\s*@media \(max-width: 1279\.98px\) \{\s*\.framer-jwc929.*?</style>', '', content, flags=re.DOTALL)

    robust_logic = """<script>
(function() {
  function fixMobileAccordion() {
     if (window.innerWidth >= 1280) return;
     
     var allEls = document.querySelectorAll('*');
     
     function isFooter(el) {
         var temp = el;
         while(temp && temp.tagName !== 'BODY') {
             if (temp.tagName === 'FOOTER' || (temp.className && typeof temp.className === 'string' && (temp.className.toLowerCase().indexOf('footer') !== -1 || temp.className.toLowerCase().indexOf('socials') !== -1))) {
                 return true;
             }
             temp = temp.parentNode;
         }
         return false;
     }

     // 1. Hide HABLEMOS, CONTACT, and UTILITY PAGES button/link globally in the mobile menu (not footer)
     for (var i = 0; i < allEls.length; i++) {
         if (allEls[i].children.length === 0) {
             var txt = (allEls[i].textContent || '').trim().toUpperCase();
             if (txt === 'HABLEMOS' || txt === 'CONTACT' || txt === 'UTILITY PAGES' || txt === 'CMS') {
                 if (!isFooter(allEls[i])) {
                     var p = allEls[i].parentNode;
                     var s = 0;
                     while (p && p.tagName !== 'BODY' && s < 6) {
                         if (p.tagName === 'A' || (p.className && typeof p.className === 'string' && p.className.indexOf('framer-') !== -1)) {
                             p.style.setProperty('display', 'none', 'important');
                             // Keep going up slightly to ensure we hide the whole wrapper if needed
                         }
                         p = p.parentNode;
                         s++;
                     }
                 }
             }
         }
     }

     // 2. Reorder main accordion menu
     var targetNode = null;
     for (var i = 0; i < allEls.length; i++) {
         if (allEls[i].children.length === 0) {
             var txt = (allEls[i].textContent || '').trim().toUpperCase();
             if ((txt === 'NOSOTROS' || txt === 'ABOUT') && !isFooter(allEls[i])) {
                 targetNode = allEls[i];
                 break;
             }
         }
     }
     
     if (targetNode) {
         var parent = targetNode.parentNode;
         var safety = 0;
         while (parent && parent.tagName !== 'BODY' && safety < 10) {
             if (parent.children.length >= 4 && parent.children.length <= 15) {
                 var fullText = parent.textContent.toUpperCase();
                 if (fullText.indexOf('SERVICIOS') !== -1 || fullText.indexOf('SERVICES') !== -1) {
                     parent.style.setProperty('display', 'flex', 'important');
                     parent.style.setProperty('flex-direction', 'column', 'important');
                     
                     for (var c = 0; c < parent.children.length; c++) {
                         var child = parent.children[c];
                         var childTxt = (child.textContent || '').toUpperCase();
                         
                         if (childTxt.indexOf('UTILITY PAGES') !== -1) {
                             child.style.setProperty('display', 'none', 'important');
                         } else if (childTxt.indexOf('NOSOTROS') !== -1 || childTxt.indexOf('ABOUT') !== -1) {
                             child.style.setProperty('order', '1', 'important');
                             child.style.setProperty('display', 'block', 'important');
                         } else if (childTxt.indexOf('SERVICIOS') !== -1 || childTxt.indexOf('SERVICES') !== -1) {
                             child.style.setProperty('order', '2', 'important');
                             child.style.setProperty('display', 'block', 'important');
                         } else if (childTxt.indexOf('PROYECTOS') !== -1 || childTxt.indexOf('WORK') !== -1 || childTxt.indexOf('JOBS') !== -1) {
                             child.style.setProperty('order', '3', 'important');
                             child.style.setProperty('display', 'block', 'important');
                         } else if (childTxt.indexOf('BLOG') !== -1 || childTxt.indexOf('NEWS') !== -1) {
                             child.style.setProperty('order', '4', 'important');
                             child.style.setProperty('display', 'block', 'important');
                         } else {
                             child.style.setProperty('display', 'none', 'important');
                         }
                     }
                     break;
                 }
             }
             parent = parent.parentNode;
             safety++;
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
