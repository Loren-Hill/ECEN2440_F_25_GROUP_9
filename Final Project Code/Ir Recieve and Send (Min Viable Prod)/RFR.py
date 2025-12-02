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

pwm = min(max(int(2**16 * abs(1)), 0), 65535) 

# Initializing RF
RF_A = Pin(7, Pin.IN, Pin.PULL_DOWN)
RF_B = Pin(6, Pin.IN, Pin.PULL_DOWN)
RF_C = Pin(5, Pin.IN, Pin.PULL_DOWN)
RF_D = Pin(4, Pin.IN, Pin.PULL_DOWN)


# Main 
def main():
    global start
    while True:
        now = time.ticks_ms()
        A = RF_A.value()
        B = RF_B.value()
        C = RF_C.value()
        D = RF_D.value()
        if A or B or C or D:
            start = now
            if A: # Left Motor Forward
                print("Motor Forward Left") # Print to REPL
                Left_Motor.low() 
                Left_Motor_PWM.duty_u16(pwm) 
            if B: # Right Motor Forward
                print("Motor Forward Right") # Print to REPL
                Right_Motor.high() 
                Right_Motor_PWM.duty_u16(pwm)         
            if C: # Left Motor Backwards
                print("Motor Backwards Left") # Print to REPL
                Left_Motor.high() 
                Left_Motor_PWM.duty_u16(pwm)  
            if D: # Right Motor Backwards
                print("Motor Backwards Right") # Print to REPL
                Right_Motor.low() 
                Right_Motor_PWM.duty_u16(pwm) 
        else:    
        # Will count how long in between each signal, if that is over 300 ms, stop all motors.
            if (time.ticks_diff(now,start) >= 200):
                print("Motor off") # Print to REPL
                Left_Motor.low() 
                Left_Motor_PWM.duty_u16(0) 
                Right_Motor.low() 
                Right_Motor_PWM.duty_u16(0)
                # Reset timer
                # start = now
            
        # sleep as to not slam cpu
        time.sleep_ms(50)
if __name__ == "__main__":
    main()