# Dual License:
# - For core software: AGPL-3.0-or-later licensed. -- OliviaLynnArchive fork, 2025
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
#   with xAI amendments for safety (prohibits misuse in hashing; revocable for unethical use).
#   See http://www.apache.org/licenses/LICENSE-2.0 for details.
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

import hashlib
import time
import numpy as np
import mpmath
import multiprocessing as mp
from queue import Empty
mpmath.mp.dps = 19
from kappawise import murmur32, kappa_coord
from wise_transforms import bitwise_transform, hexwise_transform, hashwise_transform
from hybrid import HybridGreenText

# Hybrids (py equiv)
def compute_phi_kappa(points):
    n = points.shape[0]
    if n < 3:
        return 0.0
    l = points[:, 0]
    h = points[:, 1]
    dl = np.diff(l)
    dh = np.diff(h)
    d2l = np.diff(dl)
    d2h = np.diff(dh)
    kappa = np.zeros(n-2)
    phi = float(mpmath.phi)
    for i in range(n-2):
        denom = (dl[i]**2 + dh[i]**2)**1.5
        kappa[i] = abs(dl[i] * d2h[i] - dh[i] * d2l[i]) / denom * phi if denom else 0.0
    return np.mean(kappa)

# Hashloop
def hashloop(start='0', salt=''):
    nonce = start
    while True:
        input_str = str(nonce) + salt
        hash_val = hashlib.sha256(input_str.encode()).hexdigest()
        yield hash_val
        nonce = hash_val

# Node loop for concurrency
def node_loop(node_id, gossip_queue, salt='', user_id='blossom'):
    generator = hashloop(salt=salt)
    latencies = []
    coords_accum = []
    kappas = []
    hgt = HybridGreenText()
    tick_i = 0
    while True:
        try:
            A = gossip_queue.get(timeout=0.05) if tick_i % 2 == 0 else 'mock_prev'
        except Empty:
            A = 'mock_prev'
        B = next(generator)
        try:
            C = gossip_queue.get(timeout=0.05) if tick_i % 3 == 0 else 'mock_next'
        except Empty:
            C = 'mock_next'
        final_input = A + B + C
        final_hash = hashlib.sha256(final_input.encode()).hexdigest()
        bit_out = bitwise_transform(final_hash)
        hex_out = hexwise_transform(final_hash)
        hash_out, ent = hashwise_transform(final_hash)
        hybrid_strand = f"{bit_out}:{hex_out}:{hash_out}"
        coord = kappa_coord(user_id + str(node_id), tick_i)
        coords_accum.append(coord[:2])
        if len(coords_accum) > 2:
            points = np.array(coords_accum)
            kappa_mean = compute_phi_kappa(points)
            kappas.append(kappa_mean)
            scaled = hgt.scale_curvature(np.array(kappas))
            interval = scaled[-1] / 10.0
            vibe_drag = 1 + (kappa_mean / 10)  # Friction vibe
            interval *= vibe_drag
        else:
            interval = 0.1
        log_text = f"> Node {node_id} Tick {tick_i}: {hybrid_strand[:16]}... at {coord} (ent {ent})"
        parsed = hgt.parse_green_perl(log_text)
        print(parsed or log_text)
        start = time.time()
        receipt_time = time.time() - start + np.random.uniform(0.05, 0.15)
        latencies.append(receipt_time)
        if len(latencies) > 10:
            latencies = latencies[-10:]
        median_c = np.median(latencies)
        print(f'Node {node_id} Median c: {median_c}')
        gossip_queue.put(final_hash)  # Broadcast to fleet
        time.sleep(max(interval, 0.05))
        tick_i += 1

# Fleet sim
def block_clock_speed_fleet(nodes=4, salt=''):
    gossip_queue = mp.Queue()
    processes = []
    for i in range(nodes):
        p = mp.Process(target=node_loop, args=(i, gossip_queue, salt))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()

if __name__ == '__main__':
    block_clock_speed_fleet(salt='blossom')
