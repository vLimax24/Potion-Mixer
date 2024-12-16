import curses
import random


def main(stdscr):
    # Terminal setup
    curses.curs_set(0)
    stdscr.clear()
    curses.start_color()

    # Initialize colors
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  # Feuerblume
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Eisblume
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Schattenblatt
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Sonnenstein
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Nebelstein
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Wasserkranz
    curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Erdenfrucht
    curses.init_pair(8, curses.COLOR_RED, curses.COLOR_WHITE)  # Sturmessenz
    curses.init_pair(9, curses.COLOR_BLUE, curses.COLOR_WHITE)  # Mondblüte
    curses.init_pair(10, curses.COLOR_YELLOW, curses.COLOR_WHITE)  # Sternenstaub

    # Materials and combinations
    materials = [
        {"name": "Feuerblume", "color": 1},
        {"name": "Eisblume", "color": 2},
        {"name": "Schattenblatt", "color": 3},
        {"name": "Sonnenstein", "color": 4},
        {"name": "Nebelstein", "color": 5},
        {"name": "Wasserkranz", "color": 6},
        {"name": "Erdenfrucht", "color": 7},
        {"name": "Sturmessenz", "color": 8},
        {"name": "Mondblüte", "color": 9},
        {"name": "Sternenstaub", "color": 10},
    ]

    available_materials = materials[:4]
    locked_materials = materials[4:]

    valid_combinations = [
        # Zweierkombinationen
        {"name": "Flammenfrost-Trank", "materials": ["Feuerblume", "Eisblume"], "quality_range": (0, 100)},
        {"name": "Schattenlicht-Elixier", "materials": ["Schattenblatt", "Sonnenstein"], "quality_range": (0, 100)},
        {"name": "Nebelbrand-Trank", "materials": ["Nebelstein", "Feuerblume"], "quality_range": (0, 100)},
        {"name": "Lebensessenz", "materials": ["Wasserkranz", "Erdenfrucht"], "quality_range": (0, 100)},
        {"name": "Sturm der Schatten", "materials": ["Sturmessenz", "Schattenblatt"], "quality_range": (0, 100)},
        {"name": "Sonnentau-Trank", "materials": ["Sonnenstein", "Wasserkranz"], "quality_range": (0, 100)},

        # Dreierkombinationen
        {"name": "Inferno-Eislicht", "materials": ["Feuerblume", "Eisblume", "Sonnenstein"], "quality_range": (0, 100)},
        {"name": "Nebelflut-Elixier", "materials": ["Nebelstein", "Sturmessenz", "Erdenfrucht"],
         "quality_range": (0, 100)},
        {"name": "Wasserfrost-Schatten", "materials": ["Wasserkranz", "Eisblume", "Schattenblatt"],
         "quality_range": (0, 100)},
        {"name": "Sonnenflammen-Sturm", "materials": ["Sonnenstein", "Feuerblume", "Sturmessenz"],
         "quality_range": (0, 100)},
        {"name": "Erdige Nebelschatten", "materials": ["Erdenfrucht", "Nebelstein", "Schattenblatt"],
         "quality_range": (0, 100)},
        {"name": "Wassersturm-Feuer", "materials": ["Wasserkranz", "Feuerblume", "Sturmessenz"],
         "quality_range": (0, 100)},
    ]

    recipe_book = {}

    # Level, XP, Coins
    level = 1
    current_xp = 0
    xp_to_next_level = 100
    coins = 20
    double_xp_counter = 0  # Tracks remaining double XP brews
    hint_price = 10  # Base price for hints
    unlock_price = 20  # Base price for unlocking new materials

    def draw_progress_bar():
        """Draws the progress bar for XP."""
        bar_width = 20
        filled_length = int(bar_width * current_xp / xp_to_next_level)
        bar = "█" * filled_length + "-" * (bar_width - filled_length)
        stdscr.addstr(1, 50, f"Level {level} | XP: {current_xp}/{xp_to_next_level}")
        stdscr.addstr(2, 50, f"[{bar}]")

    def draw_sidebar(scroll_offset=0):
        stdscr.addstr(4, 2, "Materialien:", curses.color_pair(6))
        visible_materials = available_materials[scroll_offset:scroll_offset + 7]
        for idx, material in enumerate(visible_materials):
            color = curses.color_pair(material["color"])
            stdscr.addstr(6 + idx, 4, f"{scroll_offset + idx + 1}. {material['name']}", color)

        if scroll_offset > 0:
            stdscr.addstr(5, 4, "↑", curses.A_BOLD)
        if scroll_offset + 7 < len(available_materials):
            stdscr.addstr(13, 4, "↓", curses.A_BOLD)

    def draw_potion_area(selected_materials):
        stdscr.addstr(4, 30, "Hexenkessel:", curses.color_pair(6))
        for idx, material in enumerate(selected_materials):
            color = curses.color_pair(next(m["color"] for m in materials if m["name"] == material))
            stdscr.addstr(6 + idx, 32, material, color)

    def draw_recipe_book():
        stdscr.addstr(10, 2, "Rezeptbuch:", curses.color_pair(6))
        if not recipe_book:
            stdscr.addstr(12, 4, "(Keine Rezepte gespeichert)", curses.A_DIM)
        else:
            for idx, (name, details) in enumerate(recipe_book.items()):
                materials = details["materials"]
                quality = details["quality"]
                count = details["count"]
                stdscr.addstr(12 + idx, 4, f"{name} | {materials} | Qualität: {quality}% | Gebraut: {count}x")

    def process_potion(selected_materials):
        """
        Processes the selected materials and checks for an exact match in valid combinations.
        """
        nonlocal current_xp, level, xp_to_next_level, coins, double_xp_counter

        for combo in valid_combinations:
            # Check if materials exactly match a valid recipe (both content and order)
            if sorted(selected_materials) == sorted(combo["materials"]):
                quality = random.randint(*combo["quality_range"])
                name = combo["name"]

                base_xp = 10
                xp_gained = base_xp + quality
                if double_xp_counter > 0:
                    xp_gained *= 2
                    double_xp_counter -= 1

                # Double XP bonus for 100% quality
                if quality == 100:
                    double_xp_counter = 5

                # Add XP and check for level up
                current_xp += xp_gained
                if current_xp >= xp_to_next_level:
                    current_xp -= xp_to_next_level
                    level += 1
                    xp_to_next_level = int(xp_to_next_level * 1.5)  # Increase XP requirement

                # Coins reward: base coins + quality-based increment
                coins_gained = 5 + (quality // 10)
                coins += coins_gained

                if name not in recipe_book:
                    # Initialize recipe entry with materials, quality, and count
                    recipe_book[name] = {"materials": combo["materials"], "quality": quality, "count": 1}
                else:
                    if recipe_book[name]["quality"] < quality:
                        recipe_book[name]["quality"] = quality  # Update quality if better
                    recipe_book[name]["count"] += 1  # Increment count

                return f"Erfolgreich! {name} - Qualität: {quality}% (+{xp_gained} XP, +{coins_gained} Münzen)"

        # If no match, return failure message
        return "Fehlgeschlagen!"

    def shop():
        """Displays the shop and allows the player to purchase hints or unlock materials."""
        nonlocal coins, hint_price, unlock_price, locked_materials
        while True:
            stdscr.clear()
            stdscr.addstr(2, 2, f"Shop ({coins} Münzen verfügbar):", curses.color_pair(6))
            stdscr.addstr(4, 4, f"1. Rezept-Hinweis kaufen ({hint_price} Münzen)")
            if locked_materials:
                stdscr.addstr(5, 4, f"2. Neues Material freischalten ({unlock_price} Münzen)")
            else:
                stdscr.addstr(5, 4, "(Alle Materialien freigeschaltet!)", curses.A_DIM)
            stdscr.addstr(7, 2, "Drücke 'q', um zurückzukehren.")

            key = stdscr.getch()
            if key == ord('q'):
                break
            elif key == ord('1'):
                # Get valid hints for owned materials
                valid_hints = [
                    combo for combo in valid_combinations
                    if all(mat in [m["name"] for m in available_materials] for mat in combo["materials"])
                ]
                if coins >= hint_price and valid_hints:
                    coins -= hint_price
                    hint = random.choice(valid_hints)
                    partial_hint = hint["materials"][:-1] + ["..."]  # Hide the last material
                    stdscr.addstr(9, 4, f"Tipp: {partial_hint}", curses.A_BOLD)
                    hint_price += 5  # Hints become progressively more expensive
                elif not valid_hints:
                    stdscr.addstr(9, 4, "Keine Rezepte verfügbar, die du mit deinen Materialien brauen kannst.",
                                  curses.A_BOLD)
                else:
                    stdscr.addstr(9, 4, "Nicht genug Münzen!", curses.A_BOLD)
                stdscr.refresh()
                stdscr.getch()
            elif key == ord('2') and locked_materials:
                if coins >= unlock_price:
                    coins -= unlock_price
                    new_material = locked_materials.pop(0)
                    available_materials.append(new_material)
                    stdscr.addstr(9, 4, f"Neues Material freigeschaltet: {new_material['name']}!", curses.A_BOLD)
                    unlock_price += 10  # Unlocking materials becomes more expensive
                else:
                    stdscr.addstr(9, 4, "Nicht genug Münzen!", curses.A_BOLD)
                stdscr.refresh()
                stdscr.getch()

    def game_loop():
        selected_materials = []
        scroll_offset = 0

        while True:
            stdscr.clear()
            draw_progress_bar()
            draw_sidebar(scroll_offset)
            draw_potion_area(selected_materials)
            draw_recipe_book()
            stdscr.addstr(20, 2, f"Münzen: {coins}", curses.A_BOLD)
            stdscr.addstr(21, 2, "Drücke 'c', um einen Trank zu brauen.", curses.A_BOLD)
            stdscr.addstr(22, 2, "Drücke 's', um den Shop zu öffnen.", curses.A_BOLD)
            stdscr.addstr(23, 2, "Drücke 'q', um das Spiel zu beenden.", curses.A_BOLD)


            key = stdscr.getch()
            if key == ord('q'):
                break
            elif key == ord('s'):
                shop()
            elif ord('1') <= key <= ord(str(min(len(available_materials), 9))):
                material_idx = key - ord('1')
                if len(selected_materials) < 3:
                    selected_materials.append(available_materials[material_idx]["name"])
            elif key in [ord('c')]:
                if selected_materials:
                    result = process_potion(selected_materials)
                    selected_materials.clear()
                    stdscr.addstr(24, 2, result, curses.A_BOLD)
                    stdscr.refresh()
                    stdscr.getch()
            elif key == curses.KEY_DOWN:
                if scroll_offset < max(0, len(materials) - 7):
                    scroll_offset += 1
            elif key == curses.KEY_UP:
                if scroll_offset > 0:
                    scroll_offset -= 1

    game_loop()


curses.wrapper(main)