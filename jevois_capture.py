#!/usr/bin/python3
#capture changes in the background picture to be used for training Yolo

import os,sys
import time
import shutil
import cv2
import serial
import logging
from datetime import datetime

def SendParm(cmd):
   ser.write (cmd)
   time.sleep(1)
   line = ser.readline()
   if Headless:
      logging.info(cmd.decode('utf8'))
      logging.info(line.decode('utf8'))
   else:
      print (cmd.decode('utf8'))
      print (line.decode('utf8'))
      
#main -------
thresh=1000000 # default detection threshold **in pixels**
Headless=True

#Headless=False #for debugging. Remove for deployment
if len(sys.argv)>1:
   if sys.argv[1]=='-show':
      Headless=False
   elif 'thresh' in sys.argv[1]: 
      thresh_arg=sys.argv[1].split("=")
      thresh=int(thresh_arg[1])

if len(sys.argv)>2:
   if 'thresh' in sys.argv[2]:
      thresh_arg=sys.argv[2].split("=")
      thresh=int(thresh_arg[1])

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

SendParm (b'setpar serout All\n') # output everything on serial
time.sleep(2)

tps = 'setthresh '+str(thresh)+'\n'
thresh_param = tps.encode('utf-8')
SendParm (thresh_param) # set the threshold for detection %
time.sleep(1)
frameno=0
while True:
   if not Headless:
      s,img = camera.read()
      cv2.imshow("jevois", img )
      cv2.waitKey(1)
   line = ser.readline()
   if not Headless:
      print (line.decode('utf8'))
   #example output: "Frame Changed" when the image changes
   
   if len(line)>0:
      if "Frame Changed" in str(line):
         s,img = camera.read()
         frameno=frameno+1
         if frameno % 3 == 0:#reduce the number of dups
            #save the picture
#            folder1 = folder + "/raw/"
            folder1=folder + "/"
            imagefile = datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg'
            if Headless:
              logging.info("writing image: "+imagefile)
            else:
              print("writing image: "+imagefile)
            cv2.imwrite(folder1+imagefile,img)
      else:
         if Headless:
           #log every 1000 to avoid overwhelming the log
            if frameno % 100 == 0:
               logging.info(line.decode('utf8'))
         else:
            print(line.decode('utf8'))

   


