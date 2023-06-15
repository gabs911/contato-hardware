import rtmidi
import rtmidi.midiutil

print(f"api: {rtmidi.get_api_name(rtmidi.MidiOut().get_current_api())}")
print(rtmidi.get_compiled_api())
print(rtmidi.midiutil.get_api_from_environment(rtmidi.API_WINDOWS_MM))

