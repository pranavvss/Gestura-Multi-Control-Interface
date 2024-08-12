# Gestura- Multi Control Interface

### Control your mouse and system volume without even touching your keyboard and mouse.(No Hardware Required)

It is innovative application that allows users to control their computer's system volume and mouse pointer through simple hand gestures. Utilizing computer vision technology and hand tracking via a webcam, the software interprets finger movements to adjust the volume or move the mouse cursor seamlessly.

# Final Output

https://github.com/user-attachments/assets/51a02a42-782a-4ce7-8af2-429ba9004691


https://github.com/user-attachments/assets/666f121a-53fe-4caf-84aa-b46e4910ad0d


------------------------------------------------------------------------------------------

# <code style="color : darkorange">Scrole to the very bottom "TO SEE UPDATED FEATURES - CHANGELOGS"</code> 



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

```
pip install opencv-python mediapipe pycaw comtypes pyautogui numpy
```
Make sure your webcam setup is ready for time we will need it.

Also make sure your directory looks same 

![image](https://github.com/user-attachments/assets/985fa8e4-26e5-45cc-9b21-5fc3d5b1a534)


------------------------------------------------------------------------------------------
