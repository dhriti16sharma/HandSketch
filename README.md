# ✋ HandSktech — Gesture-Based Drawing Application

HandSktech is a real-time **gesture-controlled drawing application** built using **Computer Vision** and **MediaPipe Hands**.  
It allows users to draw, erase, change colors, adjust brush size, undo/redo strokes, and manage saved canvases — **all without using a mouse or keyboard**.

The entire interaction happens through **hand gestures detected via webcam**.


## 🚀 Features

### ✍️ Drawing & Interaction
- Draw in the air using your **index finger**
- Smooth stroke rendering (jitter-free drawing)
- Toggle **Draw Mode** on/off
- Eraser mode (true canvas erase)

### 🎨 Color & Brush Controls
- Gesture-based color selection using **color circles**
- Adjustable brush size (`+ / -`)
- Active color and brush size indicators

### ↩️ Undo / Redo
- **Undo** using fist gesture ✊
- **Redo** using index + middle finger ✌️

### 💾 Canvas Management
- Save drawings as images
- Clear canvas instantly
- **In-app gallery** to view and load saved canvases
- No webcam interruption while saving/loading

### 🖐️ Gesture-Only UI
- No mouse
- No keyboard
- No hand restrictions (any hand can perform any action)
- Button clicks via **hover (dwell)** interaction

### 🪟 User-Friendly Window
- Starts in **normal window mode**
- User can resize or fullscreen manually


## 🧠 Gesture Guide

| Action | Gesture |
|------|--------|
| Draw | Index finger up |
| Stop drawing | Relax hand |
| Click buttons | Hover index finger over UI |
| Undo | Fist ✊ |
| Redo | Index + Middle ✌️ |
| Erase | Toggle Erase button |
| Change color | Hover over color circle |
| Brush size | Hover on + / − |


## 🛠️ Tech Stack
- **Python**
- **OpenCV** – video capture & rendering
- **MediaPipe Hands** – real-time hand landmark detection
- **NumPy** – canvas operations


## 📁 Project Structure
HandSktech/
├── HandSktech.py
├── requirements.txt
├── README.md
└── saved_canvases/
├── canvas_101530.png
├── canvas_102145.png
└── ...


## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
git clone 
cd HandSketch

### 2️⃣ Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate   # Windows


### 3️⃣ Install dependencies
pip install -r requirements.txt

### 4️⃣ Run the application
python HandSketch.py


## 📷 System Requirements

* Webcam (built-in or external)
* Python **3.10 – 3.11** (recommended)
* Good lighting for accurate hand detection


## 🧪 Tips for Best Performance

* Keep your hand **30–60 cm** from the camera
* Avoid strong backlight
* Use clear, slow gestures near UI buttons
* Keep fingers clearly visible to the camera


## 🌟 Use Cases

* Touchless drawing & whiteboarding
* Gesture-based UI experiments
* Computer Vision learning projects
* Interactive presentations
* Accessibility-focused interfaces


## 📌 Future Enhancements

* Pressure-based brush thickness
* Gesture tutorial overlay
* Multi-user canvas
* Export drawing as video
* AI-based gesture correction

## 👩‍💻 Author

**Dhriti Sharma**
B.Tech CSE | AI & Full-Stack Enthusiast
UI/UX Designer | Computer Vision Developer


## ⭐ Show Your Support

If you like this project:

* ⭐ Star the repository
* 🍴 Fork it
* 📢 Share it

Happy Air Drawing! ✨✋

