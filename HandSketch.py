import cv2
import mediapipe as mp
import numpy as np
import os
import time
from datetime import datetime
import math

# ================= SETUP =================
SAVE_DIR = "saved_canvases"
os.makedirs(SAVE_DIR, exist_ok=True)

cap = cv2.VideoCapture(0)
cv2.namedWindow("AirCanvas", cv2.WINDOW_NORMAL)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ================= STATE =================
draw_mode = False
eraser_mode = False
brush_size = 6
color = (0, 0, 255)

canvas = None
undo_stack = []
redo_stack = []

# Stroke smoothing
points_buffer = []

# Gallery
gallery_mode = False
gallery_images = []
gallery_boxes = []

# ================= UI CONFIG =================
TOP_BAR_H = 95
BTN_W, BTN_H = 80, 32
GAP = 8

buttons_row1 = ["DRAW", "ERASE", "UNDO", "REDO", "SAVE", "CLEAR", "GALLERY"]
buttons = {}

x = 10
for name in buttons_row1:
    buttons[name] = (x, 10, x + BTN_W, 10 + BTN_H)
    x += BTN_W + GAP

# Colors (circles)
palette = [
    (0, 0, 255),
    (255, 0, 0),
    (0, 255, 0),
    (0, 255, 255),
    (255, 255, 255)
]

palette_centers = []
px = 20
for col in palette:
    palette_centers.append((px, 60, col))
    px += 40

minus_btn = (px + 20, 45, px + 60, 75)
plus_btn  = (px + 70, 45, px + 110, 75)

# ================= CLICK STATE =================
hover_item = None
hover_start = 0
HOVER_TIME = 0.6

# ================= HELPERS =================
def index_up(hand):
    return hand.landmark[8].y < hand.landmark[6].y

def is_fist(hand):
    return all(hand.landmark[t].y > hand.landmark[t-2].y for t in [8,12,16,20])

def index_middle(hand):
    return hand.landmark[8].y < hand.landmark[6].y and \
           hand.landmark[12].y < hand.landmark[10].y

def dist(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

def draw_button(img, name, rect, active=False):
    x1,y1,x2,y2 = rect
    col = (0,180,0) if active else (60,60,60)
    cv2.rectangle(img, (x1,y1), (x2,y2), col, -1)
    cv2.putText(img, name, (x1+6,y1+22),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

def smooth_draw(canvas, pts, col, size):
    if len(pts) < 3:
        return
    avg_x = int(sum(p[0] for p in pts[-3:]) / 3)
    avg_y = int(sum(p[1] for p in pts[-3:]) / 3)
    cv2.line(canvas, pts[-2], (avg_x, avg_y), col, size)

# ================= GALLERY =================
def load_gallery():
    images = []
    for f in sorted(os.listdir(SAVE_DIR)):
        if f.endswith(".png"):
            img = cv2.imread(os.path.join(SAVE_DIR, f))
            images.append((f, img))
    return images

# ================= LOOP =================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if canvas is None:
        canvas = np.zeros_like(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    frame = cv2.add(frame, canvas)

    finger = None
    active_hand = None

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            if index_up(hand):
                lm = hand.landmark[8]
                finger = (int(lm.x*w), int(lm.y*h))
                active_hand = hand
                break

    # ================= DRAW =================
    if draw_mode and finger and finger[1] > TOP_BAR_H and not gallery_mode:
        points_buffer.append(finger)
        if len(points_buffer) > 5:
            points_buffer.pop(0)
        draw_col = (0,0,0) if eraser_mode else color
        smooth_draw(canvas, points_buffer, draw_col, brush_size)
    else:
        if points_buffer:
            undo_stack.append(canvas.copy())
            redo_stack.clear()
        points_buffer.clear()

    # ================= UNDO / REDO =================
    if active_hand:
        if is_fist(active_hand) and undo_stack:
            redo_stack.append(undo_stack.pop())
            canvas = undo_stack[-1].copy() if undo_stack else np.zeros_like(canvas)

        if index_middle(active_hand) and redo_stack:
            canvas = redo_stack.pop().copy()
            undo_stack.append(canvas.copy())

    # ================= UI CLICK =================
    clicked = None
    now = time.time()

    if finger:
        fx, fy = finger

        for name,(x1,y1,x2,y2) in buttons.items():
            if x1 < fx < x2 and y1 < fy < y2:
                if hover_item != name:
                    hover_item = name
                    hover_start = now
                elif now-hover_start > HOVER_TIME:
                    clicked = name
                    hover_item = None
                break
        else:
            for cx,cy,col in palette_centers:
                if dist((fx,fy),(cx,cy)) < 15:
                    if hover_item != col:
                        hover_item = col
                        hover_start = now
                    elif now-hover_start > HOVER_TIME:
                        color = col
                        eraser_mode = False
                        hover_item = None
                    break
            else:
                if minus_btn[0] < fx < minus_btn[2] and minus_btn[1] < fy < minus_btn[3]:
                    if hover_item != "-":
                        hover_item = "-"
                        hover_start = now
                    elif now-hover_start > HOVER_TIME:
                        brush_size = max(2, brush_size-2)
                        hover_item = None

                elif plus_btn[0] < fx < plus_btn[2] and plus_btn[1] < fy < plus_btn[3]:
                    if hover_item != "+":
                        hover_item = "+"
                        hover_start = now
                    elif now-hover_start > HOVER_TIME:
                        brush_size = min(30, brush_size+2)
                        hover_item = None
                else:
                    hover_item = None

    # ================= ACTIONS =================
    if clicked:
        if clicked == "DRAW":
            draw_mode = not draw_mode
        elif clicked == "ERASE":
            eraser_mode = not eraser_mode
        elif clicked == "SAVE":
            cv2.imwrite(f"{SAVE_DIR}/canvas_{datetime.now().strftime('%H%M%S')}.png", canvas)
        elif clicked == "CLEAR":
            canvas[:] = 0
            undo_stack.clear()
            redo_stack.clear()
        elif clicked == "UNDO" and undo_stack:
            redo_stack.append(undo_stack.pop())
            canvas = undo_stack[-1].copy() if undo_stack else np.zeros_like(canvas)
        elif clicked == "REDO" and redo_stack:
            canvas = redo_stack.pop().copy()
            undo_stack.append(canvas.copy())
        elif clicked == "GALLERY":
            gallery_mode = not gallery_mode
            gallery_images = load_gallery()

    # ================= UI DRAW =================
    cv2.rectangle(frame, (0,0), (w,TOP_BAR_H), (30,30,30), -1)

    for name,rect in buttons.items():
        active = (name=="DRAW" and draw_mode) or (name=="ERASE" and eraser_mode)
        draw_button(frame, name, rect, active)

    for cx,cy,col in palette_centers:
        cv2.circle(frame, (cx,cy), 12, col, -1)
        if col == color:
            cv2.circle(frame, (cx,cy), 15, (255,255,255), 2)

    cv2.rectangle(frame, minus_btn[:2], minus_btn[2:], (80,80,80), -1)
    cv2.putText(frame, "-", (minus_btn[0]+10, minus_btn[1]+22),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.rectangle(frame, plus_btn[:2], plus_btn[2:], (80,80,80), -1)
    cv2.putText(frame, "+", (plus_btn[0]+10, plus_btn[1]+22),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.putText(frame, f"Brush {brush_size}", (w-130, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    if finger:
        cv2.circle(frame, finger, 6, color, -1)

    # ================= GALLERY OVERLAY =================
    if gallery_mode:
        overlay = frame.copy()
        cv2.rectangle(overlay, (50,110), (w-50,h-50), (0,0,0), -1)
        frame = cv2.addWeighted(overlay, 0.85, frame, 0.15, 0)

        x,y = 80,130
        for name,img in gallery_images[:6]:
            thumb = cv2.resize(img, (160,120))
            frame[y:y+120, x:x+160] = thumb
            x += 180
            if x+160 > w-80:
                x = 80
                y += 140

    cv2.imshow("AirCanvas", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
