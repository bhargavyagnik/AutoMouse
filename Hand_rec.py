import cv2 as cv
import numpy as np
import pyautogui as p


def main():
    # try:
    vid = cv.VideoCapture(0)  # Get video from Screen
    HAND_RECOGNISED = False
    hand_cascade = cv.CascadeClassifier('haarcascade_hand.xml')
    fgbg=cv.createBackgroundSubtractorKNN(1)
    while True:
        ret, frame = vid.read()
        frame = np.flip(frame, axis=1)  # Getting the Reverse of the Frame so now it is exact as we see
        cv.imshow('original', frame)
        gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        blur=cv.GaussianBlur(gray,(5,5),0)
        hand=hand_cascade.detectMultiScale(frame)
        for (x,y,w,h) in hand:
            cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            print(x,y,w,h)
        cv.imshow('Hand',frame)




        if cv.waitKey(30) & 0xff == 27:
            break
        if HAND_RECOGNISED:
            print("Yeha I Got you")

        elif not HAND_RECOGNISED:
            print("No input")
            # p.moveTo(34,315) To move mouse Cursor to a given place
    vid.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
