import machine
import math, time
from machine import Pin
from machine import PWM


# Initializing LEDS
LED1 = Pin(xxx,Pin.OUT, value = 0)
LED2 = Pin(xxx,Pin.OUT, value = 0)
LED3 = Pin(xxx,Pin.OUT, value = 0)
LED4 = Pin(xxx,Pin.OUT, value = 0)

# Creating Interupt function
def callback(pin):
    LED1.value(0)
    LED2.value(0)
    LED3.value(0)
    LED4.value(0)
    if pin is RF_A:
        LED1.value(1)
    elif pin is RF_B:
        LED2.value(1)   
    elif pin is RF_C:
        LED3.value(1)   
    elif pin is RF_D:
        LED4.value(1)


# Initializing RF
RF_A = Pin(xxx, Pin.IN, Pin.PULL_DOWN)
RF_B = Pin(xxx, Pin.IN, Pin.PULL_DOWN)
RF_C = Pin(xxx, Pin.IN, Pin.PULL_DOWN)
RF_D = Pin(xxx, Pin.IN, Pin.PULL_DOWN)

# Interupts calls
RF_A.irq(trigger=Pin.IRQ_RISING, handler = RF_Signal)
RF_B.irq(trigger=Pin.IRQ_RISING, handler = RF_Signal)
RF_C.irq(trigger=Pin.IRQ_RISING, handler = RF_Signal)
RF_D.irq(trigger=Pin.IRQ_RISING, handler = RF_Signal)

# Main 

while True:
    continue