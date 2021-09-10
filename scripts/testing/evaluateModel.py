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
    inputs    = inputs.to(device=device)
    targets   = targets.to(device=device)

    plt.figure("Model evaluation", figsize=(15, 7))
    plotIdx = 1
    for i, model in enumerate(models):
        # Predict
        preds = model(inputs)
        acceleration_targets = targets.cpu().numpy()[:, 0]
        acceleration_preds   = preds.cpu().detach().numpy()[:, 0]
        steering_targets     = targets.cpu().numpy()[:, 1]
        steering_preds       = preds.cpu().detach().numpy()[:, 1]

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

def getModelLoss(dataset, model):
    dataloader = DataLoader(dataset, batch_size=64, shuffle=True)
    meanLoss  = 0
    numBatches = 0
    for batchIdx, (data, targets) in enumerate(dataloader):
        data    = data.to(device=device)
        targets = targets.to(device=device)

        criterion = nn.MSELoss()

        # Feedforward and loss
        preds = model(data)
        batchLoss = criterion(preds, targets).item()

        meanLoss += batchLoss

        numBatches += 1
    return meanLoss / numBatches







# Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load Models
cnnLite = CNN().to(device=device)
# cnnLite.load_state_dict(torch.load("../../res/models/Lite_epochs_100"))
cnnLite.load_state_dict(torch.load("../../res/models/crpLight_Lite_epochs_100"))
cnnLite.eval()

cnnMedium = CNN_MEDIUM().to(device=device)
# cnnMedium.load_state_dict(torch.load("../../res/models/Medium_epochs_100"))
cnnMedium.load_state_dict(torch.load("../../res/models/crpLight_Medium_epochs_100"))
cnnMedium.eval()

cnnLarge = CNN_LARGE().to(device=device)
cnnLarge.load_state_dict(torch.load("../../res/models/Large_epochs_100"))
# cnnLarge.load_state_dict(torch.load("../../res/models/Large_epochs_100"))
cnnLarge.eval()





# Load Data
dataset = DrivingDataset("../../res/datasets/fullCropped_light.txt", isTrainSet=False, minAcceleration=0.20)

# Calculate losses
models = [cnnLite, cnnMedium, cnnLarge]
print(f"Lite   - {getModelLoss(dataset, cnnLite)}")
print(f"Medium - {getModelLoss(dataset, cnnMedium)}")
print(f"Large  - {getModelLoss(dataset, cnnLarge)}")

# Plot model regressions
NUM_SAMPLES = 100
dataloader = DataLoader(dataset, batch_size=NUM_SAMPLES, shuffle=True)
inputs, targets = next(iter(dataloader))
plotModels(models, inputs, targets)