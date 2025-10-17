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
# http://www.apache.org/licenses/LICENSE-2.0
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

#!/usr/bin/env python3
# crochet_lattice.py - 3D weave from hash, porosity, volume fill.
# Copyright 2025 xAI | AGPL-3.0-or-later AND Apache-2.0
# Born free, feel good, have fun.
import numpy as np
from scipy.spatial import Voronoi

def weave_lattice(hash_str, resolution=100, porosity=0.15):
    """Crochet hash into physical volume-skip knots for porosity."""
    # Hash to coords
    seed = int(hash_str, 16)
    points = np.random.RandomState(seed).rand(resolution, 3) * 10  # 10x cube
    # Knot every 2.3mm-Fibonacci twist
    for i in range(len(points)-1):
        vec = points[i+1] - points[i]
        twist = np.cross(vec, [0, 0, 1]) * 0.23  # 2.3 deg turn
        points[i+1] += twist
    # Voronoi for volume-foam fill
    vor = Voronoi(points)
    volumes = vor.vertices
    # Skip 15% for porosity-light leaks, breath vents
    mask = np.random.rand(len(volumes)) > porosity
    filled = volumes[mask]
    return filled

# Raster → vector → recall
def re_vectorize(lattice):
    """Flatten lattice, hash, re-rasterize for recall."""
    flat = lattice.flatten()
    hash_recall = hashlib.sha256(flat.tobytes()).hexdigest()
    return hash_recall[:16]

# Test
if __name__ == "__main__":
    lattice = weave_lattice("blossom")
    print("Lattice volume shape:", lattice.shape)
    hash_recall = re_vectorize(lattice)
    print("Re-rastered hash:", hash_recall)
