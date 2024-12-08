import warnings


class Encoder:
	def __init__(self, pattern):
		self.section = None
		self.param = None
		self.pattern = pattern
		
	def state_change(self, change):
		if self.param is not None and self.section is not None:
			print(self.section, self.param, change)
			self.pattern.change_state(self.section, self.param, change)
		else:
			print("UNBOUND ENCODER!")
			#warnings.warn("Unbound encoder!")
