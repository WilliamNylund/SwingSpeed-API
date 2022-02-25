import cv2
import time



def analyze(path):
    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    cap = cv2.VideoCapture(path)

    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")

    frames = 0

    # Read until video is completed
    print('looping through video...')
    start = time.time()
    object_detector = cv2.createBackgroundSubtractorMOG2()
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            # temp frame counter
            frames = frames + 1
            mask = object_detector.apply(frame)
            edges= cv2.Canny(frame,400,603)
        # Break the loop
        else: 
            break

    # When everything done, release the video capture object
    end = time.time()
    print('analysis done in: ' + str(end - start))
    cap.release()
    print(frames)
    # Closes all the frames
    #cv2.destroyAllWindows()
    return frames