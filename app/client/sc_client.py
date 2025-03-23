from pythonosc import udp_client


class SuperColliderClient:
	def __init__(self, UDP_IP = "127.0.0.1", UDP_PORT = 57120):
		self.client = udp_client.SimpleUDPClient(UDP_IP, UDP_PORT)

	def set_param(self, param_name, param_value):
		self.client.send_message(param_name, param_value)

	def start_sequencer(self):
		client.send_message("/start_seq", None)

	def stop_sequencer(self):		
		client.send_message("/stop_seq", None)


# sc client
UDP_IP = "127.0.0.1"
UDP_PORT = 57120
client = udp_client.SimpleUDPClient(UDP_IP, UDP_PORT)

client.send_message("/stop_seq", None)
'''
client.send_message("/rate_1", 2)
client.send_message("/freq_1", [0, 10, 0, 10])
'''