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
    from encoder import GPIOZeroEncoder
    from gpiozero import Button
    import RPi.GPIO as GPIO

short_names = {
    "Home":
    {
        "amp": "amp",
        "bufnum": "buf",
        "rate": "rte",
    },
    "Amp":
    {
        "attack": "atk",
        "decay": "dcy",
        "sustain_level": "stl",
        "release": "rls"
    },
    "Filter":
    {
        "cutoff": "ctf",
        "resonance": "res"
    }
}

value_intervals = {
    "Home": 
    {
        "amp": [0, 4]
    },
    "Amp":
    {
        "attack": [0, 1],
        "decay": [0, 1],
        "sustain_level": [0, 1],
        "release": [0, 1],
    },
    "Filter":
    {
        "cutoff": [0, 2200],
        "resonance": [1, 0]
    }
}


button_map = {
    "left_extender": {
        4: 0,
        1: 1,
        3: 2,
        5: 3,
        0: 8,
        2: 9,
        6: 10,
        7: 11
    },
    "right_extender": {
        7: 4,
        3: 5,
        1: 6,
        4: 7,
        5: 12,
        6: 13,
        2: 14,
        0: 15
    },
    "menu_extender": {
    	4: 0,
    	0: 1,
    	1: 2,
    	2: 3,
    	3: 4,
    	7: None, #mute
    	6: None  #func
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

class ButtonModel:
	def __init__(self):
		self.l_extender = "11111111"
		self.r_extender = "11111111"
		self.menu_extender = "11111111"

button_model = ButtonModel()

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

def get_interval(scene_name, value_name):
    if scene_name in value_intervals.keys() and value_name in value_intervals[scene_name].keys():
        return value_intervals[scene_name][value_name]
    else:
        return None

class DataObject:
    def __init__(self, name, value, scene):
        self.name = name
        self.value = value
        self.scene = scene
        self.interval = get_interval(scene, name)

    def text(self):
        v = str(self.value)
        if len(v) < 3:
            v = "{:<3}".format(v)
        return v, short_names[self.scene][self.name]

    def change_state(self, amnt):
        if self.interval is None:
            self.value += amnt
            sc_client.set_param("/" + self.name + "_" + current_track, self.value)
            render_gui()
        else:
            if 0 <= (self.value + amnt) <= 100:
                self.value += amnt
                update_value = self.interval[0] + (self.interval[1]-self.interval[0])*float(self.value)/100
                print(self.scene, self.name, self.value, update_value)
                sc_client.set_param("/" + self.name + "_" + current_track, update_value+0.0001)
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
    t2 = []
    for e in t:
        t2.append(e)#.ljust(20))
    if RPI_CONTROLLER:
        lcd_screen.write_lines(t2)
    print(t2[0])
    print(t2[1])
    print(t2[2])
    print(t2[3])

def change_track(trk):
    global current_track
    global current_scene_idx
    current_track = str(trk)
    change_scene_to(current_scene_idx)

def change_scene_to(scn):
    global current_scene_idx
    if len(scenes[current_track]) <= scn:
        return
    unbind_encoders()
    current_scene_idx = scn
    bind_encoders()
    render_gui()


def change_scene(amnt):
    global current_scene_idx
    global current_track
    
    current_scene_idx += amnt
    current_scene_idx %= len(scenes[current_track])
    change_scene_to(current_scene_idx)
    

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


if RPI_CONTROLLER:
    rpi_encoders = [GPIOZeroEncoder(17, 4, encoders[0]),
                    GPIOZeroEncoder(6, 27, encoders[1]), 
                    GPIOZeroEncoder(13, 5, encoders[2]), 
                    GPIOZeroEncoder(26, 19, encoders[3]),
                    GPIOZeroEncoder(8, 25, encoders[4]),
                    GPIOZeroEncoder(24, 1, encoders[5]),
                    GPIOZeroEncoder(16, 20, encoders[6]),
                    GPIOZeroEncoder(7, 12, encoders[7])]

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
keyboard.add_hotkey('v', lambda: change_track(3))
keyboard.add_hotkey('b', lambda: change_track(4))

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
    print(i2cbus)
    menu_extender_address = 0x23
    l_extender_adress = 0x26
    r_extender_adress = 0x25

def find_all_indices(lst, element):
    indices = []
    for i in range(len(lst)):
        if lst[i] == element:
            indices.append(i)
    return indices

interrupt_counter = 0
btn_counter_map = {}

def append_first_zero(binary_number):
    if len(binary_number) < 8:
        binary_number = "0" + binary_number
    return binary_number

def find_differences(str1, str2):
    return [i for i, (a, b) in enumerate(zip(str1, str2)) if a != b]

def keep_only_zeros(diff_indexes, extender_bin):
	r = []
	for ind in diff_indexes:
		if extender_bin[ind] == "0":
			r.append(ind)
	return r

def button_pressed_callback(a):
    global interrupt_counter
    interrupt_counter += 1
    
    print("INTERRUPT RECEIVED", flush=True)
    l_extender = i2cbus.read_byte_data(l_extender_adress,0xFF)
    r_extender = i2cbus.read_byte_data(r_extender_adress,0xFF)
    menu_extender = i2cbus.read_byte_data(menu_extender_address,0xFF)
    l_extender_bin = append_first_zero(str(bin(l_extender))[2:])
    r_extender_bin = append_first_zero(str(bin(r_extender))[2:])
    menu_extender_bin = append_first_zero(str(bin(menu_extender))[2:])

    l_ext_diffs = keep_only_zeros(find_differences(button_model.l_extender, l_extender_bin), l_extender_bin)
    r_ext_diffs = keep_only_zeros(find_differences(button_model.r_extender, r_extender_bin), r_extender_bin)
    menu_ext_diffs = keep_only_zeros(find_differences(button_model.menu_extender, menu_extender_bin), menu_extender_bin)
    for dif in l_ext_diffs:
    	if menu_extender_bin[7] == "0":
    		print("muting track: ", button_map["left_extender"][dif] + 1)
    	elif menu_extender_bin[6] == "0":
    		change_track(button_map["left_extender"][dif] + 1)
    	else:
    		seq_pressed(button_map["left_extender"][dif])

    for dif in r_ext_diffs:
    	if menu_extender_bin[7] == "0":
    		print("muting track: ", button_map["right_extender"][dif] + 1)
    	elif menu_extender_bin[6] == "0":
    		change_track(button_map["right_extender"][dif] + 1)
    	else:
    		seq_pressed(button_map["right_extender"][dif])

    for dif in menu_ext_diffs:
    	if dif < 5:
    		change_scene_to(button_map["menu_extender"][dif])

    button_model.l_extender = l_extender_bin
    button_model.r_extender = r_extender_bin
    button_model.menu_extender = menu_extender_bin

if RPI_CONTROLLER:
    import pigpio
    pi = pigpio.pi()
    BUTTON_GPIO = 21
    
    button1 = Button(21)
    button1.when_pressed = button_pressed_callback

while True:
    time.sleep(1)
