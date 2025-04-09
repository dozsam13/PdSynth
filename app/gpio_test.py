#!/usr/bin/env python2.7
#
# file: wait_for_edge-falling-ramp-fix.py
#
# wait_for_edge solution for slowly falling ramps
# a falling edge is detected at approx. 1.16V
#
# The input pin should be defined as active low.
#

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

Input_Sig = 23 # any plain GPIO pin
# if the pin has a pull-up, you can remove the one below
GPIO.setup(Input_Sig, GPIO.IN, pull_up_down=GPIO.PUD_UP)

valid_edge = True


def main():
    global valid_edge

    try:
        while True:
            pass # your code

            # setup the event recognition, (you can set a timeout)
            GPIO.wait_for_edge(Input_Sig, GPIO.FALLING)

            # if we're here, the event happened
            if valid_edge == True :
                # only the first event is valid
                # check if we have a logical low (falling edge)
                if GPIO.input(Input_Sig) == 0:
                    print "FALLING"
                    valid_edge = False
            # if we are back at a logical 1, reset the cycle
            if GPIO.input(Input_Sig) == 1:
                valid_edge = True

    except KeyboardInterrupt:
        pass
    finally:
        print "\nRelease the used pin(s)"
        GPIO.cleanup([Input_Sig])


if __name__ == '__main__':
    main()
