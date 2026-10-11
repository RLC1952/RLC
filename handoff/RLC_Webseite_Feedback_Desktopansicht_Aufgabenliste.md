# RLC Webseite – Aufgabenliste aus Feedback Desktopansicht

Quelle: `RLC_Webseite_Feedback_Desktopansicht.docx`
Preview im Dokument: https://85957764.rlc-1952-recklinghausen.pages.dev/
Auswertung: 2026-06-16

## Kurzfazit

Das Dokument ist kein loser Kommentarblock, sondern enthält konkrete Änderungswünsche, Bugmeldungen, Content-Vorgaben und offene Rückfragen zur Desktopansicht. Es sollte in Aufgaben überführt werden. Einige Inhalte müssen direkt eingepflegt werden, andere brauchen Material/Entscheidungen vor der Umsetzung.

Wichtig: Im DOCX gibt es einen Word-Kommentar zu der Startseiten-Kachel „Verein“: **„Hinweis: Die mobile Version zeigt hier einen ganz anderen Inhalt“**. Das ist zusätzlich als Mobile/Desktop-Konsistenzproblem zu behandeln, obwohl das Dokument primär „Desktopansicht“ heißt.


## Umsetzungsstand nach Umsetzungsrunde 2026-06-16

Lokal umgesetzt auf Branch `codex/rlc-customer-go-content-round` und über `http://127.0.0.1:4173/` geprüft.

Verifiziert:

- HTTP 200 für Startseite, Termine, Training, Verein, Trainerteam, Sportstätten, Kontakt, Impressum, Datenschutz, Newsübersicht und eine Newsdetailseite.
- JS-Syntaxchecks für `components.js`, `training_schedule.js`, `news_data.js` erfolgreich.
- `git diff --check` erfolgreich.
- Browser-Smoke: Startseite, Termine, Training-U6-Filter, Verein/Partner, Sportstätten, Kontakt/Rechtliches, Newsdetail, Footer und mobile Startseite.
- Linkcheck-Fund bereinigt: alte importierte News-Links auf nicht vorhandene historische PDFs/Legacy-Ziele (`rlc.php`, alte Ergebnislisten) sind nicht mehr als anklickbare 404-Ziele sichtbar. Die Originalquellen bleiben als Materialfrage offen, falls die alten Ergebnislisten/PDFs später wiederhergestellt werden sollen.

## Muss direkt eingepflegt / umgesetzt werden

### Global / Designsystem

- [x] Titel-/Hero-Bereiche auf Startseite und Unterseiten verkleinern.
  - Boxen wirken zu groß.
  - Überschriften sind zu dominant.
  - Desktop soll mehr Breite nutzen und weniger vertikalen Raum verschwenden.
- [x] Farbschema stärker mit Vereinsfarben + Dunkelblau verbinden.
  - Aktueller Look hat laut Feedback noch zu wenig Vereinsbezug.
- [x] Footer anpassen: Beim Instagram-Icon zusätzlich den klickbaren Text **„Instagram“** anzeigen.

### Startseite

- [x] Hero-/Überschriftenblock weniger dominant gestalten.
- [x] Bereich **„Nächste Termine“** klickbar machen.
  - Klick soll direkt zu Termininformationen führen.
- [x] Button/Link **„Alle Termine im Überblick“** reparieren.
  - Mouseover ist aktuell schlecht/nicht lesbar.
  - Link soll zur vollständigen Terminseite führen, nicht nur ein Pop-up/Flyout öffnen.
- [x] Termine im Seitenfenster klickbar machen.
  - Detailseite/Detailansicht soll Informationen enthalten: Was, Wann, Wo, Wer, Anmeldung.
- [x] Rubrik **„Der Verein auf einen Blick“** von der Startseite entfernen.
  - Begründung: macht die Seite zu unübersichtlich; Inhalte passen besser in „Rund um den Verein“.
- [x] Rubrik **„Rund um den Verein“** neu strukturieren.
  - Reihenfolge analog zur Menüreihenfolge.
  - Weitere Blöcke ergänzen.

#### Vorgaben für „Rund um den Verein“-Kacheln

1. **Termine**
   - Unterzeile: `Veranstaltungen im Überblick`
   - Text: `Wettkämpfe und Veranstaltungen mit weiteren Informationen (Datum, Ort, Anmeldung usw.)`
2. **Training**
   - Unterzeile: `Angebote für Kinder, Jugendliche und Erwachsene.`
   - Text: `Details zu Trainingszeiten, Gruppen und Orten zur Übersicht.`
3. **Verein**
   - Unterzeile: `Vorstand, Geschichte und Partner`
   - Text: `Die Vereinsseite bündelt Vorstand, Historie, Partner, Satzung, Schutzkonzept und Mitgliedsunterlagen. Unser Trainerteam im Überblick.`
   - Zusatzcheck: Mobile Version zeigt laut Word-Kommentar anderen Inhalt → Desktop/Mobile abgleichen.
4. **Trainerteam**
   - Unterzeile: `Unser Trainerteam im Überblick.`
   - Text: `Hier findest du die Trainerinnen und Trainer, die aktuell unsere Gruppen begleiten, mit ihren Einsatzbereichen und Trainingstagen.`
5. **Sportstätten**
   - Unterzeile: `Stadion, Hallen und Kursräume`
   - Text: `Stadion und Hallen für Training, Kurse und Wettkämpfe uvm.`
6. **Einstieg**
   - Unterzeile: `Probetraining und Kontakt`
   - Text: `Nimm Kontakt auf und vereinbare ein erstes Probetraining oder stelle Deine offen Fragen.`
7. **Instagram**
   - Unterzeile: `Aktuelles aus dem Vereinsalltag`
   - Text: `Auf Instagram findest Du von aktuellen Beiträgen aus dem Vereinsalltag bis hin zu Wettkampfbildern /-videos nützliche Einblicke in das Vereinsgeschehen.`

### Aktuelles / News

- [x] Hero-/Headerblock **„Aktuelles“** verkleinern.
  - Es reicht: `Neuigkeiten und Ergebnisse aus dem Verein`
  - Sub-Headline entfernen.
- [x] Druckfunktion aus Beitragsdetailseiten entfernen.
  - Begründung: Webseite ist nicht für Browserdruck optimiert.
- [x] News-Kacheln reparieren, die laut Screenshot „zerschossen“ sind.
- [x] Footer in Meldungsdetailseiten reparieren; aktuell unvollständig/defekt.
- [ ] Alle News-Einträge vor Go-live vollständig von der alten Homepage übernehmen.
  - Stand 2026-06-16: Newsdetailseiten sind vorhanden/importiert; alte fehlende Legacy-Links/PDF-Ziele wurden als anklickbare 404-Ziele entschärft. Die Original-PDFs/Ergebnislisten können später ergänzt werden, wenn Recklinghausen die alten Quellen liefert.

### Termine

- [x] Terminseite allgemeiner benennen.
  - Titel nicht speziell auf **2026** festlegen.
  - Jahr erst bei den Terminen selbst nennen.
- [x] Vergangene Termine automatisch ausblenden oder deutlich schwächer darstellen.
  - Feedbackpräferenz: vergangene Termine können automatisch ausgeblendet werden.
- [x] Termin-Detailinformationen herstellen/verlinken.
  - Was, Wann, Wo, Wer, Anmeldung.

### Training

- [x] Filter reparieren; Beispiel im Dokument: **U6** fehlerhaft.
- [ ] Klären und dokumentieren, wie neue Trainingszeiten bzw. Änderungen eingepflegt werden.
  - Redaktions-/CMS-Prozess oder Datenquelle definieren.

### Verein / Vorstand / Partner

- [x] Vorstandsseite anpassen.
- [x] Vorstandsdaten und Rollen strukturiert einpflegen.
- [x] E-Mail-Adressen hinterlegen, soweit freigegeben.

#### Im Dokument genannte Vorstandsdaten

- 1. Vorstand: Christian Dahmen – `c.dahmen@rlc1952.de`
- 2. Vorstand: Marc Manderla
- 1. Geschäftsführerin: Barbara Zismer-Praßni – `geschaeftsfuehrung@rlc1952.de`
- 2. Geschäftsführer: Sebastian Stephani – `geschaeftsfuehrung@rlc1952.de`
- 1. Kassierer: Stephen Wandelt
- 2. Kassierer: Marc Manderla
- weitere Rollen laut Screenshot/Bestand prüfen

- [ ] Falls Fotos eingefügt werden: je Person eine eigene Kachel vorsehen.
- [x] Partnerseiten mit Links ergänzen:
  - Bodynostic by Lückenotto: https://bodynostic.de/
  - Lauflust: https://www.lauflust-re.de/
  - Sparkasse Vest: https://www.sparkasse-re.de/

### Trainerteam

- [x] Titelbild austauschen; aktuelles Bild passt laut Feedback nicht zur Kategorie.
- [ ] Trainerfotos einbauen.
- [x] Details zu Trainingstagen/Gruppen je Trainer anzeigen.
- [ ] Klären, ob diese Details manuell gepflegt werden oder aus dem Trainingsplan kommen.
- [ ] Optional/ggf. sportliche Ausbildung ergänzen:
  - Trainerschein
  - Lizenz
  - Kampfrichter usw.
- [x] Headlines unter Namen entfernen oder sinnvoll ersetzen, z. B. `Trainer U20`, `Trainer U18` etc.

### Sportstätten

Seite im Dokument: https://85957764.rlc-1952-recklinghausen.pages.dev/pages/facilities

- [x] Hauptgrafik vom Stadion zwingend mit Copyright versehen:
  - `©RVR, 2020 DL-DE/BY-2-0`
- [x] Link/Button **„Zum Trainingsplan“** entfernen.
- [ ] Fotos von Trainingsstätten einbauen.
- [x] Marker beim Stadion Hohenhorst von **„BAHN“** in **„OUTDOOR“** ändern.
  - Passend zu den anderen Markern wie `INDOOR` und `KRAFT`.

### Kontakt

Seite im Dokument: https://85957764.rlc-1952-recklinghausen.pages.dev/pages/contact

- [x] Überflüssige Bereiche entfernen, damit die Seite übersichtlicher wird.
- [x] Kachelinhalte ausrichten; aktuell wirkt es unruhig.
- [x] Rechte Box/Bereich **„Und jetzt?“** entfernen.
- [x] Impressum und Datenschutz aus der Kontaktseite entfernen.
- [x] Impressum und Datenschutz als eigene Seiten/Bereiche implementieren.
- [x] Footer-Links für Impressum und Datenschutz auf die jeweiligen eigenen Seiten/Bereiche führen.
- [x] Lesbarkeit im Bereich Impressum/Datenschutz verbessern; Screenshot zeigt schwer lesbare/überladene Darstellung.

## Offene Rückfragen / benötigtes Material

- [ ] Alte Homepage/Quelle für vollständigen News-Import bereitstellen bzw. prüfen.
- [x] Entscheiden: vergangene Termine ausblenden oder nur visuell schwächer darstellen.
  - Entscheidung umgesetzt: vergangene Termine werden automatisch ausgeblendet.
- [ ] Trainingszeiten-Pflegeprozess klären:
  - manuell im CMS/Content?
  - aus Trainingsplan-Daten?
  - aus Datei/CSV/anderer Quelle?
- [ ] Trainerteam-Datenquelle klären:
  - Trainingstage/Gruppen manuell oder aus Trainingsplan?
- [ ] Trainerfotos liefern/freigeben.
- [ ] Fotos der Trainingsstätten liefern/freigeben.
- [ ] Vorstandsfotos liefern/freigeben, falls Personenkacheln mit Bildern gewünscht sind.
- [ ] Fehlende Vorstandsdaten/E-Mail-Adressen/weitere Rollen final bestätigen.
- [ ] Partnerliste final bestätigen; im Dokument sind drei Links genannt.

## Empfohlene Umsetzungspakete

1. **Globales Layout/Design glattziehen**
   - Hero-Größen, Überschriften, Breite, Vereinsfarben/Dunkelblau, Footer-Instagram.
2. **Startseite umbauen**
   - Termin-Klickpfade, „Rund um den Verein“-Kacheln, Entfernen „Der Verein auf einen Blick“.
3. **Termine & Training Datenlogik**
   - Terminseite, Termin-Details, vergangene Termine, Trainingsfilter, Pflegeprozess.
4. **Content-Seiten Verein/Trainer/Sportstätten/Kontakt**
   - Vorstand/Partner, Trainerteam, Sportstätten-Copyright/Fotos/Marker, Kontakt entschlacken, Impressum/Datenschutz auslagern.
5. **News/Go-live-Content**
   - News-Import alte Homepage, Kachelbugs, Beitragsfooter, Druckfunktion entfernen.
6. **QA-Gate vor Kundenfreigabe**
   - Desktop + Mobile prüfen.
   - Startseite, Aktuelles, Termine, Training, Verein, Trainerteam, Sportstätten, Kontakt, Impressum, Datenschutz.
   - Linkziele, Hoverzustände, Lesbarkeit, Footer, Responsiveness und Content-Vollständigkeit prüfen.

## Einschätzung: Was muss eingepflegt werden?

Ja, aus dem Dokument müssen mehrere konkrete Inhalte eingepflegt werden:

- Startseiten-Kacheltexte für „Rund um den Verein“.
- Vorstandsdaten inklusive teils genannter E-Mail-Adressen.
- Partnerlinks.
- Stadion-Copyright.
- Marker-Textänderung `BAHN` → `OUTDOOR`.
- Footer-Instagram-Textlink.
- Separates Impressum/Datenschutz-Konzept statt Anzeige unter Kontakt.
- Vollständiger News-Bestand von der alten Homepage vor Go-live.

Nicht direkt ohne weiteres Material einpflegbar sind:

- Trainerfotos.
- Sportstättenfotos.
- ggf. Vorstandsfotos.
- vollständige/abschließend freigegebene Vorstandsdaten.
- Detaildaten zu Trainer-Ausbildungen/Lizenzen.
- genaue Datenquelle/Pflegeprozess für Trainingszeiten und Trainerdetails.
