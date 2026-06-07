import tkinter as tk
import cv2
import pyautogui
import math
import subprocess
import os
from cvzone.HandTrackingModule import HandDetector
from screeninfo import get_monitors

# =====================================================
# CAMERA SELECTION
# =====================================================

selected_camera = None

def choose_camera(cam_id):
    global selected_camera
    selected_camera = cam_id
    root.destroy()

available_cameras = []

for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        available_cameras.append(i)
    cap.release()

root = tk.Tk()
root.title("Select Camera")
root.geometry("300x250")

tk.Label(
    root,
    text="Choose Camera",
    font=("Arial", 14)
).pack(pady=10)

for cam in available_cameras:
    tk.Button(
        root,
        text=f"Camera {cam}",
        command=lambda c=cam: choose_camera(c),
        width=20
    ).pack(pady=5)

root.mainloop()

if selected_camera is None:
    raise SystemExit

# =====================================================
# MULTI MONITOR DESKTOP
# =====================================================

monitors = get_monitors()

desktop_left = min(m.x for m in monitors)
desktop_top = min(m.y for m in monitors)

desktop_right = max(m.x + m.width for m in monitors)
desktop_bottom = max(m.y + m.height for m in monitors)

desktop_width = desktop_right - desktop_left
desktop_height = desktop_bottom - desktop_top

print(
    f"Desktop: {desktop_width} x {desktop_height}"
)

# =====================================================
# HAND TRACKING
# =====================================================

cap = cv2.VideoCapture(selected_camera)
cv2.namedWindow("WallTouch v6", cv2.WINDOW_NORMAL)

detector = HandDetector(
    staticMode=False,
    maxHands=2,
    detectionCon=0.7,
    minTrackCon=0.5
)

pyautogui.FAILSAFE = False

FRAME_MARGIN_LEFT_RIGHT = 40
FRAME_MARGIN_TOP = 30
FRAME_MARGIN_BOTTOM = 20
PREVIEW_SCALE = 1.5

CLICK_HOLD_FRAMES = 8
DRAG_HOLD_FRAMES = 12
DRAG_MOVE_THRESHOLD = 15
DRAG_2SEC_FRAMES = 60
RIGHT_CLICK_HOLD_FRAMES = 60

cursor_x = None
cursor_y = None

SMOOTHING = 0.35

left_click_latch = False
right_click_latch = False
right_click_active = False
right_click_start_frame = 0

dragging = False
thumb_index_active = False
thumb_index_start_frame = 0
frame_count = 0

last_peace_x = None
swipe_cooldown = 0

# NEW GESTURES STATE TRACKING
open_palm_active = False
open_palm_start_frame = 0
open_palm_latch = False

fist_active = False
fist_start_frame = 0
fist_latch = False

GEST_2SEC_FRAMES = 60  # Frames for 2 seconds at ~30fps
gesture_hold_active = False

# =====================================================
# MAIN LOOP
# =====================================================

while True:

    success, img = cap.read()

    if not success:
        break

    # Webcam above screen -> keep mirrored
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    h, w, _ = img.shape

    status = "WAIT"

    # =================================================
    # VIRTUAL SCREEN BORDER
    # =================================================

    cv2.rectangle(
        img,
        (FRAME_MARGIN_LEFT_RIGHT, FRAME_MARGIN_TOP),
        (w - FRAME_MARGIN_LEFT_RIGHT, h - FRAME_MARGIN_BOTTOM),
        (255, 255, 0),
        2
    )

    cv2.putText(
        img,
        "TOP LEFT",
        (FRAME_MARGIN_LEFT_RIGHT, FRAME_MARGIN_TOP - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 0),
        1
    )

    cv2.putText(
        img,
        "TOP RIGHT",
        (w - FRAME_MARGIN_LEFT_RIGHT - 90, FRAME_MARGIN_TOP - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 0),
        1
    )

    cv2.putText(
        img,
        "BOTTOM LEFT",
        (FRAME_MARGIN_LEFT_RIGHT, h - FRAME_MARGIN_BOTTOM + 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 0),
        1
    )

    cv2.putText(
        img,
        "BOTTOM RIGHT",
        (w - FRAME_MARGIN_LEFT_RIGHT - 120, h - FRAME_MARGIN_BOTTOM + 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 0),
        1
    )

    # =================================================
    # HAND DETECTED
    # =================================================

    if hands:

        hand = hands[0]

        lm = hand["lmList"]
        fingers = detector.fingersUp(hand)

        thumb = lm[4]
        index = lm[8]
        middle = lm[12]
        pinky = lm[20]

        x = index[0]
        y = index[1]

        x = max(FRAME_MARGIN_LEFT_RIGHT, min(x, w - FRAME_MARGIN_LEFT_RIGHT))
        y = max(FRAME_MARGIN_TOP, min(y, h - FRAME_MARGIN_BOTTOM))

        mouse_x = int(
            ((x - FRAME_MARGIN_LEFT_RIGHT) /
             (w - FRAME_MARGIN_LEFT_RIGHT * 2))
            * desktop_width
        ) + desktop_left

        mouse_y = int(
            ((y - FRAME_MARGIN_TOP) /
             (h - FRAME_MARGIN_TOP - FRAME_MARGIN_BOTTOM))
            * desktop_height
        ) + desktop_top

        # =============================================
        # GESTURES
        # =============================================

        pointing = (
            fingers[1] == 1 and
            fingers[2] == 0 and
            fingers[3] == 0 and
            fingers[4] == 0
        )

        peace_sign = (
            fingers[1] == 1 and
            fingers[2] == 1 and
            fingers[3] == 0 and
            fingers[4] == 0
        )

        # OPEN PALM: all fingers up
        open_palm = (
            fingers[0] == 1 and
            fingers[1] == 1 and
            fingers[2] == 1 and
            fingers[3] == 1 and
            fingers[4] == 1
        )

        # FIST: all fingers down (closed hand)
        fist = (
            fingers[0] == 0 and
            fingers[1] == 0 and
            fingers[2] == 0 and
            fingers[3] == 0 and
            fingers[4] == 0
        )

        cursor_color = (0, 0, 255)

        # =============================================
        # OPEN PALM GESTURE (F5 - PowerPoint Slideshow)
        # =============================================

        if open_palm:
            if not open_palm_active:
                open_palm_active = True
                open_palm_start_frame = frame_count
                open_palm_latch = False

            duration = frame_count - open_palm_start_frame

            if duration >= GEST_2SEC_FRAMES and not open_palm_latch:
                pyautogui.press("f5")
                open_palm_latch = True
                gesture_hold_active = True
                status = "OPEN PALM - F5 PRESSED"
                cursor_color = (255, 255, 0)
            elif duration >= GEST_2SEC_FRAMES:
                status = "OPEN PALM - F5 ACTIVE"
                cursor_color = (255, 255, 0)
                gesture_hold_active = True
            else:
                status = f"OPEN PALM {duration}/{GEST_2SEC_FRAMES}"
                cursor_color = (255, 200, 0)
                gesture_hold_active = False
        else:
            if open_palm_active:
                open_palm_active = False
                open_palm_latch = False
                gesture_hold_active = False

        # =============================================
        # FIST GESTURE (Alt+F4 - Close Window)
        # =============================================

        if fist:
            if not fist_active:
                fist_active = True
                fist_start_frame = frame_count
                fist_latch = False

            duration = frame_count - fist_start_frame

            if duration >= GEST_2SEC_FRAMES and not fist_latch:
                pyautogui.hotkey("alt", "F4")
                fist_latch = True
                gesture_hold_active = True
                status = "FIST - WINDOW CLOSED"
                cursor_color = (0, 0, 200)
            elif duration >= GEST_2SEC_FRAMES:
                status = "FIST - CLOSING"
                cursor_color = (0, 0, 200)
                gesture_hold_active = True
            else:
                status = f"FIST {duration}/{GEST_2SEC_FRAMES}"
                cursor_color = (100, 100, 150)
                gesture_hold_active = False
        else:
            if fist_active:
                fist_active = False
                fist_latch = False
                gesture_hold_active = False

        # =============================================
        # CURSOR MOVE
        # =============================================

        if pointing and not gesture_hold_active:

            status = "MOVE"
            cursor_color = (0, 255, 0)

            if cursor_x is None:
                cursor_x = mouse_x
                cursor_y = mouse_y
            else:
                cursor_x += (
                    mouse_x - cursor_x
                ) * SMOOTHING

                cursor_y += (
                    mouse_y - cursor_y
                ) * SMOOTHING

            pyautogui.moveTo(
                int(cursor_x),
                int(cursor_y)
            )

        thumb_index_distance = math.hypot(
            thumb[0] - index[0],
            thumb[1] - index[1]
        )

        thumb_pinky_distance = math.hypot(
            thumb[0] - pinky[0],
            thumb[1] - pinky[1]
        )

        # =============================================
        # THUMB + INDEX: LEFT CLICK or DRAG MODE
        # =============================================

        if thumb_index_distance < 40 and not gesture_hold_active:
            if not thumb_index_active:
                thumb_index_active = True
                thumb_index_start_frame = frame_count

            duration = frame_count - thumb_index_start_frame

            if duration > DRAG_2SEC_FRAMES and not dragging:
                pyautogui.mouseDown()
                dragging = True
                status = "DRAG MODE"
                cursor_color = (0, 255, 255)
            
            if dragging:
                status = "DRAG MODE"
                cursor_color = (0, 255, 255)
                pyautogui.moveTo(int(mouse_x), int(mouse_y))
        else:
            if thumb_index_active:
                duration = frame_count - thumb_index_start_frame
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False
                    status = "DROP"
                elif duration <= CLICK_HOLD_FRAMES:
                    status = "LEFT CLICK"
                    cursor_color = (0, 255, 255)
                    pyautogui.click()
                thumb_index_active = False

        # =============================================
        # THUMB + PINKY: RIGHT CLICK
        # =============================================

        if not peace_sign and thumb_pinky_distance < 40 and not gesture_hold_active:
            if not right_click_active:
                right_click_active = True
                right_click_start_frame = frame_count

            duration = frame_count - right_click_start_frame

            status = "RIGHT CLICK"
            cursor_color = (255, 0, 0)

            if duration >= RIGHT_CLICK_HOLD_FRAMES and not right_click_latch:
                pyautogui.rightClick()
                right_click_latch = True
        else:
            right_click_active = False
            right_click_latch = False

        # =============================================
        # POWERPOINT MODE (PEACE SIGN + POINT DIRECTION)
        # =============================================

        if swipe_cooldown > 0:
            swipe_cooldown -= 1

        if peace_sign:

            cursor_color = (255, 0, 255)
            status = "PRESENTATION"

            # Index finger base and tip
            index_base = lm[5]
            index_tip = lm[8]

            direction_x = index_tip[0] - index_base[0]

            # Pointing RIGHT
            if direction_x > 40 and swipe_cooldown == 0:
                pyautogui.press("right")
                status = "NEXT SLIDE"
                swipe_cooldown = 30

            # Pointing LEFT
            elif direction_x < -40 and swipe_cooldown == 0:
                pyautogui.press("left")
                status = "PREVIOUS SLIDE"
                swipe_cooldown = 30

        # =============================================
        # VISUAL MARKER
        # =============================================

        cv2.circle(
            img,
            (x, y),
            12,
            cursor_color,
            cv2.FILLED
        )

        cv2.line(
            img,
            (x - 20, y),
            (x + 20, y),
            cursor_color,
            2
        )

        cv2.line(
            img,
            (x, y - 20),
            (x, y + 20),
            cursor_color,
            2
        )

    cv2.putText(
        img,
        f"Top:{FRAME_MARGIN_TOP} Bottom:{FRAME_MARGIN_BOTTOM} LR:{FRAME_MARGIN_LEFT_RIGHT}",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        img,
        "W/S top  A/D sides  Q/E bottom",
        (20, h - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1
    )

    cv2.putText(
        img,
        status,
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )

    preview_img = cv2.resize(
        img,
        (int(w * PREVIEW_SCALE), int(h * PREVIEW_SCALE)),
        interpolation=cv2.INTER_LINEAR
    )

    cv2.imshow(
        "WallTouch v6",
        preview_img
    )

    if cv2.getWindowProperty("WallTouch v6", cv2.WND_PROP_VISIBLE) < 1:
        status = "CLOSING..."
        cv2.putText(
            img,
            status,
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )
        preview_img = cv2.resize(
            img,
            (int(w * PREVIEW_SCALE), int(h * PREVIEW_SCALE)),
            interpolation=cv2.INTER_LINEAR
        )
        cv2.imshow(
            "WallTouch v6",
            preview_img
        )
        cv2.waitKey(500)
        break

    key = cv2.waitKey(1)

    if key == ord("w"):
        FRAME_MARGIN_TOP = max(0, FRAME_MARGIN_TOP - 5)
    elif key == ord("s"):
        FRAME_MARGIN_TOP = min(int(h * 0.45), FRAME_MARGIN_TOP + 5)
    elif key == ord("q"):
        FRAME_MARGIN_BOTTOM = max(0, FRAME_MARGIN_BOTTOM - 5)
    elif key == ord("e"):
        FRAME_MARGIN_BOTTOM = min(int(h * 0.45), FRAME_MARGIN_BOTTOM + 5)
    elif key == ord("a"):
        FRAME_MARGIN_LEFT_RIGHT = max(0, FRAME_MARGIN_LEFT_RIGHT - 5)
    elif key == ord("d"):
        FRAME_MARGIN_LEFT_RIGHT = min(int(w * 0.45), FRAME_MARGIN_LEFT_RIGHT + 5)
    elif key == 27 or key == ord("x"):
        break

    frame_count += 1

cap.release()
cv2.destroyAllWindows()