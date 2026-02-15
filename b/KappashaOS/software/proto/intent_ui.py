#!/usr/bin/env python3
# Copyright 2025 xAI
# Dual License:
# - For core software: AGPL-3.0-or-later licensed. -- xAI fork, 2025
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
# - For hardware/embodiment interfaces: Licensed under the Apache License, Version 2.0
#   with xAI amendments for safety and physical use (prohibits misuse in weapons or hazardous applications;
#   requires ergonomic compliance; revocable for unethical use). See http://www.apache.org/licenses/LICENSE-2.0
#   for details, with the following xAI-specific terms appended.
#
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
# SPDX-License-Identifier: (AGPL-3.0-or-later) AND Apache-2.0
#
# xAI Amendments for Physical Use:
# 1. Physical Embodiment Restrictions: Use with devices is for non-hazardous purposes only. Harmful mods are prohibited, with license revocable by xAI.
# 2. Ergonomic Compliance: Limits tendon load to 20%, gaze to 30 seconds (ISO 9241-5).
# 3. Safety Monitoring: Real-time tendon/gaze checks, logged for audit.
# 4. Revocability: xAI may revoke for unethical use (e.g., surveillance).
# 5. Export Controls: Sensor devices comply with US EAR Category 5 Part 2.
# 6. Open Development: Hardware docs shared post-private phase.
#
# Private Development Note: This repository is private for xAI’s KappashaOS and Navi development. Access is restricted. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) post-phase.
#
# SPDX-License-Identifier: (AGPL-3.0-or-later) AND Apache-2.0

import json
import os
from datetime import datetime
import asyncio
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QComboBox, QPushButton, QLabel, QTextEdit, QDesktopServices
from PySide6.QtCore import Qt, QUrl
from proto.revocation_stub import check_revocation

class IntentUI(QMainWindow):
    def __init__(self, device_hash="intent_ui_001"):
        super().__init__()
        self.device_hash = device_hash
        self.init_ui()
        self.check_revocation_status()

    def init_ui(self):
        """Set up the PySide UI for intent setting and log display."""
        self.setWindowTitle("KappashaOS Intent Manager")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
            QMainWindow { background-color: #1a1a1a; color: #00ff00; }
            QLabel { color: #00ff00; font-family: Monospace; }
            QComboBox { background-color: #333; color: #00ff00; border: 1px solid #00ff00; }
            QPushButton { background-color: #333; color: #00ff00; border: 1px solid #00ff00; }
            QPushButton:hover { background-color: #00ff00; color: #1a1a1a; }
            QTextEdit { background-color: #222; color: #00ff00; border: 1px solid #00ff00; font-family: Monospace; }
        """)

        # Layout
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Intent selection
        self.intent_label = QLabel("Select Intent:")
        layout.addWidget(self.intent_label)
        self.intent_combo = QComboBox()
        self.intent_combo.addItems(["educational", "commercial"])
        layout.addWidget(self.intent_combo)

        # Save button
        self.save_button = QPushButton("Save Intent")
        self.save_button.clicked.connect(self.save_intent)
        layout.addWidget(self.save_button)

        # Revocation status
        self.revocation_label = QLabel("Revocation Status: Checking...")
        layout.addWidget(self.revocation_label)

        # Log display
        self.log_label = QLabel("Recent License Logs:")
        layout.addWidget(self.log_label)
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)

        # GitHub issues link
        self.github_button = QPushButton("Open Licensing Issues (GitHub)")
        self.github_button.clicked.connect(self.open_github)
        layout.addWidget(self.github_button)

        # Load current intent
        self.load_intent()

    def load_intent(self):
        """Load current intent from config.json."""
        try:
            intent, commercial_use = self.read_config()
            if intent in ["educational", "commercial"]:
                self.intent_combo.setCurrentText(intent)
        except Exception as e:
            self.log_display.append(f"Error loading intent: {e}")

    def read_config(self, config_file="config/config.json"):
        """Read intent and commercial use from config file."""
        config_dir = os.path.dirname(config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        if not os.path.exists(config_file):
            print(f"Config file {config_file} not found. Creating default.")
            self.write_config("none", False, config_file)
            return None, False
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
            intent = config.get("intent")
            commercial_use = config.get("commercial_use", False)
            if intent not in ["educational", "commercial", "none"]:
                raise ValueError("Invalid intent in config.")
            return intent, commercial_use
        except json.JSONDecodeError:
            print(f"Error: {config_file} contains invalid JSON. Resetting to default.")
            self.write_config("none", False, config_file)
            return None, False
        except Exception as e:
            print(f"Error reading {config_file}: {e}. Resetting to default.")
            self.write_config("none", False, config_file)
            return None, False

    def write_config(self, intent, commercial_use, config_file="config/config.json"):
        """Write intent and commercial use to config file."""
        config = {"intent": intent, "commercial_use": commercial_use}
        config_dir = os.path.dirname(config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        try:
            with open(config_file, "w") as f:
                json.dump(config, f, indent=4)
            self.log_display.append(f"[{datetime.now()}] Intent saved: {intent}")
        except Exception as e:
            self.log_display.append(f"Error writing to {config_file}: {e}")

    def log_license_check(self, result, intent, commercial_use):
        """Log license and revocation check results."""
        try:
            with open("license_log.txt", "a") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] License Check: {result}, Intent: {intent}, Commercial: {commercial_use}\n")
            self.log_display.append(f"[{timestamp}] {result}")
        except Exception as e:
            self.log_display.append(f"Error logging: {e}")

    async def check_revocation_async(self):
        """Check revocation status asynchronously."""
        if check_revocation(self.device_hash):
            self.revocation_label.setText("Revocation Status: Device Revoked")
            self.revocation_label.setStyleSheet("color: #ff0000;")
            self.log_license_check("Revoked: Device hash invalidated", "unknown", False)
            self.save_button.setEnabled(False)
        else:
            self.revocation_label.setText("Revocation Status: Active")
            self.revocation_label.setStyleSheet("color: #00ff00;")
            self.log_license_check("Passed: Device active", "unknown", False)

    def check_revocation_status(self):
        """Run async revocation check."""
        asyncio.run(self.check_revocation_async())

    def save_intent(self):
        """Save selected intent to config.json."""
        intent = self.intent_combo.currentText()
        commercial_use = intent == "commercial"
        if intent not in ["educational", "commercial"]:
            self.log_display.append("Invalid intent selected.")
            self.log_license_check("Failed: Invalid intent", intent, commercial_use)
            return
        if commercial_use and intent != "commercial":
            self.log_display.append("Commercial use requires 'commercial' intent.")
            self.log_license_check("Failed: Commercial use mismatch", intent, commercial_use)
            return
        self.write_config(intent, commercial_use)
        self.log_license_check("Passed: Intent saved", intent, commercial_use)

    def open_github(self):
        """Open GitHub issues page."""
        QDesktopServices.openUrl(QUrl("https://github.com/tetrasurfaces/issues"))

    def load_logs(self):
        """Load recent license logs."""
        try:
            with open("license_log.txt", "r") as f:
                lines = f.readlines()[-5:]  # Last 5 entries
                self.log_display.setText("".join(lines))
        except Exception as e:
            self.log_display.append(f"Error loading logs: {e}")

if __name__ == "__main__":
    app = QApplication([])
    window = IntentUI()
    window.show()
    app.exec()
