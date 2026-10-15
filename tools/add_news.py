#!/usr/bin/env python3
"""
tools/add_news.py - Idiotensicherer News-Generator fuer RLC 1952

Ermoeglicht es KIs (Claude, Cursor, Copilot) und Redakteuren, mit einem einzigen
Befehl einen neuen News-/Blog-Beitrag anzulegen, ohne das 1-MB-JSON manuell zu bearbeiten.

Verwendung:
    python tools/add_news.py --title "Titel des Beitrags" --text "Inhalt..." [--date "03. September 2026"] [--image "pfad/zum/bild.jpg"]
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
ARCHIVE_FILE = ROOT_DIR / "news_archive.json"
CURRENT_FILE = ROOT_DIR / "news_current.json"
NEWS_ASSETS_DIR = ROOT_DIR / "news_assets"
MERGE_SCRIPT = ROOT_DIR / "tools" / "merge_news.py"
GENERATE_SCRIPT = ROOT_DIR / "generate_detail_pages.py"
UPDATE_SCRIPT = ROOT_DIR / "update_js_data.py"

MONTHS_DE = [
    "", "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember"
]

def get_current_date_de():
    now = datetime.datetime.now()
    return f"{now.day}. {MONTHS_DE[now.month]} {now.year}"

def clean_title(title):
    return title.strip().upper()

def main():
    parser = argparse.ArgumentParser(description="Neuen Newsbeitrag fuer RLC 1952 anlegen")
    parser.add_argument("--title", required=True, help="Titel/Ueberschrift der Meldung")
    parser.add_argument("--text", required=True, help="Textinhalt des Beitrags (Absaetze durch Zeilenumbrueche trennen)")
    parser.add_argument("--date", default=None, help="Datum (z.B. '03. September 2026', Standard: heute)")
    parser.add_argument("--image", default=None, help="Optionaler Pfad zu einem Bild")
    parser.add_argument("--skip-gen", action="store_true", help="Detailseiten-Generierung ueberspringen (nur fuer Tests)")

    args = parser.parse_args()

    if not CURRENT_FILE.exists():
        print(f"FEHLER: {CURRENT_FILE} nicht gefunden!", file=sys.stderr)
        sys.exit(1)
    if not ARCHIVE_FILE.exists():
        print(f"FEHLER: {ARCHIVE_FILE} nicht gefunden!", file=sys.stderr)
        sys.exit(1)

    # 1. JSON sicher laden (CMS-Datei news_current.json ist die Schreib-Quelle)
    try:
        with open(CURRENT_FILE, "r", encoding="utf-8") as f:
            current = json.load(f)
        with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
            archive = json.load(f)
    except Exception as e:
        print(f"FEHLER beim Lesen der News-Dateien: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Naechste ID ermitteln (ueber beide Dateien, damit nichts kollidiert)
    existing_ids = [int(item["id"]) for item in current + archive if str(item.get("id", "")).isdigit()]
    next_id = max(existing_ids) + 1 if existing_ids else 10000
    str_id = str(next_id)

    # 3. Datum formatieren
    article_date = args.date.strip() if args.date else get_current_date_de()

    # 4. Bild verarbeiten
    images_list = []
    if args.image:
        src_image = Path(args.image).resolve()
        if src_image.exists() and src_image.is_file():
            target_dir = NEWS_ASSETS_DIR / str_id
            target_dir.mkdir(parents=True, exist_ok=True)
            
            clean_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', src_image.name)
            target_file = target_dir / clean_name
            shutil.copy2(src_image, target_file)

            rel_local_path = f"news_assets/{str_id}/{clean_name}"
            images_list.append({
                "remote": f"https://www.rlc1952.de/{rel_local_path}",
                "local": rel_local_path
            })
            print(f"[+] Bild kopiert nach: {rel_local_path}")
        else:
            print(f"[!] Warnung: Angegebenes Bild '{args.image}' existiert nicht. Beitrag wird ohne Bild angelegt.")

    # 5. HTML und Text aufbereiten
    text_content = args.text.strip()
    paragraphs = [p.strip() for p in text_content.split("\n") if p.strip()]
    if paragraphs:
        html_paragraphs = "".join(f"<p>{p}</p>" for p in paragraphs)
    else:
        html_paragraphs = f"<p>{text_content}</p>"

    if images_list:
        img_tag = f'<div class="preView"><img alt="" src="{images_list[0]["local"]}"/></div>'
        content_html = f"{img_tag}{html_paragraphs}"
    else:
        content_html = html_paragraphs

    # 6. Artikel-Objekt erstellen
    new_article = {
        "url": f"https://www.rlc1952.de/rlc.php?id=0-0000-0-{str_id}",
        "id": str_id,
        "title": clean_title(args.title),
        "date": article_date,
        "content_html": content_html,
        "content_text": text_content,
        "images": images_list
    }

    # 7. Vorne in news_current.json einfuegen (neueste zuerst)
    current.insert(0, new_article)

    # 8. Atomar speichern
    tmp_file = CURRENT_FILE.with_suffix(".tmp")
    try:
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(current, f, ensure_ascii=False, indent=2)
        shutil.move(tmp_file, CURRENT_FILE)
        print(f"[+] news_current.json aktualisiert (Artikel-ID: {str_id})")
    except Exception as e:
        if tmp_file.exists():
            tmp_file.unlink()
        print(f"FEHLER beim Speichern: {e}", file=sys.stderr)
        sys.exit(1)

    # 9. Automatisch Archiv spiegeln, Detailseiten und news_data.js regenerieren
    if not args.skip_gen:
        print("[*] Generiere Detailseite und aktualisiere JavaScript-Datenbestand...")
        try:
            subprocess.run([sys.executable, str(MERGE_SCRIPT)], check=True, cwd=str(ROOT_DIR))
            subprocess.run([sys.executable, str(GENERATE_SCRIPT)], check=True, cwd=str(ROOT_DIR))
            subprocess.run([sys.executable, str(UPDATE_SCRIPT)], check=True, cwd=str(ROOT_DIR))
            print(f"[OK] Fertig! Neuer Artikel verfuegbar:")
            print(f"     -> Detailseite: pages/news/{str_id}.html")
            print(f"     -> Uebersicht:   pages/news.html")
        except subprocess.CalledProcessError as e:
            print(f"[!] Warnung: Fehler bei Folge-Generierung: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
