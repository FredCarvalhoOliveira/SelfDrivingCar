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
      self.fileName    = "../../res/datasets/" + date_time + "_" + fileName
      self.bufferSize  = bufferSize
      self.bufferCount = 0
      self.buffer      = ""

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



   def addDataLine(self, inputsArray, outputsArray):

      if len(inputsArray.shape) > 2:
         print("ERROR: Cant handle array shape in DatasetBuilder addDataLine()")
         return
      elif len(inputsArray.shape) == 2:
         inputsArray = inputsArray.flatten() # flatten 2d array


      # Dump buffer
      if self.bufferCount == self.bufferSize:
         self.__writeToFile()
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

   def __writeToFile(self):
      file = open(self.fileName, "a")
      file.write(self.buffer)
      file.close()

   # Dump the rest of buffer contents
   def finish(self):
      self.__writeToFile()


if __name__ == '__main__':
   db = DatasetBuilder("teste.txt", 2)
   db.addDataLine(np.random.randint(0, 256, 5), np.random.rand(2))
   # db.addDataLine2([1.2, 1.897, 3], [212.421234, 25])

   db.finish()




