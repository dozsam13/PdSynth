
value_intervals = {
    "Home": 
    {
        "amp": [0, 4]
    },
    "Amp":
    {
        "attack": [0, 1],
        "sustain": [0, 2],
        "release": [0, 1],
    },
    "Filter":
    {
        "cutoff": [0, 2200],
        "resonance": [1, 0]
    }
}



def get_interval(scene_name, value_name):
    if scene_name in value_intervals.keys() and value_name in value_intervals[scene_name].keys():
        return value_intervals[scene_name][value_name]
    else:
        return None
