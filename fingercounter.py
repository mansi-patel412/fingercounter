import cv2
import mediapipe as mp

# Create hand detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Start the camera
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip for mirror view

    # Convert to RGB (for Mediapipe)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    finger_count = 0

    # If hand detected
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            # Get all landmark positions
            h, w, c = img.shape
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                lmList.append((int(lm.x * w), int(lm.y * h)))

            # Finger tip landmark IDs
            tipIds = [4, 8, 12, 16, 20]

            # Count fingers
            if lmList[tipIds[0]][0] > lmList[tipIds[0] - 1][0]:  # Thumb
                finger_count += 1
            for id in range(1, 5):
                if lmList[tipIds[id]][1] < lmList[tipIds[id] - 2][1]:
                    finger_count += 1

    # Show count on screen
    cv2.putText(img, f"Fingers: {finger_count}", (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    # Show camera window
    cv2.imshow("Finger Counter", img)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
