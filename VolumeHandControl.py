import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import alsaaudio
import os
mixer = alsaaudio.Mixer()
vol_range = mixer.getvolume()
print(vol_range)


wcam,hcam = 640,480

cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
pTime=0

detector = htm.handDetector()


while True:

    success , img = cap.read()

    img = detector.findHands(img)
    lmsList = detector.findPosition(img,draw=False)
    if len(lmsList)!=0:
        #print(lmsList[4],lmsList[8])

        x1,y1 = lmsList[4][1],lmsList[4][2]
        x2, y2 = lmsList[8][1], lmsList[8][2]
        cx,cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img,(x1,y1),10,(255,0,0),cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        #print(length)

        vol = np.interp(length, [50, 250], [0, 100])
        mixer.setvolume(int(vol))

        if length < 50 :
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,f'FPS:  {int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,
                1,(255,0,0),3)

    cv2.imshow("Img",img)
    cv2.waitKey(1)