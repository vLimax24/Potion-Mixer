import matplotlib.pyplot as plt
import numpy as np

# Funktion zum Erzeugen eines Grids mit farbigen Zellen basierend auf einem Elementtyp
def generate_unique_pattern(element_type, size=(10, 10)):
    np.random.seed(hash(element_type) % (2**32))  # Seed basierend auf Elementtyp
    pattern = np.zeros(size + (3,), dtype=np.uint8)  # RGB-Muster initialisieren

    if element_type == "Feuer":
        base_color = [255, 0, 0]  # Rot
        color_variations = [[255, 69, 0], [255, 99, 71], [255, 165, 0]]  # Rottöne und Orange
    elif element_type == "Frost":
        base_color = [0, 0, 255]  # Blau
        color_variations = [[0, 191, 255], [135, 206, 250], [173, 216, 230]]  # Blautöne und Cyan
    elif element_type == "Natur":
        base_color = [0, 128, 0]  # Grün
        color_variations = [[34, 139, 34], [50, 205, 50], [107, 142, 35]]  # Grüntöne und Olivgrün
    else:
        base_color = [128, 128, 128]  # Grau für unbekannte Typen
        color_variations = [[169, 169, 169], [192, 192, 192], [211, 211, 211]]

    # Grid mit zufälligen Farben aus den Variationen füllen
    for i in range(size[0]):
        for j in range(size[1]):
            if np.random.rand() > 0.3:  # Wahrscheinlich primäre Farbe
                pattern[i, j, :] = base_color
            else:  # Zufällige Sekundärfarben
                pattern[i, j, :] = color_variations[np.random.randint(len(color_variations))]

    return pattern

# Funktion, um ein Muster anzuzeigen
def show_pattern(pattern, title):
    plt.figure(figsize=(4, 4))
    plt.imshow(pattern)
    plt.axis("off")  # Achsen ausblenden
    plt.title(title)
    plt.show()

# Elemente und ihre Typen definieren
elements = ["Feuer", "Frost", "Natur", "Feuer", "Frost"]

# Muster generieren und anzeigen
for i, element in enumerate(elements):
    pattern = generate_unique_pattern(element)
    show_pattern(pattern, title=f"Muster {i+1}: {element}")
