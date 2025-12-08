# Main 
import IRReciever
import RFReciever
import activity
import MotorControl
import machine
import math, time
from machine import Pin
from machine import PWM

# Setting what time out will be for recieving no signal, in ms
Max_No_Signal = 150

# Define button pins
Control_Button_Pin = 16
Control_Button = Pin(Control_Button_Pin, Pin.IN,Pin.PULL_UP)
# Setting Control_Law
RF_Control = 0
IR_Control = 1

Control_Law = IR_Control
# last_press for debounce declaration
last_press = time.ticks_ms()

# Interupt for changing control from RF to IR
def Control_Type_irq(pin):
    global Control_Law, last_press

    now = time.ticks_ms()
    # Debounce setup of 200 ms
    if time.ticks_diff(now, last_press) < 200:
        return
    
    last_press = now

    # Toggle between 
    if Control_Law == IR_Control:
        Control_Law = RF_Control
        print("Switched to RF")
    else:
        Control_Law = IR_Control
        print("Switched to IR")   

     # Tell the other modules (optional but nice)
    IRReciever.set_mode(Control_Law)
    #RFReciever.set_mode(Control_Law) 
    

    # Set Control_Law = to what it is not, aka if 1 set to 0 if 0 set to 1    



def main():
    global Control_Law

    # Telling files which mode we are in for control
    # Initialize modules with current mode
    IRReciever.set_mode(Control_Law)
    #RFReciever.set_mode(Control_Law)

    # Attach interrupt to the button 
    Control_Button.irq(trigger=Pin.IRQ_FALLING, handler=Control_Type_irq)
    # Setting loop
    while True:
        if Control_Law == IR_Control:
            # change for button as needed, run IR
            print("Run off of IR")
            
        else:
            # change for button as needed, runs RF
            #print("Run off of RF")
            RFReciever.RF_Reciever()
        # Govern to not blase CPU
        if activity.ms_since_last_activity() >= Max_No_Signal:
            # Call stop motor function
            MotorControl.Motor_Off()
        time.sleep_ms(10)
        
        

if __name__ == "__main__":
    main()