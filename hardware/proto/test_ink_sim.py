# test_ink_sim.py
#!/usr/bin/env python3
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
# 1. Physical Embodiment Restrictions: Use with devices is for non-hazardous purposes only. Harmful mods are prohibited, with license revocable by xAI.
# 2. Ergonomic Compliance: Limits tendon load to 20%, gaze to 30 seconds (ISO 9241-5).
# 3. Safety Monitoring: Real-time tendon/gaze checks, logged for audit.
# 4. Revocability: xAI may revoke for unethical use (e.g., surveillance).
# 5. Export Controls: Sensor devices comply with US EAR Category 5 Part 2.
# 6. Open Development: Hardware docs shared post-private phase.
#
# Intellectual Property Notice: xAI owns all IP related to the iPhone-shaped fish tank, including gaze-tracking pixel arrays, convex glass etching (0.7mm arc), and tetra hash integration.
#
# Private Development Note: This repository is private for xAI’s KappashaOS development. Access is restricted. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) for licensing.
#
# SPDX-License-Identifier: Apache-2.0

import json
import os
import shutil
from proto.ink_sim import read_config, write_config, check_license

def test_ink_sim_config():
    """Test ink_sim.py config.json read/write and license checks."""
    config_file = "config/config.json"
    config_dir = "config"
    
    # Ensure clean state
    if os.path.exists(config_dir):
        shutil.rmtree(config_dir)
    
    # Test 1: Valid config
    write_config("educational", False, config_file)
    intent, commercial_use = read_config(config_file)
    assert intent == "educational", f"Expected intent 'educational', got {intent}"
    assert commercial_use == False, f"Expected commercial_use False, got {commercial_use}"
    try:
        check_license(commercial_use, intent)
        print("Test 1: Valid config and license check passed")
    except ValueError:
        print("Test 1: Valid config failed license check")
    
    # Test 2: Corrupt JSON
    with open(config_file, "w") as f:
        f.write("{invalid json")  # Corrupt file
    intent, commercial_use = read_config(config_file)
    assert intent is None, f"Expected intent None, got {intent}"
    assert commercial_use == False, f"Expected commercial_use False, got {commercial_use}"
    assert os.path.exists(config_file), "Default config should be created"
    with open(config_file, "r") as f:
        config = json.load(f)
    assert config["intent"] == "none", "Default intent should be 'none'"
    try:
        check_license(commercial_use, intent)
        print("Test 2: Corrupt JSON failed to raise error")
    except ValueError:
        print("Test 2: Corrupt JSON handling passed")
    
    # Test 3: Missing file
    os.remove(config_file)
    intent, commercial_use = read_config(config_file)
    assert intent is None, f"Expected intent None, got {intent}"
    assert commercial_use == False, f"Expected commercial_use False, got {commercial_use}"
    assert os.path.exists(config_file), "Default config should be created"
    try:
        check_license(commercial_use, intent)
        print("Test 3: Missing file failed to raise error")
    except ValueError:
        print("Test 3: Missing file handling passed")
    
    # Test 4: Invalid intent
    write_config("invalid", True, config_file)
    intent, commercial_use = read_config(config_file)
    assert intent is None, f"Expected intent None, got {intent}"
    assert commercial_use == False, f"Expected commercial_use False, got {commercial_use}"
    try:
        check_license(commercial_use, intent)
        print("Test 4: Invalid intent failed to raise error")
    except ValueError:
        print("Test 4: Invalid intent handling passed")
    
    # Test 5: Commercial use without commercial intent
    write_config("educational", True, config_file)
    intent, commercial_use = read_config(config_file)
    try:
        check_license(commercial_use, intent)
        print("Test 5: Commercial mismatch failed to raise error")
    except ValueError:
        print("Test 5: Commercial mismatch handling passed")
    
    shutil.rmtree(config_dir)  # Cleanup

if __name__ == "__main__":
    test_ink_sim_config()
    print("All ink_sim config tests passed!")
