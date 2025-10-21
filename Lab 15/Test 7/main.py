import math, time
import ir_rx
import machine
# load the MicroPython pulse-width-modulation module for driving hardware
import math, time
from machine import Pin
from machine import PWM
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging


time.sleep(1) # Wait for USB to become ready

pwm_rate = 2000
# Initializing LEDS
LED1 = Pin(13,Pin.OUT, value = 0)
LED2 = Pin(14,Pin.OUT, value = 0)
LED3 = Pin(15,Pin.OUT, value = 0)
# Initializing motor 
# Motor 1
ain1_ph = Pin(16, Pin.OUT) # Initialize GP14 as an OUTPUT
ain2_en = PWM(17, freq = pwm_rate, duty_u16 = 0)
# Motor 2
ain3_ph = Pin(18, Pin.OUT) # Initialize GP14 as an OUTPUT
ain4_en = PWM(19, freq = pwm_rate, duty_u16 = 0)


pwm = min(max(int(2**16 * abs(1)), 0), 65535)
# Callback function to execute when an IR code is received

def ir_callback(data, addr, _):
    # print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")
    if (data == 1):
        print("LED 1:Motor Forward") # Print to REPL
        # Turn LED on
        LED1.value(1)
        ain1_ph.low()
        ain2_en.duty_u16(int(pwm*0.5))
        ain3_ph.low()
        ain4_en.duty_u16(int(pwm*0.5))
        time.sleep(2)
        LED1.value(0)
        
    elif (data == 2):
        print("LED 2:Motor Backwords") # Print to REPL
        # Turn LED on
        LED2.value(1)
        ain1_ph.high()
        ain2_en.duty_u16(int(pwm*0.5))
        ain3_ph.high()
        ain4_en.duty_u16(int(pwm*0.5))
        time.sleep(2)
        LED2.value(0)
        
    elif (data == 3):
        print("LED 3:Motor Off") # Print to REPL
        # Turn LED on and off
        LED3.value(1)
        ain1_ph.low()   
        ain2_en.duty_u16(0)
        ain3_ph.low()
        ain4_en.duty_u16(0)
        time.sleep(2)
        LED3.value(0)
    else: 
        print("no idea what that is")
         

# This Is reciever Code

# Setup the IR receiver
ir_pin = Pin(20, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wirin

ir_receiver = NEC_8(ir_pin, callback=ir_callback)
# Optional: Use the print_error function for debugging

ir_receiver.error_function(print_error)


while True:
    pass # Execution is interrupt-driven, so just keep the script aliv