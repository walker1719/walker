import threading
import subprocess
import time
import thread
import os
import numpy as np
from sense_hat import SenseHat 


def disconnect():
    print("Disconnect")
    os.system("pgrep -f 'rfcomm listen' > rfcommpid.txt")
    with open ('rfcommpid.txt', 'r') as file:
        temp = file.read().splitlines()
        for it in temp:
            print(it)
            os.system("sudo kill " + it)

def connexion():
    subprocess.call("/home/pi/Documents/Test_BLE/walker.sh")

class myThread(threading.Thread): 
    def __init__(self, nom = ''): 
        threading.Thread.__init__(self) 
        self.nom = nom 
        self._stopevent = threading.Event( ) 
    def run(self): 
       	sense = SenseHat()
        while not self._stopevent.isSet(): 
            for event in sense.stick.get_events():
		if event.action == "pressed":
		    #Sensing environnement
                    if event.direction == "up":
			thread.start_new_thread(connexion, ())
		    if event.direction == "middle":
			sense.clear()
			humidity = sense.get_humidity()
			temp = sense.get_temperature()
			pressure = sense.get_pressure()
			text = "T:{}C H: {}% P: {}mb".format(np.round(temp,1),np.round(humidity,0),np.round(pressure,0))
			sense.show_message(text)
         	    if event.direction == "down":
      			#thread.start_new_thread(disconnect,())
			#sense.clear()
                        sense.clear((0, 64, 0))
                        print("Downloading data...")
                        os.system("curl http://walkerpfe-rando.ovh/data/api/fr/treks.geojson -o /home/pi/Documents/Test_guidage/treks.geojson")
                        print("Done")
                        sense.clear()
                if event.action == "held":
                    if event.direction == "down":
                        thread.start_new_thread(disconnect,())
                        sense.clear()

    def stop(self): 
        print "le thread "+self.nom +" s'est termine proprement"
        self._stopevent.set( ) 

thread_main = myThread('Thread principal')
thread_main.start()


