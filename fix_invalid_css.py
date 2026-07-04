import glob

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Fix the invalid CSS
    content = content.replace("font-family: 'U_NDERS_FIX', inherit;", "font-family: 'U_NDERS_FIX', 'General Sans', sans-serif;")

    with open(filepath, 'w') as f:
        f.write(content)
        print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
