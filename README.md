# SelfDrivingCar

This project is an implementation of a self driving car.

### The Car
The car is built on a frame from a toy RC car, I removed all the controller circuits and left only the DC-Motor that powers the wheels, originally the stearing was built using a DC-Motor which meant that there were only three stearing states possible: fully right, fully left or centered. So I removed the old DC-Motor that controlled the stearing and replaced it with a servo motor that enables gradual stearing.

### Preparing Video Frame for Analysis
- resize frame
- crop horizon in order to keep only the road in the image
- convert image to grayscale, apply segmentation algorithm and morphological operators
- apply ROI(region of interest) mask
- apply perspective transformation to create a bird's eye view of the road

### Lane Detection & Feature Extraction
- find points in lane lines
- estimate lane lines
- extract features from estimated lane lines

### Building the Dataset

### Training the NeuralNet

### Autonomous Driving
