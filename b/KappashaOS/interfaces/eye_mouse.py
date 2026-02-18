#!/usr/bin/env python3
# eye_mouse.py - Eye mouse for Blossom: gaze cursor, blink click, drag ectoplasm, lens interaction.
# Integrates with frank.py for ectoplasm drag and lens_stack.py for blind spot overlays.
# Dual License:
# - For core software: AGPL-3.0-or-later licensed. -- OliviaLynnArchive fork, 2025
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# - For hardware/embodiment interfaces (if any): Licensed under the Apache License, Version 2.0
#   with xAI amendments for safety (prohibits misuse in hashing; revocable for unethical use).
#   See http://www.apache.org/licenses/LICENSE-2.0 for details.
#
# Copyright 2025 Coneing and Contributors

import cv2
import numpy as np
import pyautogui
import time  # For blink timing
from cv2 import __version__
from core.frank import Frank  # Integrate for ectoplasm drag
from hardware.lens_stack import LensStack  # Integrate for lens interaction
import random  # For sim

# Print OpenCV version for attribution
print(f"Using OpenCV {__version__}")

class EyeMouse:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.prev_x, prev_y = 0, 0
        self.blink_start = 0
        self.blink_threshold = 0.3  # Seconds for click (short blink) vs drag (long)
        self.frank = Frank()  # Instance for ectoplasm
        self.lens = LensStack()  # Instance for blind spot stacking
        self.dragging = False
        self.drag_pos = None
        print("EyeMouse initialized - gaze cursor ready with blink click and ectoplasm drag.")
    
    def detect_blink(self, frame):
        """Detect blink: sim with eye area threshold (real: use dlib or eye aspect ratio)."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            if time.time() - self.blink_start > self.blink_threshold:
                return True  # Blink detected (long for drag)
            return False
        else:
            self.blink_start = time.time()
            return False
    
    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            # Convert frame to grayscale and apply threshold
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
            # Find contours (pupil)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
                cx, cy = int(x + w/2), int(y + h/2)
                # Smooth prediction
                if abs(cx - self.prev_x) < 10:
                    pred_x = cx + (cx - self.prev_x)
                    pred_y = cy + (cy - self.prev_y)
                else:
                    pred_x, pred_y = cx, cy
                self.prev_x, self.prev_y = cx, cy
                # Move cursor to predicted position
                pyautogui.moveTo(pred_x * 3.5, pred_y * 3.5, duration=0.05)
                # Draw ghost cursor
                cv2.circle(frame, (pred_x, pred_y), 10, (255, 0, 0), 2)
            # Blink detection for click/drag
            is_blink = self.detect_blink(frame)
            if is_blink:
                if time.time() - self.blink_start > self.blink_threshold * 2:  # Long blink for drag
                    if not self.dragging:
                        self.dragging = True
                        self.drag_pos = (pred_x, pred_y)
                        print("Long blink - start drag ectoplasm.")
                    else:
                        self.dragging = False
                        drag_end = (pred_x, pred_y)
                        self.drag_ectoplasm(self.drag_pos, drag_end)
                        print("Long blink release - end drag.")
                else:
                    pyautogui.click()
                    print("Short blink - click.")
                    self.lens_interaction("sim object")  # Interact with lens on click
            # Display frame
            cv2.imshow('Ghost Cursor', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    def drag_ectoplasm(self, start, end):
        """Drag ectoplasm: tug on Frank's trail, stack in lens."""
        proximity = math.dist(start, end) / 100.0  # Sim proximity
        self.frank.heat_tug(proximity)
        intensity = random.uniform(0, 1)
        self.frank.pain_echo(intensity)
        print(f"Dragged ectoplasm from {start} to {end}.")
    
    def lens_interaction(self, object_name):
        """Lens interaction: stack on blink/click."""
        entropy = random.uniform(0, 1)
        self.lens.stack_buffer(object_name, entropy)
        ghost = self.lens.sixth_sense_ghost()
        print("Lens interacted - ghost overlay stacked.")
    
    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()

# For standalone testing
if __name__ == "__main__":
    mouse = EyeMouse()
    mouse.run()
    mouse.close()