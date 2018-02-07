import subprocess
import os
from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

sense.clear()

os.system("python /home/pi/Documents/Test_guidage/download_treks.py")

while True:
	for event in sense.stick.get_events():
    		# Check if the joystick was pressed
		if event.action == "pressed":
			#Check which direction
			if event.direction == "up":
				subprocess.call("/home/pi/Documents/Test_BLE/walker.sh")

