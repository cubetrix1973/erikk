import os
import glob

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # We will search for the block:
    # if (/Fashionwerk/i.test(element.nodeValue)) {
    #   var parent = element.parentElement;
    #   if (parent) {
    #     if(window.innerWidth < 810) { element.nodeValue = "U_NDERS"; } else { parent.innerHTML = "U<span class=\"unders-lift\">_</span>NDERS"; }
    #   } else {
    #     element.nodeValue = 'U_NDERS';
    #   }
    # }

    new_logic = """        if (/Fashionwerk/i.test(element.nodeValue)) {
          var parent = element.parentElement;
          if (parent) {
             var isSvg = parent.tagName && parent.tagName.toLowerCase().includes('tspan');
             if(isSvg) { parent = parent.parentElement; }
             var isSvgText = parent && parent.tagName && parent.tagName.toLowerCase().includes('text');
             
             if (window.innerWidth < 810) {
                 if (isSvgText || isSvg) {
                     parent.innerHTML = 'U<tspan style="font-family: Arial, sans-serif; font-size: 0.8em;">_</tspan>NDERS';
                 } else {
                     parent.innerHTML = 'U<span class="unders-lift" style="font-family: Arial, sans-serif; font-size: 0.8em; transform: translateY(0px) !important;">_</span>NDERS';
                 }
             } else {
                 if (isSvgText || isSvg) {
                     parent.innerHTML = 'U<tspan class="unders-lift">_</tspan>NDERS';
                 } else {
                     parent.innerHTML = 'U<span class="unders-lift">_</span>NDERS';
                 }
             }
          } else {
            element.nodeValue = 'U_NDERS';
          }
        }"""
        
    # We need a regex or simple replace
    # Let's find the start and end of the block
    start_str = "if (/Fashionwerk/i.test(element.nodeValue)) {"
    end_str = "        // Reemplazo de Erikk en cargador"
    
    if start_str in content and end_str in content:
        start_idx = content.find(start_str)
        end_idx = content.find(end_str)
        content = content[:start_idx] + new_logic + "\n" + content[end_idx:]
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed {filepath}")

for f in glob.glob("/root/projects/erikk/*.html"):
    fix_file(f)
