#!/usr/bin/env python3
"""
Aktualisiert alle YAML-Dateien:
- Squarespace-URLs → Cloudinary-URLs
- Lokale /images/portfolio/ Pfade → Cloudinary-URLs

Benötigt: pip install pyyaml requests
Ausfuehren: python migrate_to_cloudinary.py
"""

import yaml, os, re, requests, hashlib
from pathlib import Path

# ── Konfiguration ──────────────────────────────────────────────────────────────
CLOUD_NAME   = "DEIN_CLOUD_NAME"    # z.B. dqww81axk
API_KEY      = "DEIN_API_KEY"
API_SECRET   = "DEIN_API_SECRET"
FOLDER       = "portfolio"
# ──────────────────────────────────────────────────────────────────────────────

def get_all_cloudinary_assets():
    """Lädt alle Assets aus dem portfolio-Ordner via Cloudinary Admin API."""
    assets = {}
    next_cursor = None
    
    print("Lade Cloudinary Asset-Liste...")
    while True:
        params = {
            "type": "upload",
            "prefix": FOLDER,
            "max_results": 500,
        }
        if next_cursor:
            params["next_cursor"] = next_cursor

        resp = requests.get(
            f"https://api.cloudinary.com/v1_1/{CLOUD_NAME}/resources/image",
            params=params,
            auth=(API_KEY, API_SECRET)
        )
        data = resp.json()
        
        if "error" in data:
            print(f"Cloudinary API Fehler: {data['error']['message']}")
            return {}

        for asset in data.get("resources", []):
            public_id = asset["public_id"]  # z.B. "portfolio/vasecocoon_fm6i8u"
            filename = Path(public_id).name  # z.B. "vasecocoon_fm6i8u"
            # Suffix entfernen (letzter _xxxxx Teil)
            base = re.sub(r'_[a-z0-9]{6,8}$', '', filename)
            url = asset["secure_url"]
            assets[base.lower()] = url
            assets[filename.lower()] = url  # auch mit Suffix speichern

        next_cursor = data.get("next_cursor")
        if not next_cursor:
            break

    print(f"  {len(assets)} Assets gefunden")
    return assets

def squarespace_to_filename(url):
    """Extrahiert den Dateinamen aus einer Squarespace-URL."""
    # z.B. .../vasecocoon.jpg?format=1000w → vasecocoon
    path = url.split("?")[0]
    name = path.split("/")[-1]
    stem = Path(name).stem
    return stem.lower()

def local_to_stem(path):
    """Extrahiert den Stem aus einem lokalen Pfad."""
    # z.B. /images/portfolio/DSCF9813.jpg → dscf9813
    return Path(path).stem.lower()

def find_cloudinary_url(key, assets):
    """Sucht die Cloudinary-URL für einen Dateinamen (case-insensitive)."""
    return assets.get(key.lower())

def process_yaml_value(value, assets, stats):
    """Ersetzt einen Bildpfad durch die Cloudinary-URL."""
    if not isinstance(value, str):
        return value
    
    if "squarespace-cdn.com" in value:
        stem = squarespace_to_filename(value)
        url = find_cloudinary_url(stem, assets)
        if url:
            stats["ersetzt"] += 1
            print(f"  ✓ Squarespace: {stem} → Cloudinary")
            return url
        else:
            stats["nicht_gefunden"] += 1
            print(f"  ✗ Nicht gefunden: {stem} (Squarespace)")
            return value

    if value.startswith("/images/portfolio/"):
        stem = local_to_stem(value)
        url = find_cloudinary_url(stem, assets)
        if url:
            stats["ersetzt"] += 1
            print(f"  ✓ Lokal: {stem} → Cloudinary")
            return url
        else:
            stats["nicht_gefunden"] += 1
            print(f"  ✗ Nicht gefunden: {stem} (lokal)")
            return value

    return value

def process_obj(obj, assets, stats):
    """Rekursiv alle Werte in einem Dict/List durchgehen."""
    if isinstance(obj, dict):
        return {k: process_obj(v, assets, stats) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [process_obj(item, assets, stats) for item in obj]
    elif isinstance(obj, str):
        return process_yaml_value(obj, assets, stats)
    return obj

def main():
    assets = get_all_cloudinary_assets()
    if not assets:
        print("Keine Assets gefunden – Abbruch.")
        return

    stats = {"ersetzt": 0, "nicht_gefunden": 0}
    
    # Kategorien
    kategorien_dir = Path("_kategorien")
    for fname in sorted(kategorien_dir.glob("*.yaml")):
        print(f"\n{fname.name}:")
        data = yaml.safe_load(fname.read_text(encoding="utf-8"))
        if not data:
            continue
        updated = process_obj(data, assets, stats)
        fname.write_text(
            yaml.dump(updated, allow_unicode=True, default_flow_style=False, sort_keys=False),
            encoding="utf-8"
        )

    # About (Profilfoto)
    about_file = Path("_data/about.yaml")
    print(f"\n{about_file.name}:")
    data = yaml.safe_load(about_file.read_text(encoding="utf-8"))
    updated = process_obj(data, assets, stats)
    about_file.write_text(
        yaml.dump(updated, allow_unicode=True, default_flow_style=False, sort_keys=False),
        encoding="utf-8"
    )

    print(f"\n{'─'*50}")
    print(f"✓ Ersetzt:        {stats['ersetzt']}")
    print(f"✗ Nicht gefunden: {stats['nicht_gefunden']}")
    if stats["nicht_gefunden"] > 0:
        print("  → Diese Bilder sind evtl. unter anderem Namen auf Cloudinary.")
    print("\nFertig! Bitte YAML-Dateien prüfen und dann committen.")

if __name__ == "__main__":
    main()
