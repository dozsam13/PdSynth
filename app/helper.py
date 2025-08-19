
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


short_names = {
    "Home":
    {
        "amp": "amp",
        "bufnum": "buf",
        "rate": "rte",
    },
    "Amp":
    {
        "start_pos": "sps",
        "attack": "atk",
        "sustain": "stn",
        "release": "rls"
    },
    "Filter":
    {
        "cutoff": "ctf",
        "resonance": "res"
    },
    "Effect":
    {
        "distortion_amp": "dam",
        "distortion_smooth": "dsm",
        "reverb_send": "rvs",
        "delay_send": "dls"
    }
}