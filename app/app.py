import json
from param_encoder import Encoder
from client.sc_client import SuperColliderClient
import keyboard
import time
from enum import Enum
import argparse
from helper import get_interval, preprocess_button_map_config
from sshkeyboard import listen_keyboard

parser = argparse.ArgumentParser()
parser.add_argument('--rpi', action='store_true', default=False, 
                    help='Use RaspberryPI hardware')
parser.add_argument('--cli', action='store_true', default=False, 
                    help='Use command line interface')
parser.add_argument('--pattern_path', default="patterns/test_patterns.json", 
                    help='Path to saved pattern files')
args = parser.parse_args()


RPI_CONTROLLER = args.rpi
COMMAND_LINE_INTERFACE = args.cli
PATTERN_PATH = args.pattern_path

if RPI_CONTROLLER:
    from lcd_screen import LCDScreen
    from encoder import GPIOZeroEncoder
    from gpiozero import Button
    import RPi.GPIO as GPIO

with open('app/config.json', 'r') as file:
    config = json.load(file)
short_names = config["short_names"]
button_map = preprocess_button_map_config(config)
value_intervals = config["value_intervals"]


sc_client = SuperColliderClient()

current_track = "1"
current_scene_idx = 0

if RPI_CONTROLLER:
    lcd_screen = LCDScreen()

def read_patterns():
    with open(PATTERN_PATH, 'r') as file:
        data = json.load(file)
    return data

class ButtonModel:
	def __init__(self):
		self.l_extender = "11111111"
		self.r_extender = "11111111"
		self.menu_extender = "11111111"

button_model = ButtonModel()

class Scene:
    def __init__(self, name, data_objects):
        self.data_objects = data_objects
        self.name = name

    def text(self):
        result = [[], [], [], []]
        for i, data_object in enumerate(self.data_objects):
            value, label = data_object.text()
            if value is not None and label is not None:
                result[i//4*2].append(value)
                result[i//4*2+1].append(label)
        
        for i in range(len(result)):
            result[i] = " ".join(result[i])

        return result

class AbstractDataObject:
    def __init__(self):
        pass

    def text(self):
        return None, None

    def change_state(self, amnt):
        pass

    def pad_to_length(self, v, n):
        return v.rjust(n)

    def render(self, value, index):
        if RPI_CONTROLLER:
            render_param_change(render_param_changevalue, index)
        render_gui(to_rpi = False)

    def is_saveable():
        return True


dummy_data_object = AbstractDataObject()

class PatternNameDataObject(AbstractDataObject):
    def __init__(self, patterns, sc_client, current_pattern_index, index, load_pattern_to_ui):
        super()
        self.sc_client = sc_client
        self.patterns = patterns
        self.current_pattern_index = current_pattern_index
        self.index = index
        self.current_pattern_name = patterns[current_pattern_index]["Global"]["Name"]
        self.scenes = None
        self.load_pattern_to_ui = load_pattern_to_ui

    def text(self):
        return self.current_pattern_name.ljust(11), "pattern".ljust(11)

    def change_state(self, amnt):
        self.current_pattern_index += amnt
        self.current_pattern_index %= len(self.patterns)
        self.current_pattern_name = self.patterns[self.current_pattern_index]["Global"]["Name"]
        # load new pattern to SC
        self.sc_client.load_pattern(self.patterns[self.current_pattern_index], value_intervals)
        # load new params to app
        self.load_pattern_to_ui(self.current_pattern_index)
        
    def write_value_to_pattern(self, pattern):
        pattern["Global"]["Name"] = self.current_pattern_name


class BPMDataObject(AbstractDataObject):
    def __init__(self, value, index):
        super()
        self.value = value
        self.index = index

    def text(self):
        v = str(self.value).rjust(3)
        return v, "bpm"

    def change_state(self, amnt):
        if 0 < (self.value + amnt) <= 350:
            self.value += amnt
            update_value = self.value

            sc_client.set_param("/" + self.name, update_value)
            self.render(str(self.value).rjust(3), self.index)

    def write_value_to_pattern(self, pattern):
        pattern["Global"]["bpm"] = self.value


class PatternDataObject(AbstractDataObject):
    def __init__(self, name, value, scene_name, index, track_id):
        super()
        self.name = name
        self.value = value
        self.scene_name = scene_name
        self.interval = get_interval(value_intervals, scene_name, name)
        self.index = index
        self.track_id = track_id

    def text(self):
        v = str(self.value)
        if len(v) < 3:
            v = "{:>3}".format(v)
        return v, short_names[self.scene_name][self.name]

    def change_state(self, amnt):
        update_value = None
        if self.interval is None:
            self.value += amnt
            update_value = self.value

        else:
            if 0 <= (self.value + amnt) <= 100:
                self.value += amnt
                update_value = self.get_interval_value()
        if update_value is not None:
            sc_client.set_param("/" + self.name + "_" + current_track, update_value)
            self.render(str(self.value).rjust(3), self.index)

    def get_interval_value(self):
        return self.interval[0] + (self.interval[1]-self.interval[0])*float(self.value)/100+0.000001

    def write_value_to_pattern(self, pattern):
        pattern["track_data"][self.track_id][self.scene_name][self.name] = self.value


def load_pattern_to_ui(pattern_index):
    global scenes
    scenes = create_scenes(patterns, pattern_index)
    unbind_encoders()
    bind_encoders()
    render_gui()

def create_global_scene(patterns, current_pattern_index):
    l_p_t_ui = lambda x: load_pattern_to_ui(x)
    pattern_name_data_object = PatternNameDataObject(patterns, sc_client, current_pattern_index, 0, l_p_t_ui)
    bpm_data_object = BPMDataObject(patterns[current_pattern_index]["Global"]["bpm"], 4)
    global_data_objects = [pattern_name_data_object, dummy_data_object, dummy_data_object, dummy_data_object, bpm_data_object]
    global_scene = Scene("Global", global_data_objects)
    return global_scene

def create_scenes(patterns, current_pattern_index):
    result = {}
    global_scene = create_global_scene(patterns, current_pattern_index)
    for trk_id, scenes_data in patterns[current_pattern_index]["track_data"].items():
        scenes = [global_scene]
        for scene_name, scene_data in scenes_data.items():
            if scene_name not in {"Sequence", "Mute"}:
                data_objects = []
                for i, (label, value) in enumerate(scene_data.items()):
                    data_objects.append(PatternDataObject(label, value, scene_name, i, trk_id))
                scenes.append(Scene(scene_name, data_objects))
        result[trk_id] = scenes
    return result

def render_gui(to_rpi=True):
    t = scenes[current_track][current_scene_idx].text()
    t2 = []
    for e in t:
        t2.append(e)
    if RPI_CONTROLLER and to_rpi:
        print("write lines")
        lcd_screen.write_lines(t2)
    print(t2[0])
    print(t2[1])
    print(t2[2])
    print(t2[3])

def render_param_change(value, index):
    row = index // 4
    column = index % 4


    lcd_screen.write_param_value(row, column, value)

def mute_track(trk):
    v = int(not patterns[0].data["track_data"][str(trk)]["Mute"])
    patterns[0].data["track_data"][str(trk)]["Mute"] = v
    sc_client.mute_track(trk, v)

def change_track(trk):
    global current_track
    global current_scene_idx
    current_track = str(trk)
    change_scene_to(current_scene_idx)

def change_scene_to(scn):
    global current_scene_idx

    unbind_encoders()
    # lcd cleanup
    if RPI_CONTROLLER:
        print(current_scene_idx, scn,len(scenes))
        lcd_screen.cleanup()
    current_scene_idx = scn
    bind_encoders()
    render_gui()
    
def save_current_pattern():
    for scene in scenes:
        for data_object in scene.data_objects:
            if data_object.is_saveable():
                data_object.write_value_to_pattern(patterns[current_pattern_index])


def change_scene(amnt):
    global current_scene_idx
    global current_track
    
    current_scene_idx += amnt
    current_scene_idx %= len(scenes[current_track])
    change_scene_to(current_scene_idx)
    

def unbind_encoders():
    for i, encoder in enumerate(encoders):
        encoder.data_object = None


def bind_encoders():
    global current_scene_idx
    global scenes
    global encoders
    global current_track
    l = min([len(encoders), len(list(scenes[current_track][current_scene_idx].data_objects))])
    for i in range(l):
        encoders[i].data_object = scenes[current_track][current_scene_idx].data_objects[i]


patterns = read_patterns()
scenes = create_scenes(patterns, current_pattern_index=0)
encoders = [Encoder(), Encoder(), Encoder(), Encoder(), Encoder(), Encoder(), Encoder(), Encoder()]
sc_client.load_pattern(patterns[0], value_intervals)

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
        print("starting sequencer")
        sc_client.start_sequencer()
    else:
        sc_client.stop_sequencer()
        print("stopping sequencer")
    seq_running = not seq_running

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
    patterns[0]["track_data"][current_track]["Sequence"]["freq"][idx] = int(not patterns[0]["track_data"][current_track]["Sequence"]["freq"][idx])

    print(patterns[0]["track_data"][current_track]["Sequence"]["freq"])
    sc_client.set_param("/freq_" + current_track, list(map(lambda x: x if x==1 else "", patterns[0]["track_data"][current_track]["Sequence"]["freq"])))

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
    global current_track
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
    for (extender_name, diffs) in [("left_extender", l_ext_diffs), ("right_extender", r_ext_diffs)]:
        for dif in diffs:
            if menu_extender_bin[7] == "0":
                mute_track(button_map[extender_name][dif] + 1)
            elif menu_extender_bin[6] == "0":
                change_track(button_map[extender_name][dif] + 1)
            else:
                seq_pressed(button_map[extender_name][dif])

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
