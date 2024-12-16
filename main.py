import tkinter as tk
from tkinter import messagebox

zutaten = [
    {"name": "Heilkräuter", "wirkung": "heilen", "kraft": 20},
    {"name": "Feuerblume", "wirkung": "schaden", "kraft": 10},
    {"name": "Eiswasser", "wirkung": "frost", "kraft": 15},
    {"name": "Lavendel", "wirkung": "entspannen", "kraft": 10},
    {"name": "Blutmondbeere", "wirkung": "stärkung", "kraft": 25},
    {"name": "Dunkelpilz", "wirkung": "schaden", "kraft": 30},
    {"name": "Wassergeist-Essenz", "wirkung": "heilung", "kraft": 35}
]

tränke = {
    "Heiltrank": {
        "zutaten": ["Heilkräuter", "Wassergeist-Essenz"],
        "wirkung": "Heilt den Träger um 50 Lebenspunkte."
    },
    "Feuertrank": {
        "zutaten": ["Feuerblume", "Dunkelpilz"],
        "wirkung": "Verursacht 40 Schaden (Feuer- und Gift-Effekt)."
    },
    "Frosttrank": {
        "zutaten": ["Eiswasser", "Lavendel"],
        "wirkung": "Verlangsamt Gegner für 3 Runden und heilt den Träger um 20 Lebenspunkte."
    },
    "Stärketrank": {
        "zutaten": ["Blutmondbeere", "Lavendel"],
        "wirkung": "Erhöht die Angriffskraft des Trägers für 5 Runden."
    },
    "Lavaschaden-Trank": {
        "zutaten": ["Feuerblume", "Blutmondbeere"],
        "wirkung": "Verursacht 50 Feuerschaden und verstärkt den Angriff des Trägers für 2 Runden."
    },
    "Schattentrank": {
        "zutaten": ["Dunkelpilz", "Eiswasser"],
        "wirkung": "Verursacht 30 Schaden und verlangsamt den Gegner."
    },
    "Regenerationstrank": {
        "zutaten": ["Heilkräuter", "Lavendel"],
        "wirkung": "Stellt 40 Lebenspunkte wieder her und lindert Erschöpfung."
    },
    "Gifttrank": {
        "zutaten": ["Dunkelpilz", "Blutmondbeere"],
        "wirkung": "Verursacht über 3 Runden hinweg 10 Gift-Schaden pro Runde an einem Gegner."
    },
    "Verlangsamungstrank": {
        "zutaten": ["Eiswasser", "Lavendel"],
        "wirkung": "Verlangsamt den Gegner für 5 Runden und heilt den Träger um 15 Lebenspunkte."
    },
    "Krafttrank": {
        "zutaten": ["Blutmondbeere", "Wassergeist-Essenz"],
        "wirkung": "Erhöht die Angriffskraft des Trägers und heilt ihn um 30 Lebenspunkte."
    },
    "Feuerschutztrank": {
        "zutaten": ["Feuerblume", "Wassergeist-Essenz"],
        "wirkung": "Gewährt dem Träger für 3 Runden Feuerschutz, der 50% des eingehenden Feuerschadens blockiert."
    },
    "Eisschild-Trank": {
        "zutaten": ["Eiswasser", "Dunkelpilz"],
        "wirkung": "Erzeugt ein Schild, das 40 Schaden abwehrt, und fügt dem Gegner 10 Eisschaden zu."
    },
    "Nachttrank": {
        "zutaten": ["Dunkelpilz", "Lavendel"],
        "wirkung": "Macht den Träger für 3 Runden unsichtbar und heilt ihn um 20 Lebenspunkte."
    },
    "Schlaftrank": {
        "zutaten": ["Heilkräuter", "Lavendel"],
        "wirkung": "Versetzt den Gegner in Schlaf für 2 Runden und heilt den Träger um 15 Lebenspunkte."
    },
    "Wassertrank": {
        "zutaten": ["Wassergeist-Essenz", "Heilkräuter"],
        "wirkung": "Stellt 40 Lebenspunkte des Trägers wieder her und erhöht seine Ausdauer."
    },
    "Dunkelheits-Trank": {
        "zutaten": ["Dunkelpilz", "Eiswasser", "Lavendel"],
        "wirkung": "Verursacht 20 Schaden und reduziert die Sicht des Gegners für 3 Runden."
    },
    "Blutflammentrank": {
        "zutaten": ["Feuerblume", "Blutmondbeere", "Dunkelpilz"],
        "wirkung": "Verursacht 60 Feuerschaden und 20 Gift-Schaden an einem Gegner."
    },
    "Frostbiss-Trank": {
        "zutaten": ["Eiswasser", "Blutmondbeere"],
        "wirkung": "Verursacht 30 Frostschaden und reduziert die Beweglichkeit des Gegners."
    },
    "Lebensschutztrank": {
        "zutaten": ["Wassergeist-Essenz", "Lavendel"],
        "wirkung": "Schützt den Träger für 2 Runden vor Schaden und heilt ihn um 30 Lebenspunkte."
    },
    "Kraftfeld-Trank": {
        "zutaten": ["Blutmondbeere", "Eiswasser", "Heilkräuter"],
        "wirkung": "Erhöht die Verteidigung des Trägers und heilt ihn gleichzeitig um 25 Lebenspunkte."
    },
    "Rasender Sturmtrank": {
        "zutaten": ["Feuerblume", "Eiswasser", "Blutmondbeere"],
        "wirkung": "Verursacht 40 Feuerschaden, 20 Frostschaden und erhöht die Angriffsgeschwindigkeit des Trägers für 3 Runden."
    },
    "Heiliger Trank": {
        "zutaten": ["Heilkräuter", "Blutmondbeere", "Wassergeist-Essenz"],
        "wirkung": "Heilt 50 Lebenspunkte und gewährt dem Träger für 2 Runden zusätzliche Regeneration."
    },
    "Verwandlungstrank": {
        "zutaten": ["Dunkelpilz", "Lavendel", "Wassergeist-Essenz"],
        "wirkung": "Verwandelt den Träger für 3 Runden in eine andere Kreatur, was seine Eigenschaften verändert."
    }
}


# Funktion, um einen Trank zu brauen
def braue_trank():
    # Abrufen der ausgewählten Zutaten (nur den Namen der Zutat verwenden)
    ausgewählte_zutaten = []
    for zutat_dict in zutaten:
        if zutaten_checkbuttons[zutat_dict["name"]].get() == 1:
            ausgewählte_zutaten.append(zutat_dict["name"])

    # Überprüfen, ob eine Kombination existiert
    passende_tränke = []
    for trank_name, trank in tränke.items():
        if set(ausgewählte_zutaten) == set(trank["zutaten"]):
            passende_tränke.append(trank_name)

    # Ausgabe der passenden Tränke
    if passende_tränke:
        trank_ausgabe = "\n".join(f"{trank}: {tränke[trank]['wirkung']}" for trank in passende_tränke)
        messagebox.showinfo("Passende Tränke",
                            f"Mit diesen Zutaten kannst du folgenden Trank brauen:\n\n{trank_ausgabe}")
    else:
        messagebox.showinfo("Kein passender Trank",
                            "Es gibt keinen Trank, der mit diesen Zutaten gemischt werden kann.")


# GUI-Erstellung
root = tk.Tk()
root.title("Zaubertrank Brauen")

# Überschrift
label = tk.Label(root, text="Wähle Zutaten für deinen Trank aus:", font=("Helvetica", 14))
label.pack(pady=10)

# Erstellen der Checkbuttons für Zutaten
zutaten_checkbuttons = {}
for zutat_dict in zutaten:
    # Nur den Namen der Zutat als Schlüssel verwenden
    zutaten_checkbuttons[zutat_dict["name"]] = tk.IntVar()
    checkbutton = tk.Checkbutton(root, text=zutat_dict["name"], variable=zutaten_checkbuttons[zutat_dict["name"]])
    checkbutton.pack(anchor="w")

# Brau-Button
brau_button = tk.Button(root, text="Brau einen Trank!", command=braue_trank)
brau_button.pack(pady=20)

# Starten der GUI
root.mainloop()
