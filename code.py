import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_macropad import MacroPad

# Initialisation du MacroPad et MIDI
macropad = MacroPad()
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# Notes MIDI associées aux touches du MacroPad (Do, Ré, Mi, Fa, Sol, La, Si, Do...)
MIDI_NOTES = [
    60, 62, 64, 65, 67, 69, 71, 72,  # Octave centrale (C4 à C5)
    74, 76, 77, 79  # Notes supplémentaires
]

# Affichage sur l’écran du MacroPad
macropad.display.auto_refresh = False
text_area = macropad.display_text("Appuie sur une touche !")
macropad.display.refresh()

while True:
    key_event = macropad.keys.events.get()
    if key_event:
        key_index = key_event.key_number

        if key_event.pressed and key_index < len(MIDI_NOTES):
            note = MIDI_NOTES[key_index]
            midi.send(NoteOn(note, 127))  # Envoie la note MIDI avec vélocité max
            text_area.text = f"Note: {note}"
            macropad.display.refresh()

        elif key_event.released and key_index < len(MIDI_NOTES):
            note = MIDI_NOTES[key_index]
            midi.send(NoteOff(note, 0))  # Arrête la note
            text_area.text = "Appuie sur une touche !"
            macropad.display.refresh()

    time.sleep(0.01)
