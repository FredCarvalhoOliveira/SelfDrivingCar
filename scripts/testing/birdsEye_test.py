import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import getPerspectiveMatrix

cap_obj = cv2.VideoCapture("../res/driving.mp4")
while cap_obj.isOpened():
   ret, frame = cap_obj.read()

   if frame is None:
      cap_obj.set(cv2.CAP_PROP_POS_FRAMES, 0)
      continue


   # img  = cv2.imread("../res/road.jpg")
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   crop = gray[440:, :] #450 pode ser
   thresh, binImg = cv2.threshold(crop, 180, 255, cv2.THRESH_BINARY)

   #ROI
   roi_trap = np.array([[(460, 0), #TL
                        (100, binImg.shape[0]), #BL
                        (1250, binImg.shape[0]), #BR
                        (760, 0)]]) #TR
   roi_mask = np.zeros_like(binImg)
   cv2.fillPoly(roi_mask, roi_trap, 255)
   roi = cv2.bitwise_and(roi_mask, binImg)

   #Birds eye Perspective
   top_L, top_R = [590, 0], [660, 0]
   bot_L, bot_R = [280, 680], [1118, 680]

   src = np.float32([bot_L, top_L, top_R, bot_R])
   dst = np.float32([(250, 720), (250, 0), (430, 0), (430, 720)])
   warp_img, M, Minv = getPerspectiveMatrix(roi, src, dst, (720, 720))
   # dewarp = cv2.warpPerspective(warp_img, Minv, (roi.shape[1], roi.shape[0]), flags=cv2.INTER_LINEAR)


   cv2.imshow('img_original',  frame)
   cv2.imshow('img_debugging', roi)
   cv2.imshow('img_debugging2', warp_img)
   if cv2.waitKey(20) & 0xFF == ord('q'):
      break

   plt.plot(np.sum(warp_img, axis=0))
   plt.show()

cv2.destroyAllWindows()

