import cv2 as cv
import pyautogui as pag
import mediapipe as mp
import time

# Initializing MediaPipe Hand
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Opening the camera and creating a window
video_capture = cv.VideoCapture(0)
cv.namedWindow("VDPAD")

# Delay between actions to avoid rapid firing
action_delay = 0.5
last_action_time = time.time()

# Track key states
key_pressed = {
    "up": False,
    "down": False,
    "left": False,
    "right": False
}

frame_skip = 3  # Process every 3rd frame
frame_count = 0

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % frame_skip != 0:
        continue

    # Flip the frame for correct left-right orientation
    frame_flipped = cv.flip(frame, 1)

    # Resize frame for faster processing
    height, width, _ = frame_flipped.shape
    frame_resized = cv.resize(frame_flipped, (width // 2, height // 2))
    rgb_frame = cv.cvtColor(frame_resized, cv.COLOR_BGR2RGB)

    # Process the frame and detect hands
    result = hands.process(rgb_frame)

    # Get frame dimensions after resizing
    height, width, _ = frame_resized.shape
    roi_height = height // 3
    roi_width = width // 3

    # Define ROIs (regions of interest)
    up_roi = (0, roi_width, 2 * roi_width, roi_height)  # Center-top
    down_roi = (2 * roi_height, roi_width, 2 * roi_width, height)  # Center-bottom
    left_roi = (roi_height, 0, roi_width, 2 * roi_height)  # Center-left
    right_roi = (roi_height, 2 * roi_width, width, 2 * roi_height)  # Center-right

    # Draw ROI rectangles
    cv.rectangle(frame_resized, (up_roi[1], up_roi[0]), (up_roi[2], up_roi[3]), (0, 255, 0), 2)  # Up region
    cv.rectangle(frame_resized, (down_roi[1], down_roi[0]), (down_roi[2], down_roi[3]), (0, 255, 255), 2)  # Down region
    cv.rectangle(frame_resized, (left_roi[1], left_roi[0]), (left_roi[2], left_roi[3]), (255, 0, 0), 2)  # Left region
    cv.rectangle(frame_resized, (right_roi[1], right_roi[0]), (right_roi[2], right_roi[3]), (0, 0, 255), 2)  # Right region

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Extract coordinates for the bottom of the middle finger (landmark 9)
            x, y = int(hand_landmarks.landmark[9].x * width), int(hand_landmarks.landmark[9].y * height)

            # Debug information: Draw a circle at the detected bottom of the middle finger position
            cv.circle(frame_resized, (x, y), 10, (0, 255, 255), -1)

            # Handle key presses
            if up_roi[0] <= y <= up_roi[3] and up_roi[1] <= x <= up_roi[2]:
                if not key_pressed["up"]:
                    print("up")
                    pag.keyDown("up")
                    key_pressed["up"] = True
            else:
                if key_pressed["up"]:
                    pag.keyUp("up")
                    key_pressed["up"] = False

            if down_roi[0] <= y <= down_roi[3] and down_roi[1] <= x <= down_roi[2]:
                if not key_pressed["down"]:
                    print("down")
                    pag.keyDown("down")
                    key_pressed["down"] = True
            else:
                if key_pressed["down"]:
                    pag.keyUp("down")
                    key_pressed["down"] = False

            if left_roi[0] <= y <= left_roi[3] and left_roi[1] <= x <= left_roi[2]:
                if not key_pressed["left"]:
                    print("left")
                    pag.keyDown("left")
                    key_pressed["left"] = True
            else:
                if key_pressed["left"]:
                    pag.keyUp("left")
                    key_pressed["left"] = False

            if right_roi[0] <= y <= right_roi[3] and right_roi[1] <= x <= right_roi[2]:
                if not key_pressed["right"]:
                    print("right")
                    pag.keyDown("right")
                    key_pressed["right"] = True
            else:
                if key_pressed["right"]:
                    pag.keyUp("right")
                    key_pressed["right"] = False

    cv.imshow("VDPAD", frame_resized)

    key = cv.waitKey(1)  # wait for 1 ms
    if key == 27:  # exit on Esc key
        break

# Release resources
video_capture.release()
cv.destroyWindow("VDPAD")
hands.close()
