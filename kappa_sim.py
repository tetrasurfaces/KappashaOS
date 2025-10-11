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

#!/usr/bin/env python3
# kappa_sim.py - Situational awareness simulator with kappa-tilted rasterization.
# Integrates Navi and MasterHand for real-time mapping.

import simpy
import numpy as np
import asyncio
import hashlib
import time
from master_hand import MasterHand  # Local path
from wise_transforms import bitwise_transform, hexwise_transform, hashwise_transform  # Local path

class Sym:
    """Gyroscopic rig for situational tilt simulation."""
    def __init__(self):
        self.spin_rate = 0.0
        self.tilt_angle = np.array([0.0, 0.0, 0.0])
    
    def tilt(self, axis, rate):
        idx = {"x": 0, "y": 1, "z": 2}.get(axis[0].lower(), 0)
        self.tilt_angle[idx] = rate
        print(f"Tilting {axis} by {rate} degrees")
    
    def stabilize(self):
        self.tilt_angle = np.where(abs(self.tilt_angle) < 1e-6, 0.0, self.tilt_angle * 0.9)
        print("Stabilizing tilt angles:", self.tilt_angle)

class TetraVibe:
    """Vibe model for rasterization effects."""
    def friction_vibe(self, pos1, pos2, kappa=0.3):
        dist = np.linalg.norm(pos1 - pos2)
        if dist < 1e-6:
            print("heat spike-flinch")
            return 1.0, np.zeros(3)
        if dist < 0.1:
            vibe = np.sin(2 * np.pi * dist / 0.05)
            gyro = np.cross(pos1, pos2) / dist if dist > 0 else np.zeros(3)
            warp = 1 / (1 + kappa * dist)
            return vibe * warp, gyro
        return 1.0, np.zeros(3)

class KappaSim:
    def __init__(self, env):
        self.env = env
        self.gate = np.array([0, 0, 0])
        self.kappa = 0.1  # Baseline situational awareness
        self.history = []  # Kappa register
        self.lockouts = set()  # Situational tags
        self.sensors = []  # Point cloud placeholder
        self.hand = MasterHand(kappa=self.kappa)
        self.gimbal = Sym()
        self.vibe = TetraVibe()
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        print("KappaSim initialized - situational awareness with rasterization ready.")

    async def navi_sense(self):
        """Navi senses situational changes with safety checks."""
        while True:
            # Mock sensor drift
            drift = np.random.rand() * 0.1
            if drift > 0.05:
                self.kappa += 0.05
                self.hand.pulse(2)
                print(f"Navi: Hey! Kappa adjusted to {self.kappa:.3f} due to drift {drift:.2f}")

            # Safety monitoring
            self.tendon_load = np.random.rand() * 0.3
            self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
            if self.tendon_load > 0.2:
                print("KappaSim: Warning - Tendon overload. Resetting.")
                self.hand.reset()
            if self.gaze_duration > 30.0:
                print("KappaSim: Warning - Excessive gaze. Pausing.")
                await asyncio.sleep(2.0)
                self.gaze_duration = 0.0

            await asyncio.sleep(1.0 / 60)

    def register_kappa(self, incident=None):
        """Register situational kappa with hash."""
        now = time.time()
        key = hashlib.sha3_256(f"{now}{self.kappa:.2f}{incident or ''}".encode()).hexdigest()
        self.history.append((now, self.kappa, key))
        if len(self.history) > 1000:
            self.history.pop(0)
        return key

    def get_situational_kappa(self):
        """Compute real-time situational kappa."""
        if not self.history:
            return self.kappa
        last_kappa = self.history[-1][1]
        if len(self.history) > 5:
            drift = np.std([k[1] for k in self.history[-5:]])
            return last_kappa + drift
        return last_kappa

    def trigger_emergency(self, incident):
        """Respond to situational emergency."""
        self.kappa += 0.2
        self.lockouts.add(incident)
        self.hand.pulse(2)
        print(f"{incident.upper()} - Kappa now {self.kappa:.2f}")

    def auto_adjust(self, target, adjust_time=5):
        """Auto-adjust situational state."""
        yield self.env.timeout(adjust_time)
        print(f"{target} adjusted. Lockout cleared.")
        self.lockouts.discard(target)
        self.kappa -= 0.2
        self.hand.pulse(1)

    def camera_array(self):
        """Simulate sensor array with rasterized vibe effects."""
        points = np.random.rand(100, 3) * 100
        drift = np.linalg.norm(points[-1] - self.gate)
        if drift > 5:
            self.kappa += 0.05
            self.hand.pulse(3)
        vibe, gyro = self.vibe.friction_vibe(self.gate, points[-1], self.kappa)
        self.gimbal.tilt('z', gyro[2] if gyro[2] else 0.1)
        self.gimbal.stabilize()
        # Rasterize to light
        light_hash = hashlib.sha256(str(points).encode()).hexdigest()[:16]
        bit_str = bitwise_transform(light_hash)
        hex_str = hexwise_transform(light_hash)
        hash_str, entropy = hashwise_transform(light_hash)
        hybrid = f"{bit_str}:{hex_str}:{hash_str}"
        print(f"Rasterized: {hybrid} (Entropy {entropy})")
        return points

    def run_day(self):
        """Simulate a situational awareness day."""
        print(f"Day start - Situational Kappa = {self.get_situational_kappa():.3f}")
        asyncio.run(self.navi_sense())  # Start Navi loop
        yield self.env.timeout(20)
        self.trigger_emergency("sensor_drift")
        self.register_kappa("sensor_drift")
        yield self.env.process(self.auto_adjust("sensor_line"))
        self.camera_array()
        self.register_kappa()
        print(f"Day end - Situational Kappa = {self.get_situational_kappa():.3f}")

if __name__ == "__main__":
    env = simpy.Environment()
    sim = KappaSim(env)
    env.process(sim.run_day())
    env.run(until=60)
