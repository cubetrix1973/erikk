import glob
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    old_script_regex = r"// ROBUST HERO TITLE REPLACEMENT.*?setInterval\(forceHeroTitle, 200\);"
    
    new_script = """// ROBUST HERO TITLE REPLACEMENT
  function forceHeroTitle() {
      var els = document.querySelectorAll('h1, h2, p, div, span');
      for (var i = 0; i < els.length; i++) {
          var el = els[i];
          if (el.children.length === 0 || el.tagName === 'H1' || el.tagName === 'H2' || (el.className && typeof el.className === 'string' && el.className.indexOf('framer-') !== -1)) {
              var txt = (el.textContent || '').trim().toUpperCase().replace(/\\s/g, '');
              if (txt === 'FASHIONWERK' || txt === 'U_NDERS' || txt === 'UNDERS' || txt === 'U—NDERS') {
                  if (el.innerHTML.indexOf('unders-lift') !== -1) {
                      continue;
                  }
                  
                  // Destroy the rolling-text container completely by going up to the h1 or closest block wrapper
                  var targetEl = el;
                  if (el.classList && el.classList.contains('rolling-text-inner')) {
                      targetEl = el.parentElement || el;
                  } else if (el.tagName !== 'H1' && el.closest && el.closest('h1')) {
                      targetEl = el.closest('h1');
                  }
                  
                  // Use the exact same HTML that works perfectly on desktop
                  var styleStr = "font-family: Arial, sans-serif !important; font-size: 0.8em !important; display: inline-block !important;";
                  var shiftStr = window.innerWidth < 810 ? "transform: translateY(-8px) !important;" : "transform: translateY(-5px) !important;";
                  
                  targetEl.innerHTML = 'U<span class="unders-lift" style="' + styleStr + ' ' + shiftStr + '">_</span>NDERS';
                  targetEl.style.display = 'block'; // Ensure it's not a flex container that breaks spans
              }
          }
      }
  }
  setInterval(forceHeroTitle, 200);"""

    content = re.sub(old_script_regex, lambda m: new_script, content, flags=re.DOTALL)

    with open(filepath, 'w') as f:
        f.write(content)
        print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
