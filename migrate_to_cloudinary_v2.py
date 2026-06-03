#!/usr/bin/env python3
"""
Aktualisiert alle YAML-Dateien mit Cloudinary-URLs.
Keine API nötig – Zuordnung ist direkt eingebaut.

Ausfuehren: python3 migrate_to_cloudinary_v2.py
"""

import yaml, os, re
from pathlib import Path

CLOUD_NAME = "dqww81axk"

# Komplette Zuordnung: original-name (lowercase, ohne extension) → cloudinary public_id
CLOUDINARY_MAP = {
    "vasecocoon":              "portfolio/vasecocoon_fm6i8u",
    "wahl":                    "portfolio/wahl_d1dpp5",
    "vasemitloch":             "portfolio/vasemitloch_rruz7d",
    "vase mit blumen":         "portfolio/vase_mit_blumen_iozzye",
    "dscf9876":                "portfolio/DSCF9876_x9hfrt",
    "dscf9813":                "portfolio/DSCF9813_qdppuv",
    "tschurtsche":             "portfolio/tschurtsche_kjof3m",
    "20260509_145600":         "portfolio/20260509_145600_g492oq",
    "damen":                   "portfolio/damen_klcvrm",
    "ohnovorne":               "portfolio/ohnovorne_mdzxs0",
    "dsc01998":                "portfolio/DSC01998_yyfm9i",
    "dscf8620":                "portfolio/DSCF8620_csw65s",
    "dscf9235":                "portfolio/DSCF9235_usc587",
    "dscf8616":                "portfolio/DSCF8616_qtu7u0",
    "dscf9238":                "portfolio/DSCF9238_xseadk",
    "dsc01804":                "portfolio/DSC01804_cszvem",
    "dscf7559":                "portfolio/DSCF7559_ngld3l",
    "dsc01884":                "portfolio/DSC01884_dzdyku",
    "knospe":                  "portfolio/knospe_i1ljqa",
    "dsc01947":                "portfolio/DSC01947_koo401",
    "dsc01904":                "portfolio/DSC01904_ojxzxx",
    "dscf9052":                "portfolio/DSCF9052_kxg36h",
    "dscf7863":                "portfolio/DSCF7863_bokusz",
    "dscf8400":                "portfolio/DSCF8400_m5xpm4",
    "dscf9061":                "portfolio/DSCF9061_cebond",
    "dscf7953":                "portfolio/DSCF7953_yxyueh",
    "teller giacometti":       "portfolio/tELLER_GIACOMETTI_gx1mvb",
    "teller+giacometti":       "portfolio/tELLER_GIACOMETTI_gx1mvb",
    "dscf7917":                "portfolio/DSCF7917_rgmucw",
    "tassen(grünblau)":        "portfolio/tassen_grünblau_stltkw",
    "espresso":                "portfolio/espresso_g9fvyo",
    "eisbecher":               "portfolio/eisbecher_miudjt",
    "dscf0499":                "portfolio/DSCF0499_btqck0",
    "dscf0495":                "portfolio/DSCF0495_phueq6",
    "dscf0508":                "portfolio/DSCF0508_nhlspe",
    "dscf0494":                "portfolio/DSCF0494_bi7cre",
    "hängelampe.det.":         "portfolio/hängelampe.det._jg98kc",
    "lampeblume-ausschnitt":   "portfolio/lampeblume-ausschnitt_tq9suj",
    "dscf0533":                "portfolio/DSCF0533_abiq1y",
    "dsc01846":                "portfolio/DSC01846_zyex7k",
    "maskenadia":              "portfolio/maskenadia_nhb8ku",
    "dscf0546":                "portfolio/DSCF0546_n6qjyg",
    "kugelfisch":              "portfolio/kugelfisch_lq14zc",
    "dscf9143":                "portfolio/DSCF9143_kff6au",
    "maske":                   "portfolio/maske_vy5uzn",
    "blumeninwelle für dipl":  "portfolio/blumeninwelle_für_dipl_zwfhmf",
    "blumeninwelle_für_dipl":  "portfolio/blumeninwelle_für_dipl_zwfhmf",
    "presentazionwelle":       "portfolio/presentazionwelle_jfznje",
    "20230316_152442":         "portfolio/20230316_152442_d0lkzq",
    "dscf4508":                "portfolio/DSCF4508_j8tyg2",
    "2023_0427_15565300-2":    "portfolio/2023_0427_15565300-2_mthi0r",
    "blumecloseupmodell":      "portfolio/blumecloseupmodell_ehyofd",
}

def public_id_to_url(public_id):
    return f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/f_auto,q_auto,w_1800/{public_id}"

def squarespace_to_stem(url):
    path = url.split("?")[0]
    name = path.split("/")[-1]
    # URL-decode
    name = name.replace("+", " ").replace("%20", " ")
    return Path(name).stem.lower()

def local_to_stem(path):
    return Path(path).stem.lower()

def find_url(stem):
    key = stem.lower()
    if key in CLOUDINARY_MAP:
        return public_id_to_url(CLOUDINARY_MAP[key])
    return None

def process_value(value, stats):
    if not isinstance(value, str):
        return value

    if "squarespace-cdn.com" in value:
        stem = squarespace_to_stem(value)
        url = find_url(stem)
        if url:
            stats["ersetzt"] += 1
            print(f"  ✓ {stem}")
            return url
        else:
            stats["nicht_gefunden"] += 1
            print(f"  ✗ NICHT GEFUNDEN: {stem}")
            return value

    if value.startswith("/images/portfolio/"):
        stem = local_to_stem(value)
        url = find_url(stem)
        if url:
            stats["ersetzt"] += 1
            print(f"  ✓ {stem}")
            return url
        else:
            stats["nicht_gefunden"] += 1
            print(f"  ✗ NICHT GEFUNDEN: {stem}")
            return value

    return value

def process_obj(obj, stats):
    if isinstance(obj, dict):
        return {k: process_obj(v, stats) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [process_obj(item, stats) for item in obj]
    elif isinstance(obj, str):
        return process_value(obj, stats)
    return obj

def main():
    stats = {"ersetzt": 0, "nicht_gefunden": 0}

    for fname in sorted(Path("_kategorien").glob("*.yaml")):
        print(f"\n{fname.name}:")
        data = yaml.safe_load(fname.read_text(encoding="utf-8"))
        if not data:
            continue
        updated = process_obj(data, stats)
        fname.write_text(
            yaml.dump(updated, allow_unicode=True, default_flow_style=False, sort_keys=False),
            encoding="utf-8"
        )

    about = Path("_data/about.yaml")
    print(f"\n{about.name}:")
    data = yaml.safe_load(about.read_text(encoding="utf-8"))
    updated = process_obj(data, stats)
    about.write_text(
        yaml.dump(updated, allow_unicode=True, default_flow_style=False, sort_keys=False),
        encoding="utf-8"
    )

    print(f"\n{'─'*50}")
    print(f"✓ Ersetzt:        {stats['ersetzt']}")
    print(f"✗ Nicht gefunden: {stats['nicht_gefunden']}")
    print("\nFertig! Bitte committen und pushen.")

if __name__ == "__main__":
    main()
