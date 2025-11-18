import machine
import math, time
from machine import Pin
from machine import PWM

time.sleep(1) # Wait for USB to become ready
# CHANGE VARIABLES TO WHAT YOUR PINOUT IS
# Pinout variables
LMotor = 12
LMotorPWM = 13
RMotor = 14
RMotorPWM = 15

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

pwm = min(max(int(2**16 * abs(1)), 0), 65535) * 0.5
""""
# Creating Interupt function
def RF_Signal(pin, _):
    global start
    start = time.ticks_ms()
    if pin is RF_A:
        print("Motor 1") # Print to REPL
        Left_Motor.high() 
        Left_Motor_PWM.duty_u16(pwm) 
    elif pin is RF_B:
        print("Motor 2") # Print to REPL
        Left_Motor.low() 
        Left_Motor_PWM.duty_u16(pwm)          
    elif pin is RF_C:
        print("Motor 3") # Print to REPL
        Right_Motor.low() 
        Right_Motor_PWM.duty_u16(pwm) 
    elif pin is RF_D:
        print("Motor 4") # Print to REPL
        Right_Motor.high() 
        Right_Motor_PWM.duty_u16(pwm)     
 """   

# Initializing RF
RF_A = Pin(7, Pin.IN, Pin.PULL_DOWN)
RF_B = Pin(6, Pin.IN, Pin.PULL_DOWN)
RF_C = Pin(5, Pin.IN, Pin.PULL_DOWN)
RF_D = Pin(4, Pin.IN, Pin.PULL_DOWN)

""""
# Interupts calls
RF_A.irq(trigger=Pin.IRQ_RISING, handler = RF_Signal)
RF_B.irq(trigger=Pin.IRQ_RISING, handler = RF_Signal)
RF_C.irq(trigger=Pin.IRQ_RISING, handler = RF_Signal)
RF_D.irq(trigger=Pin.IRQ_RISING, handler = RF_Signal)
"""
# Main 

while True:
    if RF_A.value() == 1:
        start = time.ticks_ms()
        print("Motor 1") # Print to REPL
        Left_Motor.high() 
        Left_Motor_PWM.duty_u16(int(pwm)) 
    if RF_B.value() == 1:
        start = time.ticks_ms()
        print("Motor 2") # Print to REPL
        Left_Motor.low() 
        Left_Motor_PWM.duty_u16(int(pwm))          
    if RF_C.value() == 1:
        start = time.ticks_ms()
        print("Motor 3") # Print to REPL
        Right_Motor.low() 
        Right_Motor_PWM.duty_u16(int(pwm)) 
    if RF_D.value() == 1:
        start = time.ticks_ms()
        print("Motor 4") # Print to REPL
        Right_Motor.high() 
        Right_Motor_PWM.duty_u16(int(pwm))     
    """"
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
    """
    # sleep as to not slam cpu
    time.sleep_ms(50)
