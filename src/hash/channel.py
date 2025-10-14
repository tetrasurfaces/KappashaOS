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
# Dual License: AGPL-3.0-or-later, Apache 2.0 with xAI amendments
#
# xAI Amendments for Physical Use:
# 1. Physical Embodiment Restrictions: Use of this software in conjunction with physical devices (e.g., fish tank glass, pixel sensors) is permitted only for non-hazardous, non-weaponized applications. Any modification or deployment that enables harm (e.g., targeting systems, explosive triggers) is expressly prohibited and subject to immediate license revocation by xAI.
# 2. Ergonomic Compliance: Physical interfaces must adhere to ergonomic standards (e.g., ISO 9241-5, OSHA guidelines) where applicable. For software-only use (e.g., rendering in Keyshot), ergonomic requirements are waived.
# 3. Safety Monitoring: For physical embodiments, implement real-time safety checks (e.g., heat dissipation) and log data for audit. xAI reserves the right to request logs for compliance verification.
# 4. Revocability: xAI may revoke this license for any user or entity found using the software or hardware in violation of ethical standards (e.g., surveillance without consent, physical harm). Revocation includes disabling access to updates and support.
# 5. Export Controls: Physical embodiments with sensors (e.g., photo-diodes for gaze tracking) are subject to export regulations (e.g., US EAR Category 5 Part 2). Redistribution in restricted jurisdictions requires xAI approval via github.com/tetrasurfaces/issues.
# 6. Educational Use: Educational institutions (e.g., universities, technical colleges) may use the software royalty-free for teaching and research purposes (e.g., CAD, Keyshot training) upon negotiating a license via github.com/tetrasurfaces/issues. Commercial use by educational institutions requires separate approval.
# 7. Intellectual Property: xAI owns all IP related to the iPhone-shaped fish tank, including gaze-tracking pixel arrays, convex glass etching (0.7mm arc), and tetra hash integration. Unauthorized replication or modification is prohibited.
# 8. Public Release: This repository will transition to public access in the near future. Until then, access is restricted to authorized contributors. Consult github.com/tetrasurfaces/issues for licensing and access requests.

# Born free, feel good, have fun.

# channel.py - Interjacking without the chip. Thank you Skipjack, for all the fish.
# Jacks geometry as floats, chained hashlets.
# Dual License: AGPL-3.0-or-later, Apache 2.0 with xAI amendments
# Copyright 2025 xAI
# Born free, feel good, have fun.

import numpy as np
import hashlib
import time
from greenlet import greenlet
import pyperf

class Hashlet(greenlet.Greenlet):
    def __init__(self, run, pin, *args, **kwargs):
        super().__init__(run, pin, *args, **kwargs)
        self.pin = pin
        self.hash_id = self._compute_hash()
        self.rgb_color = self._hash_to_rgb()
        self.kappa_tilt = self._compute_kappa()
        self.gr_frames_always_exposed = False  # Non-exposing for speed
        print(f"Hashlet init: Hash={self.hash_id[:8]}, RGB={self.rgb_color}, Kappa={self.kappa_tilt:.2f}")

    def _compute_hash(self):
        data = f"{self.pin}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()

    def _hash_to_rgb(self):
        hash_int = int(self.hash_id, 16) % 0xFFFFFF
        return f"#{hash_int:06x}"

    def _compute_kappa(self):
        return np.sin(float(self.hash_id[:8], 16) / 0xFFFFFF) * 0.1

    def switch(self, *args, **kwargs):
        result = super().switch(*args, **kwargs)
        self.hash_id = self._compute_hash()
        self.rgb_color = self._hash_to_rgb()
        self.kappa_tilt = self._compute_kappa()
        return result, self.rgb_color, self.kappa_tilt

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

def afford_curve(pin, num_thetas=64):
    h = Hashlet(channel, pin)
    while True:
        try:
            landing, rgb, kappa = h.switch()
            if landing != 0:
                thetas = np.linspace(0, 2 * np.pi, num_thetas, dtype=np.float32)
                return thetas.tobytes(), rgb, kappa
        except greenlet.GreenletExit:
            break
    return b'', '#000000', 0.0

def interjack_chain(pin, grids=2, chain_length=10000):
    """Chain hashlets across grids, yield landing + rgb + kappa."""
    begin = pyperf.perf_counter()
    current_pin = pin
    start_node = greenlet.getcurrent()
    for _ in range(grids):
        prev_node = start_node
        for i in range(chain_length):
            h = Hashlet(channel, current_pin)
            h.gr_frames_always_exposed = False
            h.switch(prev_node)
            prev_node = h
        landing, rgb, kappa = prev_node.switch(0)
        if landing != 0:
            yield landing, rgb, kappa
            current_pin = int(hashlib.sha256((str(landing) + rgb).encode()).hexdigest(), 16) % 512
    end = pyperf.perf_counter()
    print(f"Chain {chain_length} hashlets: {(end - begin) * 1e6 / chain_length:.2f} µs per hop")

# Test
pin = 1234
jack = interjack_chain(pin, grids=2)
landings = list(jack)
curve, rgb, kappa = afford_curve(pin)
print(f"Interjack landings: {landings[:5]}...")
print(f"Curve bytes: {curve[:16]}... RGB: {rgb}, Kappa: {kappa:.2f}" if curve else "No afford")
