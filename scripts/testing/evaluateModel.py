import sys
sys.path.append("..")
import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from DatasetBuilding.drivingDataset import DrivingDataset
from torch.utils.data import DataLoader
from modelCNN import CNN


# Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load Model
model = CNN()
model.load_state_dict(torch.load("../../res/models/FINAL_CNN_epochs_500_2.0"))
model.eval()

# Load Data
dataset = DrivingDataset("../../res/datasets/full.txt", isTrainSet=False, minAcceleration=0.20)
dataloader = DataLoader(dataset, batch_size=100, shuffle=True)
inputs, targets = next(iter(dataloader))

# Predict
preds = model(inputs)
acceleration_targets = targets.numpy()[:,0]
acceleration_preds   = preds.detach().numpy()[:,0]
steering_targets = targets.numpy()[:,1]
steering_preds   = preds.detach().numpy()[:,1]

# Plot
plt.figure("Model evaluation", figsize=(15, 7))
plt.subplot(2, 1, 1)
plt.plot(acceleration_targets, 'g')
plt.plot(acceleration_preds, 'b')
plt.title("Acceleration Regression")
plt.ylim([-1, 1])
plt.ylabel("Acceleration")
plt.xlabel("Timestep")
plt.grid()
targets_patch = mpatches.Patch(color='green', label='Target')
preds_patch   = mpatches.Patch(color='blue',  label='Prediction')
plt.legend(handles=[targets_patch, preds_patch])

plt.subplot(2, 1, 2)
plt.plot(steering_targets, 'g')
plt.plot(steering_preds, 'b')
plt.title("Steering Regression")
plt.ylim([-1, 1])
plt.ylabel("Steering")
plt.xlabel("Timestep")
plt.grid()
targets_patch = mpatches.Patch(color='green', label='Target')
preds_patch   = mpatches.Patch(color='blue',  label='Prediction')
plt.legend(handles=[targets_patch, preds_patch])

plt.tight_layout()
plt.show()