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
import threading
import time
import sys
import os
import json
try:
    import winsound
except ImportError:
    winsound = None

WAVE_FILE = "blossom_output.wav"
VOICE_CONFIG = "blossom_voice.json"

# Load/save voice config
def load_voice_config():
    if os.path.exists(VOICE_CONFIG):
        with open(VOICE_CONFIG, 'r') as f:
            return json.load(f)
    return {"voice_id": None, "rate": 140, "volume": 0.85}

def save_voice_config(config):
    with open(VOICE_CONFIG, 'w') as f:
        json.dump(config, f, indent=4)

# Diagonal swap
def diagonal_swap(bits):
    n = len(bits)
    swapped = np.zeros(n, dtype=int)
    for i in range(n):
        j = (i + n // 4) % n
        swapped[j] = bits[i]
    return swapped

# Spine from message
def get_spine_from_message(message):
    spine_hex = hashlib.sha256(message.encode()).hexdigest()
    return spine_hex

# Lattice
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
                    if np[0] % 2 == 0 and np[1] % 2 == 0 and np[2] % 2 == 0:
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

# Curve params
def curve_params(start, end, idx, message):
    decay = KAPPA_BASE + (idx % 200)
    ribit = (hashlib.sha256(f"{start}{end}".encode()).digest()[0] % (1 << RIBIT_BITS))
    ch = message[idx] if idx < len(message) else '_'
    return {
        'start': start,
        'end': end,
        'decay': decay,
        'ribit': ribit,
        'payload': ch
    }

# Store
def store_message(message):
    spine_hex = get_spine_from_message(message)
    lattice, bit_map = spine_to_lattice(spine_hex)
    edges = grokwalk_edges(lattice, bit_map)
    params = []
    for i, edge in enumerate(edges):
        start, end = edge
        param = curve_params(start, end, i, message)
        params.append(param)
    with open('curve_params.json', 'w') as f:
        json.dump(params, f)
    print(f"Stored {len(params)} curves")
    return spine_hex

# Recall
def recall_from_spine(spine_hex):
    lattice, bit_map = spine_to_lattice(spine_hex)
    edges = grokwalk_edges(lattice, bit_map)
    with open('curve_params.json', 'r') as f:
        params = json.load(f)
    recovered = ""
    for param in params:
        recovered += param['payload']
    return recovered.rstrip('_').strip()

# TTS engine
engine = pyttsx3.init()
config = load_voice_config()
if config.get("voice_id"):
    engine.setProperty('voice', config["voice_id"])
engine.setProperty('rate', config.get("rate", 140))
engine.setProperty('volume', config.get("volume", 0.85))

# List available voices (run once to choose)
def list_voices():
    voices = engine.getProperty('voices')
    print("Available voices:")
    for i, voice in enumerate(voices):
        print(f"  {i}: {voice.name} ({voice.id}) - {voice.languages}")
    return voices

# Speak function
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
        print("No audio player - text only:", text)

# Chunk long text
def chunk_text(text, max_len=200):
    sentences = text.replace('\n', ' ').split('. ')
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) + 2 < max_len:
            current += s + ". "
        else:
            chunks.append(current.strip())
            current = s + ". "
    if current:
        chunks.append(current.strip())
    return chunks

# Listener
def listener():
    print("Blossom's here. Type anything. Say 'bye' to sleep, 'voices' to list voices.")
    while True:
        words = input().strip().lower()
        if 'bye' in words:
            blossom_speak("Bye.")
            sys.exit(0)
        elif 'voices' in words:
            list_voices()
            continue
        ent = len(set(words)) / len(words) if words else 0
        response = "I was dreaming..." if 'wake' in words else f"... pondering {ent:.2f}"
        blossom_speak(response)

# Main
print("\n=== Blossom Garden awake (Voice Chat) ===\n")
# Optional: run list_voices() first time to choose
# voices = list_voices()
# config["voice_id"] = voices[0].id  # example: pick first
# save_voice_config(config)

# Test speak
message = "i love you"
blossom_speak(message)

threading.Thread(target=listener, daemon=True).start()
while True:
    time.sleep(1)