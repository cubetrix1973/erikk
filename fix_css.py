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
             
             if (isSvgText || isSvg) {
                 parent.innerHTML = 'U<tspan style="font-family: Arial, sans-serif !important; font-size: 0.8em !important;">_</tspan>NDERS';
             } else {
                 parent.innerHTML = 'U<span class="unders-lift" style="font-family: Arial, sans-serif !important; font-size: 0.8em !important;">_</span>NDERS';
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

    # Remove all aggressive transforms that could clip the text on mobile
    content = content.replace("transform: translateY(-10px) !important;", "transform: translateY(-2px) !important;")
    content = content.replace("transform: translateY(-15px) !important;", "transform: translateY(-2px) !important;")
    content = content.replace("transform: translateY(-25px) !important;", "transform: translateY(-5px) !important;")
    content = content.replace("transform: translateY(-35px) !important;", "transform: translateY(-8px) !important;")

    with open(filepath, 'w') as f:
        f.write(content)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
