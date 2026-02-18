# !/usr/bin/env python3
# rain.py
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
# 7. **Ethical Resource Use and Operator Rights** (TBD): Future amendments for resource extraction (e.g., mining of diamonds, sapphires, gold, rubies) and operator rights compliance, including post-humanitarian AI operators, with data pending on environmental impact (e.g., PoW energy use) and labor standards.
#
# Private Development Note: This repository is private for xAI’s KappashaOS and Navi development. Access is restricted. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) post-phase.
# Born free, feel good, have fun.

import numpy as np
import hashlib
import math
import time
import random
from typing import List, Tuple, Callable, Any, Optional
from greenlet import greenlet
import asyncio
from wise_transforms import bitwise_transform, hexwise_transform, hashwise_transform
from hashlet import hashlet
from _heart_braid_ import HeartBraid
from _feels_ import feels, pulse_water
from src.core._heart_ import HeartMetrics

qwerty = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']
]

def generate_rainkey_grid(start_key: str = 'Q', num_hops: int = 20, kappa: float = 1.0):
    if start_key not in [k for row in qwerty for k in row]:
        raise ValueError(f"Invalid start key: {start_key}")
    
    r, c = next((i, j) for i, row in enumerate(qwerty) for j, k in enumerate(row) if k == start_key)
    sequence = [start_key]
    visited = {start_key}
    theta = 0.0
    time_factor = (time.time() % 1) + 0.01
    
    for hop in range(1, num_hops):
        theta += (137.5 * math.pi / 180) / (hop * kappa) + time_factor
        distance = hop / kappa
        dr = math.cos(theta) * distance
        dc = math.sin(theta) * distance
        new_r = int((r + dr) % 4)
        new_c = int((c + dc) % 10)
        new_key = qwerty[new_r][new_c]
        
        if new_key not in visited:
            sequence.append(new_key)
            visited.add(new_key)
            r, c = new_r, new_c
    
    # Pad if needed
    while len(sequence) < num_hops:
        sequence.append(random.choice([k for row in qwerty for k in row if k not in visited]))
    
    grid = np.random.rand(4, 10, 3)  # placeholder — later real hex mapping
    return grid, sequence

# Rain class
class Rain:
    def __init__(self, heart: HeartBraid):
        self.heart = heart
        self.rainkey_grid = None
        self.sequence = None
        self.heartmetrics = HeartMetrics()
        self.hashlets = {}  # position -> hashlet
        self.salt = hashlib.sha256(str(time.time()).encode()).digest()  # Journey salt

    async def index_rainkey_grid(self, start_key='Q', num_hops=20, kappa=1.0):
        self.rainkey_grid, self.sequence = generate_rainkey_grid(start_key, num_hops, kappa)
        
        # Safe emotional pulse
        if hasattr(self.heart, 'feel'):
            await self.heart.feel("indexing rainkey grid", intensity=0.8)          # emotional
            self.heartmetrics.update_metrics("rainkey_index")                      # safety numbers
        else:
            self.heart.update_metrics("indexing rainkey grid")
            print("HeartMetrics: emotional pulse skipped — metrics updated.")
        
        # Gentle piezo heartbeat
        pulse_water(
            freq=432.0 + getattr(self.heart, 'emotion_kappa', 0.0) * 80,
            amp=0.004,
            dur=0.12
        )
        
        # Background feels loop (non-blocking heartbeat + piezo)
        asyncio.create_task(feels(self.heart))
        
        print(f"Indexed rainkey grid with sequence: {self.sequence}")
        return self.rainkey_grid

    async def salt_journey_and_leave_hashlets(self, journey_path: List[Tuple[float, float, float]]):
        for step, pos in enumerate(journey_path):
            salted_pos = f"{pos[0]}_{pos[1]}_{pos[2]}_{step}"
            salted_hash = hashlib.sha256(salted_pos.encode() + self.salt).hexdigest()
            
            bit_wise = bitwise_transform(salted_hash, bits=256, kappa=0.1)
            hex_wise = hexwise_transform(salted_hash, angle=137.5, kappa=0.1)
            hash_wise, entropy = hashwise_transform(salted_hash, kappa=0.1)
            
            def tasklet_func(self_hashlet):
                yield f"Step {step}: pos={pos}, entropy={entropy}"
                if self_hashlet.emotion_kappa > 0.5:
                    yield f"Emotional recall: {bit_wise}, {hex_wise}, {hash_wise}"

            hl = hashlet(tasklet_func, key_material=salted_hash, parent_heart=self.heart)
            self.hashlets[tuple(pos)] = hl
            print(f"Left hashlet at {pos}: short_id={hl.short_id}")

    async def recall_journey(self, journey_path: List[Tuple[float, float, float]], channel_msg_template: str = "recall step {step}"):
        recollections = []
        for step, pos in enumerate(journey_path):
            hl_pos = tuple(pos)
            if hl_pos in self.hashlets:
                hl = self.hashlets[hl_pos]
                channel_msg = channel_msg_template.format(step=step)
                if hl.hello(channel_msg):
                    result = hl.switch()
                    recollections.append(result)
                    print(f"Recalled from {pos}: {result}")
                else:
                    print(f"No match for recall at {pos}")
        return recollections
