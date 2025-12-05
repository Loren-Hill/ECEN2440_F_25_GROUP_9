# Code that controls motor functions 
import machine
import math, time
from machine import Pin
from machine import PWM

# Setting up motors
    # Pins
# Pinout variables
LMotor = 12
LMotorPWM = 13
RMotor = 14
RMotorPWM = 15
    # PWM
pwm_rate = 2000
#change pins if needed
Left_Motor = Pin(LMotor, Pin.OUT) # 
Left_Motor_PWM = PWM(LMotorPWM, freq = pwm_rate, duty_u16 = 0)
# Right Motors
Right_Motor = Pin(RMotor, Pin.OUT) # 
Right_Motor_PWM = PWM(RMotorPWM, freq = pwm_rate, duty_u16 = 0)


# Mapping for left and right motors,
    # For left, High is Forwards and Low is Backwards
    # For right, High is Backwards and Low is Forwards

# Takes power value for PWM and a direction for high or low.
def Left_Motor_Control(power,direction):
    # Normalize direction variable
    direction = 1 if direction else 0 
    # Set a max value for power
    power = max(0, min(int(power), 65535)) 
    # Apply values to motor
    Left_Motor.value(direction)
    Left_Motor_PWM.duty_u16(power)

def Right_Motor_Control(power,direction):
    # Normalize direcition variable
    direction = 1 if direction else 0 
    # Set a max value for power
    power = max(0, min(int(power), 65535)) 
    # Since right motor has high as backwards, we set reverse direction
    direction = 1 - direction
    # Apply values to motor
    Right_Motor.value(direction)
    Right_Motor_PWM.duty_u16(power)

def Motor_Off ():
    print("Off") # Print to REPL
    Left_Motor.low()
    Left_Motor_PWM.duty_u16(0)
    Right_Motor.low() 
    Right_Motor_PWM.duty_u16(0)