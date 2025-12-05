# activity.py, for the no signal function.
import time

# Shared "last input" timestamp
last_activity = time.ticks_ms()

# When a signal is recieved
def touch():
    """Call this whenever any control (IR or RF) is used."""
    global last_activity
    last_activity = time.ticks_ms()
# Checking time between last time signal recieved and now.
def ms_since_last_activity():
    """How many ms since the last IR or RF input."""
    now = time.ticks_ms()
    return time.ticks_diff(now, last_activity)