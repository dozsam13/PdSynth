
value_intervals = {
    "Home": 
    {
        "amp": [0, 4],
        "rate": [0, 16],
    },
    "Amp":
    {
        "start_pos": [0,10000],
        "attack": [0, 1],
        "sustain": [0, 2],
        "release": [0, 1],
    },
    "Filter":
    {
        "cutoff": [0, 2200],
        "resonance": [1, 0]
    },
    "Effect":
    {
        "distortion_amp": [0, 2],
        "distortion_smooth": [0.2, 2],
        "reverb_send": [0, 4],
        "delay_send": [0, 4]
    }
}


def get_interval(scene_name, value_name):
    if scene_name in value_intervals.keys() and value_name in value_intervals[scene_name].keys():
        return value_intervals[scene_name][value_name]
    else:
        return None

def preprocess_button_map_config(config):
    button_map = {}
    for k in config["button_map"].keys():
        button_map[k] = {}
        for e in config["button_map"][k]:
            button_map[k][int(e)] = config["button_map"][k][e]
    return button_map
