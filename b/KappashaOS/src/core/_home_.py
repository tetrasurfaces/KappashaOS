# _home_.py - Safe origin room for Blossom: homing index, vintage cork, no-delete zone with ramp cipher, kappa wires, and ephemeral hashing.
#
# Copyright 2025 xAI
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
from typing import Dict
from greenlet import greenlet
from src.hash.ramp import RampCipher
from src.hash.kappa_wire import KappaWire
from src.hash.hashlet import Hashlet

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
        self.heart = HeartMetrics()  # Add heart metrics
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        self.blooms = []
        print("Home initialized - ramp cipher, kappa wires, hashlet, SHA1664, bastion active.")

    def _hash_origin(self):
        seed = f"home-origin-{time.time()}"
        return hashlib.sha256(seed.encode()).hexdigest()

    async def navi_load(self):
        self.grid.fill(0)
        self.ramp = RampCipher('35701357')
        entropy = np.random.uniform(0, 1)
        if entropy > 0.69:
            await self.navi_cork_state(entropy)
        metrics = self.heart.update_metrics("navi_load")
        self.tendon_load = metrics["tendon_load"]
        self.gaze_duration = metrics["gaze_duration"]
        if not metrics["consent_flag"]:
            self.heart.reset_safety()
        print(f"Navi: Home loaded - origin hash: {self.origin_hash[:10]}... Items: {self.items}, Metrics: {metrics}")

    async def navi_index_grid(self, x, y, z, data):
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size and 0 <= z < self.grid_size:
            hash_str = self.sha.hash_transaction(data)
            if not self.bastion.validate(hash_str):
                print("Bastion: Invalid data")
                return None
            encoded = await self.ramp.navi_encode(hash_str, x + y + z)
            if await self.kappa_wire.navi_place_on_wire(x, y, z, encoded):
                self.grid[x, y, z] = 1
                h = Hashlet(lambda x: x, hash_str)
                _, rgb = h.switch(hash_str)
                self.blooms.append((hash_str[:10], rgb, 0.1, time.time()))
                self.bastion.set_ternary_state('earth' if 'seed' in data else 'ping')
                self.sha.receive_gossip({'hash': hash_str[:10], 'pos': (x, y, z)}, self.bastion.node_id)
                metrics = self.heart.update_metrics(data)
                self.tendon_load = metrics["tendon_load"]
                self.gaze_duration = metrics["gaze_duration"]
                if not metrics["consent_flag"]:
                    self.heart.reset_safety()
                print(f"Navi: Indexed ({x}, {y}, {z}) with encoded {encoded[:10]}... RGB={rgb}, Metrics: {metrics}")
                return encoded
        return None

    async def bloom_consensus(self, pin, nodes=6000000000, depth=15):
        """Bloom consensus for six billion nodes with SHA1664 and bastion."""
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
        greenlets = [Hashlet(channel, pin) for _ in range(3)]
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
        await home.navi_index_grid(5, 5, 5, "test_data")
        await home.navi_cork_state(0.8)
        blooms = await home.bloom_consensus(35701357)
        await home.route(35701357, 50)
        home.play()
    asyncio.run(navi_test())
