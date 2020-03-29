import cv2
import jsonpickle
import numpy as np



def getPerspectiveMatrix(img, src, dst, size):
   transformMatrix    = cv2.getPerspectiveTransform(src, dst)
   transformMatrixInv = cv2.getPerspectiveTransform(dst, src)
   img_warped = cv2.warpPerspective(img, transformMatrix, size, flags=cv2.INTER_LINEAR)

   return img_warped, transformMatrix, transformMatrixInv


def createTrackbars(frameWidth, frameHeight):
   ### Creating slider control window ###
   def doNothing(x):
      pass

   cv2.namedWindow('calib', cv2.WINDOW_NORMAL)
   # Crop slider
   cv2.createTrackbar('crop TopY', 'calib', 0, frameHeight - 2, doNothing)
   cv2.createTrackbar('crop BotY', 'calib', 0, frameHeight - 1, doNothing)
   cv2.setTrackbarPos('crop TopY', 'calib', 176)
   cv2.setTrackbarPos('crop BotY', 'calib', 260)

   # ROI sliders
   cv2.createTrackbar('roiTL x', 'calib', 0, frameWidth - 1, doNothing)
   cv2.createTrackbar('roiTR x', 'calib', 0, frameWidth - 1, doNothing)
   cv2.createTrackbar('roiBL x', 'calib', 0, frameWidth - 1, doNothing)
   cv2.createTrackbar('roiBR x', 'calib', 0, frameWidth - 1, doNothing)
   cv2.setTrackbarPos('roiTL x', 'calib', 215)
   cv2.setTrackbarPos('roiTR x', 'calib', 290)
   cv2.setTrackbarPos('roiBL x', 'calib', 110)
   cv2.setTrackbarPos('roiBR x', 'calib', 490)
   # Perspective warp sliders
   cv2.createTrackbar('warperTL x', 'calib', 0, frameWidth - 1, doNothing)
   cv2.createTrackbar('warperTR x', 'calib', 0, frameWidth - 1, doNothing)
   cv2.createTrackbar('warperBL x', 'calib', 0, frameWidth - 1, doNothing)
   cv2.createTrackbar('warperBR x', 'calib', 0, frameWidth - 1, doNothing)
   cv2.setTrackbarPos('warperTL x', 'calib', 244)
   cv2.setTrackbarPos('warperTR x', 'calib', 261)
   cv2.setTrackbarPos('warperBL x', 'calib', 122)
   cv2.setTrackbarPos('warperBR x', 'calib', 429)

def readTrackbars():
   """ Returns a dict containing trackbar values """
   values = {
      'crop TopY':  cv2.getTrackbarPos('crop TopY', 'calib'),
      'crop BotY':  cv2.getTrackbarPos('crop BotY', 'calib'),

      'roiTL x':    cv2.getTrackbarPos('roiTL x', 'calib'),
      'roiTR x':    cv2.getTrackbarPos('roiTR x', 'calib'),
      'roiBL x':    cv2.getTrackbarPos('roiBL x', 'calib'),
      'roiBR x':    cv2.getTrackbarPos('roiBR x', 'calib'),

      'warperTL x': cv2.getTrackbarPos('warperTL x', 'calib'),
      'warperTR x': cv2.getTrackbarPos('warperTR x', 'calib'),
      'warperBL x': cv2.getTrackbarPos('warperBL x', 'calib'),
      'warperBR x': cv2.getTrackbarPos('warperBR x', 'calib')
   }
   return values

def saveCalibValues(filename, values):
   f = open(filename, 'w')
   f.write(jsonpickle.encode(values))

def loadCalibValues(filename):
   f = open(filename, 'r')
   values = jsonpickle.decode(f.read())
   return values

def setCalibValues(values):
   # Crop slider
   cv2.setTrackbarPos('crop TopY', 'calib', values['crop TopY'])
   cv2.setTrackbarPos('crop BotY', 'calib', values['crop BotY'])

   # ROI sliders
   cv2.setTrackbarPos('roiTL x', 'calib', values['roiTL x'])
   cv2.setTrackbarPos('roiTR x', 'calib', values['roiTR x'])
   cv2.setTrackbarPos('roiBL x', 'calib', values['roiBL x'])
   cv2.setTrackbarPos('roiBR x', 'calib', values['roiBR x'])
   # Perspective warp sliders
   cv2.setTrackbarPos('warperTL x', 'calib', values['warperTL x'])
   cv2.setTrackbarPos('warperTR x', 'calib', values['warperTR x'])
   cv2.setTrackbarPos('warperBL x', 'calib', values['warperBL x'])
   cv2.setTrackbarPos('warperBR x', 'calib', values['warperBR x'])






