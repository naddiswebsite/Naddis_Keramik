#!/usr/bin/env python3
import yaml, os, shutil, re
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('_templates'), autoescape=True)

# Daten laden
with open('_data/nav.yaml', encoding='utf-8') as f:
    nav = yaml.safe_load(f)
with open('_data/about.yaml', encoding='utf-8') as f:
    about = yaml.safe_load(f)
with open('_data/course.yaml', encoding='utf-8') as f:
    course = yaml.safe_load(f)
with open('_data/imprint.yaml', encoding='utf-8') as f:
    imprint = yaml.safe_load(f)

import re

def cloudinary_resize(url, width):
    """Replace w_XXXX in a Cloudinary URL with a new width."""
    return re.sub(r'w_\d+', f'w_{width}', url)

env.globals['cloudinary_resize'] = cloudinary_resize

# Alle Kategorien laden und Bilder sammeln
kategorien = []
alle_bilder = []

for fname in sorted(os.listdir('_kategorien')):
    if not (fname.endswith('.yaml') or fname.endswith('.yml')):
        continue
    with open(os.path.join('_kategorien', fname), encoding='utf-8') as f:
        kat = yaml.safe_load(f)
    if not kat:
        continue
    if 'bilder' not in kat or kat['bilder'] is None:
        kat['bilder'] = []
    kategorien.append(kat)
    
    # Alle Bilder sammeln mit Kategorie-Info
    for bild in kat['bilder']:
        bild_entry = dict(bild)
        bild_entry['kategorie_slug'] = kat.get('slug', '')
        bild_entry['kategorie_name_de'] = kat.get('name_de', '')
        bild_entry['kategorie_name_it'] = kat.get('name_it', '')
        bild_entry['kategorie_name_en'] = kat.get('name_en', '')
        alle_bilder.append(bild_entry)

# dist/ aufbauen
os.makedirs('dist/de', exist_ok=True)
os.makedirs('dist/it', exist_ok=True)
os.makedirs('dist/en', exist_ok=True)

for fname in ['styles.css', 'scripts.js']:
    shutil.copy(fname, f'dist/{fname}')
    print(f'✓ dist/{fname}')

if os.path.exists('dist/admin'):
    shutil.rmtree('dist/admin')
shutil.copytree('admin', 'dist/admin')
print('✓ dist/admin/')

# Bilder kopieren - WICHTIG für Cloudflare Pages!
if os.path.exists('images/portfolio'):
    shutil.copytree('images/portfolio', 'dist/images/portfolio', dirs_exist_ok=True)
    img_count = len([f for f in os.listdir('images/portfolio') if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))])
    print(f'✓ dist/images/portfolio/ ({img_count} Bilder)')

# Seiten für alle drei Sprachen generieren
import random
for lang in ['de', 'it', 'en']:
    # Bilder randomisieren
    alle_bilder_shuffled = alle_bilder.copy()
    random.shuffle(alle_bilder_shuffled)
    
    ctx = dict(
        nav=nav,
        about=about,
        kategorien=kategorien,
        alle_bilder=alle_bilder_shuffled,
        lang=lang
    )

    # index.html - neue Filteransicht
    with open(f'dist/{lang}/index.html', 'w', encoding='utf-8') as f:
        f.write(env.get_template('index.html').render(**ctx))
    print(f'✓ dist/{lang}/index.html')

    # about.html
    with open(f'dist/{lang}/about.html', 'w', encoding='utf-8') as f:
        f.write(env.get_template('about.html').render(about=about, **ctx))
    print(f'✓ dist/{lang}/about.html')

    # course.html
    with open(f'dist/{lang}/course.html', 'w', encoding='utf-8') as f:
        f.write(env.get_template('course.html').render(course=course, **ctx))
    print(f'✓ dist/{lang}/course.html')

    # imprint.html
    with open(f'dist/{lang}/imprint.html', 'w', encoding='utf-8') as f:
        f.write(env.get_template('imprint.html').render(imprint=imprint, **ctx))
    print(f'✓ dist/{lang}/imprint.html')

# Root index.html: leitet zur Browsersprache weiter (DE als Standard)
root_redirect = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<script>
  var lang = (navigator.language || navigator.userLanguage || 'de').toLowerCase();
  if (lang.startsWith('it')) {
    window.location.replace('/it/index.html');
  } else if (lang.startsWith('en')) {
    window.location.replace('/en/index.html');
  } else {
    window.location.replace('/de/index.html');
  }
</script>
<meta http-equiv="refresh" content="0;url=/de/index.html">
</head>
<body></body>
</html>"""

with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(root_redirect)
print('✓ dist/index.html (Sprachweiche)')

print(f'\nBuild fertig → dist/ (DE + IT + EN, {len(alle_bilder)} Bilder, {len(kategorien)} Kategorien)')
