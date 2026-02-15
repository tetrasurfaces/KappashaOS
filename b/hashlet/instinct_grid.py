#!/usr/bin/env python3
# instinct_grid.py - Instinct grid for Blossom: fight/freeze/flee, flat as silence.
# Integrates with thought_curve.py for instinct choices and ramps.
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
import random  # For sim choices
from thought_curve import ThoughtCurve  # Integrate for ramp/graduate on choices

class InstinctGrid:
    def __init__(self, grid_size=3):  # 3x3 grid for fight/freeze/flee
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size))  # Flat grid as silence
        self.instincts = {
            'fight': (0, 0),  # Left corner
            'freeze': (1, 1),  # Center
            'flee': (2, 2)    # Right corner
        }
        self.flat_silence = 0  # Flat as silence (no peaks)
        print("InstinctGrid initialized - fight/freeze/flee ready, flat as silence.")
    
    def choose_instinct(self, gaze_x, gaze_y):
        """Choose instinct by gaze position (eyes vote)."""
        x, y = int(gaze_x * (self.grid_size - 1)), int(gaze_y * (self.grid_size - 1))  # Normalize [0,1] to grid
        closest = min(self.instincts, key=lambda k: abs(self.instincts[k][0] - x) + abs(self.instincts[k][1] - y))
        self.grid[x, y] = 1  # Mark choice
        print(f"Instinct chosen by gaze ({x}, {y}): {closest}")
        self.react(closest)
        return closest
    
    def react(self, instinct):
        """React to instinct: fight = spike, freeze = stop, flee = flip (flat silence between)."""
        if instinct == 'fight':
            self.grid += np.random.rand(self.grid_size, self.grid_size) * 2  # Spike noise
            print("Fight: Room spikes - Frank charges.")
        elif instinct == 'freeze':
            self.grid.fill(0)  # Stop everything
            print("Freeze: Time stops - flat silence.")
        elif instinct == 'flee':
            self.grid = np.flip(self.grid)  # Flip world
            print("Flee: World flips - fall upward.")
        # Flat silence reset if no peaks
        if np.max(self.grid) == 0:
            self.flat_silence += 1
            print(f"Flat as silence ({self.flat_silence}): Watch Frank loop.")
    
    def integrate_curve(self, curve_level):
        """Integrate with thought_curve: instinct choice triggers ramp/graduate."""
        gaze_x, gaze_y = random.uniform(0, 1), random.uniform(0, 1)  # Sim gaze
        instinct = self.choose_instinct(gaze_x, gaze_y)
        self.curve = ThoughtCurve()  # Instance for integration
        ramped = self.curve.quiet_loud_ramp(curve_level)  # Use quiet-loud for instinct silence
        return ramped, instinct

# For standalone testing
if __name__ == "__main__":
    grid = InstinctGrid()
    for _ in range(5):  # Sim 5 choices
        gaze_x, gaze_y = random.uniform(0, 1), random.uniform(0, 1)
        grid.choose_instinct(gaze_x, gaze_y)
        integrated, instinct = grid.integrate_curve(random.randint(-3, 10))  # Sim curve level
        print(f"Integrated: {integrated}, Instinct: {instinct}")
