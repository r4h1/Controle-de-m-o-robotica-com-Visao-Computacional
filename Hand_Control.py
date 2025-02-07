import cv2
import mediapipe as mp
import serial
import time

# Initialize Serial (Change "COM3" to your Arduino port, e.g., "/dev/ttyUSB0" for Linux/Mac)
arduino = serial.Serial("COM3", 9600, timeout=1)
time.sleep(2)  # Wait for serial connection

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Start Webcam
cap = cv2.VideoCapture(0)

# Hand Initialization (Wait until hand is fully open)
hand_initialized = False

# Define landmarks for finger tips and their corresponding joints
FINGER_TIPS = [8, 12, 16, 20, 4]  # Index, Middle, Ring, Pinky, Thumb
FINGER_JOINTS = [6, 10, 14, 18, 2]  # Lower joint of each finger

# Track LED states (1 = ON, 0 = OFF)
led_states = [0, 0, 0, 0, 0]

print("Show an open hand to initialize...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Check if hand is fully open (all tips above joints)
            if not hand_initialized:
                all_fingers_stretched = all(
                    hand_landmarks.landmark[FINGER_TIPS[i]].y < hand_landmarks.landmark[FINGER_JOINTS[i]].y
                    for i in range(5)
                )
                if all_fingers_stretched:
                    print("Hand initialized! Now tracking fingers...")
                    hand_initialized = True
                continue  # Wait until hand is initialized

            # Track each finger state
            for i in range(5):
                tip = hand_landmarks.landmark[FINGER_TIPS[i]]
                joint = hand_landmarks.landmark[FINGER_JOINTS[i]]

                # Finger is bent if tip is below joint
                if tip.y > joint.y and led_states[i] == 0:
                    led_states[i] = 1
                    arduino.write(f"ON{i}\n".encode())  # Send ON signal for LED[i]
                    print(f"Finger {i+1} bent → LED {i+1} ON")

                # Finger is stretched if tip is above joint
                elif tip.y < joint.y and led_states[i] == 1:
                    led_states[i] = 0
                    arduino.write(f"OFF{i}\n".encode())  # Send OFF signal for LED[i]
                    print(f"Finger {i+1} stretched → LED {i+1} OFF")

    # Display the camera feed
    cv2.imshow("Hand Pose Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
arduino.close()
