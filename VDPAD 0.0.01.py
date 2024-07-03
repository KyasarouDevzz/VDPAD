# Attempt at making a camera based dance pad for DDR.

# importing opencv and pyautogui

import cv2 as c
import pyautogui as p

# Opening a camera and a window

video_capture = c.VideoCapture(0)
c.namedWindow("VDPAD")

while True:
    ret, frame = video_capture.read()
    frame_flipped = c.flip(frame, 1)  # Flip horizontally
    c.imshow("VDPAD", frame_flipped)

    key = c.waitKey(1) # wait for 1 ms
    if key == 27: #exit on esc key
        break

#stops window

c.destroyWindow("VDPAD")
video_capture.release()
