#!/usr/bin/env python3
"""
Entfernt /portfolio/ aus den Cloudinary-URLs in allen YAML-Dateien.
Ausfuehren: python3 fix_cloudinary_urls.py
"""

import os
from pathlib import Path

def fix_file(path):
    text = path.read_text(encoding="utf-8")
    fixed = text.replace(
        "/image/upload/f_auto,q_auto,w_1800/portfolio/",
        "/image/upload/f_auto,q_auto,w_1800/"
    )
    if fixed != text:
        path.write_text(fixed, encoding="utf-8")
        print(f"  ✓ {path.name}")
        return True
    return False

count = 0
for fname in sorted(Path("_kategorien").glob("*.yaml")):
    if fix_file(fname):
        count += 1

if fix_file(Path("_data/about.yaml")):
    count += 1

print(f"\nFertig! {count} Dateien korrigiert.")
