![image](https://github.com/user-attachments/assets/d273947d-7d7a-4e1a-8c09-a4acf01cf47a)
# Hotel Reservation System

Dieses Projekt wurde im Rahmen des Moduls **„Anwendungsentwicklung mit Python“ (FS25)** an der FHNW umgesetzt. Ziel war es, ein funktionales Hotelreservierungssystem zu entwickeln, welches Konzepte wie objektorientierte Programmierung, eine mehrschichtige Architektur und Datenbankzugriffe mit SQLite abbildet und die vorgegebenen User Stories erfüllt.

---

## 1. Projektübersicht

Das System ermöglicht es Gästen, nach verfügbaren Hotels und Zimmern zu suchen, Buchungen anzulegen, zu stornieren und nach einem Aufenthalt Rechnungen zu erhalten. Gleichzeitig bietet es Administratoren Einsicht in sämtliche Buchungen.

- **Ziel:** Ein funktionales Hotelreservierungssystem zu entwickeln, welches Konzepte der Python-Programmierung abbildet.  
- **IDE:** Visual Studio Code  
- **Versionskontrolle & Kollaboration:** GitHub  
- **Architektur (Schichtenmodell):**  
  1. **Model Layer** – Domänenklassen (Hotel, Room, Guest, Booking, Invoice, …)  
  2. **Data Access Layer (DAL)** – CRUD-Operationen auf SQLite  
  3. **Business Logic Layer (BLL)** – Geschäftslogik und Validierungen  
  4. **UI Layer** – Konsolen-Menü (`run.py`), Eingabe- und Validierungshelfer (`input_helper.py`, `validation_helper.py`)  
  5. **User Stories** – Skripte je Anwendungsfall (`user_stories/…`)

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

## 3. Code-Architektur & Ordnerstruktur

Die Architektur ist in klassische Schichten (Layers) gegliedert. Jeder Layer hat klar abgegrenzte Verantwortlichkeiten:





### 3.1 Model Layer (Domänenklassen)

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

## 3.2 Data Access Layer (DAL)

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

- **Wesentliche Designentscheidungen:**  
  1. **Einzelverantwortung pro DAO:** Jeder DAO ist nur für eine Tabelle zuständig. So bleibt die SQL-Logik wirklich vollständig im DAL, und Änderungen am Schema betreffen nur eine Klasse.  
  2. **Konvertierung zu Model-Objekten:** Bei `fetchone()` und `fetchall()` übersetzen wir die reinen Datenbank-Zeilen in Instanzen der Domänenklassen (z. B. `Hotel`, `Room`, `Booking`). Damit ist sichergestellt, dass der BLL-Layer ausschließlich mit Objekten arbeitet und nicht mit rohen Tupeln.  
  3. **Keine Geschäftsregeln im DAL:** Validierungen wie „Ist der Gast wirklich ein `Guest`?“ oder „Sind Check-in und Check-out gültige Daten?“ werden komplett im BLL-Layer erledigt. Das DAL führt nur SQL aus und erstellt Model-Instanzen.  

Mit diesem Ansatz stellen wir sicher, dass die Schichtentrennung strikt eingehalten wird und Änderungen im Datenbankschema (z. B. Hinzufügen einer neuen Spalte) nur minimale Anpassungen im DAL erfordern.  



---

### 3.3 Business Logic Layer (BLL)

| **Manager-Klasse**   | **Verantwortung**                                                                                                                                                                                             |
|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **HotelManager**     | Filtern von Hotels nach Stadt, Sternen, Verfügbarkeit; Koordinierung von `RoomDataAccess` – liefert `Room`-Objekte als Antwort.                                                                                |
| **GuestManager**     | Validiert Eingaben (Vor-/Nachname, E-Mail), Erstellung & Abfrage von Gästen über `GuestDataAccess`.                                                                                                             |
| **BookingManager**   | Erstellt neue Buchungen (`insert_booking`), listet Buchungen pro Gast (`read_bookings_by_guest_id`), storniert Buchungen und markiert deren Invoice.                                                            |
| **InvoiceManager**   | Generiert Rechnungen für abgeschlossene oder stornierte Buchungen: Berechnung des Betrags, Anlegen in DB, Laden über `InvoiceDataAccess`.                                                                       |
| **PricingManager**   | Berechnet dynamische Preise: Basispreis = `base_price_per_night * nights`, ergänzt um saisonale Auf- oder Abschläge (z. B. Sommeraufschlag, Winterrabatt).                                                       |

---

### 3.4 UI Layer

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

## 4. User Stories – Überblick

### 4.1 Einfache User Stories (1.x – 4.x)

Einfacher Ablauf im System:

1. **US 1.1** – Hotels in Stadt anzeigen  
2. **US 1.2** – Hotels in Stadt mit Mindeststernen anzeigen  
3. **US 1.3** – Hotels in Stadt mit Zimmern für X Gäste anzeigen  
4. **US 1.4** – Hotels in Stadt nach Verfügbarkeit (Check-in/Check-out) durchsuchen  
5. **US 1.5** – Kombination: Stadt + Sterne + Gäste + Datum (Filterkombi)  
6. **US 1.6** – Detaillierte Hotelinformationen (Ausstattung, Adresse, Sterne)  
7. **US 2.x/3.x** – Zimmertypen und Ausstattung anzeigen und Hotels bearbeiten (entfernen, hinzufügen)
8. **US 4** – Zimmer buchen  

> Diese Stories liefen über einfache SQL-Abfragen im DAL und direktes Mapping in Model-Objekte; die Geschäftslogik war geradlinig und ohne größere Schichtgrenzen-Probleme umsetzbar.

---

### 4.2 Komplexe User Stories: US 5, US 6 & US 7

Wir beschreiben hier nur die Abläufe der drei komplexesten User Stories. Die tiefergehende technische Umsetzung (SQL-Statements, genaue Klassenmethoden etc.) findet sich in unserem Deepnote-Notebook.

---

#### US 5 – Rechnung nach Aufenthalt erstellen

- **Ziel:**  
  Nach Abschluss eines Aufenthalts möchte der Gast eine Rechnung (Zahlungsnachweis) erhalten.

- **Konzepte & Ablauf:**  
  1. **E-Mail validieren:** Die UI fragt via `input_helper` nach einer gültigen E-Mail.  
  2. **Gast laden:** `GuestManager.read_guest_by_email(email)` holt das `Guest`-Objekt. Ist keine Buchung vorhanden, wird eine Fehlermeldung angezeigt.  
  3. **Abgeschlossene Buchungen filtern:**  
     - Mit `BookingManager.get_bookings_for_guest(guest)` werden alle Buchungen des Gastes geholt.  
     - Anschließend filtert die UI nur die Buchungen heraus, deren `check_out_date` in der Vergangenheit liegt und die nicht storniert wurden.  
  4. **Rechnung erzeugen:**  
     - Der Gast wählt eine abgeschlossene Buchung aus der Liste.  
     - `InvoiceManager.generate_invoice(booking)` legt einen neuen Datensatz in der Tabelle `invoice` an (mit Feldern `booking_id`, `issue_date`, `total_amount`).  
     - Intern wird der Rechnungsbetrag berechnet (entweder über `booking.calculate_total_price()` oder direkt `booking.total_amount`) und das Ausstellungsdatum (`date.today()`) gesetzt.  
  5. **Anzeige:** Die UI zeigt dem Gast anschließend die generierte Rechnung, z. B.:  
     ```
     Rechnung für Buchung 7: Datum 2025-05-10, Betrag 760.00 CHF
     ```

> **Hinweis zur Umsetzung:**  
> - Wichtig war, dass die `invoice`-Tabelle nur genau die Spalten `invoice_id`, `booking_id`, `issue_date` (TEXT), `total_amount` (REAL) enthält, weil unser `Invoice`-Konstruktor keine zusätzliche `invoice_id` als Argument erwartet.  
> - Ein früheres Mapping-Problem führte zu einem `TypeError`, weil wir zu viele Parameter an `Invoice.__init__()` übergeben hatten. Dieses Mapping wurde im DAL korrigiert.

---

#### US 6 – Buchung stornieren

- **Ziel:**  
  Ein Gast möchte eine eigene Buchung stornieren, wenn er das Zimmer nicht mehr benötigt. Gleichzeitig soll eine (Storno-)Rechnung angelegt werden.

- **Konzepte & Ablauf:**  
  1. **Identifikation via E-Mail:** Die UI fragt den Gast nach seiner E-Mail und zeigt anschließend alle aktiven (nicht stornierten, zukünftigen) Buchungen an.  
  2. **Buchungsauswahl & Storno:**  
     - Der Gast wählt eine Buchung aus, die storniert werden soll.  
     - `BookingManager.cancel_booking(booking_id)` setzt intern das Flag `is_cancelled = True`.  
     - Die zugehörige `Invoice`-Referenz im `Booking`-Objekt wird auf `None` gesetzt.  
  3. **Storno-Rechnung erzeugen:**  
     - Nach der Stornierung ruft die UI `InvoiceManager.generate_invoice(booking)` auf, um eine neue Rechnung (z. B. Gutschrift oder Storno-Quittung) in der Tabelle `invoice` anzulegen.  
     - Die Rechnung verweist auf die stornierten Buchung und enthält das Ausstellungsdatum sowie den berechneten Betrag (meist 0 CHF oder ein Storno-Betrag).  
  4. **Anzeige:** Die UI bestätigt dem Gast, dass die Buchung storniert und eine Storno-Rechnung angelegt wurde.

> **Hinweis zur Umsetzung:**  
> - Wir haben darauf geachtet, dass im `Booking`-Konstruktor standardmäßig eine `Invoice` erstellt wird (Komposition). Beim Storno (`Booking.cancel()`) wird dieses Invoice-Attribut auf `None` gesetzt.  
> - Ein früherer Fehler war, dass wir versucht haben, eine `BookingDataAccess`-Instanz ohne Import zu verwenden. Dies wurde korrigiert, indem `BookingDataAccess` im DAL- und BLL-Code korrekt importiert wurde.  
> - Außerdem trat ein `TypeError` auf, weil unser `Invoice`-Model nur drei Konstruktor-Parameter (ohne `invoice_id`) erwartet. Mit angepasstem DAL-Mapping war der Fehler behoben.

---

#### US 7 – Dynamische Preisgestaltung anzeigen

- **Ziel:**  
  Gäste sollen basierend auf Saisonzeiten unterschiedliche Preise sehen, um immer den besten Tarif zu wählen.

- **Konzepte & Ablauf:**  
  1. **Zeitraum und Gästezahl erfragen:** Die UI fragt nach Check-in, Check-out und Anzahl Personen.  
  2. **Verfügbare Zimmer laden:** `HotelManager.get_available_rooms(hotel_id, check_in, check_out)` liefert alle freien `Room`-Objekte.  
  3. **Preisberechnung:** Im `PricingManager.calculate_price(room_id, check_in, check_out, guests)` wird:  
     - Die Aufenthaltsdauer berechnet: `(check_out - check_in).days`.  
     - Der Grundpreis: `room.price_per_night * nights`.  
     - **Saisonalität:**  
       - **Hochsaison (Juni–August):** + 20 % zum Basispreis.  
       - **Nebensaison (November–Februar):** – 10 % zum Basispreis.  
       - Standard: Basispreis beibehalten.  
  4. **Anzeige:** Die UI zeigt pro Zimmernummer den dynamisch berechneten Gesamtpreis an, z. B.:  
     ```
     Zimmer 102: Basis 400 CHF/Nacht → 4 Nächte = 1600 CHF (Hochsaison-Aufschlag) → Endpreis 1920 CHF
     ```

> **Hinweis zur Umsetzung:**  
> - In unserem Deepnote-Notebook sind die genauen Monatsbereiche (z. B. `if check_in.month in [6,7,8]:`) und die Prozentrechnungen dokumentiert.  
> - Wir haben bewusst darauf verzichtet, jeden möglichen Sonderfall (Wechsel von Saison-Mitgliedsjahren, Feiertage) abzubilden, da der Prototyp vor allem die dynamische Grundidee demonstrieren soll.  

---

#### Reflexion zu US 5, US 6 & US 7

- Bei allen drei Stories war die enge Zusammenarbeit zwischen DAL, BLL und UI besonders wichtig.  
- Immer wieder sind wir an „Layer-Grenzen“ gescheitert, z. B. wenn in einer BLL-Methode ein falscher DAL-Import fehlte oder wenn Model-Konstruktoren nicht exakt zu den SQL-Resultaten passten.  
- **Beispiel US 6:** Ein `TypeError` („`Invoice.__init__() takes 4 positional arguments but 5 were given`“) zeigte, dass unser DAL zunächst zu viele Felder an den `Invoice`-Konstruktor weiterreichte.  
- Solche Probleme traten auch in US 5 (falsches Mapping von Datumstypen) und US 7 (falsche Monatsbereiche) auf.

## 5. Herausforderungen & Lessons Learned

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



> **Vielen Dank fürs Lesen!**  
> Dieses README bietet einen kompakten Überblick über Architektur, Aufgabenteilung und technische Entscheidungen. Weitere Details zu Klassen, Methoden und SQL-Statements finden sich im Quellcode in den jeweiligen Layer-Ordnern, wie auch im Deepnote. 





