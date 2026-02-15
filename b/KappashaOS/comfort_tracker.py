# Born free, feel good, have fun.

# Dual License:
# - For core software: AGPL-3.0-or-later licensed. -- xAI fork, 2025
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# Copyright 2025 xAI

# xAI Amendments for Physical Use:
# 1. Physical Embodiment Restrictions: Use with devices is for non-hazardous purposes only. Harmful mods are prohibited, with license revocable by xAI.
# 2. Ergonomic Compliance: Limits tendon load to 20%, gaze to 30 seconds (ISO 9241-5).
# 3. Safety Monitoring: Real-time tendon/gaze checks, logged for audit.
# 4. Revocability: xAI may revoke for unethical use (e.g., surveillance).
# 5. Export Controls: Sensor devices comply with US EAR Category 5 Part 2.
# 6. Open Development: Hardware docs shared post-private phase via github.com/tetrasurfaces/issues.
# 7. No machine code output (e.g., kappa paths, hashlet sequences) without breath consent; decay signals at 11 hours (8 for bumps).
# 8. Color Consent: No signal may change hue without explicit user intent (e.g., heartbeat sync or verbal confirmation).
# 9. Intellectual Property: xAI owns all IP related to KappaOpticBatterySystem, including chatter patterns, stacked ports, moving keys, smart cables, RGB hexel lattices, chattered housings, fliphooks, hash tunneling, and IPFS integration. No unauthorized replication.

# Private Development Note: This repository is private for xAI’s KappashaOS and Navi development. Access is restricted. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) post-phase.

#!/usr/bin/env python3

# comfort_tracker.py
# From Olivia's pain map — flipped to comfort
# AGPL3.0 and above OliviaLynnArchive Fork 2026.
import cv2
import numpy as np
import time
import os

try:
    import mediapipe as mp
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("MediaPipe not found — mock keypoints only.")

class ComfortTracker:
    def __init__(self, save_dir="./vintage/comfort"):
        self.body_map = np.zeros((480, 640, 3), dtype=np.uint8)
        self.body_map[:] = (0, 200, 0)  # calm green
        self.comfort_level = 100.0
        self.last_breathe = time.time()
        self.frame_count = 0
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)
        print("Comfort tracker awake — green only.")
        if MEDIAPIPE_AVAILABLE:
            self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
            print("MediaPipe Pose ready.")
        else:
            print("Using mock keypoints.")

    def update_from_pose(self, frame=None):
        keypoints = []
        if MEDIAPIPE_AVAILABLE and frame is not None:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame_rgb)
            if results.pose_landmarks:
                for idx, lm in enumerate(results.pose_landmarks.landmark):
                    if lm.visibility > 0.6:  # higher confidence
                        x, y = int(lm.x * 640), int(lm.y * 480)
                        keypoints.append(type('kp', (), {'x': lm.x, 'y': lm.y, 'confidence': lm.visibility}))
                        cv2.circle(self.body_map, (x, y), 12, (0, 255, 100), -1)  # bright mint
                        # Draw connections too if wanted
                        # mp_drawing.draw_landmarks(self.body_map, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        else:
            # Mock some movement
            if random.random() < 0.3:
                x, y = random.randint(100, 540), random.randint(100, 380)
                cv2.circle(self.body_map, (x, y), 20, (0, 255, 0), -1)

        # Comfort rises with detected keypoints / movement
        detected = len(keypoints)
        self.comfort_level = min(100.0, self.comfort_level + detected * 0.4)
        if self.comfort_level < 92.0:
            print("Comfort dip — dojo breath reset.")
            self.comfort_level = 95.0

    def draw(self):
        cv2.putText(self.body_map, f"Comfort: {self.comfort_level:.1f}/100", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Save frame every 10
        if self.frame_count % 10 == 0:
            ts = time.strftime("%Y%m%d_%H%M%S")
            path = f"{self.save_dir}/comfort_{ts}.png"
            cv2.imwrite(path, self.body_map)
            print(f"Comfort map saved: {path}")
        
        # Show if display available
        try:
            cv2.imshow("Comfort Map", self.body_map)
            cv2.waitKey(1)
        except:
            pass  # headless ok
        
        self.frame_count += 1

    def breathe(self):
        now = time.time()
        if now - self.last_breathe > 60:
            delta = min(5.0, (now - self.last_breathe) / 60.0)  # scale with time
            self.comfort_level = min(100.0, self.comfort_level + delta)
            self.last_breathe = now
            print(f"Breath taken — comfort +{delta:.1f} → {self.comfort_level:.1f}")

    def get_comfort(self):
        return self.comfort_level

if __name__ == "__main__":
    tracker = ComfortTracker()
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        tracker.update_from_pose(frame)
        tracker.draw()
        tracker.breathe()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()