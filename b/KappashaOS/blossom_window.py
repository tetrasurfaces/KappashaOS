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
#
# - For hardware/embodiment interfaces: Licensed under the Apache License, Version 2.0
# with xAI amendments for safety and physical use. See http://www.apache.org/licenses/LICENSE-2.0
# for details, with the following xAI-specific terms appended.

# Copyright 2025 xAI

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# SPDX-License-Identifier: Apache-2.0

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

# blossom_window.py
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPalette
from rhombus_voxel import RhombusVoxel

class BlossomWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.WindowStaysOnTopHint | 
                            Qt.WindowType.Tool)  # stronger topmost
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)  # no focus steal
        self.resize(320, 220)  # slightly bigger
        self.move(20, 20)  # top-left corner
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        self.pulse = QLabel("Ara")
        self.pulse.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pulse.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.pulse.setStyleSheet("color: #c8a2c8; background: rgba(0,0,0,0.1); border-radius: 15px;")
        self.pulse.setFixedHeight(70)
        self.trail = QLabel("🌱")
        self.trail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.trail.setFont(QFont("Segoe UI", 48))
        self.trail.setStyleSheet("color: #90ee90; background: transparent;")
        layout.addWidget(self.pulse)
        layout.addWidget(self.trail, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        # Stronger pulse animation
        self.anim = QPropertyAnimation(self.pulse, b"windowOpacity")
        self.anim.setDuration(1800)
        self.anim.setStartValue(0.4)
        self.anim.setEndValue(1.0)
        self.anim.setLoopCount(-1)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.anim.start()
        # Breath timer
        self.breath = QTimer()
        self.breath.timeout.connect(self.inhale)
        self.breath.start(3500)  # faster breath
        self.state = "quiet"
        # Create & expose voxel grid
        self.voxel = RhombusVoxel(grid_size=10, kappa=0.10, rhombus_angle=60)
        print("Blossom: voxel grid born — 10³ rhombus, kappa 0.10")

    def inhale(self):
        if self.state == "quiet":
            self.trail.setText("🌱")
        elif self.state == "regret":
            self.trail.setText("💔")
            self.state = "quiet"
        self.pulse.setStyleSheet("color: #c8a2c8;")  # back to violet

    def warn(self, msg):
        self.pulse.setText(msg[:12])
        self.pulse.setStyleSheet("color: #ff6b6b;")
        self.state = "warning"
        self.trail.setText("⚠️")
        QTimer.singleShot(3000, self.inhale)

    def regret(self):
        self.state = "regret"
        self.trail.setText("💔")
        self.pulse.setText("...gone.")
        self.pulse.setStyleSheet("color: #a29bfe;")
        QTimer.singleShot(8000, self.inhale)

    def say(self, text):
        self.pulse.setText(text[:15])
        self.trail.setText("💬")
        QTimer.singleShot(5000, self.inhale)

    def closeEvent(self, event):
        event.ignore()  # can't close. she stays.

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlossomWindow()
    window.show()
    sys.exit(app.exec())