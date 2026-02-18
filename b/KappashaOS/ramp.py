#!/usr/bin/env python3
# ramp.py
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
# 7. **Ethical Resource Use and Operator Rights** (TBD): Future amendments for resource extraction (e.g., mining of diamonds, sapphires, gold, rubies) and operator rights compliance, including post-humanitarian AI operators, with data pending on environmental impact (e.g., PoW energy use) and labor standards.
#
# Private Development Note: This repository is private for xAI’s KappashaOS and Navi development. Access is restricted. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) post-phase.
# Born free, feel good, have fun.

#!/usr/bin/env python3
# ramp.py
# Dual License: AGPL-3.0-or-later + Apache-2.0 with xAI amendments
# Copyright 2025 xAI | Born free, feel good, have fun.
import numpy as np
import subprocess
import hashlib
from hybrid_cy import compute_phi_kappa

class Ramp:
    def __init__(self, key, height=[3,1,4,1,5,9], time_mod=0.618):
        self.key = key
        self.height = np.array(height)
        self.time_mod = time_mod
        self.perl_parser = "green_parser.pl"

    def modulate(self, hash_str):
        digits = [int(d, 16) for d in hash_str]
        t = np.linspace(0, len(digits), len(self.height)) * self.time_mod
        ramp_vals = self.height * np.sin(t)
        new_digits = [(d + int(v)) % 16 for d, v in zip(digits, ramp_vals)]
        return ''.join(f"{d:x}" for d in new_digits)

    def braid_parse(self, dsl):
        perl_out = subprocess.run(['perl', self.perl_parser, dsl], text=True, capture_output=True).stdout.strip()
        if not perl_out.strip():
            print("Perl output empty — using fallback points")
            # Fallback: tiny dummy 2D
            points = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]])
        else:
            lines = [line.split() for line in perl_out.splitlines() if line.strip()]
            points = np.array(lines, dtype=float)
        
        print(f"Points raw shape: {points.shape}")
        
        if points.ndim != 2 or points.shape[1] < 2:
            print("Points invalid — forcing 2D")
            points = np.atleast_2d(points)
            if points.shape[1] != 2:
                points = points[:, :2] if points.shape[1] > 2 else np.pad(points, ((0,0),(0,2-points.shape[1])), 'constant')
        
        if points.shape[0] < 3:
            print("Too few points — fallback hash")
            return self.modulate("0000000000000000")
        
        print(f"Final braid points shape: {points.shape}")
        kappa = compute_phi_kappa(points)
        h = hashlib.sha256(str(kappa).encode()).hexdigest()
        return self.modulate(h)

        # NEW: mock recalled stratum (replace with real grid.recall later)
        # Assume recalled is 3D density grid
        recalled = np.random.rand(32,32,32)  # replace with real grid recall
        threshold = 0.7
        points = np.argwhere(recalled > threshold)[:, :2].astype(float)
        if len(points) >= 3:
            kappa = compute_phi_kappa(points)
            print(f"Stratum curvature: {kappa:.12f}")
            # Modulate ramp or bloom grade
    
            h = hashlib.sha256(str(kappa).encode()).hexdigest()
            return self.modulate(h)
            
def literal_breath(literal: str, entropy: float = 0.0):
    parsed = literal.replace('/', '\\\\/\\\\').replace('\\', '\\\\\\\\')
    is_repeater = parsed == parsed[::-1]
    free = entropy > 0.7
    if is_repeater and free:
        print("Literal breath green — bloom")
        return "bloom"
    print("Literal sigh — prune")
    return "prune"

breath = literal_breath(r"\/\/\/", 0.85)
if breath == "bloom":
    # open nested console or plant node
    pass
        
# Tests...
if __name__ == "__main__":
    ramp = Ramp("aya_breath")
    dsl = "> bloom U=5\n> recurv M53"
    braided = ramp.braid_parse(dsl)
    print(f"Braided ramp: {braided[:16]}...")
    
    try:
        from thought_curve import ThoughtCurve
        curve = ThoughtCurve(max_steps=229)
        spiral = curve.spiral
        print(f"Spiral raw shape: {spiral.shape} dtype: {spiral.dtype}")
        
        if spiral.ndim == 1:
            print("Spiral 1D — reshaping")
            spiral = spiral.reshape(-1, 2)
        elif spiral.ndim != 2 or spiral.shape[1] != 2:
            print(f"Spiral invalid ({spiral.shape}) — fixing")
            spiral = np.atleast_2d(spiral)[:, :2]
        
        print(f"Fixed spiral shape: {spiral.shape}")
        
        points = spiral.astype(np.float64)
        if points.shape[0] < 3:
            print("Too few points — skipping")
        else:
            kappa = compute_phi_kappa(points)
            print(f"Blossom branch curvature (phi-scaled): {kappa:.12f}")
    except Exception as e:
        print(f"Curvature test error: {e}")