import os
from sense_hat import SenseHat

sense = SenseHat()

sense.clear()

wait = True

while wait == True:
	for event in sense.stick.get_events():
    		# Check if the joystick was pressed
		if event.action == "held":
			#Check which direction
			if event.direction == "middle":
				print("Downloading data...")
				# Put the link to your Geotrek api here
				os.system("curl http://walkerpfe-rando.ovh/data/api/fr/treks.geojson -o /home/pi/Documents/Test_guidage/treks.geojson")
				print("Done")
				wait = False
