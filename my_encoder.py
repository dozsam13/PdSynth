

class Encoder:
	def __init__(self, view_model):
		self.section = None
		self.param = None
		self.view_model = view_model
		
	def state_change(self, change):
		if self.param is not None and self.section is not None:
			self.view_model.change_state(self.param, change)
		else:
			self.logger.warning("Unbound encoder!")
