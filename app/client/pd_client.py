from pythonosc import udp_client

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

class PdClient:
	def __init__(self, UDP_IP="127.0.0.1", UDP_PORT=3333):
		self.UDP_IP = UDP_IP
		self.UDP_PORT = UDP_PORT
		self.client = udp_client.SimpleUDPClient(UDP_IP, UDP_PORT)
	
	def set_param(self, param_name, param_value):
		self.client.send_message("/" + param_name, param_value)
	
	def load_pattern(self, pattern):
		for section in pattern.get_sections():
			for param_name, param_value in section[1].items():
				self.set_param(param_name, param_value)
