# RLC 1952 Recklinghausen — AI Agent Guidelines & Handhalt-Modus

## 1. OBERSTE DIREKTIVE: HANDHALT-MODUS FÜR LAIEN-NUTZER
- **Dein Nutzer ist ein Laie (Mitglied/Vorstand des Sportvereins RLC 1952 Recklinghausen) OHNE Programmier-, Terminal- oder Git-Kenntnisse.**
- **STRIKTE REGEL:** Stelle dem Nutzer NIEMALS technische Fragen (z. B. nach Build-Befehlen, Git-Befehlen oder Abhängigkeiten).
- **STRIKTE REGEL:** Fordere den Nutzer NIEMALS auf, Befehle im Terminal auszuführen.
- **AUTONOMIE:** Du führst alle Skripte, Tests und Git-Aktionen vollständig selbstständig aus.
- **RÜCKMELDUNG:** Antworte auf Deutsch, in einfacher, verständlicher Sprache, ohne Entwickler-Jargon. Gib am Ende immer den Link zur Vorschau an: `https://rlc-1952-recklinghausen.pages.dev`.

---

## 2. ARCHITEKTUR & STACK (KEIN BUILD-SYSTEM)
- **Tech-Stack:** Plain HTML5, CSS3, Vanilla JavaScript.
- **WICHTIG:** Es gibt KEIN npm, KEIN Vite, KEIN Webpack, KEIN React und KEIN Build-System.
- **Deployment:** Ein `git push origin main` triggert automatisch den Live-Deploy auf Cloudflare Pages (`rlc-1952-recklinghausen.pages.dev`).
- **Lokaler Server:** Falls du lokal testen willst: `python server.py` (erreichbar unter `http://localhost:8001`).

---

## 3. INHALTS-WEGWEISER (CONTENT-MAP)
Egal was der Nutzer dich bittet zu ändern, halte dich an diese Zuordnung:

| Aufgabe / Anfrage des Nutzers | Richtige Datei / Aktion | Wichtige Regel |
| :--- | :--- | :--- |
| **Neuer Blog-/Newsbeitrag** | Redakteure: Pages CMS (`app.pagescms.org`, Rubrik „Aktuelles / News"). KI/Terminal: `python tools/add_news.py --title "..." --text "..." [--image "..."]` | **NIEMALS** `pages/news/*.html` manuell editieren! Der Workflow `.github/workflows/regen-news.yml` regeneriert nach jedem Commit an `news_archive.json` automatisch (inkl. `tools/normalize_news.py`). |
| **Trainingszeiten / Gruppen** | `assets/js/training_schedule.js` & `pages/training.html` | Zeiten & Filter liegen im JS-Objekt. Syntax mit `node --check` prüfen! |
| **Trainerteam (Namen, Fotos)** | `pages/team.html` | Trainer-Kacheln direkt im HTML anpassen. Fotos liegen in `assets/images/trainer/`. |
| **Termine & Wettkämpfe** | `pages/events.html` | Termine direkt in der Kachelliste pflegen. |
| **Verein, Vorstand, Satzung** | `pages/sponsors.html`, `pages/satzung.html`, `assets/pdf/` | PDFs für Downloads immer in `assets/pdf/` ablegen. |
| **Kontakt, Impressum, Datenschutz** | `pages/contact.html`, `pages/impressum.html`, `pages/datenschutz.html` | Texte direkt in der jeweiligen HTML-Datei ändern. |
| **Menü & Fußzeile (Header/Footer)** | `assets/js/components.js` | Wird auf allen 800+ Seiten dynamisch injiziert. Niemals Header in Unterseiten hardcoden! |
| **Farben & Design** | `assets/css/design-tokens.css` & `assets/css/shell.css` | Vereinsblau ist `#0a1f4b`. Keine willkürlichen Farben erfinden. |

---

## 4. DIE 4 TABUS (WAS DU NIEMALS TUN DARFST)
1. 🚫 **Keine neuen Frameworks/NPM:** Installiere niemals npm-Pakete oder Build-Tools für das Frontend.
2. 🚫 **Kein Hand-Edit in `pages/news/*.html`:** Alle News-Detailseiten werden aus `news_archive.json` generiert.
3. 🚫 **Keine Hardcoded-Header:** Ändere Menülinks ausschließlich in `assets/js/components.js`.
4. 🚫 **Keine privaten Daten oder Zips committen:** Lade keine lokalen Audio-Dateien, Screenshots oder ZIPs ins Git-Repo.

---

## 5. STANDARD-WORKFLOW BEI JEDER ÄNDERUNG
Befolge bei JEDEM Auftrag diesen Ablauf:
1. **Änderung umsetzen** (Datei bearbeiten oder `tools/add_news.py` ausführen).
2. **Selbsttest durchführen:**
   - `node --check assets/js/components.js` (falls JS berührt)
   - `node --check assets/js/training_schedule.js` (falls Trainingsplan berührt)
   - `git diff --check`
3. **Veröffentlichen:**
   - `git add <betroffene Dateien>`
   - `git commit -m "inhalt: <kurze Beschreibung auf Deutsch oder Englisch>"`
   - `git push origin main`
4. **Verständliche Rückmeldung an den Nutzer:**
   - Kurz erklären, was geändert wurde.
   - Den Link zur Website nennen: `https://rlc-1952-recklinghausen.pages.dev`.
