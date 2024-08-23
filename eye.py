


"""
import cv2
import numpy as np

# Read the original image
image = cv2.imread("apple.jpg")




# Define the strength of the simulated blur (adjust as needed)
diopters = -10.00  # This corresponds to the prescription needed for the viewer

# Calculate the blur kernel size based on the diopters
# This is a simplistic conversion and may not accurately represent the visual impairment
# You may need to experiment with different values to achieve the desired effect
blur_kernel_size = max(int(abs(diopters) / 3), 1)  # Ensure a minimum kernel size of 1
# Ensure the kernel size is odd
blur_kernel_size = blur_kernel_size + 1 if blur_kernel_size % 2 == 0 else blur_kernel_size

# Apply Gaussian blur to simulate the effect of -6.00 diopter glasses
blurred_image = cv2.GaussianBlur(image, (blur_kernel_size, blur_kernel_size), 0)

# Display the original and blurred images
cv2.imshow('Original Image', image)
cv2.imshow('Simulated Image with -6.00 Diopter Blur', blurred_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""

"""
from time import sleep
import cv2
import pygame.image
from PIL import Image
import pyautogui
from util import get_limits


ScreenWidth, ScreenHeight =  1920, 1080
CameraWidth, CameraHeight = 640, 480


# Defining the scaling factors
WidthScale = ScreenWidth / CameraWidth
HeightScale = ScreenHeight / CameraHeight








def mouse_control():
    #yellow = [0, 255, 255]  # yellow in BGR colorspace
                          # Need change later on to a color that is uncommon in the surroundings

    color_for_detection = [0, 255, 0]


    cap = cv2.VideoCapture(0)

    smooth_factor = 0.3  # Adjust this value to control the smoothing level
    prev_mouse_pos = None

    while True:



        ret, frame = cap.read()

        frame = cv2.flip(frame, 1)

        hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lowerLimit, upperLimit = get_limits(color=color_for_detection)

        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

        mask_ = Image.fromarray(mask)

        bbox = mask_.getbbox()

        if bbox is not None:
            x1, y1, x2, y2 = bbox

            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

            # Calculate the center of the bounding box
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            scaled_center_x = int(center_x * WidthScale)
            scaled_center_y = int(center_y * HeightScale)

            # Smoothen the cursor movement
            if prev_mouse_pos is None:
                smoothed_mouse_pos = (scaled_center_x, scaled_center_y)
            else:
                smoothed_mouse_pos = (
                    int((1 - smooth_factor) * prev_mouse_pos[0] + smooth_factor * scaled_center_x),
                    int((1 - smooth_factor) * prev_mouse_pos[1] + smooth_factor * scaled_center_y)
                )

            pyautogui.moveTo(smoothed_mouse_pos[0], smoothed_mouse_pos[1])

            # Update previous mouse position
            prev_mouse_pos = smoothed_mouse_pos

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


mouse_control()
map.release()

cv2.destroyAllWindows()


"""



import cv2
from mediapipe.python import mediapipe as mp
import pyautogui




#access cam
camera = cv2.VideoCapture(0)

screenWidth, screenHeight = pyautogui.size()


#track hand gesture using landmarks
handGesture = mp.solutions.hands.Hands()
#draw landmarks on hand
drawingTools = mp.solutions.drawing_utils



def finger_control():
    while True:
        _, frame = camera.read()
        frame = cv2.flip(frame,1)
        value = frameHeight, frameWidth, _ = frame.shape
        rgbConvertedFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        #find landmark 8 
        output = handGesture.process(rgbConvertedFrame)
        hands = output.multi_hand_landmarks

        if hands:
            for hand in hands:
                drawingTools.draw_landmarks(frame, hand)
                landmarks = hand.landmark
                for id, landmark in enumerate(landmarks):
                    if id == 8:
                        x = int(landmark.x*frameWidth)
                        y = int(landmark.y*frameHeight)
                        cv2.circle(img=frame, center=(x,y), radius=30, color=(0, 255, 255))
                        mousePositionX = screenWidth/frameWidth*x
                        mousePositionY = screenHeight/frameHeight*y
                        pyautogui.moveTo(mousePositionX, mousePositionY)

        
        
        #accessing webcam tracking each frame specifically landmark 8 (index finger)
        cv2.imshow("Finger Tracker 2000", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

finger_control()
camera.release()

cv2.destroyAllWindows()




