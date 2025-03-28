import json
from pattern import Pattern
from my_encoder import Encoder
from client.sc_client import SuperColliderClient
import keyboard
import time
from enum import Enum


RPI_CONTROLLER = True

sc_client = SuperColliderClient()
if RPI_CONTROLLER:
    from my_lcd_screen import LCDScreen
    import RPi.GPIO as GPIO

short_names = {
    "Home":
    {
        "amp": "amp",
        "bufnum": "buf",
        "rate": "rte"
    }
}

#button_map = [,,,,0]

button_map = {
    "left_extender": {
        247: 0,
        191: 1,
        239: 2,
        251: 3,
        127: 8,
        223: 9,
        253: 10,
        254: 11
    },
    "right_extender": {
        254: 4,
        239: 5,
        191: 6,
        247: 7,
        251: 12,
        253: 13,
        223: 14,
        127: 15
    }
}

current_track = "1"
current_scene_idx = 0

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
        sc_client.set_param("/" + self.name + "_" + current_track, self.value)
        render_gui()


class ViewModel:
    def __init__(self, scenes):
        self.scenes = scenes

    def change_state(self, param, amnt):
        self.scenes[current_track][current_scene_idx].data[param].change_state(amnt)



def create_scenes(ptn):
    result = {}
    for trk_id, pattern in ptn.items():
        scenes = []
        for scene_name, scene_data in pattern.items():
            if scene_name not in {"Name", "Sequence"}:
                scenes.append(Scene(scene_name, scene_data))
        result[trk_id] = scenes
    return result

def render_gui():
    t = scenes[current_track][current_scene_idx].text()
    if RPI_CONTROLLER:
        lcd_screen.write_lines(t)
    print(t[0])
    print(t[1])
    print(t[2])
    print(t[3])

def change_track(trk):
    global current_track
    current_track = str(trk)
    change_scene(0)

def change_scene(amnt):
    global current_scene_idx
    global current_track
    unbind_encoders()
    current_scene_idx += amnt
    current_scene_idx %= len(scenes[current_track])
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
    global current_track
    print(len(list(scenes[current_track][current_scene_idx].data.items())))
    l = min([len(encoders), len(list(scenes[current_track][current_scene_idx].data.items()))])
    for i in range(l):
        encoders[i].section = scenes[current_track][current_scene_idx].name
        encoders[i].param = list(scenes[current_track][current_scene_idx].data.items())[i][0]



patterns = read_patterns()
scenes = create_scenes(patterns[0].data)
view_model = ViewModel(scenes)
encoders = [Encoder(view_model), Encoder(view_model), Encoder(view_model), Encoder(view_model), Encoder(view_model), Encoder(view_model), Encoder(view_model), Encoder(view_model)]

seq_running = False
def seq_start_stop():
    global seq_running
    if not seq_running:
        sc_client.start_sequencer()
    else :
        sc_client.stop_sequencer()
    seq_running = not seq_running
    print("space pressed")

keyboard.add_hotkey('space', seq_start_stop)
keyboard.add_hotkey('x', lambda: change_track(1))
keyboard.add_hotkey('c', lambda: change_track(2))

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


def seq_pressed(idx):
    patterns[0].data[current_track]["Sequence"]["freq"][idx] = int(not patterns[0].data[current_track]["Sequence"]["freq"][idx])
    print(patterns[0].data[current_track]["Sequence"]["freq"])
    sc_client.set_param("/freq_" + current_track, list(map(lambda x: x if x==1 else "", patterns[0].data[current_track]["Sequence"]["freq"])))

## bind sequencer keyboard keys
def on_seq_press(event):
    seq_keys = ['0', '1', '2', '3', '4', '5', '6', '7', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k']
    if event.name in seq_keys:
        seq_index = seq_keys.index(event.name)
        seq_pressed(seq_index)

keyboard.on_press(on_seq_press)


bind_encoders()
render_gui()
if RPI_CONTROLLER:
    i2cbus = lcd_screen.screen.bus
    l_extender_adress = 0x26
    r_extender_adress = 0x25

interrupt_counter = 0
def button_pressed_callback(a):
    global interrupt_counter
    interrupt_counter += 1
    
    #print("INTERRUPT RECEIVED", flush=True)
    #print(a)
    l_extender = i2cbus.read_byte_data(l_extender_adress,0xFF)
    r_extender = i2cbus.read_byte_data(r_extender_adress,0xFF)
    #print(bin(l_extender), flush=True)
    #print(bin(r_extender), flush=True)
    l_extender_bin = str(bin(l_extender))[2:]
    r_extender_bin = str(bin(r_extender))[2:]
    
    #print(interrupt_counter, " ", l_extender_bin, " ", r_extender_bin)  
    
    l_z_i = l_extender_bin.find('0')
    pressed_button = None
    #print(interrupt_counter, " ", l_extender_bin)
    if l_z_i > -1 or l_extender == 127:
        pressed_button = button_map["left_extender"][l_extender]
        #print(pressed_button)
    else:
        r_z_i = r_extender_bin.find('0')
        if r_z_i > -1 or r_extender == 127:
            pressed_button = button_map["right_extender"][r_extender]
            #print(pressed_button)
    if pressed_button is not None:
        seq_pressed(pressed_button)
            

if RPI_CONTROLLER:
    BUTTON_GPIO = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=300)


while True:
    pass
