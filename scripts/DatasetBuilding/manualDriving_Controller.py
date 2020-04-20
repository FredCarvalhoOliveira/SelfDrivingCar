import pygame, sys
import socket
from scripts.utils import loadCalibValues, writeFeaturesDebugText
from time import sleep
import cv2
from remoteController import RemoteController
from videoStreamReceiver import VideoStreamReceiver
from scripts.imageProcessing import ImageProcessing
from datasetBuilder import DatasetBuilder
import imutils

host = '192.168.1.8'  # myLocalIp

# Init RemoteControl
remoteController = RemoteController()
remoteController.setupCommChannel(host, 5005)

# Init VideoStream Receiver
videoReceiver = VideoStreamReceiver()
videoReceiver.setupVideoStreamReceiver(host, 8089)

# Init Image Processing and load calibration
calibValues = loadCalibValues("../../res/calibration_values")
imgProcess = ImageProcessing()
imgProcess.setCalibValues(calibValues)

# Define the codec and instantiate VideoWriter object
# fourcc      = cv2.VideoWriter_fourcc(*'mp4v')
# vidRecorder = cv2.VideoWriter('../../res/VideoRecording.mp4', fourcc, 20.0, (frame.shape[1], frame.shape[0]))

# Dataset Builder
# datasetBuilder = DatasetBuilder("carTest.txt", 1000)

MESSAGE_SIZE = 13
while True:

   leftVertical, rightHorizontal = remoteController.readJoysticks()
   remoteController.sendCommands(leftVertical, rightHorizontal, MESSAGE_SIZE)

   # Receive Frame and resize it
   frame = videoReceiver.recvVideoFrame()

   # Save Video Frame
   # backtorgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
   # vidRecorder.write(backtorgb)


   scale = 5
   frame = imutils.resize(frame, frame.shape[1] * scale, frame.shape[0] * scale)
   # Feature extraction
   croppedImg = imgProcess.cropFrame(frame)
   binImg     = imgProcess.segmentFrame(croppedImg, 30)
   roi        = imgProcess.applyRoiMask(binImg)
   warp_img   = imgProcess.applyBirdsEyePerspective(roi)
   curv, centerX, coefs = imgProcess.extractLaneFeatures(warp_img)

   # Debugging
   lane  = imgProcess.getLane()
   debug = lane.getDebugFrame()
   debug = lane.debugLanePoints(debug)
   debug = lane.debugLaneEstimation(debug)
   debug = imutils.resize(debug, width=frame.shape[1])

   writeFeaturesDebugText(debug, curv, centerX, coefs)

   # Display
   cv2.imshow('frame', frame)
   cv2.imshow('Debug Frame', debug)

   if cv2.waitKey(1) & 0xFF == ord('q'):
      print('Done')
      break


videoReceiver.endConnection()
#vidRecorder.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()



