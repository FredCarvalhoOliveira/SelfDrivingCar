import math
import sys
import imutils

sys.path.append("..")
import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from DatasetBuilding.drivingDataset import DrivingDataset
from torch.utils.data import DataLoader
from modelCNN import CNN


def drawLivePredictions(frame, acceleration, steering):
   OPEN_ANGLE   = 120
   LINE_LENGTH  = 120
   CENTER       = (int(frame.shape[1]/2), frame.shape[0])
   CENTER_ANGLE = -90
   ACCEL_DISPLAY_OFFSET = 150

   # Angles
   angleLeft   = CENTER_ANGLE - int(OPEN_ANGLE/2)
   angleRight  = CENTER_ANGLE + int(OPEN_ANGLE/2)
   anglePred   = CENTER_ANGLE + int(OPEN_ANGLE/2*steering)

   # Left
   x_left = int(CENTER[0] + math.cos(math.radians(angleLeft)) * LINE_LENGTH)
   y_left = int(CENTER[1] + math.sin(math.radians(angleLeft)) * LINE_LENGTH)

   # Right
   x_right = int(CENTER[0] + math.cos(math.radians(angleRight)) * LINE_LENGTH)
   y_right = int(CENTER[1] + math.sin(math.radians(angleRight)) * LINE_LENGTH)

   # Prediction
   x_pred = int(CENTER[0] + math.cos(math.radians(anglePred)) * LINE_LENGTH)
   y_pred = int(CENTER[1] + math.sin(math.radians(anglePred)) * LINE_LENGTH)

   cv2.line(frame, CENTER, (x_left,  y_left),  (0, 255, 0), 3)
   cv2.line(frame, CENTER, (x_right, y_right), (0, 255, 0), 3)
   cv2.line(frame, CENTER, (x_pred,  y_pred),  (0, 0, 255), 3)

   accelerationColor = (0, 255, 0)
   if acceleration < 0:
      accelerationColor = (0, 0, 255)
   cv2.line(frame, (CENTER[0] - ACCEL_DISPLAY_OFFSET, CENTER[1]), (CENTER[0] - ACCEL_DISPLAY_OFFSET,  int(CENTER[1] - LINE_LENGTH)),  (0, 0, 0), 10)
   cv2.line(frame, (CENTER[0] - ACCEL_DISPLAY_OFFSET, CENTER[1]), (CENTER[0] - ACCEL_DISPLAY_OFFSET,  int(CENTER[1] - LINE_LENGTH * acceleration)),  accelerationColor, 5)

   return frame


# Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load Model
model = CNN()
model.load_state_dict(torch.load("../../res/models/FINAL_CNN_epochs_500_3.0"))
model.eval()

# Load Data
dataset = DrivingDataset("../../res/datasets/full.txt", isTrainSet=False, minAcceleration=0.20)
dataloader = DataLoader(dataset, batch_size=100, shuffle=False)
# inputs, targets = next(iter(dataloader))

end = False
while not end:
   for batchIdx, (batchData, targets) in enumerate(dataloader):
      for frame in batchData:
         preds = model(frame.view(1, 1, frame.shape[1], frame.shape[2]))
         preds = preds.flatten().detach().numpy()
         accel = preds[0]
         steer = preds[1]
         steer = max(min(steer, 1), -1)

         frame = frame[0].numpy().astype(np.uint8)
         frame = np.dstack((frame, frame))
         frame = np.dstack((frame, frame))
         frame = imutils.resize(frame, width=500)



         drawLivePredictions(frame, acceleration=accel, steering=steer)

         frame = imutils.resize(frame, width=1000)


         cv2.imshow('Live Model Decisions', frame)
         if cv2.waitKey(100) & 0xFF == ord('q'):
            end = True
            break
      if end:
         break

cv2.destroyAllWindows()
