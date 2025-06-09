import ui.input_helper as input_helper
from business_logic.analytics_manager import AnalyticsManager
import matplotlib.pyplot as plt


def run(_hotel_manager=None):
    """
    Diese Funktion nutzt nur den AnalyticsManager, um die Belegungsraten je Zimmertyp
    für ein ausgewähltes Hotel zu visualisieren. Wir fragen nur noch die Hotel‐ID ab,
    damit kein Aufruf zu `read_hotels_by_city` nötig ist.
    """

    print("\n=== Belegungsraten (DV 1) ===\n")

    # 1) Hotel‐ID abfragen (direkt, ohne vorherige Stadtauswahl)
    hotel_id = input_helper.input_valid_int(
        "Bitte die Hotel‐ID für die Belegungsraten eingeben: ",
        min_value=1
    )

    # 2) DataFrame mit Analysedaten holen
    analytics_manager = AnalyticsManager()
    df_occupancy = analytics_manager.get_occupancy_by_room_type(hotel_id)

    # 3) DataFrame in Deepnote anzeigen (Deepnote rendert es automatisch als Tabelle)
    #    Wenn Du nicht in Deepnote bist, kannst Du stattdessen `print(df_occupancy)` verwenden.
    display(df_occupancy)

    # 4) Balkendiagramm zeichnen
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(
        df_occupancy["description"],    # Spalte "description" aus dem DataFrame
        df_occupancy["belegung_rate"],  # Spalte "belegung_rate" aus dem DataFrame
        edgecolor="gray"
    )
    ax.set_title(f"Belegungsrate nach Zimmertyp (Hotel {hotel_id})")
    ax.set_xlabel("Zimmertyp")
    ax.set_ylabel("Belegungsrate (0–1)")
    ax.set_ylim(0, 1.0)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()