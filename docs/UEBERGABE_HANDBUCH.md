# Technisches Übergabe-Handbuch — RLC 1952 Recklinghausen

**Dokumentation für den technischen Betrieb, Domain-Verwaltung und Deployment-Infrastruktur**  
**Zielgruppe:** Administrator Jörg-Stefan Praßni sowie zukünftige Webmaster und technische Betreuer des Recklinghäuser Leichtathletik Clubs 1952 e.V.  
**Stand:** September 2026  
**Version:** 1.0.0  
**Produktions-Domain:** `https://www.rlc1952.de` (Apex-Weiterleitung von `https://rlc1952.de`)  
**Cloudflare Pages Live-URL:** `https://rlc-1952-recklinghausen.pages.dev`  
**GitHub Repository:** `https://github.com/maexftw/recklinghausen.git` (Hauptbranch: `main`)  

---

## Inhaltsverzeichnis

1. [Systemarchitektur & Zero-Build-Philosophie](#1-systemarchitektur--zero-build-philosophie)
   - 1.1 [Technische Grundpfeiler (HTML5, CSS3, Vanilla JS)](#11-technische-grundpfeiler)
   - 1.2 [Warum bewusst kein npm/Vite/Webpack im Frontend?](#12-warum-bewusst-kein-npmvitewebpack-im-frontend)
   - 1.3 [Verzeichnis- & Dateistruktur im Überblick](#13-verzeichnis---dateistruktur-im-überblick)
   - 1.4 [News-Generierungspipeline & Datenhaltung](#14-news-generierungspipeline--datenhaltung)
   - 1.5 [Shared Shell / Zentrale Komponenten-Injektion (`components.js`)](#15-shared-shell--zentrale-komponenten-injektion-componentsjs)
2. [HostEurope DNS- & Domain-Leitfaden](#2-hosteurope-dns---domain-leitfaden)
   - 2.1 [Ausgangssituation im HostEurope KIS (`kis.hosteurope.de`)](#21-ausgangssituation-im-hosteurope-kis-kishosteuropede)
   - 2.2 [CNAME-Record für `www.rlc1952.de`](#22-cname-record-für-wwwrlc1952de)
   - 2.3 [HTTP-301-Webweiterleitung für die Apex-Domain `rlc1952.de`](#23-http-301-webweiterleitung-für-die-apex-domain-rlc1952de)
   - 2.4 [HÖCHSTE PRIORITÄT: Absoluter Schutz der MX-Records & E-Mail-Infrastruktur](#24-höchste-priorität-absoluter-schutz-der-mx-records--e-mail-infrastruktur)
   - 2.5 [Alternative Voll-Delegation an Cloudflare (Risiken & Bedingungen)](#25-alternative-voll-delegation-an-cloudflare-risiken--bedingungen)
   - 2.6 [DNS-Prüfung & Verifikationsbefehle (Terminal/PowerShell)](#26-dns-prüfung--verifikationsbefehle)
3. [Cloudflare Pages Konfiguration](#3-cloudflare-pages-konfiguration)
   - 3.1 [Projektübersicht im Cloudflare Dashboard](#31-projektübersicht-im-cloudflare-dashboard)
   - 3.2 [Die Konfigurationsdatei `wrangler.toml`](#32-die-konfigurationsdatei-wranglertoml)
   - 3.3 [Build- & Deployment-Einstellungen (Zero-Build)](#33-build---deployment-einstellungen-zero-build)
   - 3.4 [Umgebungsvariablen (Environment Variables & Secrets)](#34-umgebungsvariablen-environment-variables--secrets)
   - 3.5 [Custom Domain & Automatisches SSL/TLS-Zertifikat](#35-custom-domain--automatisches-ssltls-zertifikat)
   - 3.6 [Cloudflare Serverless Functions (`/functions/api/`)](#36-cloudflare-serverless-functions-functionsapi)
4. [Deployment- & GitHub-Workflow](#4-deployment---github-workflow)
   - 4.1 [Automatisches Deployment per `git push origin main`](#41-automatisches-deployment-per-git-push-origin-main)
   - 4.2 [Branching-Strategie & Preview-Deployments](#42-branching-strategie--preview-deployments)
   - 4.3 [1-Klick-Rollback im Notfall](#43-1-klick-rollback-im-notfall)
   - 4.4 [Lokale Entwicklung & Vorschau (`python server.py`)](#44-lokale-entwicklung--vorschau-python-serverpy)
5. [Wartung, Pflege & Best Practices](#5-wartung-pflege--best-practices)
   - 5.1 [Menü- und Navigationsanpassungen (`assets/js/components.js`)](#51-menü--und-navigationsanpassungen-assetsjscomponentsjs)
   - 5.2 [Trainingszeiten und Gruppen (`assets/js/training_schedule.js`)](#52-trainingszeiten-und-gruppen-assetsjstraining_schedulejs)
   - 5.3 [Trainerteam, Termine & Vereinsdokumente](#53-trainerteam-termine--vereinsdokumente)
   - 5.4 [Kontaktformular, Turnstile & Webhook-Zustellung](#54-kontaktformular-turnstile--webhook-zustellung)
   - 5.5 [Content-Management-Optionen im Vergleich (KI-Handhalt vs. PagesCMS vs. TinaCMS)](#55-content-management-optionen-im-vergleich-ki-handhalt-vs-pagescms-vs-tinacms)
6. [Notfall-Runbook & Fehlerbehebung (Troubleshooting)](#6-notfall-runbook--fehlerbehebung-troubleshooting)
   - 6.1 [Kontaktformular meldet Fehler 503 (`mail_delivery_not_configured`)](#61-kontaktformular-meldet-fehler-503-mail_delivery_not_configured)
   - 6.2 [DNS löst nicht auf oder zeigt falsche Inhalte](#62-dns-löst-nicht-auf-oder-zeigt-falsche-inhalte)
   - 6.3 [E-Mails an `@rlc1952.de` kommen nicht an](#63-e-mails-an-rlc1952de-kommen-nicht-an)
   - 6.4 [Build- oder Sync-Fehler auf Cloudflare Pages](#64-build--oder-sync-fehler-auf-cloudflare-pages)
   - 6.5 [Notfall-Kontakte & Checkliste](#65-notfall-kontakte--checkliste)

---

## 1. Systemarchitektur & Zero-Build-Philosophie

### 1.1 Technische Grundpfeiler
Die Website des RLC 1952 Recklinghausen basiert auf einer **robusten, wartungsarmen Zero-Build-Architektur**:
- **HTML5:** Semantisches, standardkonformes Markup für Startseite, 12 Hauptseiten und über 860 statische News-Detailseiten.
- **CSS3 / Tailwind:** Auslieferung des Tailwind-CSS-Frameworks über das performante Tailwind Play CDN (`cdn.tailwindcss.com`) kombiniert mit maßgeschneiderten Vereins-Stylesheets (`assets/css/design-tokens.css`, `assets/css/shell.css`).
- **Vanilla JavaScript:** Leichtgewichtiges JavaScript ohne clientseitiges Framework (weder React noch Vue noch Angular). Navigation, Modals, dynamische Filter und Kontaktvalidierung laufen rein nativ im Browser.
- **Hosting & Edge:** Weltweite Auslieferung über das Hochgeschwindigkeits-CDN **Cloudflare Pages** mit integrierten Edge-Funktionen (`Cloudflare Pages Functions`) für das Kontaktformular.

### 1.2 Warum bewusst kein npm/Vite/Webpack im Frontend?
Viele moderne Webprojekte scheitern im Vereinsumfeld nach 2 bis 3 Jahren an sogenanntem „Dependency Drift“: Tausende npm-Pakete in `node_modules`, veraltete Build-Tools, inkompatible Node-Versionen und Sicherheitswarnungen (`npm audit`), die ehrenamtliche Administratoren frustrieren und überfordern.

Beim RLC 1952 gilt daher die **goldene Vereins-Regel:**
1. **Keine Node/npm-Abhängigkeiten für die Website-Auslieferung.**
2. **Jede Datei im Repository ist direkt im Browser lauffähig.**
3. **Kein Build-Schritt erforderlich:** Was im Git-Repository liegt, wird 1:1 von Cloudflare Pages in unter 15 Sekunden weltweit synchronisiert und gecacht.
4. **Maximale Haltbarkeit:** Die Website funktioniert heute genauso wie in zehn Jahren, ohne dass jemals `npm update` ausgeführt werden muss.

### 1.3 Verzeichnis- & Dateistruktur im Überblick

```
happy-chandrasekhar/
├── index.html                      # Startseite des RLC 1952
├── wrangler.toml                   # Cloudflare Pages Konfiguration (Zero-Build)
├── _redirects                      # HTTP-Weiterleitungsregeln (z.B. alte PHP-URLs)
├── server.py                       # Lokaler Entwicklungs-Webserver (Python 3)
├── news_archive.json               # Master-Archiv aller News-Beiträge (~950 KB, 866+ Einträge)
│
├── assets/                         # Statische Ressourcen
│   ├── css/
│   │   ├── design-tokens.css       # RLC-Farben, Typografie, Radien & Variablen
│   │   └── shell.css               # Stile für Header, Footer und Navigation
│   ├── js/
│   │   ├── components.js           # Gemeinsamer Header & Footer (Shared Shell)
│   │   ├── news_data.js            # Kompaktes JSON/JS-Array der neuesten 36 Artikel
│   │   ├── cms_content.js         # Lader für CMS-Daten assets/data/*.json
│   │   └── training_schedule.js   # Lader für assets/data/training.json
│   ├── images/                     # Vereinsfotos, Trainerporträts, Icons
│   └── pdf/                        # Satzung, Schutzkonzept, Aufnahmeantrag, Zeiten
│
├── pages/                          # Hauptunterseiten der Website
│   ├── news.html                   # Aktuelles-Übersicht mit Pagination/Filter
│   ├── training.html               # Trainingszeiten, Sportgruppen, Hallen/Plätze
│   ├── team.html                   # Trainerteam & Übungsleiter
│   ├── events.html                 # Termine, Wettkämpfe, Meisterschaften
│   ├── sponsors.html               # Verein, Vorstand, Partner & Satzungs-Download
│   ├── facilities.html             # Sportstätten (Campus Blumenthal, Hohenhorster Heide)
│   ├── gallery.html                # Redaktionelle Bildergalerie
│   ├── contact.html                # Kontaktformular mit Turnstile-Spamschutz
│   ├── impressum.html              # Gesetzliches Impressum
│   ├── datenschutz.html            # Datenschutzerklärung (DSGVO-konform, kein Tracking)
│   ├── schutzkonzept.html          # Kinderschutzkonzept & Ansprechpartner
│   ├── links.html                  # Verbandslinks (FLVW, DLV, Leichtathletik.de)
│   └── news/                       # 866+ statisch generierte Detailseiten
│       ├── 10001.html
│       ├── ...
│       └── 10243.html
│
├── functions/                      # Cloudflare Pages Serverless Edge Functions
│   └── api/
│       ├── contact.js              # POST-Handler: Honeypot, Turnstile & Mail-Webhook
│       └── contact-config.js       # GET-Handler: Liefert öffentlichen Turnstile-Key
│
├── tools/                          # Python-Hilfswerkzeuge für Administratoren & Redaktion
│   └── add_news.py                 # News-Generator (aktualisiert JSON, baut Detailseite & JS)
│
├── generate_detail_pages.py        # Erzeugt aus news_archive.json alle pages/news/*.html
├── update_js_data.py               # Generiert aus news_archive.json die assets/js/news_data.js
└── docs/                           # Projektdokumentation
    ├── UEBERGABE_HANDBUCH.md       # Dieses Handbuch (für Admin Jörg-Stefan Praßni)
    └── REDAKTIONSLEITFADEN.md      # Leitfaden für Barbara Ziesmer-Praßni & Redaktion
```

### 1.4 News-Generierungspipeline & Datenhaltung
Das Vereinsarchiv umfasst über 860 historische Berichte seit den 2000er-Jahren. Die Datenhaltung ist einfach und transparent:
1. **Master-Datenbank:** `news_archive.json` speichert alle Artikel als strukturiertes JSON-Array (ID, Titel, Datum, HTML-Inhalt, Plaintext, Bildpfade).
2. **Detailseiten-Generator:** `generate_detail_pages.py` liest das JSON und schreibt für jeden Beitrag eine vollständig statische HTML-Datei nach `pages/news/<id>.html`. Dadurch sind alle Artikel von Suchmaschinen perfekt indexierbar und laden ohne jede Datenbankabfrage in Millisekunden.
3. **JS-Index-Generator:** `update_js_data.py` extrahiert die neuesten 36 Beiträge nach `assets/js/news_data.js`. Diese Datei wird von `index.html` und `pages/news.html` geladen, um Kacheln und Teaser anzuzeigen.
4. **Kompaktes Admin-Tool:** Das Skript `tools/add_news.py` bündelt alle drei Schritte in einem einzigen Befehl:
   ```bash
   python tools/add_news.py --title "Titel" --text "Inhalt..." --image "bild.jpg"
   ```
   Es vergibt automatisch die nächste ID, legt das Bild in `news_assets/<id>/` ab, schreibt den Eintrag in `news_archive.json`, erzeugt die Detailseite und aktualisiert `news_data.js`.

### 1.5 Shared Shell / Zentrale Komponenten-Injektion (`components.js`)
Damit Navigation und Fußzeile nicht auf 870 verschiedenen HTML-Seiten manuell gepflegt werden müssen, existiert die Datei `assets/js/components.js`:
- Beim Ereignis `DOMContentLoaded` injiziert das Skript den kompletten Header (mit Vereinslogo, Desktop-Menü, Mobile-Drawer und „Mitmachen“-CTA) sowie den Footer (mit Vereinsdaten, Instagram-Link, Dokumenten-Links und rechtlichen Angaben).
- **Pfad-Intelligenz (`getSharedBasePath()`):** Das Skript erkennt automatisch, auf welcher Verzeichnisebene sich der Besucher befindet. Auf der Startseite (`/index.html`) lauten Links `pages/news.html`, auf einer Unterseite (`/pages/news.html`) lauten sie `news.html` bzw. `../index.html`, und in einer News-Detailseite (`/pages/news/10243.html`) automatisch `../../index.html`.
- **Aktiver Menüzustand:** Der aktuelle Menüpunkt wird anhand des Pfads automatisch hervorgehoben (`highlightActiveNavigation()`).
- **Änderungen:** Soll ein neuer Menüpunkt hinzukommen oder die Telefonnummer im Footer geändert werden, geschieht dies **an einer einzigen Stelle** in `assets/js/components.js` und ist sofort seitenweit aktiv.

---

## 2. HostEurope DNS- & Domain-Leitfaden

Die Domain `rlc1952.de` ist bei **HostEurope** registriert. Ebenso läuft die gesamte E-Mail-Kommunikation des Vereins (`info@rlc1952.de`, Vorstandsadressen) über die Mailserver von HostEurope.

### 2.1 Ausgangssituation im HostEurope KIS (`kis.hosteurope.de`)
- **Login-Portal:** [https://kis.hosteurope.de](https://kis.hosteurope.de)
- **Klickpfad im KIS:**  
  `Administration` ➔ `Domainservices` ➔ `Domain-Administration` ➔ Domain **`rlc1952.de`** auswählen ➔ `DNS-Administration` / `Nameserver- & DNS-Einstellungen editieren`.

---

### 2.2 CNAME-Record für `www.rlc1952.de`
Die Subdomain `www.rlc1952.de` soll auf die neue Cloudflare Pages Infrastruktur zeigen.

**Schritt-für-Schritt im HostEurope KIS:**
1. Navigieren Sie zu `DNS-Administration` für `rlc1952.de`.
2. Suchen Sie in der Tabelle den bestehenden Hostnamen **`www`**.
3. Falls für `www` aktuell ein `A-Record` (IPv4-Adresse) existiert: Ändern Sie den Typ auf **`CNAME`** (oder löschen Sie den alten A-Record für `www` und legen Sie einen neuen CNAME-Record an).
4. Tragen Sie als Zieladresse (Target) exakt Folgendes ein:
   ```text
   rlc-1952-recklinghausen.pages.dev.
   ```
   *(Wichtig: Beachten Sie den Punkt am Ende `pages.dev.`, sofern das HostEurope KIS vollqualifizierte Domain-Namen [FQDN] mit abschließendem Punkt verlangt. Bei den meisten KIS-Versionen genügt `rlc-1952-recklinghausen.pages.dev`).*
5. Setzen Sie die **TTL** (Time To Live) auf den Standardwert (z.B. `3600` oder `Standard`).
6. Klicken Sie auf **Speichern** / **Änderungen übernehmen**.

---

### 2.3 HTTP-301-Webweiterleitung für die Apex-Domain `rlc1952.de`
Die sogenannte **Apex-Domain** (auch Root-Domain genannt: `rlc1952.de` ohne führendes `www`) kann bei traditionellen DNS-Anbietern wie HostEurope **nicht** per CNAME weitergeleitet werden, da der DNS-Standard (RFC 1034/1035) verbietet, dass auf der Zonenspitze ein CNAME koexistiert mit SOA-, NS- und vor allem **MX-Records**.

**Empfohlene, 100% ausfallsichere Lösung im HostEurope KIS:**
1. Navigieren Sie im HostEurope KIS zu:  
   `Administration` ➔ `Domainservices` ➔ `Domain-Administration` ➔ `rlc1952.de` ➔ **`Web-Weiterleitung`** (oder `Domainspezifische Weiterleitung`).
2. Richten Sie für die Domain `rlc1952.de` (Apex / ohne www) eine permanente Weiterleitung ein:
   - **Art der Weiterleitung:** `HTTP 301 (Permanent Redirect)`
   - **Ziel-URL:** `https://www.rlc1952.de`
3. Speichern Sie die Einstellung.

**Vorteile dieser Lösung:**
- Jeder Besucher, der im Browser `rlc1952.de` tippt, wird sofort sauber und verschlüsselt auf `https://www.rlc1952.de` geleitet.
- Die Suchmaschinen (Google) erkennen den HTTP-Status 301 und bündeln die gesamte SEO-Relevanz auf `www.rlc1952.de`.
- **Die DNS-Zonenspitze bleibt bei HostEurope unberührt – E-Mails laufen ungestört weiter!**

---

### 2.4 HÖCHSTE PRIORITÄT: Absoluter Schutz der MX-Records & E-Mail-Infrastruktur

> ⚠️ **WARNUNG: GEFAHR VON E-MAIL-AUSFÄLLEN!**  
> Beim RLC 1952 hängen die gesamte offizielle Vereinskommunikation, Mitgliedsanfragen, Wettkampfanmeldungen und Vorstandsangelegenheiten an E-Mail-Adressen mit der Endung `@rlc1952.de` (z.B. `info@rlc1952.de`, `geschaeftsfuehrung@rlc1952.de`).  
> **Jede Fehlkonfiguration der MX-Einträge führt dazu, dass Absender weltweit die Fehlermeldung „550 User unknown“ oder „Mailbox unavailable“ erhalten und Mails verloren gehen!**

#### Was Sie NIEMALS tun dürfen:
- ❌ Ändern Sie **nicht** die Nameserver auf HostEurope, solange Sie die E-Mails über HostEurope betreiben.
- ❌ Löschen oder überschreiben Sie **niemals** Einträge vom Typ `MX`.
- ❌ Legen Sie **keinen Wildcard-CNAME (`*`)** an, der mit bestehenden Mail-Subdomains kollidiert.
- ❌ Verändern Sie **keine TXT-Records**, die für `v=spf1 ...` (Sender Policy Framework) oder DKIM hinterlegt sind.

#### Übersicht der unantastbaren HostEurope Mail-Records:
Die folgenden DNS-Einträge müssen im HostEurope KIS zwingend unverändert erhalten bleiben:

| Hostname / Subdomain | Typ | Priorität | Wert / Zielserver | Zweck |
| :--- | :--- | :--- | :--- | :--- |
| `@` (oder `rlc1952.de.`) | **MX** | 10 | `mx0.hosteurope.de.` | Primärer Mail-Exchange-Server des Vereins |
| `@` (oder `rlc1952.de.`) | **MX** | 20 | `mx1.hosteurope.de.` | Sekundärer Backup-Mail-Exchange-Server |
| `@` (oder `rlc1952.de.`) | **TXT** | - | `v=spf1 include:_spf.hosteurope.de ~all` | Spam-Schutz & E-Mail-Zustellbarkeit (SPF) |
| `mail` / `smtp` / `imap` | **A / CNAME** | - | *(HostEurope Mail-IP oder Servername)* | Zugriff der Vorstandsmitglieder auf Outlook/Webmail |
| `autodiscover` / `autoconfig` | **CNAME / SRV** | - | *(HostEurope Autokonfiguration)* | Automatische Einrichtung von Mail-Clients |

---

### 2.5 Alternative Voll-Delegation an Cloudflare (Risiken & Bedingungen)
Theoretisch bietet Cloudflare die Möglichkeit, die Nameserver der Domain `rlc1952.de` bei HostEurope vollständig auf Cloudflare-Nameserver umzustellen (z.B. `alina.ns.cloudflare.com` und `dave.ns.cloudflare.com`). Dies ermöglicht Features wie automatisches CNAME-Flattening an der Apex-Domain.

**Wir raten dem Verein aktuell davon ab, AUSSER folgende Vorbedingungen werden strikt erfüllt:**
1. **Vollständiger DNS-Export:** Vor der Umstellung müssen alle vorhandenen HostEurope-DNS-Einträge (insbesondere MX-, TXT-, SPF-, Autodiscover- und Subdomain-Records) 1:1 im Cloudflare DNS-Dashboard manuell angelegt werden.
2. **Mail-Proxy deaktivieren:** Im Cloudflare DNS dürfen MX-Records und Mail-Hostnamen (`mail.rlc1952.de`, `smtp.rlc1952.de`) **NIEMALS** durch die Cloudflare-Orange-Cloud („Proxied“) geschleift werden, sondern müssen auf „DNS only“ (graue Wolke) stehen. Cloudflare leitet auf Port 25/587 keinen Mailverkehr ohne Enterprise-Zusatzpaket weiter.
3. **Fazit:** Die in Kapitel 2.2 und 2.3 beschriebene Lösung (CNAME für `www` + Webweiterleitung im KIS für Apex) ist **weitaus sicherer, erfordert keine Migration der Postfächer und schließt ein Ausfallrisiko für den E-Mail-Verkehr zu 100% aus.**

---

### 2.6 DNS-Prüfung & Verifikationsbefehle
Nachdem die Änderungen im HostEurope KIS gespeichert wurden, kann es zwischen 15 Minuten und 24 Stunden (DNS-Propagation) dauern, bis die neuen Einträge weltweit sichtbar sind.

Sie können den Status jederzeit in der Windows PowerShell oder Linux-Konsole überprüfen:

```powershell
# 1. CNAME für www.rlc1952.de prüfen
Resolve-DnsName -Name www.rlc1952.de -Type CNAME

# Erwartete Ausgabe:
# Name                           Type   NameHost
# ----                           ----   --------
# www.rlc1952.de                 CNAME  rlc-1952-recklinghausen.pages.dev

# 2. MX-Records prüfen (MÜSSEN auf HostEurope zeigen!)
Resolve-DnsName -Name rlc1952.de -Type MX

# Erwartete Ausgabe:
# Name                           Type   Exchange              Preference
# ----                           ----   --------              ----------
# rlc1952.de                     MX     mx0.hosteurope.de     10
# rlc1952.de                     MX     mx1.hosteurope.de     20

# 3. HTTP-Weiterleitung der Apex-Domain prüfen
curl -I https://rlc1952.de

# Erwartete Ausgabe:
# HTTP/1.1 301 Moved Permanently
# Location: https://www.rlc1952.de/
```

---

## 3. Cloudflare Pages Konfiguration

Cloudflare Pages stellt das globale Edge-Netzwerk bereit, liefert die HTML-, CSS- und JS-Dateien verschlüsselt aus und führt serverseitige JavaScript-Funktionen für das Kontaktformular aus.

### 3.1 Projektübersicht im Cloudflare Dashboard
- **Dashboard-URL:** [https://dash.cloudflare.com](https://dash.cloudflare.com)
- **Navigationspfad:** `Compute (Workers & Pages)` ➔ `Pages` ➔ Projekt: **`rlc-1952-recklinghausen`**
- **Direkte Pages-URL:** `https://rlc-1952-recklinghausen.pages.dev`

---

### 3.2 Die Konfigurationsdatei `wrangler.toml`
Im Wurzelverzeichnis des Repositories liegt die Konfigurationsdatei `wrangler.toml`:

```toml
name = "rlc-1952-recklinghausen"
pages_build_output_dir = "."
compatibility_date = "2024-01-01"
```

**Bedeutung der Einstellungen:**
- `name`: Eindeutiger Projektbezeichner in Cloudflare.
- `pages_build_output_dir = "."`: Weist Cloudflare an, das Wurzelverzeichnis direkt als Auslieferungsverzeichnis zu nutzen (Zero-Build-Architektur). Es existiert kein `dist/` oder `build/`-Ordner.
- `compatibility_date = "2024-01-01"`: Definiert das Laufzeitverhalten der Serverless Functions in `functions/`.

---

### 3.3 Build- & Deployment-Einstellungen (Zero-Build)
Falls Sie das Projekt im Cloudflare Dashboard inspizieren oder neu anlegen müssen, verwenden Sie exakt diese Werte:

| Einstellungs-Feld | Wert | Erklärung |
| :--- | :--- | :--- |
| **Framework preset** | `None` | Kein Framework (kein Astro, kein Next.js, kein React) |
| **Build command** | *(leer lassen)* | **Wichtig:** Kein Befehl! Keine npm-Installation ausführen |
| **Build output directory** | `.` | Wurzelverzeichnis des Repositories ausliefern |
| **Root directory** | `/` | Hauptverzeichnis |
| **Production branch** | `main` | Jeder Push auf diesen Branch deployt live |

---

### 3.4 Umgebungsvariablen (Environment Variables & Secrets)
Für das Kontaktformular und den Spamschutz benötigt Cloudflare Pages Umgebungsvariablen.

**Klickpfad im Cloudflare Dashboard:**  
`Projekt rlc-1952-recklinghausen` ➔ `Settings` ➔ `Environment variables` ➔ Reiter `Production` (und ggf. `Preview`).

Hier müssen folgende Variablen konfiguriert werden:

| Variablenname | Typ | Wert / Beschreibung | Woher stammt der Wert? |
| :--- | :--- | :--- | :--- |
| `TURNSTILE_SITE_KEY` | Plaintext | Öffentlicher Sitekey für das Cloudflare Turnstile Widget (z.B. `0x4AAAAAA...`). | Cloudflare Dashboard ➔ Turnstile ➔ Sitekey des RLC-Widgets. |
| `TURNSTILE_SECRET_KEY` | **Secret** (verschlüsselt) | Privater Geheimschlüssel für die Server-Validierung des Turnstile-Tokens. | Cloudflare Dashboard ➔ Turnstile ➔ Secret Key des RLC-Widgets. |
| `CONTACT_WEBHOOK_URL` | **Secret** (verschlüsselt) | HTTP-POST-Endpunkt zur Weiterleitung empfangener Kontaktformulardaten. | URL Ihres Webhook-Empfängers (z.B. Make.com, Zapier, Cloudflare Worker Mail Relay). |
| `CONTACT_WEBHOOK_TOKEN` | **Secret** (optional) | Optionaler Bearer-Token, der im `Authorization: Bearer <TOKEN>` Header mitgesendet wird. | Frei gewähltes Token zur Absicherung des Webhooks. |

---

### 3.5 Custom Domain & Automatisches SSL/TLS-Zertifikat
Sobald der CNAME-Eintrag im HostEurope KIS eingerichtet ist (Kapitel 2.2), wird die Domain mit Cloudflare Pages verknüpft:

1. Navigieren Sie im Cloudflare Dashboard zu:  
   `Pages` ➔ `rlc-1952-recklinghausen` ➔ Reiter **`Custom domains`**.
2. Klicken Sie auf **`Set up a custom domain`**.
3. Geben Sie die Domain ein: **`www.rlc1952.de`**.
4. Cloudflare prüft nun automatisch die DNS-Verbindung zur Adresse `rlc-1952-recklinghausen.pages.dev`.
5. Sobald der CNAME erkannt wird, wechselt der Status auf **`Active`**.
6. **SSL/TLS-Zertifikat:** Cloudflare generiert vollautomatisch ein kostenloses SSL/TLS-Zertifikat (via Let's Encrypt / DigiCert). Es ist keine manuelle Verlängerung oder Zertifikats-Installation notwendig; Cloudflare erneuert das Zertifikat alle 90 Tage automatisch.
7. **Empfohlene SSL-Optionen:** Unter `SSL/TLS` ➔ `Edge Certificates` sicherstellen, dass **`Always Use HTTPS`** und **`Automatic HTTPS Rewrites`** aktiviert sind.

---

### 3.6 Cloudflare Serverless Functions (`/functions/api/`)
Im Verzeichnis `functions/` liegen zwei serverseitige JavaScript-Dateien, die von Cloudflare Pages automatisch als API-Endpunkte bereitgestellt werden:

1. **`functions/api/contact-config.js` (GET):**
   - Wird von `pages/contact.html` im Browser per AJAX aufgerufen.
   - Gibt den öffentlichen `turnstileSiteKey` aus den Umgebungsvariablen zurück, damit das Captcha-Widget dynamisch geladen werden kann.
2. **`functions/api/contact.js` (POST):**
   - **Honeypot-Prüfung:** Prüft das verdeckte Feld `website`. Füllen Spambots dieses Feld aus, wird die Nachricht lautlos verworfen (HTTP 200).
   - **Validierung:** Prüft Vorname, Nachname, E-Mail-Format und Nachrichtenlänge.
   - **Turnstile-Verifikation:** Sendet das Captcha-Token serverseitig an `https://challenges.cloudflare.com/turnstile/v0/siteverify`. Ist der Token ungültig, wird mit HTTP 422 abgebrochen.
   - **Mail-Weiterleitung:** Sendet ein bereinigtes JSON-Objekt an `CONTACT_WEBHOOK_URL`. Ist diese URL nicht konfiguriert, meldet die API HTTP 503 (`mail_delivery_not_configured`).

---

## 4. Deployment- & GitHub-Workflow

### 4.1 Automatisches Deployment per `git push origin main`
Das Git-Repository auf GitHub (`https://github.com/maexftw/recklinghausen.git`) ist direkt mit Cloudflare Pages verknüpft.

**Der Standard-Deployment-Ablauf:**
1. Sie führen eine Änderung an einer HTML-Seite, einem Stylesheet oder einem Skript durch.
2. Sie führen einen lokalen Selbsttest durch:
   ```bash
   node --check assets/js/components.js
   git diff --check
   ```
3. Sie committen und pushen die Änderung:
   ```bash
   git add .
   git commit -m "inhalt: Trainingszeiten Sommer 2026 aktualisiert"
   git push origin main
   ```
4. **Was geschieht nun?**
   - GitHub sendet einen Webhook an Cloudflare Pages.
   - Cloudflare Pages holt die geänderten Dateien ab.
   - Da kein Build-Befehl existiert, dauert der gesamte Vorgang **nur 10 bis 20 Sekunden**.
   - Die Änderung ist sofort weltweit auf `https://www.rlc1952.de` und `https://rlc-1952-recklinghausen.pages.dev` online.

---

### 4.2 Branching-Strategie & Preview-Deployments
Möchten Sie größere Umstrukturierungen (z.B. neues Design, neues Anmeldeformular) testen, ohne die Live-Website zu gefährden, nutzen Sie **Preview-Branches**:

1. Erstellen Sie einen neuen Branch:
   ```bash
   git checkout -b feature/neues-design
   ```
2. Nehmen Sie Ihre Änderungen vor, committen Sie und pushen Sie den Branch:
   ```bash
   git push origin feature/neues-design
   ```
3. **Automatische Preview-URL:** Cloudflare Pages erkennt den neuen Branch und erzeugt automatisch eine isolierte Vorschau-URL nach folgendem Muster:
   ```text
   https://feature-neues-design.rlc-1952-recklinghausen.pages.dev
   ```
4. Der Vorstand und die Redaktion können die Änderungen auf dieser URL auf Smartphones und PCs begutachten und freigeben.
5. Nach der Freigabe wird der Branch in `main` gemergt und live geschaltet:
   ```bash
   git checkout main
   git merge feature/neues-design
   git push origin main
   ```

---

### 4.3 1-Klick-Rollback im Notfall
Sollte versehentlich ein fehlerhafter Stand auf `main` gepusht werden, der die Website beschädigt, bietet Cloudflare Pages eine **sofortige 1-Klick-Rollback-Funktion**, die unabhängig von Git innerhalb von 5 Sekunden funktioniert:

1. Öffnen Sie das Cloudflare Dashboard: `Compute (Workers & Pages)` ➔ `Pages` ➔ `rlc-1952-recklinghausen`.
2. Klicken Sie auf den Reiter **`Deployments`**.
3. In der Liste sehen Sie alle bisherigen Deployments mit Datum, Commit-Hash und Commit-Nachricht.
4. Suchen Sie das letzte funktionierende Deployment heraus.
5. Klicken Sie ganz rechts auf die **drei Punkte (`...`)** neben dem Deployment.
6. Wählen Sie **`Rollback to this deployment`** und bestätigen Sie.
7. Die Live-Domain wird **sofort** wieder auf den ausgewählten stabilen Stand geschaltet. Sie können den Fehler anschließend in Ruhe lokal analysieren.

---

### 4.4 Lokale Entwicklung & Vorschau (`python server.py`)
Um die Website auf dem eigenen PC anzusehen, wird **kein Apache, kein Nginx und kein Node.js** benötigt. Im Repository liegt das Skript `server.py`:

```bash
# Lokalen Server starten (benötigt lediglich installiertes Python 3)
python server.py
```

- Der Server startet auf Port **8001**:  
  Öffnen Sie im Browser: `http://localhost:8001`
- Alle relativen Pfade, Bilder und JavaScript-Module verhalten sich exakt wie auf dem Cloudflare-Live-Server.
- Beenden des Servers: `Strg + C` im Terminal.

---

## 5. Wartung, Pflege & Best Practices

### 5.1 Menü- und Navigationsanpassungen (`assets/js/components.js`)
Alle Navigationslinks des Kopfmenüs und des Footers werden zentral gesteuert.

**Beispiel: Neuen Menüpunkt hinzufügen:**
1. Öffnen Sie `assets/js/components.js`.
2. Suchen Sie nach `aria-label="Hauptnavigation"` (~Zeile 79).
3. Fügen Sie den neuen Link in der Desktop-Navigation ein:
   ```html
   <a class="site-nav-link text-sm font-semibold transition-colors" href="${basePath}pages/neue-seite.html">Neue Rubrik</a>
   ```
4. Fügen Sie denselben Link im Mobile-Menü (`site-mobile-panel`) ein:
   ```html
   <a class="site-mobile-link block px-3 py-4 text-base font-semibold" href="${basePath}pages/neue-seite.html">Neue Rubrik</a>
   ```
5. Speichern und mit `node --check assets/js/components.js` auf Syntaxfehler prüfen.

---

### 5.2 Trainingszeiten und Gruppen (`assets/js/training_schedule.js`)
Die Trainingszeiten werden interaktiv auf `pages/training.html` dargestellt. Die Datenbasis liegt in `assets/data/training.json` (im Pages CMS unter „Trainingszeiten & Sportgruppen" pflegbar); `assets/js/training_schedule.js` ist nur noch der Lader:
- Jede Trainingsgruppe ist ein strukturiertes Objekt mit:
  - `group`: Name der Gruppe (z.B. `U10 (Kinder 8-9 Jahre)`)
  - `days`: Wochentage & Uhrzeiten
  - `coach`: Verantwortlicher Trainer / Ansprechpartner
  - `location`: Sportstätte (z.B. `Campus Blumenthal`, `Hohenhorst`)
  - `category`: Filter-Kategorie (`nachwuchs`, `jugend`, `erwachsene`, `wettkampf`)
- Änderungen von Hallen- auf Sommerzeiten werden im Pages CMS (Rubrik „Trainingszeiten & Sportgruppen") oder direkt in `assets/data/training.json` gepflegt. Danach die JSON-Syntax prüfen.

---

### 5.3 Trainerteam, Termine & Vereinsdokumente
- **Trainerteam (`pages/team.html`):** Trainer-Kacheln mit Foto, Name, Lizenzstufe und Kontakt. Fotos neuer Trainer werden vorab auf max. 800×800 Pixel zugeschnitten und unter `assets/images/trainer/vorname_nachname.jpg` abgelegt.
- **Terminkalender (`pages/events.html`):** Wettkampf- und Vereinstermine werden chronologisch in der Kachelliste gepflegt.
- **Vereinsdokumente (`assets/pdf/`):** Satzung, Kinderschutzkonzept, Beitragsordnung oder Anmeldeformulare werden stets als PDF in `assets/pdf/` hinterlegt und in `pages/sponsors.html` bzw. im Footer verlinkt.

---

### 5.4 Kontaktformular, Turnstile & Webhook-Zustellung
Damit Anfragen von `pages/contact.html` an den Verein zugestellt werden, muss in Cloudflare Pages die Umgebungsvariable `CONTACT_WEBHOOK_URL` gesetzt sein:
- **Empfohlene Mail-Relay-Optionen:**
  1. **Make.com / Zapier (Kostenlos bis 1.000 Mails/Monat):** Ein einfacher Webhook-Trigger empfängt das JSON vom Kontaktformular und sendet über das SMTP-Konto von HostEurope (`info@rlc1952.de`) eine formatierte E-Mail an den Vorstand.
  2. **Cloudflare Worker Email Routing:** Ein kleiner, kostenloser Cloudflare Worker mit SendEmail-Binding, der eingehende Webhooks direkt an `info@rlc1952.de` verschickt.
- **Sicherheits-Check:** Das Formular sendet automatisch eine Kopie an den Anfragenden (`submission.cc = submission.email`) und protokolliert den Turnstile-Prüfstatus.

---

### 5.5 Content-Management-Optionen im Vergleich (KI-Handhalt vs. PagesCMS vs. TinaCMS)

Die Pflege von News-Artikeln ist für einen Sportverein entscheidend. Hier stehen drei Wege zur Auswahl:

| Kriterium | Option 1: KI-Handhalt-Modus (`tools/add_news.py`) | Option 2: PagesCMS (`pagescms.org`) | Option 3: TinaCMS (`tinacms.org`) |
| :--- | :--- | :--- | :--- |
| **Architektur** | Rein Python-basiert, Zero-Build | Browserbasiertes Git-CMS, Zero-Build | React-/Node.js-basiertes CMS |
| **Build-Schritt im Repo** | **Keiner** | **Keiner** (nur `.pages.yml`) | **Erfordert Node.js & Build-Schritt** |
| **Bedienung** | Vorstand sendet Text/Bild an KI/Admin | Redakteur loggt sich im Browser ein | Redakteur loggt sich im Browser ein |
| **Wartungsaufwand** | Nahezu 0 | Sehr gering | Hoch (npm-Updates, React-Build) |
| **Vereins-Eignung** | **Hervorragend (Aktueller Standard)** | **Hervorragend (Für Web-Oberfläche)** | **Nicht empfohlen (Verstößt gegen Tabu 1)** |

**Empfehlung für Jörg-Stefan:**
- Behalten Sie den **KI-Handhalt-Modus** als Standard bei. Er ist erprobt, robust und erfordert von der Redaktion keinerlei Einarbeitung.
- Sollte die Redaktion zwingend eine Web-Maske wünschen, richten Sie **PagesCMS** ein. Die Konfigurationsdatei `.pages.yml` liegt im Repo bereit.
- Vermeiden Sie klassisches TinaCMS, da es die Zero-Build-Garantie des Repos aufhebt.

---

## 6. Notfall-Runbook & Fehlerbehebung (Troubleshooting)

### 6.1 Kontaktformular meldet Fehler 503 (`mail_delivery_not_configured`)
- **Ursache:** Die Cloudflare Pages Serverless Function `functions/api/contact.js` findet keine gesetzte Variable `CONTACT_WEBHOOK_URL`.
- **Lösung:**
  1. Öffnen Sie das Cloudflare Dashboard ➔ `Compute (Workers & Pages)` ➔ `rlc-1952-recklinghausen`.
  2. Gehen Sie zu `Settings` ➔ `Environment variables`.
  3. Fügen Sie `CONTACT_WEBHOOK_URL` mit der URL Ihres Mail-Relays (z.B. Make.com Webhook) hinzu.
  4. Lösen Sie ein neues Deployment aus (oder speichern Sie die Variable).

---

### 6.2 DNS löst nicht auf oder zeigt falsche Inhalte
- **Checkliste:**
  1. Ist der CNAME für `www.rlc1952.de` im HostEurope KIS korrekt auf `rlc-1952-recklinghausen.pages.dev.` gesetzt?
  2. Ist im Cloudflare Dashboard unter `Custom domains` die Domain `www.rlc1952.de` auf Status `Active`?
  3. Prüfen Sie mit `Resolve-DnsName -Name www.rlc1952.de -Type CNAME` in PowerShell, ob globale DNS-Server den Eintrag bereits sehen.

---

### 6.3 E-Mails an `@rlc1952.de` kommen nicht an
- **Sofortmaßnahme:**
  1. Führen Sie sofort in der PowerShell aus:
     ```powershell
     Resolve-DnsName -Name rlc1952.de -Type MX
     ```
  2. Wenn die Einträge **nicht** auf `mx0.hosteurope.de` und `mx1.hosteurope.de` zeigen:
     - Loggen Sie sich sofort in das HostEurope KIS ein.
     - Stellen Sie die MX-Records auf die Standardwerte zurück (Priorität 10: `mx0.hosteurope.de.`, Priorität 20: `mx1.hosteurope.de.`).
     - Löschen Sie eventuell fehlerhaft angelegte Wildcard-Records (`*`).

---

### 6.4 Build- oder Sync-Fehler auf Cloudflare Pages
- **Ursache:** In den Projekteinstellungen wurde versehentlich ein Build-Command eingetragen (z.B. `npm run build`), obwohl kein `package.json` existiert.
- **Lösung:**
  - Cloudflare Dashboard ➔ `Pages` ➔ `rlc-1952-recklinghausen` ➔ `Settings` ➔ `Builds & deployments`.
  - Stellen Sie sicher:
    - **Build command:** *(vollständig leer)*
    - **Build output directory:** `.`
    - **Root directory:** `/`

---

### 6.5 Notfall-Kontakte & Checkliste

| Rolle | Name | Kontakt / Zuständigkeit |
| :--- | :--- | :--- |
| **Technischer Administrator** | Jörg-Stefan Praßni | HostEurope KIS, DNS, Vereinsführung |
| **Redaktionsleitung** | Barbara Ziesmer-Praßni | Inhalte, News, Vereinsberichte |
| **Hosting & CDN** | Cloudflare Pages Support | [https://dash.cloudflare.com](https://dash.cloudflare.com) |
| **Domain- & Mail-Provider** | HostEurope Support | [https://kis.hosteurope.de](https://kis.hosteurope.de) / Hotline: 0221 999 99 333 |
| **Quellcode-Repository** | GitHub | `https://github.com/maexftw/recklinghausen.git` |

---
*Dieses Handbuch ist im Git-Repository versioniert unter `docs/UEBERGABE_HANDBUCH.md` und sollte bei wesentlichen Infrastruktur-Änderungen stets aktualisiert werden.*
