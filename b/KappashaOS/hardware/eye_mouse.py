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
# eye_mouse.py - Mock eye mouse for KappashaOS: gaze cursor, blink click, drag ectoplasm.
# Navi-integrated.

import numpy as np
import time
import asyncio
from master_hand import MasterHand  # Local mock
from lens_stack import LensStack  # Local mock

class EyeMouse:
    def __init__(self):
        self.prev_x, self.prev_y = 0, 0
        self.blink_start = 0
        self.blink_threshold = 0.3
        self.hand = MasterHand()
        self.lens = LensStack()
        self.dragging = False
        self.drag_pos = None
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        print("EyeMouse initialized - gaze cursor ready.")

    async def navi_detect(self):
        """Navi detects blink with safety checks."""
        while True:
            is_blink = np.random.rand() > 0.8  # Mock blink
            if is_blink:
                if time.time() - self.blink_start > self.blink_threshold * 2:
                    if not self.dragging:
                        self.dragging = True
                        self.drag_pos = (self.prev_x, self.prev_y)
                        print("Long blink - start drag ectoplasm.")
                    else:
                        self.dragging = False
                        drag_end = (self.prev_x, self.prev_y)
                        self.lens.integrate_blocsym("sim bloom")  # Integrate lens on drag
                        print("Long blink release - end drag.")
                else:
                    print("Short blink - click.")
                    self.lens.integrate_blocsym("sim bloom")  # Integrate lens on click
            self.tendon_load = np.random.rand() * 0.3
            self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
            if self.tendon_load > 0.2:
                print("EyeMouse: Warning - Tendon overload. Resetting.")
                self.reset()
            if self.gaze_duration > 30.0:
                print("EyeMouse: Warning - Excessive gaze. Pausing.")
                await asyncio.sleep(2.0)
                self.gaze_duration = 0.0
            await asyncio.sleep(0.01)

    def reset(self):
        """Reset eye mouse state and safety counters."""
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        self.dragging = False
        self.drag_pos = None

if __name__ == "__main__":
    mouse = EyeMouse()
    asyncio.run(mouse.navi_detect())
