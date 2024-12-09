import tkinter as tk

class ViewModel:
	def __init__(self, 
		bpm, volume, slew, seq_last_step,
		cutoff, resonance, 
		amp_mod_freq, amp_mod_amnt, freq_mod_freq, freq_mod_amnt,
		delay_time, delay_volume, delay_feedback, reverb_dry, reverb_wet, reverb_level, reverb_feedback,
		pd_client, root
	):
		self.data = {
			"Home":
			{
				"bpm": tk.StringVar(root, str(bpm)),
				"volume": tk.StringVar(root, str(volume)),
				"slew": tk.StringVar(root, str(slew)),
				"seq_last_step": tk.StringVar(root, str(seq_last_step))
			},
			"Filters":
			{
				"cutoff": tk.StringVar(root, str(cutoff)),
				"resonance": tk.StringVar(root, str(resonance))
			},
			"Modulation":
			{
				"amp_mod_freq": tk.StringVar(root, str(amp_mod_freq)),
				"amp_mod_amnt": tk.StringVar(root, str(amp_mod_amnt)),
				"freq_mod_freq": tk.StringVar(root, str(freq_mod_freq)),
				"freq_mod_amnt": tk.StringVar(root, str(freq_mod_amnt))
			},
			"Effects":
			{
				"delay_time": tk.StringVar(root, str(delay_time)),
				"delay_volume": tk.StringVar(root, str(delay_volume)),
				"delay_feedback": tk.StringVar(root, str(delay_feedback)),
				"reverb_dry": tk.StringVar(root, str(reverb_dry)),
				"reverb_wet": tk.StringVar(root, str(reverb_wet)),
				"reverb_level": tk.StringVar(root, str(reverb_level)),
				"reverb_feedback": tk.StringVar(root, str(reverb_feedback))
			}
		}
		self.pd_client = pd_client
	
	def change_state(self, section, param, change):
		new_value = int(self.data[section][param].get()) + change
		self.pd_client.set_param(param, new_value)
		self.data[section][param].set(str(new_value))
		
