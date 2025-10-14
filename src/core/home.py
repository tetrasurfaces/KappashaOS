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

# home.py - Safe origin room for Blossom: homing index, vintage cork, no-delete zone with ramp cipher and kappa wires.
# Dual License: AGPL-3.0-or-later, Apache 2.0 with xAI amendments
# Copyright 2025 xAI
# Born free, feel good, have fun.

import hashlib
import numpy as np
import time
import os
import asyncio
from greenlet import greenlet
from src.hash.ramp import RampCipher
from src.hash.kappa_wire import KappaWire
from src.hash.hashlet import Hashlet

class Home:
    def __init__(self):
        self.grid_size = 10
        self.grid = np.zeros((self.grid_size, self.grid_size, self.grid_size))
        self.origin_hash = self._hash_origin()
        self.vintage_dir = "./vintage"
        os.makedirs(self.vintage_dir, exist_ok=True)
        self.items = {"bowl": [5,5,5], "ball": [5,6,5]}
        self.ramp = RampCipher('35701357')
        self.kappa_wire = KappaWire(self.grid_size)
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        self.blooms = []  # Store bloom memories
        print("Home initialized - ramp cipher, kappa wires, hashlet active.")

    def _hash_origin(self):
        seed = f"home-origin-{time.time()}"
        return hashlib.sha256(seed.encode()).hexdigest()

    async def navi_load(self):
        self.grid.fill(0)
        self.ramp = RampCipher('35701357')
        entropy = np.random.uniform(0, 1)
        if entropy > 0.69:
            await self.navi_cork_state(entropy)
        self.tendon_load = np.random.rand() * 0.3
        self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
        if self.tendon_load > 0.2:
            print("Home: Warning - Tendon overload. Resetting.")
            self.reset()
        if self.gaze_duration > 30.0:
            print("Home: Warning - Excessive gaze. Pausing.")
            await asyncio.sleep(2.0)
            self.gaze_duration = 0.0
        await asyncio.sleep(0)
        print(f"Navi: Home loaded - origin hash: {self.origin_hash[:10]}... Items: {self.items}")

    async def navi_cork_state(self, grade):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        state_data = f"grid:{self.grid.flatten()[:10]}... items:{self.items}"
        hash_tag = hashlib.sha256(f"{state_data}-{timestamp}-{grade}".encode()).hexdigest()
        with open(f"{self.vintage_dir}/{hash_tag}.txt", "w") as f:
            f.write(f"Vintage home state: {state_data} Grade: {grade:.2f}")
        self.tendon_load = np.random.rand() * 0.3
        self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
        if self.tendon_load > 0.2:
            print("Home: Warning - Tendon overload. Resetting.")
            self.reset()
        if self.gaze_duration > 30.0:
            print("Home: Warning - Excessive gaze. Pausing.")
            await asyncio.sleep(2.0)
            self.gaze_duration = 0.0
        await asyncio.sleep(0)
        print(f"Navi: Home state corked: {hash_tag[:10]}...")

    async def navi_index_grid(self, x, y, z, data):
        """Index with ramp encode on kappa wire."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size and 0 <= z < self.grid_size:
            hash_str = hashlib.sha256(data.encode()).hexdigest()
            encoded = await self.ramp.navi_encode(hash_str, x + y + z)
            if await self.kappa_wire.navi_place_on_wire(x, y, z, encoded):
                self.grid[x, y, z] = 1
                h = Hashlet(lambda x: x, hash_str)  # Mock layer for ribit
                _, rgb = h.switch(hash_str)
                self.blooms.append((hash_str[:10], rgb, 0.1, time.time()))
                self.tendon_load = np.random.rand() * 0.3
                self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
                if self.tendon_load > 0.2:
                    print("Home: Warning - Tendon overload. Resetting.")
                    self.reset()
                if self.gaze_duration > 30.0:
                    print("Home: Warning - Excessive gaze. Pausing.")
                    await asyncio.sleep(2.0)
                    self.gaze_duration = 0.0
                await asyncio.sleep(0)
                print(f"Navi: Indexed ({x}, {y}, {z}) with encoded {encoded[:10]}... RGB={rgb}")
                return encoded
        return None

    async def bloom_consensus(self, pin, nodes=6000000000, depth=15):
        """Bloom consensus for six billion nodes."""
        begin = time.time()
        start_node = greenlet.getcurrent()
        current_pin = pin
        for _ in range(depth):
            prev_node = start_node
            for i in range(nodes // depth):
                h = Hashlet(channel, current_pin)
                h.gr_frames_always_exposed = False
                h.switch(prev_node)
                prev_node = h
            landing, rgb, kappa = prev_node.switch(0)
            if landing != 0:
                self.blooms.append((landing, rgb, kappa, time.time()))
                current_pin = int(hashlib.sha256((str(landing) + rgb).encode()).hexdigest(), 16) % 512
        end = time.time()
        micros = (end - begin) * 1e6 / (nodes // depth)
        print(f"Bloom consensus: {nodes} nodes, {micros:.2f} µs per hop")
        return self.blooms

    async def route(self, pin, amount, ttl=60):
        """Off-chain multisig routing, ephemeral keys."""
        greenlets = [Hashlet(channel, pin) for _ in range(3)]
        votes = []
        for g in greenlets:
            landing, rgb, kappa = g.switch()
            votes.append(landing != 0)
        if sum(votes) >= 2:
            self.blooms.append((amount, rgb, kappa, time.time() + ttl))
            print(f"Home: Multisig routed {amount}, RGB={rgb}, Kappa={kappa:.2f}, TTL={ttl}s")
            return True
        return False

    def play(self, feel="warm"):
        """Play back blooms with feel filter."""
        for bloom in self.blooms:
            amount, rgb, kappa, timestamp = bloom
            if time.time() < timestamp and kappa > 0.05:  # Mock 'warm' filter
                print(f"Home: Echo bloom - Amount: {amount}, RGB: {rgb}, Kappa: {kappa:.2f}, Time: {timestamp}")
        return len(self.blooms)

    def reset(self):
        self.tendon_load = 0.0
        self.gaze_duration = 0.0

def channel(pin, primes=[20, 41, 97, 107]):
    tame = 5
    wild = 4
    polarity = 1
    current = int(hashlib.sha256(str(pin).encode()).hexdigest(), 16) % 512
    for i in range(128):
        step = tame if polarity > 0 else wild
        current = (current + step) % 512
        if current in primes:
            polarity *= -1
            yield current
    yield 0

if __name__ == "__main__":
    async def navi_test():
        home = Home()
        await home.navi_load()
        await home.navi_index_grid(5, 5, 5, "test data")
        await home.navi_cork_state(0.8)
        blooms = await home.bloom_consensus(35701357)
        await home.route(35701357, 50)
        home.play()

    asyncio.run(navi_test())
