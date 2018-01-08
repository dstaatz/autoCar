import RPi.GPIO as io
import time

DELAY = 2

io.setmode(io.BCM)

io.setup(18, io.OUT)
io.setup(17, io.OUT)

while True:
	io.output(17, False)
	io.output(18, False)
	time.sleep(1)
	io.output(17, True)
	io.output(18, False)
	time.sleep(DELAY)
	io.output(17, True)
	io.output(18, True)
	time.sleep(1)
	io.output(17, False)
	io.output(18, True)
	time.sleep(DELAY)
