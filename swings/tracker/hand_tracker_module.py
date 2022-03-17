import mediapipe as mp
import cv2
from mediapipe.framework.formats import landmark_pb2

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

def track(frame, drawImage = False):
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        print(1)
        frame.flags.writeable = False
        print(15)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        print(16)
        results = pose.process(frame) #errrrrrror
        print(7)
        # Draw the pose annotation on the image.
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        print(3)
        keypoints = landmark_pb2.NormalizedLandmarkList(
            landmark = [
                results.pose_landmarks.landmark[19],
                results.pose_landmarks.landmark[20], 
            ]
        )

        if drawImage:
            mp_drawing.draw_landmarks(
                frame,
                keypoints)
            frame = cv2.resize(frame, (540, 960))
            cv2.imshow('wrists', frame)
        return keypoints