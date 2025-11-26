# ✋ Finger Counter using OpenCV & MediaPipe

This project uses **OpenCV** and **MediaPipe** to detect hands in real time and accurately count raised fingers, including the thumb. It includes improved logic for both **right and left hands** and displays the result on the screen.

## 🚀 Features
- Accurate thumb + finger detection  
- Supports both Left and Right hands  
- Real-time camera feed with smooth tracking  
- Displays finger count per hand and total  
- Works with any webcam  

## 🛠️ Technologies Used
- Python  
- OpenCV  
- MediaPipe  

## 📦 Installation
Install Python packages:
```bash
pip install opencv-python mediapipe
```

## ▶️ How to Run
Run the script using:
```bash
python finger_counter.py
```
Press **q** to close the window.

## 🧠 How It Works

### Landmark System
MediaPipe provides **21 hand landmarks**.  
Finger tips have fixed IDs:
- Thumb → 4  
- Index → 8  
- Middle → 12  
- Ring → 16  
- Little → 20  

### Finger Detection Logic
- For normal fingers (index to little):  
  A finger is considered **raised** when its **tip landmark is above the joint landmark** (tip_y < pip_y).

- For the **thumb**, the horizontal direction is used:
  - **Right Hand:** thumb is up if tip_x > joint_x  
  - **Left Hand:** thumb is up if tip_x < joint_x  

This ensures accurate detection on both hands.

## 🎯 Output
- Displays total raised fingers  
- Displays per-hand finger count (Right / Left)  
- Live video feed with hand landmarks drawn  

## 📄 License
Free to use, modify, and learn from.
