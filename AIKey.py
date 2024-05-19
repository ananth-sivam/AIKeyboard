from time import sleep

import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import cvzone

from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280) # width
cap.set(4, 720) # height

detector = HandDetector(detectionCon=0.8, maxHands=2)
keyboard = Controller()

class AlphabetButtons():
    def __init__(self, pos, text, size=(85,85)):
        self.pos = pos
        self.text = text
        self.size = size


# basic draw keyboard
def draw_key(alphaList, img):
    for myAlphaButton in alphaList:
        x, y = myAlphaButton.pos
        w, h = myAlphaButton.size
        cv2.rectangle(img, myAlphaButton.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, myAlphaButton.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


# def draw_key(alphaList, img):
#     imgNew = np.zeros_like(img, np.uint8)
#     for myAlphaButton in alphaList:
#         x,y = myAlphaButton.pos
#         cvzone.cornerRect(imgNew, (myAlphaButton.pos[0], myAlphaButton.pos[1], myAlphaButton.size[0],
#                                    myAlphaButton.size[1]), 20, rt=0)
#         cv2.rectangle(imgNew, myAlphaButton.pos, (x+myAlphaButton.size[0],y+myAlphaButton.size[1]),
#                       (255,0,255), cv2.FILLED)
#         cv2.putText(imgNew, myAlphaButton.text, (x+40, y+60), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 3)
#
#     out = img.copy()
#     transparency = 0.5
#     mask = imgNew.astype(bool)
#     print(mask.shape)
#     out[mask] = cv2.addWeighted(img, transparency, imgNew, 1-transparency, 0)[mask]
#     return out


alphabets = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
             ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
             ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
alphaList = []
finalText = ""
gap = 10

for row in range(0, len(alphabets)):
    shift = 0
    for alphabet in alphabets[row]:
        alphaList.append(AlphabetButtons((100*shift+50+gap, 100*row+50), alphabet))
        shift = shift+1

while True:
    success, img = cap.read()

    img = draw_key(alphaList, img)

    hands, img = detector.findHands(img, flipType=False)
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bboxInfo = hand1["bbox"]
        lmList2 = None
        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
        for myAlphaButton in alphaList:
            x,y = myAlphaButton.pos
            w,h = myAlphaButton.size
            if x < lmList1[8][0] < x+w and y <lmList1[8][1]<y+h:
                cv2.rectangle(img, myAlphaButton.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, myAlphaButton.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                if lmList1:
                    l,_,_ = detector.findDistance(lmList1[8], lmList1[12], img) # index-finger=8 and middle-finger=12
                    print(l)
                    if l < 25:
                        keyboard.press(myAlphaButton.text)
                        cv2.rectangle(img, myAlphaButton.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, myAlphaButton.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        finalText += myAlphaButton.text
                        sleep(0.15)

    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 425), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)














