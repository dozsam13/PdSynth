import tkinter as tk
from pattern import *
# Create the main application window

def build_section(frame, section):
	for i, e in enumerate(section):
		label1 = tk.Label(frame, text=e, bg="red", width=15, height=2)
		label1.grid(row=int(i/4), column=i%4*2, padx=5, pady=5)
		label2 = tk.Label(frame, text=str(section[e]), bg="red", width=15, height=2)
		label2.grid(row=int(i/4), column=i%4*2+1, padx=5, pady=5)

my_pattern = Pattern(1,9,2,3,4,1,1,1,1,1,1,1,1,1,1,1,1)

root = tk.Tk()
root.title("PdSynth")

# Create a frame to hold widgets
main_frame = tk.Frame(root, bg="lightgray", padx=10, pady=10)
main_frame.grid(row=0, column=0, padx=10, pady=10)

build_section(main_frame, my_pattern.main_section)

# Add additional widgets to the main window if needed
main_label = tk.Label(root, text="Main Window Label", bg="blue", fg="white")
main_label.grid(row=1, column=0, pady=10)

# Run the Tkinter event loop
root.mainloop()
