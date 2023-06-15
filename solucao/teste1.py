import rtmidi
import rtmidi.midiutil

midiout = rtmidi.MidiOut(rtapi=rtmidi.API_WINDOWS_MM)
print(f"api: {rtmidi.get_api_name(midiout.get_current_api())}")
print(rtmidi.get_compiled_api())
print(midiout.get_ports())