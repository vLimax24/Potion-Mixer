import curses  # Importiere das Modul curses für die Terminal-GUI
import random  # Importiere das Modul random für Zufallszahlen
import time    # Importiere das Modul time für Zeitfunktionen

def main(stdscr):
    # Initiale Einstellungen und Setup für curses
    curses.curs_set(0)  # Verstecke den Cursor
    stdscr.clear()      # Leere das Terminal-Fenster
    curses.start_color()  # Aktiviere Farbunterstützung

    # Farben definieren: Liste von Tupeln (Farbpaar-ID, Farbe)
    farben = [
        (1, curses.COLOR_RED), (2, curses.COLOR_CYAN), (3, curses.COLOR_GREEN),
        (4, curses.COLOR_YELLOW), (5, curses.COLOR_WHITE), (6, curses.COLOR_BLUE),
        (7, curses.COLOR_MAGENTA), (8, curses.COLOR_RED), (9, curses.COLOR_BLUE), (10, curses.COLOR_YELLOW)
    ]
    for idx, farbe in enumerate(farben):
        curses.init_pair(idx + 1, farbe[1], curses.COLOR_BLACK)  # Initialisiere Farbpaar (Vordergrundfarbe, schwarzer Hintergrund)

    # Materialien und Kombinationen definieren
    materialien = [
        {"name": name, "farbe": idx + 1} for idx, name in enumerate(
            ["Lavendel", "Drachenblut", "Salbei", "Rosmarin", "Kamille", "Bambus", "Echtes Gold", "Schwarzes Salz",
             "Fliederblüten", "Eisenfeilen"]
        )
    ]

    # Unterteile Materialien in verfügbare und gesperrte
    verfuegbare_materialien = materialien[:4]  # Die ersten 4 Materialien sind initial verfügbar
    gesperrte_materialien = materialien[4:]       # Die restlichen Materialien sind zunächst gesperrt

    # Liste der gültigen Rezeptkombinationen
        gueltige_kombinationen = [
        {"name": "Lavendelzauber", "materialien": ["Lavendel", "Salbei"], "qualitaet_spanne": (0, 100)},
        {"name": "Rosmarin-Elixier", "materialien": ["Rosmarin", "Kamille"], "qualitaet_spanne": (0, 100)},
        {"name": "Schutztrank", "materialien": ["Salbei", "Rosmarin"], "qualitaet_spanne": (0, 100)},
        {"name": "Beruhigungstrank", "materialien": ["Lavendel", "Kamille"], "qualitaet_spanne": (0, 100)},
        {"name": "Stärketrank", "materialien": ["Eisenfeilen", "Lavendel"], "qualitaet_spanne": (0, 100)},
        {"name": "Goldener Segen", "materialien": ["Eisenfeilen", "Rosmarin", "Echtes Gold"],
         "qualitaet_spanne": (0, 100)},
        {"name": "Liebe der Fliederblüte", "materialien": ["Fliederblüten", "Lavendel"], "qualitaet_spanne": (0, 100)},
        {"name": "Schutzflieder", "materialien": ["Fliederblüten", "Salbei"], "qualitaet_spanne": (0, 100)},
        {"name": "Reichtumstrank", "materialien": ["Eisenfeilen", "Lavendel", "Echtes Gold"],
         "qualitaet_spanne": (0, 100)},
        {"name": "Magische Essenz", "materialien": ["Fliederblüten", "Rosmarin"], "qualitaet_spanne": (0, 100)},
        {"name": "Heilender Zauber", "materialien": ["Kamille", "Salbei"], "qualitaet_spanne": (0, 100)},
        {"name": "Flexibilitäts-Elixier", "materialien": ["Bambus", "Salbei"], "qualitaet_spanne": (0, 100)},
        {"name": "Wind der Freiheit", "materialien": ["Bambus", "Rosmarin"], "qualitaet_spanne": (0, 100)},
        {"name": "Verwandlungszauber", "materialien": ["Bambus", "Fliederblüten"], "qualitaet_spanne": (0, 100)},
        {"name": "Schwächungstrank", "materialien": ["Eisenfeilen", "Lavendel"], "qualitaet_spanne": (0, 100)},
        {"name": "Harmonie-Elixier", "materialien": ["Kamille", "Fliederblüten"], "qualitaet_spanne": (0, 100)},
        {"name": "Reinigungstrank", "materialien": ["Salbei", "Lavendel"], "qualitaet_spanne": (0, 100)},
        {"name": "Zaubertrank der Weisheit", "materialien": ["Kamille", "Rosmarin"], "qualitaet_spanne": (0, 100)},
        {"name": "Heilende Magie", "materialien": ["Lavendel", "Kamille", "Fliederblüten"],
         "qualitaet_spanne": (0, 100)},
        {"name": "Sturmtrank", "materialien": ["Fliederblüten", "Eisenfeilen", "Lavendel"],
         "qualitaet_spanne": (0, 100)},
        {"name": "Kraft des Goldes", "materialien": ["Eisenfeilen", "Fliederblüten", "Echtes Gold"],
         "qualitaet_spanne": (0, 100)},
        {"name": "Mächtiger Segen", "materialien": ["Rosmarin", "Bambus", "Eisenfeilen"], "qualitaet_spanne": (0, 100)},
        {"name": "Banntrank", "materialien": ["Fliederblüten", "Eisenfeilen", "Lavendel"],
         "qualitaet_spanne": (0, 100)},
        {"name": "Essenz des Lebens", "materialien": ["Kamille", "Bambus", "Salbei"], "qualitaet_spanne": (0, 100)},
        {"name": "Flimmertrank", "materialien": ["Bambus", "Fliederblüten", "Rosmarin"], "qualitaet_spanne": (0, 100)},
        {"name": "Magischer Schutz", "materialien": ["Fliederblüten", "Rosmarin", "Kamille"],
         "qualitaet_spanne": (0, 100)},
        {"name": "Liebeszauber", "materialien": ["Rosmarin", "Fliederblüten", "Kamille"], "qualitaet_spanne": (0, 100)},
        {"name": "Schattenbringer", "materialien": ["Bambus", "Salbei", "Eisenfeilen"], "qualitaet_spanne": (0, 100)},
        {"name": "Seelenzauber", "materialien": ["Kamille", "Bambus", "Rosmarin"], "qualitaet_spanne": (0, 100)},
        {"name": "Zauber der Freiheit", "materialien": ["Bambus", "Kamille", "Fliederblüten"],
         "qualitaet_spanne": (0, 100)},
        {"name": "Essenz des Glücks", "materialien": ["Kamille", "Bambus", "Fliederblüten"],
         "qualitaet_spanne": (0, 100)},
        {"name": "Lichtzauber", "materialien": ["Lavendel", "Rosmarin", "Eisenfeilen"], "qualitaet_spanne": (0, 100)},
        {"name": "Energie-Elixier", "materialien": ["Rosmarin", "Bambus", "Fliederblüten"],
         "qualitaet_spanne": (0, 100)},
        {"name": "Feuer der Wiedergeburt", "materialien": ["Fliederblüten", "Bambus", "Kamille"],
         "qualitaet_spanne": (0, 100)},
        {"name": "Kristallklarer Zauber", "materialien": ["Fliederblüten", "Rosmarin", "Kamille"],
         "qualitaet_spanne": (0, 100)},
        {"name": "Lebensquell-Elixier", "materialien": ["Fliederblüten", "Lavendel", "Eisenfeilen"],
         "qualitaet_spanne": (0, 100)},
        {"name": "Trank der Unendlichkeit", "materialien": ["Bambus", "Kamille", "Fliederblüten"],
         "qualitaet_spanne": (0, 100)},
        {"name": "Glücksbringer", "materialien": ["Fliederblüten", "Lavendel", "Kamille"], "qualitaet_spanne": (0, 100)}
    ]

    # Initialisiere Spiel-Statistiken
    level, aktuelle_xp, xp_bis_naechstes_level, muenzen, doppel_xp_zaehler = 1, 0, 100, 200, 0
    hinweis_preis, freischalt_preis = 50, 100
    rezeptbuch = {}  # Rezeptbuch als leeres Dictionary
    kesselabnutzung = 100  # Zustand des Kessels in Prozent

    max_rezepte = 3  # Maximale Anzahl von Rezepten pro Seite im Rezeptbuch
    gesamt_seiten = (len(rezeptbuch) + max_rezepte - 1) // max_rezepte  # Berechne die Gesamtseitenzahl

    # Aktuelle Seite im Rezeptbuch (Index beginnt bei 0)
    aktuelle_seite = 0 

    def minispiel_kessel_reparatur(stdscr, muenzen):
        """
        Minispiel zur Reparatur des Kessels.
        Gibt einen Erfolgsstatus und die aktualisierte Münzenanzahl zurück.
        """
        curses.curs_set(0)
        stdscr.clear()
        reparatur_gesamt = 0  # Gesamt-Reparatur in Prozent
        kessel_status = 0     # Aktueller Zustand des Kessels
        zeile_offset = 5      # Vertikaler Versatz für die Kesseldarstellung

        while True:
            stdscr.clear()
            stdscr.addstr(2, 2, "✨ Kessel-Reparatur ✨", curses.color_pair(4) | curses.A_BOLD)
            stdscr.addstr(3, 2, f"💸 Münzen verfügbar: {muenzen}", curses.color_pair(7))
            stdscr.addstr(4, 2, f"🔧 Gesamtreparatur: {reparatur_gesamt}%", curses.color_pair(3))

            # Zeichne den Kessel basierend auf dem Reparaturstatus
            if kessel_status < 50:  # Kessel in Rot anzeigen, wenn Reparatur < 50%
                stdscr.addstr(zeile_offset, 10, "╔═════╗", curses.color_pair(1))
            else:  # Kessel in Blau anzeigen, wenn Reparatur >= 50%
                stdscr.addstr(zeile_offset, 10, "╔═════╗", curses.color_pair(3))
            for i in range(1, 11):
                if i <= kessel_status // 10:
                    if kessel_status < 50:
                        stdscr.addstr(zeile_offset + i, 10, "║█████║", curses.color_pair(1))
                    else:
                        stdscr.addstr(zeile_offset + i, 10, "║█████║", curses.color_pair(3))
                else:
                    stdscr.addstr(zeile_offset + i, 10, "", curses.color_pair(1))
            stdscr.addstr(zeile_offset + 11, 10, "╚═════╝", curses.color_pair(2))

            stdscr.addstr(16, 2, "Drücke [LEERTASTE], um zu reparieren.")
            stdscr.addstr(17, 2, "Drücke [Q], um zum Hauptmenü zurückzukehren.")
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord(' '):  # Leertaste gedrückt
                kosten = random.randint(10, 20)  # Zufällige Reparaturkosten
                reparatur = random.randint(12, 20)  # Zufälliger Reparaturfortschritt in Prozent

                if muenzen < kosten:
                    stdscr.addstr(19, 2, "Nicht genug Münzen! Spiel verloren!", curses.color_pair(1) | curses.A_BOLD)
                    stdscr.refresh()
                    time.sleep(2)
                    return False, muenzen  # Reparatur fehlgeschlagen

                muenzen -= kosten  # Ziehe die Kosten von den Münzen ab
                reparatur_gesamt += reparatur  # Erhöhe den Gesamt-Reparaturfortschritt
                kessel_status = min(reparatur_gesamt, 100)  # Aktualisiere den Kesselzustand (max. 100%)

                stdscr.addstr(18, 2, f"Repariert um {reparatur}%. Kosten: {kosten} Münzen.", curses.color_pair(3))
                stdscr.refresh()
                time.sleep(0.5)

                if reparatur_gesamt >= 100:
                    stdscr.refresh()
                    return True, muenzen  # Reparatur erfolgreich

            elif key == ord('q'):  # Q gedrückt – verlasse das Minispiel
                return False, muenzen

    def zeichne_rahmen():
        """
        Zeichnet den Rahmen der Spieloberfläche.
        """
        stdscr.addstr(0, 0, "╔" + "═" * 48 + "╦" + "═" * 30 + "╦" + "═" * 40 + "╗")
        for i in range(1, 21):
            stdscr.addstr(i, 0, "║")
            stdscr.addstr(i, 49, "║")
            stdscr.addstr(i, 80, "║")
            stdscr.addstr(i, 121, "║")
        stdscr.addstr(21, 0, "╚" + "═" * 48 + "╩" + "═" * 30 + "╩" + "═" * 40 + "╝")
        stdscr.addstr(0, 49, "╦")
        stdscr.addstr(0, 80, "╦")
        stdscr.addstr(21, 49, "╩")
        stdscr.addstr(21, 80, "╩")

    def zeichne_status():
        """
        Zeichnet den Statusbereich mit Level, XP und Münzen.
        """
        stdscr.addstr(1, 2, f"Level: {level}   XP: {aktuelle_xp}/{xp_bis_naechstes_level}", curses.color_pair(3))
        gefuellte_laenge = int(20 * aktuelle_xp / xp_bis_naechstes_level)
        balken = "█" * gefuellte_laenge + "-" * (20 - gefuellte_laenge)
        stdscr.addstr(2, 2, f"Fortschritt: [{balken}]", curses.color_pair(6))
        stdscr.addstr(3, 2, f"Münzen: {muenzen}", curses.color_pair(4))

    def zeichne_kessel(ausgewaehlte_materialien):
        """
        Zeichnet den Hexenkessel und zeigt die ausgewählten Materialien an.
        """
        stdscr.addstr(1, 51, "🧙 Hexenkessel", curses.color_pair(6) | curses.A_BOLD)
        stdscr.addstr(3, 51, f"Kesselabnutzung: {kesselabnutzung}%", curses.color_pair(3))

        # Zeige die im Kessel ausgewählten Materialien
        stdscr.addstr(5, 52, "Im Kessel:", curses.color_pair(4))
        for idx, material in enumerate(ausgewaehlte_materialien):
            farbe_index = [m["name"] for m in materialien].index(material)
            stdscr.addstr(7 + idx, 54, f"- {material}", curses.color_pair(materialien[farbe_index]["farbe"]))

    def zeichne_rezeptbuch():
        """
        Zeichnet das Rezeptbuch, zeigt Rezepte auf der aktuellen Seite und gibt Navigationshinweise.
        """
        nonlocal aktuelle_seite, gesamt_seiten
        stdscr.addstr(1, 82, "📜 Rezeptbuch", curses.color_pair(6) | curses.A_BOLD)

        # Berechne den Indexbereich der Rezepte, die auf der aktuellen Seite angezeigt werden
        start_idx = aktuelle_seite * max_rezepte
        end_idx = start_idx + max_rezepte
        recipes_to_display = list(rezeptbuch.items())[start_idx:end_idx]

        # Zeige die Rezepte der aktuellen Seite an
        for idx, (name, details) in enumerate(recipes_to_display):
            stdscr.addstr(3 + idx * 5, 82, f"{name}:", curses.color_pair(6))
            stdscr.addstr(4 + idx * 5, 82, f"Materialien: {', '.join(details['materialien'])}", curses.color_pair(4))
            stdscr.addstr(5 + idx * 5, 82, f"Beste Qualität: {details['qualitaet']}%", curses.color_pair(3))
            stdscr.addstr(6 + idx * 5, 82, f"Anzahl: {details['anzahl']}", curses.color_pair(5))
            stdscr.addstr(7 + idx * 5, 82, "-------------------", curses.color_pair(6))

        # Navigationshinweise und Seiteninfo
        gesamt_seiten = max((len(rezeptbuch) + max_rezepte - 1) // max_rezepte, 1)
        stdscr.addstr(18, 82, f"Seite {aktuelle_seite + 1} von {gesamt_seiten}", curses.A_BOLD)
        stdscr.addstr(19, 82, "Drücke ← für nächste", curses.A_DIM)
        stdscr.addstr(20, 82, "Drücke → für vorherige.", curses.A_DIM)

    def zeichne_materialien(ausgewaehlte_materialien):
        """
        Zeichnet den Bereich der Materialien, die der Spieler auswählen kann.
        """
        stdscr.addstr(5, 2, "🪄 Materialien:", curses.color_pair(6) | curses.A_BOLD)
        for idx, material in enumerate(verfuegbare_materialien):
            stdscr.addstr(7 + idx, 4, f"{idx + 1}. {material['name']}", curses.color_pair(material["farbe"]))
        stdscr.addstr(19, 2, "Wähle Materialien mit den Tasten [1-4],", curses.A_DIM)
        stdscr.addstr(20, 2, "bestätige mit [ENTER].", curses.A_DIM)

    def verarbeite_trank(ausgewaehlte_materialien):
        """
        Verarbeitet die Herstellung eines Tranks anhand der ausgewählten Materialien.
        Berechnet Qualität, XP, Münzen und aktualisiert das Rezeptbuch.
        """
        nonlocal aktuelle_xp, level, xp_bis_naechstes_level, muenzen, doppel_xp_zaehler, kesselabnutzung

        for kombination in gueltige_kombinationen:
            if sorted(ausgewaehlte_materialien) == sorted(kombination["materialien"]):
                qualitaet = random.randint(*kombination["qualitaet_spanne"])
                xp_gewonnen = round(10 + qualitaet / 5)
                if doppel_xp_zaehler > 0:
                    xp_gewonnen *= 2
                    doppel_xp_zaehler -= 1
                if qualitaet == 100:
                    doppel_xp_zaehler = 5

                aktuelle_xp += xp_gewonnen
                if aktuelle_xp >= xp_bis_naechstes_level:
                    aktuelle_xp -= xp_bis_naechstes_level
                    level += 1
                    xp_bis_naechstes_level = int(xp_bis_naechstes_level * 1.5)

                base_coins = round(5 + qualitaet * 0.2)
                if len(ausgewaehlte_materialien) == 3:
                    base_coins = int(base_coins * 1.5)  # Falls drei Materialien verwendet werden, erhöhe die Basis-Münzen um 50%

                if kombination["name"] in rezeptbuch:
                    gebraute_anzahl = rezeptbuch[kombination["name"]]["anzahl"]
                    coins = max(int(base_coins * (1 - 0.01 * gebraute_anzahl)), 3)  # Pro hergestelltem Trank sinken die Münzen um 1%, mindestens 3
                    rezeptbuch[kombination["name"]]["anzahl"] += 1
                else:
                    coins = base_coins
                    rezeptbuch[kombination["name"]] = {"materialien": kombination["materialien"],
                                                       "qualitaet": qualitaet, "anzahl": 1}

                muenzen += coins
                kesselabnutzung -= random.randint(3, 5)  # Verringere den Kesselzustand zufällig

                return f"Erfolgreich! {kombination['name']} - Qualität: {qualitaet}% (+{xp_gewonnen} XP, +{coins} Münzen)"

        # Falls keine gültige Kombination gefunden wird, verringere den Kesselzustand stärker
        kesselabnutzung -= random.randint(6, 12)
        if kesselabnutzung < 0:
            kesselabnutzung = 0

        if kesselabnutzung == 0:
            reparatur_erfolgreich, muenzen = minispiel_kessel_reparatur(stdscr, muenzen)
            if reparatur_erfolgreich:
                kesselabnutzung = 100
                stdscr.refresh()
                time.sleep(2)
                return "Kessel erfolgreich repariert!"
            else:
                stdscr.addstr(10, 2, "Spiel verloren! Du hattest nicht genug Münzen.", curses.color_pair(1) | curses.A_BOLD)
                stdscr.refresh()
                time.sleep(2)
                curses.endwin()
                quit()

        return "Fehlgeschlagen! Kesselabnutzung steigt!"

    def laden():
        """
        Öffnet den Shop, in dem der Spieler Rezept-Hinweise kaufen oder neue Materialien freischalten kann.
        """
        nonlocal muenzen, hinweis_preis, freischalt_preis, gesperrte_materialien

        # Definiere Wachstumsfaktoren für die Preise im Shop
        hinweis_wachstumsfaktor = 1.3  # Preissteigerung für Rezept-Hinweise
        freischalt_wachstumsfaktor = 1.75  # Preissteigerung für Materialfreischaltungen

        while True:
            stdscr.clear()
            stdscr.addstr(2, 2, f"Shop ({muenzen} Münzen verfügbar):", curses.color_pair(6))
            stdscr.addstr(4, 4, f"1. Rezept-Hinweis kaufen ({hinweis_preis} Münzen)")

            if gesperrte_materialien:
                stdscr.addstr(5, 4, f"2. Neues Material freischalten ({freischalt_preis} Münzen)")
            else:
                stdscr.addstr(5, 4, "(Alle Materialien freigeschaltet!)", curses.A_DIM)

            stdscr.addstr(7, 2, "Drücke [Q], um zurückzukehren.")
            key = stdscr.getch()

            if key == ord('q'):
                break
            elif key == ord('1'):
                if muenzen >= hinweis_preis:
                    # Filtere gültige Rezeptkombinationen basierend auf den aktuell verfügbaren Materialien
                    gueltige_hinweise = [kombination for kombination in gueltige_kombinationen if all(
                        mat in [m["name"] for m in verfuegbare_materialien] for mat in kombination["materialien"]
                    )]

                    if gueltige_hinweise:
                        muenzen -= hinweis_preis
                        hinweis = random.choice(gueltige_hinweise)
                        teil_hinweis = hinweis["materialien"][:-1] + ["..."]
                        stdscr.addstr(9, 4, f"Tipp: {teil_hinweis}", curses.A_BOLD)

                        # Erhöhe den Preis für den Hinweis exponentiell
                        hinweis_preis = round(hinweis_preis * hinweis_wachstumsfaktor)
                    else:
                        stdscr.addstr(9, 4, "Keine Rezepte verfügbar.", curses.A_BOLD)
                else:
                    stdscr.addstr(9, 4, "Nicht genug Münzen!", curses.A_BOLD)
                stdscr.refresh()
                stdscr.getch()

            elif key == ord('2') and gesperrte_materialien:
                if muenzen >= freischalt_preis:
                    muenzen -= freischalt_preis
                    neues_material = gesperrte_materialien.pop(0)
                    verfuegbare_materialien.append(neues_material)
                    stdscr.addstr(9, 4, f"Neues Material freigeschaltet: {neues_material['name']}!", curses.A_BOLD)

                    # Erhöhe den Preis für die Materialfreischaltung exponentiell
                    freischalt_preis = round(freischalt_preis * freischalt_wachstumsfaktor)
                else:
                    stdscr.addstr(9, 4, "Nicht genug Münzen!", curses.A_BOLD)
                stdscr.refresh()
                stdscr.getch()

    def zeichne_info(stdscr, muenzen):
        """
        Zeichnet den statischen Informationsbereich mit den Steuerungsanweisungen.
        """
        stdscr.addstr(22, 2, "Drücke [ENTER], um einen Trank zu brauen.", curses.A_BOLD)
        stdscr.addstr(23, 2, "Drücke [S], um den Shop zu öffnen.", curses.A_BOLD)
        stdscr.addstr(24, 2, "Drücke [Q], um das Spiel zu beenden.", curses.A_BOLD)
        stdscr.refresh()  # Aktualisiere den Bildschirm

    def spiel_schleife():
        """
        Haupt-Spielschleife, die alle Spielaktionen und Benutzerinteraktionen verarbeitet.
        """
        curses.curs_set(0)  # Cursor verbergen
        nonlocal muenzen, kesselabnutzung, aktuelle_seite
        ausgewaehlte_materialien = []  # Liste der aktuell im Kessel ausgewählten Materialien

        while True:
            stdscr.clear()  # Leere das Terminal
            # Zeichne alle GUI-Komponenten
            zeichne_info(stdscr, muenzen)
            zeichne_rahmen()
            zeichne_status()
            zeichne_materialien(ausgewaehlte_materialien)
            zeichne_kessel(ausgewaehlte_materialien)
            zeichne_rezeptbuch()

            stdscr.refresh()  # Aktualisiere das Terminal
            time.sleep(0.1)   # Warte 0.1 Sekunden

            # Verarbeite Benutzereingaben
            key = stdscr.getch()

            # Überprüfe, ob der Kessel defekt ist
            if kesselabnutzung <= 0:
                stdscr.addstr(8, 2, "Der Kessel ist kaputt! Reparatur notwendig.", curses.color_pair(1) | curses.A_BOLD)
                stdscr.refresh()
                time.sleep(2)

                erfolgreich, muenzen = minispiel_kessel_reparatur(stdscr, muenzen)
                if erfolgreich:
                    kesselabnutzung = 100
                    stdscr.addstr(10, 2, "Kessel erfolgreich repariert!", curses.color_pair(2) | curses.A_BOLD)
                else:
                    stdscr.addstr(10, 2, "Spiel verloren! Du hattest nicht genug Münzen.", curses.color_pair(1) | curses.A_BOLD)
                    stdscr.refresh()
                    time.sleep(2)
                    break

                stdscr.refresh()
                time.sleep(2)
                continue

            # Rezeptbuch-Navigation
            if key == curses.KEY_RIGHT:  # Nächste Seite
                if aktuelle_seite < gesamt_seiten - 1:
                    aktuelle_seite += 1
            elif key == curses.KEY_LEFT:  # Vorherige Seite
                if aktuelle_seite > 0:
                    aktuelle_seite -= 1

            # Spiel beenden
            if key == ord('q'):
                break
            elif key == ord('s'):
                laden()
            # Falls "0" gedrückt wird (entspricht Material Nr. 10, da es keine Taste "10" gibt)
            elif key == ord('0') and len(verfuegbare_materialien) >= 10:
                if len(ausgewaehlte_materialien) < 3:
                    ausgewaehlte_materialien.append(verfuegbare_materialien[9]["name"])
            # Verarbeitung von Tastatureingaben für Materialien 1-9
            elif ord('1') <= key <= ord(str(min(len(verfuegbare_materialien), 9))):
                material_idx = key - ord('1')  # Ermittle den Index des gedrückten Materials
                if len(ausgewaehlte_materialien) < 3:
                    ausgewaehlte_materialien.append(verfuegbare_materialien[material_idx]["name"])

            # Wenn ENTER gedrückt wird und es Materialien im Kessel gibt, verarbeite den Trank
            elif key == ord('\n') and ausgewaehlte_materialien:
                result = verarbeite_trank(ausgewaehlte_materialien)
                ausgewaehlte_materialien.clear()  # Leere den Kessel nach der Verarbeitung
                stdscr.addstr(24, 2, result, curses.A_BOLD)  # Zeige das Ergebnis an
                stdscr.refresh()
                stdscr.getch()

    # Starte die Spielschleife
    spiel_schleife()

# Starte das curses-Programm mit der main-Funktion als Einstiegspunkt
curses.wrapper(main)
