import glob
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find the current robust logic and replace the mobile innerHTML
    old_mobile_logic = "el.innerHTML = 'U—NDERS';"
    new_mobile_logic = "el.innerHTML = 'U<span style=\"display: inline-block !important; transform: translateY(5px) !important;\">—</span>NDERS';"
    
    if old_mobile_logic in content:
        content = content.replace(old_mobile_logic, new_mobile_logic)
        with open(filepath, 'w') as f:
            f.write(content)
        print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
