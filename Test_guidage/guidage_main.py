#! /usr/bin/python
 
import os
from gps import *
import time
import threading
import json
import math
from sense_hat import SenseHat
 
gpsd = None #setting the global variable

PIN = 0000 #Enter your SIM card's PIN code here

###############
## HELPER CLASS
###############
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

###############
## HELPER FUNCTION
###############
# Returns the bearing (direction) between two points given in the form of tuples or lists of latitude, longitude
def get_direction(pointA, pointB):
  # Check type of input arguments
  if ((type(pointA) != tuple) and (type(pointA) != list)) or ((type(pointB) != tuple) and (type(pointB) != list)):
    raise TypeError("Only tuples and lists are supported as arguments")

  lat1 = math.radians(pointA[0])
  lat2 = math.radians(pointB[0])
  diffLong = math.radians(pointB[1] - pointA[1])

  x = math.sin(diffLong) * math.cos(lat2)
  y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))
  # Get bearing between -180 and + 180
  initial_bearing = math.atan2(x, y)
  # Normalize to get value between 0 and 360
  initial_bearing = math.degrees(initial_bearing)
  compass_bearing = (initial_bearing + 360) % 360

  return compass_bearing

###############
## MAIN
###############
if __name__ == '__main__':

  ###############
  ## SENSEHAT INITIALIZATION
  ###############
  sense = SenseHat()

  sense.set_rotation(0)
  sense.clear()

  B = (0, 0, 255)
  R = (255, 0, 0)
  G = (255, 255, 255)
  W = G

  arrow_thin = [
    B, B, B, G, G, B, B, B,
    B, B, B, W, W, B, B, B,
    B, B, W, W, W, W, B, B,
    B, W, B, W, W, B, W, B,
    G, B, B, W, W, B, B, G,
    B, B, B, W, W, B, B, B,
    B, B, B, W, W, B, B, B,
    B, B, B, W, W, B, B, B
  ]

  arrow_thin_quasi = [
    W, W, W, W, W, W, W, W,
    B, B, B, B, B, G, W, W,
    B, B, B, B, G, W, G, W,
    B, B, B, G, W, G, B, W,
    B, B, G, W, G, B, B, W,
    B, G, W, G, B, B, B, W,
    G, W, G, B, B, B, B, W,
    W, G, B, B, B, B, B, W
  ]

  sos = [
    R, R, R, R, R, R, R, R,
    R, R, R, W, W, R, R, R,
    R, R, R, W, W, R, R, R,
    R, R, R, W, W, R, R, R,
    R, R, R, W, W, R, R, R,
    R, R, R, R, R, R, R, R,
    R, R, R, W, W, R, R, R,
    R, R, R, W, W, R, R, R
  ]

  ###############
  ## LOAD DATA
  ###############
  with open("/home/pi/Documents/Test_BLE/idrando.txt", "r") as idfile:
    ID = int(idfile.read())

  with open("/home/pi/Documents/Test_guidage/treks.geojson") as treksfile:
    # Load all treks from file
    data = json.load(treksfile)

  ###############
  ## GUIDE USER THROUGH CHOSEN TREK
  ###############

  # Get data from chosen trek by ID
  trek = None
  for d in data['features']:
    if d['id'] == ID:
      trek = d
      break

  index_point = 0  # initialize index of current next point
  error_radius = 0.0000089928 * 30 # 30 meters gps precision (NB: 1m = 0.0000089928)
  num_points = len(trek['geometry']['coordinates'])  # number of points in the trek

  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start()  # start thread
    ###############
    ## GUIDING LOOP
    ###############
    # Loop until the user reaches the last point of the trek
    while index_point < num_points:
      GPS = [gpsd.fix.longitude, gpsd.fix.latitude]
      print(GPS)
      next_point = trek['geometry']['coordinates'][index_point]
      print("Index of next point: {}".format(index_point))
      # Check if the gps position is within the error radius of the next point
      # meaning the user has reached the next point and we can increment it
      if ((GPS[0] - next_point[0]) ** 2 + (GPS[1] - next_point[1]) ** 2) <= (error_radius ** 2):
        print("Reached a new point")
        index_point = index_point + 1
      # Compute direction from the user's gps position to the next point
      current_direction = get_direction(GPS, next_point)
      print(current_direction)
      # Get compass value for orientation
      compass = sense.get_compass()
      direction_raw = current_direction
      direction = (450 - direction_raw) % 360
      dir = (compass - direction) % 360
      print("compass: %s" % compass)

      # Display arrow indicating direction to next point
      if dir < 22.5:
        sense.set_pixels(arrow_thin)
        sense.set_rotation(90)
      elif dir < 67.5:
        sense.set_pixels(arrow_thin_quasi)
        sense.set_rotation(0)
      elif dir < 112.5:
        sense.set_pixels(arrow_thin)
        sense.set_rotation(0)
      elif dir < 157.5:
        sense.set_pixels(arrow_thin_quasi)
        sense.set_rotation(270)
      elif dir < 202.5:
        sense.set_pixels(arrow_thin)
        sense.set_rotation(270)
      elif dir < 247.5:
        sense.set_pixels(arrow_thin_quasi)
        sense.set_rotation(180)
      elif dir < 292.5:
        sense.set_pixels(arrow_thin)
        sense.set_rotation(180)
      elif dir < 337.5:
        sense.set_pixels(arrow_thin_quasi)
        sense.set_rotation(90)
      else:
        sense.set_pixels(arrow_thin)
        sense.set_rotation(90)

      # Fall detection
      acceleration = sense.get_accelerometer_raw()
      z = acceleration['z']
      z = abs(z)
      # if a fall is detected
      if z > 2:
        sense.set_pixels(sos)
        sense.set_rotation(0)
        btn = False
        decompte = 60  # 30 seconds

        # Wait for confirmation or not to send message
        while btn == False and decompte > 0:
          # check if left button was pressed
          for event in sense.stick.get_events():
            if event.direction == "left" and event.action == "pressed":
              btn = True
          time.sleep(0.5)
          decompte = decompte - 1

        # If button was pressed, do not send message
        if btn == True:
          sense.clear()
        # If button was not pressed at the end of the 30 seconds, send message
        else:
          # Get emergency contacts
          with open("/home/pi/Documents/Test_BLE/numeros.txt", "r") as f:
            # Send text to every contact
            for num in f.readlines():
              os.system("gammu entersecuritycode PIN {}".format(PIN))
              os.system("echo \"SOS : Votre proche vous a défini comme contact d'urgence. Une chute a été détectée.\nVoici sa position : {}, {}.\n\n-- WALKER (1/2)\" | gammu --sendsms TEXT {}".format(GPS[1], GPS[0], num))
              os.system("echo \"Cliquez ici pour voir dans Google Maps: http://maps.google.com/maps?q=loc:{},{}\n\n-- WALKER (2/2)\" | gammu --sendsms TEXT {}".format(GPS[1], GPS[0], num))
          sense.clear()

      # Stop guiding via button
      for event in sense.stick.get_events():
        # Check if the joystick was held
        if event.action == "held":
          # Check which direction
          if event.direction == "right":
            index_point = num_points + 1

    # Send text when the user has reached their destination
    if index_point == num_points:
      # Get emergency contacts
      with open("/home/pi/Documents/Test_BLE/numeros.txt", "r") as f2:
        for num in f2.readlines():
          os.system("gammu entersecuritycode PIN {}".format(PIN))
          os.system("echo \"Votre proche est bien arrivé à destination pour sa randonnée !\n-- WALKER\" | gammu --sendsms TEXT {}".format(num))

    sense.clear()

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print("\nKilling Thread...")
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
    print("Done.\nExiting.")
    sense.clear()

