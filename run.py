import cv2, mediapipe as mp, pyautogui, time
pyautogui.FAILSAFE = False
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
sw, sh = pyautogui.size()
cap = cv2.VideoCapture(0)
prev_x, prev_y, last_click = 0, 0, 0
print("Started! Show your hand. Press Q to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot open webcam!")
        break
    frame = cv2.flip(frame, 1)
    res = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    label = "No hand"
    if res.multi_hand_landmarks:
        for lm in res.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
            tips = [lm.landmark[i].y < lm.landmark[i-2].y for i in [8,12,16,20]]
            total = sum(tips)
            ix = int(lm.landmark[8].x * sw)
            iy = int(lm.landmark[8].y * sh)
            prev_x = prev_x + (ix - prev_x) / 5
            prev_y = prev_y + (iy - prev_y) / 5
            now = time.time()
            if total == 1:
                pyautogui.moveTo(prev_x, prev_y)
                label = "MOVE"
            elif total == 2 and now - last_click > 0.8:
                pyautogui.click()
                last_click = now
                label = "CLICK"
            elif total == 0 and now - last_click > 0.8:
                pyautogui.rightClick()
                last_click = now
                label = "RIGHT CLICK"
    cv2.putText(frame, label, (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.imshow("Hand Gesture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
