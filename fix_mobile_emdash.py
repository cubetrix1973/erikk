import glob
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    new_logic = """        if (/Fashionwerk/i.test(element.nodeValue) || element.nodeValue.trim() === 'U_NDERS') {
          if (window.innerWidth < 810) {
              element.nodeValue = 'U—NDERS';
          } else {
              var parent = element.parentElement;
              if (parent) {
                 var isSvg = parent.tagName && parent.tagName.toLowerCase().includes('tspan');
                 if(isSvg) { parent = parent.parentElement; }
                 var isSvgText = parent && parent.tagName && parent.tagName.toLowerCase().includes('text');
                 
                 var styleStr = "font-family: Arial, sans-serif !important; font-size: 0.8em !important; display: inline-block !important; transform: translateY(-5px) !important;";
                 
                 if (isSvgText || isSvg) {
                     parent.innerHTML = 'U<tspan style="' + styleStr + '">_</tspan>NDERS';
                 } else {
                     parent.innerHTML = 'U<span class="unders-lift" style="' + styleStr + '">_</span>NDERS';
                 }
              } else {
                element.nodeValue = 'U_NDERS';
              }
          }
        }

        // Fix for individual underscore spans in animated components on mobile
        if (element.nodeValue === '_') {
            if (window.innerWidth < 810) {
                element.nodeValue = '—';
            } else {
                if (element.parentElement) {
                    element.parentElement.style.setProperty('font-family', 'Arial, sans-serif', 'important');
                    element.parentElement.style.setProperty('font-size', '0.8em', 'important');
                    element.parentElement.style.setProperty('transform', 'translateY(-5px)', 'important');
                    element.parentElement.style.setProperty('display', 'inline-block', 'important');
                }
            }
        }"""
        
    start_str = "if (/Fashionwerk/i.test(element.nodeValue) || element.nodeValue.trim() === 'U_NDERS') {"
    end_str = "        // Reemplazo de Erikk en cargador"
    
    if start_str in content and end_str in content:
        start_idx = content.find(start_str)
        end_idx = content.find(end_str)
        content = content[:start_idx] + new_logic + "\n" + content[end_idx:]

    # Remove the old individual underscore block if it exists before Comprehensive
    old_unders_regex = r"\s*// Fix for individual underscore spans in animated components\s*if \(element\.nodeValue === '_'\) \{[\s\S]*?\}\s*\n"
    content = re.sub(old_unders_regex, '\n', content)

    with open(filepath, 'w') as f:
        f.write(content)
        print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
