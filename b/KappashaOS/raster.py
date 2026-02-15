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
import hashlib
import struct

# Your green_curve basis functions (copied clean)
def bspline_basis(u, i, p, knots):
    if p == 0:
        if i < 0 or i + 1 >= len(knots):
            return 0.0
        return 1.0 if knots[i] <= u <= knots[i + 1] else 0.0
    if i < 0 or i >= len(knots) - 1:
        return 0.0
    term1 = 0.0
    if i + p < len(knots):
        den1 = knots[i + p] - knots[i]
        if den1 > 0:
            term1 = ((u - knots[i]) / den1) * bspline_basis(u, i, p - 1, knots)
    term2 = 0.0
    if i + p + 1 < len(knots):
        den2 = knots[i + p + 1] - knots[i + 1]
        if den2 > 0:
            term2 = ((knots[i + p + 1] - u) / den2) * bspline_basis(u, i + 1, p - 1, knots)
    return term1 + term2

def custom_interoperations_green_curve(points, kappas, is_closed=False):
    points = np.array(points)
    kappas = np.array(kappas)
    degree = 3
    num_output_points = 1000
    if is_closed and len(points) > degree:
        n = len(points)
        extended_points = np.concatenate((points[n-degree:], points, points[0:degree]))
        extended_kappas = np.concatenate((kappas[n-degree:], kappas, kappas[0:degree]))
        len_extended = len(extended_points)
        knots = np.linspace(-degree / float(n), 1 + degree / float(n), len_extended + 1)
        u_fine = np.linspace(0, 1, num_output_points, endpoint=False)
        smooth_x = np.zeros(num_output_points)
        smooth_y = np.zeros(num_output_points)
        for j, u in enumerate(u_fine):
            num_x, num_y, den = 0.0, 0.0, 0.0
            for i in range(len_extended):
                b = bspline_basis(u, i, degree, knots)
                w = extended_kappas[i] * b
                num_x += w * extended_points[i, 0]
                num_y += w * extended_points[i, 1]
                den += w
            if den > 0:
                smooth_x[j] = num_x / den
                smooth_y[j] = num_y / den
        smooth_x = np.append(smooth_x, smooth_x[0])
        smooth_y = np.append(smooth_y, smooth_y[0])
    else:
        n = len(points)
        knots = np.concatenate(([0] * (degree + 1), np.linspace(0, 1, n - degree + 1)[1:-1], [1] * (degree + 1)))
        u_fine = np.linspace(0, 1, num_output_points)
        smooth_x = np.zeros(num_output_points)
        smooth_y = np.zeros(num_output_points)
        for j, u in enumerate(u_fine):
            num_x, num_y, den = 0.0, 0.0, 0.0
            for i in range(n):
                b = bspline_basis(u, i, degree, knots)
                w = kappas[i] * b
                num_x += w * points[i, 0]
                num_y += w * points[i, 1]
                den += w
            if den > 0:
                smooth_x[j] = num_x / den
                smooth_y[j] = num_y / den
    return smooth_x, smooth_y

# Raster flow
def vectors_to_grid(vectors, size=32):
    grid = np.zeros((size, size, size), dtype=np.uint8)
    for start, end in vectors:
        t = np.linspace(0, 1, 100)
        pts = (1 - t[:, None]) * start + t[:, None] * end
        for p in pts.astype(int):
            x, y, z = np.clip(p, 0, size - 1)
            grid[x, y, z] = 255
    return grid

def flatten_grid(grid):
    flat = grid.flatten()
    byte_str = struct.pack(f'<{len(flat)}B', *flat)
    return byte_str.decode('latin1')

def divide_by_pi(s):
    h = 0
    for c in s:
        h = (h * 31 + ord(c)) % (2**64 - 1)
    return h / np.pi % 369.0

def eclipse(grid):
    coords = np.indices(grid.shape)
    even_mask = ((coords[0] + coords[1] + coords[2]) % 2 == 0)
    grid[even_mask] = 0
    return grid

def curve_raster_loop(json_str, size=32):
    # Mock vectors from hash seed
    seed = int(hashlib.sha256(json_str.encode()).hexdigest(), 16) % 1000
    theta = np.linspace(0, 6 * np.pi, 200)
    r = 0.3 * theta
    points = np.column_stack([r * np.cos(theta), r * np.sin(theta), theta / 6])
    points = (points - points.min(axis=0)) / (points.max(axis=0) - points.min(axis=0)) * (size - 2) + 1

    # Rasterize spline to grid (no scipy)
    kappas = [1.0] * len(points)
    smooth_x, smooth_y = custom_interoperations_green_curve(points[:, :2], kappas, is_closed=False)
    smooth_z = np.linspace(1, size-2, len(smooth_x))  # linear z
    smooth_points = np.column_stack([smooth_x, smooth_y, smooth_z])
    vecs = [(smooth_points[i], smooth_points[i+1]) for i in range(len(smooth_points)-1)]
    grid = vectors_to_grid(vecs, size)

    # Eclipse prune
    grid = eclipse(grid)

    # Flatten & tweak
    raw = flatten_grid(grid)
    flat_val = divide_by_pi(raw)
    print(f"Flattened param: {flat_val:.6f}")

    return grid, flat_val, raw

# Test
if __name__ == "__main__":
    json_str = '{"note": "To whoever finds this—"}'
    grid, flat_val, raw = curve_raster_loop(json_str)
    print(f"Grid non-zero voxels: {np.sum(grid > 0)}")
    print(f"Raw flatten length: {len(raw)}")