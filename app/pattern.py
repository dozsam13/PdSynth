
class Pattern:
	def __init__(self, 
		bpm, volume, slew, seq_last_step,
		cutoff, resonance, 
		amp_mod_freq, amp_mod_amnt, freq_mod_freq, freq_mod_amnt,
		delay_time, delay_volume, delay_feedback, reverb_dry, reverb_wet, reverb_level, reverb_feedback,
		
	):
		self.main_section = [
			"Home",
			{
				"bpm": bpm,
				"volume": volume,
				"slew": slew,
				"seq_last_step": seq_last_step
			}
		]
		self.filter_section = [
			"Filters",
			{
				"cutoff": cutoff,
				"resonance": resonance
			}
		]
		self.mod_section = [
			"Modulation",
			{
				"amp_mod_freq": amp_mod_freq,
				"amp_mod_amnt": amp_mod_amnt,
				"freq_mod_freq": freq_mod_freq,
				"freq_mod_amnt": freq_mod_amnt
			}
		]
		self.effect_section = [
			"Effects",
			{
				"delay_time": delay_time,
				"delay_volume": delay_volume,
				"delay_feedback": delay_feedback,
				"reverb_dry": reverb_dry,
				"reverb_wet": reverb_wet,
				"reverb_level": reverb_level,
				"reverb_feedback": reverb_feedback
			}
		]

	def get_sections(self):
		return self.main_section, self.filter_section, self.mod_section, self.effect_section
