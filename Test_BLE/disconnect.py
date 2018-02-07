import os
from sense_hat import SenseHat

sense = SenseHat()

sense.show_message("Hi")
sense.clear()
os.system("pgrep -f 'rfcomm listen' > rfcommpid.txt")
with open ('rfcommpid.txt', 'r') as file:
	temp = file.read().splitlines()
for it in temp:
	print(it)
	os.system("sudo kill " + it)

