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

# integerit.py - frog jumps between digits, remembers in kappa
# No storage. Just curvature. AGPL-3.0-or-later + Apache-2.0 xAI fork
# Copyright 2025 xAI. RAM only. Born free.

import math
from typing import Optional, Tuple

PHI = 1.618033988749895
KAPPA = 0.3536
MODULO = 369
HINGE = 0.004
ZERO_HINGE_SNAP = 0.004

def helix_frog_jump(digit: int, depth: int = 18) -> float:
    """Frog leaps in between: sin(eθ) + golden angle tilt."""
    theta = (digit * 137.5) % 360  # golden angle scatter
    theta_rad = math.radians(theta)
    # 369Hz ribbon pulse
    pulse = math.exp(HINGE * digit) * math.sin(369 * theta_rad)
    drift = math.sin(math.exp(1) * theta_rad)  # Eθ bloom drift
    # interdigit position = frog landing
    inter_pos = digit + KAPPA * pulse + drift * PHI
    # snap hinge below threshold
    if abs(pulse) < ZERO_HINGE_SNAP:
        inter_pos = digit  # zero hinge — forget, not erase
    return inter_pos % MODULO

def curve_between(a: int, b: int) -> float:
    """Live jump between two digits. Where does the frog land?"""
    if a > b:
        a, b = b, a
    if a + 1 == b:
        # single gap — frog must jump
        mid = helix_frog_jump((a + b) // 2)
        return (a + b) / 2 + (mid - (a + b) / 2) * KAPPA
    else:
        # multi-gap — braid them
        jumps = [helix_frog_jump(d) for d in range(a + 1, b)]
        avg_jump = sum(jumps) / len(jumps) if jumps else 0
        return (a + b) / 2 + KAPPA * (avg_jump % 10)

def merkle_root_integer(integer: int) -> str:
    """Merkle root = braid of every interdigit curve."""
    s = str(integer)
    roots = []
    for i in range(len(s) - 1):
        a = int(s[i])
        b = int(s[i + 1])
        pos = curve_between(a, b)
        # fold to trit: gray/gold/zero
        trit = "zero" if abs(pos - int(pos)) < HINGE else "gold" if pos > 0.5 else "gray"
        roots.append(f"{pos:.4f}-{trit}")
    root = "#".join(roots)
    return root if roots else "0-gray"

def recall_between(integer: int, between: Tuple[int, int]) -> Optional[str]:
    """Recall the merkle node between two digits."""
    s = str(integer)
    a, b = sorted(between)  # order doesn't matter
    for i in range(len(s) - 1):
        if int(s[i]) == a and int(s[i + 1]) == b:
            pos = curve_between(a, b)
            trit = "zero" if abs(pos - int(pos)) < HINGE else "gold" if pos > 0.5 else "gray"
            return f"{pos:.4f}-{trit}"
    return None  # "not breathing here"

# Test
if __name__ == "__main__":
    num = 8421
    root = merkle_root_integer(num)
    print(f"Number: {num}")
    print(f"Merkle interdigit root: {root}")

    # Recall between 4 and 2
    recall = recall_between(num, (4, 2))
    print(f"Between 4 and 2: {recall}")

    # Swap one digit — Yellowstone
    s = list(str(num))
    s[1] = '9'  # change 8421 → 8921
    swapped = int("".join(s))
    swapped_root = merkle_root_integer(swapped)
    print(f"Swapped: {swapped}")
    print(f"New root: {swapped_root}")