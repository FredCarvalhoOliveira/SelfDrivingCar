import sys
sys.path.append("..")

import pygame, sys
import socket
from scripts.utils import loadCalibValues, drawFeaturesDebugText
from time import sleep
import cv2
import torch
import numpy as np
from DatasetBuilding.remoteController import RemoteController
from DatasetBuilding.videoStreamReceiver import VideoStreamReceiver
import imutils
from modelCNN import CNN


# Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load Model
model = CNN()
model.load_state_dict(torch.load("../../res/models/FINAL_CNN_epochs_500_2.0"))
model.eval()


# host = '192.168.2.245'  # myLocalIp
host = '192.168.1.3'  # myLocalIp

# Init RemoteControl
remoteController = RemoteController()
remoteController.setupCommChannel(host, 5005)

# Init VideoStream Receiver
videoReceiver = VideoStreamReceiver()
videoReceiver.setupVideoStreamReceiver(host, 8089)

# # Init Image Processing and load calibration
# calibValues = loadCalibValues("../../res/calibration_values_new")
# imgProcess = ImageProcessing()
# imgProcess.setCalibValues(calibValues)

MESSAGE_SIZE = 13
while True:

   # leftVertical, rightHorizontal = remoteController.readJoysticks()
   # remoteController.sendCommands(leftVertical, rightHorizontal, MESSAGE_SIZE)

   # Receive Frame and resize it
   frame = videoReceiver.recvVideoFrame()

   # Document this TESTING
   inputs = torch.from_numpy(frame).view(1, frame.shape[0], frame.shape[1]).float()
   inputs = inputs.view(1, 1, inputs.shape[1], inputs.shape[2])


   preds = model(inputs)
   preds = preds.flatten().detach().numpy()
   accel = preds[0]
   accel = max(min(accel, 1), -1)
   accel = float("%.3f" % accel)


   steer = preds[1]
   steer = max(min(steer, 1), -1)
   steer = float("%.3f" % steer)



   remoteController.sendCommands(accel, steer, MESSAGE_SIZE)


   scale = 5
   frame = imutils.resize(frame, frame.shape[1] * scale, frame.shape[0] * scale)

   # Display
   cv2.imshow('frame', frame)
   # cv2.imshow('Debug Frame', debug)

   if cv2.waitKey(1) & 0xFF == ord('q'):
      print('Done')
      break

videoReceiver.endConnection()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()



