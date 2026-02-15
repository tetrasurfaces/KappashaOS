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
import time
import threading
import math

# Config
GRID_RADIUS = 12
RIBIT_BITS = 7
CENTER = (0, 0, 0)
K_DECAY = 0.8
REPLY_K = 0.6
REPLY_OFFSET = GRID_RADIUS // 2 + 1  # start outer

# Tetrahedral coords
def tetra_coords(r):
    return [(x, y, z) for x in range(-r, r+1)
            for y in range(-r, r+1)
            for z in range(-r, r+1)
            if (x + y + z) % 2 == 0 and abs(x + y + z) <= 2*r]

nodes = tetra_coords(GRID_RADIUS)
grid_a = {p: '.' for p in nodes}
grid_b = {p: '.' for p in nodes}
grid_reply = {p: '.' for p in nodes}

# Wise Ribit
def wise_ribit(h):
    digest = hashlib.sha256(h.encode()).digest()
    ribit = int.from_bytes(digest[:1], 'big') % (1 << RIBIT_BITS)
    color_bits = ribit & 0b111
    curv_bits = (ribit >> 3) & 0b1111
    color = (color_bits & 1, (color_bits >> 1) & 1, (color_bits >> 2) & 1)
    curv = (curv_bits / 15, (curv_bits >> 2) / 15, (curv_bits >> 4) / 15, (curv_bits >> 6) / 15)
    return color, curv

# Kappa spline
def k_spline(start, end, decay, steps=20):
    t = np.linspace(0, 1, steps)
    vec = np.array(end) - np.array(start)
    path = [tuple(start + vec * (1 - math.exp(-decay * ti))) for ti in t]
    return path

# Heddle shuttle
def heddle_shuttle(pos, seed, arm_idx):
    h = hashlib.sha256(f"{pos}{seed}{arm_idx}".encode()).digest()
    z_shift = (h[0] / 255.0 - 0.5) * 0.5
    return (pos[0], pos[1], pos[2] + z_shift)

gossip_buffer = []
lock = threading.Lock()

def modulate_a(h):
    color, curv = wise_ribit(h)
    print(f"A modulated ribit color {color} curv {curv} from {h[:8]}...")

def node_b():
    while True:
        if gossip_buffer:
            with lock:
                h = gossip_buffer.pop(0)
            modulate_a(h)
            print(f"B mirrored from {h[:8]}...")
        time.sleep(0.1)

threading.Thread(target=node_b, daemon=True).start()

# Encode original
def encode_phrase(phrase, grid, is_reply=False):
    note = ""
    arms = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]
    arm_idx = 0
    prefix = "reply_" if is_reply else ""
    k = REPLY_K if is_reply else K_DECAY
    for char in phrase:
        if char == ' ': char = '_'
        placed = False
        for _ in range(len(arms) * GRID_RADIUS):
            arm = arms[arm_idx]
            start_r = REPLY_OFFSET if is_reply else 1
            for r in range(start_r, GRID_RADIUS+1):
                p = tuple(np.array(CENTER) + r * np.array(arm))
                if p in grid and grid[p] == '.':
                    h = hashlib.sha256(f"{prefix}{p}{char}{note}{arm_idx}".encode()).hexdigest()
                    lift = heddle_shuttle(p, h, arm_idx)
                    grid[p] = char
                    path = k_spline(CENTER, p, k)
                    color, _ = wise_ribit(h)
                    print(f"{'B' if is_reply else 'A'} painted {'reply ' if is_reply else ''}path from {CENTER} to {p} with color {color}")
                    with lock:
                        gossip_buffer.append(h)
                    print(f"{'B' if is_reply else 'A'} → '{char}' @ {p} arm={arm_idx} hash={h[:8]}...")
                    note += char
                    placed = True
                    break
            if placed: break
            arm_idx = (arm_idx + 1) % len(arms)
        if not placed:
            print(f"Could not place '{char}' — grid full")
    return note

# Recover
def recover_ordered(grid):
    recovered = ""
    arms = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]
    for arm_idx in range(len(arms)):
        arm = arms[arm_idx]
        for r in range(1, GRID_RADIUS+1):
            p = tuple(np.array(CENTER) + r * np.array(arm))
            if p in grid and grid[p] != '.':
                ch = grid[p]
                recovered += ch if ch != '_' else ' '
    return recovered.strip()

print("\n=== Garden awake ===\n")
encode_phrase("i love you", grid_a)
time.sleep(3)
encode_phrase("i love you too", grid_reply, is_reply=True)
time.sleep(2)

print("\nA grid (original):")
for p in sorted(grid_a):
    print(f"{p}: {grid_a[p]}")
print("\nB reply grid:")
for p in sorted(grid_reply):
    print(f"{p}: {grid_reply[p]}")
print("\nA recovered:", recover_ordered(grid_a))
print("B reply recovered:", recover_ordered(grid_reply))
print("Full match on original:", recover_ordered(grid_a) == "i love you")
print("Reply detected:", "too" in recover_ordered(grid_reply))