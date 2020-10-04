import cv2
import imutils
import numpy as np
from   lane  import Lane
from DatasetBuilding.videoStreamReceiver import VideoStreamReceiver
from imageProcessing import ImageProcessing
from   utils import getPerspectiveMatrix, createTrackbars, readTrackbars, \
                    saveCalibValues, loadCalibValues, setCalibValues, \
                    drawFeaturesDebugText, drawRoiTrap, drawPerspectiveTrap



############################
###  Init Video Capture  ###
cap_obj = cv2.VideoCapture("../res/driving.mp4")
WIDTH   = 500
HEIGHT  = int((cap_obj.get(cv2.CAP_PROP_FRAME_HEIGHT) * WIDTH) / cap_obj.get(cv2.CAP_PROP_FRAME_WIDTH))


################################
###  Create Trackbar Window  ###
ret, frame = cap_obj.read()
createTrackbars(frame.shape[1], frame.shape[0])
values = loadCalibValues("../res/calibration_values_video")
setCalibValues(values)



NUM_SKIP_FRAMES = 0
frameCount      = 0

imageProcess = ImageProcessing()
lane = Lane()


while cap_obj.isOpened():
   ret, frame = cap_obj.read()


   ################################
   ###  Loop Video for Testing  ###
   if frame is None:
      cap_obj.set(cv2.CAP_PROP_POS_FRAMES, 0)
      continue


   #####################
   ###  Skip Frames  ###
   frameCount += 1
   if frameCount <= NUM_SKIP_FRAMES:
      continue
   frameCount = 0


   ##############################
   ###  Read Trackbar Values  ###
   values = readTrackbars()
   imageProcess.setCalibValues(values)


   ###############################
   ###  Crop and Resize Frame  ###
   frame = imutils.resize(frame, width=WIDTH)
   crop  = imageProcess.cropFrame(frame)


   ############################
   ###  Frame segmentation  ###
   gray   = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
   binImg = imageProcess.segmentFrame(gray, 180)


   #####################
   ###  ROI Masking  ###
   roi = imageProcess.applyRoiMask(binImg)
   drawRoiTrap(frame, values)


   ###############################
   ###  Birds eye Perspective  ###
   warp_img = imageProcess.applyBirdsEyePerspective(roi)
   drawPerspectiveTrap(frame, values)


   #############################################
   ###  Lane detection / Feature Extraction  ###
   lane.updateLaneView(warp_img)
   leftPts, rightPts = lane.findLaneLines(numLanePts=20)
   lane.estimateLaneLines(leftPts, rightPts)
   curv    = lane.getCurvature()
   centerX = lane.getCenter(55)
   coefs   = lane.leftLineCoef


   ########################
   ###  Debugging only  ###
   debug = lane.getDebugFrame()
   debug = lane.debugLanePoints(debug)
   debug = lane.debugLaneEstimation(debug)

   if centerX:
      cv2.line(debug, (centerX, int(debug.shape[0]/2)), (centerX,  debug.shape[0]-1), (255, 0, 0), 1) #FIX CENTER METRIC

   # cv2.line(debug, (int(debug.shape[1]/2), 0), (int(debug.shape[1]/2), debug.shape[0]-1),   (255, 0, 0), 2)

   debug = imutils.resize(debug, width=frame.shape[1])

   # warped_debug = cv2.warpPerspective(debug, Minv, (frame.shape[0], frame.shape[1]), flags=cv2.INTER_LINEAR)
   # warped_debug = cv2.warpPerspective(debug, Minv, (int(800), int(800)), flags=cv2.INTER_LINEAR)


   ##################################
   ###  Show Windows and results  ###
   drawFeaturesDebugText(frame, curv, centerX, coefs)
   cv2.imshow('img_original', frame)
   cv2.imshow('ROI', roi)
   cv2.imshow('Birds eye View', debug)
   # cv2.imshow('Warped Debug', warped_debug)

   key = cv2.waitKey(1) & 0xFF
   if key == ord('s'):
      calibFilePath = "../res/calibration_values_video"
      saveCalibValues(calibFilePath, values)
      break
   elif key == ord('q'):
      break

cv2.destroyAllWindows()







