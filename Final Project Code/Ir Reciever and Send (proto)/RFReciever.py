import machine
import activity
import MotorControl
import math, time
from machine import Pin


time.sleep(1) # Wait for USB to become ready

# Initializing RF
RF_A = Pin(7, Pin.IN, Pin.PULL_DOWN)
RF_B = Pin(6, Pin.IN, Pin.PULL_DOWN)
RF_C = Pin(5, Pin.IN, Pin.PULL_DOWN)
RF_D = Pin(4, Pin.IN, Pin.PULL_DOWN)
# set PWM max value
PWM_max = 65535

# Main 
def RF_Reciever():
    A = RF_A.value()
    B = RF_B.value()
    C = RF_C.value()
    D = RF_D.value()
    if A or B or C or D:
        activity.touch()
        #start = now
        if A: # Left Motor Forward
            print("Motor Forward Left") # Print to REPL
            # Left motor control
            power = int(PWM_max) # Later will multiply PWM_Max by a value from 0 to 1 to change speed
            # Direction, either 1 for forwards or 0 for backwards
            direction = 1
            MotorControl.Left_Motor_Control(power,direction)
        if B: # Right Motor Forward
            print("Motor Forward Right") # Print to REPL
            # Right motor control
            power = int(PWM_max) # Later will multiply PWM_Max by a value from 0 to 1 to change speed
            # Direction, either 1 for forwards or 0 for backwards
            direction = 1
            MotorControl.Right_Motor_Control(power,direction)         
        if C: # Left Motor Backwards
            print("Motor Backwards Left") # Print to REPL
            # Left motor control
            power = int(PWM_max) # Later will multiply PWM_Max by a value from 0 to 1 to change speed
            # Direction, either 1 for forwards or 0 for backwards
            direction = 0
            MotorControl.Left_Motor_Control(power,direction)
        if D: # Right Motor Backwards
            print("Motor Backwards Right") # Print to REPL
            # Right motor control
            power = int(PWM_max) # Later will multiply PWM_Max by a value from 0 to 1 to change speed
            # Direction, either 1 for forwards or 0 for backwards
            direction = 0
            MotorControl.Right_Motor_Control(power,direction) 
            