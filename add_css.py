import glob
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    css_fallback = """<style>
@media (max-width: 1279.98px) {
  .framer-jwc929, .framer-rcc1qw, .framer-anttwh {
    display: none !important;
  }
}
</style>"""

    # Remove any old injection of this css block if needed
    content = re.sub(r'<style>\s*@media \(max-width: 1279\.98px\) \{\s*\.framer-jwc929.*?</style>', '', content, flags=re.DOTALL)
    
    # Inject it right before </head>
    content = content.replace("</head>", css_fallback + "\n</head>")

    with open(filepath, 'w') as f:
        f.write(content)
        print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
