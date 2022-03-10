import numpy as np
import cv2

# Canny edge detection configs (optimisable)
    #OpenCv defaults
minVal = 50
maxVal = 200
sobelKernel = 3
# True = more taxing but also more accurate (currently not used)
L2Gradient = True

# Line detection config

rho = 0.5  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 30  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 80  # minimum number of pixels making up a line
max_line_gap = 17  # maximum gap in pixels between connectable line segments

def trackLines(frame, drawImage = False, drawSteps = False):

    # Edge detection
        #default thresholds
    edgeFrame = cv2.Canny(frame, minVal, maxVal)
    
    # Setup frame to draw lines on
    if drawImage:
        lineFrame = np.copy(frame)
        lineFrame = cv2.cvtColor(lineFrame, cv2.COLOR_GRAY2BGR)

    # Line detection
    lines = cv2.HoughLinesP(edgeFrame, rho, theta, threshold, np.array([]),min_line_length, max_line_gap)
    if drawImage and lines is not None:
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(lineFrame,(x1,y1),(x2,y2),(255,0,0),2)
    
    #5. Line merging

    #6. Discard irrelevant lines

    if drawImage and not drawSteps:
        lineFrame = cv2.resize(lineFrame, (540, 960))
        cv2.imshow('1.og', lineFrame)
    if drawSteps:
        cv2.imshow('4.edges', edgeFrame)
        cv2.imshow('1.og', lineFrame)
    return lines