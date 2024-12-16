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


def braue_trank(mischung):
    # Umwandlung der Eingabe in eine Liste
    zutaten = [zutat.strip() for zutat in mischung.split(",")]

    # Überprüfen, ob eine Kombination existiert
    passende_tränke = []
    for trank_name, trank in tränke.items():
        if set(zutaten) == set(trank["zutaten"]):
            passende_tränke.append(trank_name)

    # Ausgabe der passenden Tränke
    if passende_tränke:
        print("Mit diesen Zutaten kannst du folgenden Trank brauen:")
        for trank in passende_tränke:
            print(f"- {trank}: {tränke[trank]['wirkung']}")
    else:
        print("Es gibt keinen Trank, der mit diesen Zutaten gemischt werden kann.")


# Benutzer nach Zutaten fragen
user_input = input("Gib die Zutaten im Format 'Material1, Material2' ein: ")
braue_trank(user_input)
