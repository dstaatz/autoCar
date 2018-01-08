import RPi.GPIO as io
import time


# Define pinouts
DRIVE1 = 17
DRIVE2 = 18
STEER1 = 23
STEER2 = 24

# Use pin names not pin numbers
io.setmode(io.BCM)

# Setup pin types
io.setup(DRIVE1, io.OUT)
io.setup(DRIVE2, io.OUT)
io.setup(STEER1, io.OUT)
io.setup(STEER2, io.OUT)

## Test all directions
# Test forward-left
io.output(DRIVE1, True)
io.output(DRIVE2, False)
io.output(STEER1, False)
io.output(STEER2, True)
time.sleep(1)

# Test forward
io.output(DRIVE1, True)
io.output(DRIVE2, False)
io.output(STEER1, False)
io.output(STEER2, False)
time.sleep(1)

# Test forward-right
io.output(DRIVE1, True)
io.output(DRIVE2, False)
io.output(STEER1, True)
io.output(STEER2, False)
time.sleep(1)

# Test back-left
io.output(DRIVE1, False)
io.output(DRIVE2, True)
io.output(STEER1, False)
io.output(STEER2, True)
time.sleep(1)

# Test back
io.output(DRIVE1, False)
io.output(DRIVE2, True)
io.output(STEER1, False)
io.output(STEER2, False)
time.sleep(1)

# Test back-right
io.output(DRIVE1, False)
io.output(DRIVE2, True)
io.output(STEER1, True)
io.output(STEER2, False)
time.sleep(1)
