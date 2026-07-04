import glob

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    old_cond = "if (/Fashionwerk/i.test(element.nodeValue)) {"
    new_cond = "if (/Fashionwerk/i.test(element.nodeValue) || element.nodeValue.trim() === 'U_NDERS') {"
    
    if old_cond in content:
        content = content.replace(old_cond, new_cond)
        with open(filepath, 'w') as f:
            f.write(content)
        print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
