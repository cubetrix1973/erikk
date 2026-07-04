import glob, re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Limpiar todo anterior
    content = re.sub(r'<style id="menu-fix">.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style id="mobile-menu-fix">.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script id="menu-fix">.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script id="mobile-menu-js">.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script id="jobs-intercept">.*?</script>', '', content, flags=re.DOTALL)

    # CLAVE: quitar #template-overlay del display:none (era el que causaba pantalla negra)
    content = content.replace('#template-overlay,', '')
    content = content.replace(', #template-overlay', '')
    content = content.replace('#template-overlay', '')

    # CSS minimo: solo ocultar Utility Pages
    CSS = """<style id="menu-fix">
/* Ocultar Utility Pages en el menu movil */
[data-framer-name="Utility Pages"] { display: none !important; }
</style>
"""

    # JS para reordenar (el overlay se renderiza en #template-overlay)
    JS = """<script id="menu-fix-js">
(function() {
    function fixMenu() {
        var portal = document.getElementById('template-overlay');
        if (!portal || !portal.children.length) return;

        var navPages = portal.querySelector('nav.framer-1a5fctm');
        var navCms   = portal.querySelector('nav.framer-2z7mtb');

        if (!navPages || !navCms) return;
        if (navPages.dataset.fixed) return;

        function getContainer(nav, href) {
            var a = nav.querySelector('a[href="' + href + '"]');
            if (!a) return null;
            var el = a;
            while (el.parentNode !== nav) el = el.parentNode;
            return el;
        }

        var aboutEl    = getContainer(navPages, 'about.html');
        var servicesEl = getContainer(navPages, 'services.html');
        var workEl     = getContainer(navCms,   'work.html');
        var newsEl     = getContainer(navCms,   'news.html');

        if (!aboutEl || !servicesEl || !workEl || !newsEl) {
            console.log('[menu-fix] missing:', !!aboutEl, !!servicesEl, !!workEl, !!newsEl);
            return;
        }

        navPages.innerHTML = '';
        navPages.appendChild(aboutEl);
        navPages.appendChild(servicesEl);
        navPages.appendChild(workEl);
        navPages.appendChild(newsEl);
        navPages.dataset.fixed = '1';

        var cmsCol = portal.querySelector('.framer-4lqmxf');
        if (cmsCol) cmsCol.style.setProperty('display', 'none', 'important');

        console.log('[menu-fix] DONE');
    }

    setInterval(fixMenu, 100);
})();
</script>"""

    content = content.replace('</head>', CSS + '\n</head>')
    content = content.replace('</body>', JS + '\n</body>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done: " + filepath)

for f in glob.glob('/home/dev/projects/erikk/*.html'):
    fix_file(f)
