import tkinter as tk
from encoder import Encoder


class View:
	def __init__(self, viewmodel=None):
		root = tk.Tk()
		root.geometry("1200x500")
		#root.attributes('-fullscreen', True)
		root.title("PdSynth")
		self.root = root
		self.current_param_frame_idx = 0
		self.section_frames = []
		self.viewmodel = viewmodel
		self.encoders = []


	def build(self, viewmodel):
		self.viewmodel = viewmodel
		self.encoders = [Encoder(viewmodel) for _ in range(8)] 

		for section_name, section_data in viewmodel.data.items():
			self.section_frames.append(self.build_section(section_name, section_data))

		self.section_frames[self.current_param_frame_idx].grid(row=1, column=0, padx=10, pady=10)
		frame_data = list(self.viewmodel.data.items())[self.current_param_frame_idx]
		self.bind_encoders(frame_data[0], frame_data[1])

		self.bind_keys()

		self.root.mainloop()


	def build_section(self, section_name, section_data):
		frame = tk.Frame(self.root, padx=10, pady=10)
		label1 = tk.Label(frame, text=section_name, bg="red", width=15, height=2)
		label1.grid(row=0, column=0, padx=5, pady=5)
		for i, e in enumerate(section_data.items()):
			label1 = tk.Label(frame, text=e[0], bg="red", width=15, height=2)
			label1.grid(row=int(i/4)+1, column=i%4*2, padx=5, pady=5)
			label2 = tk.Label(frame, textvariable=e[1], bg="red", width=15, height=2)
			label2.grid(row=int(i/4)+1, column=i%4*2+1, padx=5, pady=5)
		return frame


	def menu_switch(self, direction):
		self.section_frames[self.current_param_frame_idx].grid_forget()
		self.unbind_encoders()
		
		self.current_param_frame_idx += direction
		self.current_param_frame_idx %= len(self.section_frames)
		self.section_frames[self.current_param_frame_idx].grid(row=1, column=0, padx=10, pady=10)
		frame_data = list(self.viewmodel.data.items())[self.current_param_frame_idx]
		self.bind_encoders(frame_data[0], frame_data[1])



	def bind_keys(self):
		self.root.bind("n", lambda x: self.menu_switch(-1))
		self.root.bind("m", lambda x: self.menu_switch(1))
		
		encoder_keylist = "qwertzui"
		for i, key in enumerate(encoder_keylist):
			amnt = int(i%2!=0)*2-1 
			def make_lambda(encoders, i, amnt):
				return lambda x: encoders[i//2].state_change(amnt)
			
			self.root.bind(str(key), make_lambda(self.encoders, i, amnt))

		self.root.bind("0", lambda x: self.change_keyboard_state())
		self.bind_pitch_keys()
		

	def change_keyboard_state(self):
		self.viewmodel.keyboard_state = (self.viewmodel.keyboard_state+1) % 2
		print(self.viewmodel.keyboard_state)
		if self.viewmodel.keyboard_state == 0:
			self.unbind_keys()
			self.bind_pitch_keys()
		else:
			self.unbind_keys()
			self.bind_seq_keys()

	def bind_seq_keys(self):
		for i in range(1,9):
			def make_lambda(i):
				return lambda x: self.viewmodel.seq_step(i)
			self.root.bind(str(i), make_lambda(i))

	def unbind_keys(self):
		for i in range(1,9):
			def make_lambda(i):
				return lambda x: self.viewmodel.seq_step(i)
			self.root.unbind(str(i))

	def bind_pitch_keys(self):
		for i in range(1,9):
			def make_lambda(i):
				return lambda x: self.viewmodel.play_pitch(i)
			self.root.bind(str(i), make_lambda(i))

	def bind_encoders(self, section_name, param_names):
		bind_len = len(self.encoders) if len(self.encoders) < len(param_names) else len(param_names)
		param_names_ = list(param_names.items())
		for i in range(bind_len):
			self.encoders[i].section = section_name
			self.encoders[i].param = param_names_[i][0]


	def unbind_encoders(self):
		for encoder in self.encoders:
			encoder.section = None
			encoder.param = None
		









