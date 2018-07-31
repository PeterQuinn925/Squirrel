import libjevois as jevois
import cv2
import numpy as np

lastimg =None #initialize global. todo: figure out how to put in the class
lastcolorimg=None
x=1000000 #number of pixel changes before the scene is deemed to be different.

## Store changed images
#
# Write a message to the serial output anytime the image changes more than x pixels

#
# @author peter quinn
# 
# @videomapping YUYV 640 480 10 YUYV 640 480 15 PDQ CV_Diff
# @email peterquinn925@gmail.com
# @address 123 first street, Los Angeles CA 90012, USA
# @copyright Copyright (C) 2018 by peter quinn
# @mainurl 
# @supporturl 
# @otherurl 
# @license 
# @distribution Unrestricted
# @restrictions None
# @ingroup modules
class CV_Diff:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("processing timer", 100, jevois.LOG_INFO)
        # a simple frame counter used to demonstrate sendSerial():
        self.frame = 0
        
    # ###################################################################################################
    ## Process function with no USB output
    def processNoUSB(self, inframe):
        # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR. If you need a
        # grayscale image, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB() and getCvRGBA():
        inimg = inframe.getCvGRAY()

        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()
        
        jevois.LINFO("Processing video frame {} now...".format(self.frame))

        # TODO: you should implement some processing.
        # Once you have some results, send serial output messages:

        # Get frames/s info from our timer:
        fps = self.timer.stop()

        # Send a serial output message:
        jevois.sendSerial("DONE frame {} - {}".format(self.frame, fps));
        self.frame += 1
        
    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe, outframe):
        global lastimg
        global lastcolorimg
        global x #num of changed pixels before considering the scene different
        
        # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR. If you need a
        # grayscale image, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB() and getCvRGBA():
        inimg = inframe.getCvGRAY()
        colorimg = inframe.getCvBGR()
        if lastimg is None:
           lastimg =  inframe.getCvGRAY()
           lastcolorimg = colorimg
        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()
    
        diffimg= cv2.absdiff(inimg,lastimg) # compare two images. Will be all black if they are the same.
        totaldiff = np.sum(diffimg) #count how many pixels are not black
        
        if totaldiff > x: #the image has changed, update it.
            outimg=colorimg
            lastcolorimg=colorimg
            jevois.sendSerial("Frame Changed");
        else:
            #outimg = diffimg #use for checking the tolerances
            outimg = lastcolorimg
            
        lastimg = inframe.getCvGRAY()
        # Write a title:
        cv2.putText(outimg, "JeVois CV_Diff", (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        
        # Write frames/s info from our timer into the edge map (NOTE: does not account for output conversion time):
        fps = self.timer.stop()#not used
        height = outimg.shape[0]
        width = outimg.shape[1]
        cv2.putText(outimg, str(totaldiff), (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        
        # Convert our output image to video output format and send to host over USB:
        outframe.sendCv(outimg)

        # Example of sending some serial output message:
        jevois.sendSerial("DONE frame {}".format(self.frame));
        self.frame += 1
        
    # ###################################################################################################
    ## Parse a serial command forwarded to us by the JeVois Engine, return a string
    def parseSerial(self, str):
        global x #the threshold pixels to trigger a change
        jevois.LINFO("parseserial received command [{}]".format(str))
        if str == "hello":
            return self.hello()
        elif "setthresh" in str:
           inputline=str.split(" ")
           x=int(inputline[1])
           return self.setthresh()
        else:
           return "ERR Unsupported command"
    
    # ###################################################################################################
    ## Return a string that describes the custom commands we support, for the JeVois help message
    def supportedCommands(self):
        # use \n seperator if your module supports several commands
        return "setthresh"

    # ###################################################################################################
    ## Internal method that gets invoked as a custom command
    def hello(self):
        return "Hello from python!"
    def setthresh(self):
        return "Threshold set"     
