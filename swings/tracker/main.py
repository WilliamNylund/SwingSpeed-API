import time
import math
from . import hand_tracker_module as ht
from . import line_tracker_module as lt
from . import background_subtractor as bs
from . import region_tracker_module as rt
import cv2

def analyze(path):
    # Timing 
    print("starting analysis")
    print(path)
    start = time.time()

    # Relative url to input video
    cap = cv2.VideoCapture(path)

    # Getting first frame of video for various uses
    _, firstFrame = cap.read()

    # inits
    key = ''
    lineList = []
    frameCount = 0

    #roi stuff
    w= int(cap.get(3))
    h= int(cap.get(4)/2)
    x= 0
    y= 1200
    track_window= (x,y,h,w)

    term_critera = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,100,3)

    formatted_lines = []
    max_wrist_dist = 30
    velocity = 0,0
    fucky_pos = False
    print("yes")
    while(1):
        # read frames
        print("1")
        ret, frame = cap.read()
        if frame is None:
            break
        print("2")
        frameCount += 1
        lines_in_frame = []
        wrists_in_frame = []
        club_end = None
        previous_velocity = velocity
        previous_track_window = track_window
        print("3")
        frame = cv2.resize(frame, (540, 960))  
        print("35")
        wristCords = ht.track(frame) #error ehre
        print("4")
        morphFrame = bs.removeBG(frame)
        track_window = rt.track(track_window, morphFrame)
        lineCords = lt.trackLines(morphFrame)
        print("Frame: ", frameCount)
        if lineCords is not None:
            for line in lineCords:
                line = line[0]
                lines_in_frame.append(line)

        #TODO: Denormalizing wrist values should definitely not be hardcoded
        for landmark in wristCords.landmark:
            x1 = round(landmark.x * 540)
            y1 = round(landmark.y * 960)
            wrist = x1, y1
            wrists_in_frame.append(wrist)

        #TODO: Filter out lines intersecting body
        longest_possible_club = 0
        for frame_line in lines_in_frame:
            xf1 = frame_line[0]
            yf1 = frame_line[1]
            xf2 = frame_line[2]
            yf2 = frame_line[3]
            length = math.sqrt(abs(xf1-xf2) ** 2 + abs(yf1-yf2) ** 2)

            for wrist in wrists_in_frame:
                x1dist = abs(xf1 - wrist[0])
                y1dist = abs(yf1 - wrist[1])
                x2dist = abs(xf2 - wrist[0])
                y2dist = abs(yf2 - wrist[1])

                if ((x1dist < max_wrist_dist) and (y1dist < max_wrist_dist) and (length > longest_possible_club)):
                    formatted_lines.append(frame_line)
                    longest_possible_club = length
                    club_end = xf2,yf2
                    cv2.line(frame,(xf1,yf1),(xf2,yf2),(255,0,0),2)
                elif ((x2dist < max_wrist_dist) and (y2dist < max_wrist_dist) and (length > longest_possible_club)):
                    formatted_lines.append(frame_line)
                    longest_possible_club = length
                    club_end = xf1,yf1
                    cv2.line(frame,(xf1,yf1),(xf2,yf2),(255,0,0),2)


        
        club_x, club_y, _, _ = track_window
        prev_club_x, prev_club_y, _, _ = previous_track_window

        #TODO: Add predictive position fixing(momentum)
        if (previous_track_window == track_window):
            print("lost club, attempting to fix")
            if club_end is not None:
                track_window = club_end + track_window[2:]

        # 'o' to pause then:
            # 'q' to close
            # 'p' to move one frame ahead
            # any other key to unpause

        frame = cv2.circle(frame, (club_end), radius=5, color=(0, 255, 0), thickness=-1)
        frame = cv2.circle(frame, (track_window[0]+15,track_window[1]+15), radius=5, color=(0, 0, 255), thickness=-1)
        cv2.imshow('filtered lines', frame)

        print('club position: ',track_window[0],track_window[1])
        print('club end:', club_end)

        if (cv2.waitKey(30) & 0xff == ord('o')) or key == ord('p'):
            key = cv2.waitKey(0) & 0xff
            if key == ord('q'):
                break
            else:
                None

    end = time.time()
    print('Run time: ' + str(end - start))
    print(frameCount)
    cap.release()
