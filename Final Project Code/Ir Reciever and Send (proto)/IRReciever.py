# Code of IR Reciever
import ir_rx
import machine
# load the MicroPython pulse-width-modulation module for driving hardware
import activity
import MotorControl
import math, time
from machine import Pin
from machine import PWM
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging

time.sleep(1) # Wait for USB to become ready
# CHANGE VARIABLES TO WHAT YOUR PINOUT IS

IRRPin = 18
# What the device address is
device_ad = 0xff

# Set Control_law and mode for this file
RF_Control = 0
IR_Control = 1

Control_Law = IR_Control  # default value

def set_mode(mode):
    global Control_Law
    Control_Law = mode

# Function for motor movement upon recieving IR Code
# set PWM max value
PWM_max = 65535

def IR_Motor(data, addr, _):
    global PWM_max
    # Handles 4 inputs for forward, backwards, left, and right.
    # Handler for if no signal recieved
    activity.touch()

    if (data == 0 and addr == device_ad):
        print("Motor Forward") # Print to REPL
        # Set both motors Forwards at max speed
        # Left motor control
        power = int(PWM_max) # Later will multiply PWM_Max by a value from 0 to 1 to change speed
            # Direction, either 1 for forwards or 0 for backwards
        direction = 1 
        MotorControl.Left_Motor_Control(power,direction)
        # Right Motor Control
        power = int(PWM_max) # Later will multiply PWM_Max by a value from 0 to 1 to change speed
            # Direction, either 1 for forwards or 0 for backwards
        direction = 1
        MotorControl.Right_Motor_Control(power,direction)
    elif (data == 1 and addr == device_ad):
        print("Motor Backwards") # Print to REPL
        # Set both motors backwards at max speed
        # Left motor control
        power = int(PWM_max) # Later will multiply PWM_Max by a value from 0 to 1 to change speed
            # Direction, either 1 for forwards or 0 for backwards
        direction = 0
        MotorControl.Left_Motor_Control(power,direction)
        # Right Motor Control
        power = int(PWM_max) # Later will multiply PWM_Max by a value from 0 to 1 to change speed
            # Direction, either 1 for forwards or 0 for backwards
        direction = 0
        MotorControl.Right_Motor_Control(power,direction)
    elif (data == 2 and addr == device_ad):   
        print("Right Turn") # Print to REPL
        # Sets left motor forward, right motor backwards
        # Left motor control
        power = int(PWM_max) # Later will multiply PWM_Max by a value from 0 to 1 to change speed
            # Direction, either 1 for forwards or 0 for backwards
        direction = 1 
        MotorControl.Left_Motor_Control(power,direction)
        # Right Motor Control
        power = int(PWM_max) # Later will multiply PWM_Max by a value from 0 to 1 to change speed
            # Direction, either 1 for forwards or 0 for backwards
        direction = 0
        MotorControl.Right_Motor_Control(power,direction)
    elif (data == 3 and addr == device_ad): 
        print("Left Turn") # Print to REPL
        # Sets right motor forward and left motor backwards
        # Left motor control
        power = int(PWM_max) # Later will multiply PWM_Max by a value from 0 to 1 to change speed
            # Direction, either 1 for forwards or 0 for backwards
        direction = 0
        MotorControl.Left_Motor_Control(power,direction)
        # Right Motor Control
        power = int(PWM_max) # Later will multiply PWM_Max by a value from 0 to 1 to change speed
            # Direction, either 1 for forwards or 0 for backwards
        direction = 1
        MotorControl.Right_Motor_Control(power,direction)
    elif (data == 4 and addr == device_ad):
        MotorControl.Motor_Off() 

# Function for turning motors off




# Function for IR interrupt
def ir_callback(data, addr, _):
    # Checking if IR is current mode
    global Control_Law
    if Control_Law != IR_Control:
        # We're not in IR mode, so ignore this command
        return
    
    # Call motor functino
    IR_Motor(data,addr, _)

# Setup the IR receiver
ir_pin = Pin(IRRPin, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wirin

ir_receiver = NEC_8(ir_pin, callback=ir_callback)