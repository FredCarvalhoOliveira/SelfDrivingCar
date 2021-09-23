from picamera.array import PiRGBArray
from picamera import PiCamera


import numpy as np
import time
import cv2


camera     = PiCamera()
camera.resolution = (160, 128)#(160, 120)#(640, 480)
camera.framerate  = 30
rawCapture = PiRGBArray(camera, size=((160, 128)))

time.sleep(0.1)



for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
        
    cv2.imshow('Original', image)
    
    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

