#!/usr/bin/python3
#capture changes in the background picture to be used for training Yolo

import os,sys
import time
import shutil
import cv2
import serial
import logging
from datetime import datetime
      
#main -------
Headless=True
if len(sys.argv)>1:
   if sys.argv[1]=='-show':
      Headless=False

if os.name == 'nt':
   folder = 'C:\\users\\peter/jevois_capture'
   logfile = 'c:\\users\\peter/jevois.log'
   port = 'COM6'
   camno = 1
else: #linux
   folder = '/home/pi/jevois_capture'
   logfile = '/home/pi/jevois.log'
   port = '/dev/ttyACM0'
   camno = 0
Headless=False
logging.basicConfig(filename=logfile,level=logging.DEBUG)
logging.info('------- Jevois Cam Startup jevois_capture--------')
ser = serial.Serial(port,115200,timeout=1)

# No windows in headless
if not Headless:
   cv2.namedWindow("jevois", cv2.WINDOW_NORMAL)
   cv2.resizeWindow("jevois",640,480) 

# cam 0 on pi, cam 1 on PC
camera = cv2.VideoCapture(camno)

#initialize the jevois cam. See below - don't change these as it will change the Jevois engine
#to something else
#this should load my custom python code
camera.set(3,640) #width
camera.set(4,480) #height
camera.set(5,10) #fps
s,img = camera.read()
#wait for Yolo to load on camera.
time.sleep(1)

while True:
   s,img = camera.read()
   if not Headless:
      cv2.imshow("jevois", img )
      cv2.waitKey(1)
   line = ser.readline()
   if not Headless:
      print (line.decode('utf8'))
   #example output: "Frame Changed" when the image changes
   
   if len(line)>0:
      if "Frame Changed" in str(line): 
         #save the picture
         folder1 = folder + "/raw/"
         imagefile = datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg'
         if Headless:
           logging.info("writing image: "+imagefile)
         else:
            print("writing image: "+imagefile)
         cv2.imwrite(folder1+imagefile,img)
      

   


