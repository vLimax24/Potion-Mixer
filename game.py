import pygame
import os
import random
from pygame._sdl2 import Window

# Pygame initialisieren
pygame.init()

# Bildschirmkonfiguration (Vollbild)
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Zaubertrank Simulator")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (93, 0, 124, 190)
DARK_PURPLE = (40, 0, 60)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)

# Schriftarten
pygame.font.init()
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 48)

# Hintergrundbild laden
def load_background():
    bg_path = os.path.join(os.path.dirname(__file__), 'hintergrund.jpg')
    return pygame.transform.scale(pygame.image.load(bg_path), (SCREEN_WIDTH, SCREEN_HEIGHT))

background = load_background()

# Materialeigenschaften
materials = [
    {"name": "Feuerblume", "color": (255, 0, 0)},
    {"name": "Eisblume", "color": (0, 255, 255)},
    {"name": "Schattenblatt", "color": (0, 100, 0)},
    {"name": "Sonnenstein", "color": (255, 215, 0)},
    {"name": "Nebelstein", "color": (169, 169, 169)}
]

# Kombinationslogik
valid_combinations = [
    {"materials": ["Feuerblume", "Eisblume"], "quality_range": (70, 90)},
    {"materials": ["Schattenblatt", "Sonnenstein"], "quality_range": (50, 80)},
    {"materials": ["Nebelstein", "Feuerblume"], "quality_range": (30, 60)}
]

# Spielvariablen
selected_materials = []
clicks_required = 0
clicks_made = 0
current_potion = None
recipe_book = []

# Positionen
MATERIAL_SIZE = 80
SIDEBAR_WIDTH = 300
cauldron_pos = (SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 75)
cauldron_rect = pygame.Rect(*cauldron_pos, 150, 150)
recipe_button_rect = pygame.Rect(SCREEN_WIDTH - 200, 20, 150, 50)

# Liste der Material-Rechtecke
material_rects = []

# Funktionen
def draw_sidebar():
    sidebar_rect = pygame.Rect(0, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT)
    s = pygame.Surface((SIDEBAR_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    s.fill(PURPLE)
    screen.blit(s, (0, 0))
    y_offset = 50
    material_rects.clear()  # Rechtecke zurücksetzen
    for material in materials:
        rect = pygame.Rect(20, y_offset, MATERIAL_SIZE, MATERIAL_SIZE)
        material_rects.append((rect, material["name"]))  # Rechteck und Materialname speichern
        pygame.draw.ellipse(screen, material["color"], rect)
        text = font.render(material["name"], True, WHITE)
        screen.blit(text, (20, y_offset + MATERIAL_SIZE + 10))
        y_offset += MATERIAL_SIZE + 40

def draw_level_bar():
    level_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 20, 400, 30)
    pygame.draw.rect(screen, DARK_PURPLE, level_rect)
    pygame.draw.rect(screen, GOLD, (level_rect.x, level_rect.y, 300, 30))  # Fortschritt
    text = font.render("15", True, WHITE)
    screen.blit(text, (level_rect.x - 30, level_rect.y))
    text = font.render("16", True, WHITE)
    screen.blit(text, (level_rect.x + level_rect.width + 10, level_rect.y))

def draw_added_materials():
    overlay_width, overlay_height = 300, 150
    overlay_rect = pygame.Rect(SCREEN_WIDTH // 2 - overlay_width // 2, cauldron_pos[1] - 180, overlay_width,
                               overlay_height)

    # Hintergrund des Overlays
    pygame.draw.rect(screen, PURPLE[:-1], overlay_rect, border_radius=10)
    title = font.render("Hinzugefügte Materialien:", True, WHITE)
    screen.blit(title, (overlay_rect.x + 10, overlay_rect.y + 10))

    # Materialien anzeigen
    x_offset = overlay_rect.x + 30
    y_offset = overlay_rect.y + 50
    for i, material_name in enumerate(selected_materials):
        material_color = next(item["color"] for item in materials if item["name"] == material_name)
        pygame.draw.circle(screen, material_color, (x_offset + i * 70, y_offset), 30)
        text = font.render(material_name, True, WHITE)
        screen.blit(text, (x_offset + i * 70 - 40, y_offset + 40))

def draw_recipe_button():
    pygame.draw.rect(screen, PURPLE[:-1], recipe_button_rect, border_radius=10)
    text = font.render("Rezeptbuch", True, WHITE)
    screen.blit(text, (recipe_button_rect.x + 15, recipe_button_rect.y + 10))

def draw_cauldron():
    pygame.draw.ellipse(screen, GRAY, cauldron_rect)
    pygame.draw.ellipse(screen, DARK_PURPLE, cauldron_rect, 5)
    text = font.render("Hexenkessel", True, GOLD)
    screen.blit(text, (cauldron_pos[0] + 20, cauldron_pos[1] + 160))

def draw_recipe_book():
    book_rect = pygame.Rect(200, 50, SCREEN_WIDTH - 400, SCREEN_HEIGHT - 100)
    pygame.draw.rect(screen, BLACK, book_rect, border_radius=15)
    pygame.draw.rect(screen, GOLD, book_rect, 5, border_radius=15)
    title = title_font.render("Rezeptbuch", True, GOLD)
    screen.blit(title, (book_rect.x + 20, book_rect.y + 20))
    for i, (combo, quality) in enumerate(recipe_book):
        text = font.render(f"{', '.join(combo)} | Qualität: {quality}%", True, WHITE)
        screen.blit(text, (book_rect.x + 20, book_rect.y + 80 + i * 40))

# Interaktionen
def cauldron_interaction(pos):
    return cauldron_rect.collidepoint(pos)

show_recipe_book = False
running = True
while running:
    screen.blit(background, (0, 0))
    draw_sidebar()
    draw_level_bar()
    draw_recipe_button()
    draw_cauldron()
    draw_added_materials()

    # Rezeptbuch anzeigen
    if show_recipe_book:
        draw_recipe_book()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Material in Sidebar ausgewählt
            for rect, material_name in material_rects:
                if rect.collidepoint(event.pos):
                    if len(selected_materials) < 2:
                        selected_materials.append(material_name)
                        print("Material hinzugefügt:", selected_materials)
            # Hexenkessel-Interaktion
            if cauldron_interaction(event.pos):
                if len(selected_materials) == 2 and clicks_required == 0:
                    clicks_required = random.randint(5, 10)
                    clicks_made = 0
                if clicks_required > 0:
                    clicks_made += 1
                    if clicks_made >= clicks_required:
                        for combo in valid_combinations:
                            if set(selected_materials) == set(combo["materials"]):
                                quality = random.randint(*combo["quality_range"])
                                recipe_book.append((selected_materials.copy(), quality))
                                print("Trank erfolgreich! Qualität:", quality)
                                break
                        else:
                            print("Trank fehlgeschlagen!")
                        selected_materials = []
                        clicks_required = 0
                        clicks_made = 0
            # Rezeptbuch-Button
            if recipe_button_rect.collidepoint(event.pos):
                show_recipe_book = not show_recipe_book
    pygame.display.flip()

pygame.quit()

