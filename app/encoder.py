import RPi.GPIO as GPIO
import time


class RPIEncoder:
    def __init__(self, clk_pin, dt_pin, sw_pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(clk_pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.setup(dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.counter = 0
        self.clk_state = 0
        self.clk_pin = clk_pin
        self.dt_pin = dt_pin
        self.sw_pin = sw_pin
        self.prev_clk_state = GPIO.input(clk_pin)
    
    def callback(self, channel):
        clk_state = GPIO.input(self.clk_pin)
        dt_state = GPIO.input(self.dt_pin)
        #if clk_state != self.prev_clk_state and clk_state == GPIO.HIGH:
        #    self.counter += (dt_state != clk_state) * 2 -1
        self.counter += (dt_state == GPIO.HIGH)*2-1
        #self.prev_clk_state = clk_state
        print("counter: {}, dir: {}, dt_state: {}, clk_state: {}".format(self.counter, (dt_state != clk_state) * 2 -1, dt_state, clk_state))

def test_class():
    try:        
        encoder = RPIEncoder(13, 6, 23)
        GPIO.add_event_detect(encoder.clk_pin, GPIO.RISING, callback=encoder.callback, bouncetime=10)

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
            GPIO.cleanup()  # Clean up GPIO on program exit

def main():
    # Pin numbers on Raspberry Pi
    #TOP RIGHT elso 
    #CLK_PIN = 12   # GPIO7 connected to the rotary encoder's CLK pin
    #DT_PIN = 20    # GPIO8 connected to the rotary encoder's DT pin
    #SW_PIN = 16   # GPIO25 connected to the rotary encoder's SW pin

    #4 17
    #5 27 szar
    #13 6 kicsit szar (a 6os pin szar ha berakom clocknak, egyfolytaban olvas...)
    #19 26 szar
    CLK_PIN = 13   # GPIO7 connected to the rotary encoder's CLK pin
    DT_PIN = 6  # GPIO8 connected to the rotary encoder's DT pin
    SW_PIN = 16 
    DIRECTION_CW = 0
    DIRECTION_CCW = 1

    counter = 0
    direction = DIRECTION_CW
    CLK_state = 0
    prev_CLK_state = 0

    button_pressed = False
    prev_button_state = GPIO.HIGH
    # Configure GPIO pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CLK_PIN, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    prev_CLK_state = GPIO.input(CLK_PIN)

    try:
        while True:
            CLK_state = GPIO.input(CLK_PIN)
            #print(CLK_state, " ", GPIO.input(DT_PIN))

            # If the state of CLK is changed, then pulse occurred
            # React to only the rising edge (from LOW to HIGH) to avoid double count
            if CLK_state != prev_CLK_state and CLK_state == GPIO.HIGH:
                # If the DT state is HIGH, the encoder is rotating in counter-clockwise direction
                # Decrease the counter
                DT_state = GPIO.input(DT_PIN)
                if DT_state == GPIO.HIGH:
                    counter -= 1
                    direction = DIRECTION_CCW
                else:
                    # The encoder is rotating in clockwise direction => increase the counter
                    counter += 1
                    direction = DIRECTION_CW
                print("CLK_STATE: {} PREV_CLK_STATE: {} DT_state: {}".format(CLK_state, prev_CLK_state, DT_state))
                print("Rotary Encoder:: direction:", "CLOCKWISE" if direction == DIRECTION_CW else "ANTICLOCKWISE",
                      "- count:", counter)

            # Save last CLK state
            prev_CLK_state = CLK_state

            # State change detection for the button
            button_state = GPIO.input(SW_PIN)
            if button_state != prev_button_state:
                time.sleep(0.01)  # Add a small delay to debounce
                if button_state == GPIO.LOW:
                    print("The button is pressed")
                    button_pressed = True
                else:
                    button_pressed = False

            prev_button_state = button_state

    except KeyboardInterrupt:
        GPIO.cleanup()  # Clean up GPIO on program exit

if __name__ == "__main__":
    #main()
    test_class()
