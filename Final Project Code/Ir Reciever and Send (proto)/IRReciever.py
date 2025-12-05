# Code of IR Reciever
import ir_rx
import machine
import main
# load the MicroPython pulse-width-modulation module for driving hardware
import math, time
from machine import Pin
from machine import PWM
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging

time.sleep(1) # Wait for USB to become ready
# CHANGE VARIABLES TO WHAT YOUR PINOUT IS
# Pinout variables
LMotor = 12
LMotorPWM = 13
RMotor = 14
RMotorPWM = 15

IRRPin = 18
# What the device address is
device_ad = 0xff

# This is Motor Code
# Start ticker from code start
last_input = time.ticks_ms()

pwm_rate = 2000
#change pins if needed
Left_Motor = Pin(LMotor, Pin.OUT) # 
Left_Motor_PWM = PWM(LMotorPWM, freq = pwm_rate, duty_u16 = 0)
# Right Motors
Right_Motor = Pin(RMotor, Pin.OUT) # 
Right_Motor_PWM = PWM(RMotorPWM, freq = pwm_rate, duty_u16 = 0)

pwm = min(max(int(2**16 * abs(1)), 0), 65535)

# Function for motor movement upon recieving IR Code

def IR_Motor(data, addr, _):
    # Handles 4 inputs for forward, backwards, left, and right.
    # Start ticker from code start, every 300 ms turn off motors
    global last_input
    last_input = time.ticks_ms()
    if (data == 0 and addr == device_ad):
        print("Motor Forward") # Print to REPL
        Left_Motor.low() 
        Left_Motor_PWM.duty_u16(pwm) 
        Right_Motor.low() 
        Right_Motor_PWM.duty_u16(pwm) 
    elif (data == 1 and addr == device_ad):
        print("Motor Backwards") # Print to REPL
        Left_Motor.high() 
        Left_Motor_PWM.duty_u16(pwm)
        Right_Motor.high() 
        Right_Motor_PWM.duty_u16(pwm) 
    elif (data == 2 and addr == device_ad):   
        print("Right Turn") # Print to REPL
        Left_Motor.high()
        Left_Motor_PWM.duty_u16(pwm)
        Right_Motor.low() 
        Right_Motor_PWM.duty_u16(pwm)
    elif (data == 3 and addr == device_ad): 
        print("Left Turn") # Print to REPL
        Left_Motor.low()
        Left_Motor_PWM.duty_u16(pwm)
        Right_Motor.high() 
        Right_Motor_PWM.duty_u16(pwm) 
    elif (data == 4 and addr == device_ad):
        Motor_Off() 

# Function for turning motors off
def Motor_Off ():
    print("Off") # Print to REPL
    Left_Motor.low()
    Left_Motor_PWM.duty_u16(0)
    Right_Motor.low() 
    Right_Motor_PWM.duty_u16(0)

# Function to handle 
def No_Signal():
    global last_input
    now = time.ticks_ms()
# Will count how long in between each signal, if that is over 300 ms, stop all motors.
    if (time.ticks_diff(now,last_input) >= 300):
        Motor_Off()
        # Reset timer
        last_input = now
    # sleep as to not slam cpu
    time.sleep_ms(50)

# Function for IR interrupt
def ir_callback(data, addr, _):
    global last_input, Control_Law
    if Control_Law != MODE_IR:
        # We're not in IR mode, so ignore this command
        return
    # Call motor functino
    IR_Motor(data,addr, _)

# Setup the IR receiver
ir_pin = Pin(IRRPin, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wirin

ir_receiver = NEC_8(ir_pin, callback=ir_callback)
