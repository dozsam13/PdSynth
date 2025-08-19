

def get_interval(value_intervals, scene_name, value_name):
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
