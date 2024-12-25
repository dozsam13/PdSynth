import tkinter as tk

class ViewModel:
	def __init__(self, engine_client, root, patterns, current_pattern_idx):
		
		data = {}
		pattern = patterns[current_pattern_idx]
		for section_name in pattern.data:
			data[section_name] = {}
			for param_name in pattern.data[section_name]:
				data[section_name][param_name] = tk.StringVar(root, str(pattern.data[section_name][param_name]))
		
		self.patterns = patterns
		self.current_pattern_idx = current_pattern_idx		
		self.data = data
		self.engine_client = engine_client
	
	def change_state(self, section, param, change):
		if section == "Home" and param == "name":
			self.current_pattern_idx += change
			self.current_pattern_idx %= len(self.patterns)
			self.load_pattern()
		else:
			new_value = int(self.data[section][param].get()) + change
			self.engine_client.set_param(param, new_value)
			self.data[section][param].set(str(new_value))

	def load_pattern(self):
		pattern = self.patterns[self.current_pattern_idx]
		for section_name in pattern.data:
			for param_name in pattern.data[section_name]:
				new_value = str(pattern.data[section_name][param_name])
				self.engine_client.set_param(param_name, new_value)
				print(section_name, param_name, new_value)
				self.data[section_name][param_name].set(str(new_value))


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
			
