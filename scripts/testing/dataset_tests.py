import sys
sys.path.append("..")
import cv2
import numpy as np
from DatasetBuilding.datasetBuilder import DatasetBuilder
from DatasetBuilding.datasetParser import DatasetParser
import imutils


scale = 0.1

# cam = cv2.VideoCapture(1)
#
#
# db = DatasetBuilder("face.txt", 50)
#
#
# for i in range(100):
#    ret_val, frame = cam.read()
#    frame = imutils.resize(frame, int(frame.shape[1] * scale), int(frame.shape[0] * scale))
#    # frame = frame[int(frame.shape[0]/2):frame.shape[0]]
#
#    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#    outputs = np.random.rand(2)
#
#
#    db.addDataLine(frame, outputs)
#
#
#
#    cv2.imshow("img", frame)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#       break  # esc to quit
# db.finish()


parser = DatasetParser("04-09-2021__22-47-17_face.txt")
inputs, outputs = parser.loadDataset()
print(inputs)
print(outputs)

imgIdx = 0

while True:
   frame = inputs[imgIdx]
   frame = imutils.resize(frame, int(frame.shape[1] / scale), int(frame.shape[0] / scale))
   cv2.imshow("img", frame)

   if cv2.waitKey(0) & 0xFF == ord('n'):
      if imgIdx < len(inputs)-1:
         imgIdx += 1
   if cv2.waitKey(0) & 0xFF == ord('b'):
      if imgIdx > 0:
         imgIdx -= 1
   if cv2.waitKey(0) & 0xFF == ord('q'):
      break  # esc to quit
