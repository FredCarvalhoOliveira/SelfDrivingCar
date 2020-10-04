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


def drawFeaturesDebugText(debugFrame, curv, centerX, coefs):
   if curv is None:
      cv2.putText(debugFrame, "Curvature = ",    (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
   else:
      cv2.putText(debugFrame, "Curvature = " + str(curv),    (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

   if centerX is None:
      cv2.putText(debugFrame, "   Center = ", (10, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
   else:
      cv2.putText(debugFrame, "   Center = " + str(centerX), (10, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

   if coefs is None:
      cv2.putText(debugFrame, "   A Coef = ", (10, 47), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
      cv2.putText(debugFrame, "   B Coef = ", (10, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
      cv2.putText(debugFrame, "   C Coef = ", (10, 77), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
   else:
      cv2.putText(debugFrame, "   A Coef = " + str(coefs[0]), (10, 47), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
      cv2.putText(debugFrame, "   B Coef = " + str(coefs[1]), (10, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
      cv2.putText(debugFrame, "   C Coef = " + str(coefs[2]), (10, 77), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)


def drawRoiTrap(frame, values):
   # Adjust trapezoid values for visualization
   cropBotY = values['crop BotY']
   cropTopY = values['crop TopY']
   roi_trap_bottomY = cropBotY - cropTopY
   roi_trap = np.array([[(values['roiTL x'], 0),  # TL
                         (values['roiBL x'], roi_trap_bottomY),  # BL
                         (values['roiBR x'], roi_trap_bottomY),  # BR
                         (values['roiTR x'], 0)]])  # TR

   roi_trap[0][1][1] = cropBotY
   roi_trap[0][2][1] = cropBotY
   roi_trap[0][0][1] = cropTopY
   roi_trap[0][3][1] = cropTopY
   cv2.polylines(frame, [roi_trap], True, (0, 0, 255))

def drawPerspectiveTrap(frame, values):
   cropBotY = values['crop BotY']
   cropTopY = values['crop TopY']

   top_L, top_R = (values['warperTL x'], 0), (values['warperTR x'], 0)
   bot_L, bot_R = (values['warperBL x'], cropBotY), (values['warperBR x'], cropBotY)
   # Adjust trapezoid values for visualization
   pts = np.array([top_L, bot_L, bot_R, top_R])
   pts[0][1] = cropTopY
   pts[3][1] = cropTopY
   cv2.polylines(frame, [pts], True, (0, 255, 0))




