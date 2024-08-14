import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy  # For controlling the mouse pointer
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

# Initialize hand detector
detector = htm.HandDetector(maxHands=2)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Get screen width and height for mouse control
wScr, hScr = autopy.screen.size()
frameR = 100  # Frame Reduction
smoothening = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Initialize pycaw for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    img, handsType = detector.findHands(img)

    if len(handsType) > 0:
        for i, handType in enumerate(handsType):
            lmList = detector.findPosition(img, i)
            if len(lmList) != 0:
                if handType == "Right":
                    # Mouse Control
                    x1, y1 = lmList[8][1:]  # Index finger tip
                    x2, y2 = lmList[12][1:]  # Middle finger tip
                    
                    # Check which fingers are up
                    fingers = []
                    if lmList[4][1] > lmList[3][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                    for id in range(1, 5):
                        if lmList[8 + id * 4][2] < lmList[6 + id * 4][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    
                    # Only Index Finger: Moving Mode
                    if fingers[1] == 1 and fingers[2] == 0:
                        # Convert Coordinates
                        x3 = np.interp(x1, (frameR, 640 - frameR), (0, wScr))
                        y3 = np.interp(y1, (frameR, 480 - frameR), (0, hScr))
                        
                        # Smoothen Values
                        clocX = plocX + (x3 - plocX) / smoothening
                        clocY = plocY + (y3 - plocY) / smoothening

                        # Move Mouse
                        autopy.mouse.move(wScr - clocX, clocY)
                        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                        plocX, plocY = clocX, clocY

                    # Both Index and Middle fingers are up: Clicking Mode
                    if fingers[1] == 1 and fingers[2] == 1:
                        # Find distance between fingers
                        length = math.hypot(x2 - x1, y2 - y1)
                        # Click mouse if distance short
                        if length < 40:
                            cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                            autopy.mouse.click()

                elif handType == "Left":
                    # Volume Control
                    x1, y1 = lmList[4][1], lmList[4][2]
                    x2, y2 = lmList[8][1], lmList[8][2]
                    length = math.hypot(x2 - x1, y2 - y1)

                    # Hand range 50 - 300
                    # Volume range -65 - 0
                    vol = np.interp(length, [50, 300], [minVol, maxVol])
                    volBar = np.interp(length, [50, 300], [400, 150])
                    volPer = np.interp(length, [50, 300], [0, 100])

                    volume.SetMasterVolumeLevel(vol, None)
                    cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)

                    # Drawings
                    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
                    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN,
                                1, (0, 255, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
