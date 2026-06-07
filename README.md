# HandMotion Mouse

A computer vision-based hand tracking application that controls mouse movement, clicks, drag-and-drop, and PowerPoint presentations using hand gestures.

## Features

* Hand tracking using webcam
* Mouse movement control
* Left click gesture
* Right click gesture
* Drag and drop gesture
* PowerPoint next slide
* PowerPoint previous slide
* Multi-monitor support

## Requirements

* Windows 10/11
* Python 3.11+
* Webcam

## Dependencies

This project uses:

- cvzone
- mediapipe
- opencv-contrib-python
- PyAutoGUI
- screeninfo

## Installation

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python hand_trackv6.py
```

## Notes

* Tested on Windows 11
* Requires a webcam
* Supports multi-monitor environments
