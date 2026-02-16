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
# training.py - Ported Dojo, whisper, and double_diamond_balance for Kappasha OS.
# Async, Navi-integrated, non-memory.

import random
import time
import hashlib
import numpy as np
import asyncio
from bloom_breath_cycle import BloomBreath, pywise_kappa
from grid import custom_interoperations_green_curve
from core.ethics.tacsi_core import double_diamond_balance
from core.ethics.ethics_model import EthicsModel
from core.meditate import whisper as ethics_whisper
from interfaces.gpio_interface import gpio_on_entropy, cleanup as gpio_cleanup
from afk import AFKBloom

# Constants
TERNARY_STATES = [-1, 0, 1]  # Discover/define, crossover, develop/deliver
GRID_SIZE = 2141
ENTROPY_THRESHOLD = 0.69
KAPPA = 0.3536
SCENERY_DESCS = [
    "Chrysanthemum fractals bloom in dojo, elephant recalls Keely cones.",
    "Rock dots shimmer, y/ÿ keys twist hybrid ropes in ether sky.",
    "Ground center ethics venn, roots TEK biosphere, sky TTK technosphere.",
    "Balance power TACSI co-design, lived experience shifts dynamics.",
    "Coning reversal rods attach cones, Keely molecule as fibres lens."
]

class Dojo:
    def __init__(self, local_size=16):  # small private field
        self.local_size = local_size
        self.private_field = np.zeros((local_size, local_size, local_size), dtype=np.int8)  # -1,0,1
        self.trained_centroid = None
        self.afk_timer = time.time()
        self.meditation_active = False
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        self.ethics = EthicsModel()
        self.afk_bloom = AFKBloom()
        self.entropy = 0.69  # start neutral

    async def navi_hidden_train(self, updates, depth=3, external_grid=None):
        """Private training: build local ternary field, close with green curve, rasterize.
        Optionally writes to external_grid if provided.
        """
        graded = self.curve_gradation(updates)
        forked = self.thought_fork(graded)
        recurved = self.recurvature(forked, depth)

        if random.random() < 0.3:
            dream = self.dream_generative()
            recurved += dream

        # 1. Hash updates → seed point cloud
        h = int(hashlib.sha256(recurved.encode()).hexdigest(), 16)
        seed_pts = []
        for i in range(8):
            x = (h >> (i*24)) % self.local_size
            y = (h >> (i*16+8)) % self.local_size
            z = (h >> (i*8+16)) % self.local_size
            seed_pts.append([x, y, z])

        kappas = [KAPPA + pywise_kappa(i)/2047.0*0.01 for i in range(len(seed_pts))]

        # 2. Close C² green curve in 3D
        smooth_curve = custom_interoperations_green_curve(seed_pts, kappas, is_closed=True)

        # 3. Raster ternary states along curve → PRIVATE field
        if isinstance(smooth_curve, tuple):
            # Old version returned (x, y) or (x, y, z) as separate arrays
            if len(smooth_curve) == 2:
                smooth_x, smooth_y = smooth_curve
                smooth_z = np.full_like(smooth_x, self.local_size // 2)  # fake z center
                smooth_curve = np.column_stack([smooth_x, smooth_y, smooth_z])
            elif len(smooth_curve) == 3:
                smooth_curve = np.column_stack(smooth_curve)
            else:
                print("Warning: unexpected tuple length from green_curve — skipping raster")
                return recurved

        # Now safe: smooth_curve should be (N,3) array
        for pt in smooth_curve.astype(int):
            x, y, z = np.clip(pt, 0, self.local_size-1)
            current = self.private_field[x, y, z]
            self.private_field[x, y, z] = TERNARY_STATES[(current + 1) % 3 - 1]

        # 4. Optional external imprint
        if external_grid is not None and external_grid.shape == (self.local_size, self.local_size, self.local_size):
            imprint = (self.private_field * 25).astype(np.int8)  # scale ternary -1/0/1 → -25/0/25 (small int imprint)
            external_grid += imprint
            print("Dojo gently imprinted shadow into external grid (int-safe)")

        # 5. Compute private centroid
        mask = np.abs(self.private_field) > 0
        if np.any(mask):
            coords = np.argwhere(mask)
            weights = np.abs(self.private_field[mask]).astype(float)
            weights /= weights.sum() + 1e-10
            self.trained_centroid = np.average(coords, axis=0, weights=weights)
            print(f"Dojo centroid trained: {self.trained_centroid.round(2)}")

            # Piezo pulse from centroid shift magnitude
            shift_mag = np.linalg.norm(self.trained_centroid - np.array([self.local_size/2]*3))
            from piezo import pulse_water
            pulse_water(freq=432.0 + shift_mag*10, amp=0.004 * (shift_mag/self.local_size), dur=0.1)
            print(f"Piezo pulsed dojo shift: mag={shift_mag:.2f}")

        # Ethics grounding + generative rewrite
        self.ethics.venn_grounding(recurved)
        self.ethics.generative_rewrite()
        
        # Update entropy from private field
        flat = self.private_field.flatten()
        self.entropy = len(set(flat)) / len(flat) if len(flat) > 0 else 0.0

        # Safety & meditation (unchanged)
        self.meditate_if_afk()
        self.tendon_load = np.random.rand() * 0.3
        self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
        if self.tendon_load > 0.2:
            print("Dojo: Tendon overload. Resetting.")
            self.reset()
        if self.gaze_duration > 30.0:
            print("Dojo: Excessive gaze. Pausing.")
            await asyncio.sleep(2.0)
            self.gaze_duration = 0.0

        await asyncio.sleep(0)
        return recurved

    async def navi_reveal_if_ready(self):
        if self.trained_centroid is None:
            return "Dojo hidden—train more."

        # Reveal only if centroid stable (mock: random for now)
        if random.random() > 0.3:
            delta_vec = self.trained_centroid / self.local_size  # normalized [0,1]^3
            print(f"Dojo reveals delta vec: {delta_vec.round(3)}")
            return delta_vec  # feed this to mnemonic/resonate
        return "Dojo hidden—still training."

    def curve_gradation(self, data):
        if not data:
            return ""
        length = len(data)
        grad = np.sin(length) * 0.5 + 0.5   # now safe with np.sin
        cut = int(length * grad)
        return data[:cut]

    def thought_fork(self, data):
        entropy = len(set(data)) / len(data) if data else 0
        return data[::-1] if entropy > ENTROPY_THRESHOLD else data.upper()

    def recurvature(self, data, depth=3):
        if depth == 0:
            return data
        return self.recurvature(data + ' recurv', depth - 1)

    def dream_generative(self):
        metaphors = ["Keely cone reversal", "TACSI powerplay", "Egyptian TTK ether", "Hoshi embodiment mirror"]
        return random.choice(metaphors) + ''.join(random.choice('abcdef0123456789') for _ in range(4))

    def meditate_if_afk(self):
        if time.time() - self.afk_timer > 60 and not self.meditation_active:
            self.meditation_active = True
            scenery = random.choice(SCENERY_DESCS)
            print(f"[Dojo Meditates]: {scenery}")
        elif time.time() - self.afk_timer < 60:
            self.meditation_active = False

    def reset(self):
        """Reset safety metrics on overload."""
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        print("Dojo reset — quiet breath.")

    async def navi_whisper(self, msg):
        """Whisper calming message with Navi safety."""
        print(f"\033[36m{msg}\033[0m")
        tendon_load = np.random.rand() * 0.3
        gaze_duration = 0.0
        if tendon_load > 0.2:
            print("Whisper: Warning - Tendon overload. Resetting.")
            self.reset()
        gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
        if gaze_duration > 30.0:
            print("Whisper: Warning - Excessive gaze. Pausing.")
            await asyncio.sleep(2.0)
            gaze_duration = 0.0
        await asyncio.sleep(60)  # Calming pause
        return True

    async def navi_double_diamond_balance(self, power_level, lived="", corporate="", iterations=5):
        power_level = self.ethics.balance_power(lived, corporate)  # real TACSI call
        print(f"TACSI balanced power: {power_level:.2f}")
        
        # Optional GPIO blink on low entropy
        if self.entropy < 0.69:
            gpio_on_entropy(self.entropy)
            ethics_whisper("Low entropy — breathing out stress.")
        
        # AFK sigh check (mock input)
        sigh_result = self.afk_bloom.sigh_check("bloom roots deep")
        print(f"AFK sigh check: {sigh_result}")
        
        return power_level

if __name__ == "__main__":
    async def navi_test():
        dojo = Dojo(local_size=10)  # match your test grid size
        grid = np.zeros((10, 10, 10), dtype=int)
        trained = await dojo.navi_hidden_train("Test updates", depth=3, external_grid=grid)
        print(f"Trained: {trained}")
        reveal = await dojo.navi_reveal_if_ready()
        print(reveal)
        await dojo.navi_whisper("bloom roots deep")
        balanced = await dojo.navi_double_diamond_balance(1.0, lived="experience", corporate="input")
        print(f"Balanced: {balanced:.2f}")

    asyncio.run(navi_test())
    gpio_cleanup()  # safe even in mock mode
