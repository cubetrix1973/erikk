import glob

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # We will replace translateY(-2px) with translateY(-12px) in the CSS
    content = content.replace("transform: translateY(-2px) !important;", "transform: translateY(-12px) !important;")
    
    with open(filepath, 'w') as f:
        f.write(content)
        print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
