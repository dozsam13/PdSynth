import RPi.GPIO as GPIO
import time

print(GPIO.__name__)
print(dir(GPIO))

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
#print(GPIO.RPI_INFO)
kaki=GPIO.PWM(17,10)
kaki.start(50)
kaki2=0

while True:
	kaki.ChangeDutyCycle(float(kaki2))
	kaki2 += 13
	kaki2 %= 100
	time.sleep(0.5)

# https://bobrathbone.com/raspberrypi/gpio_converter.html
# https://github.com/bobrathbone/GPIOconverter
