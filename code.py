import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_macropad import MacroPad

# Ajout des bibliothèques nécessaires pour l'affichage à l'écran du MacroPad
import displayio
import terminalio
from adafruit_display_text import label

# Initialisation du MacroPad et du module MIDI USB
macropad = MacroPad()
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# Liste des notes MIDI associées aux touches du MacroPad.
# Chaque touche correspond à une note de l’échelle musicale.
MIDI_NOTES = [36, 43, 48, 52, 55, 60, 64, 67, 72, 76, 79, 84]


# Configuration de l'affichage sur l’écran du MacroPad
macropad.display.auto_refresh = False  # Désactivation du rafraîchissement automatique
group = displayio.Group()  # Création d'un groupe d'affichage

# Création d'une zone de texte pour afficher la note jouée
text_area = label.Label(terminalio.FONT, text="Appuie sur une touche !", color=0xFFFFFF)
text_area.anchor_point = (0.5, 0.5)  # Positionnement au centre de l'écran
text_area.anchored_position = (macropad.display.width // 2, macropad.display.height // 2)

# Ajout du texte au groupe d'affichage et mise à jour de l'écran
group.append(text_area)
macropad.display.root_group = group
macropad.display.refresh()

while True:
    # Vérifie si une touche a été pressée ou relâchée
    key_event = macropad.keys.events.get()
    if key_event:
        key_index = key_event.key_number  # Récupère l'index de la touche

        if key_event.pressed and key_index < len(MIDI_NOTES):
            note = MIDI_NOTES[key_index]  # Récupère la note MIDI associée
            midi.send(NoteOn(note, 127))  # Envoie un signal MIDI "Note On" avec vélocité max
            text_area.text = f"Note: {note}"  # Met à jour l'affichage avec la note jouée
            macropad.display.refresh()  # Rafraîchit l'affichage

        elif key_event.released and key_index < len(MIDI_NOTES):
            note = MIDI_NOTES[key_index]  # Récupère la note MIDI associée
            midi.send(NoteOff(note, 0))  # Envoie un signal MIDI "Note Off" pour arrêter la note
            text_area.text = "Appuie sur une touche !"  # Réinitialise l'affichage
            macropad.display.refresh()  # Rafraîchit l'affichage

    time.sleep(0.01)  # Légère pause pour éviter une boucle trop rapide
