# ✋🎨 HandSketch

**HandSketch** is a real-time, gesture-based drawing application that enables users to create digital artwork using only hand gestures captured through a webcam. By eliminating the need for traditional input devices such as a mouse, keyboard, or touchscreen, HandSketch provides a fully touchless and intuitive drawing experience powered by Computer Vision.

The project uses advanced hand-tracking techniques to recognize finger movements and gestures, translating them into smooth, precise strokes on a virtual canvas. HandSketch focuses on natural human–computer interaction, making it suitable for creative applications, accessibility-focused systems, and educational demonstrations of real-time vision-based interaction.

---

## 🚀 Key Features

### ✍️ Gesture-Based Drawing

* Draw by raising the index finger
* Automatically stops drawing when the palm is open
* Supports drawing with **either hand**

### 🎨 Drawing Tools & Controls

* Multiple color selection using on-screen color circles
* Adjustable brush size via UI controls
* Eraser tool for precise corrections
* Smooth stroke rendering using interpolation and filtering

### 🖐️ Gesture-Driven Interaction

* On-screen buttons activated through hand gestures
* No mouse or keyboard input required
* Gesture-based undo and redo functionality
* Dedicated draw-mode toggle to enable or disable drawing

### 💾 Canvas Management

* Save drawings without closing the webcam feed
* Automatically stores canvases in a local gallery
* Open and view previously saved drawings inside the application

### 🖥️ User Experience

* Real-time hand skeleton visualization
* Stable and optimized finger detection
* Resizable application window with user-controlled fullscreen option
* Minimal UI that does not obstruct the drawing area

---

## 🛠️ Technologies Used

* **Python** – core application logic
* **OpenCV** – webcam access, rendering, and image processing
* **MediaPipe Hands** – real-time hand landmark detection
* **NumPy** – canvas operations and numerical processing

---

## 📁 Project Structure

```
HandSketch/
├── HandSketch.py
├── requirements.txt
├── README.md
└── saved_canvases/
    ├── canvas_101530.png
    ├── canvas_102145.png
    └── ...
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/dhriti16sharma/HandSketch.git
cd HandSketch
```

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

```bash
python HandSketch.py
```

Ensure that:

* A webcam is connected and accessible
* Adequate lighting is available for accurate hand detection

---

## 🧠 How HandSketch Works

HandSketch utilizes MediaPipe’s real-time hand tracking model to detect 21 hand landmarks per hand from the webcam feed. The position of the index finger tip is mapped onto a virtual canvas to create drawing strokes. Gesture logic determines whether the user is drawing, interacting with UI elements, erasing, or navigating the gallery.

To improve usability, stroke smoothing algorithms are applied to reduce jitter and create fluid, natural-looking lines. All UI interactions are processed directly within the video feed, enabling a fully immersive touchless experience.

---

## 🎯 Applications & Use Cases

* Touchless drawing and creative tools
* Human–Computer Interaction (HCI) demonstrations
* Computer Vision learning and experimentation
* Accessibility-friendly interfaces
* Academic projects, hackathons, and portfolio showcases

---

## 📜 License

This project is licensed under the **MIT License**, allowing free use, modification, and distribution with proper attribution.

---

## 🙌 Acknowledgements

* **MediaPipe** by Google for real-time hand tracking
* **OpenCV** community for computer vision tools

---

## ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub!

---
