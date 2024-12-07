import tkinter as tk
from pattern import *

current_param_frame_idx = 0
section_frames = None

def build_section(section_data):
	frame = tk.Frame(root, bg="lightgray", padx=10, pady=10)
	label1 = tk.Label(frame, text=section_data[0], bg="red", width=15, height=2)
	label1.grid(row=0, column=0, padx=5, pady=5)
	for i, e in enumerate(section_data[1]):
		label1 = tk.Label(frame, text=e, bg="red", width=15, height=2)
		label1.grid(row=int(i/4)+1, column=i%4*2, padx=5, pady=5)
		label2 = tk.Label(frame, text=str(section_data[1][e]), bg="red", width=15, height=2)
		label2.grid(row=int(i/4)+1, column=i%4*2+1, padx=5, pady=5)
	return frame

def menu_switch(direction):
	global current_param_frame_idx
	global section_frames
	section_frames[current_param_frame_idx].grid_forget()
	#TODO: remove keybindings
	
	current_param_frame_idx += direction
	if current_param_frame_idx < 0:
		current_param_frame_idx = len(section_frames)-1
		
	current_param_frame_idx %= len(section_frames)
	section_frames[current_param_frame_idx].grid(row=1, column=0, padx=10, pady=10)
	#TODO: add keybindings


def bind_menu_keys(root):
	root.bind("l", lambda x: menu_switch(1))
	root.bind("j", lambda x: menu_switch(-1))


my_pattern = Pattern(1,9,2,3,4,1,1,1,1,1,1,1,1,1,1,1,1)

root = tk.Tk()
root.title("PdSynth")

section_frames = []
for section_data in my_pattern.get_sections():
	section_frames.append(build_section(section_data))

section_frames[current_param_frame_idx].grid(row=1, column=0, padx=10, pady=10)

main_label = tk.Label(root, text="Parameters", bg="blue", fg="white")
main_label.grid(row=0, column=0, pady=10)


bind_menu_keys(root)

root.mainloop()
