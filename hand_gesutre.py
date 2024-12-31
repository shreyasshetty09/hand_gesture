import cv2
import mediapipe as mp
import RPi.GPIO as GPIO
import time

# Setup GPIO
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
photo_count = 0  # Counter for saved photos

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    gesture = "No Gesture"
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Extract coordinates
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            middle_tip = hand_landmarks.landmark[12]
            wrist = hand_landmarks.landmark[0]
            
            # Thumbs up detection
            if thumb_tip.y < wrist.y and index_tip.y > wrist.y:
                gesture = "Thumbs Up"
                GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED
            else:
                GPIO.output(LED_PIN, GPIO.LOW)  # Turn off LED
            
            # Scissors detection
            if index_tip.y < wrist.y and middle_tip.y < wrist.y and thumb_tip.y > wrist.y:
                gesture = "Scissors"
                # Capture photo
                photo_name = f"photo_{photo_count}.jpg"
                cv2.imwrite(photo_name, frame)
                print(f"Photo captured: {photo_name}")
                photo_count += 1
    
    # Display gesture on frame
    cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Hand Gesture Recognition", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
