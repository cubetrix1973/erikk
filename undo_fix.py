import glob

def undo_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    start_marker = "// NUEVO FIX PARA FORZAR EL GUION BAJO"
    end_marker = "// Reemplazo de Fashionwerk (Logo/Titular principal)"
    
    if start_marker in content and end_marker in content:
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)
        content = content[:start_idx] + content[end_idx:]
        with open(filepath, 'w') as f:
            f.write(content)

for f in glob.glob('/root/projects/erikk/*.html'):
    undo_file(f)
