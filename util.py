import numpy as np
import cv2


def get_limits(color):

    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Get the hue value, first index is hue, second is saturation and last is the value or range

    # Handle red hue wrap-around, red because its the cloese to the lowest value of range and the highest
    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit


# This code essentially tells the computer, "Hey, when you're looking at colors, don't think of them the way humans do with RGB or BGR.
# Instead, think about them in terms of HSV, which stands for Hue (kind of color), Saturation (intensity of the color), and Value (the range of how dark or bright it  is).
# I'll help you understand colors better that way."
# So, when you show the computer a color, it's like saying, "I see yellow," but the computer might not exactly see it as "yellow." Instead,
# it will think about it in terms of its hue (the type of color it is), saturation (how intense it is), and value (how bright or dark it is). Then,
# it will try to find other colors in a range that are similar to what you showed it, so it can work with colors in a way it's more familiar with."
