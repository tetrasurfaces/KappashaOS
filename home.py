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
# 1. **Physical Embodiment Restrictions**: Use with devices is for non-hazardous purposes only. Harmful mods are prohibited, with license revocable by xAI.
# 2. **Ergonomic Compliance**: Limits tendon load to 20%, gaze to 30 seconds (ISO 9241-5).
# 3. **Safety Monitoring**: Real-time tendon/gaze checks, logged for audit.
# 4. **Revocability**: xAI may revoke for unethical use (e.g., surveillance).
# 5. **Export Controls**: Sensor devices comply with US EAR Category 5 Part 2.
# 6. **Open Development**: Hardware docs shared post-private phase.
#
# Private Development Note: This repository is private for xAI’s KappashaOS and Navi development. Access is restricted. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) post-phase.

#!/usr/bin/env python3
# home.py - Safe origin room for Blossom: homing index, vintage cork, no-delete zone with ramp cipher and kappa wires.

import hashlib
import numpy as np
import time
import os
import asyncio

class RampCipher:
    def __init__(self, pin: str = '12345678'):
        self.pin = pin.zfill(8)
        self.theta = np.linspace(0, 180, 200)
        self.heights = self._build_spline()

    def _build_spline(self):
        h = np.zeros(200)
        h[:50] = self.theta[:50] * (3.8 / 45)
        h[50:100] = 3.8 + np.sin(self.theta[50:100] * 0.05 + 1) * 2
        h[100:] = 84.6 + (self.theta[100:] - 100) * (89 - 84.6) / 100
        for i, d in enumerate(self.pin):
            knot_pos = 50 + i * 6
            h[int(knot_pos):int(knot_pos)+4] *= (1 + int(d) / 9)
        return h

    def encode(self, hash_str: str, index: int = 0) -> str:
        encoded = ''
        for j, char in enumerate(hash_str):
            idx = (index + j) % len(self.heights)
            delta = int(char, 16) + self.heights[idx] * 10
            encoded += chr(delta % 256)
        return encoded

class KappaWire:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.wires = np.zeros((grid_size, grid_size, grid_size), dtype=object)
        self.high_points = np.random.rand(grid_size, grid_size, grid_size) * 100  # Mock high points

    def place_on_wire(self, x, y, z, encoded):
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size and 0 <= z < self.grid_size:
            self.wires[x, y, z] = encoded
            return True
        return False

class Home:
    def __init__(self):
        self.grid_size = 10
        self.grid = np.zeros((self.grid_size, self.grid_size, self.grid_size))
        self.origin_hash = self._hash_origin()
        self.vintage_dir = "./vintage"
        os.makedirs(self.vintage_dir, exist_ok=True)
        self.items = {"bowl": [5,5,5], "ball": [5,6,5]}
        self.ramp = RampCipher('35701357')
        self.kappa_wire = KappaWire(self.grid_size)
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        print("Home initialized - ramp cipher and kappa wires active.")

    def _hash_origin(self):
        seed = f"home-origin-{time.time()}"
        return hashlib.sha256(seed.encode()).hexdigest()

    async def navi_load(self):
        self.grid.fill(0)
        self.ramp = RampCipher('35701357')
        entropy = np.random.uniform(0, 1)
        if entropy > 0.69:
            await self.navi_cork_state(entropy)
        self.tendon_load = np.random.rand() * 0.3
        self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
        if self.tendon_load > 0.2:
            print("Home: Warning - Tendon overload. Resetting.")
            self.reset()
        if self.gaze_duration > 30.0:
            print("Home: Warning - Excessive gaze. Pausing.")
            await asyncio.sleep(2.0)
            self.gaze_duration = 0.0
        await asyncio.sleep(0)
        print(f"Navi: Home loaded - origin hash: {self.origin_hash[:10]}... Items: {self.items}")

    async def navi_cork_state(self, grade):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        state_data = f"grid:{self.grid.flatten()[:10]}... items:{self.items}"
        hash_tag = hashlib.sha256(f"{state_data}-{timestamp}-{grade}".encode()).hexdigest()
        with open(f"{self.vintage_dir}/{hash_tag}.txt", "w") as f:
            f.write(f"Vintage home state: {state_data} Grade: {grade:.2f}")
        self.tendon_load = np.random.rand() * 0.3
        self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
        if self.tendon_load > 0.2:
            print("Home: Warning - Tendon overload. Resetting.")
            self.reset()
        if self.gaze_duration > 30.0:
            print("Home: Warning - Excessive gaze. Pausing.")
            await asyncio.sleep(2.0)
            self.gaze_duration = 0.0
        await asyncio.sleep(0)
        print(f"Navi: Home state corked: {hash_tag[:10]}...")

    async def navi_index_grid(self, x, y, z, data):
        """Index with ramp encode on kappa wire."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size and 0 <= z < self.grid_size:
            hash_str = hashlib.sha256(data.encode()).hexdigest()
            encoded = self.ramp.encode(hash_str, x + y + z)
            if self.kappa_wire.place_on_wire(x, y, z, encoded):
                self.grid[x, y, z] = 1
                self.tendon_load = np.random.rand() * 0.3
                self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
                if self.tendon_load > 0.2:
                    print("Home: Warning - Tendon overload. Resetting.")
                    self.reset()
                if self.gaze_duration > 30.0:
                    print("Home: Warning - Excessive gaze. Pausing.")
                    await asyncio.sleep(2.0)
                    self.gaze_duration = 0.0
                await asyncio.sleep(0)
                print(f"Navi: Indexed ({x}, {y}, {z}) with encoded {encoded[:10]}...")
                return encoded
        return None

    def reset(self):
        self.tendon_load = 0.0
        self.gaze_duration = 0.0

if __name__ == "__main__":
    async def navi_test():
        home = Home()
        await home.navi_load()
        await home.navi_index_grid(5, 5, 5, "test data")
        await home.navi_cork_state(0.8)

    asyncio.run(navi_test())
