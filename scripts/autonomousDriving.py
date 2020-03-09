import cv2
import imutils
import numpy as np
from   utils import getPerspectiveMatrix, createTrackbars, readTrackbars, saveCalibValues, loadCalibValues
from   lane  import Lane

def applyMorphOps(frame):
   kernel   = np.ones((3, 5), np.uint8)
   kernel2  = np.ones((3, 3), np.uint8)
   dilation = cv2.dilate(frame,   kernel,  iterations=1)
   erosion  = cv2.erode(dilation, kernel2, iterations=1)
   return erosion

def cropImg(img, cropTopY, cropBotY):
   return img[cropTopY:cropBotY, :]

############################
###  Init Video Capture  ###
cap_obj = cv2.VideoCapture("../res/driving.mp4")
WIDTH   = 500
HEIGHT  = int((cap_obj.get(cv2.CAP_PROP_FRAME_HEIGHT) * WIDTH) / cap_obj.get(cv2.CAP_PROP_FRAME_WIDTH))


##############################
###  Read Trackbar Values  ###
values = loadCalibValues("../res/calibration_values")

lane = Lane()

while cap_obj.isOpened():
   ret, frame = cap_obj.read()

   if frame is None:
      cap_obj.set(cv2.CAP_PROP_POS_FRAMES, 0)
      continue


   ###############################
   ###  Crop and Resize Frame  ###
   frame      = imutils.resize(frame, width=WIDTH)
   cropTopY   = values['crop TopY']
   cropBotY   = values['crop BotY']
   crop       = cropImg(frame, cropTopY, cropBotY)


   ############################
   ###  Frame segmentation  ###
   gray           = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
   thresh, binImg = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
   binImg         = applyMorphOps(binImg)


   #####################
   ###  ROI Masking  ###
   roi_trap = np.array([[(values['roiTL x'], 0),               #TL
                         (values['roiBL x'], binImg.shape[0]), #BL
                         (values['roiBR x'], binImg.shape[0]), #BR
                         (values['roiTR x'], 0)]])             #TR
   roi_mask = np.zeros_like(binImg)
   cv2.fillPoly(roi_mask, roi_trap, 255)
   roi = cv2.bitwise_and(roi_mask, binImg)


   ###############################
   ###  Birds eye Perspective  ###
   top_L, top_R = (values['warperTL x'], 0),        (values['warperTR x'], 0)
   bot_L, bot_R = (values['warperBL x'], cropBotY), (values['warperBR x'], cropBotY)
   src               = np.float32([bot_L, top_L, top_R, bot_R])
   dst               = np.float32([(320, 550), (320, 0), (480, 0), (480, 550)]) #720
   warp_img, M, Minv = getPerspectiveMatrix(roi, src, dst, (800, 500))
   warp_img          = applyMorphOps(warp_img)


   #############################################
   ###  Lane detection / Feature Extraction  ###
   lane.updateLaneView(warp_img)
   leftPts, rightPts = lane.findLaneLines(numLanePts=20)
   lane.estimateLaneLines(leftPts, rightPts)
   curv    = lane.getCurvature()
   centerX = lane.getCenter()


   ########################
   ###  Debugging only  ###
   debug = lane.getDebugFrame()
   debug = lane.debugLanePoints(debug)
   debug = lane.debugLaneEstimation(debug)
   cv2.line(debug, (centerX, 0),               (centerX,               debug.shape[0] - 1), (0, 255, 0), 2)
   cv2.line(debug, (int(debug.shape[1]/2), 0), (int(debug.shape[1]/2), debug.shape[0]-1),   (255, 0, 0), 2)


   ##################################
   ###  Show Windows and results  ###
   cv2.putText(debug, "Curvature = " + str(curv), (200, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (244, 235, 66), 1, cv2.LINE_AA)
   cv2.imshow('img_original',   frame)
   cv2.imshow('ROI',  roi)
   cv2.imshow('Birds eye View', debug)

   key = cv2.waitKey(20) & 0xFF
   if   key == ord('s'):
      calibFilePath = "../res/calibration_values"
      saveCalibValues(calibFilePath, values)
      break
   elif key == ord('q'):
      break

cv2.destroyAllWindows()