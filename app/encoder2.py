import lgpio
import time
from gpiozero import RotaryEncoder
from signal import pause

# Pin configuration (BCM numbering)
CLK_PIN = 5  # Encoder pin A (CLK)
DT_PIN = 27   # Encoder pin B (DT)
#SW_PIN = 27   # Push button (optional)

class LGPIOEncoder:
	def __init__(self, CLK_PIN, DT_PIN):
		self.counter = 0
		handle = lgpio.gpiochip_open(0)
		self.handle = handle
		self.CLK_PIN = CLK_PIN
		self.DT_PIN = DT_PIN
		lgpio.gpio_claim_input(handle, self.CLK_PIN, 32)
		lgpio.gpio_claim_input(handle, self.DT_PIN, 32)
		print("asd")

	def encoder_callback(self, handle, pin, level, tick):
		print("kurva")
		clk_state = lgpio.gpio_read(handle, self.CLK_PIN)
		dt_state = lgpio.gpio_read(handle, self.DT_PIN)
		if dt_state == 0:
			self.counter += 1
			direction = "Clockwise"
		else:
			self.counter -= 1
			direction = "Counter-Clockwise"
		print(f"Counter: {self.counter} CLK: {clk_state} DT: {dt_state}")

	def start(self):
		try:
			print("ddd")
			lgpio.callback(self.handle, self.CLK_PIN, lgpio.FALLING_EDGE, self.encoder_callback)
			while True:
				time.sleep(1)

		except KeyboardInterrupt:
			self.cleanup()

	def cleanup(self):
		if self.handle:
			lgpio.callback_cancel(self.handle, CLK_PIN)
			lgpio.callback_cancel(self.handle, SW_PIN)
			lgpio.gpiochip_close(self.handle)
		print("\nCleaned up and exited")
		

def rotated_clockwise():
    print(f"Clockwise - Position: {encoder.steps}")

def rotated_counter_clockwise():
    print(f"Counter-clockwise - Position: {encoder.steps}")
		
if __name__ == "__main__":
	#encoder = LGPIOEncoder(CLK_PIN, DT_PIN)
	#encoder.start()
	
	encoder = RotaryEncoder(a=CLK_PIN, b=DT_PIN, max_steps=100000)
	encoder.when_rotated_clockwise = rotated_clockwise
	encoder.when_rotated_counter_clockwise = rotated_counter_clockwise
	
	pause()
