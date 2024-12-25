import tkinter as tk


class ViewModel:
	def __init__(self, engine_client, root, patterns):
		
		data = {}
		pattern = patterns[0]
		for section_name in pattern.data:
			if section_name in {"Sequence"}:
				continue
			data[section_name] = {}
			for param_name in pattern.data[section_name]:
				data[section_name][param_name] = tk.StringVar(root, str(pattern.data[section_name][param_name]))
		
		self.patterns = patterns
		self.current_pattern_idx = 0
		self.data = data
		self.engine_client = engine_client
		self.pitch_offset = 50

	
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
			if section_name == "Sequence":
				continue
			for param_name in pattern.data[section_name]:
				new_value = pattern.data[section_name][param_name]
				if not(section_name == "Home" and param_name == "name"):
					new_value = int(new_value)
				self.engine_client.set_param(param_name, new_value)
				self.data[section_name][param_name].set(str(new_value))


	def play_pitch(self, i):
		self.engine_client.set_param("pitch", self.pitch_offset + i)
