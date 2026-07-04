import glob
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # We will inject a global CSS rule to force Arial for the underscore character
    global_css = """<style>
@font-face {
  font-family: 'U_NDERS_FIX';
  src: local('Arial'), local('Helvetica');
  unicode-range: U+005F;
}
</style>"""
    if "U_NDERS_FIX" not in content:
        content = content.replace('</head>', global_css + '\n</head>')

    # Update the script to use pure text on mobile
    old_script_regex = r"// ROBUST HERO TITLE REPLACEMENT.*?setInterval\(forceHeroTitle, 200\);"
    
    new_script = """// ROBUST HERO TITLE REPLACEMENT
  function forceHeroTitle() {
      var els = document.querySelectorAll('h1, h2, p, div, span');
      for (var i = 0; i < els.length; i++) {
          var el = els[i];
          if (el.children.length === 0 || el.tagName === 'H1' || el.tagName === 'H2' || (el.className && typeof el.className === 'string' && el.className.indexOf('framer-') !== -1)) {
              var txt = (el.textContent || '').trim().toUpperCase().replace(/\\s/g, '');
              if (txt === 'FASHIONWERK' || txt === 'U_NDERS' || txt === 'UNDERS' || txt === 'U—NDERS') {
                  
                  if (window.innerWidth < 810) {
                      // MOBILE: PURE TEXT to avoid breaking layout. Global CSS forces Arial for the underscore.
                      if (el.textContent !== 'U_NDERS') {
                          // Apply the font-family directly to the container to ensure it uses the fix
                          el.style.fontFamily = "'U_NDERS_FIX', 'General Sans', sans-serif";
                          el.textContent = 'U_NDERS';
                      }
                  } else {
                      // DESKTOP: Keep the span injection since it works fine there
                      if (el.innerHTML.indexOf('unders-lift') !== -1) {
                          continue;
                      }
                      var targetEl = el;
                      if (el.classList && el.classList.contains('rolling-text-inner')) {
                          targetEl = el.parentElement || el;
                      } else if (el.tagName !== 'H1' && el.closest && el.closest('h1')) {
                          targetEl = el.closest('h1');
                      }
                      var styleStr = "font-family: Arial, sans-serif !important; font-size: 0.8em !important; display: inline-block !important; transform: translateY(-5px) !important;";
                      targetEl.innerHTML = 'U<span class="unders-lift" style="' + styleStr + '">_</span>NDERS';
                  }
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
