import tkinter as tk
from pattern import *
from pd_client import PdClient
from encoder import Encoder
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


current_param_frame_idx = 0
section_frames = None

def build_section(section_name, section_data):
	frame = tk.Frame(root, padx=10, pady=10)
	label1 = tk.Label(frame, text=section_name, bg="red", width=15, height=2)
	label1.grid(row=0, column=0, padx=5, pady=5)
	for i, e in enumerate(section_data.items()):
		label1 = tk.Label(frame, text=e[0], bg="red", width=15, height=2)
		label1.grid(row=int(i/4)+1, column=i%4*2, padx=5, pady=5)
		label2 = tk.Label(frame, textvariable=e[1], bg="red", width=15, height=2)
		label2.grid(row=int(i/4)+1, column=i%4*2+1, padx=5, pady=5)
	return frame


def menu_switch(direction, encoders, pattern):
	global current_param_frame_idx
	global section_frames
	section_frames[current_param_frame_idx].grid_forget()
	unbind_encoders(encoders)
	
	current_param_frame_idx += direction
	if current_param_frame_idx < 0:
		current_param_frame_idx = len(section_frames)-1
		
	current_param_frame_idx %= len(section_frames)
	section_frames[current_param_frame_idx].grid(row=1, column=0, padx=10, pady=10)
	frame_data = list(pattern.data.items())[current_param_frame_idx]
	bind_encoders(encoders, frame_data[0], frame_data[1])


def bind_pitch_keys(pd_client, offset):
	root.bind("1", lambda x: pd_client.set_param("pitch", offset + 1))
	root.bind("2", lambda x: pd_client.set_param("pitch", offset + 2))
	root.bind("3", lambda x: pd_client.set_param("pitch", offset + 3))
	root.bind("4", lambda x: pd_client.set_param("pitch", offset + 4))
	root.bind("5", lambda x: pd_client.set_param("pitch", offset + 5))
	root.bind("6", lambda x: pd_client.set_param("pitch", offset + 6))
	root.bind("7", lambda x: pd_client.set_param("pitch", offset + 7))
	root.bind("8", lambda x: pd_client.set_param("pitch", offset + 8))


def bind_keys(root, encoders, viewmodel, pd_client):
	root.bind("n", lambda x: menu_switch(-1, encoders, viewmodel))
	root.bind("m", lambda x: menu_switch(1, encoders, viewmodel))
	
	#encoder_keylist = "qwertzui"
	#for i, key in enumerate(encoder_keylist):
	#	amnt = -1 if i%2==0 else 1
	#	print(i//2, amnt, key)
	#	root.bind(str(key), lambda x: encoders[i//2].state_change(amnt))
	root.bind("q", lambda x: encoders[0].state_change(-1))
	root.bind("w", lambda x: encoders[0].state_change(1))
	
	root.bind("e", lambda x: encoders[1].state_change(-1))
	root.bind("r", lambda x: encoders[1].state_change(1))
	
	root.bind("t", lambda x: encoders[2].state_change(-1))
	root.bind("z", lambda x: encoders[2].state_change(1))
	
	root.bind("u", lambda x: encoders[3].state_change(-1))
	root.bind("i", lambda x: encoders[3].state_change(1))
	
	root.bind("a", lambda x: encoders[4].state_change(-1))
	root.bind("s", lambda x: encoders[4].state_change(1))
	
	root.bind("d", lambda x: encoders[5].state_change(-1))
	root.bind("f", lambda x: encoders[5].state_change(1))
	
	root.bind("g", lambda x: encoders[6].state_change(-1))
	root.bind("h", lambda x: encoders[6].state_change(1))
	
	root.bind("j", lambda x: encoders[7].state_change(-1))
	root.bind("k", lambda x: encoders[7].state_change(1))
	
	bind_pitch_keys(pd_client, 50)


def bind_encoders(encoders, section_name, param_names):
	bind_len = len(encoders) if len(encoders) < len(param_names) else len(param_names)
	param_names_ = list(param_names.items())
	for i in range(bind_len):
		encoders[i].section = section_name
		encoders[i].param = param_names_[i][0]


def unbind_encoders(encoders):
	for encoder in encoders:
		encoder.section = None
		encoder.param = None
		

pd_client = PdClient()
root = tk.Tk()
root.geometry("1200x500")
root.title("PdSynth")
ptn = Pattern(1,9,2,3,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)
viewmodel = ViewModel(pd_client, root, ptn)
encoders = [Encoder(my_pattern) for _ in range(8)] 


section_frames = []
for section_name, section_data in viewmodel.data.items():
	section_frames.append(build_section(section_name, section_data))

section_frames[current_param_frame_idx].grid(row=1, column=0, padx=10, pady=10)
frame_data = list(viewmodel.data.items())[current_param_frame_idx]
bind_encoders(encoders, frame_data[0], frame_data[1])


#main_label = tk.Label(root, text="Parameters", bg="blue", fg="white")
#main_label.grid(row=0, column=0, pady=10)


bind_keys(root, encoders, viewmodel, pd_client)

root.mainloop()
