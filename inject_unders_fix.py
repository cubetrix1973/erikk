import glob

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    new_observer_logic = """
  // NUEVO FIX PARA FORZAR EL GUION BAJO EN U_NDERS CUALQUIERA QUE SEA SU ESTADO
  function forceUnderscore(root) {
      if (!root || !root.querySelectorAll) return;
      // Buscamos todos los elementos contenedores de texto que podrian tener U_NDERS o U NDERS
      var elements = root.querySelectorAll('h1, h2, p, div');
      for (var i = 0; i < elements.length; i++) {
          var el = elements[i];
          // Solo miramos elementos que directamente contengan el texto, o que sus hijos lo formen
          if (el.children.length === 0 || el.tagName === 'H1' || el.tagName === 'H2' || (el.className && typeof el.className === 'string' && el.className.indexOf('framer-') !== -1)) {
              var text = el.textContent || "";
              // Si el texto completo es exactamente "U NDERS", "U_NDERS", "UNDERS" (ignorando espacios extra)
              if (/^U\s*_?\s*N\s*D\s*E\s*R\s*S$/i.test(text.trim())) {
                  // Reemplazamos el innerHTML completamente para matar los spans de animacion y forzar el guion
                  var styleStr = "font-family: Arial, sans-serif !important; font-size: 0.8em !important; display: inline-block !important; color: inherit !important;";
                  var shift = window.innerWidth < 810 ? "transform: translateY(-5px) !important;" : "transform: translateY(-10px) !important;";
                  
                  // Evitamos loop infinito verificando si ya tiene el span Arial
                  if (el.innerHTML.indexOf('Arial') === -1) {
                      el.innerHTML = 'U<span class="unders-lift" style="' + styleStr + ' ' + shift + '">_</span>NDERS';
                  }
              }
          }
      }
  }
  
  // Ejecutamos en load y observador
  document.addEventListener('DOMContentLoaded', function() { forceUnderscore(document); });
  window.addEventListener('load', function() { forceUnderscore(document); });
  var undersObserver = new MutationObserver(function() { forceUnderscore(document); });
  undersObserver.observe(document.documentElement, { childList: true, subtree: true, characterData: true });
"""
        
    start_str = "// Reemplazo de Fashionwerk (Logo/Titular principal)"
    
    if start_str in content and "forceUnderscore" not in content:
        start_idx = content.find(start_str)
        content = content[:start_idx] + new_observer_logic + "\n        " + content[start_idx:]
        with open(filepath, 'w') as f:
            f.write(content)
        print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
