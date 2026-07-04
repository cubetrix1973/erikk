import glob

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Inject global CSS if not present
    global_css = """<style>
@font-face {
  font-family: 'U_NDERS_FIX';
  src: local('Arial'), local('Helvetica');
  unicode-range: U+005F;
}
</style>"""
    if "U_NDERS_FIX" not in content:
        content = content.replace('</head>', global_css + '\n</head>')

    # The exact script block from the backup
    old_script_start = "// ROBUST HERO TITLE REPLACEMENT"
    old_script_end = "setInterval(forceHeroTitle, 200);"
    
    if old_script_start in content and old_script_end in content:
        start_idx = content.find(old_script_start)
        end_idx = content.find(old_script_end) + len(old_script_end)
        
        old_block = content[start_idx:end_idx]
        
        new_block = """// ROBUST HERO TITLE REPLACEMENT
  function forceHeroTitle() {
      // 1. Hero Title
      var els = document.querySelectorAll('h1, h2, p, div, span');
      for (var i = 0; i < els.length; i++) {
          var el = els[i];
          if (el.children.length === 0 || el.tagName === 'H1' || el.tagName === 'H2' || (el.className && typeof el.className === 'string' && el.className.indexOf('framer-') !== -1)) {
              var txt = (el.textContent || '').trim().toUpperCase().replace(/\\s/g, '');
              if (txt === 'FASHIONWERK' || txt === 'U_NDERS' || txt === 'UNDERS' || txt === 'U—NDERS') {
                  
                  if (window.innerWidth < 810) {
                      // MOBILE: PURE TEXT
                      if (el.textContent !== 'U_NDERS') {
                          el.style.fontFamily = "'U_NDERS_FIX', 'General Sans', sans-serif";
                          el.textContent = 'U_NDERS';
                      }
                  } else {
                      // DESKTOP: SPAN
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
      
      // 2. Logo SVG Replacement
      var links = document.querySelectorAll('a[href="index.html"], a[href="/"], a[href="./"]');
      for (var j = 0; j < links.length; j++) {
          var link = links[j];
          var linkTxt = (link.textContent || '').trim().toUpperCase().replace(/\\s/g, '');
          if (linkTxt === 'ERIKK®' || linkTxt === 'ERIKK' || linkTxt === 'U_NDERS' || linkTxt === 'UNDERS') {
              if (link.innerHTML.indexOf('<svg') !== -1) continue; // Already replaced
              
              var svgLogo = '<svg width="45" height="24" viewBox="0 0 50 25" fill="currentColor" xmlns="http://www.w3.org/2000/svg" style="display: block;"><path d="M 2,0 L 9,0 L 9,14 C 9,19 11,21 15,21 C 19,21 21,19 21,14 L 21,0 L 28,0 L 28,14 C 28,22 24,25 15,25 C 6,25 2,22 2,14 Z" /><rect x="32" y="21" width="17" height="4" /></svg>';
              
              var target = link.querySelector('.rolling-text-inner') || link.querySelector('.framer-mgrps-container > div') || link.querySelector('p') || link;
              
              if (target.classList && target.classList.contains('rolling-text-inner')) {
                  target = target.parentElement || target;
              }
              
              target.innerHTML = svgLogo;
              target.style.display = 'flex';
              target.style.alignItems = 'center';
              target.style.justifyContent = 'center';
          }
      }
  }
  setInterval(forceHeroTitle, 200);"""
        
        content = content.replace(old_block, new_block)
        
        with open(filepath, 'w') as f:
            f.write(content)
        print('Fixed ' + filepath)
    else:
        print('Could not find script block in ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
