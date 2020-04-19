import numpy as np
import os


class DatasetParser:
   def __init__(self, fileName):
      self.filepath = "../../res/datasets/" + fileName

   def loadDataset(self):
      inputs  = None
      outputs = None

      with open(self.filepath) as f:
         for _, line in enumerate(f):
            data       = line.rstrip().split('|')
            rawInputs  = data[0].split(';')
            rawOutputs = data[1].split(';')

            if inputs is None or outputs is None:
               inputs = np.array(rawInputs)
               outputs = np.array(rawOutputs)
            else:
               inputs  = np.vstack((inputs, np.array(rawInputs)))
               outputs = np.vstack((outputs, np.array(rawOutputs)))
      return inputs.astype(np.float), outputs.astype(np.float)
