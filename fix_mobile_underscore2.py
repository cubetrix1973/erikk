import glob

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    new_logic = """
        // Fix for individual underscore spans in animated components
        if (element.nodeValue === '_') {
            if (element.parentElement) {
                element.parentElement.style.setProperty('font-family', 'Arial, sans-serif', 'important');
                element.parentElement.style.setProperty('font-size', '0.8em', 'important');
                if (window.innerWidth < 810) {
                    element.parentElement.style.setProperty('transform', 'translateY(-2px)', 'important');
                    element.parentElement.style.setProperty('display', 'inline-block', 'important');
                } else {
                    element.parentElement.style.setProperty('transform', 'translateY(-5px)', 'important');
                    element.parentElement.style.setProperty('display', 'inline-block', 'important');
                }
            }
        }
    """
    
    start_str = "if (/Comprehensive\s+(branding|marketing\s+digital)\s+solutions/i.test(element.nodeValue)) {"
    
    if start_str in content and "element.nodeValue === '_'" not in content:
        content = content.replace(start_str, new_logic + "\n        " + start_str)
        with open(filepath, 'w') as f:
            f.write(content)
        print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
