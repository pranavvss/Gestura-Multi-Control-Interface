import cv2
import numpy as np
import math
import time
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.7, trackCon=0.7):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = float(detectionCon)
        self.trackCon = float(trackCon)

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS,
                        self.mpDraw.DrawingSpec(color=(255, 0, 255), thickness=4, circle_radius=6),
                        self.mpDraw.DrawingSpec(color=(0, 255, 0), thickness=4, circle_radius=6)
                    )

        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 12, (255, 0, 0), cv2.FILLED)

        return lmList

# Safe move function to avoid triggering PyAutoGUI's fail-safe
def safe_move_to(x, y):
    wScr, hScr = pyautogui.size()
    margin = 10  
    x = max(margin, min(wScr - margin, x))
    y = max(margin, min(hScr - margin, y))
    pyautogui.moveTo(x, y)

# Main function
def main():
    wCam, hCam = 640, 480
    frameR = 100  # Frame reduction for the mouse pointer control area
    smoothening = 7  # Smoothing factor for mouse pointer movement (Make it less if you want)

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    pTime = 0

    detector = handDetector(detectionCon=0.7)

    wScr, hScr = pyautogui.size() 
    plocX, plocY = 0, 0 
    clocX, clocY = 0, 0 
    
    # Set up system audio control using pycaw
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    volRange = volume.GetVolumeRange()
    minVol = volRange[0]  # Typically this is a negative value
    maxVol = volRange[1]  # Typically this is 0

    vol = 0
    volBar = 400
    volPer = 0

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            x1, y1 = lmList[8][1], lmList[8][2]
            x2, y2 = lmList[12][1], lmList[12][2]

            fingers = [lmList[i][2] < lmList[i - 2][2] for i in [8, 12, 16, 20]]
            if fingers[1] == 0 and fingers[2] == 0:  # If index and middle fingers are up
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                safe_move_to(wScr - clocX, clocY)
                plocX, plocY = clocX, clocY

                cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

            if fingers[1] == 1 and fingers[2] == 1:  # Clicking mode: both index and middle fingers up
                length = math.hypot(x2 - x1, y2 - y1)
                if length < 40:
                    cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                    pyautogui.click()

            # To be able to control volume you can only use thumb and index fingers, no other fingers will be tracked.
            if fingers[0] == 1 and fingers[1] == 0:  
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                length = math.hypot(x2 - x1, y2 - y1)

                volPer = np.interp(length, [50, 300], [20, 80])
                volBar = np.interp(length, [50, 300], [400, 150])

                vol = np.interp(volPer, [20, 80], [minVol, maxVol])
                volume.SetMasterVolumeLevel(vol, None)

                if length < 50:
                    cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

                cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
                cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
                cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_SIMPLEX,
                            1.5, (255, 0, 0), 3, lineType=cv2.LINE_AA)

        # Below will calculate and show your fps on the output cam
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS: {int(fps)}', (40, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 3, lineType=cv2.LINE_AA)

        cv2.namedWindow("Volume & Mouse Control by Pranav", cv2.WINDOW_NORMAL)
        cv2.imshow("Volume & Mouse Control by Pranav", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
