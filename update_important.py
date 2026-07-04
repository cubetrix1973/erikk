import glob

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    new_logic = """        if (/Fashionwerk/i.test(element.nodeValue)) {
          var parent = element.parentElement;
          if (parent) {
             var isSvg = parent.tagName && parent.tagName.toLowerCase().includes('tspan');
             if(isSvg) { parent = parent.parentElement; }
             var isSvgText = parent && parent.tagName && parent.tagName.toLowerCase().includes('text');
             
             var styleStr = "font-family: Arial, sans-serif !important; font-size: 0.8em !important; display: inline-block !important;";
             
             if (window.innerWidth < 810) {
                 if (isSvgText || isSvg) {
                     parent.innerHTML = 'U<tspan style="' + styleStr + '">_</tspan>NDERS';
                 } else {
                     parent.innerHTML = 'U<span class="unders-lift" style="' + styleStr + ' transform: translateY(-5px) !important;">_</span>NDERS';
                 }
             } else {
                 if (isSvgText || isSvg) {
                     parent.innerHTML = 'U<tspan class="unders-lift" style="' + styleStr + '">_</tspan>NDERS';
                 } else {
                     parent.innerHTML = 'U<span class="unders-lift" style="' + styleStr + '">_</span>NDERS';
                 }
             }
          } else {
            element.nodeValue = 'U_NDERS';
          }
        }"""
        
    start_str = "if (/Fashionwerk/i.test(element.nodeValue)) {"
    end_str = "        // Reemplazo de Erikk en cargador"
    
    if start_str in content and end_str in content:
        start_idx = content.find(start_str)
        end_idx = content.find(end_str)
        content = content[:start_idx] + new_logic + "\n" + content[end_idx:]
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'Fixed {filepath}')

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
