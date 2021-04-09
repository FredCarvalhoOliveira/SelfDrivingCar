import numpy as np
import os


class DatasetParser:
   def __init__(self, fileName):
      self.filepath = "../../res/datasets/" + fileName
      self.inShape    = None
      self.outShape   = None
      self.inVarType  = None
      self.outVarType = None

   def __parseMetadata(self, metadataStr):
      metadata = metadataStr.split('|')

      inShape = metadata[0].split(';')
      for i in range(len(inShape)):
         inShape[i] = int(inShape[i])
      self.inShape = tuple(inShape) if len(inShape) > 1 else inShape[0]

      outShape = metadata[1].split(';')
      for i in range(len(outShape)):
         outShape[i] = int(outShape[i])
      self.outShape = tuple(outShape) if len(outShape) > 1 else outShape[0]

      self.inVarType  = metadata[2]
      self.outVarType = metadata[3]

   def __parseDataLine(self, line):
      inputs, outputs = line.split("|")
      inputs  = inputs.split(";")
      outputs = outputs.split(";")

      inputs  = np.array(inputs).astype(self.inVarType).reshape(self.inShape)
      outputs = np.array(outputs).astype(self.outVarType).reshape(self.outShape)

      return inputs, outputs

   def loadDataset(self):
      dataFile = open(self.filepath, 'r')
      lines    = dataFile.readlines()

      inputs  = [None for l in range(len(lines) - 1)] # -1 because first line is metadata
      outputs = [None for l in range(len(lines) - 1)] # -1 because first line is metadata

      for lineIdx in range(len(lines)):
         line = lines[lineIdx].rstrip()

         if lineIdx == 0:
            self.__parseMetadata(line)
         else:
            parsedIn, parsedOut = self.__parseDataLine(line)

            inputs[lineIdx-1]  = parsedIn
            outputs[lineIdx-1] = parsedOut

      return inputs, outputs



   # def loadDataset(self):
   #    inputs  = None
   #    outputs = None
   #
   #    with open(self.filepath) as f:
   #       for _, line in enumerate(f):
   #          data       = line.rstrip().split('|')
   #          rawInputs  = data[0].split(';')
   #          rawOutputs = data[1].split(';')
   #
   #          if inputs is None or outputs is None:
   #             inputs = np.array(rawInputs)
   #             outputs = np.array(rawOutputs)
   #          else:
   #             inputs  = np.vstack((inputs, np.array(rawInputs)))
   #             outputs = np.vstack((outputs, np.array(rawOutputs)))
   #    return inputs.astype(np.float), outputs.astype(np.float)


if __name__ == '__main__':
   parser = DatasetParser("04-07-2021__15-28-27_teste.txt")
   parser.loadDataset()
