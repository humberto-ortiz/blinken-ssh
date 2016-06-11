# blinken-ssh
Use a raspberry pi 3 and LED to alert about failed ssh attempts.


## Introduction

The ssh protocol is in wide use on the Internet to allow secure access
to servers. The raspberry pi is a small, inexpensive computer that can
be programmed to control devices in the real world. This exercise will
build a detector of failed ssh connections to a raspberry pi.

It was adapted from this adafruit tutorial on
[checking mail and turning on LEDs](https://learn.adafruit.com/raspberry-pi-e-mail-notifier-using-leds/overview).

## Methods

### SSH

ssh logs successful and failed attempts to `/var/log/auth.log` on the
pi.

```{text}
$ grep sshd /var/log/auth.log
May  5 08:42:56 raspberrypi sshd[21479]: Failed password for pi from 10.0.1.4 port 65157 ssh2
May  5 08:43:09 raspberrypi sshd[21479]: Failed password for pi from 10.0.1.4 port 65157 ssh2
May  5 08:43:33 raspberrypi sshd[21479]: Failed password for pi from 10.0.1.4 port 65157 ssh2
May  5 08:44:17 raspberrypi sshd[21523]: Accepted password for pi from 10.0.1.4 port 65174 ssh2
May  5 08:54:34 raspberrypi sshd[23682]: Accepted publickey for pi from 10.0.1.4 port 65320 ssh2
```

It looks like no matter the method of authentication, we can just
check for sshd logs that say "Failed" or "Accepted".

### LED

Following the tutorial on blinking leds, I constructed a circuit with
a red LED on pin 23 on the pi. You want to connect a jumper to GPIO
pin 23 and a jumper to ground. See the
[online diagram](http://pinout.xyz/). Pin 23 should run to the long
wire of the LED, and the short wire to GND. Connect a resistor in
series with the LED to prevent it from shorting out.

We can set up code to initialize the leds to off, and to blink a
specified led.

```{python}
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
RED_LED = 23
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.output(RED_LED, False)

def blink_led(led, duration):
    GPIO.output(led, True)
    time.sleep(duration.0)
    GPIO.output(led, False)
```

We're going to use [python generators](http://www.dabeaz.com/generators/Generators.pdf) to produce a *stream*, an infinite
list of sshd log entries from `/var/log/auth.log`. If these lines
match "Failed" we blink the red LED.

```{python}
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
            blink_led(RED_LED, 0.5)

GPIO.cleanup()
```

## Results

This program loops forever, waiting for failed ssh login attempts and
blinking the LED.

## Discussion

I like the program, and python generators are a lot cooler than I thought.

## References

1. <https://learn.adafruit.com/raspberry-pi-e-mail-notifier-using-leds/overview>

1. <http://www.dabeaz.com/generators/Generators.pdf>


## Scanning Script

https://github.com/WSTNPHX/scripts-n-tools/blob/master/sshscan.py
