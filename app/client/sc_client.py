from pythonosc import udp_client
import time
import threading
from helper import get_interval

from pythonosc import dispatcher
from pythonosc import osc_server

def default_handler(address, *args):
    print(f"Unhandled OSC message: {address} {args}")

def specific_handler(address, *args):
    print(f"Specific message received: {address} with values {args}", flush=True)



class SuperColliderClient:
	def __init__(self, UDP_IP = "127.0.0.1", UDP_PORT_IN = 57121, UDP_PORT_OUT = 57120):
		self.client = udp_client.SimpleUDPClient(UDP_IP, UDP_PORT_OUT)
		dispatcherr = dispatcher.Dispatcher()
		#dispatcherr.set_default_handler(default_handler)
		dispatcherr.map("/test", specific_handler)

		server = osc_server.ThreadingOSCUDPServer((UDP_IP, UDP_PORT_IN), dispatcherr)
		self.osc_server = server
		#osc_server_thread = threading.Thread(target=server.serve_forever)
		#osc_server_thread.start()

		#print("SERVER ADDRESS: ", server.server_address)
		#self.osc_server_thread = osc_server_thread

	def set_param(self, param_name, param_value):
		self.client.send_message(param_name, param_value)

	def start_sequencer(self):
		self.client.send_message("/start_seq", "")

	def stop_sequencer(self):		
		self.client.send_message("/stop_seq", "")

	def set_bpm(self, bpm):
		self.client.send_message("/bpm", bpm)
	
	def mute_track(self, trk, value):
		self.set_param(f"/mute_{trk}", value)

	def stop(self):
		self.osc_server.shutdown()
		#self.osc_server_thread.join()

	def load_pattern(self, pattern, value_intervals):
		track_data = pattern["track_data"]

		for track_id in track_data.keys():
			for scene_name in track_data[track_id].keys():
				if scene_name != "Mute":
					for param_name, param_value in track_data[track_id][scene_name].items():
						if not scene_name in {"Sequence"}:
							interval = get_interval(value_intervals, scene_name, param_name)
							if interval is None:
								value = param_value
							else:
								value = interval[0] + (interval[1]-interval[0])*float(param_value)/100
							self.set_param("/" + param_name + "_" + track_id, value)
						elif scene_name == "Sequence":
							self.set_param("/freq_" + track_id, list(map(lambda x: x if x==1 else "", track_data[track_id]["Sequence"]["freq"])))
				else:
					self.mute_track(track_id, track_data[track_id][scene_name])
		self.set_bpm(pattern["Global"]["bpm"])


if __name__=="__main__":
	sc_client = SuperColliderClient()

	sc_client.start_sequencer()

	sc_client.set_bpm(50)
	time.sleep(15)
	sc_client.set_bpm(200)

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		sc_client.stop()