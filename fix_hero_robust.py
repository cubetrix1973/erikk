import glob
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove the old Fashionwerk logic block
    old_logic_regex = r"\s*// Reemplazo de Fashionwerk.*?element\.nodeValue = 'U_NDERS';\s*\}\s*\}\s*\}\n"
    content = re.sub(old_logic_regex, '\n', content, flags=re.DOTALL)
    
    # We might have left some parts, let's just make sure we remove the Fashionwerk replacements
    content = re.sub(r'if \(/Fashionwerk/i\.test.*?(?:element\.nodeValue = \'U_NDERS\';|element\.nodeValue = \'U—NDERS\';)\s*\}\s*\}\s*\}', '', content, flags=re.DOTALL)

    new_robust_logic = """
  // ROBUST HERO TITLE REPLACEMENT
  function forceHeroTitle() {
      var els = document.querySelectorAll('h1, h2, p, div, span');
      for (var i = 0; i < els.length; i++) {
          var el = els[i];
          // Only check elements that have no children OR are block containers to avoid replacing document body
          if (el.children.length === 0 || el.tagName === 'H1' || el.tagName === 'H2' || (el.className && typeof el.className === 'string' && el.className.indexOf('framer-') !== -1)) {
              var txt = (el.textContent || '').trim().toUpperCase().replace(/\\s/g, '');
              if (txt === 'FASHIONWERK' || txt === 'U_NDERS' || txt === 'UNDERS') {
                  // Make sure we don't infinitely replace if it's already correct
                  if (el.innerHTML.indexOf('U—NDERS') !== -1 || el.innerHTML.indexOf('unders-lift') !== -1) {
                      continue;
                  }
                  
                  if (window.innerWidth < 810) {
                      el.innerHTML = 'U—NDERS';
                  } else {
                      var styleStr = "font-family: Arial, sans-serif !important; font-size: 0.8em !important; display: inline-block !important; transform: translateY(-5px) !important;";
                      el.innerHTML = 'U<span class="unders-lift" style="' + styleStr + '">_</span>NDERS';
                  }
              }
          }
      }
  }
  setInterval(forceHeroTitle, 200);
"""
    
    if "ROBUST HERO TITLE REPLACEMENT" not in content:
        # Inject at the end of the script block
        end_script = "</script>"
        if end_script in content:
            content = content.replace(end_script, new_robust_logic + "\n" + end_script)

    with open(filepath, 'w') as f:
        f.write(content)
        print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
