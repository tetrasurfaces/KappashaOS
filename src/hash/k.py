#  KappashaOS/core/hash/k.py
#  License::
#  - For core software: AGPL-3.0-or-later licensed. -- xAI fork, 2025
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
# 
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
# 
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/>.
# 
#  - For hardware/embodiment interfaces (if any):see xAI amendments after contacting Tetrasurfaces at github.com/tetrasurfaces/issues for license (revokable).
#    with xAI amendments for safety and physical use (prohibits misuse in weapons or hazardous applications;
#    requires ergonomic compliance; revocable for unethical use). See http://www.apache.org/licenses/LICENSE-2.0
#    for details, with the following xAI-specific terms appended.
# 
#  Copyright 2025 xAI
# 

#
#  xAI Amendments for Physical Use:
#  1. **Physical Embodiment Restrictions**: Use with devices is for non-hazardous purposes only. Harmful mods are prohibited, with license revocable by xAI.
#  2. **Ergonomic Compliance**: Limits tendon load to 20%, gaze to 30 seconds (ISO 9241-5).
#  3. **Safety Monitoring**: Real-time tendon/gaze checks, logged for audit.
#  4. **Revocability**: xAI may revoke for unethical use (e.g., surveillance).
#  5. **Export Controls**: Sensor devices comply with US EAR Category 5 Part 2.
#  6. **Open Development**: Hardware docs shared post-private phase.
# 
#  Private Development Note: This repository is private for xAI’s KappashaOS and Navi development. Access is restricted. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) post-phase.


import numpy as np

def fibonacci_spiral(laps=18, ratio=1.618):
    theta = np.linspace(0, 2 * np.pi * laps, 1000)
    r = np.exp(theta / ratio) / 10  # scaled for mm
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = theta / (2 * np.pi)  # depth in laps
    return np.stack((x, y, z), axis=1)

def tonage_map(point, delays=[0.2, 0.4, 0.6]):
    norm = np.linalg.norm(point)
    idx = int(norm % 3)  # cycle through delays
    color = ['red', 'yellow', 'green'][idx]
    delay = delays[idx]
    return delay, color

def generate_k(curve, primes=[2, 3, 5, 7, 11, 13]):
    k_code = []
    for i in range(0, len(curve), len(primes)):
        segment = curve[i:i+len(primes)]
        for j, p in enumerate(primes):
            point = segment[j % len(segment)]
            delay, color = tonage_map(point)
            gap = p / 10.0  # scaled gap
            k_code.append(f"K {p} {delay:.1f} {color} {gap:.1f}")
    return "\n".join(k_code)

# Run it
spiral = fibonacci_spiral()
k_script = generate_k(spiral)
print(k_script)  # Save to .k
