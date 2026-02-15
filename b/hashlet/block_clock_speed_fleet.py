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
import requests  # pip install requests if needed
import sympy as sp
from kappawise import murmur32, kappa_coord
from wise_transforms import bitwise_transform, hexwise_transform, hashwise_transform
from hybrid import HybridGreenText
from ribit_telemetry import ribit_generate
from ghost_hand import GhostHand
from secure_hash_two import secure_hash_two

mpmath.mp.dps = 19

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

# Real Bitcoin poll
last_height = 0
last_time = 0
last_diff = 0.0
def get_latest_block():
    global last_height, last_time, last_diff
    try:
        resp = requests.get('https://blockchain.info/latestblock')
        data = resp.json()
        height = data['height']
        block_time = data['time']
        resp_diff = requests.get('https://blockchain.info/q/getdifficulty')
        diff = float(resp_diff.text)
        if height > last_height:
            delta = block_time - last_time if last_time else 600
            print(f"New block {height} at {block_time}, delta {delta}s, diff {diff}")
            last_height = height
            last_time = block_time
            last_diff = diff
            return height, block_time, delta, diff
        return None, None, None, None
    except:
        print("heat spike-flinch")  # Api fail
        return None, None, None, None

# Hashloop
def hashloop(start='0', salt=''):
    nonce = start
    while True:
        input_str = str(nonce) + salt
        hash_val = hashlib.sha256(input_str.encode()).hexdigest()
        yield hash_val
        nonce = hash_val

# Node loop for concurrency
def node_loop(node_id, gossip_queue, salt='', user_id='she'):
    generator = hashloop(salt=salt)
    latencies = []
    coords_accum = []
    kappas = []
    hgt = HybridGreenText()
    vibe_model = TetraVibe()
    ghost = GhostHand()
    tick_i = 0
    prev_diff = 0.0
    while True:
        height, block_time, delta, diff = get_latest_block()
        if delta is None and tick_i > 0 and time.time() - last_time > 1800:
            print("heat spike-flinch")  # Timeout no new
            time.sleep(60)
            continue
        if delta is not None:
            thimble = sp.symbols('thimble')
            eq = sp.Eq(sp.sin(thimble * diff / last_diff), delta / 600.0)
            sols = sp.solve(eq, thimble)
            if not sols:
                print("heat spike-flinch")  # No sol
            else:
                print(f"Thimble sol: {sols[0]}")
            curl = ghost.gimbal_flex(delta) if diff < prev_diff else False
            if curl:
                print("Gimbal flex drop")
            prev_diff = diff
            rod_pressure = delta / 600.0
            tension = ghost.rod_whisper(rod_pressure)
            print(f"Rod tension: {tension}")
        else:
            delta = 600.0  # Default avg
        vibe, _ = vibe_model.friction_vibe(np.array([0,0,0]), np.array([delta/600, 0, 0]))
        interval = delta * vibe
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
        salted_strand = secure_hash_two(hybrid_strand, 'she_key', str(block_time))
        coord = kappa_coord(user_id + str(node_id), height if height else tick_i)
        coords_accum.append(coord[:2])
        if len(coords_accum) > 2:
            points = np.array(coords_accum)
            kappa_mean = compute_phi_kappa(points)
            kappas.append(kappa_mean)
            scaled = hgt.scale_curvature(np.array(kappas))
            interval = scaled[-1] / 10.0
            interval *= 1 + (kappa_mean / 10)  # Friction vibe
        else:
            interval = 600.0
        log_text = f"> Node {node_id} Tick {tick_i}: {salted_strand[:16]}... at {coord} (ent {ent})"
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
        ribit_int, state, color = ribit_generate(str(diff))
        print(f"Diff RIBIT: {ribit_int}, State: {state}, Color: {color}")
        time.sleep(max(interval, 60.0))  # Min 1min poll
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
