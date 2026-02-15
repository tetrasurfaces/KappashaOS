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

import timeit
import math
import random

GRID_SIZE = 16
VOXEL_COUNT = GRID_SIZE ** 3  # 4096
GOLDEN_ANGLE = 2.39996322972865332  # radians ≈137.5°
KAPPA_BASE = 0.3536
FROG_HOPS = [22, 25, 28, -13, 7]

def build_grid(seed=42):
    """Precompute 16³ voxel grid with tetrahedral + spiral seed"""
    random.seed(seed)
    grid = []
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            for z in range(GRID_SIZE):
                # Simple tetrahedral breathing + spiral offset
                r = math.sqrt(x**2 + y**2 + z**2) / (GRID_SIZE * math.sqrt(3))
                theta = math.atan2(y, x) + GOLDEN_ANGLE * r
                grid.append((x + r * math.cos(theta),
                             y + r * math.sin(theta),
                             z + r * math.sin(theta * 0.5)))
    return grid

GRID = build_grid()  # Build once at startup

def field_shear(pos: tuple, angle_deg: float):
    """Simple shear: tilt x/y by cos(angle)"""
    x, y, z = pos
    cos_a = math.cos(math.radians(angle_deg))
    return (x + y * cos_a, y, z)

def helix_frog_field(data: bytes, salt: int = 0, breath_rate: float = 12.0):
    """Map input to voxel bucket with helix + shear + frog hops"""
    # Fast base hash (Python's siphash, ~3 ns)
    val = hash(data) & 0xFFFFFFFF

    # Flat mods
    offset = (val + salt) % 255

    # Rotations
    azimuth = (offset % 360)
    pitch = (offset * 1.618) % 255
    yaw = (offset * 0.618) % 255

    # Kappa decay
    decay = KAPPA_BASE + (offset / 255) * 0.02

    # Field shear: breath modulates angle
    shear_angle = 45 + (breath_rate - 12.0) * 2  # 45°–75° range
    pos = field_shear((offset, offset * 0.5, offset * 0.3), shear_angle)

    # Final spiral wrap (trig once)
    kappa = KAPPA_BASE + (offset / 255) * 0.01
    theta = math.radians(azimuth + pitch + yaw)
    r = math.exp(kappa * theta) * decay * GRID_SIZE  # scale to 16

    # Nearest voxel index (mocked distance for speed)
    voxel_idx = int(r + pos[0] + pos[1] + pos[2]) % VOXEL_COUNT

    # Frog hops for chaos
    for hop in FROG_HOPS:
        voxel_idx = (voxel_idx + hop) % VOXEL_COUNT

    return voxel_idx, 'green'  # placeholder breath color

# Test & speed
if __name__ == '__main__':
    tests = [b'hello', b'2042', b'mersenne52']
    for t in tests:
        idx, color = helix_frog_field(t, salt=42, breath_rate=12.0)
        print(f"Input: {t.decode(errors='ignore')!r} → Voxel: {idx:6} color: {color}")

    time_ns = timeit.timeit(
        lambda: helix_frog_field(b'speedtest', salt=42),
        number=100_000
    ) / 100_000 * 1e9
    print(f"Avg map time (100k runs): {time_ns:.1f} ns")
