# catch-ssh.py - detect failed ssh attempts

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GREEN_LED = 18
RED_LED = 23
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.output(RED_LED, False)

def blink_led(led, duration):
    GPIO.output(led, True)
    time.sleep(duration)
    GPIO.output(led, False)

def follow(thefile):
    thefile.seek(0,2) # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1) # Sleep briefly
            continue
        yield line

if __name__ == "__main__":
    log = open("/var/log/auth.log")
    lines = follow(log)
    lines = (line for line in lines if "sshd" in line)

    for line in lines:
        if "Failed" in line:
            print("failed ssh attempt")
            blink_led(RED_LED, 1.0)


GPIO.cleanup()
