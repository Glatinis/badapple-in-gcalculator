import cv2
import numpy as np
import os
import time

# Load the video file
video = cv2.VideoCapture('bad apple.mp4')

# Define the ASCII characters to use
ASCII_CHARS = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']

# Function to convert a frame to ASCII characters
def frame_to_ascii(frame):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize the frame to a smaller size
    resized_frame = cv2.resize(gray_frame, (80, 45))

    # Normalize the pixel values to the range [0, 9]
    normalized_frame = (resized_frame / 255) * 9

    # Convert the pixel values to ASCII characters
    ascii_frame = np.array([ASCII_CHARS[int(p)] for p in normalized_frame.flatten()])

    # Reshape the ASCII characters to the original frame size
    ascii_frame = ascii_frame.reshape(resized_frame.shape)

    return ascii_frame

# Main program loop
while True:
    # Read a frame from the video
    ret, frame = video.read()

    # Check if we have reached the end of the video
    if not ret:
        break

    # Convert the frame to ASCII characters
    ascii_frame = frame_to_ascii(frame)

    # Clear the console window
    print('\033[2J')

    # Print the ASCII characters to the console window
    print('\033[1;1H')
    print('\n'.join([''.join(row) for row in ascii_frame]))

    # Wait for a short amount of time before displaying the next frame
    time.sleep(1/30)

# Release the video file
video.release()
