import sys
sys.path.append("..")
import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from DatasetBuilding.drivingDataset import DrivingDataset
from torch.utils.data import DataLoader
from modelCNN import CNN, CNN_MEDIUM, CNN_LARGE
import torch.nn as nn


def plotModels(models, inputs, targets):
    plt.figure("Model evaluation", figsize=(15, 7))
    plotIdx = 1
    for i, model in enumerate(models):
        # Predict
        preds = model(inputs)
        acceleration_targets = targets.numpy()[:, 0]
        acceleration_preds   = preds.detach().numpy()[:, 0]
        steering_targets     = targets.numpy()[:, 1]
        steering_preds       = preds.detach().numpy()[:, 1]

        # Calculate loss
        criterion = nn.MSELoss()
        loss = criterion(preds, targets)
        print(f"{model.name} - loss: {loss.item()}")

        # Plot acceleration regression
        plt.subplot(len(models), 2, plotIdx)
        plt.plot(acceleration_targets, 'g')
        plt.plot(acceleration_preds, 'b')
        plt.title(f"Acceleration Regression {model.name}")
        plt.ylim([-1, 1])
        plt.ylabel("Acceleration")
        plt.xlabel("Timestep")
        plt.grid()
        targets_patch = mpatches.Patch(color='green', label='Target')
        preds_patch   = mpatches.Patch(color='blue', label='Prediction')
        plt.legend(handles=[targets_patch, preds_patch])
        plotIdx += 1

        # Plot steering regression
        plt.subplot(len(models), 2, plotIdx)
        plt.plot(steering_targets, 'g')
        plt.plot(steering_preds, 'b')
        plt.title(f"Steering Regression {model.name}")
        plt.ylim([-1, 1])
        plt.ylabel("Steering")
        plt.xlabel("Timestep")
        plt.grid()
        targets_patch = mpatches.Patch(color='green', label='Target')
        preds_patch = mpatches.Patch(color='blue', label='Prediction')
        plt.legend(handles=[targets_patch, preds_patch])
        plotIdx += 1
    plt.tight_layout()
    plt.show()




# Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load Models
cnnLite = CNN()
cnnLite.load_state_dict(torch.load("../../res/models/Lite_epochs_100"))
cnnLite.eval()

cnnMedium = CNN_MEDIUM()
cnnMedium.load_state_dict(torch.load("../../res/models/Medium_epochs_100"))
cnnMedium.eval()

cnnLarge = CNN_LARGE()
cnnLarge.load_state_dict(torch.load("../../res/models/Large_epochs_100"))
cnnLarge.eval()





# Load Data
dataset = DrivingDataset("../../res/datasets/fullCropped.txt", isTrainSet=False, minAcceleration=0.20)
dataloader = DataLoader(dataset, batch_size=100, shuffle=True)
inputs, targets = next(iter(dataloader))


models = [cnnLite, cnnMedium, cnnLarge]
plotModels(models, inputs, targets)



# # Predict
# preds = model(inputs)
# acceleration_targets = targets.numpy()[:,0]
# acceleration_preds   = preds.detach().numpy()[:,0]
# steering_targets = targets.numpy()[:,1]
# steering_preds   = preds.detach().numpy()[:,1]
#
# # Calculate loss
# criterion = nn.MSELoss()
# loss = criterion(preds, targets)
# print(loss.item())
#
#
#
# # Plot
# plt.figure("Model evaluation", figsize=(15, 7))
# plt.subplot(1, 2, 1)
# plt.plot(acceleration_targets, 'g')
# plt.plot(acceleration_preds, 'b')
# plt.title("Acceleration Regression")
# plt.ylim([-1, 1])
# plt.ylabel("Acceleration")
# plt.xlabel("Timestep")
# plt.grid()
# targets_patch = mpatches.Patch(color='green', label='Target')
# preds_patch   = mpatches.Patch(color='blue',  label='Prediction')
# plt.legend(handles=[targets_patch, preds_patch])
#
# plt.subplot(1, 2, 2)
# plt.plot(steering_targets, 'g')
# plt.plot(steering_preds, 'b')
# plt.title("Steering Regression")
# plt.ylim([-1, 1])
# plt.ylabel("Steering")
# plt.xlabel("Timestep")
# plt.grid()
# targets_patch = mpatches.Patch(color='green', label='Target')
# preds_patch   = mpatches.Patch(color='blue',  label='Prediction')
# plt.legend(handles=[targets_patch, preds_patch])
#
# plt.tight_layout()
# plt.show()