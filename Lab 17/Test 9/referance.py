from machine import I2C, Pin
import seesaw
import time


# Initialize I2C. Adjust pin numbers based on your Pico's configuration
i2c = I2C(0, scl=Pin(17), sda=Pin(16))


# Initialize the Seesaw driver with the I2C interface
# Use the Gamepad QT's I2C address from the Arduino code (0x50)
seesaw_device = seesaw.Seesaw(i2c, addr=0x50)


# Define button and joystick pin numbers as per the Arduino code
BUTTON_A = 5
BUTTON_B = 1
BUTTON_X = 6
BUTTON_Y = 2
BUTTON_START = 16
BUTTON_SELECT = 0
JOYSTICK_X_PIN = 14
JOYSTICK_Y_PIN = 15


# Button mask based on Arduino code
BUTTONS_MASK = (1 << BUTTON_X) | (1 << BUTTON_Y) | \
               (1 << BUTTON_A) | (1 << BUTTON_B) | \
               (1 << BUTTON_SELECT) | (1 << BUTTON_START)


# Define LED pins
LED_1_PIN = 12
LED_2_PIN = 13
LED_3_PIN = 15
LED_4_PIN = 14


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


# Initialize last button states
last_buttons = 0


# Initialize joystick center position
joystick_center_x = 511
joystick_center_y = 497


# Control mode: 'button' or 'joystick'
control_mode = 'button'


def setup_buttons():
    """Configure the pin modes for buttons."""
    seesaw_device.pin_mode_bulk(BUTTONS_MASK, seesaw_device.INPUT_PULLUP)


def read_buttons():
    """Read and return the state of each button."""
    return seesaw_device.digital_read_bulk(BUTTONS_MASK)


def handle_button_press(button):
    """Toggle the corresponding LED state on button press"""
    global control_mode
    control_mode = 'button'  # Switch to button control mode
   
    # Toggle the LED state
    led_states[button] = not led_states[button]
   
    # Update the physical LED if it has one
    if button in led_pins:
        led_pins[button].value(led_states[button])
        print("Button", button, "LED is now", "ON" if led_states[button] else "OFF")


def main():
    """Main program loop."""
    global last_buttons, control_mode
    setup_buttons()
   
    last_x, last_y = seesaw_device.analog_read(JOYSTICK_X_PIN), seesaw_device.analog_read(JOYSTICK_Y_PIN)
    joystick_threshold = 50  # Adjust threshold as needed
   
    print("Starting main loop. Press buttons to test...")
   
    while True:
        current_buttons = read_buttons()
       
        # Check each button for state changes
        for button in led_states:
            current_state = current_buttons & (1 << button)
            last_state = last_buttons & (1 << button)
           
            # Detect button release (transition from 0 to 1 with pullup)
            if not last_state and current_state:
                print(f"Button {button} released")
                handle_button_press(button)
       
        # Read joystick values
        current_x = seesaw_device.analog_read(JOYSTICK_X_PIN)
        current_y = seesaw_device.analog_read(JOYSTICK_Y_PIN)
       
        # Check if joystick position has changed significantly
        if abs(current_x - last_x) > joystick_threshold or abs(current_y - last_y) > joystick_threshold:
            control_mode = 'joystick'  # Switch to joystick control mode
            print("Joystick moved - X:", current_x, ", Y:", current_y)
            last_x, last_y = current_x, current_y
           
            # Turn off all LEDs
            for pin in led_pins.values():
                pin.value(False)
           
            # Determine which LED to turn on based on joystick direction
            if current_y < joystick_center_y - joystick_threshold:  # Joystick moved up
                led_pins[BUTTON_A].value(True)
            elif current_y > joystick_center_y + joystick_threshold:  # Joystick moved down
                led_pins[BUTTON_B].value(True)
            elif current_x < joystick_center_x - joystick_threshold:  # Joystick moved left
                led_pins[BUTTON_X].value(True)
            elif current_x > joystick_center_x + joystick_threshold:  # Joystick moved right
                led_pins[BUTTON_Y].value(True)
       
        last_buttons = current_buttons
        time.sleep(0.1)  # Delay to prevent overwhelming the output


if __name__ == "__main__":
    main()
