import tkinter as tk
from pattern import *
from pd_client import PdClient
from encoder import Encoder
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


current_param_frame_idx = 0
section_frames = None
current_pattern_idx = 0

def build_section(root, section_name, section_data):
	frame = tk.Frame(root, padx=10, pady=10)
	label1 = tk.Label(frame, text=section_name, bg="red", width=15, height=2)
	label1.grid(row=0, column=0, padx=5, pady=5)
	for i, e in enumerate(section_data.items()):
		label1 = tk.Label(frame, text=e[0], bg="red", width=15, height=2)
		label1.grid(row=int(i/4)+1, column=i%4*2, padx=5, pady=5)
		label2 = tk.Label(frame, textvariable=e[1], bg="red", width=15, height=2)
		label2.grid(row=int(i/4)+1, column=i%4*2+1, padx=5, pady=5)
	return frame

def build_pattern_section(root, ptns):
	frame = tk.Frame(root, padx=10, pady=10)
	label1 = tk.Label(frame, text="Patterns", bg="red", width=15, height=2)
	label1.grid(row=0, column=0, padx=5, pady=5)
	label1 = tk.Label(frame, text=e[0], bg="red", width=15, height=2)
	label1.grid(row=int(i/4)+1, column=i%4*2, padx=5, pady=5)
	label2 = tk.Label(frame, textvariable=e[1], bg="red", width=15, height=2)
	label2.grid(row=int(i/4)+1, column=i%4*2+1, padx=5, pady=5)

	return frame

def menu_switch(direction, encoders, viewmodel):
	global current_param_frame_idx
	global section_frames
	section_frames[current_param_frame_idx].grid_forget()
	unbind_encoders(encoders)
	
	current_param_frame_idx += direction
	if current_param_frame_idx < 0:
		current_param_frame_idx = len(section_frames)-1
		
	current_param_frame_idx %= len(section_frames)
	section_frames[current_param_frame_idx].grid(row=1, column=0, padx=10, pady=10)
	frame_data = list(viewmodel.data.items())[current_param_frame_idx]
	bind_encoders(encoders, frame_data[0], frame_data[1])


def bind_pitch_keys(root, engine_client, offset):
	for i in range(1,9):
		def make_lambda(engine_client, offset, i):
			return lambda x: engine_client.set_param("pitch", offset + i)
		root.bind(str(i), make_lambda(engine_client, offset, i))
	

def bind_keys(root, encoders, viewmodel, engine_client):
	root.bind("n", lambda x: menu_switch(-1, encoders, viewmodel))
	root.bind("m", lambda x: menu_switch(1, encoders, viewmodel))
	
	encoder_keylist = "qwertzui"
	for i, key in enumerate(encoder_keylist):
		amnt = int(i%2!=0)*2-1 
		print(i//2, amnt, key)
		def make_lambda(encoders, i, amnt):
			return lambda x: encoders[i//2].state_change(amnt)
		
		root.bind(str(key), make_lambda(encoders, i, amnt))


	bind_pitch_keys(root, engine_client, 50)


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
		
def read_patterns():
	return [Pattern("Pattern1", 1,9,2,3,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1), Pattern("Pattern2", 1,9,2,3,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2)]

def main():
	global section_frames
	global current_param_frame_idx
	global current_pattern_idx

	engine_client = PdClient()
	root = tk.Tk()
	root.geometry("1200x500")
	#root.attributes('-fullscreen', True)
	root.title("PdSynth")


	ptns = read_patterns()
	viewmodel = ViewModel(engine_client, root, ptns, current_pattern_idx)
	encoders = [Encoder(viewmodel) for _ in range(8)] 

	section_frames = []
	for section_name, section_data in viewmodel.data.items():
		section_frames.append(build_section(root, section_name, section_data))

	section_frames[current_param_frame_idx].grid(row=1, column=0, padx=10, pady=10)
	frame_data = list(viewmodel.data.items())[current_param_frame_idx]
	bind_encoders(encoders, frame_data[0], frame_data[1])


	#main_label = tk.Label(root, text="Parameters", bg="blue", fg="white")
	#main_label.grid(row=0, column=0, pady=10)


	bind_keys(root, encoders, viewmodel, engine_client)

	root.mainloop()

if __name__ == "__main__":
	main()

