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
# navi_core.py

import asyncio
import numpy as np
from js import document, window  # Emscripten JS interop
from ghosthand import GhostHand  # Placeholder, will need Wasm port

FPS = 60
GRID_SIZE = 10
TENDON_THRESHOLD = 0.2
GAZE_THRESHOLD = 30.0

async def safety_monitor(hand):
    gaze_duration = 0.0
    tendon_load = 0.0
    while True:
        # Mock sensor data (replace with WebGyro/WebSocket later)
        tendon_load = np.random.rand() * 0.3
        gaze_duration += 1.0 / FPS if np.random.rand() > 0.7 else 0.0

        if tendon_load > TENDON_THRESHOLD:
            print("Warning: Tendon overload. Disengaging.")
            hand.reset()
            window.alert("Tendon safety limit reached. Resetting.")
        if gaze_duration > GAZE_THRESHOLD:
            print("Warning: Excessive gaze. Pausing.")
            await asyncio.sleep(2.0)
            gaze_duration = 0.0
            window.alert("Gaze pause activated.")

        await asyncio.sleep(1.0 / FPS)

async def main():
    grid = np.zeros((GRID_SIZE, GRID_SIZE, GRID_SIZE), dtype=np.uint8)
    hand = GhostHand(grid)

    # Start safety monitor
    asyncio.create_task(safety_monitor(hand))

    canvas = document.getElementById("naviCanvas")  # Assume HTML canvas
    ctx = canvas.getContext("2d")

    while True:
        # Simulate EEG twitch (intent from user event)
        twitch = np.random.rand() * 0.3
        if twitch > 0.2:
            hand.move(twitch)
            print(f"Navi: Hey! Move by {twitch:.2f}")
            ctx.fillText(f"Navi: Move {twitch:.2f}", 10, 20)

        # Gyro input from device orientation (WebGyro API mock)
        gyro_data = np.array([np.random.rand() * 0.2 - 0.1,
                             np.random.rand() * 0.2 - 0.1,
                             0.0])
        hand.adjust_kappa(gyro_data)
        print(f"Navi: Adjusting kappa by {gyro_data}")
        ctx.fillText(f"Navi: Kappa {gyro_data[0]:.2f}", 10, 40)

        await asyncio.sleep(1.0 / FPS)

# Emscripten-specific entry point
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
