import glob

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # The pure CSS fix that does absolutely nothing to JS, only adds a font-face that maps the underscore
    # to Arial, and applies it to the mobile hero title elements.
    global_css = """<style>
@font-face {
  font-family: 'U_NDERS_FIX';
  src: local('Arial'), local('Helvetica'), local('sans-serif');
  unicode-range: U+005F;
}

/* Apply this fix globally on mobile devices */
@media (max-width: 809.98px) {
  body, h1, h2, p, div, span, .rolling-text-inner, .rolling-text-inner span {
    font-family: 'U_NDERS_FIX', inherit;
  }
}
</style>"""
    if "U_NDERS_FIX" not in content:
        content = content.replace('</head>', global_css + '\n</head>')

        with open(filepath, 'w') as f:
            f.write(content)
        print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
