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
        shadows  = np.ones(img.shape)
        shadows *= 255

        centerCoords = (random.randint(0, img.shape[1]), random.randint(0, img.shape[0]))
        axesLength   = (random.randint(0, int(img.shape[0]/4)), random.randint(0, int(img.shape[0]/4)))

        angle        = random.randint(0, 360)
        startAngle   = 0
        endAngle     = 360

        shadows  = cv2.ellipse(shadows, centerCoords, axesLength, angle, startAngle, endAngle, random.randint(0, 511), -1)
        shadows /= 255

        result = img * shadows
        # result = cv2.multiply(img, shadows)
        return result

    def transformCrop(self, img, cropY):
        return img[cropY:]

    def mirrorData(self, img, cmds):
        mirrored = np.flip(img, 1)  # Mirror image
        cmds[0] *= -1  # Flip steering
        return mirrored, cmds




def augmentDataset(datasetPath, numVariations):
    db = DatasetBuilder("generated.txt", 50)
    augmenter = DataAugmentation()

    print(">>> Loading dataset...")
    parser = DatasetParser(datasetPath)
    inputs, desiredOutputs = parser.loadDataset()
    print(">>> Dataset loaded with " + str(len(inputs)) + " frames")
    print(">>> Augmenting with " + str(numVariations) + " frame variations")

    for i in range(len(inputs)):
        frame = inputs[i]
        cmds  = desiredOutputs[i]


        # Crop dataset
        db.addDataLine(augmenter.transformCrop(frame, 40), cmds)

        # db.addDataLine(frame, cmds)

        # lightVariations  = augmenter.generateLightVariations(frame, numVariations)
        # for j in range(len(lightVariations)):
        #     db.addDataLine(lightVariations[j], cmds)
        #
        # shadowVariations = augmenter.generateShadowVariations(frame, numVariations)
        # for j in range(len(shadowVariations)):
        #     db.addDataLine(shadowVariations[j], cmds)

        if i % 100 == 0 and i != 0:
            print("Processed " + str(i) + " frames")
    db.finish()

    # print(">>> Augmented data has " + str(len(inputs) + 2 * (len(inputs) * numVariations)) + " entries")







if __name__ == "__main__":
    # augmentDataset("../../res/datasets/full.txt", numVariations=1)


    augment = DataAugmentation()
    img = cv2.imread('../../res/imgs/roadImg.PNG', 0)
    # plt.imshow(img, cmap='gray')
    # plt.show()
    # plt.imshow(np.flip(img, 1), cmap='gray')
    # plt.show()
    #
    #
    # variations = augment.generateLightVariations(img, 25)
    # variations = augment.generateShadowVariations(img, 25)

    controls = [0.83, 0.61]

    variations = augment.mirrorData(img, [0, 0])
    #

    plt.figure("Data Augmentation", figsize=(15, 7))
    plt.subplot(1, 2, 1)
    plt.title("Aceleração = " + str(controls[0]) + "  Direção = " + str(controls[1]), fontsize=20)

    plt.imshow(img, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title("Aceleração = " + str(controls[0]) + "  Direção = " + str(controls[1] * -1), fontsize=20)
    plt.imshow(variations[0], cmap='gray')
    plt.axis('off')

    # plt.figure("Data Augmentation", figsize=(15, 7))
    # for i in range(25):
    #     plt.subplot(5, 5, i+1)
    #     plt.imshow(variations[i], cmap='gray')
    #     plt.axis('off')

    plt.tight_layout()
    plt.show()