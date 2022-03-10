import numpy as np
import cv2
    
term_critera = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,100,3)
tracking_width = 30
tracking_height = 30

def track(track_window, frame, drawImage = False):

    x, y, _, _ = track_window
    _, track_window = cv2.meanShift(
        frame,
        (x, y, tracking_width, tracking_height),
        term_critera
        )
    if drawImage:
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        x, y, _, _ = track_window
        cv2.rectangle(frame, (x, y), (x + tracking_width, y + tracking_height), (0, 255, 0), 2)
        cv2.imshow('roi', frame)
    return track_window