from pythonosc import udp_client

UDP_IP = "127.0.0.1"
UDP_PORT = 3333
MESSAGE = b"freqRoute 3"

client = udp_client.SimpleUDPClient(UDP_IP, UDP_PORT)
client.send_message("/seq_start_stop", 1)
