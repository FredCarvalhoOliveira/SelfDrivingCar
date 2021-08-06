import cv2
import matplotlib.pyplot as plt
import numpy as np
import random

from datasetParser import DatasetParser


class DataAugmentation:
    def __init__(self):
        pass

    def changeGlobalLightLevel(self, img, numVariations):
        height, width = img.shape

        variations = np.empty((numVariations, height, width))

        for i in range(numVariations):
            lightOffset = random.randint(0, 200)
            variations[i] = cv2.subtract(img, np.random.randint(lightOffset))

        return variations

if __name__ == "__main__":
    # parser = DatasetParser("../../res/datasets/08-03-2021__22-29-34_carTest.txt")
    # inputs, desiredOutputs = parser.loadDataset()

    augment = DataAugmentation()


    img = cv2.imread('../../res/imgs/roadImg.PNG', 0)

    variations = augment.changeGlobalLightLevel(img, 25)


    plt.figure("Data Augmentation", figsize=(15, 7))


    for i in range(25):
        plt.subplot(5, 5, i+1)
        plt.imshow(variations[i], cmap='gray')
        plt.axis('off')

    plt.tight_layout()
    plt.show()
