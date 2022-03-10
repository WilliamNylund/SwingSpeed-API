import numpy as np
import cv2

fgbg = cv2.createBackgroundSubtractorMOG2(history=30, varThreshold=70)
#fgbg = cv2.bgsegm.createBackgroundSubtractorGSOC()
#fgbg = cv2.createBackgroundSubtractorKNN(history=30, dist2Threshold=2000, detectShadows= False) #Very noise sensitive
#fgbg = cv2.bgsegm.createBackgroundSubtractorCNT(); #Shitty
#fgbg = cv2.bgsegm.createBackgroundSubtractorLSBP()

# morph kernels (optimisable)
#kernel = np.ones((2,2),np.uint8)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(6,6))
#kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))

# Morph operations
morphAlgorithm = cv2.MORPH_CLOSE
#morphAlgorithm = cv2.MORPH_OPEN

def removeBG(frame, drawImage = False, drawSteps = False):
    #1. apply mask for background subtraction
    fgFrame = fgbg.apply(frame)

    #fgFrame = cv2.GaussianBlur(fgFrame,(7,7),0)

    #2. Morphological transform to remove noise
    morphedFrame = cv2.morphologyEx(fgFrame, morphAlgorithm, kernel)
    
        #Alternate custom morph stack
    #morphedFrame = customMorph.morph(fgFrame)
    if drawImage and not drawSteps:
        frame = cv2.resize(morphedFrame, (540, 960))
        cv2.imshow('morphed', morphedFrame)
    if drawSteps:
        cv2.imshow('fg', fgFrame)
        cv2.imshow('morphed', morphedFrame)
    return morphedFrame