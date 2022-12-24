import cv2
import numpy as np
import math
import random as rd
import time
from  cvzone.HandTrackingModule import  HandDetector


cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(maxHands=1,detectionCon=0.8)

x = [300,245,200,170,145,130,112,103,93,87,80,75,70,67,62,59,57]
y = [20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]

coff = np.polyfit(x,y,2)
A,B,C = coff

x = 80
y = 80
w = 220
h = 30

# Target
cx,cy = 250,250
color = (255,0,0)
counter = 0
def createTarget(img,cx,cy):
    cv2.circle(img, (cx, cy), 30, color, -1)
    cv2.circle(img, (cx, cy), 10, (255, 255, 255), -1)
    cv2.circle(img, (cx, cy), 30, (50, 55, 55), 2)

# Score
score = 0
def createScore(score):
    cv2.rectangle(img, (100, 40), (290,95), (36, 36, 12), -1)
    cv2.putText(img, f'Score {str(score).zfill(2)}', (120, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

#Time
timeStart = time.time()
totalTime = 20
gameOverCounter = 0
playAgainBgColor = (36,36,12)
def createTimer():
    cv2.rectangle(img, (1000, 40), (1190,95), (36, 36, 12), -1)
    cv2.putText(img, f'Time : {int(totalTime-(time.time()-timeStart))}', (1020, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

def gameOver():
    cv2.rectangle(img, (500, 100), (750,300), (36, 10, 255), -1)
    cv2.putText(img, f'Game Over', (540, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(img, f'Score : {score}', (560, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.rectangle(img, (500, 400), (750,500), playAgainBgColor, -1)
    cv2.putText(img, f'Play Again!', (540, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

while True:
    success,img = cap.read()
    img = cv2.flip(img,1)

    hand,img = detector.findHands(img)
    if time.time() - timeStart < totalTime:
        if hand:
            lmList = hand[0]["lmList"]
            bx, by, bw, bh = hand[0]["bbox"]
            x1, y1 = lmList[5][0], lmList[5][1]
            x2, y2 = lmList[17][0], lmList[17][1]
            distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
            distanceCM = int((A * distance ** 2) + (B * distance) + C)

            if distanceCM < 60:
                if bx < cx < bx + bw and by < cy < by + bh:
                    print("click")
                    counter = 1
            if counter:
                counter += 1
                color = (0, 255, 0)
                if counter == 3:
                    cx = rd.randint(50, 700)
                    cy = rd.randint(80, 700)
                    color = (255, 0, 0)
                    score += 1
                    counter = 0

            cv2.rectangle(img, (bx - 30, by - 20), (bx + 220, by - 60), (36, 36, 12), -1)
            cv2.putText(img, f'Distance {distanceCM} cm', (bx - 20, by - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (255, 255, 255), 2)

            print(distanceCM)

        createTarget(img, cx, cy)
        createScore(score)
        createTimer()
    else:
        gameOver()
        if hand:
            lmList = hand[0]["lmList"][8]
            print(hand[0]["lmList"][8])
            if 500<lmList[0]<750 and 400<lmList[1]<500:
                gameOverCounter = 1
        if gameOverCounter:
            gameOverCounter += 1
            playAgainBgColor = (100,210,100)
            if gameOverCounter == 3:
                timeStart = time.time()
                score = 0
                gameOverCounter = 0
                playAgainBgColor = (36,36,19)


    cv2.imshow("image",img)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break


