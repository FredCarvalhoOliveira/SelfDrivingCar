import numpy as np
import cv2

class Lane:
   def __init__(self):
      self.__original        = None
      self.__laneView        = None
      self.__sliderWindWidth = 50  # maybe change this
      self.leftLine          = None
      self.rightLine         = None
      self.leftLineCoef      = None
      self.rightLineCoef     = None
      self.__leftLinePoints  = None
      self.__rightLinePoints = None
      self.__numLanePoints   = None


   def updateLaneView(self, viewImg):
      self.__original = viewImg
      self.__laneView = viewImg/255


   def __sliceWindow(self, windowTopLeftCoords, width, height):
      x = windowTopLeftCoords[0]
      y = windowTopLeftCoords[1]

      window = self.__laneView[y+1 : y+height+1,  x+1 : x+width+1]

      return window


   def findLaneLine(self, numLanePts, isLeftLane):
      MAX_X_OFFSET     = 20
      line             = np.zeros((numLanePts, 2)).astype(int) # [0, 0] values although valid will be ignored
      sliderWindHeight = int(self.__laneView.shape[0] / numLanePts)
      last_coords      = None

      # Pixel ranges to slide the windows
      if isLeftLane:
         # Left To Right
         iterPxls = np.arange(0, self.__laneView.shape[1] - self.__sliderWindWidth + 1, self.__sliderWindWidth)
      else:
         # Right To Left
         iterPxls = np.arange(self.__laneView.shape[1] - self.__sliderWindWidth, -1, -self.__sliderWindWidth)

      pointIdx = 0
      # Bottom to Top
      for windowY in np.arange(self.__laneView.shape[0] -1 -sliderWindHeight, -1, -sliderWindHeight):
         # NOTE: LAST ITER WINDOW SIZE MIGHT BE SMALLER THAN OTHERS FIX?
         lanePoint = None

         for windowX in iterPxls:
            # slice ROI FOR PIXEL ANALYSIS
            windowTopLeftCoords = (windowX, windowY)
            window = self.__sliceWindow(windowTopLeftCoords, self.__sliderWindWidth, sliderWindHeight)

            rows, cols = np.where(window == 1)
            coordsX    = cols + windowTopLeftCoords[0]

            # Are there enough white pixels to be considered a point
            if len(coordsX > 10):
               lanePoint = [int(np.mean(coordsX)), windowY + int(sliderWindHeight/2)]
               break

         # Lane point found, save it and update last point var
         if lanePoint is not None:
            if not line.any():
               # Middle validation only occurs for first line point
               if isLeftLane:
                  if lanePoint[0] <= int(self.__laneView.shape[1]/2):
                     # is valid
                     last_coords = lanePoint
                     line[pointIdx] = lanePoint
               else:
                  if lanePoint[0] > int(self.__laneView.shape[1]/2):
                     # is valid
                     last_coords = lanePoint
                     line[pointIdx] = lanePoint

            else:
               if last_coords is None or abs(lanePoint[0] - last_coords[0]) <= MAX_X_OFFSET:
                  last_coords = lanePoint
                  line[pointIdx] = lanePoint

         pointIdx += 1

      return np.array(line)


   def findLaneLines(self, numLanePts):
      self.__numLanePoints = numLanePts

      leftLinePts            = self.findLaneLine(numLanePts, isLeftLane=True)
      self.__leftLinePoints  = leftLinePts[~np.all(leftLinePts == 0, axis=1)]
      rightLinePts           = self.findLaneLine(numLanePts, isLeftLane=False)
      self.__rightLinePoints = rightLinePts[~np.all(rightLinePts == 0, axis=1)]

      return self.__leftLinePoints, self.__rightLinePoints


   def fitCurve(self, lanePts):
      # At Least this many points to make a good estimation
      minLanePtsAcceptable = self.__numLanePoints * 0.25

      if len(lanePts) > minLanePtsAcceptable:
         # invert coords
         x = lanePts[:, 1]
         y = lanePts[:, 0]
         # calculate polynomial
         coef = np.polyfit(x, y, 2)  # CONSIDER PASSING Z COEFFICIENTS TO NEURAL NET
         f    = np.poly1d(coef)
         return f, coef
      else:
         return None


   def estimateLaneLines(self, leftLinePts, rightLinePts):
      self.leftLine  = None
      self.rightLine = None
      leftLineInfo   = self.fitCurve(leftLinePts)
      rightLineInfo  = self.fitCurve(rightLinePts)

      if leftLineInfo is not None:
         leftLine, leftLineCoef = leftLineInfo
         self.leftLine     = leftLine
         self.leftLineCoef = leftLineCoef

      if rightLineInfo is not None:
         rightLine, rightLineCoef = rightLineInfo
         self.rightLine     = rightLine
         self.rightLineCoef = rightLineCoef

      return self.leftLine, self.rightLine


   def getCurvature(self):
      # as duas estao boas fazer a media
      # uma esta boa usar essa
      # nenhuma esta boa return None
      if self.leftLine is None:
         return None
      return int(self.leftLine(0) - self.leftLine(self.__laneView.shape[0]-1))


   def getCenter(self, distanceToKeep):
      if self.leftLine is None and self.rightLine is None:
         return None

      # Can see left line, Cant see right line
      elif callable(self.leftLine) and self.rightLine is None:
         bottomLeftLine = self.leftLine(self.__laneView.shape[0]-1)
         return int(bottomLeftLine + distanceToKeep)

      # Cant see left line, Can see right line
      elif self.leftLine is None and callable(self.rightLine):
         bottomRightLine = self.rightLine(self.__laneView.shape[0]-1)
         return int(bottomRightLine - distanceToKeep)

      # Can see both
      else:
         bottomLeftLine  = self.leftLine(self.__laneView.shape[0]-1)
         bottomRightLine = self.rightLine(self.__laneView.shape[0]-1)
         return int(bottomLeftLine + (bottomRightLine - bottomLeftLine)/2)


   #########################
   ###  DEBUG FUNCTIONS  ###

   def debugLanePoints(self, debugFrame):
      for pt in self.__leftLinePoints:
         cv2.circle(debugFrame, (pt[0],      pt[1]), 2, (0, 255, 0), -1)
         cv2.circle(debugFrame, (pt[0] + 20, pt[1]), 1, (0, 0, 255), -1)
      for pt in self.__rightLinePoints:
         cv2.circle(debugFrame, (pt[0],      pt[1]), 2, (255, 0, 0), -1)
         cv2.circle(debugFrame, (pt[0] + 20, pt[1]), 1,  (0, 0, 255), -1)
      return debugFrame


   def debugLaneEstimation(self, debugFrame):
      if self.leftLine is not None:
         for pxl in range(debugFrame.shape[0]):
            cv2.circle(debugFrame, (int(self.leftLine(pxl)), pxl), 2, (0, 255, 0), -1)

      if self.rightLine is not None:
         for pxl in range(debugFrame.shape[0]):
            cv2.circle(debugFrame, (int(self.rightLine(pxl)), pxl), 2, (0, 255, 0), -1)

      return debugFrame

   def getDebugFrame(self):
      frame = self.__original.copy()
      frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
      return frame




