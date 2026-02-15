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

import time
import math
import random
import string

def frog_hash(seed, base=9, laps=25, kappa=0.3536, decay=0.5):
    # Seed to numeric drift (simple sum + tiny wobble)
    s = sum(ord(c) for c in seed) % 65536
    drift = s * 0.001  # small seed influence
    
    # Generate 256 spiral points
    points = []
    for i in range(256):
        theta = i * kappa + drift % (2 * math.pi)
        r = theta * base  # radial growth
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        z = 0.0
        points.append([x, y, z, i])
    
    # Modulations
    # 1. Tilt (elevation/azimuth/yaw — simple z lift + rotation)
    for i in range(3):
        tilt = i * 0.2 * decay  # scale with decay
        for p in points:
            p[2] += tilt  # elevation
            # Simple azimuth/yaw rotation on x/y
            rx = p[0] * math.cos(tilt) - p[1] * math.sin(tilt)
            ry = p[0] * math.sin(tilt) + p[1] * math.cos(tilt)
            p[0], p[1] = rx, ry
    
    # 2. Decay + flatten (unwrap 2πr → linear)
    for p in points:
        r = math.sqrt(p[0]**2 + p[1]**2)
        if r > 0:
            flat_r = r / (2 * math.pi) * (1 - decay)  # decay pulls toward flat
            p[0] = flat_r
            p[1] = 0.0  # collapse to x-axis
    
    # Final bucket: hash of final point coords mod 256
    last = points[-1]
    h = int((last[0] * 31 + last[1] * 17 + last[2] * 7) * 1000) % 256
    return h  # 0–255, overflow handled outside if needed

# Benchmark
def benchmark(base=9, laps=25, decay=0.5, n=10000):
    start = time.time()
    buckets = set()
    collisions = 0
    for _ in range(n):
        seed = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        h = frog_hash(seed, base=base, laps=laps, decay=decay)
        if h in buckets:
            collisions += 1
        buckets.add(h)
    elapsed = time.time() - start
    unique = len(buckets)
    collision_rate = collisions / n * 100
    speed = n / elapsed if elapsed > 0 else 0
    print(f"Base {base} | Laps {laps} | Decay {decay:.2f}")
    print(f"  Speed: {speed:,.0f} h/s")
    print(f"  Unique buckets: {unique}/256")
    print(f"  Collision rate: {collision_rate:.2f}%")
    print("")

# Run tests
print("HelixFrog benchmark (10k random 16-char seeds)")
benchmark(base=9, laps=25, decay=0.3536)   # baseline
benchmark(base=7, laps=8, decay=0.3536)    # tighter, slower
benchmark(base=11, laps=32, decay=0.3536)  # looser, faster?
benchmark(base=9, laps=25, decay=0.0)   # flat spiral
benchmark(base=9, laps=25, decay=1.0)   # full circle flatten