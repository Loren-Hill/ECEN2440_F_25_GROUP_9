# Rename to main.py if transmitting
import ir_tx
import machine
import seesaw
import time
from machine import I2C, Pin
from ir_tx.nec import NEC

# CHANGE VARIABLES TO WHAT YOUR PINOUT IS
# Pin Variables
PinIr = 15 # Pin for IR transmitter
PinScl = 17 # Pin for SCL on joystick
PinSda = 16 # Pin for SDA on joystick
# Seesaw ADC channel 14 and 15 NOT pins on pico. "Virtual" pins, generally dont change
PinJoyX = 14 # Pin for X value of joytstick
PinJoyY = 15 # Pin for Y value of joystick



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
i2c = I2C(0, scl=Pin(PinScl), sda=Pin(PinSda))


# Initialize the Seesaw driver with the I2C interface
# Use the Gamepad QT's I2C address from the Arduino code (0x50)
seesaw_device = seesaw.Seesaw(i2c, addr=0x50)

""""
# Define button and joystick pin numbers as per the Arduino code
BUTTON_A = 5
BUTTON_B = 1
BUTTON_X = 6
BUTTON_Y = 2
BUTTON_START = 16
BUTTON_SELECT = 0
"""
JOYSTICK_X_PIN = PinJoyX
JOYSTICK_Y_PIN = PinJoyY
""""

# Button mask based on Arduino code
BUTTONS_MASK = (1 << BUTTON_X) | (1 << BUTTON_Y) | \
               (1 << BUTTON_A) | (1 << BUTTON_B) | \
               (1 << BUTTON_SELECT) | (1 << BUTTON_START)


# Define LED pins
LED_1_PIN = 7
LED_2_PIN = 8
LED_3_PIN = 9
LED_4_PIN = 10


# Initialize LED pin objects
led_pins = {
    BUTTON_A: Pin(LED_1_PIN, Pin.OUT),
    BUTTON_B: Pin(LED_2_PIN, Pin.OUT),
    BUTTON_X: Pin(LED_3_PIN, Pin.OUT),
    BUTTON_Y: Pin(LED_4_PIN, Pin.OUT)
}


# Initialize LED states
led_states = {
    BUTTON_A: False,
    BUTTON_B: False,
    BUTTON_X: False,
    BUTTON_Y: False,
    BUTTON_START: False,
    BUTTON_SELECT: False
}
"""

# Initialize last button states
last_buttons = 0


# Initialize joystick center position
joystick_center_x = 511
joystick_center_y = 497


# Control mode: 'button' or 'joystick'
control_mode = 'button'

""""
def setup_buttons():
    #Configure the pin modes for buttons.
    seesaw_device.pin_mode_bulk(BUTTONS_MASK, seesaw_device.INPUT_PULLUP)


def read_buttons():
    #Read and return the state of each button.
    return seesaw_device.digital_read_bulk(BUTTONS_MASK)


def handle_button_press(button):
    #Toggle the corresponding LED state on button press"
    global control_mode
    control_mode = 'button'  # Switch to button control mode
   
    # Toggle the LED state
    led_states[button] = not led_states[button]
   
    # Update the physical LED if it has one
    if button in led_pins:
        led_pins[button].value(led_states[button])
        print("Button", button, "LED is now", "ON" if led_states[button] else "OFF")
"""

def main():
    """Main program loop."""

    global last_buttons, control_mode
    #setup_buttons()
   
    last_x, last_y = seesaw_device.analog_read(JOYSTICK_X_PIN), seesaw_device.analog_read(JOYSTICK_Y_PIN)
    joystick_threshold = 50  # Adjust threshold as needed
   
    print("Starting main loop. Press buttons to test...")
    # init motor_state
    motor_state = 0xff
   
    while True:
        #current_buttons = read_buttons()
       
        # Check each button for state changes
       # for button in led_states:
        #    current_state = current_buttons & (1 << button)
         #   last_state = last_buttons & (1 << button)
           
            # Detect button release (transition from 0 to 1 with pullup)
           # if not last_state and current_state:
             #   print(f"Button {button} released")
              #  handle_button_press(button)
       
        # Read joystick values
        current_x = seesaw_device.analog_read(JOYSTICK_X_PIN)
        current_y = seesaw_device.analog_read(JOYSTICK_Y_PIN)
       
        # Check if joystick position has changed significantly
        #if abs(current_x - last_x) > joystick_threshold or abs(current_y - last_y) > joystick_threshold:
        control_mode = 'joystick'  # Switch to joystick control mode
        print("Joystick moved - X:", current_x, ", Y:", current_y)
        last_x, last_y = current_x, current_y
        
        # Turn off all LEDs
        #for pin in led_pins.values():
            #  pin.value(False)
        
            # Simple Implementation,
        """
            4 commands for each state possible state of motors
            0x00 = motor 1 and motor 2 forward
            0x01 = motor 1 and motor 2 backwards
            0x02 = motor 1 forwards and motor 2 backwards
            0x03 = motor 1 backwards and motor 2 forward
        """
        """
        # Will use current x and current y, from 0 - 1023, starting in bottom left, going top right
        # Creating boolean true of false for if the stick is within the "deadzone" 
        x_centered = joystick_center_x - joystick_threshold <= current_x <= joystick_center_x + joystick_threshold
        y_centered = joystick_center_y - joystick_threshold <= current_y <= joystick_center_y + joystick_threshold


        
        # If stick is in center, send a command to stop all motors
        if x_centered and y_centered:
            # centered
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
                

        elif current_x < joystick_center_x - joystick_threshold:  # Joystick moved right
            # Send a hex value through IR that will mean 100% motor right
                # X will be min value 0
                # Y will be joystick center y
                motor_state = 0x02
                print('Motor Right')

        elif current_x > joystick_center_x + joystick_threshold:  # Joystick moved left
            # Send a hex value through IR that will mean 100% motor left 
                # X will be max value 1023
                # Y will be joystick center y
                motor_state = 0x03
                print('Motor Left')
        elif       (current_x < joystick_center_x + joystick_threshold # Handles Joystick being in center x-axis
                and current_x > joystick_center_x - joystick_threshold
                and current_y < joystick_center_y + joystick_threshold # Handles Joystick being in center y-axis
                and current_y > joystick_center_y - joystick_threshold
            ):
            # Send a hex value through IR that will mean motor off
                # X will be value ~510
                # Y will be value ~510
                motor_state = 0x04 
                print('motor Off')
              
            
                
        transmitter.transmit(device_addr,motor_state) # Transmit address and motor state
            
        #last_buttons = current_buttons
        time.sleep(0.1)  # Delay to prevent overwhelming the output


if __name__ == "__main__":
    main()
