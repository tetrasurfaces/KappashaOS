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

import hashlib
import math

mersennes = [  # your 64 list here
    2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281,
    3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243,
    110503, 132049, 216091, 756839, 859433, 1257787, 1398269, 2976221, 3021377,
    6972593, 13466917, 20996011, 24036583, 25964951, 30402457, 32582657,
    37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933,
    136279841, 194087760, 393668989, 1137184133, 4678395213, 27411294813,
    228732945894, 2718281472161, 46007290309705, 1108984342777087,
    38070686010400544, 1861326323879814400, 129604733991207583744
]

KAPPA_ODD = 0.3536
KAPPA_EVEN = 0.3563

def modulated_mersenne(lane: int) -> int:
    idx = lane % 64
    p = mersennes[idx]
    kappa = KAPPA_ODD if idx % 2 == 1 else KAPPA_EVEN
    pitch = (lane / 64.0) * 0.1
    roll = (lane * 0.02) % (2 * math.pi)
    az = math.sin(lane * 0.04)
    collapse = 1 / (1 + (lane / 64.0)**2)
    modulated = int(p * kappa * (1 + pitch) * (1 + az) * collapse)
    # Rotation twist: shift by lane % 13 bits
    twist = modulated >> (lane % 13)
    return modulated ^ twist

def p_hash_256(message: bytes) -> int:
    # Strong pre-mix: sha256 → 256-bit digest
    pre = int.from_bytes(hashlib.sha256(message).digest(), 'big')
    h = 0
    for i in range(64):
        # Take 4 bytes from message (pad if short)
        start = i * 4
        chunk = message[start:start+4] + b'\x00' * (4 - (len(message) - start) % 4)
        lane_hash = int.from_bytes(chunk, 'big') ^ modulated_mersenne(i)
        # Stronger fold: rotate + multiply + xor
        rot = (lane_hash << (i % 64)) | (lane_hash >> (64 - (i % 64)))
        h = (h * 0x9e3779b97f4a7c15) ^ rot  # golden ratio constant multiply
    return h & ((1 << 256) - 1)

# Test it
print("p-hash-256 examples:")
for s in ["hello", "world", "xoxo <3", "Ara", "Frank here", "M53 candidate"]:
    h = p_hash_256(s.encode())
    print(f"'{s}' → {h:064x}")

# Quick collision feel (uncomment for 10k test)
import secrets
collisions = set()
for _ in range(10000):
    seed = secrets.token_bytes(16)
    h = p_hash_256(seed)
    collisions.add(h)
print(f"Unique hashes: {len(collisions)} / 10000")