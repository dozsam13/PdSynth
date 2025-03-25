from pythonosc import udp_client
import time
import threading

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

	def stop(self):
		self.osc_server.shutdown()
		#self.osc_server_thread.join()




if __name__=="__main__":
	sc_client = SuperColliderClient()

	#sc_client.start_sequencer()
	#sc_client.set_param("/freq_1", [0, "", "", "",0, "", "", "", 0, "", 0, "", 0, "", "", ""])
	#sc_client.set_param("/freq_1", [0, "", "", ""])
	sc_client.stop_sequencer()
	exit()

	sc_client.set_bpm(50)
	time.sleep(15)
	sc_client.set_bpm(200)

	try:
		while True:
			time.sleep(1)
			print("loop")
	except KeyboardInterrupt:
		sc_client.stop()