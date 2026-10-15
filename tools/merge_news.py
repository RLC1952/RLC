#!/usr/bin/env python3
"""
tools/merge_news.py - Spiegelt news_current.json in news_archive.json.

Das Pages CMS pflegt nur news_current.json (Beitraege ab 2025, ~100 Eintraege),
damit die CMS-Liste klein und schnell bleibt. Dieses Skript laeuft im
GitHub-Workflow .github/workflows/regen-news.yml VOR normalize_news.py und:

  1. Vervollstaendigt neue Eintraege in news_current.json (ID vergeben,
     Grossbuchstaben-Titel, deutsches Datum, content_html, Bildpfade) -
     dieselbe Logik wie tools/normalize_news.py.
  2. Sortiert news_current.json nach ID absteigend (neueste zuerst).
  3. Schreibt news_current.json ZURUECK (damit vergebene IDs im CMS ankommen).
  4. Ersetzt im Archiv alle Eintraege mit ID >= CURRENT_MIN_ID durch die
     Version aus news_current.json (inkl. Loeschungen: ein im CMS geloeschter
     Beitrag verschwindet auch aus dem Archiv).
  5. Idempotent: Ein zweiter Lauf ohne Aenderungen schreibt nichts.

Nur Python-Stdlib, keine Abhaengigkeiten.
"""

import json
import shutil
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "tools"))

from normalize_news import (  # noqa: E402
    DATE_PATTERN,
    german_date_today,
    build_content_html,
    normalize_images,
)

CURRENT_FILE = ROOT_DIR / "news_current.json"
ARCHIVE_FILE = ROOT_DIR / "news_archive.json"

# Ab dieser ID ist news_current.json die fuehrende Quelle (Beitraege ab 2025).
# Aendert sich der Schnitt nur nach hinten (neue Jahre), bleibt der Wert gueltig.
CURRENT_MIN_ID = 10128


def valid_id(article):
    return isinstance(article, dict) and str(article.get("id") or "").isdigit()


def normalize_current_entries(current, max_id):
    """Neue Eintraege vervollstaendigen; Rueckgabe (geaendert?, max_id)."""
    changed = False
    for article in current:
        if not isinstance(article, dict):
            print("FEHLER: Ungueltiger Eintrag (kein Objekt) in news_current.json.",
                  file=sys.stderr)
            sys.exit(1)
        if not str(article.get("id") or "").isdigit():
            max_id += 1
            str_id = str(max_id)
            article["id"] = str_id
            title = str(article.get("title") or "").strip().upper()
            article["title"] = title or "VEREINSMELDUNG"
            date_value = article.get("date")
            if not (isinstance(date_value, str) and DATE_PATTERN.match(date_value.strip())):
                article["date"] = german_date_today()
            article["url"] = "https://www.rlc1952.de/rlc.php?id=0-0000-0-" + str_id
            if not article.get("content_html"):
                article["content_html"] = build_content_html(article)
            article["images"] = normalize_images(article.get("images"))
            changed = True
            print(f"[+] Neuer Beitrag ID {str_id}: {article['title']}")
    return changed, max_id


def write_json(path, data):
    tmp = path.with_suffix(".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        shutil.move(str(tmp), str(path))
    except Exception as e:
        if tmp.exists():
            tmp.unlink()
        print(f"FEHLER beim Schreiben von {path.name}: {e}", file=sys.stderr)
        sys.exit(1)


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"FEHLER beim Lesen von {path}: {e}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, list):
        print(f"FEHLER: {path.name} ist keine Liste!", file=sys.stderr)
        sys.exit(1)
    return data


def main():
    if not CURRENT_FILE.exists():
        print(f"FEHLER: {CURRENT_FILE} nicht gefunden!", file=sys.stderr)
        sys.exit(1)
    if not ARCHIVE_FILE.exists():
        print(f"FEHLER: {ARCHIVE_FILE} nicht gefunden!", file=sys.stderr)
        sys.exit(1)

    current = load_json(CURRENT_FILE)
    archive = load_json(ARCHIVE_FILE)

    all_ids = [int(a["id"]) for a in archive + current if valid_id(a)]
    max_id = max(all_ids, default=10240)

    # 1+2. Neue CMS-Eintraege vervollstaendigen
    changed, max_id = normalize_current_entries(current, max_id)

    # 3. news_current.json absteigend sortieren und ZURUECKSCHREIBEN
    #    (vergebene IDs und Normalisierungen muessen ins CMS zurueck)
    current_sorted = sorted(current, key=lambda a: int(a["id"]), reverse=True)
    if current_sorted != current or changed:
        write_json(CURRENT_FILE, current_sorted)
        current = current_sorted
        changed = True

    # 4. Archiv spiegeln: alles unterhalb der Schwelle bleibt, oberhalb gilt current
    keep_old = [a for a in archive
                if valid_id(a) and int(a["id"]) < CURRENT_MIN_ID]
    new_archive = sorted(keep_old + current,
                         key=lambda a: int(a["id"]), reverse=True)
    if new_archive != archive:
        write_json(ARCHIVE_FILE, new_archive)
        changed = True
        print(f"[OK] news_archive.json gespiegelt "
              f"({len(keep_old)} alte + {len(current)} aktuelle Beitraege = {len(new_archive)}).")

    if not changed:
        print("[OK] Keine Aenderungen - bereits synchron.")
        return

    print(f"[OK] Synchronisation abgeschlossen "
          f"(news_current.json: {len(current)}, news_archive.json: {len(new_archive)} Eintraege).")


if __name__ == "__main__":
    main()
