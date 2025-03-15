import json
from pattern import Pattern
from my_encoder import Encoder

import keyboard
import time
from enum import Enum


RPI_CONTROLLER = False

if RPI_CONTROLLER:
    from my_lcd_screen import LCDScreen
    import RPi.GPIO as GPIO

short_names = {
    "Home":
            {
                "name": "nm",
                "bpm": "bpm",
                "volume": "vlm",
                "slew_rate": "slw",
                "seq_last_step": "sls"
            },
            "Filters":
            {
                "cutoff": "ctf",
                "resonance": "rsn"
            },
            "Modulation":
            {
                "amp_mod_freq": "amf",
                "amp_mod_amnt": "ama",
                "freq_mod_freq": "fmf",
                "freq_mod_amnt": "fma"
            },
            "Effects":
            {
                "delay_time": "dlt",
                "delay_volume": "dlv",
                "delay_feedback": "dlf",
                "reverb_dry": "rvd",
                "reverb_wet": "rvw",
                "reverb_level": "rvl",
                "reverb_feedback": "rvf"
            },
            "Envelope":
            {
                "attack": "atk",
                "decay": "dcy",
                "sustain_level": "slv",
                "sustain_length": "sle",
                "release": "rel",
            },
}

if RPI_CONTROLLER:
    lcd_screen = LCDScreen()

def read_patterns():
    with open('patterns/patterns.json', 'r') as file:
        data = json.load(file)
    patterns = []
    for pattern_data in data:
        pattern = Pattern()
        pattern_data
        pattern_data.pop('Name', None)
        pattern.data = pattern_data
        patterns.append(pattern)
    return patterns

class Scene:
    def __init__(self, name, data):
        self.name = name

        self.data = {k : DataObject(k, v, name) for k,v in data.items()}

    def text(self):
        result = [[], []]
        for k, d_obj in self.data.items():
            value, value_text = d_obj.text()
            result[0].append(value)
            result[1].append(value_text)
        values = " ".join(result[0])
        texts = " ".join(result[1])

        final_text = [values[:16], texts[:16], values[16:], texts[16:]]

        return final_text
        


class DataObject:
    def __init__(self, name, value, scene):
        self.name = name
        self.value = value
        self.scene = scene

    def text(self):
        v = str(self.value)
        if len(v) < 3:
            v = "{:<3}".format(v)
        return v, short_names[self.scene][self.name]

    def change_state(self, amnt):
        self.value += amnt
        render_gui()



class ViewModel:
    def __init__(self, scenes):
        self.scenes = scenes

    def change_state(self, param, amnt):
        self.scenes[current_scene_idx].data[param].change_state(amnt)



def create_scenes(pattern):
    scenes = []
    for scene_name, scene_data in pattern.data.items():
            if scene_name not in {"Name", "Sequence"}:
                scenes.append(Scene(scene_name, scene_data))
    return scenes


def render_gui():
    t = scenes[current_scene_idx].text()
    if RPI_CONTROLLER:
        lcd_screen.write_lines(t)
    print(t[0])
    print(t[1])
    print(t[2])
    print(t[3])

current_scene_idx = 0

def change_scene(amnt):
    global current_scene_idx
    unbind_encoders()
    current_scene_idx += amnt
    current_scene_idx %= len(scenes)
    bind_encoders()
    render_gui()


def unbind_encoders():
    for i, encoder in enumerate(encoders):
        encoder.section = None
        encoder.param = None

def bind_encoders():
    global current_scene_idx
    global scenes
    global encoders

    l = min([len(encoders), len(list(scenes[current_scene_idx].data.items()))])
    for i in range(l):
        encoders[i].section = scenes[current_scene_idx].name
        encoders[i].param = list(scenes[current_scene_idx].data.items())[i][0]


patterns = read_patterns()
scenes = create_scenes(patterns[0])
view_model = ViewModel(scenes)
encoders = [Encoder(view_model), Encoder(view_model), Encoder(view_model), Encoder(view_model), Encoder(view_model), Encoder(view_model), Encoder(view_model), Encoder(view_model)]


keyboard.add_hotkey('n', lambda: change_scene(-1))
keyboard.add_hotkey('m', lambda: change_scene(1))
keyboard.add_hotkey('q', lambda: encoders[0].state_change(-1))
keyboard.add_hotkey('w', lambda: encoders[0].state_change(1))
keyboard.add_hotkey('e', lambda: encoders[1].state_change(-1))
keyboard.add_hotkey('r', lambda: encoders[1].state_change(1))
keyboard.add_hotkey('t', lambda: encoders[2].state_change(-1))
keyboard.add_hotkey('z', lambda: encoders[2].state_change(1))
keyboard.add_hotkey('u', lambda: encoders[3].state_change(-1))
keyboard.add_hotkey('i', lambda: encoders[3].state_change(1))



bind_encoders()
render_gui()
if RPI_CONTROLLER:
    i2cbus = lcd_screen.screen.bus
    l_extender_adress = 0x26
    r_extender_adress = 0x25

def button_pressed_callback(a):
    print("INTERRUPT RECEIVED", flush=True)
    print(a)
    l_extender = i2cbus.read_byte_data(l_extender_adress,0xFF)
    r_extender = i2cbus.read_byte_data(r_extender_adress,0xFF)
    print(bin(l_extender), flush=True)
    print(bin(r_extender), flush=True)

if RPI_CONTROLLER:
    BUTTON_GPIO = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=100)

#env = EnvGen.kr(Env.new, doneAction:2);
while True:
    pass