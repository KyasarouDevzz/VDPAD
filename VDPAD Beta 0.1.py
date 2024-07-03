# Attempt at making a camera based dance pad for DDR.

# importing libraries
import cv2 as c
import pyautogui as p
import numpy as n
import time

# Opening a camera and a window

video_capture = c.VideoCapture(0)
c.namedWindow("VDPAD")

# define what's black and what not
lower_black = n.array([0, 0, 0], dtype=n.uint8)
upper_black = n.array([210, 0, 50], dtype=n.uint8)

while True:
    ret, frame = video_capture.read()

    # Get frame dimensions
    height, width, _ = frame.shape
    roi_height = height // 3  # Center-top third
    roi_width = width // 3

    # Convert BGR to HSV
    hsv_frame = c.cvtColor(frame, c.COLOR_BGR2HSV)

    # Create a mask for black
    mask = c.inRange(hsv_frame, lower_black, upper_black)

    # Check if mask contains white pixels in the ROI
    if n.any(mask[:roi_height, roi_width:2*roi_width]):
        # Simulate up arrow key press
        print("up")
        
        time.sleep(0.1)
    elif n.any(mask[:roi_height, :roi_width]):
        # Simulate right arrow key press
        print("right")
        
        time.sleep(0.1)
    elif n.any(mask[:roi_height, 2*roi_width:]):
        # Simulate left arrow key press
        print("left")
        
        time.sleep(0.1)
    elif n.any(mask[2*roi_height:, :]):
        # Simulate down arrow key press
        print("down")
        
        time.sleep(0.1)
    
    frame_flipped = c.flip(frame, 1)  # Flip horizontally
    c.imshow("VDPAD", frame_flipped)

    key = c.waitKey(1) # wait for 1 ms
    if key == 27: #exit on esc key
        break

#stops window

c.destroyWindow("VDPAD")
video_capture.release()
