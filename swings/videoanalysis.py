import cv2
import time
from os.path import exists
from celery_progress.backend import ProgressRecorder

def analyze(self, path):
    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    progress_recorder = ProgressRecorder(self)
    cap = cv2.VideoCapture(path)
    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    tot_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
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
            progress_recorder.set_progress(frames, tot_frames, description="Loading")
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