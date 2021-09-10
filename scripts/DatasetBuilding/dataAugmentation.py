import cv2
import matplotlib.pyplot as plt
import numpy as np
import random

from datasetParser import DatasetParser
from datasetBuilder import DatasetBuilder

from scripts.imageProcessing import ImageProcessing
from scripts.utils import loadCalibValues



class DataAugmentation:
    def __init__(self):
        calibValues = loadCalibValues("../../res/calibration_values_new")
        self.__imgProcess  = ImageProcessing()
        self.__imgProcess.setCalibValues(calibValues)

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

    def transformImgToFeatures(self, img):
        # Feature extraction
        croppedImg = self.__imgProcess.cropFrame(img)
        binImg     = self.__imgProcess.segmentFrame(croppedImg)
        roi        = self.__imgProcess.applyRoiMask(binImg)
        warp_img   = self.__imgProcess.applyBirdsEyePerspective(roi)
        curv, centerOffset, coefs = self.__imgProcess.extractLaneFeatures(warp_img)
        features = np.hstack((np.array([curv, centerOffset]), coefs))
        return features




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

        # Save cropped img
        # cropImg = augmenter.transformCrop(frame, 40)
        db.addDataLine(frame, cmds)

        # # Save mirrored img and commands
        mirroredImg, mirroredCmds = augmenter.mirrorData(frame, cmds)
        db.addDataLine(mirroredImg, mirroredCmds)


        # lightVariations  = augmenter.generateLightVariations(cropImg, numVariations)
        # for j in range(len(lightVariations)):
        #     db.addDataLine(lightVariations[j], cmds)

        # lightVariationsMirror = augmenter.generateLightVariations(mirroredImg, numVariations)
        # for j in range(len(lightVariationsMirror)):
        #     db.addDataLine(lightVariationsMirror[j], mirroredCmds)

        # shadowVariations = augmenter.generateShadowVariations(frame, numVariations)
        # for j in range(len(shadowVariations)):
        #     db.addDataLine(shadowVariations[j], cmds)

        if i % 100 == 0 and i != 0:
            print("Processed " + str(i) + " frames")
    db.finish()

    # print(">>> Augmented data has " + str(len(inputs) + 2 * (len(inputs) * numVariations)) + " entries")







if __name__ == "__main__":
    augmentDataset("../../res/datasets/fullCropped_light.txt", numVariations=0)