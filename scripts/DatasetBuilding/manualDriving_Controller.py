import pygame, sys
import socket
from scripts.utils import loadCalibValues, drawFeaturesDebugText
from time import sleep
import cv2
import numpy as np
from remoteController import RemoteController
from videoStreamReceiver import VideoStreamReceiver
from scripts.imageProcessing import ImageProcessing
from datasetBuilder import DatasetBuilder
import imutils


# host = '192.168.2.245'  # myLocalIp
host = '192.168.1.6'  # myLocalIp

# Init RemoteControl
remoteController = RemoteController()
remoteController.setupCommChannel(host, 5005)

# Init VideoStream Receiver
videoReceiver = VideoStreamReceiver()
videoReceiver.setupVideoStreamReceiver(host, 8089)

# Init Image Processing and load calibration
calibValues = loadCalibValues("../../res/calibration_values_new")
imgProcess = ImageProcessing()
imgProcess.setCalibValues(calibValues)

# Init dataset builder
db = DatasetBuilder("carTest.txt", 50)

MESSAGE_SIZE = 13
while True:

   leftVertical, rightHorizontal = remoteController.readJoysticks()
   remoteController.sendCommands(leftVertical, rightHorizontal, MESSAGE_SIZE)

   # Receive Frame and resize it
   frame = videoReceiver.recvVideoFrame()


   db.addDataLine(frame, np.array([leftVertical, rightHorizontal]))


   scale = 5
   frame = imutils.resize(frame, frame.shape[1] * scale, frame.shape[0] * scale)
   # # Feature extraction
   # croppedImg = imgProcess.cropFrame(frame)
   # binImg     = imgProcess.segmentFrame(croppedImg)
   # roi        = imgProcess.applyRoiMask(binImg)
   # warp_img   = imgProcess.applyBirdsEyePerspective(roi)
   # curv, centerX, coefs = imgProcess.extractLaneFeatures(warp_img)

   # # Debugging
   # lane  = imgProcess.getLane()
   # debug = lane.getDebugFrame()
   # debug = lane.debugLanePoints(debug)
   # debug = lane.debugLaneEstimation(debug)
   # debug = imutils.resize(debug, width=frame.shape[1])
   #
   # drawFeaturesDebugText(debug, curv, centerX, coefs)

   # Display
   cv2.imshow('frame', frame)
   # cv2.imshow('Debug Frame', debug)

   if cv2.waitKey(1) & 0xFF == ord('q'):
      print('Done')
      break

db.finish()
videoReceiver.endConnection()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()



