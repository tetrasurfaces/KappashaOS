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

import numpy as np

# Mock / paste minimal custom_interoperations_green_curve (replace with real import later)
def custom_interoperations_green_curve(points, kappas, is_closed=False):
    # Simplified placeholder — returns linear interp for testing
    points = np.array(points)
    n = len(points)
    t = np.linspace(0, 1, 1000)
    smooth_x = np.interp(t, np.linspace(0,1,n), points[:,0])
    smooth_y = np.interp(t, np.linspace(0,1,n), points[:,1])
    if is_closed:
        smooth_x = np.append(smooth_x, smooth_x[0])
        smooth_y = np.append(smooth_y, smooth_y[0])
    return smooth_x, smooth_y

MERSENNES = np.array([2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281,
    3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243,
    110503, 132049, 216091, 756839, 859433, 1257787, 1398269, 2976221, 3021377,
    6972593, 13466917, 20996011, 24036583, 25964951, 30402457, 32582657,
    37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933,
    136279841, 194087760, 393668989, 1137184133, 4678395213, 27411294813,
    228732945894, 2718281472161, 46007290309705, 1108984342777087,
    38070686010400544, 1861326323879814400, 129604733991207583744])

KAPPA_ODD = 0.3536
KAPPA_EVEN = 0.3563
FLUCT = 0.0027

def mersenne_helix_spline(n_nodes=64, radius=16.0):
    exponents = MERSENNES[:n_nodes].astype(float) + 1  # avoid log(0)
    angles = np.cumsum(np.log(exponents))              # now safe
    angles = angles / angles[-1] * 2 * np.pi * 5       # 5 full turns
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)
    z = np.linspace(-n_nodes/2, n_nodes/2, n_nodes) * 0.5
    return np.column_stack([x, y, z])

def envelope_green_curve(spline_points, lane_kappas):
    kappas = np.array(lane_kappas)
    points = spline_points[:, :2]  # xy for 2D spline
    smooth_x, smooth_y = custom_interoperations_green_curve(
        points.tolist(),
        kappas.tolist(),
        is_closed=False
    )
    smooth_z = np.linspace(spline_points[0,2], spline_points[-1,2], len(smooth_x))
    return np.column_stack([smooth_x, smooth_y, smooth_z])

def frog_entry_to_spline(data: bytes, spline_points, salt=42):
    """helix_frog_field → nearest point on spline."""
    idx, _ = helix_frog_field(data, salt=salt, breath_rate=12.0)
    # Map 4096 buckets → 64 spline nodes (coarse)
    node_idx = idx % len(spline_points)
    return spline_points[node_idx]

# Run example
spline = mersenne_helix_spline()
kappas = [KAPPA_ODD if i%2 else KAPPA_EVEN + np.random.uniform(-FLUCT, FLUCT)
          for i in range(len(spline))]
envelope = envelope_green_curve(spline, kappas)
print("Spine nodes:", len(spline))
print("Envelope points:", len(envelope))
print("Envelope sample (first 3):")
print(envelope[:3])
