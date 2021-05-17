import sys
sys.path.append("..")

import torch
from torch.utils.data import Dataset
from DatasetBuilding.datasetParser import DatasetParser

class DrivingDataset(Dataset):
   def __init__(self, filename, isTrainSet=True, minAcceleration=0.20):
      self.inputs = None
      self.targets = None
      self.__parseDataset(filename, isTrainSet, minAcceleration)

   def __len__(self):
      return len(self.inputs)

   def __getitem__(self, idx):
      inputs = self.inputs[idx]
      inputs = torch.from_numpy(inputs).view(1, inputs.shape[0], inputs.shape[1]).float()

      targets = self.targets[idx]
      targets = torch.from_numpy(targets).float()

      return inputs, targets

   def __parseDataset(self, filename, isTrainSet, minAcceleration):
      print(">>> Parsing datafile " + filename.split("/")[-1])
      print(">>> Loading dataset...")
      parser = DatasetParser(filename)
      inputs, targets = parser.loadDataset(minAcceleration)

      trainTestRatio = 0.7
      if isTrainSet:
         self.inputs = inputs[:int(len(inputs) * trainTestRatio)]
         self.targets = targets[:int(len(targets) * trainTestRatio)]
      else:
         self.inputs = inputs[int(len(inputs) * trainTestRatio):]
         self.targets = targets[int(len(targets) * trainTestRatio):]
      print(">>> " + ("Trainset" if isTrainSet else "Testset") + " loaded successfully with " + str(len(self.inputs)) + " entries")


if __name__ == '__main__':
    dataset = DrivingDataset("../../res/datasets/05-14-2021__15-05-20_carTest.txt", isTrainSet=True, minAcceleration=0.20)
    print(">>> Example sample (first):")
    print(dataset[0])