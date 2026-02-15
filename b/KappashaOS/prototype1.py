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

import numpy as np

GRID_SIZE = 5
grid = np.full((GRID_SIZE, GRID_SIZE), '.', dtype='<U1')

splines = []
for row in range(GRID_SIZE):
    c = np.array([
        [0.0, float(row)],
        [1.0, float(row)],
        [3.0, float(row)],
        [4.0, float(row)]
    ])
    splines.append(c)

def hash_to_delta(seed_str, dim=1.0):
    seed = hash(seed_str) & 0xFFFFFFFF  # safe 32-bit hash
    np.random.seed(seed)
    return np.random.uniform(-dim/2, dim/2)

def modulate(h):
    for row, spline in enumerate(splines):
        delta_y1 = hash_to_delta(f"{h}_row{row}_y1", dim=GRID_SIZE)
        delta_y2 = hash_to_delta(f"{h}_row{row}_y2", dim=GRID_SIZE)
        delta_x1 = hash_to_delta(f"{h}_row{row}_x1", dim=0.5)
        delta_x2 = hash_to_delta(f"{h}_row{row}_x2", dim=0.5)
        
        spline[1, 1] += delta_y1
        spline[2, 1] += delta_y2
        spline[1, 0] += delta_x1
        spline[2, 0] += delta_x2

def cubic_bezier(t, p0, p1, p2, p3):
    u = 1 - t
    tt = t * t
    uu = u * u
    uuu = uu * u
    ttt = tt * t
    return (uuu * p0 + 3 * uu * t * p1 + 3 * u * tt * p2 + ttt * p3)

def show():
    print("\nGrid + spline wobble (console approx):")
    for row in range(GRID_SIZE):
        line = list(grid[row])
        print(' '.join(line))
    
    print("\nSpline paths (y values per column):")
    for row_idx, spline in enumerate(splines):
        print(f"Row {row_idx}: ", end='')
        for col in range(GRID_SIZE):
            t = col / (GRID_SIZE - 1) if GRID_SIZE > 1 else 0.5
            point = cubic_bezier(t, *spline)
            y_approx = round(point[1], 1)
            print(f"{y_approx:5.1f}", end=' ')
        print()

show()
modulate('deadbeef')
show()
modulate('a1b2c3d4')
show()
