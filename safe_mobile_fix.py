import glob

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Update the CSS to be strongly targeted to the hero title with !important
    old_css = """@media (max-width: 809.98px) {
  body, h1, h2, p, div, span, .rolling-text-inner, .rolling-text-inner span {
    font-family: 'U_NDERS_FIX', 'General Sans', sans-serif;
  }
}"""
    new_css = """@media (max-width: 809.98px) {
  .framer-10mngps h1, .framer-10mngps h1 *, h1.framer-text, h1.framer-text * {
    font-family: 'U_NDERS_FIX', 'General Sans', sans-serif !important;
  }
}"""
    if old_css in content:
        content = content.replace(old_css, new_css)
    elif "U_NDERS_FIX" not in content:
        # Just in case the CSS isn't there at all
        global_css = """<style>
@font-face {
  font-family: 'U_NDERS_FIX';
  src: local('Arial'), local('Helvetica'), local('sans-serif');
  unicode-range: U+005F;
}
""" + new_css + "\n</style>\n</head>"
        content = content.replace('</head>', global_css)

    # 2. Update the JS logic precisely
    old_js = """        // Reemplazo de Fashionwerk (Logo/Titular principal)
        if (/Fashionwerk/i.test(element.nodeValue)) {
          var parent = element.parentElement;
          if (parent) {
            parent.innerHTML = 'U<span class="unders-lift">_</span>NDERS';
          } else {
            element.nodeValue = 'U_NDERS';
          }
        }"""
        
    new_js = """        // Reemplazo de Fashionwerk (Logo/Titular principal)
        if (/Fashionwerk/i.test(element.nodeValue)) {
          if (window.innerWidth < 810) {
            // MOBILE: Pure text
            element.nodeValue = 'U_NDERS';
          } else {
            // DESKTOP: Original span logic (UNTOUCHED)
            var parent = element.parentElement;
            if (parent) {
              parent.innerHTML = 'U<span class="unders-lift">_</span>NDERS';
            } else {
              element.nodeValue = 'U_NDERS';
            }
          }
        }"""
        
    if old_js in content:
        content = content.replace(old_js, new_js)

    with open(filepath, 'w') as f:
        f.write(content)
        print('Fixed ' + filepath)

for f in glob.glob('/root/projects/erikk/*.html'):
    fix_file(f)
