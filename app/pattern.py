import tkinter as tk

class ViewModel:
	def __init__(self, engine_client, root, pattern):
		
		data = {}
		for section_name in pattern.data:
			data[section_name] = {}
			for param_name in pattern.data[section_name]:
				if param_name != "name":
					data[section_name][param_name] = tk.StringVar(root, str(pattern.data[section_name][param_name]))
				else:
					self.pattern_name = tk.StringVar(root, str(pattern.data[section_name][param_name]))
				
		self.data = data
		self.engine_client = engine_client
	
	def change_state(self, section, param, change):
		new_value = int(self.data[section][param].get()) + change
		self.engine_client.set_param(param, new_value)
		self.data[section][param].set(str(new_value))

class Pattern:
	def __init__(self,
		name, bpm, volume, slew, seq_last_step,
		cutoff, resonance, 
		amp_mod_freq, amp_mod_amnt, freq_mod_freq, freq_mod_amnt,
		delay_time, delay_volume, delay_feedback, reverb_dry, reverb_wet, reverb_level, reverb_feedback,
		attack, decay, sustain_level, sustain_length, release):
			
		self.data = {
			"Home":
			{
				"name": name,
				"bpm": bpm,
				"volume": volume,
				"slew_rate": slew,
				"seq_last_step": seq_last_step
			},
			"Filters":
			{
				"cutoff": cutoff,
				"resonance": resonance
			},
			"Modulation":
			{
				"amp_mod_freq": amp_mod_freq,
				"amp_mod_amnt": amp_mod_amnt,
				"freq_mod_freq": freq_mod_freq,
				"freq_mod_amnt": freq_mod_amnt
			},
			"Effects":
			{
				"delay_time": delay_time,
				"delay_volume": delay_volume,
				"delay_feedback": delay_feedback,
				"reverb_dry": reverb_dry,
				"reverb_wet": reverb_wet,
				"reverb_level": reverb_level,
				"reverb_feedback": reverb_feedback
			},
			"Envelope":
			{
				"attack": attack,
				"decay": decay,
				"sustain_level": sustain_level,
				"sustain_length": sustain_length,
				"release": release,
			}
		}
			
