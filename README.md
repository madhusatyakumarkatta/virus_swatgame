# 🦠 Virus Swat - Gesture Controlled Arcade Game

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/engine-pygame--ce-green.svg)](https://pyga.me/)
[![OpenCV](https://img.shields.io/badge/vision-OpenCV-orange.svg)](https://opencv.org/)

**Virus Swat** is a high-octane, cyberpunk-themed arcade game where you defend a central system core from incoming viral infections—using nothing but your hands. This project utilizes computer vision to track your hand movements via webcam, turning real-world gestures into in-game actions.

---

## 🚀 Features

- **✋ Gesture-Based Controls:** No mouse or keyboard needed! Swat viruses with a quick swipe or deploy a digital shield with an open palm.
- **🌃 Cyberpunk Aesthetic:** Neon visuals, a techy grid background, and a "System Breached" HUD designed for a premium feel.
- **⚡ Dynamic Mechanics:**
  - **Combos:** Chain virus destructions to increase your score multiplier.
  - **Power Meter:** Charge up your energy to deploy a temporary shield.
  - **Difficulty Scaling:** Viruses become more aggressive as your score increases.
- **💥 Visual Feedback:** Screen flashes, particle explosions, and pulsing core animations.

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/madhusatyakumarkatta/virus_swatgame.git
cd virus_swatgame
```

### 2. Install Dependencies
Make sure you have Python installed. Then, install the required libraries:
```bash
pip install -r requirements.txt
```

### 3. Run the Game
```bash
python main.py
```

---

## 🎮 How to Play

### Controls
| Action | Gesture |
| :--- | :--- |
| **Start/Restart** | Perform a fast swipe across the screen |
| **Attack** | Swipe through a virus to destroy it |
| **Shield** | Hold your **palm open** when the power meter (bottom purple bar) is full |
| **Exit** | Press `ESC` on your keyboard |

### Objectives
1. **Protect the Core:** Don't let viruses reach the central blue pulsing core.
2. **Score High:** Each virus destroyed adds to your score. Keep the streak alive for combos!
3. **Manage Health:** If the core takes too much damage, the system is breached.

---

## 📂 Project Structure

- `main.py`: The entry point that orchestrates hand tracking, logic, and rendering.
- `game_logic.py`: Handles virus spawning, collision detection, and score management.
- `hand_tracking.py`: Leverages OpenCV for real-time hand and finger detection.
- `gesture_detection.py`: Processes hand coordinates to detect swipes and palm states.
- `ui.py`: Manages the cyberpunk HUD, start screen, and game-over menus.
- `virus.py`: Contains the logic and movement patterns for different virus types.

---

## 🔧 Technologies Used

- **[Python](https://www.python.org/):** Core programming language.
- **[OpenCV](https://opencv.org/):** Real-time computer vision for hand tracking.
- **[Pygame-ce](https://pyga.me/):** High-performance game engine for logic and rendering.
- **[NumPy](https://numpy.org/):** Efficient numerical computations for trajectory and distance logic.

---

## 📜 License
This project is open-source. Feel free to modify and build upon it!

---
*Created as part of a Semester 1 Project.*
