import glob
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Just replace the translateY(-8px) with translateY(-3px)
    content = content.replace("transform: translateY(-8px)", "transform: translateY(-3px)")

    with open(filepath, 'w') as f:
        f.write(content)
        print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
