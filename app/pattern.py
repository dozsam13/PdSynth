
class Pattern:
	def __init__(self, 
		bpm, volume, slew, seq_last_step,
		cutoff, resonance, 
		amp_mod_freq, amp_mod_amnt, freq_mod_freq, freq_mod_amnt,
		delay_time, delay_volume, delay_feedback, reverb_dry, reverb_wet, reverb_level, reverb_feedback,
		pd_client
	):
		self.data = {
			"Home":
			{
				"bpm": bpm,
				"volume": volume,
				"slew": slew,
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
			}
		}
		self.pd_client = pd_client
	
	def change_state(self, section, param, change):
		self.pd_client.set_param(param, self.data[section][param] + change)
		self.data[section][param] += change
		
