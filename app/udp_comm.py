from pythonosc import udp_client


class PdClient:
	def __init__(self, UDP_ID="127.0.0.1", UDP_PORT=3333):
		self.UDP_IP = UDP_IP
		self.UDP_PORT = UDP_PORT
		self.client = udp_client.SimpleUDPClient(UDP_IP, UDP_PORT)
	
	def send_message(self, param_name, param_value)
		self.client.send_message("/" + param_name, param_value)
	
	def load_pattern(self, pattern):
		for section in pattern.get_sections():
			for param_name, param_value in section[1].items():
				self.send_message(param_name, param_value)
