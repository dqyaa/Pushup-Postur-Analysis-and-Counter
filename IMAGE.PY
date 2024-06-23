import cv2
import mediapipe as mp
from pushupCounter import analyze_pushup, pushup_count, mp_pose, mp_drawing

# Function to analyze a single image
def analyze_image(image_path):
    # Reset the pushup count to 0
    pushup_count['count'] = 0

    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image from path {image_path}")
        return

    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and detect pose landmarks
    results = mp_pose.Pose().process(image_rgb)

    # Draw pose landmarks and analyze the pushup
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        feedback, is_good_pushup = analyze_pushup(results.pose_landmarks)
        cv2.putText(image, feedback, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        
        # Display push-up count
        cv2.putText(image, f"Total Pushups: {pushup_count['count']}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    # Display the image with annotations
    cv2.imshow('Pushup Analysis', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Specify the path to the input image
image_path = '2.jpeg'
analyze_image(image_path)
