# main.py

import cv2
import mediapipe as mp
from pushupCounter import analyze_pushup, pushup_count, mp_pose, mp_drawing

# Load video
cap = cv2.VideoCapture('pushup.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_pose.Pose().process(image)
    
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        feedback, is_good_pushup = analyze_pushup(results.pose_landmarks)
        cv2.putText(frame, feedback, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        
        # Display push-up count
        cv2.putText(frame, f"Total Pushups: {pushup_count['count']}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    
    cv2.imshow('Pushup Analysis', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
