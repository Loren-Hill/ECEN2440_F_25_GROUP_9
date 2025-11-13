import ir_tx
import machine
import seesaw
import time
from machine import I2C, Pin
from ir_tx.nec import NEC
from machine import Pin

# This is code for IR transmitter circuit
# Change name of file to Main if uploading to PICO

# Pin Variables
PinIr = 15 # Pin for IR transmitter
PinScl = 17 # Pin for SCL on joystick
PinSda = 16 # Pin for SDA on joystick
PinJoyX = 13 # Pin for X value of joytstick
PinJoyY = 12 # Pin for Y value of joystick

# Setting device address for now, not sure if needed yet
device_addr = 0x01

# Initialize IR transmitter pin 
tx_pin = Pin(PinIr,Pin.OUT,value=0)
transmitter = NEC(tx_pin)
""""
transmitter.transmit(device_addr,command) # Important for transmitting IR,
can use device_addr and command to send x and y of joystick
"""
# Initialize I2C. Adjust pin numbers based on your Pico's configuration
i2c = I2C(0, scl=Pin(PinScl), sda=Pin(PinSda)) # SCL is yellow, SDA is Blue


# Initialize the Seesaw driver with the I2C interface
# Use the Gamepad QT's I2C address from the Pico code (0x50)
seesaw_device = seesaw.Seesaw(i2c, addr=0x50)

# Define button and joystick pin numbers as per the Pico code
JOYSTICK_X_PIN = PinJoyX
JOYSTICK_Y_PIN = PinJoyY

# Initialize joystick center position
joystick_center_x = 511 # Arbitrarily chosen, change if needed 
joystick_center_y = 497 # Arbitrarily chosen, change if needed 

# Initialize last button states
last_buttons = 0

# Control mode: 'button' or 'joystick'
control_mode = 'button'



def main():
    """Main program loop."""
    global last_buttons, control_mode
   
    last_x, last_y = seesaw_device.analog_read(JOYSTICK_X_PIN), seesaw_device.analog_read(JOYSTICK_Y_PIN)
    joystick_threshold = 50  # Adjust threshold as needed
    
    while True:
       
        # Read joystick values
        current_x = seesaw_device.analog_read(JOYSTICK_X_PIN)
        current_y = seesaw_device.analog_read(JOYSTICK_Y_PIN)
       
        # Check if joystick position has changed significantly
        if abs(current_x - last_x) > joystick_threshold or abs(current_y - last_y) > joystick_threshold:
            control_mode = 'joystick'  # Switch to joystick control mode
            print("Joystick moved - X:", current_x, ", Y:", current_y)
            last_x, last_y = current_x, current_y
            
            # Determine which Direction to go based on joystick direction
            # Simple Implementation,
            """"
                4 commands for each state possible state of motors
	            0x00 = motor 1 and motor 2 forward
	            0x01 = motor 1 and motor 2 backwards
	            0x02 = motor 1 forwards and motor 2 backwards
	            0x03 = motor 1 backwards and motor 2 forward
            """
            if current_y < joystick_center_y - joystick_threshold:  # Joystick moved up
                # Send a hex value through IR that will mean 100% motor up
                    # X will be joystick center x
                    # Y will be max value, or 1023
                    motor_state = 0x00
                    print('Motor Up')
                    
            elif current_y > joystick_center_y + joystick_threshold:  # Joystick moved down
                # Send a hex value through IR that will mean 100% motor down
                    # X will be joystick center x
                    # Y will be min value, or 0
                    motor_state = 0x01
                    print('Motor Down')
                    

            elif current_x < joystick_center_x - joystick_threshold:  # Joystick moved left
                # Send a hex value through IR that will mean 100% motor left
                    # X will be min value 0
                    # Y will be joystick center y
                    motor_state = 0x02
                    print('Motor Left')

            elif current_x > joystick_center_x + joystick_threshold:  # Joystick moved right
                # Send a hex value through IR that will mean 100% motor right 
                    # X will be max value 1023
                    # Y will be joystick center y
                    motor_state = 0x03
                    print('Motor Right')
                    
            transmitter.transmit(device_addr,motor_state) # Transmit address and motor state

        
            
        
        time.sleep(0.1)  # Delay to prevent overwhelming the output


if __name__ == "__main__":
    main()
