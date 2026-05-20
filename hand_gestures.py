import cv2
import mediapipe as mp
import numpy as np


class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.8
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None  # Initialize results attribute

    def is_fist(self, landmarks):
        # Improved fist detection logic
        thumb_tip = landmarks[4]
        middle_mcp = landmarks[9]
        distance = np.hypot(thumb_tip.x - middle_mcp.x, thumb_tip.y - middle_mcp.y)
        return distance < 0.1

    def get_gesture(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_frame)  # Store results in self.results
        gesture = "none"

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
                landmarks = hand_landmarks.landmark
                if self.is_fist(landmarks):
                    gesture = "fist"
                else:
                    gesture = "open"

        cv2.putText(
            frame, f"Gesture: {gesture}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        )
        return gesture, frame
