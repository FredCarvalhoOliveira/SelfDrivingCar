from datetime import datetime
import numpy as np
##############################################################
#           This class is a dataset building tool            #
#                                                            #
#  DATASET FORMAT                                            #
#  - CSV file                                                #
#  - curv;centerX;coef[0];coef[1];coef[2]|hCtrl;vCtrl        #
#    |--------------- INPUTS -----------| |- OUTPUTS -|      #
#                                                            #
##############################################################

class DatasetBuilder:
   def __init__(self, fileName, bufferSize=1000):
      date_time = datetime.now().strftime("%m-%d-%Y__%H-%M-%S")
      self.fileName      = "../../res/datasets/" + date_time + "_" + fileName
      self.bufferSize    = bufferSize
      self.bufferCount   = 0
      self.buffer        = ""
      self.wroteMetadata = False

   # def addDataLine2(self, inputsArray, outputsArray):
   #    # Dump buffer
   #    if self.bufferCount == self.bufferSize:
   #       self.writeToFile()
   #       self.buffer      = ""
   #       self.bufferCount = 0
   #    line = ""
   #    # MUITO MAIS RAPIDO EXPLORAR ESTA OPCAO
   #    line += str(inputsArray.tostring() + outputsArray.tostring())
   #
   #    self.buffer      += line
   #    self.bufferCount += 1

   def __writeMetadata(self, inShape, outShape, inVarType, outVarType):

      line = ""
      for i in range(len(inShape)):
         line += str(inShape[i])
         line += "|" if i == len(inShape) - 1 else ";"

      for i in range(len(outShape)):
         line += str(outShape[i])
         line += "|" if i == len(outShape) - 1 else ";"

      line += str(inVarType) + "|" + str(outVarType)

      self.__writeToFile(line + "\n")
      self.wroteMetadata = True




   def addDataLine(self, inputsArray, outputsArray):
      if not self.wroteMetadata:
         self.__writeMetadata(inputsArray.shape, outputsArray.shape, inputsArray.dtype, outputsArray.dtype)

      if len(inputsArray.shape) > 2:
         print("ERROR: Cant handle array shape in DatasetBuilder addDataLine()")
         return
      elif len(inputsArray.shape) == 2:
         inputsArray = inputsArray.flatten() # flatten 2d array


      # Dump buffer
      if self.bufferCount == self.bufferSize:
         self.__writeToFile(self.buffer)
         self.buffer      = ""
         self.bufferCount = 0

      line = ""
      for i in range(len(inputsArray)):
         if i == len(inputsArray) - 1:
            line += str(inputsArray[i]) + "|"
         else:
            line += str(inputsArray[i]) + ";"
      for i in range(len(outputsArray)):
         if i == len(outputsArray) - 1:
            line += str(outputsArray[i]) + "\n"
         else:
            line += str(outputsArray[i]) + ";"

      self.buffer      += line
      self.bufferCount += 1

   def __writeToFile(self, text):
      file = open(self.fileName, "a")
      file.write(text)
      file.close()

   # Dump the rest of buffer contents
   def finish(self):
      self.__writeToFile(self.buffer)


if __name__ == '__main__':
   import cv2
   import imutils

   scale = 0.1
   db    = DatasetBuilder("face.txt", 50)

   cam = cv2.VideoCapture(1)

   for i in range(100):
      ret_val, frame = cam.read()
      frame = imutils.resize(frame, int(frame.shape[1] * scale), int(frame.shape[0] * scale))
      # frame = frame[int(frame.shape[0]/2):frame.shape[0]]

      frame   = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      outputs = np.random.rand(2)


      db.addDataLine(frame, outputs)

      cv2.imshow("img", frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
         break  # esc to quit
   db.finish()




