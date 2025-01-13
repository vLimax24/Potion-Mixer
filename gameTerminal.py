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
            ["Feuerblume", "Eisblume", "Schattenblatt", "Sonnenstein", "Nebelstein", "Wasserkranz", "Erdenfrucht", "Sturmessenz", "Mondblüte", "Sternenstaub"]
        )
    ]

    verfuegbare_materialien = materialien[:4]
    gesperrte_materialien = materialien[4:]

    gueltige_kombinationen = [
        {"name": name, "materialien": mats, "qualitaet_spanne": (0, 100)} for name, mats in [
            ("Flammenfrost-Trank", ["Feuerblume", "Eisblume"]),
            ("Schattenlicht-Elixier", ["Schattenblatt", "Sonnenstein"]),
            ("Nebelbrand-Trank", ["Nebelstein", "Feuerblume"]),
            ("Lebensessenz", ["Wasserkranz", "Erdenfrucht"]),
            ("Sturm der Schatten", ["Sturmessenz", "Schattenblatt"]),
            ("Sonnentau-Trank", ["Sonnenstein", "Wasserkranz"]),
            ("Inferno-Eislicht", ["Feuerblume", "Eisblume", "Sonnenstein"]),
            ("Nebelflut-Elixier", ["Nebelstein", "Sturmessenz", "Erdenfrucht"]),
            ("Wasserfrost-Schatten", ["Wasserkranz", "Eisblume", "Schattenblatt"]),
            ("Sonnenflammen-Sturm", ["Sonnenstein", "Feuerblume", "Sturmessenz"]),
            ("Erdige Nebelschatten", ["Erdenfrucht", "Nebelstein", "Schattenblatt"]),
            ("Wassersturm-Feuer", ["Wasserkranz", "Feuerblume", "Sturmessenz"]),
        ]
    ]

    # Status
    level, aktuelle_xp, xp_bis_naechstes_level, muenzen, doppel_xp_zaehler = 1, 0, 100, 20, 0
    hinweis_preis, freischalt_preis = 10, 20
    rezeptbuch = {}
    kesselabnutzung = 100

    def minispiel_kessel_reparatur(stdscr, muenzen):
        reparatur_gesamt = 0
        while True:
            stdscr.clear()
            stdscr.addstr(2, 2, f"Kessel-Reparatur! (Münzen: {muenzen})", curses.color_pair(6))
            stdscr.addstr(4, 2, "Drücke [LEERTASTE], um zu reparieren (kostet 10-20 Münzen).")
            stdscr.addstr(6, 2, "Wenn du keine Münzen mehr hast, verlierst du.")
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord(' '):
                kosten = random.randint(10, 20)
                if muenzen < kosten:
                    stdscr.clear()
                    stdscr.addstr(2, 2, "Du hast nicht genug Münzen! Du hast verloren!", curses.color_pair(1))
                    stdscr.refresh()
                    time.sleep(2)
                    return False, muenzen

                reparatur = random.randint(12, 20)
                muenzen -= kosten
                reparatur_gesamt += reparatur

                stdscr.clear()
                stdscr.addstr(2, 2, f"Repariert um {reparatur}%! Kosten: {kosten} Münzen.", curses.color_pair(3))
                stdscr.addstr(4, 2, f"Gesamte Reparatur: {reparatur_gesamt}%. Münzen übrig: {muenzen}",
                              curses.color_pair(6))
                stdscr.refresh()

                if reparatur_gesamt >= 100:
                    stdscr.addstr(6, 2, "Der Kessel ist vollständig repariert!", curses.color_pair(2))
                    stdscr.refresh()
                    time.sleep(2)
                    return True, muenzen

            elif key == ord('q'):
                return False, muenzen

    # Funktionen
    def zeichne_progress_bar():
        gefuellte_laenge = int(20 * aktuelle_xp / xp_bis_naechstes_level)
        balken = "█" * gefuellte_laenge + "-" * (20 - gefuellte_laenge)
        stdscr.addstr(1, 50, f"Level {level} | XP: {aktuelle_xp}/{xp_bis_naechstes_level}")
        stdscr.addstr(2, 50, f"[{balken}]")

    def zeichne_seitenleiste(scroll_offset=0):
        stdscr.addstr(4, 2, "Materialien:", curses.color_pair(6))
        max_anzeigen = 7
        if len(verfuegbare_materialien) > max_anzeigen:
            # Zeige Pfeil nach unten, wenn mehr als 7 Materialien verfügbar sind
            stdscr.addstr(12, 4, "↓", curses.A_BOLD)

        for idx, material in enumerate(verfuegbare_materialien[scroll_offset:scroll_offset + max_anzeigen]):
            stdscr.addstr(6 + idx, 4, f"{scroll_offset + idx + 1}. {material['name']}", curses.color_pair(material["farbe"]))

        if scroll_offset > 0:
            stdscr.addstr(5, 4, "↑", curses.A_BOLD)

    def zeichne_kessel_bereich(ausgewaehlte_materialien):
        stdscr.addstr(4, 30, "Hexenkessel:", curses.color_pair(6))
        for idx, material in enumerate(ausgewaehlte_materialien):
            farbe = curses.color_pair(next(m["farbe"] for m in materialien if m["name"] == material))
            stdscr.addstr(6 + idx, 32, material, farbe)

        # Anzeige der Kesselabnutzung
        stdscr.addstr(10, 30, f"Kesselabnutzung: {kesselabnutzung}%", curses.color_pair(3))

    def zeichne_rezeptbuch():
        # Verschiebe das Rezeptbuch weiter nach unten, damit es nicht mit den Materialien kollidiert
        stdscr.addstr(15, 2, "Rezeptbuch:", curses.color_pair(6))
        if rezeptbuch:
            for idx, (name, details) in enumerate(rezeptbuch.items()):
                stdscr.addstr(17 + idx, 4, f"{name} | {details['materialien']} | Qualität: {details['qualitaet']}% | Gebraut: {details['anzahl']}x")
        else:
            stdscr.addstr(17, 4, "(Keine Rezepte gespeichert)", curses.A_DIM)

    def verarbeite_trank(ausgewaehlte_materialien):
        nonlocal aktuelle_xp, level, xp_bis_naechstes_level, muenzen, doppel_xp_zaehler, kesselabnutzung

        for kombination in gueltige_kombinationen:
            if sorted(ausgewaehlte_materialien) == sorted(kombination["materialien"]):
                qualitaet = random.randint(*kombination["qualitaet_spanne"])
                xp_gewonnen = round(10 + qualitaet / 5)
                if doppel_xp_zaehler > 0:
                    xp_gewonnen *= 2
                    doppel_xp_zaehler -= 1
                if qualitaet == 100: doppel_xp_zaehler = 5

                aktuelle_xp += xp_gewonnen
                if aktuelle_xp >= xp_bis_naechstes_level:
                    aktuelle_xp -= xp_bis_naechstes_level
                    level += 1
                    xp_bis_naechstes_level = int(xp_bis_naechstes_level * 1.5)

                muenzen += 5 + (qualitaet // 10)
                kesselabnutzung -= random.randint(3, 5)

                if kombination["name"] not in rezeptbuch:
                    rezeptbuch[kombination["name"]] = {"materialien": kombination["materialien"], "qualitaet": qualitaet, "anzahl": 1}
                else:
                    if rezeptbuch[kombination["name"]]["qualitaet"] < qualitaet:
                        rezeptbuch[kombination["name"]]["qualitaet"] = qualitaet
                    rezeptbuch[kombination["name"]]["anzahl"] += 1

                return f"Erfolgreich! {kombination['name']} - Qualität: {qualitaet}% (+{xp_gewonnen} XP, +{muenzen} Münzen)"

        # Wenn der Trank nicht erfolgreich ist, verringern wir die Kesselabnutzung
        kesselabnutzung -= random.randint(6, 12)
        if kesselabnutzung < 0:
            kesselabnutzung = 0

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

    def spiel_schleife():
        ausgewaehlte_materialien = []
        scroll_offset = 0

        while True:
            stdscr.clear()
            zeichne_progress_bar()
            zeichne_seitenleiste(scroll_offset)
            zeichne_kessel_bereich(ausgewaehlte_materialien)
            zeichne_rezeptbuch()
            stdscr.addstr(20, 2, f"Münzen: {muenzen}", curses.A_BOLD)
            stdscr.addstr(21, 2, "Drücke [ENTER], um einen Trank zu brauen.", curses.A_BOLD)
            stdscr.addstr(22, 2, "Drücke [S], um den Shop zu öffnen.", curses.A_BOLD)
            stdscr.addstr(23, 2, "Drücke [Q], um das Spiel zu beenden.", curses.A_BOLD)

            key = stdscr.getch()
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
