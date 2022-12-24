import cv2
import numpy as np
import math
import random as rd
import time
import pyautogui as pag
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 720)
cap.set(4, 720)

detector = HandDetector(maxHands=2, detectionCon=0.8)

handColor1 = (0,255,0)
handColor2 = (255,0,0)

def decisionVariable(hand1, hand2):
    hx11, hy11 = hand1["lmList"][5][:2]
    hx12, hy12 = hand1["lmList"][17][:2]

    hx21, hy21 = hand2["lmList"][5][:2]
    hx22, hy22 = hand2["lmList"][17][:2]

    distance1 = int(math.sqrt((hy12 - hy11) ** 2 + (hx12 - hx11) ** 2))
    distance2 = int(math.sqrt((hy22 - hy21) ** 2 + (hx22 - hx21) ** 2))

    return distance1, distance2

def triggerDecision(d1,d2):
    bool = [False,False]
    if d1>60:
        bool[0] = True
    if d2>60:
        bool[1] = True
    return bool

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hand, img = detector.findHands(img, draw=True)

    if hand:
        if len(hand) == 2:
            dist1, dist2 = decisionVariable(hand[0], hand[1])
            controller = triggerDecision(dist1,dist2)
            hx1,hy1 = hand[0]["lmList"][5][:2]
            hx2,hy2 = hand[1]["lmList"][5][:2]

            cv2.circle(img, (hx1, hy1), 50,handColor1, cv2.FILLED)
            cv2.circle(img, (hx2, hy2), 50,handColor2, cv2.FILLED)

            if controller[0]:
                handColor1 = (0,0,255)
                pag.press('left')
            else:
                handColor1 = (0,255,0)
            if controller[1]:
                handColor2 = (0,0,255)
                pag.press('right')
            else:
                handColor2 = (255,0,0)

    cv2.imshow("image", img)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

if __name__ == "__main__":
    pass
