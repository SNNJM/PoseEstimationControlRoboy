import cv2
import mediapipe as mp
import serial
import time

# Initialize serial communication with EduBit
ser = serial.Serial('COM6', 115200, timeout=1)  # Change COM port if needed
time.sleep(2)

# Setup MediaPipe Pose Estimation
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert frame to RGB for Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Get Y-coordinates for head, right wrist, and waist
        head_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y
        head_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x
        wrist_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y
        waist_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y  # Approximate waist

        # Get X-coordinates for shoulders and right wrist
        right_wrist_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y
        left_wrist_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y
        right_wrist_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x
        left_wrist_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x
        left_shoulder_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x
        right_shoulder_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x

        command = "STOP"  # Default command is STOP

        # Move forward if hand is above head
        #if wrist_y < head_y:
        if right_wrist_y < head_y and left_wrist_y < head_y:
            command = "FORWARD"

        # Move backward if hand is below waist
        #elif wrist_y > waist_y:
        elif right_wrist_x > head_x and left_wrist_x < head_x:
            command = "REVERSE"
        
        elif right_wrist_y > head_y and left_wrist_y > head_y:
            command = "STOP"

        # Turn Left if hand is extended far to the left
        elif right_wrist_y > head_y  and left_wrist_y < head_y :  # Adjust threshold as needed
            command = "LEFT"

        # Turn Right if hand is extended far to the right
        elif right_wrist_y < head_y  and left_wrist_y > head_y:  # Adjust threshold as needed
            command = "RIGHT"

        # Send command to EduBit
        ser.write(f"{command}\n".encode())
        time.sleep(0.02)

        # Display command on screen
        cv2.putText(frame, f"Command: {command}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Show webcam feed
    cv2.imshow('Pose Estimation', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
ser.close()
