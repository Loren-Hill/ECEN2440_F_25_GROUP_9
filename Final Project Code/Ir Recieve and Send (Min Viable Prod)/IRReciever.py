# Rename to main.py if Recieving 
import ir_rx
import machine
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

# This is Motor Code
# Start ticker from code start
start = time.ticks_ms()

pwm_rate = 2000
#change pins if needed
Left_Motor = Pin(LMotor, Pin.OUT) # 
Left_Motor_PWM = PWM(LMotorPWM, freq = pwm_rate, duty_u16 = 0)
# Right Motors
Right_Motor = Pin(RMotor, Pin.OUT) # 
Right_Motor_PWM = PWM(RMotorPWM, freq = pwm_rate, duty_u16 = 0)

pwm = min(max(int(2**16 * abs(1)), 0), 65535)



# Callback function to execute when an IR code is received

def ir_callback(data, addr, _):
    # Start ticker from code start, every 300 ms turn off motors
    global start
    start = time.ticks_ms()
    if (data == 0):
        print("Motor Forward") # Print to REPL
        Left_Motor.low() 
        Left_Motor_PWM.duty_u16(pwm) 
        Right_Motor.low() 
        Right_Motor_PWM.duty_u16(pwm) 
    elif (data == 1):
        print("Motor Backwards") # Print to REPL
        Left_Motor.high() 
        Left_Motor_PWM.duty_u16(pwm)
        Right_Motor.high() 
        Right_Motor_PWM.duty_u16(pwm) 
    elif (data == 2):   
        print("Right Turn") # Print to REPL
        Left_Motor.high()
        Left_Motor_PWM.duty_u16(pwm)
        Right_Motor.low() 
        Right_Motor_PWM.duty_u16(pwm)
    elif (data == 3): 
        print("Left Turn") # Print to REPL
        Left_Motor.low()
        Left_Motor_PWM.duty_u16(pwm)
        Right_Motor.high() 
        Right_Motor_PWM.duty_u16(pwm) 
    elif (data == 4):
        print("Off") # Print to REPL
        Left_Motor.low()
        Left_Motor_PWM.duty_u16(0)
        Right_Motor.low() 
        Right_Motor_PWM.duty_u16(0)            
    else: 
        print("no idea what that is")

# This Is reciever Code

# Setup the IR receiver
ir_pin = Pin(IRRPin, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wirin

ir_receiver = NEC_8(ir_pin, callback=ir_callback)



while True:
    
    now = time.ticks_ms()
# Will count how long in between each signal, if that is over 300 ms, stop all motors.
    if (time.ticks_diff(now,start) >= 300):
        print("Motor off") # Print to REPL
        Left_Motor.low() 
        Left_Motor_PWM.duty_u16(0) 
        Right_Motor.low() 
        Right_Motor_PWM.duty_u16(0)
        # Reset timer
        start = now
    # sleep as to not slam cpu
    time.sleep_ms(50)
