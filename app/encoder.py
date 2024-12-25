import logging

class Encoder:
	def __init__(self, pattern):
		self.section = None
		self.param = None
		self.pattern = pattern
		logger = logging.getLogger('root')
		logger.setLevel(logging.DEBUG)
		self.logger = logger
		
	def state_change(self, change):
		if self.param is not None and self.section is not None:
			self.logger.debug(self.section, self.param, change)
			self.pattern.change_state(self.section, self.param, change)
			#print(self.section, self.param, change)
		else:
			self.logger.warning("Unbound encoder!")
