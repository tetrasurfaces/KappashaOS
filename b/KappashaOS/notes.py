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

# Keyboard grid - all rows exactly 15 cols (pad with '')
GRID_ROWS = 6
GRID_COLS = 15

raw_grid = [
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '\\', 'Bksp'],
    ['Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '|', ''],
    ['Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', 'Enter', '', ''],
    ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Shift', '', '', '', ''],
    ['Ctrl', 'Win', 'Alt', ' ', ' ', ' ', ' ', ' ', ' ', 'Alt', 'Win', 'Menu', 'Ctrl', '', ''],
    ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', '', '', '']
]

# Ensure every row has exactly 15 elements
grid = np.array([row[:GRID_COLS] + [''] * (GRID_COLS - len(row)) for row in raw_grid], dtype='<U10')

def char_to_grid_index(c):
    flat = grid.flatten()
    try:
        return np.where(flat == c.lower())[0][0]
    except IndexError:
        return -1

def grid_index_to_char(idx):
    flat = grid.flatten()
    if 0 <= idx < len(flat):
        return flat[idx]
    return '?'

def hash_to_deltas(hash_hex, num_chars):
    h = int(hash_hex, 16)
    deltas = []
    for i in range(num_chars):
        delta = (h >> (i % 64)) & 0x3F  # 6 bits
        deltas.append(delta)
        h = (h * 6364136223846793005 + 1) & ((1 << 64) - 1)  # LCG mix
    return np.array(deltas)

def reconstruct_note_from_hash(hash_hex, expected_len=10):
    deltas = hash_to_deltas(hash_hex, expected_len)
    path = []
    current_idx = 0
    path.append(grid_index_to_char(current_idx))
    for step in range(1, expected_len):
        best_char = '?'
        best_score = float('inf')
        for trial_delta in range(64):
            next_idx = (current_idx + trial_delta) % len(grid.flatten())
            score = abs(trial_delta - deltas[step])
            if score < best_score:
                best_score = score
                best_char = grid_index_to_char(next_idx)
        path.append(best_char)
        current_idx = char_to_grid_index(best_char)
    return ''.join(path)

# Test
hash_hex = "d833c000ca8293dd4e61c3b4e4f44c61f74f62f9c2ae71ba16af6be96d6f4ca1"
reconstructed = reconstruct_note_from_hash(hash_hex, expected_len=100)
print("Reconstructed (approx):", reconstructed[:200])