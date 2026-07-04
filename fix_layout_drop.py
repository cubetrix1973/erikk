import glob
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # The previous logic has this block:
    # if (window.innerWidth < 810) {
    #     el.innerHTML = 'U<span style="display: inline-block !important; transform: translateY(5px) !important;">—</span>NDERS';
    # } else {
    
    old_mobile = "el.innerHTML = 'U<span style=\"display: inline-block !important; transform: translateY(5px) !important;\">—</span>NDERS';"
    
    # We will replace it with a relative-positioned span that does NOT use inline-block!
    # And we will use the underscore _ with Arial, just like desktop, but instead of transform we use relative top!
    new_mobile = "el.innerHTML = 'U<span style=\"font-family: Arial, sans-serif !important; position: relative !important; top: -2px !important; color: inherit !important;\">_</span>NDERS';"
    
    if old_mobile in content:
        content = content.replace(old_mobile, new_mobile)
        with open(filepath, 'w') as f:
            f.write(content)
        print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
