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
- **Deployment:** Änderungen werden ausschließlich per geprüftem Pull Request nach `main` übernommen. Der Merge löst den Live-Deploy auf Cloudflare Pages (`rlc-1952-recklinghausen.pages.dev`) aus. Direkte Pushes auf `main` sind verboten.
- **Vorschau:** Cloudflare erstellt bei aktivierten Branch-Deployments eine Vorschau des Arbeitsbranches. Die tatsächliche Vorschau-URL aus dem Deployment/PR verwenden und prüfen; keine URL erfinden. Die Hauptadresse ist kein Nachweis für den Stand eines offenen PR.
- **Lokaler Server:** Falls du lokal testen willst: `python server.py` (erreichbar unter `http://localhost:8001`).

---

## 3. INHALTS-WEGWEISER (CONTENT-MAP)
Egal was der Nutzer dich bittet zu ändern, halte dich an diese Zuordnung:

| Aufgabe / Anfrage des Nutzers | Richtige Datei / Aktion | Wichtige Regel |
| :--- | :--- | :--- |
| **Neuer Blog-/Newsbeitrag** | Redakteure: Pages CMS (`app.pagescms.org`, Rubrik „Aktuelles / News"). KI/Terminal: `python tools/add_news.py --title "..." --text "..." [--image "..."]` | **NIEMALS** `pages/news/*.html` manuell editieren! Der Workflow `.github/workflows/regen-news.yml` regeneriert nach jedem Commit an `news_archive.json` automatisch (inkl. `tools/normalize_news.py`). |
| **Trainingszeiten / Gruppen** | `assets/data/training.json` (CMS „Trainingszeiten & Sportgruppen") & `pages/training.html` | Zeiten liegen als CMS-pflegbares JSON; `assets/js/training_schedule.js` ist nur noch Lader. JSON-Syntax statt node --check prüfen! |
| **Trainerteam (Namen, Fotos)** | `assets/data/team.json` + `assets/data/training.json` (CMS „Trainerteam") | Kacheln werden aus beiden JSONs gerendert; Fotos via CMS in `assets/images/trainer/`. Kein Hand-Edit der Kacheln in `pages/team.html`. |
| **Termine & Wettkämpfe** | `assets/data/events.json` (CMS „Termine & Wettkämpfe") | Kacheln + Startseiten-Termindrawer rendern aus JSON; Poster-PDF via CMS-Medien. Kein Hand-Edit der Kacheln. |
| **Startseite (Texte/Bilder)** | `assets/data/home.json` (CMS „Startseite") | Hero, Karten „Rund um den Verein" und Schnellzugriffe rendern aus JSON. |
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

## 5. VERBINDLICHER WORKFLOW: BRANCH → PULL REQUEST → VORSCHAU → FREIGABE
Diese Regeln gelten für alle Änderungen durch Menschen und KI-Agenten, einschließlich Copilot, Inhaltsänderungen, CMS-Änderungen und Änderungen an dieser Anleitung. Bei widersprüchlichen älteren Anweisungen in `CLAUDE.md`, `.cursorrules` oder Handoffs hat dieser Workflow Vorrang.

1. **Sichere Arbeitsversion erstellen:**
   - Arbeitsstand, Branch und Remote prüfen; fremde oder ungesicherte Arbeit nicht überschreiben.
   - Aktuellen Stand von `origin/main` holen und einen eigenen, passend benannten Branch darauf erstellen. Kein Arbeiten oder Committen direkt auf `main`, kein Force-Push auf `main`.
2. **Änderung umsetzen und lokal testen:**
   - Nur zum Auftrag gehörende Dateien ändern und gezielt stagen; kein pauschales `git add .`.
   - `git diff --check` ausführen.
   - Geänderte JavaScript-Dateien mit `node --check <Datei>` prüfen, einschließlich Inline-Skripten nach Extraktion in eine temporäre Datei. Bei gemeinsam genutztem JavaScript zusätzlich `node --check assets/js/components.js` ausführen.
   - Geänderte JSON-Dateien auf gültige JSON-Syntax prüfen; Trainingsdaten sind JSON, kein JavaScript.
   - Bei sichtbaren Änderungen die UI-/UX-Prüfpflicht aus Abschnitt 6 erfüllen.
3. **Pull Request statt Direktveröffentlichung:**
   - Betroffene Dateien committen und ausschließlich den Arbeitsbranch pushen.
   - Einen Pull Request mit Ziel `main` öffnen. Änderung, Tests, offene Punkte und tatsächliche Cloudflare-Vorschau-URL dokumentieren.
   - Cloudflare-Deployment abwarten und die betroffenen Seiten auf der Branch-Vorschau erneut prüfen. Ein erfolgreicher Deploy allein ist kein UI-/UX-Test.
4. **Prüfung und Freigabe vor Merge:**
   - Nur bei erfolgreichen Pflichtprüfungen und ausdrücklicher Merge-Freigabe durch einen zuständigen Menschen zusammenführen. Ein Implementierungsauftrag allein ist keine Merge-Freigabe; Agenten dürfen nicht eigenmächtig mergen.
   - Fehlende Tests, fehlende Vorschau oder fehlgeschlagene Prüfungen als Blocker melden; PR offen lassen und nicht als fertig/freigegeben ausgeben.
   - CMS und Automationen müssen diesen Ablauf unterstützen. Falls sie direkt auf `main` schreiben, nicht als Ausnahme nutzen, sondern anhalten und die nötige Umstellung melden.
5. **Verständlich zurückmelden:**
   - Kurz erklären, was geändert und tatsächlich getestet wurde; PR-Link und geprüfte Branch-Vorschau nennen.
   - Klar zwischen „lokal geprüft“, „Vorschau geprüft“ und „nach Freigabe veröffentlicht“ unterscheiden.
   - Hauptadresse zusätzlich nennen: `https://rlc-1952-recklinghausen.pages.dev`.

## 6. UI-/UX-TESTPFLICHT NACH JEDER SICHTBAREN ÄNDERUNG
**Nach jeder Designänderung ist ein echter Browser-Test verpflichtend.** Das gilt auch für kleine CSS-Korrekturen, HTML-/JavaScript-Änderungen mit sichtbarer Wirkung sowie Texte, Links, Bilder und CMS-Inhalte, die das Layout beeinflussen können. Nach jeder weiteren sichtbaren Korrektur die betroffenen Prüfungen wiederholen. Reine Dokumentationsänderungen ohne Website-Auswirkung benötigen keinen UI-Test.

### Verbindliche Gerätematrix
Alle betroffenen Seiten und Zustände in folgenden Viewports prüfen (Breite × Höhe in CSS-Pixeln):

| Geräteklasse | Viewports |
| :--- | :--- |
| Kleines Smartphone | 320 × 568 |
| Smartphone | 390 × 844 |
| Smartphone quer | 844 × 390 |
| Tablet hochkant | 768 × 1024 |
| Tablet quer | 1024 × 768 |
| Laptop | 1366 × 768 |
| Großer Desktop | 1920 × 1080 |

- Die vollständige Matrix in einem aktuellen Chromium-Browser prüfen. Zusätzlich Smartphone (390 × 844) und Desktop (1366 × 768) in Firefox und WebKit prüfen. Browser-Automatisierung darf außerhalb des Frontend-Stacks genutzt werden; keine neuen Frontend-Pakete oder Build-Tools einführen.
- Dies deckt die Geräteklassen ab, nicht jedes existierende Gerät. Emulation ausdrücklich als solche kennzeichnen; echte iOS-/Android-Gerätetests nur behaupten, wenn sie tatsächlich stattgefunden haben. Fehlende Browser oder Geräteprüfungen transparent als offen ausweisen, nicht stillschweigend überspringen.

### Was jeweils geprüft werden muss
- **Layout:** Kein horizontaler Seitenüberlauf, keine überlappenden oder abgeschnittenen Texte, Links, Icons und Bilder; bündige Spalten, lesbare Zeilenumbrüche, korrekte Bildproportionen. Überlauf nicht durch pauschales `overflow: hidden` verstecken.
- **Bedienung:** Geänderte Links auf korrektes Ziel prüfen; Buttons, Navigation und gegebenenfalls Menüs/Drawer geöffnet und geschlossen testen. Touch-Ziele mindestens 44 × 44 CSS-Pixel, sichtbarer Tastaturfokus und sinnvolle Tab-Reihenfolge. Kein Test darf ohne ausdrückliche Freigabe echte Formulare absenden oder externe Datensätze erzeugen.
- **Lesbarkeit und Barrierearmut:** Ausreichender Kontrast (WCAG AA: 4,5:1 für normalen Text, 3:1 für große Schrift), verständliche Linktexte und Desktopprüfung bei 200 % Zoom ohne Verlust von Inhalt oder Funktion.
- **Regressionen:** Bei gemeinsamem CSS, Design-Tokens oder Header/Footer zusätzlich Startseite, Termine, Training, Team und eine News-Detailseite prüfen. Generierte News-Dateien dabei nicht manuell ändern.
- **Belege:** Browser und Viewports, getestete Seiten/Zustände, Ergebnisse und offene Einschränkungen im PR dokumentieren. Desktop- und Mobil-Screenshots aufnehmen und visuell prüfen; Überlauf und Überlappungen zusätzlich anhand der Elementabmessungen messen. Screenshots nicht ins Repository committen, sondern bei Bedarf als PR-Anhang bereitstellen.

**Abnahme:** Kein Merge bei fehlenden Pflichtprüfungen, Darstellungsfehlern oder ungeprüfter Cloudflare-Vorschau. Screenshots allein, Quelltextprüfung und Syntaxchecks ersetzen keinen interaktiven Browser-Test.

## 7. ANLEITUNG UND TECHNISCHER BRANCH-SCHUTZ
Diese Datei schreibt den Ablauf verbindlich vor, verhindert direkte Pushes aber nicht technisch. GitHub-Branch-Schutz bzw. Rulesets müssen separat eingerichtet werden (Pull Request und menschliches Review erforderlich, Pflichtprüfungen, keine unkontrollierten Ausnahmen). Solange das nicht geschehen ist, niemals behaupten, `main` sei technisch geschützt. Änderungen an Repository-Einstellungen brauchen einen eigenen Auftrag.
