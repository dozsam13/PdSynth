class Pattern:
	def __init__(self,
		name=None, bpm=None, volume=None, slew=None, seq_last_step=None,
		cutoff=None, resonance=None, 
		amp_mod_freq=None, amp_mod_amnt=None, freq_mod_freq=None, freq_mod_amnt=None,
		delay_time=None, delay_volume=None, delay_feedback=None, reverb_dry=None, reverb_wet=None, reverb_level=None, reverb_feedback=None,
		attack=None, decay=None, sustain_level=None, sustain_length=None, release=None,
		pitches=None, mask=None):
			
		self.data = {
			"Home":
			{
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
			},
			"Sequence":
			{
				"pitches": pitches,
				"mask": mask
			}
		}
			
