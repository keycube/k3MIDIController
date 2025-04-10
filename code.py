import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.program_change import ProgramChange
from adafruit_macropad import MacroPad

# Bibliothèques pour l'affichage
import displayio
import terminalio
from adafruit_display_text import label

# Initialisation du MacroPad et MIDI
macropad = MacroPad()
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# Liste des notes MIDI
MIDI_NOTES = [84, 79, 76, 72, 69, 65, 62, 60, 57, 55, 52, 48]

# Dictionnaire des instruments disponibles avec leurs noms et numéros MIDI
INSTRUMENTS = [
    ("Piano Electrique", 2),      # 0:2
    ("Piano Rhodes", 4),     # 0:4
    ("Guitare Classique", 24), # 0:24
    ("Violon", 40),          # 0:40
    ("Trompette", 56),       # 0:56
    ("Sax Ténor", 66),       # 0:66
    ("Flûte", 73),           # 0:73
    ("Cordes", 48),          # 0:48
    ("Harpe", 46),           # 0:46
    ("Synth Lead", 80),      # 0:80
    ("Sitar", 104),          # 0:104
    ("Kalimba", 108)         # 0:108
]

current_instrument_index = 0  # Index de l'instrument actuel
current_instrument = INSTRUMENTS[current_instrument_index]

# Configuration de l'affichage
macropad.display.auto_refresh = False
group = displayio.Group()

# Zone de texte pour l'instrument
instrument_area = label.Label(terminalio.FONT, text=current_instrument[0], color=0xFFFFFF)
instrument_area.anchor_point = (0.5, 0.5)
instrument_area.anchored_position = (macropad.display.width // 2, macropad.display.height // 2)

group.append(instrument_area)
macropad.display.root_group = group
macropad.display.refresh()

# Envoi du premier instrument
midi.send(ProgramChange(current_instrument[1]))

# Variables pour le curseur
last_position = macropad.encoder
debounce_time = 0.1
last_change = time.monotonic()

while True:
    # Gestion des touches
    key_event = macropad.keys.events.get()

    if key_event:
        key_index = key_event.key_number

        if key_event.pressed and key_index < len(MIDI_NOTES):
            note = MIDI_NOTES[key_index]
            midi.send(NoteOn(note, 127))
            instrument_area.text = f"{current_instrument[0]}:{note}"
            macropad.display.refresh()

        elif key_event.released and key_index < len(MIDI_NOTES):
            note = MIDI_NOTES[key_index]
            midi.send(NoteOff(note, 0))
            instrument_area.text = current_instrument[0]
            macropad.display.refresh()

    # Gestion du curseur pour changer d'instrument
    current_position = macropad.encoder
    now = time.monotonic()

    if current_position != last_position and (now - last_change) > debounce_time:
        if current_position > last_position:
            current_instrument_index = (current_instrument_index + 1) % len(INSTRUMENTS)
        else:
            current_instrument_index = (current_instrument_index - 1) % len(INSTRUMENTS)

        current_instrument = INSTRUMENTS[current_instrument_index]
        midi.send(ProgramChange(current_instrument[1]))
        instrument_area.text = current_instrument[0]
        macropad.display.refresh()

        last_position = current_position
        last_change = now

    # Bouton du curseur pour réinitialiser au premier instrument
    if macropad.encoder_switch:
        current_instrument_index = 0
        current_instrument = INSTRUMENTS[current_instrument_index]
        midi.send(ProgramChange(current_instrument[1]))
        instrument_area.text = current_instrument[0]
        macropad.display.refresh()
        while macropad.encoder_switch:  # Attendre le relâchement
            time.sleep(0.1)

    time.sleep(0.01)
