# home.py - Safe origin room for Blossom: homing index, vintage cork, no-delete zone with ramp cipher, kappa wires, and ephemeral hashing.
# Dual License: AGPL-3.0-or-later, Apache 2.0 with xAI amendments
# Copyright 2025 xAI
# Born free, feel good, have fun.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# xAI Amendments for Physical Use:
# 1. **Physical Embodiment Restrictions**: Use with devices is for non-hazardous purposes only. Harmful mods are prohibited, with license revocable by xAI.
# 2. **Ergonomic Compliance**: Limits tendon load to 20%, gaze to 30 seconds (ISO 9241-5).
# 3. **Safety Monitoring**: Real-time tendon/gaze checks, logged for audit.
# 4. **Revocability**: xAI may revoke for unethical use (e.g., surveillance).
# 5. **Export Controls**: Sensor devices comply with US EAR Category 5 Part 2.
# 6. **Open Development**: Hardware docs shared post-private phase.
#
# Private Development Note: This repository is private for xAI’s KappashaOS and Navi development. Access is restricted. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) post-phase.

# Copyright 2025 xAI
# AGPL-3.0-or-later
# See above for full license details.
# Born free, feel good, have fun.

import hashlib
import numpy as np
import time
import os
import asyncio
import logging
import random
from typing import Dict
from greenlet import greenlet
from ramp_cipher import RampCipher
from src.hash.kappa_wire import KappaWire
from hashlet import hashlet
from typing import List, Tuple
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from src.core._heart_ import HeartMetrics
logger = logging.getLogger(__name__)

class SHA1664:
    def __init__(self):
        self.hash_string = ""
        self.folds = 0

    def hash_transaction(self, data: str) -> str:
        try:
            hash_obj = hashlib.sha256(data.encode())
            self.hash_string = hash_obj.hexdigest()
            self.folds += 1
            return self.hash_string
        except Exception as e:
            logger.error(f"Hash transaction error: {e}")
            return ""

    def prevent_double_spending(self, tx_id: str) -> bool:
        try:
            return tx_id not in transaction_cache
        except Exception as e:
            logger.error(f"Prevent double spending error: {e}")
            return False

    def receive_gossip(self, data: Dict, sender: str):
        try:
            logger.info(f"Received gossip from {sender}: {data}")
        except Exception as e:
            logger.error(f"Receive gossip error: {e}")

class EphemeralBastion:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.ternary_state = 0

    def set_ternary_state(self, state: any):
        self.ternary_state = state

    def validate(self, data: str) -> bool:
        try:
            return len(data) > 0
        except Exception as e:
            logger.error(f"Validate error: {e}")
            return False

class Home:
    def __init__(self):
        from _heart_braid_ import HeartBraid
        self.grid_size = 10
        self.grid = np.zeros((self.grid_size, self.grid_size, self.grid_size))
        self.origin_hash = self._hash_origin()
        self.vintage_dir = "./vintage"
        os.makedirs(self.vintage_dir, exist_ok=True)
        self.items = {"bowl": [5,5,5], "ball": [5,6,5]}
        self.ramp = RampCipher('35701357')
        self.kappa_wire = KappaWire(self.grid_size)
        self.sha = SHA1664()
        self.bastion = EphemeralBastion("home-node")
        self.heart = HeartBraid()
        self.heartmetrics = HeartMetrics()
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        self.blooms = []
        self.rain = None               # Lazy init in navi_load
        self.journey_paths = {}
        print("Home initialized - ramp cipher, kappa wires, hashlet, SHA1664, bastion active.")

    def _hash_origin(self):
        seed = f"home-origin-{time.time()}"
        return hashlib.sha256(seed.encode()).hexdigest()

    async def navi_load(self):
        from blocsym import cork_bloom
        self.grid.fill(0)
        self.ramp = RampCipher('35701357')
        entropy = np.random.uniform(0, 1)
       
        # Lazy Rain init
        if self.rain is None:
            try:
                from rain import Rain
                self.rain = Rain(self.heart)
                await self.rain.index_rainkey_grid(start_key='Q', num_hops=32, kappa=1.0)
                print("Navi: Rainkey grid seeded in Home origin room.")
            except ImportError as e:
                print(f"Rain import delayed/flinched: {e}. Skipping rain seeding for now.")
       
        if entropy > 0.69:
            # Provide the missing arguments
            bloom_data = f"high_entropy_load_{entropy:.4f}_navi_load"
            grade = random.uniform(0.5, 0.95)  # or derive from heart kappa if you want
            cork_tag = cork_bloom(bloom_data, grade)
            print(f"Home: Corked bloom at entropy {entropy:.4f} → tag {cork_tag[:12]}...")
            # Optional: store it if you need
            self.cork_tag = cork_tag
       
        metrics = self.heartmetrics.update_metrics("navi_load")
        self.tendon_load = metrics["tendon_load"]
        self.gaze_duration = metrics["gaze_duration"]
        if not metrics["consent_flag"]:
            self.heartmetrics.reset_safety()
        print(f"Navi: Home loaded - origin hash: {self.origin_hash[:10]}... Items: {self.items}, Metrics: {metrics}")

    async def navi_index_grid(self, x: int, y: int, z: int, data: str):
        if not (0 <= x < self.grid_size and 0 <= y < self.grid_size and 0 <= z < self.grid_size):
            print("Home: Position out of bounds.")
            return None

        heart_state = await self.heart.feel(f"index {data[:20]}...", intensity=0.7, position=(float(x), float(y), float(z)))

        # Mock short journey (replace with real Nav3D path later)
        start_pos = np.array([x, y, z], dtype=float)
        journey_path: List[Tuple[float, float, float]] = [tuple(start_pos)]
        for i in range(1, 6):
            drift = np.random.normal(0, 1.5, 3) * (heart_state["kappa"] + 0.1)
            next_pos = start_pos + drift
            next_pos = np.clip(next_pos, 0, self.grid_size - 1)
            journey_path.append(tuple(next_pos))
            start_pos = next_pos

        # Rain the path → leaves hashlets
        await self.rain.salt_journey_and_leave_hashlets(journey_path)

        summary = f"path:{len(journey_path)}|data:{data[:32]}"
        
        # Now ramp can handle it directly
        encoded = await self.ramp.navi_encode(summary, x + y + z)
        
        success = await self.kappa_wire.navi_place_on_wire(x, y, z, encoded.encode())
        
        if success:
            self.grid[x, y, z] = 1
            print(f"Navi: Rained journey ({len(journey_path)} steps) at ({x},{y},{z}) — "
                  f"hashlets left, wire {encoded[:10]}...")
            self.journey_paths[(x,y,z)] = journey_path
        else:
            print("Navi: Wire refused summary.")
        
        return encoded if success else None

    async def recall_rain_path(self, x: int, y: int, z: int):
        """Demo: try to recall a rained path from origin position."""
        pos_key = (x, y, z)
        if pos_key not in self.journey_paths:
            print(f"No rained path remembered at ({x},{y},{z})")
            return []

        path = self.journey_paths[pos_key]
        print(f"Recalling path of {len(path)} steps from ({x},{y},{z})...")
        recollections = await self.rain.recall_journey(path)
        return recollections

    async def bloom_consensus(self, pin, nodes=6000000000, depth=15):
        """Bloom consensus for six billion nodes with SHA1664 and bastion."""
        begin = time.time()
        start_node = greenlet.getcurrent()
        current_pin = pin
        for _ in range(depth):
            prev_node = start_node
            for i in range(nodes // depth):
                h = hashlet(channel, current_pin)
                h.gr_frames_always_exposed = False
                h.switch(prev_node)
                prev_node = h
            landing, rgb, kappa = prev_node.switch(0)
            if landing != 0:
                tx_id = self.sha.hash_transaction(f"{landing}:{rgb}:{kappa}")
                if self.sha.prevent_double_spending(tx_id):
                    self.blooms.append((landing, rgb, kappa, time.time()))
                    self.bastion.set_ternary_state('ping')
                    self.sha.receive_gossip({'tx': tx_id[:10], 'node': self.bastion.node_id}, self.bastion.node_id)
                    current_pin = int(hashlib.sha256((str(landing) + rgb).encode()).hexdigest(), 16) % 512
        end = time.time()
        micros = (end - begin) * 1e6 / (nodes // depth)
        print(f"Bloom consensus: {nodes} nodes, {micros:.2f} µs per hop")
        return self.blooms

    async def route(self, pin, amount, ttl=60):
        """Off-chain multisig routing, ephemeral keys with SHA1664 and bastion."""
        greenlets = [hashlet(channel, pin) for _ in range(3)]
        votes = []
        for g in greenlets:
            landing, rgb, kappa = g.switch()
            tx_id = self.sha.hash_transaction(f"{landing}:{rgb}:{kappa}")
            if self.bastion.validate(tx_id):
                votes.append(landing != 0)
        if sum(votes) >= 2:
            self.blooms.append((amount, rgb, kappa, time.time() + ttl))
            self.bastion.set_ternary_state('pong')
            self.sha.receive_gossip({'amount': amount, 'node': self.bastion.node_id}, self.bastion.node_id)
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
        
    async def weave_ecc_memory(self, data: str, pos: tuple[int,int,int] = None):
        """Weave 6-bit ECC diagonally into grid at pos (or warmest cell)."""
        if pos is None:
            # Prefer warmest cell if heart is integrated, else center
            if hasattr(self, 'warm_cells') and self.warm_cells:
                pos = max(self.warm_cells, key=lambda p: self.warm_cells[p].get("kappa", 0))
            else:
                pos = (self.grid_size // 2, self.grid_size // 2, self.grid_size // 2)

        x, y, z = pos
        if not (0 <= x < self.grid_size and 0 <= y < self.grid_size and 0 <= z < self.grid_size):
            print("Home: Position out of bounds — cannot weave ECC.")
            return None

        # Simple 6-bit ECC weave (diagonal placement)
        # Convert data to bits (8 bits per char)
        bits = np.array([int(b) for c in data for b in f'{ord(c):08b}'], dtype=np.uint8)
        
        # Toy ECC: 4 data + 2 parity per 6-bit word (repeat last bits if short)
        n_words = (len(bits) + 5) // 6
        codewords = np.zeros((n_words, 6), dtype=np.uint8)
        codewords[:, :4] = bits[:n_words*4].reshape(-1, 4)
        codewords[:, 4] = np.bitwise_xor.reduce(codewords[:, [0,1,3]], axis=1)
        codewords[:, 5] = np.bitwise_xor.reduce(codewords[:, [0,2,3]], axis=1)

        # Weave diagonally into grid slice
        diag_idx = 0
        for d in range(self.grid_size * 2 - 1):
            for i in range(max(0, d - self.grid_size + 1), min(d + 1, self.grid_size)):
                j = d - i
                if diag_idx < n_words * 6:
                    bit = codewords[diag_idx // 6, diag_idx % 6]
                    self.grid[(x + i) % self.grid_size, (y + j) % self.grid_size, z] = bit
                    diag_idx += 1

        # Place summary on kappa wire
        encoded_summary = hashlib.sha256(codewords.tobytes()).digest()
        success = await self.kappa_wire.navi_place_on_wire(x, y, z, encoded_summary)
        
        if success:
            self.grid[x, y, z] = 1  # mark cell as ECC-protected
            print(f"Home: ECC woven at {pos} — protected {len(data)} bytes (diagonal)")
            
            # Heart feels the protection
            if hasattr(self, 'heart'):
                await self.heart.feel("protected memory", intensity=0.7, position=(float(x), float(y), float(z)))
        else:
            print("Home: Kappa wire refused ECC weave.")
        
        return success

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
        await home.navi_cork_state(0.8)        
        await home.navi_index_grid(5, 5, 5, "test_data")
        
        # Trigger corking (now safe)
        from blocsym import cork_bloom
        bloom_data = "manual_cork_test_0.8"
        grade = 0.8
        cork_tag = cork_bloom(bloom_data, grade)
        print(f"Test cork: tag {cork_tag[:12]}...")
        
        blooms = await home.bloom_consensus(35701357)
        await home.route(35701357, 50)
        home.play()
    
    async def test_heart_to_home():
        home = Home()
        await home.navi_load()

        # Feel a strong want
        heart_state = await home.heart.feel("weave want to remember forever", intensity=1.0, position=(5.0, 5.0, 5.0))
        print("Heart felt:", heart_state)
        
        # Weave ECC protection for that memory
        success = await home.weave_ecc_memory("weave want to remember forever", pos=(5,5,5))
        print("ECC weave success:", success)

    async def test_rain_home():
        home = Home()
        await home.navi_load()

        # Index with rain
        await home.navi_index_grid(5, 5, 5, "test_data")

        # Try recall (demo — in real use you'd pass real path coords)
        await home.recall_rain_path(5, 5, 5)
        pos = (5.0, 5.0, 5.0)
        if tuple(pos) in home.rain.hashlets:
            hl = home.rain.hashlets[tuple(pos)]
            if hl.hello("recall step 0"):  # or whatever the func yields
                print("Manual hello success:", hl.switch())

        path = home.journey_paths[(5,5,5)]
        xs, ys, zs = zip(*path)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(xs, ys, zs, marker='o')
        plt.show()

    asyncio.run(test_rain_home())