# Gestura- Multi Control Interface

>[!NOTE]
>Control your mouse and system volume without even touching your keyboard and mouse.(No Hardware Required)

It is innovative application that allows users to control their computer's system volume and mouse pointer through simple hand gestures. Utilizing computer vision technology and hand tracking via a webcam, the software interprets finger movements to adjust the volume or move the mouse cursor seamlessly.

# Final Output

https://github.com/user-attachments/assets/51a02a42-782a-4ce7-8af2-429ba9004691


https://github.com/user-attachments/assets/666f121a-53fe-4caf-84aa-b46e4910ad0d


------------------------------------------------------------------------------------------

>[!NOTE]
>Scrole to the very bottom "TO SEE UPDATED FEATURES - CHANGELOGS



## About the Project

It is a simple and fun project that lets you control your computer’s system volume and mouse pointer using hand gestures. By moving your hand in front of a webcam, you can increase or decrease the volume or move the mouse around the screen. This project combines two powerful features: adjusting the volume and controlling the mouse, all without touching your computer. It's designed to give you a hands-free way to interact with your computer.

------------------------------------------------------------------------------------------

## Requirements (Langauge, Libraries,Frameworks and Software)

- [Programming Language](https://www.python.org/downloads/) - Python: This project is built using Python, You must be somewhere around intermediate pyhton programmer to understand all the functions and statement.
  
- [OpenCV](https://docs.opencv.org/4.x/d0/de3/tutorial_py_intro.html#:~:text=OpenCV%2DPython%20is%20a%20Python,to%20and%20from%20Numpy%20arrays.): A library used for computer vision tasks, such as capturing and processing video from a webcam. It allows the program to "see" your hand movements.
- [Mediapipe](https://ai.google.dev/edge/mediapipe/solutions/guide): A framework developed by Google that helps with detecting and tracking hand movements in real-time. It makes hand gesture recognition easy and accurate.
- [PyAutoGUI](https://pypi.org/project/PyAutoGUI/): A library used to control the mouse and keyboard programmatically. In this project, it's used to move the mouse pointer based on your hand's position.
- [PyCaw](https://pypi.org/project/PyAutoGUI/): A library that allows Python to control the system's audio settings, such as volume. This is how the project adjusts your computer's volume based on hand gestures.
- [NumPy](https://numpy.org/doc/stable/user/absolute_beginners.html): A library for numerical computing in Python. It helps with processing the coordinates of hand movements.
- [Comtypes](https://pypi.org/project/comtypes/): A library used to interact with Windows components, required for controlling system volume through PyCaw.
  
- Ensure python is installed in our computer.
- [WebCam](https://www.dev47apps.com/): If you don’t have a webcam, you can use your smartphone as a webcam with DroidCam. It connects your phone’s camera to your computer.

------------------------------------------------------------------------------------------

## Set Up Your Environment
- Open up your Powershell (w Admin Permission) (Windows + X is the shortcut to menu)
- Under powershell locate to the directory where you want to store this project by using this command [cd C:\path\to\your\project]
- Run the following command to create a Python environmnent [python -m venv env]
- and then run [.\env\Scripts\Activate.ps1] and if this does'nt work for you run the next command [.\env\Scripts\activate]
- Somepeople may have a Windows execution problem so you can run this command [Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process] and Enter Y when asked. once done restart powershell, locate to your directory again and run the env commands.
- If sucessfully done, youll have no error and in powershell ahead of your directory path there will be written (.env) in green
  
![image](https://github.com/user-attachments/assets/efef274e-55e3-467a-9a7b-398b9536cbbc)

------------------------------------------------------------------------------------------

## Installing libraries & Setup
Run this command in the same powershell to install all libraries.

```python
pip install opencv-python mediapipe pycaw comtypes pyautogui numpy
```
Make sure your webcam setup is ready for time we will need it.

Also make sure your directory looks same 

![image](https://github.com/user-attachments/assets/985fa8e4-26e5-45cc-9b21-5fc3d5b1a534)


------------------------------------------------------------------------------------------
How It Works (Updated)
------------------------------------------------------------------------------------------

1. Import Libraries
   
```python
Copy code
import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy  # For controlling the mouse pointer
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
```

cv2: Used for image processing and video capture.

numpy: Utilized for numerical operations, including interpolation.

HandTrackingModule: A custom module for hand tracking using MediaPipe.

autopy: Provides functions to control the mouse pointer programmatically.

pycaw: A library for controlling system audio in Windows.

math: Used for mathematical operations like calculating distance.

------------------------------------------------------------------------------------------

2. Initialize Hand Detector
   
```python
Copy code
detector = htm.HandDetector(maxHands=2)
```

HandDetector: The object detector is created from the HandDetector class in HandTrackingModule. It allows us to detect up to two hands.

------------------------------------------------------------------------------------------


3. Initialize Webcam

```python
Copy code
cap = cv2.VideoCapture(0)
```

VideoCapture: This object captures video from the default webcam (0).


------------------------------------------------------------------------------------------

4. Get Screen Dimensions

```python
Copy code
wScr, hScr = autopy.screen.size()
frameR = 100  # Frame Reduction
smoothening = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0
```

autopy.screen.size(): Retrieves the width and height of the screen.

frameR: The frame reduction used to create a boundary within which the mouse movement is smoothened.

smoothening: A factor to smoothen the mouse movement.

plocX, plocY, clocX, clocY: Variables to store the previous and current location of the mouse pointer.


------------------------------------------------------------------------------------------

5. Initialize Pycaw for Volume Control

```python
Copy code
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
```
AudioUtilities.GetSpeakers(): Retrieves the speaker device.

IAudioEndpointVolume: Interface used to control the volume.

volRange: The range of the system volume, used to map hand gestures to volume levels.


------------------------------------------------------------------------------------------


6. Main Loop

```python
Copy code
while True:
    success, img = cap.read()
    img, handsType = detector.findHands(img)
```

cap.read(): Captures a frame from the webcam.

detector.findHands(img): Detects hands in the frame and determines whether they are left or right hands.

------------------------------------------------------------------------------------------

7. Process Each Hand

```python
Copy code
if len(handsType) > 0:
    for i, handType in enumerate(handsType):
        lmList = detector.findPosition(img, i)
        if len(lmList) != 0:
            if handType == "Right":
                # Mouse Control
```

handsType: Contains the type of each detected hand (left or right).

detector.findPosition(img, i): Retrieves the landmarks of the detected hand.

------------------------------------------------------------------------------------------

9. Mouse Control with Right Hand

```python
Copy code
x1, y1 = lmList[8][1:]  # Index finger tip
x2, y2 = lmList[12][1:]  # Middle finger tip
lmList[8][1:]: The coordinates of the index finger tip.
lmList[12][1:]: The coordinates of the middle finger tip.
Finger State Detection
python
Copy code
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
```

fingers[]: An array to determine which fingers are up.

------------------------------------------------------------------------------------------

10. Mouse Movement

```python

if fingers[1] == 1 and fingers[2] == 0:
    x3 = np.interp(x1, (frameR, 640 - frameR), (0, wScr))
    y3 = np.interp(y1, (frameR, 480 - frameR), (0, hScr))
    clocX = plocX + (x3 - plocX) / smoothening
    clocY = plocY + (y3 - plocY) / smoothening
    autopy.mouse.move(wScr - clocX, clocY)
    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
    plocX, plocY = clocX, clocY
```
np.interp(): Maps the finger position to the screen size.

autopy.mouse.move(): Moves the mouse pointer.

cv2.circle(): Draws a circle on the detected finger tip.

------------------------------------------------------------------------------------------

11. Mouse Click

```python
Copy code
if fingers[1] == 1 and fingers[2] == 1:
    length = math.hypot(x2 - x1, y2 - y1)
    if length < 40:
        cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
        autopy.mouse.click()
```

math.hypot(): Calculates the distance between the index and middle fingers.

autopy.mouse.click(): Performs a mouse click if the fingers are close enough.

------------------------------------------------------------------------------------------

12. Volume Control with Left Hand

```python
Copy code
elif handType == "Left":
    x1, y1 = lmList[4][1], lmList[4][2]
    x2, y2 = lmList[8][1], lmList[8][2]
    length = math.hypot(x2 - x1, y2 - y1)
    vol = np.interp(length, [50, 300], [minVol, maxVol])
    volBar = np.interp(length, [50, 300], [400, 150])
    volPer = np.interp(length, [50, 300], [0, 100])
    volume.SetMasterVolumeLevel(vol, None)
    cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
```

math.hypot(): Measures the distance between the thumb and index finger.

volume.SetMasterVolumeLevel(): Adjusts the system volume based on the finger distance.

------------------------------------------------------------------------------------------

13. Volume Bar Display

```python
Copy code
cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN,
            1, (0, 255, 0), 3)
```
cv2.rectangle(): Draws the volume bar on the screen.

cv2.putText(): Displays the current volume percentage.

------------------------------------------------------------------------------------------

14. Display the Frame
    
```python
Copy code
cv2.imshow("Image", img)
if cv2.waitKey(1) & 0xFF == ord('q'):
    break
```

cv2.imshow(): Displays the frame with the visualizations.

cv2.waitKey(1): Exits the loop when 'q' is pressed.

------------------------------------------------------------------------------------------

15. Release Resources
    
```python
Copy code
cap.release()
cv2.destroyAllWindows()
```
cap.release(): Releases the webcam.

cv2.destroyAllWindows(): Closes all OpenCV windows.

------------------------------------------------------------------------------------------

>[!NOTE]

>If you like more content like this read my other documents on computer vision, python programming, openCV etc.

>[Multi Stream Vision using OpenCV, 2022 updated version -  Click to read this Document](https://github.com/pranavvss/Multi-Stream-Vision-Real-Time-Object-Detection-)

>[Hand and face tracking model 2022 updated version , Click to read this Document](https://github.com/pranavvss/Hand-Face-detection-model-using-python)
