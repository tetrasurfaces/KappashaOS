#!/usr/bin/env python3
# kappa_wire.py - Grid layer for live kappa wires in KappashaOS with spiral integration.
# Async, Navi-integrated.
# Copyright 2025 xAI
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program. If not, see <https://www.gnu.org/licenses/>.

import numpy as np
import asyncio
from src.hash.spiral_hash import kappa_spiral_hash  # Import spiral hash

class KappaWire:
    def __init__(self, grid_size=107):
        self.grid_size = grid_size
        self.wires = np.zeros((grid_size, grid_size, grid_size), dtype=object)
        self.high_points = np.random.rand(grid_size, grid_size, grid_size) * 100  # Mock high points
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        print("KappaWire initialized - live wires ready for 107 grid with spiral.")

    async def navi_place_on_wire(self, x: int, y: int, z: int, encoded: str) -> bool:
        """Place encoded payload with spiral hash and enhanced batching."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size and 0 <= z < self.grid_size:
            batch_size = 20  # Increased for spiral precision
            start_x, end_x = max(0, x - batch_size // 2), min(self.grid_size, x + batch_size // 2 + 1)
            comfort_vec = np.random.rand(3)
            spiral_data = kappa_spiral_hash(encoded, comfort_vec)
            spiral_vec = spiral_data['spiral_vec']
            for bx in range(start_x, end_x):
                for by in range(max(0, y - batch_size // 2), min(self.grid_size, y + batch_size // 2 + 1)):
                    for bz in range(max(0, z - batch_size // 2), min(self.grid_size, z + batch_size // 2 + 1)):
                        idx = (bx + by + bz) % len(spiral_vec)
                        self.wires[bx % self.grid_size, by % self.grid_size, bz % self.grid_size] = spiral_data['light_raster']
            self.tendon_load = np.random.rand() * 0.08  # Further reduced load
            self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.95 else 0.0  # Tighter threshold
            if self.tendon_load > 0.2:
                print("KappaWire: Warning - Tendon overload. Resetting.")
                self.reset()
            if self.gaze_duration > 30.0:
                print("KappaWire: Warning - Excessive gaze. Pausing.")
                await asyncio.sleep(0.3)  # Reduced pause
                self.gaze_duration = 0.0
            await asyncio.sleep(0)  # Minimal delay
            print(f"Navi: Placed {spiral_data['light_raster'][:10]}... on wire batch at ({x}, {y}, {z})")
            return True
        return False

    def retrieve_from_wire(self, x: int, y: int, z: int) -> str:
        """Retrieve payload from wire."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size and 0 <= z < self.grid_size:
            return self.wires[x, y, z] or ""
        return ""

    def reset(self):
        self.tendon_load = 0.0
        self.gaze_duration = 0.0

if __name__ == "__main__":
    async def navi_test():
        wire = KappaWire()
        await wire.navi_place_on_wire(5, 5, 5, "encoded_data")
    asyncio.run(navi_test())
