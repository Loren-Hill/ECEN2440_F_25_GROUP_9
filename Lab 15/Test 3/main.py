from machine import Pin
import time
# Initializing LEDS
led1 = Pin(13, Pin.OUT, value =0)
led2 = Pin(12, Pin.OUT, value =0)
led3 = Pin(11, Pin.OUT, value =0)

while True:
    # Turns on the 3 leds in series, then turns them all off after 3 seconds
    led1.value(1)
    time.sleep(0.3)
    led2.value(1)
    time.sleep(0.3)
    led3.value(1)
    time.sleep(5)
    led1.value(0)
    led2.value(0)
    led3.value(0)
    time.sleep(1)