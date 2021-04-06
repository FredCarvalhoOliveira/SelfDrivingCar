import sys
sys.path.append("..")
import cv2
import numpy as np
from DatasetBuilding.datasetBuilder import DatasetBuilder
# import imutils
#
#
# cam = cv2.VideoCapture(1)
#
# scale = 0.1
#
# while True:
#    ret_val, frame = cam.read()
#    frame = imutils.resize(frame, int(frame.shape[1] * scale), int(frame.shape[0] * scale))
#    frame = frame[int(frame.shape[0]/2):frame.shape[0]]
#
#
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#    print(gray.shape)
#
#
#
#
#    cv2.imshow("img", gray)
#
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#       break  # esc to quit
# cv2.destroyAllWindows()




# arr = np.random.rand(5)
# print(arr)
#
# byteArr = arr.tobytes()
# print(byteArr)
# print(type(byteArr))
#
# strArr = str(byteArr)
# print(strArr)
# print(type(strArr))
#
# byteArr = bytes(strArr.decode("utf-8"))
# print(byteArr)
# print(type(byteArr))

# print(np.frombuffer(byteArr))


db = DatasetBuilder("teste.txt", 50)

for i in range(10):
   # inputs = np.random.randint(0, 256, (3, 2))
   # inputs = np.random.randint(0, 256, 2)
   # inputs = np.array([[1, 2], [3, 4]])
   inputs = np.array([[[1, 2], [1, 2]], [[1, 2], [1, 2]]])

   print(inputs)
   outputs = np.random.rand(2)

   db.addDataLine(inputs, outputs)

db.finish()









