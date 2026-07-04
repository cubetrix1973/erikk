import glob, re

CSS = """<style id="perfect-mobile-menu">
/* 1. Ensure the main container is a flex column */
.framer-CaFNh .framer-kshall {
  display: flex !important;
  flex-direction: column !important;
}

/* 2. Flatten the columns and nav elements so the link containers become flex children of .framer-kshall */
.framer-CaFNh .framer-19lxc5z,
.framer-CaFNh .framer-4lqmxf,
.framer-CaFNh .framer-1a5fctm,
.framer-CaFNh .framer-2z7mtb {
  display: contents !important;
}

/* 3. Hide all columns/navs content by default inside the right menu */
.framer-CaFNh .framer-kshall > * > * {
  display: none !important;
}
.framer-CaFNh .framer-kshall > * > nav > * {
  display: none !important;
}

/* 4. Show only our 4 specific menu items and set their order */
/* Using high specificity to override the hide rule above */
.framer-CaFNh .framer-kshall > * > nav > .framer-jlnza5-container, 
.framer-CaFNh .framer-kshall > * > nav > .framer-x12e3p-container {
  display: flex !important;
  order: 1 !important;
}
.framer-CaFNh .framer-kshall > * > nav > .framer-14yq27-container, 
.framer-CaFNh .framer-kshall > * > nav > .framer-9zxxrb-container {
  display: flex !important;
  order: 2 !important;
}
.framer-CaFNh .framer-kshall > * > nav > .framer-1t5plof-container, 
.framer-CaFNh .framer-kshall > * > nav > .framer-11cl96-container {
  display: flex !important;
  order: 3 !important;
}
.framer-CaFNh .framer-kshall > * > nav > .framer-1ob0dnm-container, 
.framer-CaFNh .framer-kshall > * > nav > .framer-1xzfylx-container {
  display: flex !important;
  order: 4 !important;
}

/* 5. Hide Utility Pages entirely */
.framer-CaFNh .framer-anttwh {
  display: none !important;
}
</style>
"""

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(r'<style id="perfect-mobile-menu">.*?</style>', '', content, flags=re.DOTALL)
    content = content.replace('</head>', CSS + '\n</head>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for f in glob.glob('/home/dev/projects/erikk/*.html'):
    clean_file(f)
