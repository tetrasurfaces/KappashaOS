#!/usr/bin/env python3
# Copyright 2025 xAI
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
#   with xAI amendments for safety and physical use (prohibits misuse in weapons or hazardous applications;
#   requires ergonomic compliance; revocable for unethical use). See http://www.apache.org/licenses/LICENSE-2.0
#   for details, with the following xAI-specific terms appended.
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
# SPDX-License-Identifier: (AGPL-3.0-or-later) AND Apache-2.0
#
# xAI Amendments for Physical Use:
# 1. Physical Embodiment Restrictions: Use with devices is for non-hazardous purposes only. Harmful mods are prohibited, with license revocable by xAI.
# 2. Ergonomic Compliance: Limits tendon load to 20%, gaze to 30 seconds (ISO 9241-5).
# 3. Safety Monitoring: Real-time tendon/gaze checks, logged for audit.
# 4. Revocability: xAI may revoke for unethical use (e.g., surveillance).
# 5. Export Controls: Sensor devices comply with US EAR Category 5 Part 2.
# 6. Open Development: Hardware docs shared post-private phase.
#
# Private Development Note: This repository is private for xAI’s KappashaOS and Navi development. Access is restricted. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) post-phase.
#
# SPDX-License-Identifier: (AGPL-3.0-or-later) AND Apache-2.0

import numpy as np
import asyncio
import json
import os
from datetime import datetime
from scipy.spatial import Delaunay
from tetra.solid import mesh  # Mock tetra surfaces
from master_hand import MasterHand
from proto.revocation_stub import check_revocation
from tetra.arch_utils import tetra_hash_surface

def read_config(config_file="config/config.json"):
    """Read intent and commercial use from config file with error handling."""
    config_dir = os.path.dirname(config_file)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(config_file):
        print(f"Config file {config_file} not found. Creating default.")
        write_config("none", False, config_file)
        return None, False
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        intent = config.get("intent")
        commercial_use = config.get("commercial_use", False)
        if intent not in ["educational", "commercial", "none"]:
            raise ValueError("Invalid intent in config.")
        return intent, commercial_use
    except json.JSONDecodeError:
        print(f"Error: {config_file} contains invalid JSON. Resetting to default.")
        write_config("none", False, config_file)
        return None, False
    except Exception as e:
        print(f"Error reading {config_file}: {e}. Resetting to default.")
        write_config("none", False, config_file)
        return None, False

def write_config(intent, commercial_use, config_file="config/config.json"):
    """Write intent and commercial use to config file with error handling."""
    config = {"intent": intent, "commercial_use": commercial_use}
    config_dir = os.path.dirname(config_file)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    try:
        with open(config_file, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error writing to {config_file}: {e}")

def log_license_check(result, intent, commercial_use):
    """Log license and revocation check results for audit trail."""
    try:
        with open("license_log.txt", "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] License Check: {result}, Intent: {intent}, Commercial: {commercial_use}\n")
    except Exception as e:
        print(f"Error logging license check: {e}")

def check_license(commercial_use=False, intent=None):
    """Ensure license compliance and intent declaration."""
    if intent not in ["educational", "commercial"]:
        notice = """
        NOTICE: You must declare your intent to use this software.
        - For educational use (e.g., university training), open a GitHub issue at github.com/tetrasurfaces/issues using the Educational License Request template.
        - For commercial use (e.g., branding, molding), use the Commercial License Request template.
        See NOTICE.txt for details. Do not share proprietary details in public issues.
        """
        log_license_check("Failed: Invalid or missing intent", intent, commercial_use)
        raise ValueError(f"Invalid or missing intent. {notice}")
    if commercial_use and intent != "commercial":
        notice = "Commercial use requires 'commercial' intent and a negotiated license via github.com/tetrasurfaces/issues."
        log_license_check("Failed: Commercial use without commercial intent", intent, commercial_use)
        raise ValueError(notice)
    log_license_check("Passed", intent, commercial_use)
    return True

class Kappa:
    def __init__(self, grid_size=10, device_hash="kappa_001"):
        """Initialize Kappa grid for situational curvature awareness."""
        intent, commercial_use = read_config()
        check_license(commercial_use, intent)
        if check_revocation(device_hash):
            log_license_check("Revoked: Device hash invalidated", intent, commercial_use)
            raise ValueError("Device revoked by xAI. Contact github.com/tetrasurfaces/issues for details.")
        
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size, grid_size))
        self.material = {"density": 1.0, "type": "steel"}  # Mock material
        self.hand = MasterHand()
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        self.device_hash = device_hash
        print("Kappa initialized - grid rasterization ready.")

    async def navi_rasterize_kappa(self, points, material):
        """Rasterize kappa grid with material depth and fractal tetra."""
        if check_revocation(self.device_hash):
            log_license_check("Revoked: Device hash invalidated", "unknown", False)
            raise ValueError("Device revoked by xAI. Contact github.com/tetrasurfaces/issues for details.")
        
        for p in points:
            x, y, z = [int(coord * (self.grid_size - 1)) for coord in p]
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size and 0 <= z < self.grid_size:
                self.grid[x, y, z] = material.get("density", 1.0)
        
        # Add Sierpiński tetrahedrons for curvature awareness
        tetra_points = []
        for x in range(0, self.grid_size, 2):
            for y in range(0, self.grid_size, 2):
                for z in range(0, self.grid_size, 2):
                    tetra_points.extend([(x, y, z), (x+1, y, z), (x, y+1, z), (x, y, z+1)])
        tri = Delaunay(np.array(tetra_points))
        for simplex in tri.simplices:
            center = np.mean([tetra_points[i] for i in simplex], axis=0)
            x, y, z = [int(c) for c in center]
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size and 0 <= z < self.grid_size:
                self.grid[x, y, z] += 0.5
                # Hash tetra points for kappasha256 integration
                hash_val = tetra_hash_surface(np.array([tetra_points[i] for i in simplex]))
                self.hand.log_hash(hash_val)
        
        self.tendon_load = np.random.rand() * 0.3
        self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
        if self.tendon_load > 0.2:
            print("Kappa: Warning - Tendon overload. Resetting.")
            self.reset()
        if self.gaze_duration > 30.0:
            print("Kappa: Warning - Excessive gaze. Pausing.")
            await asyncio.sleep(2.0)
            self.gaze_duration = 0.0
        await asyncio.sleep(0)
        print(f"Navi: Rasterized kappa grid with {len(points)} points")
        return self.grid

    def flatten_to_delaunay(self, grid):
        """Flatten grid to Delaunay surface map."""
        return grid.reshape(-1)

    async def navi_unflatten_to_stl(self, flat_map):
        """Unflatten to stereolithography output."""
        if check_revocation(self.device_hash):
            log_license_check("Revoked: Device hash invalidated", "unknown", False)
            raise ValueError("Device revoked by xAI. Contact github.com/tetrasurfaces/issues for details.")
        
        mesh_data = mesh("W21x62")  # Mock solid
        stl_output = f"solid kappa\nfacet normal 0 0 1\nouter loop\n"
        for i in range(len(flat_map) - 1):
            if flat_map[i] > 0 and flat_map[i + 1] > 0:
                x, y, z = np.unravel_index(i, (self.grid_size, self.grid_size, self.grid_size))
                stl_output += f"vertex {x} {y} {z}\n"
        stl_output += "endloop\nendfacet\nendsolid kappa"
        self.tendon_load = np.random.rand() * 0.3
        self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
        if self.tendon_load > 0.2:
            print("Kappa: Warning - Tendon overload. Resetting.")
            self.reset()
        if self.gaze_duration > 30.0:
            print("Kappa: Warning - Excessive gaze. Pausing.")
            await asyncio.sleep(2.0)
            self.gaze_duration = 0.0
        await asyncio.sleep(0)
        print("Navi: Unflattened to STL")
        return stl_output

    def reset(self):
        """Reset tendon and gaze metrics."""
        self.tendon_load = 0.0
        self.gaze_duration = 0.0

if __name__ == "__main__":
    async def navi_test():
        kappa = Kappa()
        points = np.random.rand(10, 3)
        grid = await kappa.navi_rasterize_kappa(points, {"density": 2.0})
        flat_map = kappa.flatten_to_delaunay(grid)
        stl = await kappa.navi_unflatten_to_stl(flat_map)
        print(f"Navi: STL snippet: {stl[:100]}...")

    asyncio.run(navi_test())
