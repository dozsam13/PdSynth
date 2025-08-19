import RPi.GPIO as GPIO
import time
from gpiozero import RotaryEncoder

			
class GPIOZeroEncoder:
	def __init__(self, clk_pin, dt_pin, app_encoder = None):
		encoder = RotaryEncoder(a=clk_pin, b=dt_pin, max_steps=100000, wrap=True)
		self.encoder = encoder
		if app_encoder is not None:
			encoder.when_rotated_clockwise = lambda: app_encoder.state_change(1)
			encoder.when_rotated_counter_clockwise = lambda: app_encoder.state_change(-1)
