import numpy as np
from imutils.video import WebcamVideoStream
import imutils
import cv2
import math
import pyautogui
import time

pyautogui.FAILSAFE = False

# setting the lower and upper range for mask1,[H,S,V], for lighter shades
lower_red = np.array([20, 70, 70])
upper_red = np.array([30, 255, 255])

# setting the lower and upper range for mask2, for darker shades
low_red = np.array([23, 41, 133])
up_red = np.array([40, 150, 255])

# setting the lower and upper range for mask, for blue
lower_b = np.array([110, 50, 50])
upper_b = np.array([130, 255, 255])

# Prior initialization of all centers for safety
one_cen, two_cen = [240, 320], [240, 320]
cursor = [960, 540]

# Area ranges for contours of different colours to be detected
area = [300, 1900]

# Rectangular kernal for eroding and dilating the mask for primary noise removal 
kernel = np.ones((7, 7), np.uint8)
showCentroid = False
cur_pos = [240, 320]
contour = -1

dim = pyautogui.size()  # Dimension of Screen

sensitivity = 4  # Scale like 1,2,3,4,5 where 1 is lowest sensitiviy and 5 max


# To bring to the top the contours with largest area in the specified range
# Used in drawContour()
def swap(array, i, j):
    temp = array[i]
    array[i] = array[j]
    array[j] = temp


def centroid(vid, contour):
    M = cv2.moments(contour)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        center = (cx, cy)
        if showCentroid:
            cv2.circle(vid, center, 5, (0, 0, 255), -1)

        return center


# Contours on the mask are detected.. Only those lying in the previously set area
# range are filtered out and the centroid of the largest of these is drawn and returned 
def drawCentroid(vid, color_area, mask, showCentroid):
    ret = False
    center = (-1, -1)

    contour, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    l = len(contour)
    area = np.zeros(l)

    # filtering contours on the basis of area range specified globally
    for i in range(l):
        if cv2.contourArea(contour[i]) > color_area[0] and cv2.contourArea(contour[i]) < color_area[1]:
            area[i] = cv2.contourArea(contour[i])
        else:
            area[i] = 0

    a = sorted(area, reverse=True)

    # bringing contours with largest valid area to the top
    for i in range(l):
        for j in range(1):
            if area[i] == a[j]:
                swap(contour, i, j)

    if l > 0:
        center = centroid(vid, contour[0])
        ret = True
    return ret, center


def setCursorPos(yc, pyp):
    if abs(yc[0] - pyp[0]) < 5 and abs(yc[1] - pyp[1]) < 5:
        y1 = yc[0] + .7 * (pyp[0] - yc[0])
        y2 = yc[1] + .7 * (pyp[1] - yc[1])
    else:
        y1 = yc[0] + .1 * (pyp[0] - yc[0])
        y2 = yc[1] + .1 * (pyp[1] - yc[1])

    return round(y1), round(y2)


# Distance between two centroids
def distance(c1, c2):
    distance = pow(pow(c1[0] - c2[0], 2) + pow(c1[1] - c2[1], 2), 0.5)
    return distance


def chooseAction(x):
    out = 'none'
    if x < 40:
        out = 'left'
    elif x > 150:
        out = 'right'
    elif x > 60 and x < 100:
        out = 'move'
    print(out)
    return out


def move_mouse(pos):
    global cursor
    cursor[0] = 3 * (pos[0])
    cursor[1] = 3 * (pos[1])
    if cursor[0] <= dim[0] and cursor[1] <= dim[1]:
        print('move mouse: ', cursor)
        pyautogui.moveTo(cursor[0], cursor[1])


def click_mouse(cliks, buttn):
    pyautogui.click(clicks=cliks, button=buttn)


def do_action(action, pos):
    if action == 'move':
        move_mouse(pos)
    elif action == 'right':
        click_mouse(1, 'right')
    elif action == 'left':
        click_mouse(1, 'left')
    else:
        print(action)

def open_onscreen_keyboard():
    pyautogui.hotkey("ctrl","winleft", "o")
def colour_filter():
    pyautogui.hotkey("ctrl", "winleft", "c")
    pyautogui.hotkey('winleft','r')
    pyautogui.typewrite('ms-settings:easeofaccess-colorfilter')
    pyautogui.hotkey('enter')
def mouse():
    global low_red, lower_b, lower_red, up_red, upper_b, upper_red, cur_pos, one_cen, two_cen
    vs = cv2.VideoCapture(0)

    while True:

        _, frame = vs.read()
        frame = cv2.bilateralFilter(frame, 5, 50, 100)
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        mask2 = cv2.inRange(hsv, low_red, up_red)
        mask1 = mask1 + mask2
        mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel)
        mask1 = cv2.dilate(mask1, kernel, iterations=1)

        maskb = cv2.inRange(hsv, lower_b, upper_b)
        maskb = cv2.morphologyEx(maskb, cv2.MORPH_OPEN, kernel)
        maskb = cv2.dilate(maskb, kernel, iterations=1)

        oldpos = cur_pos

        ret1, one_cen = drawCentroid(frame, area, mask1, showCentroid)
        ret2, two_cen = drawCentroid(frame, area, maskb, showCentroid)

        if ret1 == True and ret2 == True:
            cur_pos = setCursorPos(one_cen, oldpos)
            cv2.circle(frame, cur_pos, 5, (0, 0, 255), -1)

            x = distance(one_cen, two_cen)
            do_action(chooseAction(x), cur_pos)

        else:
            print('oops')

        cv2.imshow('blue', maskb)
        cv2.imshow('red', mask1)
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    vs.release()
    cv2.destroyAllWindows()

