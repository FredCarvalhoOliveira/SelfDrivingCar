import sys
sys.path.append("..")
import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt
from DatasetBuilding.datasetParser import DatasetParser
from modelCNN import CNN

cnn = CNN()
torch.no_grad()
cnn.eval()



parser = DatasetParser("05-14-2021__15-05-20_carTest.txt")
inputs, outputs = parser.loadDataset()
inputs, outputs = parser.cleanDataset(inputs, outputs, 0.20)
steering = outputs[:, 1]

# inputs = inputs/255
# imgs = torch.from_numpy(inputs)
# imgs = imgs.view(inputs.shape[0], 1, inputs.shape[1], inputs.shape[2]).float()





for i in [0, 10, 50, 100, 150, 300]:
   img = torch.from_numpy(inputs[i] / 255)
   img = img.view(1, 1, img.shape[0], img.shape[1]).float()
   print(cnn(img))


#    # print(preds[0])
#    print(cnn(img))
#    # plt.imshow(imgs[i][0].numpy())
#    plt.imshow(inputs[i])
#    plt.show()

# for i in range(50):
#    img = torch.rand(75, 100)
   # plt.imshow(img.numpy())
   # plt.show()

   # img = img.view(1, 1, img.shape[0], img.shape[1])
   # print(cnn(img))

# plt.plot(steering)
# plt.show()