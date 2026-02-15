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

# 5×5 grid holding characters (dots = empty)
GRID_SIZE = 5
grid = np.full((GRID_SIZE, GRID_SIZE), '.', dtype='<U1')

# One cubic spline per row (4 control points each: start, ctrl1, ctrl2, end)
splines = []
for row in range(GRID_SIZE):
    # x = column 0 → 4, y = row height
    # start at (0, row), end at (4, row)
    # initial ctrl points straight horizontal
    c = np.array([
        [0.0, row],          # anchor left
        [1.0, row],          # ctrl1
        [3.0, row],          # ctrl2
        [4.0, row]           # anchor right
    ])
    splines.append(c)

def hash_to_delta(h, dim=1.0):
    """Hash → small offset [-dim/2, +dim/2]"""
    seed = int(h, 16)
    np.random.seed(seed)
    return np.random.uniform(-dim/2, dim/2)

def modulate(h):
    """Apply hash to wobble middle control points of each spline"""
    for row, spline in enumerate(splines):
        # Wobble ctrl1 & ctrl2 y-coordinate only
        delta1 = hash_to_delta(h + str(row), dim=GRID_SIZE)
        delta2 = hash_to_delta(h + str(row) + '2', dim=GRID_SIZE)
        
        spline[1, 1] += delta1  # ctrl1 y
        spline[2, 1] += delta2  # ctrl2 y
        
        # Keep x roughly in place (small x wobble optional)
        spline[1, 0] += hash_to_delta(h + str(row) + 'x1', dim=0.5)
        spline[2, 0] += hash_to_delta(h + str(row) + 'x2', dim=0.5)

def cubic_bezier(t, p0, p1, p2, p3):
    """Cubic Bézier point at t ∈ [0,1]"""
    u = 1 - t
    tt = t * t
    uu = u * u
    uuu = uu * u
    ttt = tt * t
    return (uuu * p0 +
            3 * uu * t * p1 +
            3 * u * tt * p2 +
            ttt * p3)

def show():
    print("\nGrid + spline wobble (console approx):")
    # Print grid
    for row in range(GRID_SIZE):
        line = list(grid[row])
        print(' '.join(line))
    
    print("\nSpline paths (approximated as y values per column):")
    for row_idx, spline in enumerate(splines):
        print(f"Row {row_idx}: ", end='')
        for col in range(GRID_SIZE):
            # Sample at x = col
            t = col / (GRID_SIZE - 1) if GRID_SIZE > 1 else 0.5
            point = cubic_bezier(t,
                                 spline[0], spline[1], spline[2], spline[3])
            y_approx = round(point[1], 1)
            print(f"{y_approx:5.1f}", end=' ')
        print()

# Initial view
show()

# Modulate with example hash
modulate('deadbeef')
show()

# Modulate again — watch it dance
modulate('a1b2c3d4')
show()