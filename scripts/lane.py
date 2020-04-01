import numpy as np
import cv2

class Lane:
   def __init__(self):
      self.__original        = None
      self.__laneView        = None
      self.__sliderWindWidth = 50
      self.leftLine          = None
      self.rightLine         = None
      self.leftLineCoef      = None
      self.rightLineCoef     = None

   def updateLaneView(self, viewImg):
      self.__original = viewImg
      self.__laneView = viewImg/255



   def __sliceWindow(self, windowTopLeftCoords, width, height):
      x = windowTopLeftCoords[0]
      y = windowTopLeftCoords[1]

      window = self.__laneView[y+1 : y+height+1,  x+1 : x+width+1]

      return window

   def __findPointInSearchWindow(self, window, windowLeftX):
      return np.where(window == 1)

   def findLaneLine2(self, numLanePts, isLeftLane):
      MAX_X_OFFSET     = 20
      line = []
      sliderWindHeight = int(self.__laneView.shape[1] / numLanePts)  # review shape index
      windowY = self.__laneView.shape[1] - sliderWindHeight
      last_coords = None

      # for pointIndex in range(numLanePts)




   def findLaneLine(self, numLanePts, isLeftLane):
      MAX_X_OFFSET     = 20
      line             = []
      sliderWindHeight = int(self.__laneView.shape[0] / numLanePts)  # review shape index
      last_coords      = None



      # Pixel ranges to slide the windows
      if isLeftLane:
         iterPxls = np.arange(0, self.__laneView.shape[1] - self.__sliderWindWidth + 1, self.__sliderWindWidth)
      else:
         iterPxls = np.arange(self.__laneView.shape[1] - self.__sliderWindWidth, -1, -self.__sliderWindWidth)


      for pointIndex in np.arange(numLanePts-1, -1, -1):
         lanePoint = None

         windowY = pointIndex * sliderWindHeight

         for x in iterPxls:
            # slice ROI FOR PIXEL ANALYSIS

            windowTopLeftCoords = (x, windowY)
            window = self.__sliceWindow(windowTopLeftCoords, self.__sliderWindWidth, sliderWindHeight)

            rows, cols = np.where(window == 1)
            coordsX    = cols + windowTopLeftCoords[0]

            # Are there enough white pixels to be considered a point
            if len(coordsX > 10):
               lanePoint = (int(np.mean(coordsX)), windowY + int(sliderWindHeight/2))
               break


         # Lane point found, save it and update last point var
         if lanePoint is not None:
            if not line:
               # Middle validation only occurs for first line point
               if isLeftLane:
                  if lanePoint[0] <= int(self.__laneView.shape[1]/2):
                     # is valid
                     last_coords = lanePoint
                     line.append(lanePoint)
               else:
                  if lanePoint[0] > int(self.__laneView.shape[1]/2):
                     # is valid
                     last_coords = lanePoint
                     line.append(lanePoint)
            else:
               if last_coords is None or abs(lanePoint[0] - last_coords[0]) <= MAX_X_OFFSET:
                  last_coords = lanePoint
                  line.append(lanePoint)

      return np.array(line)


   def findLaneLines(self, numLanePts):
      leftLinePts  = self.findLaneLine(numLanePts, isLeftLane=True)
      rightLinePts = self.findLaneLine(numLanePts, isLeftLane=False)
      return leftLinePts, rightLinePts


   def fitCurve(self, lanePts):
      if len(lanePts) > 0:
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
      if self.fitCurve(leftLinePts) is not None and self.fitCurve(rightLinePts) is not None:
         leftLine,  leftLineCoef  = self.fitCurve(leftLinePts)
         rightLine, rightLineCoef = self.fitCurve(rightLinePts)
         self.leftLine      = leftLine
         self.leftLineCoef  = leftLineCoef
         self.rightLine     = rightLine
         self.rightLineCoef = rightLineCoef
         return leftLine, rightLine
      #else the lines stay the same

   def getCurvature(self):
      if self.leftLine is None:
         return None
      return int(self.leftLine(0) - self.leftLine(self.__laneView.shape[0]-1))

   def getCenter(self):
      if self.leftLine is None or self.rightLine is None:
         return None
      bottomLeftLine  = self.leftLine(self.__laneView.shape[0]-1)
      bottomRightLine = self.rightLine(self.__laneView.shape[0]-1)
      return int(bottomLeftLine + (bottomRightLine - bottomLeftLine)/2)


   #########################
   ###  DEBUG FUNCTIONS  ###

   def debugLanePoints(self, debugFrame):
      leftPts, rightPts = self.findLaneLines(numLanePts=20)
      for pt in leftPts:
         cv2.circle(debugFrame, (pt[0],      pt[1]), 2, (0, 255, 0), -1)
         cv2.circle(debugFrame, (pt[0] + 20, pt[1]), 1,  (0, 0, 255), -1)
      for pt in rightPts:
         cv2.circle(debugFrame, (pt[0],      pt[1]), 2, (255, 0, 0), -1)
         cv2.circle(debugFrame, (pt[0] + 20, pt[1]), 1,  (0, 0, 255), -1)
      return debugFrame

   def debugLaneEstimation(self, debugFrame):
      if self.leftLine is None or self.rightLine is None:
         return debugFrame
      for pxl in range(debugFrame.shape[0]):
         cv2.circle(debugFrame, (int(self.leftLine(pxl)),  pxl), 2, (0, 255, 0), -1)
         cv2.circle(debugFrame, (int(self.rightLine(pxl)), pxl), 2, (0, 255, 0), -1)
      return debugFrame

   def getDebugFrame(self):
      frame = self.__original
      frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
      return frame




