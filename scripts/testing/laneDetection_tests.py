import numpy as np
import cv2

img            = cv2.imread('../../res/road_test.jpg')
frame          = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh, binImg = cv2.threshold(frame, 180, 255, cv2.THRESH_BINARY)

class Lane:
   def __init__(self):
      self.__laneView        = binImg/255
      self.__numLanePts      = 30
      self.__sliderWindWidth = 50

   def updateLaneView(self, viewImg):
      self.__laneView = viewImg

   def findLaneLines(self):

      leftLine  = [None]*self.__numLanePts
      # rightLine = [None]*self.__numLanePts

      sliderWindHeight = int(self.__laneView.shape[1] / self.__numLanePts)
      windowY          = self.__laneView.shape[1] - sliderWindHeight


      for pointIndex in range(self.__numLanePts):
         for x in range(self.__laneView.shape[0]):
            #slice ROI FOR PIXEL ANALYSIS
            window = self.__laneView[windowY: windowY+sliderWindHeight, x: x+self.__sliderWindWidth]
            rows,    cols = np.where(window == 1)
            coordsX       = cols + x

            leftLineCoords = (0, 0)
            if len(coordsX) > int(window.shape[0] * window.shape[1] * 0.3):
               print(len(coordsX))
               print(window)
               print('Window Area = ' + str(window.shape[0] * window.shape[1]))
               leftLineCoords = (int(np.mean(coordsX)), int(windowY+sliderWindHeight/2))
               cv2.rectangle(img, (x, windowY), (x+self.__sliderWindWidth, windowY+sliderWindHeight), (0, 255, 0), 3)
               break

         leftLine[pointIndex] = leftLineCoords
         windowY -= sliderWindHeight


      # print(str(coordsX) + ' ' + str(coordsY))
      return leftLine

   # def extractLaneFeautures(self):


lane       = Lane()
lanePoints = lane.findLaneLines()

for coord in lanePoints:
   cv2.circle(img, coord, 10, (0, 255, 0), -1)

cv2.imshow('img_debugging', img)
cv2.waitKey(0)
cv2.destroyAllWindows()