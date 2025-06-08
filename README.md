![image](https://github.com/user-attachments/assets/d273947d-7d7a-4e1a-8c09-a4acf01cf47a)
# Hotel Reservation System

Dieses Projekt wurde im Rahmen des Moduls **„Anwendungsentwicklung mit Python“ (FS25)** an der FHNW umgesetzt. Ziel war es, ein funktionales Hotelreservierungssystem zu entwickeln, welches Konzepte wie objektorientierte Programmierung, eine mehrschichtige Architektur und Datenbankzugriffe mit SQLite abbildet und die vorgegebenen User Stories erfüllt.

---

## 1. Projektübersicht

Das System ermöglicht es Gästen, nach verfügbaren Hotels und Zimmern zu suchen, Buchungen anzulegen, zu stornieren und nach einem Aufenthalt Rechnungen zu erhalten. Gleichzeitig bietet es Administratoren Einsicht in sämtliche Buchungen.

- **Ziel:** Ein funktionales Hotelreservierungssystem zu entwickeln, welches Konzepte der Python-Programmierung abbildet.  
- **IDE:** Visual Studio Code
- **Modellierung:** Visual Paradigm
- **Versionskontrolle & Kollaboration:** GitHub  
- **Architektur (Schichtenmodell):**  
  1. **Model Layer** – Domänenklassen (Hotel, Room, Guest, Booking, Invoice, …)  
  2. **Data Access Layer (DAL)** – CRUD-Operationen auf SQLite  
  3. **Business Logic Layer (BLL)** – Geschäftslogik und Validierungen  
  4. **UI Layer** – Konsolen-Menü (`run.py`), Eingabe- und Validierungshelfer (`input_helper.py`, `validation_helper.py`)  
  5. **User Stories** – Skripte je Anwendungsfall (`user_stories/…`)

Das ursprüngliche Team bestand aus vier Mitgliedern. Im Verlauf des Projekts zeigte sich jedoch, dass die anderen zwei Gruppenmitglieder kaum bis keine aktive Mitarbeit leisteten – sowohl im Unterricht als auch bei der praktischen Umsetzung. Ihre unzureichenden Python-Kenntnisse erschwerten die Zusammenarbeit zusätzlich und machten eine faire Aufgabenverteilung nahezu unmöglich.

Die vollständige Entwicklung und Organisation des Projekts wurde daher von uns beiden aktiven Mitgliedern übernommen. Wir setzten sämtliche *User Stories*, entwarfen die Code-Struktur und entwickelten die wesentlichen Systemkomponenten selbstständig. 

Ein zusätzlicher Mehraufwand entstand durch folgende Probleme:

* Die anderen beiden Gruppenmitglieder reichten ihre Codeanteile ohne funktionale Überprüfung ein – zum Teil automatisiert mit ChatGPT generiert.
* Diese Änderungen wurden direkt über GitHub gepusht, ohne vorherige Rücksprache.
* Fehler in den gemeinsam genutzten Layern (z. B. Business Logic) führten dazu, dass eigene, *User Stories* nicht mehr getestet werden konnten.
* Die Korrektur dieser Beiträge erforderte viel Zeit und wiederholte Koordination.

Aufgrund dieser Situation und in Rücksprache mit unserer betreuenden Lehrperson (Charuta) haben wir uns entschieden, das Team offiziell zu trennen. Da dies zusätzlich noch zu einem ziemlich späten Zeitpunkt passierte, wurde als reduzierte Abgabevorgabe folgendes vereinbart:

* Umsetzung **aller Minimal-User-Stories**
* Umsetzung von **einer** der beiden Erweiterungen:
  * Datenbank-Schemaänderung **oder**
  * Datenvisualisierung

Wir entschieden uns bewusst für eine *Datenvisualisierungs-User-Story*, da uns deren technische Umsetzung besonders interessierte. Themen rund um Datenbankschemata und SQL hatten wir bereits im vorigen Semester vertieft behandelt.

Unser Ziel war es, die umgesetzten *User Stories* so perfekt, wie für uns möglich zu gestalten. Dies beanspruchte natürlich viel Zeit, da viele Anpassungen nötig waren, bis wir mit dem Code 100% zufrieden waren. Zusätzlich haben wir ein zentrales Test- und Startskript namens `run.py` entwickelt, das als Menüoberfläche dient. Es ermöglicht die gezielte Ausführung der implementierten User Stories, wobei zwischen der Benutzer- und der Administratorrolle unterschieden wird. 

Nach dem Start des Programms kann ausgewählt werden, ob man als *User* oder als *Admin* fortfahren möchte. Anschließend erhält man eine strukturierte Auswahl der verfügbaren Funktionen (z. B. Buchung, Stornierung, Visualisierung etc.), die per Eingabe direkt ausgeführt werden können.

Diese Lösung erleichtert nicht nur das Testen der Anwendung, sondern stellt auch sicher, dass alle User Stories sauber und unabhängig voneinander aufrufbar sind – ein zentraler Aspekt für die Präsentation und Qualitätssicherung unseres Systems.

---

## 2. Aufgabenteilung

Wir waren zu zweit im aktiven Kernteam und haben die Implementierung folgendermaßen aufgeteilt:

| Teammitglied        | Zuständigkeiten                                                                                                                                         |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Gianluca**   | Model Layer (Domänenklassen) & UI Layer (`input_helper.py`)                                              |
| **Miro**            | Data Access Layer (SQLite-SQL, DA-Klassen) & UI Layer (`validation_helper.py`)                                                                                                            |
| **Business Logic**  | Wurde passend zu den User Stories sukzessive zwischen uns beiden aufgeteilt und gemeinsam implementiert                                                 |

> **Hinweis:**  
> Anfangs waren wir vier Teammitglieder, doch zwei haben sich nur kurzfristig für GitHub-Aktivitäten eingeloggt und keinen Programmcode beigesteuert. Daher haben wir die verbleibenden User Stories fair aufgeteilt und in enger Abstimmung abgearbeitet.

---

## 3. Klassendiagramm und objektorientierte Modellierung

Im Rahmen der zweiten Unterrichtseinheit haben wir uns intensiv mit den Grundlagen der objektorientierten Programmierung (OOP) beschäftigt. Aufbauend auf einem vorgegebenen ER-Diagramm, das die Datenstruktur eines Hotelreservierungssystems beschreibt, erarbeiteten wir ein entsprechendes Klassendiagramm.

Das ER-Diagramm beinhaltete zentrale Entitäten wie zum Beispiel `Hotel`, `Room`, `Guest`, `Booking` und deren Beziehungen zueinander. Unsere Aufgabe bestand darin, diese Entitäten in Klassen zu überführen und dabei die Prinzipien der objektorientierten Modellierung korrekt anzuwenden. Dies umfasste insbesondere die Strukturierung in Attribute und Methoden sowie die Berücksichtigung von Kapselung, Verantwortlichkeiten und logischen Beziehungen zwischen den Objekten.

Das resultierende Klassendiagramm diente als Grundlage für die spätere Code-Implementierung und half dabei, eine saubere und nachvollziehbare Architektur für das System zu schaffen. Jede Klasse bildet dabei eine reale Komponente des Hotelbetriebs ab und ermöglicht durch entsprechende Methoden die zentrale Funktionalität wie z. B. Buchung, Verwaltung oder Auswertung.


## 4. Code-Architektur & Ordnerstruktur

Die Architektur ist in klassische Schichten (Layers) gegliedert. Jeder Layer hat klar abgegrenzte Verantwortlichkeiten:





### 4.1 Model Layer (Domänenklassen)

Im Model Layer haben wir alle zentralen Objekte unseres Hotelreservierungssystems abgebildet. Jede Klasse entspricht einer Entität aus dem ER‐Schema und enthält nur jene Attribute und Methoden, die für das Geschäftsverständnis nötig sind.

- **Hotel**  
  Ein `Hotel` hat einen Namen, eine Sternebewertung und eine Adresse. Aus programmtechnischer Sicht kapselt die Klasse die internen Eigenschaften („private Attributes“), und über Methoden wie `add_room()` und `remove_room()` verwalten wir die Zimmerliste. So ist garantiert, dass ein `Room` immer nur einem Hotel zugeordnet sein kann und umgekehrt.

- **Room**  
  Jeder `Room` gehört zu genau einem `Hotel` und hat eine Zimmernummer sowie einen Basispreis pro Nacht. Außerdem besitzt ein Zimmer genau einen `RoomType` (z. B. „Standard“, „Suite“). Ganz wichtig: Die Methode `is_available(check_in, check_out)` prüft anhand aller bestehenden Buchungen, ob der Zeitraum frei ist. Neu hinzukommende Buchungen werden in der Buchungsliste des Raumes abgelegt.

- **RoomType**  
  Diese Klasse dient dazu, Zimmertypen (z. B. „Doppelzimmer Deluxe“ oder „Einzelzimmer Economy“) zentral zu beschreiben. Ein `RoomType` enthält eine Kurzbeschreibung (Text) und eine maximale Personenzahl. So können wir später leicht überprüfen, ob zu viele Gäste für einen bestimmten Zimmertyp angefragt wurden.

- **Facilities**  
  Einige Hotels bieten Zusatzleistungen oder Ausstattungsmerkmale (z. B. „WLAN“, „Fitnessraum“ oder „Frühstück inklusive“) an. Um diese m:n‐Beziehung abzubilden, verwalten wir in der Klasse `Facilities` die einzelnen Ausstattungs‐Einträge und nutzen in der Datenbank eine Zwischentabelle `room_facilities`. In den Objekten halten wir einfach eine Liste aller `Facilities`, die einem Zimmer zugeordnet sind.

- **Guest**  
  Ein `Guest` steht für einen Hotelgast mit Vorname, Nachname, E-Mail und Adresse. Außerdem verwaltet er eine Liste aller eigenen Buchungen (`bookings`). Immer, wenn eine neue `Booking` für diesen Gast erzeugt wird, ruft der Konstruktor intern `guest.add_booking(thisBooking)` auf, damit die Assoziation bidirektional bleibt.

- **Booking**  
  Eine `Booking` verbindet genau einen `Guest` mit einem oder mehreren `Room`‐Objekten. In der Buchung speichern wir Anreisedatum, Abreisedatum, den Gesamtpreis (`total_amount`) und ein Flag `is_cancelled`, falls die Buchung storniert wurde. Direkt beim Erzeugen einer Buchung wird automatisch ein `Invoice`‐Objekt angelegt (Komposition). So ist garantiert, dass jede abgeschlossene Buchung‐Instanz genau eine Rechnung besitzt.

- **Invoice**  
  Eine `Invoice` enthält das Ausstellungsdatum und den Gesamtbetrag zu einer Buchung. Technisch ist sie fest an eine `Booking` gebunden („Komposition“), sodass bei Löschung einer Buchung auch die zugehörige Rechnung verschwindet. Wir haben uns bewusst entschieden, den Konstruktor so einfach wie möglich zu halten: Er nimmt nur die schon existierende `Booking`, das Datum und den Betrag entgegen, prüft die Gültigkeit und speichert die Werte.

- **Address**  
  Um Redundanzen zu vermeiden, haben wir eine eigene `Address`‐Klasse modelliert (Straße, Stadt, Postleitzahl). Sowohl ein `Hotel` als auch ein `Guest` referenzieren auf exakt ein `Address`‐Objekt. So können wir später Adressen wiederverwenden oder zentral ändern, ohne in jeder Klasse mehrfach Textdaten pflegen zu müssen.






---

### 4.2 Data Access Layer (DAL)

Der Data Access Layer bündelt alle SQLite-Zugriffe und sorgt dafür, dass die Geschäftslogik (BLL) keine SQL-Syntax kennt. Unsere Überlegungen:

- **Zentrales Basis-DAO (`BaseDataAccess`):**  
  Liest beim Erstellen einer Verbindung immer die Umgebungsvariable `DB_FILE`, öffnet die SQLite-Datenbank und stellt drei grundlegende Methoden zur Verfügung:
  - `execute(sql, params)`: Führt `INSERT`/`UPDATE`/`DELETE`-Statements aus.  
  - `fetchone(sql, params)`: Liefert genau eine Ergebnis-Zeile.  
  - `fetchall(sql, params)`: Liefert alle passenden Zeilen.  

- **Spezifische DAO-Klassen (CRUD):**  
  Für jede Entität im Model–Layer gibt es genau eine DAO-Klasse, die nur für die dazugehörige Tabelle zuständig ist. Beispiele:
  - **`HotelDataAccess` / `RoomDataAccess` / `RoomTypeDataAccess` / `FacilityDataAccess`:**  
    ­ ­ Bieten Methoden zum Einlesen von Hotels, Räumen, Zimmertypen und Ausstattungen.  
  - **`GuestDataAccess`:**  
    ­ ­ Bietet `read_guest_by_id()`, `read_guest_by_email()`, `insert_guest()`, `read_all_guests()`.  
  - **`BookingDataAccess`:**  
    ­ ­ Unterstützt `insert_booking()`, `read_booking_by_id()`, `read_bookings_by_guest_id()`, `read_bookings_by_room()`, `cancel_booking()`.  
  - **`InvoiceDataAccess`:**  
    ­ ­ Kümmert sich um `insert_invoice()`, `read_invoice_by_id()`, `read_invoice_by_booking_id()`.
  - **`AnalyticsDataAccess`:**  
    ­ ­ Liefert Analytics-Methoden wie `read_occupancy_by_hotel(hotel_id)` für Belegungsraten pro Zimmertyp. 

- **Wesentliche Designentscheidungen:**  
  1. **Einzelverantwortung pro DAO:** Jeder DAO ist nur für eine Tabelle zuständig. So bleibt die SQL-Logik wirklich vollständig im DAL, und Änderungen am Schema betreffen nur eine Klasse.  
  2. **Konvertierung zu Model-Objekten:** Bei `fetchone()` und `fetchall()` übersetzen wir die reinen Datenbank-Zeilen in Instanzen der Domänenklassen (z. B. `Hotel`, `Room`, `Booking`). Damit ist sichergestellt, dass der BLL-Layer ausschließlich mit Objekten arbeitet und nicht mit rohen Tupeln.  
  3. **Keine Geschäftsregeln im DAL:** Validierungen wie „Ist der Gast wirklich ein `Guest`?“ oder „Sind Check-in und Check-out gültige Daten?“ werden komplett im BLL-Layer erledigt. Das DAL führt nur SQL aus und erstellt Model-Instanzen.  

Mit diesem Ansatz stellen wir sicher, dass die Schichtentrennung strikt eingehalten wird und Änderungen im Datenbankschema (z. B. Hinzufügen einer neuen Spalte) nur minimale Anpassungen im DAL erfordern.  



---
### 4.3 Business Logic Layer

| **Manager-Klasse**    | **Verantwortung**                                                                                                                                                                                                                                           |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **HotelManager**      | Filtern von Hotels nach Stadt, Sternen, Verfügbarkeit; Koordinierung von `RoomDataAccess` – liefert `Room`-Objekte als Antwort.                                                                                                                            |
| **GuestManager**      | Validiert Eingaben (Vor-/Nachname, E-Mail), Erstellung & Abfrage von Gästen über `GuestDataAccess`.                                                                                                                                                          |
| **BookingManager**    | Erstellt neue Buchungen (`insert_booking()`), listet Buchungen pro Gast (`read_bookings_by_guest_id()`), storniert Buchungen und markiert deren Invoice.                                                                                                      |
| **InvoiceManager**    | Generiert Rechnungen für abgeschlossene oder stornierte Buchungen: Berechnung des Betrags, Anlegen in DB, Laden über `InvoiceDataAccess`.                                                                                                                   |
| **PricingManager**    | Berechnet dynamische Preise: Basispreis = `base_price_per_night * nights`, ergänzt um saisonale Auf- oder Abschläge (z. B. Sommeraufschlag, Winterrabatt).                                                                                                    |
| **AnalyticsManager**  | Ruft `AnalyticsDataAccess.read_occupancy_by_hotel(hotel_id)` ab und wandelt die Ergebnisse in ein `pandas.DataFrame` mit den Spalten <br>`type_id`, `description`, `total_rooms`, `booked_rooms`, `belegung_rate`. |
---

### 4.4 Unser Run.py Test

- **`run.py`** – Hauptskript mit Konsolen-Menü:  
  1. Kopiert beim Start `hotel_reservation_sample.db` → `working_hotel.db` (via `shutil.copyfile`).  
  2. Setzt `os.environ["DB_FILE"] = "database/working_hotel.db"`.  
  3. Importiert und initialisiert Manager:  
     ```python
     from business_logic.hotel_manager import HotelManager
     from business_logic.guest_manager import GuestManager
     from business_logic.booking_manager import BookingManager
     from business_logic.invoice_manager import InvoiceManager
     from business_logic.pricing_manager import PricingManager
     ```
  4. Zeigt ein Hauptmenü (US 1–10) an, liest die Wahl, und ruft dynamisch die passende User Story auf:  
     ```python
     choice = input_valid_int("Menüpunkt wählen (1–18): ", 1, 18)
     run_user_story(choice)
     ```
  Der genaue und gesamte Code ist in unserem run.py File im VSCode zu finden.

  5. Nutzt Helper-Funktionen aus `ui/input_helper.py` und `ui/validation_helper.py` für konsistente Konsoleneingaben.

- **Helper-Module**  
  - **`ui/input_helper.py`**: Eingabe-Funktionen mit Validierung (ganze Zahlen, Strings, Ja/Nein, E-Mail).  
  - **`ui/validation_helper.py`**: Reguläre Ausdrücke für `is_valid_email()` und `is_valid_name()`.

---


## 5. Herausforderungen & Lessons Learned

### 5.1 Herausforderungen

1. **Layer-Grenzen & Imports**  
   - Häufig vergaßen wir, Klassen aus einer anderen Schicht zu importieren (z. B. `BookingDataAccess` in `InvoiceDataAccess` oder `Room` in `Booking`).  
   - Um zirkuläre Importe zu vermeiden, haben wir in manchen Methoden lokale Imports genutzt und sorgfältig auf korrekte Paketpfade geachtet.

2. **Model `Invoice` vs. Datenbank-Schema**  
   - Der `Invoice`-Konstruktor (`__init__(self, booking, issue_date, total_amount)`) war auf genau drei Argumente ausgelegt – ohne `invoice_id`.  
   - Anfangs wurde versehentlich `invoice_id` mitkonstruiert, was zu:  
     ```
     TypeError: Invoice.__init__() takes 4 positional arguments but 5 were given
     ```  
     führte.  
   - Lösung: In `InvoiceDataAccess.read_invoice_by_id()` nur `(inv_id, booking, issue_date, total_amount)` an `Invoice()` übergeben und `invoice_id` nicht im Konstruktor erwarten.


3. **Storno-Logik (US 6)**  
   - Auf Objektebene (`Booking.cancel()`) und in der Datenbank (`UPDATE booking SET is_cancelled = 1`) synchronisieren.  
   - Alte Rechnung musste auf Objektebene auf `None` gesetzt werden, damit keine veraltete Rechnung weiterverwendet wird.

4. **Probleme bei mehreren US**  
   - Ähnliche Schichtgrenzen-/Import-Probleme traten auch bei US 5 und US 7 auf – z. B. falsche Parameteranzahl, fehlende `datetime`-Imports, Namensinkonsistenzen.  
   - Beispiel US 6: In `InvoiceDataAccess.read_invoice_by_id()` vergessen, `from data_access.booking_data_access import BookingDataAccess` zu importieren, was zu  
     ```
     NameError: name 'BookingDataAccess' is not defined
     ```  
     führte.

Dies waren Beispiele von Problemen die wir gerade kürzlich hatten und ebenfalls die Art von Problemen hatten, die am häufigsten vorkammen. Natürlich hatten wir im Verlauf vom Projekt noch einige andere Errors die es zu lösen gab, jedoch wäre es zu viel und nicht zielführend alle aufzulisten.

5. **Team-Kollaboration & GitHub-Workflow**  
   - Anfangs wurden ungeprüfte Änderungen direkt auf `main` gepusht, was Konflikte verursachte.  
   - Wir haben rasch gelernt, Feature-Branches zu nutzen und regelmäßig `git pull --rebase` durchzuführen.  
   - Code-Reviews und Pull-Request-Merges stellten sicher, dass nur fehlerfreier Code in `main` gelangt.

---

### 5.2 Lessons Learned

## Lessons Learned

Im Rahmen des Projekts konnten wir nicht nur unsere Python-Kenntnisse vertiefen, sondern auch wichtige Erfahrungen im Bereich der Softwareentwicklung, Projektorganisation und Teamarbeit sammeln. Die Entwicklung des Hotelreservierungssystems hat uns gezeigt, wie theoretische Konzepte aus dem Studium in ein funktionierendes, praxisnahes System überführt werden können. Im Folgenden fassen wir unsere zentralen Learnings zusammen:

### Vom Datenmodell zum Klassendiagramm

- Wir haben gelernt, wie man ein gegebenes ER-Diagramm strukturiert in ein objektorientiertes Klassendiagramm überführt.
- Dabei wurde deutlich, wie sich reale Entitäten wie `Hotel`, `Room`, `Guest` oder `Booking` in Python-Klassen abbilden lassen.
- Beziehungen zwischen Entitäten – insbesondere 1:n und m:n – konnten wir mit Zwischentabellen und passender Objektstruktur erfolgreich modellieren.
- Unser Verständnis für Datenmodellierung aus vorangegangenen Modulen (z. B. Datenbasierte Unternehmensanwendungen) konnten wir dadurch gezielt anwenden und vertiefen.

### Objektorientierte Programmierung mit Python

- Wir konnten die Prinzipien der OOP (Klassen, Attribute, Methoden, Konstruktoren) praxisnah umsetzen.
- Durch Kapselung, Getter/Setter und klare Verantwortlichkeiten in den Klassen entwickelten wir wartbaren und strukturierten Code.
- Die Anwendung von Aggregation und sinnvoller Trennung in Schichten (UI, Business Logic, Data Access) half uns dabei, ein sauberes Softwaredesign zu etablieren.
- Besonders wertvoll war auch die Implementierung einer Testumgebung (`run.py`), mit der wir die einzelnen User Stories gezielt testen und voneinander trennen konnten.

### Versionskontrolle mit GitHub

- Wir sammelten praktische Erfahrung mit Git und GitHub – vom Erstellen und Klonen von Repositories über das Pushen und Mergen bis zur Konfliktbehandlung.
- Dabei lernten wir, wie wichtig saubere Branch-Strukturen, Commit-Kommentare und Pull-Requests für die Zusammenarbeit im Team sind.
- Wir haben unser Projekt strukturiert im Repository aufgebaut und das `README.md` als zentrale Dokumentation gepflegt.

### Teamarbeit und Projektverlauf

- Die ursprünglich vierköpfige Projektgruppe musste im Verlauf geteilt werden, da es zu ungleicher Arbeitsverteilung und fehlender Beteiligung kam.
- Diese Erfahrung war lehrreich: Wir haben erkannt, wie wichtig frühzeitige Kommunikation und klare Absprachen im Team sind.
- Ein wesentliches Learning ist, bei Anzeichen von Unausgeglichenheit nicht zu lange zu warten, sondern frühzeitig nach Lösungen oder Umstrukturierungen zu suchen.
- Die spätere Gruppenaufteilung hat es uns ermöglicht, fokussierter und eigenverantwortlich zu arbeiten – was sich positiv auf Qualität und Teamdynamik ausgewirkt hat.

### Projektstruktur und Testing

- Die eigenständige Entscheidung, ein zentrales Ausführungs- und Testmenü (`run.py`) zu entwickeln, half uns, das System übersichtlich und modular zu halten.
- Dadurch konnten wir nicht nur unsere User Stories gezielt testen, sondern auch zwischen Admin- und Nutzerrollen unterscheiden.
- Diese Struktur ermöglichte uns eine systematische Qualitätssicherung und diente als wichtiger Bestandteil unserer Abschlusspräsentation.

---

Insgesamt hat uns dieses Projekt nicht nur fachlich, sondern auch methodisch und menschlich weitergebracht – sowohl im Hinblick auf die Softwareentwicklung als auch auf die Zusammenarbeit im Team.


> **Vielen Dank fürs Lesen!**  
> Dieses README bietet einen kompakten Überblick über Architektur, Aufgabenteilung und technische Entscheidungen. Weitere Details zu Klassen, Methoden und SQL-Statements finden sich im Quellcode in den jeweiligen Layer-Ordnern, wie auch im Deepnote. 





