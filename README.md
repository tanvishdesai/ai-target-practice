# AI Target Practice (Hand Gesture Controlled)

An interactive, AI-powered target shooting game built with Python, PyGame, and OpenCV. This project uses computer vision to track your hand gestures via webcam, allowing you to aim and shoot targets simply by pointing and clenching your fist!

## How It Works

- **Computer Vision**: Uses `cv2` and a custom `HandDetector` (likely powered by MediaPipe) to track hand landmarks in real-time.
- **Aiming**: The angle of your index finger relative to the center of the screen dictates the trajectory of your bullets. A debug trajectory line is drawn to help you aim.
- **Shooting**: Making a "fist" gesture for a brief moment triggers a shot, consuming ammo.
- **Game Mechanics**: Targets spawn in clusters and move. Hitting a target triggers an explosion and increases your score. If a target escapes, you lose a life.

## Key Features

- Real-time webcam integration for interactive gameplay.
- Advanced hand gesture recognition (`fist` to shoot, index finger to aim).
- PyGame-powered rendering engine with sprites, collision detection, and sound effects.
- Dynamic difficulty with target cluster spawning and ammo constraints.

## Setup Instructions

1. Ensure you have Python installed.
2. Install the required dependencies (PyGame, OpenCV, MediaPipe):
   ```bash
   pip install pygame opencv-python mediapipe
   ```
3. Run the game:
   ```bash
   python main.py
   ```
4. Stand in front of your webcam, point with your index finger to aim, and make a fist to shoot! Press 'R' to restart if you lose.
