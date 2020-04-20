from scripts.utils import getPerspectiveMatrix
from scripts.lane import Lane
import numpy as np
import cv2

class ImageProcessing:
   def __init__(self):
      self.calibValues = None
      self.lane = Lane()

   def setCalibValues(self, calibValues):
      self.calibValues = calibValues

   def getLane(self):
      # Debugging purposes
      return self.lane

   def cropFrame(self, frame):
      cropTopY   = self.calibValues['crop TopY']
      cropBotY   = self.calibValues['crop BotY']
      croppedImg = self.__cropImg(frame, cropTopY, cropBotY)
      return croppedImg

   def segmentFrame(self, grayScaleFrame, threshold=180):
      thresh, binaryImg = cv2.threshold(grayScaleFrame, threshold, 255, cv2.THRESH_BINARY)
      binaryImg = self.__applyMorphOps(binaryImg)
      return binaryImg

   def applyRoiMask(self, binaryImg):
      roi_trap = np.array([[(self.calibValues['roiTL x'], 0),  # TL
                            (self.calibValues['roiBL x'], binaryImg.shape[0]),  # BL
                            (self.calibValues['roiBR x'], binaryImg.shape[0]),  # BR
                            (self.calibValues['roiTR x'], 0)]])  # TR
      roi_mask = np.zeros_like(binaryImg)
      cv2.fillPoly(roi_mask, roi_trap, 255)
      roi = cv2.bitwise_and(roi_mask, binaryImg)
      return roi

   def applyBirdsEyePerspective(self, binaryImg):
      top_L, top_R = (self.calibValues['warperTL x'], 0),                             \
                     (self.calibValues['warperTR x'], 0)
      bot_L, bot_R = (self.calibValues['warperBL x'], self.calibValues['crop BotY']), \
                     (self.calibValues['warperBR x'], self.calibValues['crop BotY'])

      src = np.float32([bot_L, top_L, top_R, bot_R])
      dst = np.float32([(int(160 / 2), int(275 / 2)), (int(160 / 2), int(0)), (int(240 / 2), int(0)),
                        (int(240 / 2), int(275 / 2))])  # 720
      warp_img, M, Minv = getPerspectiveMatrix(binaryImg, src, dst, (int(400 / 2), int(250 / 2)))
      warp_img = self.__applyMorphOps(warp_img)
      return warp_img

   def extractLaneFeatures(self, warp_img):
      self.lane.updateLaneView(warp_img)
      leftPts, rightPts = self.lane.findLaneLines(numLanePts=20)
      self.lane.estimateLaneLines(leftPts, rightPts)
      curv    = self.lane.getCurvature()
      centerX = self.lane.getCenter(55) # TODO CHANGE THIS IMPORTANT!!!! REMOVE ARG FROM HERE
      coef    = self.lane.leftLineCoef
      return curv, centerX, coef


   def __applyMorphOps(self, binaryImg):
      kernel   = np.ones((3, 5), np.uint8)
      kernel2  = np.ones((3, 3), np.uint8)
      dilation = cv2.dilate(binaryImg, kernel,  iterations=1)
      erosion  = cv2.erode(dilation,   kernel2, iterations=1)
      return erosion

   def __cropImg(self, img, cropTopY, cropBotY):
      return img[cropTopY:cropBotY, :]