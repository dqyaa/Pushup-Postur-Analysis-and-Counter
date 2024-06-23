import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Initialize push-up counter
pushup_count = 0
previous_good_pushup = False

# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360.0 - angle
        
    return angle

# Function to analyze the push-up based on pose landmarks
def analyze_pushup(pose_landmarks):
    global pushup_count, previous_good_pushup
    
    landmarks = pose_landmarks.landmark
    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
             landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

    # Calculate angles
    elbow_angle = calculate_angle(shoulder, elbow, wrist)
    hip_angle = calculate_angle(shoulder, hip, knee)

    feedback = ""
    if elbow_angle > 160:
        feedback += "Elbows too extended. "
    elif elbow_angle < 70:
        feedback += "Elbows not bent enough. "
    
    if abs(shoulder[1] - hip[1]) > 0.1:  # Adjust threshold as needed
        feedback += "Back not straight. "
    
    if feedback == "":
        if not previous_good_pushup:  # To count only once per push-up
            pushup_count += 1
            previous_good_pushup = True
        return "Good Pushup", True
    else:
        previous_good_pushup = False
        return feedback, False

# Load video
cap = cv2.VideoCapture('pushup.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        feedback, is_good_pushup = analyze_pushup(results.pose_landmarks)
        cv2.putText(frame, feedback, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        
        # Display push-up count
        cv2.putText(frame, f"Total Pushups: {pushup_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    
    cv2.imshow('Pushup Analysis', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

