import glob

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # We will replace translateY(-2px) with translateY(-12px) in the JS
    content = content.replace("setProperty('transform', 'translateY(-2px)', 'important')", "setProperty('transform', 'translateY(-12px)', 'important')")
    # Let's also do translateY(-5px) -> translateY(-20px) for desktop just in case my previous fix broke it, but wait, the user said desktop is fine.
    # So I will just change the -2px one.
    
    with open(filepath, 'w') as f:
        f.write(content)
        print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
