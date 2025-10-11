# Dual License:
# - For core software: AGPL-3.0-or-later licensed. -- xAI fork, 2025
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
#   with xAI amendments for safety and physical use (prohibits misuse in weapons or hazardous applications;
#   requires ergonomic compliance; revocable for unethical use). See http://www.apache.org/licenses/LICENSE-2.0
#   for details, with the following xAI-specific terms appended.
#
# Copyright 2025 xAI
#
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
#
# xAI Amendments for Physical Use:
# 1. **Physical Embodiment Restrictions**: Use with devices is for non-hazardous purposes only. Harmful mods are prohibited, with license revocable by xAI.
# 2. **Ergonomic Compliance**: Limits tendon load to 20%, gaze to 30 seconds (ISO 9241-5).
# 3. **Safety Monitoring**: Real-time tendon/gaze checks, logged for audit.
# 4. **Revocability**: xAI may revoke for unethical use (e.g., surveillance).
# 5. **Export Controls**: Sensor devices comply with US EAR Category 5 Part 2.
# 6. **Open Development**: Hardware docs shared post-private phase.
#
# Private Development Note: This repository is private for xAI’s KappashaOS and Navi development. Access is restricted. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) post-phase.

#!/usr/bin/env python3
# rainkey_v2.0.py

import math
import argparse
import hashlib
import mpmath
import numpy as np
import time

mpmath.mp.dps = 19

# wise_transforms functions
def bitwise_transform(data, bits=16):
    """BitWise: Raw binary ops (mask, NOT flip) for -1 pruning."""
    int_data = int.from_bytes(data.encode(), 'big') % (1 << bits)
    mask = (1 << bits) - 1
    mirrored = (~int_data) & mask
    return bin(mirrored)[2:].zfill(bits)

def hexwise_transform(data, angle=137.5):
    """HexWise: String/hex rotations/mirrors for 0 privacy (reversible)."""
    hex_data = data.encode().hex()
    mirrored = hex_data + hex_data[::-1]
    shift = int(angle % len(mirrored))
    rotated = mirrored[shift:] + mirrored[:shift]
    return rotated

def hashwise_transform(data):
    """HashWise: SHA1664 sponge perms for +1 culture (immutable entropy)."""
    base_hash = hashlib.sha512(data.encode()).digest()
    mp_state = mpmath.mpf(int(base_hash.hex(), 16))
    for _ in range(4):
        mp_state = mpmath.sqrt(mp_state) * mpmath.phi
    partial = mpmath.nstr(mp_state, 1664 // 4)
    final_hash = hashlib.sha256(partial.encode()).hexdigest()
    entropy = int(mpmath.log(mp_state, 2))
    return final_hash, entropy

# Expanded QWERTY layout with shift (capitals), ctrl (numbers), alt (symbols)
qwerty = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']
]

# Shift for capitals
cap_qwerty = [[k.upper() for k in row] for row in qwerty]

# Ctrl for numbers/symbols (mock: reuse numbers + symbols)
ctrl_qwerty = [['!', '@', '#', '$', '%', '^', '&', '*', '(', ')'],
               cap_qwerty[1],
               cap_qwerty[2],
               cap_qwerty[3]]

# Alt for symbols (mock: special symbols)
alt_qwerty = [['`', '~', '-', '=', '[', ']', '\\', '{', '}', '|'],
              qwerty[1],
              qwerty[2],
              qwerty[3]]

# All keys (base + shift + ctrl + alt)
all_keys = qwerty + cap_qwerty + ctrl_qwerty + alt_qwerty
key_pos = {key: (r, c) for r, row in enumerate(all_keys) for c, key in enumerate(row)}

# Strict hex mapping (0-9, a-f only, mapped to all keys)
hex_map = {k: hex((r * len(all_keys[0]) + c) % 16)[2:] for r, row in enumerate(all_keys) for c, k in enumerate(row)}

def generate_spiral_sequence(start_key, time_factor, num_hops=20, kappa=1.0):
    """Generate a deterministic forward spiral sequence based on theta and time."""
    if start_key not in key_pos:
        raise ValueError(f"Invalid start key: {start_key}")
    
    r, c = key_pos[start_key]
    sequence = [start_key]
    visited = {start_key}
    theta = 0.0
    
    for hop in range(1, num_hops):
        theta += (137.5 * math.pi / 180) / (hop * kappa) + time_factor
        distance = hop / kappa
        dx = math.cos(theta) * distance
        dy = math.sin(theta) * distance
        new_r = int((r + dy) % len(all_keys))
        new_c = int((c + dx) % len(all_keys[0]))
        new_key = all_keys[new_r][new_c]
        
        if new_key not in visited and new_key != sequence[0]:
            sequence.append(new_key)
            visited.add(new_key)
            r, c = new_r, new_c
        else:
            break  # Deterministic stop on loop
    
    # Pad with deterministic hash-based keys
    while len(sequence) < num_hops:
        hash_input = f"{len(sequence)}_{theta:.6f}"
        hash_val = int(hashlib.sha256(hash_input.encode()).hexdigest(), 16) % len(key_pos)
        new_key = list(key_pos.keys())[hash_val]
        if new_key not in visited and new_key != start_key:
            sequence.append(new_key)
            visited.add(new_key)
        else:
            break
    
    # Check for input=output loop
    input_key = start_key.encode()
    output_key = hashlib.sha256(''.join(sequence).encode()).hexdigest()[:16].encode()
    if input_key == output_key:
        print("Input=output detected-flipping theta.")
        theta += math.pi  # Reroll theta for divergence
        return generate_spiral_sequence(start_key, time_factor + math.pi, num_hops, kappa)
    
    return sequence

def pollard_kangaroo_on_grid(start_pos, target_pos, steps=800):
    """Enhanced Pollard's Kangaroo with dynamic jumps including diagonals."""
    grid_rows, grid_cols = len(all_keys), len(all_keys[0])
    order_approx = grid_rows * grid_cols
    m = int(math.sqrt(order_approx)) + 15
    jumps = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    tame_map = {}
    x_t, y_t = start_pos
    for i in range(m):
        pos = (x_t % grid_rows, y_t % grid_cols)
        if pos not in tame_map:
            tame_map[pos] = i
        j = hash(str(pos) + str(i)) % len(jumps)
        dr, dc = jumps[j]
        x_t = (x_t + dr) % grid_rows
        y_t = (y_t + dc) % grid_cols
    x_w, y_w = target_pos
    for i in range(m * 4):
        pos = (x_w % grid_rows, y_w % grid_cols)
        if pos in tame_map:
            return tame_map[pos] + i
        j = hash(str(pos) + str(i)) % len(jumps)
        dr, dc = jumps[j]
        x_w = (x_w + dr) % grid_rows
        y_w = (y_w + dc) % grid_cols
    return abs(start_pos[0] - target_pos[0]) + abs(start_pos[1] - target_pos[1])

def generate_spectrum_kappa(sequence):
    """Generate strict hex spectrum kappa (0-9, a-f), padded to 16 chars."""
    spectrum = ''.join(hex_map.get(k.upper(), '0') for k in sequence)
    spectrum = (spectrum + '0' * (16 - len(spectrum)))[:16]
    return f"0x{spectrum.lower()}"

def map_hex_color_grid(sequence, hop_distance, spectrum_kappa):
    """Map a hex color grid based on spiral hop path vectors using wise transformations."""
    grid_size = (len(all_keys), len(all_keys[0]))
    color_grid = np.zeros(grid_size + (3,))  # RGB grid
    
    # Apply wise transformations to spectrum_kappa
    bit_wise = bitwise_transform(spectrum_kappa)
    hex_wise = hexwise_transform(spectrum_kappa)
    hash_wise, _ = hashwise_transform(spectrum_kappa)
    
    for i in range(len(sequence) - 1):
        current = sequence[i]
        next_key = sequence[i + 1]
        current_pos = key_pos[current]
        next_pos = key_pos[next_key]
        
        # Hop vector (direction and magnitude)
        vector = (next_pos[0] - current_pos[0], next_pos[1] - current_pos[1])
        vector_str = f"{vector[0]},{vector[1]}"
        
        # Transform vector to color
        hash_color, _ = hashwise_transform(vector_str)
        r = int(hash_color[:2], 16) % 256 / 255
        g = int(hash_color[2:4], 16) % 256 / 255
        b = int(hash_color[4:6], 16) % 256 / 255
        color = (r, g, b)
        
        # Apply color to grid at current position
        color_grid[current_pos[0], current_pos[1]] = color
    
    return color_grid

def main():
    parser = argparse.ArgumentParser(description="Rainkey v2.0: QWERTY Hexwise Input Generator with Spiral Rainbow")
    parser.add_argument("--start-key", type=str, default="Q", help="Starting key on QWERTY")
    parser.add_argument("--num-hops", type=int, default=20, help="Number of hops in sequence")
    parser.add_argument("--kappa", type=float, default=1.0, help="Kappa for flattening")
    args = parser.parse_args()

    # Time factor unique to moment (forward only, >0)
    time_factor = (time.time() % 1) + 0.01

    # Generate sequence
    sequence = generate_spiral_sequence(args.start_key.upper(), time_factor, args.num_hops, args.kappa)
    print("Generated Sequence:", sequence)

    # Kangaroo hop distance
    start_pos = key_pos[sequence[0]]
    target_pos = key_pos[sequence[-1]]
    hop_distance = pollard_kangaroo_on_grid(start_pos, target_pos)
    print(f"Kangaroo hop distance to end key: {hop_distance}")

    # Spectrum kappa
    spectrum_kappa = generate_spectrum_kappa(sequence)
    print("Spectrum Kappa:", spectrum_kappa)

    # Map color grid (visualize omitted for now)
    color_grid = map_hex_color_grid(sequence, hop_distance, spectrum_kappa)

if __name__ == "__main__":
    main()
