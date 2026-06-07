# HandMotion Mouse - Complete User Guide

## Overview

HandMotion Mouse is a computer vision-based application that allows you to control your mouse cursor and PowerPoint presentations using hand gestures and a webcam.

Supported features:

* Mouse movement
* Left click
* Right click
* Drag and drop
* PowerPoint next slide
* PowerPoint previous slide
* Multi-monitor support

---

# First Time Setup

## 1. Download the Project

Download or clone the repository:

```bash
git clone https://github.com/recklesscode-y/handmotion-mouse.git
```

Move into the project folder:

```bash
cd handmotion-mouse
```

---

## 2. Create Virtual Environment

Create a dedicated Python environment for this project:

```bash
python -m venv handmotion_mouse
```

This creates:

```text
handmotion-mouse
├── hand_trackv6.py
├── README.md
├── GUIDE.md
├── requirements.txt
└── handmotion_mouse
    ├── Scripts
    ├── Lib
    └── ...
```

---

## 3. Activate Virtual Environment

Windows:

```bash
handmotion_mouse\Scripts\activate
```

You should see:

```text
(handmotion_mouse)
```

at the beginning of your command prompt.

Example:

```text
(handmotion_mouse) C:\Projects\handmotion-mouse>
```

---

## 4. Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

This will automatically install:

* cvzone
* mediapipe
* opencv-contrib-python
* PyAutoGUI
* screeninfo

and their required dependencies.

---

## 5. Run the Application

Start HandMotion Mouse:

```bash
python hand_trackv6.py
```

---

# Camera Selection

When the application starts, a camera selection window will appear.

Example:

```text
Choose Camera

Camera 0
Camera 1
Camera 2
```

Select the webcam you want to use.

The application will then start hand tracking.

---

# Gesture Guide

## Cursor Movement

### Gesture

* Index finger up
* All other fingers down

### Action

Moves the mouse cursor.

---

## Left Click

### Gesture

Touch your thumb and index finger together briefly.

### Action

Performs a left mouse click.

---

## Right Click

### Gesture

Touch your thumb and pinky finger together.

### Action

Performs a right mouse click.

---

## Drag and Drop

### Gesture

Touch your thumb and index finger together and hold for approximately 2 seconds.

### Action

Enters drag mode.

While holding:

* Move your hand to drag files, windows, folders, or objects.

Release your fingers to drop the item.

---

## PowerPoint Presentation Mode

### Gesture

Show a peace sign:

* Index finger up
* Middle finger up
* Ring finger down
* Pinky down

---

### Next Slide

While showing the peace sign:

Point your fingers to the right.

### Action

Moves to the next PowerPoint slide.

---

### Previous Slide

While showing the peace sign:

Point your fingers to the left.

### Action

Moves to the previous PowerPoint slide.

---

# Tracking Area Calibration

A yellow rectangle appears on screen.

This rectangle defines the active tracking area.

You can adjust it while the application is running.

---

## Keyboard Controls

| Key | Function                   |
| --- | -------------------------- |
| W   | Move top boundary up       |
| S   | Move top boundary down     |
| A   | Reduce left/right margin   |
| D   | Increase left/right margin |
| Q   | Reduce bottom boundary     |
| E   | Increase bottom boundary   |

Use these controls to improve cursor accuracy based on your webcam position.

---

# Multi-Monitor Support

HandMotion Mouse automatically detects multiple monitors.

The cursor can move across the entire desktop space, including:

* Single monitor setups
* Dual monitor setups
* Multi-monitor setups

No additional configuration is required.

---

# Recommended Setup

For best results:

* Use good room lighting
* Keep your hand inside the yellow tracking rectangle
* Position the webcam above or below the monitor
* Avoid extremely dark backgrounds
* Keep the webcam stable

---

# Exit Application

To close HandMotion Mouse:

Press:

```text
ESC
```

or

```text
X
```

---

# Tested Environment

* Windows 11
* Python 3.11
* USB Webcam
* Single Monitor
* Dual Monitor
* Multi-Monitor

---

# Troubleshooting

## Camera Not Found

Check:

* Webcam is connected
* Webcam is not being used by another application
* Correct camera is selected

---

## Cursor Not Moving

Check:

* Your hand is inside the tracking rectangle
* Webcam has sufficient lighting
* Index finger is clearly visible

---

## PowerPoint Gestures Not Working

Check:

* PowerPoint presentation is active
* Peace sign gesture is clearly detected
* Your hand remains inside the tracking area

---

## Missing Python Packages

Activate the virtual environment:

```bash
handmotion_mouse\Scripts\activate
```

Then reinstall packages:

```bash
pip install -r requirements.txt
```
