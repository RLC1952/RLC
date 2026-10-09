#!/usr/bin/env python3
"""
tools/normalize_news.py - Normalisiert news_archive.json nach Pages-CMS-Aenderungen.

Wird automatisch vom GitHub-Workflow .github/workflows/regen-news.yml ausgefuehrt,
sobald news_archive.json geaendert wird (z. B. durch Pages CMS). Aufgaben:

  1. Neue Beitraege (ohne gueltige ID) bekommen die naechste freie ID,
     Grossbuchstaben-Titel, deutsches Datum und die Legacy-URL.
  2. Fehlende Felder (url, content_html, images, date) werden ergaenzt
     (gleiche Logik wie tools/add_news.py).
  3. Bildpfade aus Pages CMS ("/assets/images/uploads/x.jpg") werden zu
     Repo-Pfaden ("assets/images/uploads/x.jpg") normalisiert.
  4. Archiv wird nach ID absteigend sortiert (neueste zuerst).
  5. Verwaiste Detailseiten (ID geloescht) werden entfernt.

Idempotent: Ein zweiter Lauf ohne Aenderungen schreibt nichts.
Nur Python-Stdlib, keine Abhaengigkeiten.
"""

import json
import shutil
import sys
from datetime import datetime
from html import escape
from pathlib import Path
import re

ROOT_DIR = Path(__file__).resolve().parent.parent
ARCHIVE_FILE = ROOT_DIR / "news_archive.json"
DETAIL_PAGES_DIR = ROOT_DIR / "pages" / "news"
OLD_SITE_URL = "https://www.rlc1952.de/rlc.php?id=0-0000-0-"

MONTHS_DE = [
    "", "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember"
]

DATE_PATTERN = re.compile(
    r"^\s*(\d{1,2})\. (Januar|Februar|März|April|Mai|Juni|Juli|August|"
    r"September|Oktober|November|Dezember) (\d{4})\s*$"
)


def german_date_today():
    now = datetime.now()
    return f"{now.day}. {MONTHS_DE[now.month]} {now.year}"


def normalize_date_for_new_entry(value):
    """Nur fuer NEUE Beitraege: gueltiges deutsches Datum behalten, sonst heute."""
    if isinstance(value, str) and DATE_PATTERN.match(value.strip()):
        return value.strip()
    return german_date_today()


def build_content_html(article):
    """Baut content_html wie tools/add_news.py (preView-Bild + Absaetze)."""
    text = (article.get("content_text") or "").strip()
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    if paragraphs:
        html_paragraphs = "".join(f"<p>{escape(p)}</p>" for p in paragraphs)
    else:
        html_paragraphs = f"<p>{escape(text)}</p>"

    images = article.get("images") or []
    if images:
        img_tag = (
            f'<div class="preView"><img alt="" '
            f'src="{escape(images[0].get("local", ""))}"/></div>'
        )
        return f"{img_tag}{html_paragraphs}"
    return html_paragraphs


def normalize_images(raw_images):
    """Bild-Objekte ({remote, local}) normalisieren; Pages-CMS-Pfade ent-slashen."""
    if not isinstance(raw_images, list):
        return []
    images = []
    for item in raw_images:
        if not isinstance(item, dict):
            continue
        local = str(item.get("local") or "").strip()
        if local.startswith("/"):
            local = local.lstrip("/")
        if not local:
            continue
        remote = str(item.get("remote") or "").strip()
        images.append({"remote": remote or local, "local": local})
    return images


def main():
    if not ARCHIVE_FILE.exists():
        print(f"FEHLER: {ARCHIVE_FILE} nicht gefunden!", file=sys.stderr)
        sys.exit(1)

    original_text = ARCHIVE_FILE.read_text(encoding="utf-8")
    try:
        archive = json.loads(original_text)
    except Exception as e:
        print(f"FEHLER beim Lesen von {ARCHIVE_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(archive, list):
        print("FEHLER: news_archive.json ist keine Liste!", file=sys.stderr)
        sys.exit(1)

    changed = False
    max_id = 10240
    for article in archive:
        if isinstance(article, dict) and str(article.get("id") or "").isdigit():
            max_id = max(max_id, int(article["id"]))

    # 1. Neue Beitraege (z. B. aus Pages CMS) vervollstaendigen
    for article in archive:
        if not isinstance(article, dict):
            print("FEHLER: Ungueltiger Eintrag (kein Objekt) im Archiv.", file=sys.stderr)
            sys.exit(1)

        if not str(article.get("id") or "").isdigit():
            max_id += 1
            str_id = str(max_id)
            article["id"] = str_id
            title = str(article.get("title") or "").strip().upper()
            article["title"] = title or "VEREINSMELDUNG"
            article["date"] = normalize_date_for_new_entry(article.get("date"))
            article["url"] = OLD_SITE_URL + str_id
            changed = True
            print(f"[+] Neuer Beitrag ID {str_id}: {article['title']}")

        str_id = article["id"]

        # 2. Fehlende Felder ergaenzen (bestehende Felder bleiben unangetastet)
        if not article.get("url"):
            article["url"] = OLD_SITE_URL + str_id
            changed = True

        if not article.get("date"):
            article["date"] = german_date_today()
            changed = True

        if not article.get("content_html"):
            article["content_html"] = build_content_html(article)
            changed = True

        # 3. Bilder normalisieren (fremde Eintraege bleiben identisch -> kein Diff)
        images = normalize_images(article.get("images"))
        if images != (article.get("images") or []):
            article["images"] = images
            changed = True

    # 4. Nach ID absteigend sortieren (neueste zuerst)
    ids = [int(a["id"]) for a in archive]
    if ids != sorted(ids, reverse=True):
        archive.sort(key=lambda item: int(item["id"]), reverse=True)
        changed = True
        print("[*] Archiv nach ID absteigend sortiert.")

    # 5. Verwaiste Detailseiten entfernen (Beitrag wurde geloescht)
    valid_ids = {str(a["id"]) for a in archive}
    if DETAIL_PAGES_DIR.exists():
        for page_file in DETAIL_PAGES_DIR.glob("*.html"):
            if page_file.stem.isdigit() and page_file.stem not in valid_ids:
                page_file.unlink()
                changed = True
                print(f"[-] Verwaiste Detailseite entfernt: {page_file.name}")

    # 6. Nur schreiben, wenn sich tatsaechlich etwas geaendert hat
    if not changed:
        print("[OK] Archiv bereits normalisiert - keine Aenderungen.")
        return

    tmp_file = ARCHIVE_FILE.with_suffix(".tmp")
    try:
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(archive, f, ensure_ascii=False, indent=2)
        shutil.move(str(tmp_file), str(ARCHIVE_FILE))
        print(f"[OK] news_archive.json normalisiert ({len(archive)} Beitraege).")
    except Exception as e:
        if tmp_file.exists():
            tmp_file.unlink()
        print(f"FEHLER beim Speichern: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()