class Encoder:
	def __init__(self, data_object=None):
		self.data_object = data_object
		
	def state_change(self, change):
		if self.data_object is not None:
			self.data_object.change_state(change)
		else:
			print("Warning! Unbound encoder!")
