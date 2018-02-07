import serial
import thread
import threading
import os
import subprocess
import os.path
import time
import sys
from sense_hat import SenseHat

sense = SenseHat()
B = (107, 107, 107)
W = (0, 0, 64)

bluetooth_logo = [
    W, W, W, B, W, W, W, W,
    W, B, W, B, B, B, W, W,
    W, W, B, B, W, W, B, W,
    W, W, W, B, B, B, W, W,
    W, W, W, B, B, B, W, W,
    W, W, B, B, W, W, B, W,
    W, B, W, B, B, B, W, W,
    W, W, W, B, W, W, W, W
]

def launchTrek():
	subprocess.call("/home/pi/Documents/Test_guidage/simulation.sh")
	#print("HELLO WORLD")

#Check if port is open
fileNotFound = 1
while fileNotFound: 
	if(os.path.exists("/dev/rfcomm0")):
		print("Existe")
		fileNotFound = 0
		time.sleep(1)
		sense.set_pixels(bluetooth_logo)

	else:
		print("Pas de fichier")
		sense.show_message("Wait",0.05)

#Print connected 
ser = serial.Serial(port='/dev/rfcomm0')
while 1:
	msg= ser.readline().split(";")
	print(msg)
	#ID trek 
	if (msg[0]  == '1'):
		rando = msg[1].split(",")
		#check file exists 
		if(os.path.exists("/home/pi/Documents/Test_BLE/idrando.txt")):
			os.remove("/home/pi/Documents/Test_BLE/idrando.txt")
		#write into file
		with open("/home/pi/Documents/Test_BLE/idrando.txt","w+") as randofile:
			for j in rando:
				randofile.write("%s" %j)
			randofile.close()
		thread.start_new_thread(launchTrek, ())

	#Phone number
	if (msg[0] == '2'):
		numeros = msg[1].replace("\n", "").split(",")
		#Check file exists
		if(os.path.exists("/home/pi/Documents/Test_BLE/numeros.txt")):
			os.remove("/home/pi/Documents/Test_BLE/numeros.txt")
		#Write into file
		with  open("/home/pi/Documents/Test_BLE/numeros.txt","w+") as filenumber:
			for i in numeros:
				filenumber.write("%s\n" % i)
			filenumber.close()

	#End connexion
	if (msg[0] == '3'):
		print("Dans 3")
		os.system("pgrep -f 'rfcomm listen' > rfcommpid.txt")
		with open ('rfcommpid.txt', 'r') as file:
			temp = file.read().splitlines()
		os.system("sudo kill " + str(temp[0]) + " " + str(temp[1]))
		print("Done")
		sense.clear()
		sys.exit()
