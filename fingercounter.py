import cv2
import mediapipe as mp

# Create hand detector (tuned confidences for better accuracy)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
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
        # multi_hand_landmarks and multi_handedness are aligned, so use index to get handedness
        for hand_index, handLms in enumerate(result.multi_hand_landmarks):
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            # Get all landmark positions
            h, w, c = img.shape
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                lmList.append((int(lm.x * w), int(lm.y * h)))

            # Make sure we have landmarks
            if len(lmList) == 0:
                continue

            # Determine handedness (Left/Right)
            hand_label = "Unknown"
            if result.multi_handedness and len(result.multi_handedness) > hand_index:
                hand_label = result.multi_handedness[hand_index].classification[0].label

            # Finger tip landmark IDs
            tipIds = [4, 8, 12, 16, 20]

            # Count fingers for this hand
            fingers = []

            # Thumb: use x-coordinate comparison, depends on hand label
            # For 'Right' hand: thumb is open if tip x > previous joint x
            # For 'Left' hand: thumb is open if tip x < previous joint x
            try:
                if hand_label == "Right":
                    if lmList[tipIds[0]][0] > lmList[tipIds[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                else:
                    if lmList[tipIds[0]][0] < lmList[tipIds[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
            except IndexError:
                # In case of unexpected landmark indexing issues
                fingers.append(0)

            # Fingers (index, middle, ring, little): tip y < pip y means finger is up
            for i in range(1, 5):
                try:
                    if lmList[tipIds[i]][1] < lmList[tipIds[i] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                except IndexError:
                    fingers.append(0)

            # Add this hand's fingers to total count
            finger_count += sum(fingers)

            # (Optional) Show per-hand count near the wrist
            # wrist coord is landmark 0
            wrist_x, wrist_y = lmList[0]
            cv2.putText(img, f"{hand_label}: {sum(fingers)}", (wrist_x - 40, max(wrist_y - 20, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # Show total count on screen
    cv2.putText(img, f"Fingers: {finger_count}", (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    # Show camera window
    cv2.imshow("Finger Counter", img)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
