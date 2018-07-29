#!/usr/bin/python3

import cv2
from datetime import datetime
import time

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

cam = cv2.VideoCapture(0)
x = 130000 #threshhold for image difference to prevent false positives
jpg_limiter = 3 #only save one in n images

#winName = "Movement Indicator"
#cv2.namedWindow(winName, cv2.WINDOW_NORMAL) #commented out for headless
#cv2.resizeWindow(winName, 640, 480) #commented out for headless

s, img = cam.read()
#cv2.imshow( winName, img ) #commented out for headless
time.sleep(30) #give the camera a chance to stabilize

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
i=0 # index to limit number of jpgs
while True:
  s, img = cam.read() #not used for diff, needed for view at time of motion
  #cv2.imshow( winName, img ) #commented out for headless
  dimg=diffImg(t_minus, t, t_plus)
  #print (cv2.countNonZero(dimg)) #if you need to tweak x, uncomment this
  if cv2.countNonZero(dimg) > x:
    if i>jpg_limiter:
       #try making the image a little less bright
       #img[:,:,:]=img[:,:,:]*0.50 
       imagefile = "//home//pi//images//P" + datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg'
       cv2.imwrite(imagefile, img)
       i=0
       print (imagefile)
       print (cv2.countNonZero(dimg))
    i=i+1
  # Read next image
  t_minus = t
  t = t_plus
  t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

  key = cv2.waitKey(10)
  if key == 27:
 #   cv2.destroyWindow(winName) #commented out for headless
    break

print ("Goodbye")

