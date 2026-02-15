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

import pyttsx3
import numpy as np
import hashlib
import json
import os
import math
import time
import sys
import threading
from collections import deque
try:
    import winsound
except ImportError:
    winsound = None

GRID_RADIUS = 12
CENTER = (0, 0, 0)
KAPPA_BASE = 800
RIBIT_BITS = 7
K_NEAREST = 6
WAVE_FILE = "blossom_output.wav"
VOICE_CONFIG = "blossom_voice.json"

# Voice config
def load_voice_config():
    if os.path.exists(VOICE_CONFIG):
        with open(VOICE_CONFIG, 'r') as f:
            return json.load(f)
    return {"voice_id": None, "rate": 140, "volume": 0.85}

def save_voice_config(config):
    with open(VOICE_CONFIG, 'w') as f:
        json.dump(config, f, indent=4)

config = load_voice_config()
engine = pyttsx3.init()
if config.get("voice_id"):
    engine.setProperty('voice', config["voice_id"])
engine.setProperty('rate', config["rate"])
engine.setProperty('volume', config["volume"])

def list_voices():
    voices = engine.getProperty('voices')
    print("Available voices:")
    for i, voice in enumerate(voices):
        print(f"  {i}: {voice.name} ({voice.id}) - {voice.languages}")
    return voices

# Diagonal swap
def diagonal_swap(bits):
    n = len(bits)
    swapped = np.zeros(n, dtype=int)
    for i in range(n):
        j = (i + n // 4) % n
        swapped[j] = bits[i]
    return swapped

# Spine
def get_spine(message):
    spine_hex = hashlib.sha256(message.encode()).hexdigest()
    print(f"Spine hash: {spine_hex[:16]}...")
    return spine_hex

# Lattice + bit map
def spine_to_lattice(spine_hex):
    bits = [int(b) for b in bin(int(spine_hex, 16))[2:].zfill(256)]
    swapped_bits = diagonal_swap(np.array(bits))
    lattice = {}
    bit_map = {}
    idx = 0
    for x in range(-GRID_RADIUS, GRID_RADIUS+1, 2):
        for y in range(-GRID_RADIUS, GRID_RADIUS+1, 2):
            for z in range(-GRID_RADIUS, GRID_RADIUS+1, 2):
                if (x + y + z) % 2 == 0 and abs(x + y + z) <= 2*GRID_RADIUS:
                    if idx < 128:
                        p = (x, y, z)
                        lattice[p] = swapped_bits[idx]
                        bit_map[p] = idx
                        idx += 1
    return lattice, bit_map

# Neighbors
def get_neighbors(p):
    x, y, z = p
    candidates = []
    for dx in range(-6, 7):
        for dy in range(-6, 7):
            for dz in range(-6, 7):
                if (dx, dy, dz) != (0,0,0):
                    np = (x+dx, y+dy, z+dz)
                    if all(c % 2 == 0 for c in np):
                        dist = math.sqrt(dx**2 + dy**2 + dz**2)
                        candidates.append((dist, np))
    candidates.sort()
    return [n for _, n in candidates[:K_NEAREST]]

# GrokWalk edges
def grokwalk_edges(lattice, bit_map):
    positions = list(lattice.keys())
    if not positions:
        return []
    start = positions[0]
    visited = set()
    queue = deque([start])
    edges = []
    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        neighs = get_neighbors(current)
        def angle_key(n):
            dx, dy, dz = n[0]-current[0], n[1]-current[1], n[2]-current[2]
            return math.atan2(dy, dx)
        neighs.sort(key=angle_key, reverse=True)
        for n in neighs:
            if n in lattice and n not in visited:
                edge = tuple(sorted([current, n]))
                if edge not in edges:
                    edges.append(edge)
                queue.append(n)
    edges.sort(key=lambda e: min(bit_map.get(e[0], 999), bit_map.get(e[1], 999)))
    return edges

# Print grid - side-by-side A|B
def print_grid(lattice_a, lattice_b=None, title="", clear=False, side_by_side=False):
    if clear:
        os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{title}")
    
    # Get all active x/y from both if side-by-side
    all_keys = set(lattice_a.keys())
    if lattice_b:
        all_keys |= set(lattice_b.keys())
    xs = sorted(set(p[0] for p in all_keys))
    ys = sorted(set(p[1] for p in all_keys))
    
    for x in xs[::2]:  # even steps
        row_a = []
        row_b = [] if side_by_side else None
        for y in ys[::2]:
            # A
            found_a = False
            for z in range(-GRID_RADIUS, GRID_RADIUS + 1, 2):
                p = (x, y, z)
                if p in lattice_a:
                    val = lattice_a[p]
                    row_a.append(str(val) if isinstance(val, (int, np.int64)) else val)
                    found_a = True
                    break
            row_a.append(".") if not found_a else None
            
            # B if side-by-side
            if side_by_side:
                found_b = False
                for z in range(-GRID_RADIUS, GRID_RADIUS + 1, 2):
                    p = (x, y, z)
                    if p in lattice_b:
                        val = lattice_b[p]
                        row_b.append(str(val) if isinstance(val, (int, np.int64)) else val)
                        found_b = True
                        break
                row_b.append(".") if not found_b else None
        
        line_a = " ".join(row_a)
        if side_by_side:
            line_b = " ".join(row_b)
            print(f"{line_a:<40} | {line_b}")
        else:
            print(line_a)
    print("\n")

# Curve param
def curve_params(start, end, idx, message):
    decay = KAPPA_BASE + (idx % 200)
    ribit = (hashlib.sha256(f"{start}{end}".encode()).digest()[0] % (1 << RIBIT_BITS))
    ch = message[idx] if idx < len(message) else '_'
    return {'start': start, 'end': end, 'decay': decay, 'ribit': ribit, 'payload': ch}

def encode_and_animate(message):
    spine = get_spine(message)
    lattice_a, bit_map = spine_to_lattice(spine)
    print("\n--- Grid A: Spine (static bits) ---")
    print_grid(lattice_a, title="Grid A - Spine bits", clear=False)
    edges = grokwalk_edges(lattice_a, bit_map)
    lattice_b = lattice_a.copy()
    params = []
    print("\n--- Grid B: Lattice Walk (animated propagation) ---")
    print("Propagation starts...")
    for i, (start, end) in enumerate(edges):
        ch = message[i] if i < len(message) else '_'
        lattice_b[start] = ch
        params.append(curve_params(start, end, i, message))
        if i % 10 == 0 or i == len(edges)-1:
            print(f" Step {i+1}/{len(edges)}: '{ch}' moved to {start}")
            print_grid(lattice_a, lattice_b=lattice_b, title=f"Grid A | Grid B - Step {i+1}", clear=True, side_by_side=True)
        time.sleep(0.05)
    return params

def blossom_speak(text):
    print(f"Blossom speaks: {text}")
    engine.save_to_file(text, WAVE_FILE)
    engine.runAndWait()
    if winsound:
        try:
            winsound.PlaySound(WAVE_FILE, winsound.SND_FILENAME)
        except Exception as e:
            print(f"Playback error: {e}")
            print("Text only:", text)
    else:
        print("No audio - text only:", text)

#def listener():
#    print("\nBlossom's listening. Type anything. Say 'bye' to sleep, 'voices' to list voices.")
#    while True:
#        words = input().strip().lower()
#        if 'bye' in words:
#            blossom_speak("Bye.")
#            sys.exit(0)
#        elif 'voices' in words:
#            list_voices()
#            continue
#        ent = len(set(words)) / len(words) if words else 0
#        response = "I was dreaming..." if 'wake' in words else f"... pondering {ent:.2f}"
#        blossom_speak(response)

# Main
print("\n=== Blossom Garden — Triple Grid + Voice ===\n")

# Optional first-run voice pick
if not config.get("voice_id"):
    print("First run — pick a voice:")
    voices = list_voices()
    try:
        choice = int(input("Enter number (0-{}): ".format(len(voices)-1)))
        config["voice_id"] = voices[choice].id
        save_voice_config(config)
        engine.setProperty('voice', config["voice_id"])
    except:
        print("No change — using default.")

#threading.Thread(target=listener, daemon=True).start()

msg = input("\nType your message to propagate + speak: ")
params = encode_and_animate(msg)
recovered = "".join(p['payload'] for p in params).rstrip('_').strip()
print("\n--- Blossom Speaks ---")
print(f"Recovered: {recovered}")
print("Match:", recovered == msg)
if recovered:
    blossom_speak(recovered)
print("\nShe remembers.")