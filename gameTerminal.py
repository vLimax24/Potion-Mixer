import curses
import random
import time

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    curses.start_color()

    # Farben
    farben = [
        (1, curses.COLOR_RED), (2, curses.COLOR_CYAN), (3, curses.COLOR_GREEN),
        (4, curses.COLOR_YELLOW), (5, curses.COLOR_WHITE), (6, curses.COLOR_BLUE),
        (7, curses.COLOR_MAGENTA), (8, curses.COLOR_RED), (9, curses.COLOR_BLUE), (10, curses.COLOR_YELLOW)
    ]
    for idx, farbe in enumerate(farben):
        curses.init_pair(idx + 1, farbe[1], curses.COLOR_BLACK)

    # Materialien und Kombinationen
    materialien = [
        {"name": name, "farbe": idx + 1} for idx, name in enumerate(
            ["Lavendel", "Drachenblut", "Salbei", "Rosmarin", "Kamille", "Bambus", "Echtes Gold", "Schwarzes Salz", "Fliederblüten", "Eisenfeilen"]
        )
    ]

    verfuegbare_materialien = materialien[:4]
    gesperrte_materialien = materialien[4:]

    gueltige_kombinationen = [
        {"name": "Lavendelzauber", "materialien": ["Lavendel", "Salbei"], "qualitaet_spanne": (0, 100)},
        {"name": "Rosmarin-Elixier", "materialien": ["Rosmarin", "Kamille"], "qualitaet_spanne": (0, 100)},
        {"name": "Schutztrank", "materialien": ["Salbei", "Rosmarin"], "qualitaet_spanne": (0, 100)},
        {"name": "Beruhigungstrank", "materialien": ["Lavendel", "Kamille"], "qualitaet_spanne": (0, 100)},
        {"name": "Stärketrank", "materialien": ["Eisenfeilen", "Lavendel"], "qualitaet_spanne": (0, 100)},
        {"name": "Goldener Segen", "materialien": ["Eisenfeilen", "Rosmarin"], "qualitaet_spanne": (0, 100)},
        {"name": "Liebe der Fliederblüte", "materialien": ["Fliederblüten", "Lavendel"], "qualitaet_spanne": (0, 100)},
        {"name": "Schutzflieder", "materialien": ["Fliederblüten", "Salbei"], "qualitaet_spanne": (0, 100)},
        {"name": "Reichtumstrank", "materialien": ["Gold", "Eisenfeilen"], "qualitaet_spanne": (0, 100)},
        {"name": "Magische Essenz", "materialien": ["Fliederblüten", "Rosmarin"], "qualitaet_spanne": (0, 100)},
        {"name": "Heilender Zauber", "materialien": ["Kamille", "Salbei"], "qualitaet_spanne": (0, 100)},
        {"name": "Drachenfeuer", "materialien": ["Gold", "Feuerblume"], "qualitaet_spanne": (0, 100)},
        {"name": "Flexibilitäts-Elixier", "materialien": ["Bambus", "Salbei"], "qualitaet_spanne": (0, 100)},
        {"name": "Wind der Freiheit", "materialien": ["Bambus", "Rosmarin"], "qualitaet_spanne": (0, 100)},
        {"name": "Verwandlungszauber", "materialien": ["Bambus", "Fliederblüten"], "qualitaet_spanne": (0, 100)},
        {"name": "Schwächungstrank", "materialien": ["Schwarzes Salz", "Eisenfeilen"], "qualitaet_spanne": (0, 100)},
        {"name": "Zerstörungstrank", "materialien": ["Schwarzes Salz", "Feuerblume"], "qualitaet_spanne": (0, 100)},
        {"name": "Harmonie-Elixier", "materialien": ["Kamille", "Fliederblüten"], "qualitaet_spanne": (0, 100)},
        {"name": "Frostschutzzauber", "materialien": ["Schwarzes Salz", "Eisblume"], "qualitaet_spanne": (0, 100)},
        {"name": "Reinigungstrank", "materialien": ["Salbei", "Schwarzes Salz"], "qualitaet_spanne": (0, 100)},
        {"name": "Zaubertrank der Weisheit", "materialien": ["Kamille", "Rosmarin"], "qualitaet_spanne": (0, 100)},
        {"name": "Heilende Magie", "materialien": ["Lavendel", "Kamille", "Fliederblüten"], "qualitaet_spanne": (0, 100)},
        {"name": "Sturmtrank", "materialien": ["Fliederblüten", "Eisenfeilen", "Schwarzes Salz"], "qualitaet_spanne": (0, 100)},
        {"name": "Kraft des Goldes", "materialien": ["Gold", "Eisenfeilen", "Fliederblüten"], "qualitaet_spanne": (0, 100)},
        {"name": "Feuerzauber", "materialien": ["Feuerblume", "Fliederblüten", "Schwarzes Salz"], "qualitaet_spanne": (0, 100)},
        {"name": "Mächtiger Segen", "materialien": ["Rosmarin", "Bambus", "Eisenfeilen"], "qualitaet_spanne": (0, 100)},
        {"name": "Banntrank", "materialien": ["Schwarzes Salz", "Fliederblüten", "Eisenfeilen"], "qualitaet_spanne": (0, 100)},
        {"name": "Essenz des Lebens", "materialien": ["Kamille", "Bambus", "Salbei"], "qualitaet_spanne": (0, 100)},
        {"name": "Flimmertrank", "materialien": ["Bambus", "Fliederblüten", "Eisblume"], "qualitaet_spanne": (0, 100)},
        {"name": "Magischer Schutz", "materialien": ["Schwarzes Salz", "Fliederblüten", "Rosmarin"], "qualitaet_spanne": (0, 100)},
        {"name": "Liebeszauber", "materialien": ["Rosmarin", "Fliederblüten", "Kamille"], "qualitaet_spanne": (0, 100)},
        {"name": "Schattenbringer", "materialien": ["Bambus", "Salbei", "Eisenfeilen"], "qualitaet_spanne": (0, 100)},
        {"name": "Frost-Magie", "materialien": ["Eisblume", "Kamille", "Gold"], "qualitaet_spanne": (0, 100)},
        {"name": "Zauber der Freiheit", "materialien": ["Bambus", "Kamille", "Fliederblüten"], "qualitaet_spanne": (0, 100)},
        {"name": "Hitzewelle", "materialien": ["Feuerblume", "Bambus", "Schwarzes Salz"], "qualitaet_spanne": (0, 100)},
        {"name": "Heiltrank der Stärke", "materialien": ["Kamille", "Eisenfeilen", "Salbei"], "qualitaet_spanne": (0, 100)},
        {"name": "Verborgene Magie", "materialien": ["Fliederblüten", "Eisenfeilen", "Rosmarin"], "qualitaet_spanne": (0, 100)},
        {"name": "Kristall der Klarheit", "materialien": ["Eisenfeilen", "Salbei", "Fliederblüten"], "qualitaet_spanne": (0, 100)},
        {"name": "Drachenblut-Zauber", "materialien": ["Gold", "Kamille", "Eisenfeilen"], "qualitaet_spanne": (0, 100)},
        {"name": "Heiliger Trank", "materialien": ["Lavendel", "Fliederblüten", "Bambus"], "qualitaet_spanne": (0, 100)},
        {"name": "Zauber der Veränderung", "materialien": ["Rosmarin", "Salbei", "Bambus"], "qualitaet_spanne": (0, 100)},
        {"name": "Frostfeuer", "materialien": ["Eisblume", "Feuerblume", "Gold"], "qualitaet_spanne": (0, 100)},
        {"name": "Essenz des Glücks", "materialien": ["Kamille", "Bambus", "Fliederblüten"], "qualitaet_spanne": (0, 100)},
        {"name": "Lichtzauber", "materialien": ["Lavendel", "Rosmarin", "Eisenfeilen"], "qualitaet_spanne": (0, 100)},
        {"name": "Nebeltrank", "materialien": ["Eisblume", "Salbei", "Gold"], "qualitaet_spanne": (0, 100)},
        {"name": "Energie-Elixier", "materialien": ["Rosmarin", "Gold", "Bambus"], "qualitaet_spanne": (0, 100)},
        {"name": "Feuer der Wiedergeburt", "materialien": ["Fliederblüten", "Feuerblume", "Bambus"], "qualitaet_spanne": (0, 100)},
        {"name": "Kristallklarer Zauber", "materialien": ["Eisblume", "Fliederblüten", "Rosmarin"], "qualitaet_spanne": (0, 100)},
        {"name": "Seelenzauber", "materialien": ["Kamille", "Bambus", "Rosmarin"], "qualitaet_spanne": (0, 100)},
        {"name": "Lebensquell-Elixier", "materialien": ["Fliederblüten", "Lavendel", "Eisenfeilen"], "qualitaet_spanne": (0, 100)},
        {"name": "Trank der Unendlichkeit", "materialien": ["Gold", "Bambus", "Feuerblume"], "qualitaet_spanne": (0, 100)},
        {"name": "Glücksbringer", "materialien": ["Fliederblüten", "Lavendel", "Eisblume"], "qualitaet_spanne": (0, 100)},
        {"name": "Schattenfeuer", "materialien": ["Feuerblume", "Schwarzes Salz", "Bambus"], "qualitaet_spanne": (0, 100)},
        {"name": "Lichtritter-Trank", "materialien": ["Rosmarin", "Lavendel", "Gold"], "qualitaet_spanne": (0, 100)},
        {"name": "Trank der ewigen Liebe", "materialien": ["Fliederblüten", "Kamille", "Lavendel"], "qualitaet_spanne": (0, 100)},
        {"name": "Dunkelheitszauber", "materialien": ["Schwarzes Salz", "Feuerblume", "Kamille"], "qualitaet_spanne": (0, 100)},
        {"name": "Frostgeist-Trank", "materialien": ["Eisblume", "Rosmarin", "Fliederblüten"], "qualitaet_spanne": (0, 100)},
        {"name": "Essenz der Dunkelheit", "materialien": ["Schwarzes Salz", "Eisenfeilen", "Fliederblüten"], "qualitaet_spanne": (0, 100)},
        {"name": "Zauber des Sturms", "materialien": ["Eisenfeilen", "Salbei", "Fliederblüten"], "qualitaet_spanne": (0, 100)},
        {"name": "Essenz des Feuers", "materialien": ["Fliederblüten", "Schwarzes Salz", "Bambus"], "qualitaet_spanne": (0, 100)},
    ]


    # Status
    level, aktuelle_xp, xp_bis_naechstes_level, muenzen, doppel_xp_zaehler = 1, 0, 100, 200, 0
    hinweis_preis, freischalt_preis = 10, 20
    rezeptbuch = {}
    kesselabnutzung = 100
    scroll_offset = 0

    max_recipes_per_page = 3  # Show 3 recipes per page
    total_pages = (len(rezeptbuch) + max_recipes_per_page - 1) // max_recipes_per_page  # Calculate total pages

    # Page navigation state
    current_page = 0  # Start at the first page

    def minispiel_kessel_reparatur(stdscr, muenzen):
        curses.curs_set(0)
        stdscr.clear()
        reparatur_gesamt = 0
        kessel_status = 0
        zeile_offset = 5

        while True:
            stdscr.clear()
            stdscr.addstr(2, 2, "✨ Kessel-Reparatur ✨", curses.color_pair(4) | curses.A_BOLD)
            stdscr.addstr(3, 2, f"💸 Münzen verfügbar: {muenzen}", curses.color_pair(7))
            stdscr.addstr(4, 2, f"🔧 Gesamtreparatur: {reparatur_gesamt}%", curses.color_pair(3))
            
            # Kessel-Darstellung
            
            if kessel_status < 50:  # Kessel ist rot, wenn die Reparatur < 50%
                        stdscr.addstr(zeile_offset, 10, "╔═════╗", curses.color_pair(1))
            else:  # Kessel wird blau, wenn die Reparatur >= 50%
                        stdscr.addstr(zeile_offset, 10, "╔═════╗", curses.color_pair(3))
            for i in range(1, 11):
                if i <= kessel_status // 10:
                    if kessel_status < 50:  # Kessel ist rot, wenn die Reparatur < 50%
                        stdscr.addstr(zeile_offset + i, 10, "║█████║", curses.color_pair(1))  # Rot
                    else:  # Kessel wird blau, wenn die Reparatur >= 50%
                        stdscr.addstr(zeile_offset + i, 10, "║█████║", curses.color_pair(3))  # Blau
                else:
                    stdscr.addstr(zeile_offset + i, 10, "", curses.color_pair(1))
            stdscr.addstr(zeile_offset + 11, 10, "╚═════╝", curses.color_pair(2))

            stdscr.addstr(16, 2, "Drücke [LEERTASTE], um zu reparieren.")
            stdscr.addstr(17, 2, "Drücke [Q], um zum Hauptmenü zurückzukehren.")
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord(' '):
                kosten = random.randint(10, 20)
                reparatur = random.randint(12, 20)
                
                if muenzen < kosten:
                    stdscr.addstr(19, 2, "Nicht genug Münzen! Spiel verloren!", curses.color_pair(1) | curses.A_BOLD)
                    stdscr.refresh()
                    time.sleep(2)
                    return False, muenzen

                muenzen -= kosten
                reparatur_gesamt += reparatur
                kessel_status = min(reparatur_gesamt, 100)

                stdscr.addstr(18, 2, f"Repariert um {reparatur}%. Kosten: {kosten} Münzen.", curses.color_pair(3))
                stdscr.refresh()
                time.sleep(0.5)

                if reparatur_gesamt >= 100:
                    stdscr.refresh()
                    
                    return True, muenzen

            elif key == ord('q'):
                return False, muenzen


    def zeichne_rahmen():
        # Rahmen zeichnen
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
        stdscr.addstr(1, 2, f"Level: {level}   XP: {aktuelle_xp}/{xp_bis_naechstes_level}", curses.color_pair(3))
        gefuellte_laenge = int(20 * aktuelle_xp / xp_bis_naechstes_level)
        balken = "█" * gefuellte_laenge + "-" * (20 - gefuellte_laenge)
        stdscr.addstr(2, 2, f"Fortschritt: [{balken}]", curses.color_pair(6))
        stdscr.addstr(3, 2, f"Münzen: {muenzen}", curses.color_pair(4))

    def zeichne_kessel(ausgewaehlte_materialien):
        stdscr.addstr(1, 51, "🧙 Hexenkessel", curses.color_pair(6) | curses.A_BOLD)
        stdscr.addstr(3, 51, f"Kesselabnutzung: {kesselabnutzung}%", curses.color_pair(3))

        # Zeige die ausgewählten Materialien im Kessel
        stdscr.addstr(5, 52, "Im Kessel:", curses.color_pair(4))
        for idx, material in enumerate(ausgewaehlte_materialien):
            stdscr.addstr(7 + idx, 54, f"- {material}", curses.color_pair(materialien[[m["name"] for m in materialien].index(material)]["farbe"]))


    def zeichne_rezeptbuch():
        nonlocal current_page, total_pages
        stdscr.addstr(1, 82, "📜 Rezeptbuch", curses.color_pair(6) | curses.A_BOLD)
        
        # Calculate the range of recipes to display on the current page
        start_idx = current_page * max_recipes_per_page
        end_idx = start_idx + max_recipes_per_page
        recipes_to_display = list(rezeptbuch.items())[start_idx:end_idx]

        # Display recipes for the current page
        for idx, (name, details) in enumerate(recipes_to_display):
            stdscr.addstr(3 + idx * 5, 82, f"{name}:", curses.color_pair(6))
            stdscr.addstr(4 + idx * 5, 82, f"Materialien: {', '.join(details['materialien'])}", curses.color_pair(4))
            stdscr.addstr(5 + idx * 5, 82, f"Qualität: {details['qualitaet']}%", curses.color_pair(3))
            stdscr.addstr(6 + idx * 5, 82, f"Anzahl: {details['anzahl']}", curses.color_pair(5))
            stdscr.addstr(7 + idx * 5, 82, "-------------------", curses.color_pair(6))

        # Display page navigation instructions
        total_pages = max((len(rezeptbuch) + max_recipes_per_page - 1) // max_recipes_per_page, 1)  # Update total pages dynamically, ensuring it starts at 1
        stdscr.addstr(18, 82, f"Seite {current_page + 1} von {total_pages}", curses.A_BOLD)
        stdscr.addstr(19, 82, "Drücke ← für nächste", curses.A_DIM)
        stdscr.addstr(20, 82, "Drücke → für vorherige.", curses.A_DIM)


    def zeichne_materialien(ausgewaehlte_materialien):
        stdscr.addstr(5, 2, "🪄 Materialien:", curses.color_pair(6) | curses.A_BOLD)
        for idx, material in enumerate(verfuegbare_materialien):
            stdscr.addstr(7 + idx, 4, f"{idx + 1}. {material['name']}", curses.color_pair(material["farbe"]))
        stdscr.addstr(19, 2, "Wähle Materialien mit den Tasten [1-4],", curses.A_DIM)
        stdscr.addstr(20, 2, "bestätige mit [ENTER].", curses.A_DIM)


    def verarbeite_trank(ausgewaehlte_materialien):
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

                muenzen += 5 + (qualitaet // 5)
                kesselabnutzung -= random.randint(3, 5)

                if kombination["name"] not in rezeptbuch:
                    rezeptbuch[kombination["name"]] = {"materialien": kombination["materialien"], "qualitaet": qualitaet, "anzahl": 1}
                else:
                    if rezeptbuch[kombination["name"]]["qualitaet"] < qualitaet:
                        rezeptbuch[kombination["name"]]["qualitaet"] = qualitaet
                    rezeptbuch[kombination["name"]]["anzahl"] += 1

                return f"Erfolgreich! {kombination['name']} - Qualität: {qualitaet}% (+{xp_gewonnen} XP, +{5 + (qualitaet // 10)} Münzen)"

        # Wenn der Trank nicht erfolgreich ist, verringern wir die Kesselabnutzung
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
        nonlocal muenzen, hinweis_preis, freischalt_preis, gesperrte_materialien
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
            if key == ord('q'): break
            elif key == ord('1'):
                if muenzen >= hinweis_preis:
                    gueltige_hinweise = [kombination for kombination in gueltige_kombinationen if all(mat in [m["name"] for m in verfuegbare_materialien] for mat in kombination["materialien"])]
                    if gueltige_hinweise:
                        muenzen -= hinweis_preis
                        hinweis = random.choice(gueltige_hinweise)
                        teil_hinweis = hinweis["materialien"][:-1] + ["..."]
                        stdscr.addstr(9, 4, f"Tipp: {teil_hinweis}", curses.A_BOLD)
                        hinweis_preis += 5
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
                    freischalt_preis += 10
                else:
                    stdscr.addstr(9, 4, "Nicht genug Münzen!", curses.A_BOLD)
                stdscr.refresh()
                stdscr.getch()

        


    def zeichne_info(stdscr, muenzen):
        # Draw the static content (only once)
        stdscr.addstr(22, 2, "Drücke [ENTER], um einen Trank zu brauen.", curses.A_BOLD)
        stdscr.addstr(23, 2, "Drücke [S], um den Shop zu öffnen.", curses.A_BOLD)
        stdscr.addstr(24, 2, "Drücke [Q], um das Spiel zu beenden.", curses.A_BOLD)

        # Refresh the screen after drawing
        stdscr.refresh()

    def spiel_schleife():
        curses.curs_set(0)  # Hide cursor
        nonlocal muenzen, kesselabnutzung, current_page
        ausgewaehlte_materialien = []
        global scroll_offset
        scroll_offset = 0
        max_display = 3

        while True:
            stdscr.clear()
            zeichne_info(stdscr, muenzen)
            zeichne_rahmen()
            zeichne_status()
            zeichne_materialien(ausgewaehlte_materialien)
            zeichne_kessel(ausgewaehlte_materialien)
            zeichne_rezeptbuch()
            
            stdscr.refresh()  # Add refresh here
            time.sleep(0.1)

            key = stdscr.getch()
            # Überprüfen, ob der Kessel kaputt ist
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


            if key == ord('t') and scroll_offset > 0:
                scroll_offset -= 1  # Move up by 1 recipe
            elif key == ord('g') and scroll_offset + max_display < len(rezeptbuch):
                scroll_offset += 1  # Move down by 1 recipe

            if key == curses.KEY_RIGHT:  # Next page
                if current_page < total_pages - 1:
                    current_page += 1
            elif key == curses.KEY_LEFT:  # Previous page
                if current_page > 0:
                    current_page -= 1

            if key == ord('q'): break
            elif key == ord('s'): laden()
            elif ord('1') <= key <= ord(str(min(len(verfuegbare_materialien), 9))):
                material_idx = key - ord('1')
                if len(ausgewaehlte_materialien) < 3:
                    ausgewaehlte_materialien.append(verfuegbare_materialien[material_idx]["name"])
            elif key == ord('\n') and ausgewaehlte_materialien:
                result = verarbeite_trank(ausgewaehlte_materialien)
                ausgewaehlte_materialien.clear()
                stdscr.addstr(24, 2, result, curses.A_BOLD)
                stdscr.refresh()
                stdscr.getch()
            elif key == curses.KEY_DOWN and scroll_offset < len(verfuegbare_materialien) - 7:
                scroll_offset += 1
            elif key == curses.KEY_UP and scroll_offset > 0:
                scroll_offset -= 1

    spiel_schleife()

curses.wrapper(main)
