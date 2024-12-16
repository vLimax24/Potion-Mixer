import pygame
import random

# Initialisierung von Pygame
pygame.init()

# Bildschirmkonfiguration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zaubertrank Simulator")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Materialeigenschaften
materials = [
    {"name": "Feuerbeere", "color": RED},
    {"name": "Frostkristall", "color": BLUE},
    {"name": "Naturblatt", "color": GREEN},
    {"name": "Sonnenblume", "color": ORANGE},
    {"name": "Nebelstein", "color": GRAY}
]

# Kombinationslogik
valid_combinations = [
    {"materials": ["Feuerbeere", "Frostkristall"], "quality_range": (70, 90)},
    {"materials": ["Naturblatt", "Sonnenblume"], "quality_range": (50, 80)},
    {"materials": ["Nebelstein", "Feuerbeere"], "quality_range": (30, 60)}
]

# Spielvariablen
selected_materials = []
clicks_required = 0
clicks_made = 0
current_potion = None

# Schriftarten
font = pygame.font.Font(None, 36)

# Materialregalpositionen
material_positions = [(50 + i * 150, 50) for i in range(len(materials))]

# Kesselposition
cauldron_pos = (SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 75)

# Funktion zum Rendern von Text
def render_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Hauptspielschleife
running = True
while running:
    screen.fill(WHITE)

    # Materialien anzeigen
    for i, material in enumerate(materials):
        pygame.draw.rect(screen, material["color"], (*material_positions[i], 100, 100))
        render_text(material["name"], material_positions[i][0] - 20, material_positions[i][1] + 110)

    # Hexenkessel anzeigen
    pygame.draw.ellipse(screen, GRAY, (*cauldron_pos, 150, 150))
    render_text("Hexenkessel", cauldron_pos[0] + 10, cauldron_pos[1] + 160)

    # Kesselinhalt anzeigen
    if selected_materials:
        render_text(f"Inhalt: {', '.join(selected_materials)}", 50, SCREEN_HEIGHT - 100)

    # Fortschritt beim Brauen anzeigen
    if clicks_required > 0:
        render_text(f"Klicke den Kessel: {clicks_made}/{clicks_required}", 50, SCREEN_HEIGHT - 60)

    # Potion-Status anzeigen
    if current_potion:
        if current_potion == "failure":
            render_text("Brauen fehlgeschlagen!", 500, SCREEN_HEIGHT - 100, RED)
        else:
            render_text(f"Erfolgreicher Trank mit Qualität: {current_potion}%", 200, SCREEN_HEIGHT - 150, GREEN)

    # Ereignisse verarbeiten
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Materialien auswählen
            for i, material in enumerate(materials):
                rect = pygame.Rect(*material_positions[i], 100, 100)
                if rect.collidepoint(mouse_pos):
                    if len(selected_materials) < 2:
                        selected_materials.append(material["name"])

            # Kessel klicken
            cauldron_rect = pygame.Rect(*cauldron_pos, 150, 150)
            if cauldron_rect.collidepoint(mouse_pos):
                if selected_materials and clicks_required == 0:
                    clicks_required = random.randint(5, 10)
                    clicks_made = 0
                    current_potion = None

                if clicks_required > 0:
                    clicks_made += 1

                    if clicks_made >= clicks_required:
                        # Prüfen, ob die Kombination gültig ist
                        for combo in valid_combinations:
                            if set(selected_materials) == set(combo["materials"]):
                                quality = random.randint(*combo["quality_range"])
                                current_potion = quality
                                break

                        # Wenn keine gültige Kombination gefunden wurde
                        if not current_potion:
                            current_potion = "failure"

                        # Zurücksetzen
                        selected_materials = []
                        clicks_required = 0

    # Bildschirm aktualisieren
    pygame.display.flip()

# Spiel beenden
pygame.quit()
