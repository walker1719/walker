#!/bin/bash

sudo rfcomm listen hci0 & 
/usr/bin/python /home/pi/Documents/Test_BLE/readTest2.py 

