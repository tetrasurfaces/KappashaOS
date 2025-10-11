# Dual License:
# - For core software: AGPL-3.0-or-later licensed. -- xAI fork, 2025
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without the implied warranty of
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
# main_integration.py - Mock end-to-end PUF/kappa flow for KappashaOS.
# Orchestrates Pi entropy, grid gen, drift, litho, export, hardware preview.

from puff_grid import generate_kappa_grid, simulate_drift  # Local mock
from core_array_sim import simulate_core_array  # Local mock
from stereo_puf_export import export_to_stl  # Local mock
from kappa_litho_model import model_litho_etch  # Local mock
from pi_sensor_entropy import extract_pi_entropy  # Local mock
from pi_litho_control import hardware_preview  # Local mock
import asyncio

def run_full_flow(grid_size=20, tremor_duration=5, scale_nm=0.8):
    entropy, salt = extract_pi_entropy()
    print(f"Entropy Salt: {salt}")
    
    grid = generate_kappa_grid(size=grid_size)
    array = simulate_core_array(size=grid_size)
    
    drifted, puf_key = simulate_drift(array, piezo_noise_level=float(salt[:1][0]))
    etched, yield_est = model_litho_etch(drifted, scale_nm=scale_nm)
    print(f"Litho Yield: {yield_est:.2f}")
    
    export_file = 'integrated_puf.stl.txt'
    export_to_stl(etched, export_file)
    
    hardware_preview(etched, led_pin=18, servo_pin=17, pressure=0.01)
    
    return puf_key, export_file

async def navi_flow():
    puf_key, export_file = run_full_flow()
    print(f"Navi: Final PUF Key: {puf_key}")
    print(f"Exported to: {export_file}")

if __name__ == '__main__':
    asyncio.run(navi_flow())
