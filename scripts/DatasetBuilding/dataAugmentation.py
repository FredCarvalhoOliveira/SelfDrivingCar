import cv2
import matplotlib.pyplot as plt
import numpy as np
import random

from datasetParser import DatasetParser
from datasetBuilder import DatasetBuilder


class DataAugmentation:
    def __init__(self):
        pass

    def generateLightVariations(self, img, numVariations):
        height, width = img.shape
        variations = np.empty((numVariations, height, width))

        for i in range(numVariations):
            variations[i] = self.transformLightLevel(img)

        variations = variations.astype(img.dtype)
        return variations

    def generateShadowVariations(self, img, numVariations):
        height, width = img.shape
        variations = np.empty((numVariations, height, width))

        for i in range(numVariations):
            variations[i] = self.transformShadows(img)

        variations = variations.astype(img.dtype)
        return variations

    def transformLightLevel(self, img):
        lightOffset = random.randint(-200, 200)
        return cv2.subtract(img, lightOffset)

    def transformShadows(self, img):
        shadows = np.ones(img.shape)
        shadows *= 255

        center_coordinates = (random.randint(0, img.shape[1]), random.randint(0, img.shape[0]))
        axesLength = (random.randint(0, int(img.shape[0]/4)), random.randint(0, int(img.shape[0]/4)))

        angle = random.randint(0, 360)


        startAngle = 0
        endAngle   = 360

        shadows = cv2.ellipse(shadows, center_coordinates, axesLength, angle, startAngle, endAngle, random.randint(0, 511), -1)
        shadows /= 255

        result = img * shadows
        # result = cv2.multiply(img, shadows)

        return result

def augmentDataset(datasetPath, numVariations):
    db = DatasetBuilder("generated.txt", 50)
    augmenter = DataAugmentation()

    parser = DatasetParser(datasetPath)
    inputs, desiredOutputs = parser.loadDataset()
    print(">>> Loading dataset...")
    print(">>> Dataset loaded with " + str(len(inputs)) + " frames")
    print(">>> Augmenting with " + str(numVariations) + " frame variations")

    for i in range(len(inputs)):
        frame = inputs[i]
        cmds  = desiredOutputs[i]

        db.addDataLine(frame, cmds)

        lightVariations  = augmenter.generateLightVariations(frame, numVariations)
        for j in range(len(lightVariations)):
            db.addDataLine(lightVariations[j], cmds)

        shadowVariations = augmenter.generateShadowVariations(frame, numVariations)
        for j in range(len(shadowVariations)):
            db.addDataLine(shadowVariations[j], cmds)

        if i % 100 == 0 and i != 0:
            print("Processed " + str(i) + " frames")
    db.finish()

    print(">>> Augmented data has " + str(len(inputs) + 2 * (len(inputs) * numVariations)) + " entries")







if __name__ == "__main__":
    augmentDataset("../../res/datasets/session1.txt", 20)


    # augment = DataAugmentation()
    # img = cv2.imread('../../res/imgs/roadImg.PNG', 0)
    # # plt.imshow(augment.transformShadows(img), cmap='gray')
    # # plt.show()
    #
    #
    # variations = augment.generateLightVariations(img, 25)
    # variations = augment.generateShadowVariations(img, 25)
    #
    # plt.figure("Data Augmentation", figsize=(15, 7))
    # for i in range(25):
    #     plt.subplot(5, 5, i+1)
    #     plt.imshow(variations[i], cmap='gray')
    #     plt.axis('off')
    #
    # plt.tight_layout()
    # plt.show()
