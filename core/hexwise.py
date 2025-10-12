#!/usr/bin/env python3
# KappashaOS/core/hexwise.py
# Hex-wise color mapping for KappashaOS orientation and function states
#
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
# - For hardware/embodiment interfaces (if any): Licensed under the Apache License, Version 2.0
#   with xAI amendments for safety and physical use (prohibits misuse in weapons or hazardous applications;
#   requires ergonomic compliance; revocable for unethical use). See http://www.apache.org/licenses/LICENSE-2.0
#   for details, with the following xAI-specific terms appended.
#
# Copyright 2025 xAI
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
# SPDX-License-Identifier: Apache-2.0
#
# xAI Amendments for Physical Use:
# 1. **Physical Embodiment Restrictions**: Use with physical devices (e.g., headsets, watches) is for non-hazardous purposes only. Modifications enabling harm are prohibited, with license revocable by xAI.
# 2. **Ergonomic Compliance**: Interfaces must follow ISO 9241-5, limiting tendon load to 20% and gaze duration to 30 seconds.
# 3. **Safety Monitoring**: Real-time checks for tendon/gaze, logged for audit.
# 4. **Revocability**: xAI may revoke for unethical use (e.g., surveillance).
# 5. **Export Controls**: Sensor-based devices comply with US EAR Category 5 Part 2.
# 6. **Open Development**: Hardware docs shared under this License post-private phase.
#
# Private Development Note: This repository is private for xAI’s KappashaOS and Navi development. Access is restricted to authorized contributors. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) post-private phase.

def hexwise_color(func, entropy):
    """Map function to color based on entropy."""
    colors = {
        "stop": "#ff0000",        # Red
        "limit": "#8b4513",       # Brown
        "arbitrage": "#ffbf00",   # Amber
        "kappa": "#ffffff",       # White
        "market": "#00ffff",      # Blue
        "sell": "#00ff00",        # Green
        "up": "#00ffff",          # Sky, north
        "up_mid": "#00ff00",      # Growth
        "mid": "#ffff00",         # Focus
        "down_mid": "#ff6600",    # Warning
        "down": "#ff0000",        # Stop
        "down_low": "#8b4513",    # Earth
        "right": "#ff1493",       # East, heat
        "heat": "#ee82ee",        # Exhaustion
        "shadow": "#4b0082"       # Fatigue, dusk
    }
    return colors.get(func, "#ffffff") if entropy > 7000 else "#808080"  # Gray if low entropy

if __name__ == "__main__":
    print(f"Hex-wise stop: {hexwise_color('stop', 8000)}")  # Red
    print(f"Hex-wise sell: {hexwise_color('sell', 8000)}")  # Green
    print(f"Hex-wise up: {hexwise_color('up', 8000)}")     # Blue
