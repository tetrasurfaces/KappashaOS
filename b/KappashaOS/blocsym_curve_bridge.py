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

# blocsym_curve_bridge.py
import subprocess
import json
import os
import numpy as np

def run_curve_grid(command_args: list[str], input_data: str | None = None) -> dict:
    """
    Spawn curve.exe safely, feed stdin, capture/parse output.
    Mock fallback if exe missing.
    """
    exe_path = os.path.abspath("./curve.exe")  # full path, safer
    cmd = [exe_path] + command_args
    
    if not os.path.exists(exe_path):
        print("curve.exe not found — mock field")
        mock_voxel = np.random.randint(0, 256, (32,32,32), dtype=np.uint8)
        mock_density = np.mean(mock_voxel > 180)
        mock_poem = "To whoever finds this—\nThis line was folded into a curve.\nA place where text isn't stored,\nit's remembered."
        mock_regrets = [{"pos": (16,16,16), "delay": 0.618, "regret": "violet"}]
        return {
            "success": False,
            "error": "curve.exe missing",
            "voxel": mock_voxel,
            "density": mock_density,
            "poem": mock_poem,
            "regrets": mock_regrets
        }
    
    try:
        result = subprocess.run(
            cmd,
            input=input_data.encode('utf-8') if input_data else None,
            capture_output=True,
            text=True,
            timeout=30,
            check=False
        )
        output = result.stdout.strip()
        error = result.stderr.strip()
        
        # Parse known prints (expand as needed)
        grid_state = {}
        if "Raster flatten tweak:" in output:
            try:
                flat = float(output.split("Raster flatten tweak:")[-1].strip().split()[0])
                grid_state["flatten_tweak"] = flat
            except:
                pass
        
        # Return parsed or raw
        return {
            "success": result.returncode == 0,
            "stdout": output,
            "stderr": error,
            "returncode": result.returncode,
            "grid_state": grid_state
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "timeout"}
    except Exception as e:
        return {"success": False, "error": str(e)}