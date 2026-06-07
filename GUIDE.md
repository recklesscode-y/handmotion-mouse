# HandMotion Mouse Guide

## Overview

HandMotion Mouse is a computer vision-based application that allows you to control your mouse cursor and PowerPoint presentations using hand gestures and a webcam.

### Features

* Mouse movement control
* Left click gesture
* Right click gesture
* Drag and drop gesture
* Start PowerPoint slideshow
* Next PowerPoint slide
* Previous PowerPoint slide
* Close active window
* Multi-monitor support

### Requirements

* Windows 10 / Windows 11
* Python 3.11+
* Webcam

## Quick Start

### First Time Setup

Run:

```text
setup.bat
```

This will automatically:

* Create a virtual environment
* Install required packages
* Prepare the application

### Start Application

Run:

```text
run.bat
```

---

## Camera Selection

When the application starts, select the webcam you want to use.

---

## Gesture Controls

### Move Cursor

Gesture:

* Index finger up
* Other fingers down

Action:

* Move mouse cursor

---

### Left Click

Gesture:

* Touch thumb and index finger briefly

Action:

* Left click

---

### Right Click

Gesture:

* Touch thumb and pinky finger
* Hold for approximately 2 seconds

Action:

* Right click

---

### Drag and Drop

Gesture:

* Touch thumb and index finger
* Hold for approximately 2 seconds

Action:

* Drag mode

Release fingers to drop.

---

### Start PowerPoint Slideshow

Gesture:

* Open palm
* Hold for approximately 2 seconds

Action:

* Press F5
* Start slideshow

---

### Next Slide

Gesture:

* Peace sign
* Point right

Action:

* Next slide

---

### Previous Slide

Gesture:

* Peace sign
* Point left

Action:

* Previous slide

---

### Close Active Window

Gesture:

* Closed fist
* Hold for approximately 2 seconds

Action:

* Alt + F4

---

## Calibration Controls

| Key | Function                   |
| --- | -------------------------- |
| W   | Move top boundary up       |
| S   | Move top boundary down     |
| A   | Reduce left/right margin   |
| D   | Increase left/right margin |
| Q   | Reduce bottom boundary     |
| E   | Increase bottom boundary   |
| ESC | Exit application           |
| X   | Exit application           |

---

## Tips

* Use good lighting
* Keep your hand inside the yellow tracking box
* Position the webcam above or below the monitor
* Supports multiple monitors

---

## Troubleshooting

### Setup Issues

Run:

```text
setup.bat
```

again.

### Camera Issues

* Check webcam connection
* Close other applications using the camera
* Select the correct camera when starting

### Missing Packages

Run:

```text
setup.bat
```

again to reinstall dependencies.
