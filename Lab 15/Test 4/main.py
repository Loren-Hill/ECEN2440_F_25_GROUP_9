import math, time
import machine
# load the MicroPython pulse-width-modulation module for driving hardware
from machine import PWM

from machine import Pin

time.sleep(1) # Wait for USB to become ready
# Initialize LEDS
led1 = Pin(13, Pin.OUT, value =0)
led2 = Pin(12, Pin.OUT, value =0)
#led3 = Pin(11, Pin.OUT, value =0)

pwm_rate = 2000
# Motor 1
ain1_ph = Pin(18, Pin.OUT) # Initialize GP14 as an OUTPUT
ain2_en = PWM(19, freq = pwm_rate, duty_u16 = 0)
# Motor 2
ain3_ph = Pin(20, Pin.OUT) # Initialize GP14 as an OUTPUT
ain4_en = PWM(21, freq = pwm_rate, duty_u16 = 0)
pwm = min(max(int(2**16 * abs(1)), 0), 65535)

while True:
    print("Motor ON") # Print to REPL
    ain1_ph.low()
    ain2_en.duty_u16(pwm)
    ain3_ph.low()
    ain4_en.duty_u16(pwm)
    led1.value(1)
    led2.value(1)
    time.sleep(2)
    print("Motor OFF") # Print to REPL
    ain1_ph.low()
    ain2_en.duty_u16(0)
    ain3_ph.low()
    ain4_en.duty_u16(0)
    led1.value(0)
    led2.value(0)
    time.sleep(2)
