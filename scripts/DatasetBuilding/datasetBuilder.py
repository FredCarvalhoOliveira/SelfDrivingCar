import numpy as np

##############################################################
#           This class is a dataset building tool            #
#                                                            #
#  DATASET FORMAT                                            #
#  - CSV file                                                #
#  - curv, centerX, coef[0], coef[1], coef[2], hCtrl, vCtrl  #
#    |--------------- INPUTS ---------------| |- OUTPUTS -|  #
#                                                            #
##############################################################

class DatasetBuilder:
   def __init__(self):
      self.dataset = None

   def addDataLine(self, inputsArray, outputsArray):
      line = np.hstack((inputsArray, outputsArray))
      if self.dataset is None:
         self.dataset = line
      else:
         self.dataset = np.vstack((self.dataset, line))

   def generateDataset(self):
      print(self.dataset)


db = DatasetBuilder()
db.addDataLine(["teste", "2", "3"], ["asd", "dads"])
db.addDataLine(["teste", "2", "3"], ["asd", "dads"])
db.addDataLine(["teste", "2", "3"], ["asd", "dads"])
db.generateDataset()




