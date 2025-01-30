
from pynput.keyboard import Listener

def on_press(key):
    print(f"Key {key} pressed")

listener = Listener(on_press=on_press, suppress=True)
listener.start()


while True:
    pass
listener.join()
'''
import keyboard
keyboard.add_hotkey('m', lambda: print("asd"))

while(True):
    pass

'''