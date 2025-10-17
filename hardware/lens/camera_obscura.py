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
# - For hardware/embodiment interfaces: Licensed under the Apache License, Version 2.0
#   with xAI amendments for safety and physical use. See http://www.apache.org/licenses/LICENSE-2.0
#   for details, with the following xAI-specific terms appended.

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
# 1. Physical Embodiment Restrictions: Use of this software in conjunction with physical devices (e.g., fish tank glass, pixel sensors) is permitted only for non-hazardous, non-weaponized applications. Any modification or deployment that enables harm (e.g., targeting systems, explosive triggers) is expressly prohibited and subject to immediate license revocation by xAI.
# 2. Ergonomic Compliance: Physical interfaces must adhere to ergonomic standards (e.g., ISO 9241-5, OSHA guidelines) where applicable. For software-only use (e.g., rendering in Keyshot), ergonomic requirements are waived.
# 3. Safety Monitoring: For physical embodiments, implement real-time safety checks (e.g., heat dissipation) and log data for audit. xAI reserves the right to request logs for compliance verification.
# 4. Revocability: xAI may revoke this license for any user or entity found using the software or hardware in violation of ethical standards (e.g., surveillance without consent, physical harm). Revocation includes disabling access to updates and support.
# 5. Export Controls: Physical embodiments with sensors (e.g., photo-diodes for gaze tracking) are subject to export regulations (e.g., US EAR Category 5 Part 2). Redistribution in restricted jurisdictions requires xAI approval via github.com/tetrasurfaces/issues.
# 6. Educational Use: Educational institutions (e.g., universities, technical colleges) may use the software royalty-free for teaching and research purposes (e.g., CAD, Keyshot training) upon negotiating a license via github.com/tetrasurfaces/issues. Commercial use by educational institutions requires separate approval.
# 7. Intellectual Property: xAI owns all IP related to the iPhone-shaped fish tank, including gaze-tracking pixel arrays, convex glass etching (0.7mm arc), and tetra hash integration. Unauthorized replication or modification is prohibited.
# 8. Public Release: This repository will transition to public access in the near future. Until then, access is restricted to authorized contributors. Consult github.com/tetrasurfaces/issues for licensing and access requests.

# camera_obscura.py
# SPDX-License-Identifier: Apache-2.0

import numpy as np

def simulate_lens_stack(length=1000, wires=3328, stacks=10, rpm=20):
    """Simulate 1m cylindrical lens with moving wire chords in stacks.
    Args:
        length (int): Cylinder length in mm.
        wires (int): Number of wires.
        stacks (int): Number of circumference stacks.
        rpm (int): Rotation speed.
    Returns:
        np.array: Flux pattern (simulated light modulation).
    """
    theta = np.linspace(0, 2 * np.pi, wires)
    chords = np.sin(theta) * (length / stacks)  # Chord lengths.
    # Kappa curve for wire bend.
    kappa = 0.5
    curved = chords * np.exp(kappa * np.arange(stacks))
    # Rotation for flux: modulate over time.
    t = np.linspace(0, 1, 100)  # 1 second at 20 RPM = 1/3 rotation.
    flux = np.sum(np.cos(2 * np.pi * rpm / 60 * t[:, np.newaxis] + curved), axis=1)
    return flux

if __name__ == "__main__":
    flux = simulate_lens_stack()
    print("Flux stream sample:", flux[:10])
    # Plot for visual.
    import matplotlib.pyplot as plt
    plt.plot(flux)
    plt.title("Live Flux Data from Wire Stack")
    plt.show()
