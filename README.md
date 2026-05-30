# mediapipe-volume-controller
A computer vision project that enables real-time Windows volume control through hand gestures using MediaPipe hand tracking, OpenCV, and Pycaw.

# Gesture Volume Control

Control Windows system volume using hand gestures captured through a webcam. The project uses MediaPipe hand tracking to detect the distance between the thumb and index finger and maps that distance to the system volume level in real time.

## Features

* Real-time hand tracking
* Finger-distance-based volume control
* Live visual volume bar
* Webcam-based interaction
* Windows audio control using Pycaw

## Technologies Used

* Python 3.12
* OpenCV
* MediaPipe Tasks
* NumPy
* Pycaw

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/gesture-volume-control.git
cd gesture-volume-control
```

Create and activate a virtual environment:

```bash
python -m venv venv

# PowerShell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Requirements

* Python 3.12
* Webcam
* Windows OS (required for Pycaw volume control)

## Running the Project

Make sure the virtual environment is activated, then run:

```bash
python vol_control.py
```

## Controls

* Move thumb and index finger closer together to decrease volume.
* Move thumb and index finger farther apart to increase volume.
* Press `ctrl+c` to quit.

## Future Improvements

* Gesture smoothing
* Mute gesture
* Multi-hand support
* Brightness control
* Custom calibration

## Author

Zainab

