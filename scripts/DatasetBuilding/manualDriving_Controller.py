import pygame, sys
import socket
from scripts.utils import loadCalibValues, writeFeaturesDebugText
from time import sleep
import cv2
from videoStreamReceiver import VideoStreamReceiver
from scripts.imageProcessing import ImageProcessing
import imutils

import warnings
warnings.filterwarnings('ignore')

# setup the pygame window
pygame.init()
window = pygame.display.set_mode((200, 200), 0, 32)

# how many joysticks connected to computer?
joystick_count = pygame.joystick.get_count()
print("There is " + str(joystick_count) + " joystick/s")

if joystick_count == 0:
   # if no joysticks, quit program safely
   print("Error, I did not find any joysticks")
   pygame.quit()
   sys.exit()
else:
   # initialise joystick
   joystick = pygame.joystick.Joystick(0)
   joystick.init()

axis_map = {
   "leftVertical":    1,  # 1, 4
   "rightHorizontal": 4
}

def buildControlMsg(axis_map):
   msg  = ""
   msg += str(joystick.get_axis(axis_map["leftVertical"]) * -1)   + ";    "
   msg += str(joystick.get_axis(axis_map["rightHorizontal"]))
   return msg


# # Setup UDP socket
# host = '192.168.1.5'  # car local Ip
# port = 5005
# s = socket.socket(socket.AF_INET,  # Internet
#                   socket.SOCK_DGRAM)
# print("connecting")
# s.connect((host, port))
# print("connected")

videoReceiver = VideoStreamReceiver()
videoReceiver.setupVideoStreamReceiver('192.168.1.4', 8089)

calibValues = loadCalibValues("../../res/calibration_values")

imgProcess = ImageProcessing()
imgProcess.setCalibValues(calibValues)

# Receive first Frame and resize it
frame = videoReceiver.recvVideoFrame()

# Define the codec and create VideoWriter object
RECORD_VIDEO = True
fourcc      = cv2.VideoWriter_fourcc(*'mp4v')
vidRecorder = cv2.VideoWriter('../../res/VideoRecording.mp4', fourcc, 15.0, (frame.shape[1], frame.shape[0]))



while True:
   for event in pygame.event.get():
      # loop through events, if window shut down, quit program
      if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()

   # Build and send control message
   msg = buildControlMsg(axis_map)
   # s.sendall(msg.encode('utf-8'))


   # Receive Frame and resize it
   frame = videoReceiver.recvVideoFrame()

   # Save Video Frame
   backtorgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
   vidRecorder.write(backtorgb)


   scale = 5
   frame = imutils.resize(frame, frame.shape[1] * scale, frame.shape[0] * scale)
   # Feature extraction
   croppedImg = imgProcess.cropFrame(frame)
   binImg     = imgProcess.segmentFrame(croppedImg, 180)
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
      videoReceiver.endConnection()
      vidRecorder.release()
      break

cv2.destroyAllWindows()
pygame.quit()
sys.exit()



