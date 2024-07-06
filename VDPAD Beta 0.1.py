import cv2 as c
import pyautogui as p
import numpy as n
import time

# Opening a camera and a window
video_capture = c.VideoCapture(0)
c.namedWindow("VDPAD")

# Define the lower and upper bounds for black color in HSV
lower_black = n.array([0, 0, 0], dtype=n.uint8)
upper_black = n.array([114, 149, 70], dtype=n.uint8)

# Background subtractor
background_subtractor = c.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=False)

# Delay between actions to avoid rapid firing
action_delay = 0.5
last_action_time = time.time()

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Apply background subtraction
    fg_mask = background_subtractor.apply(frame)

    # Convert BGR to HSV
    hsv_frame = c.cvtColor(frame, c.COLOR_BGR2HSV)

    # Create a mask for black
    mask = c.inRange(hsv_frame, lower_black, upper_black)
    
    # Combine the masks
    combined_mask = c.bitwise_and(mask, mask, mask=fg_mask)

    # Apply morphological operations to clean the mask
    kernel = c.getStructuringElement(c.MORPH_RECT, (5, 5))
    combined_mask = c.morphologyEx(combined_mask, c.MORPH_CLOSE, kernel)
    combined_mask = c.morphologyEx(combined_mask, c.MORPH_OPEN, kernel)

    # Get frame dimensions
    height, width, _ = frame.shape
    roi_height = height // 3
    roi_width = width // 3

    # Define ROIs
    up_roi = (0, roi_width, 2 * roi_width, roi_height)  # Center-top
    down_roi = (2 * roi_height, roi_width, 2 * roi_width, height)  # Center-bottom
    left_roi = (roi_height, 0, roi_width, 2 * roi_height)  # Center-left
    right_roi = (roi_height, 2 * roi_width, width, 2 * roi_height)  # Center-right

    # Draw ROI rectangles (for debugging purposes)
    c.rectangle(frame, (up_roi[1], up_roi[0]), (up_roi[2], up_roi[3]), (0, 255, 0), 2)  # Up region
    c.rectangle(frame, (down_roi[1], down_roi[0]), (down_roi[2], down_roi[3]), (0, 255, 255), 2)  # Down region
    c.rectangle(frame, (left_roi[1], left_roi[0]), (left_roi[2], left_roi[3]), (255, 0, 0), 2)  # Left region
    c.rectangle(frame, (right_roi[1], right_roi[0]), (right_roi[2], right_roi[3]), (0, 0, 255), 2)  # Right region

    current_time = time.time()
    if current_time - last_action_time >= action_delay:
        if n.any(combined_mask[up_roi[0]:up_roi[3], up_roi[1]:up_roi[2]]):
            # Simulate up arrow key press
            print("up")
            p.press("up")
            last_action_time = current_time
        elif n.any(combined_mask[down_roi[0]:down_roi[3], down_roi[1]:down_roi[2]]):
            # Simulate down arrow key press
            print("down")
            p.press("down")
            last_action_time = current_time
        elif n.any(combined_mask[left_roi[0]:left_roi[3], left_roi[1]:left_roi[2]]):
            # Simulate left arrow key press
            print("left")
            p.press("left")
            last_action_time = current_time
        elif n.any(combined_mask[right_roi[0]:right_roi[3], right_roi[1]:right_roi[2]]):
            # Simulate right arrow key press
            print("right")
            p.press("right")
            last_action_time = current_time

    # Flip frame for better user experience
    frame_flipped = c.flip(frame, 1)
    c.imshow("VDPAD", frame_flipped)

    key = c.waitKey(1)  # wait for 1 ms
    if key == 27:  # exit on esc key
        break

# Release resources
video_capture.release()
c.destroyWindow("VDPAD")

