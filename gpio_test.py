import RPi.GPIO as GPIO
import time

print(GPIO.__name__)
print(dir(GPIO))

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
#print(GPIO.RPI_INFO)

while True:
	GPIO.output(17,GPIO.LOW)
	time.sleep(500)
	GPIO.output(17,GPIO.LOW)
	time.sleep(500)
	
# https://bobrathbone.com/raspberrypi/gpio_converter.html
# https://github.com/bobrathbone/GPIOconverter
