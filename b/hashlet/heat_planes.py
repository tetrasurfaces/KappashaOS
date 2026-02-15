#!/usr/bin/env python3
# heat_planes.py - Heat planes for Blossom: 3D heat map, color as temperature, wake trails.
# Integrates with idutil.py for color mapping and niagara_bridge.py for particles.
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

import numpy as np
import random  # For sim heat/proximity
from idutil import IdUtil  # Integrate for color mapping (RIBIT/orientation)

class HeatPlanes:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.heat_grid = np.zeros((grid_size, grid_size, grid_size))  # 3D heat map
        self.idutil = IdUtil()  # Instance for color/temperature mapping
        self.trail_length = 5  # Length of wake trails
        self.trails = []  # List of trails (positions over time)
        print("HeatPlanes initialized - 3D heat map ready with color temperature.")
    
    def map_heat(self, position, intensity=1.0):
        """Map heat to 3D position with intensity (decay over distance)."""
        x, y, z = map(int, position * (self.grid_size - 1))  # Normalize to grid
        dist = np.linalg.norm(np.indices((self.grid_size, self.grid_size, self.grid_size)) - np.array([x, y, z])[:, :, :, None], axis=0)
        heat = intensity * np.exp(-dist / 2)  # Gaussian decay
        self.heat_grid += heat
        self.heat_grid = np.clip(self.heat_grid, 0, 1)  # Clip 0-1
        print(f"Heat mapped at {position} with intensity {intensity:.2f}.")
        return heat
    
    def apply_temperature(self, heat_value):
        """Apply color as temperature: cool blue (low) to warm red (high)."""
        # Use RIBIT or orientation colors (interpolate low-blue to high-red)
        low_color = self.idutil.orientation_colors['up']  # Blue cool
        high_color = self.idutil.orientation_colors['left']  # Red warm
        # Sim interpolate hex
        r = int((1 - heat_value) * int(low_color[1:3], 16) + heat_value * int(high_color[1:3], 16))
        g = int((1 - heat_value) * int(low_color[3:5], 16) + heat_value * int(high_color[3:5], 16))
        b = int((1 - heat_value) * int(low_color[5:7], 16) + heat_value * int(high_color[5:7], 16))
        color = f"#{r:02x}{g:02x}{b:02x}"
        print(f"Temperature color for heat {heat_value:.2f}: {color}")
        return color
    
    def generate_wake(self, path):
        """Generate wake trails from path (fade over time)."""
        if len(self.trails) >= self.trail_length:
            self.trails.pop(0)  # FIFO trail
        self.trails.append(path)
        trail_heat = np.zeros_like(self.heat_grid)
        for i, pos in enumerate(self.trails):
            fade = (i + 1) / self.trail_length  # Fade old trails
            trail_heat += self.map_heat(pos, fade)
        print(f"Wake trail generated for path {path} (length {len(self.trails)}).")
        return trail_heat
    
    def integrate_idutil(self, heat_value):
        """Integrate with idutil: apply RIBIT color to heat."""
        color = self.idutil.ribit_map(heat_value)  # RIBIT for heat jokes/colors
        return color

# For standalone testing
if __name__ == "__main__":
    planes = HeatPlanes()
    position = np.array([0.5, 0.5, 0.5])  # Sim position
    heat = planes.map_heat(position, 0.8)
    color = planes.apply_temperature(0.8)
    for _ in range(3):  # Sim 3 trail steps
        path = position + np.random.rand(3) * 0.1
        trail = planes.generate_wake(path)
    integrated_color = planes.integrate_idutil(0.8)
    print(f"Integrated color: {integrated_color}")
