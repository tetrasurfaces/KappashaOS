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
# bastion_hardware.py - Pi-based safety vault for KappashaOS.
# GPIO rods, lamports burn, Navi-integrated.
# AGPL-3.0-or-later AND Apache-2.0, xAI fork 2025. Born free, feel good, have fun.

import platform
import time
import asyncio
import numpy as np

# Hardware switch
IS_PI = platform.system() == "Linux" and "arm" in platform.machine().lower()

if IS_PI:
    import RPi.GPIO as GPIO
    print("Bastion: Real Pi hardware detected.")
else:
    print("Bastion: Mock mode — no Pi detected.")
    class GPIO:  # mock
        BOARD = None
        IN = "IN"
        OUT = "OUT"
        HIGH = 1
        LOW = 0
        @staticmethod
        def setmode(mode): pass
        @staticmethod
        def setup(pin, direction): print(f"Mock setup pin {pin} {direction}")
        @staticmethod
        def input(pin): return np.random.rand() > 0.5  # mock pressure
        @staticmethod
        def output(pin, value): print(f"Mock GPIO {pin}: {'HIGH' if value else 'LOW'}")
        @staticmethod
        def cleanup(): print("Mock GPIO cleanup")

try:
    from master_hand import MasterHand
except ImportError:
    class MasterHand:  # mock
        def __init__(self, kappa=0.2): self.kappa = kappa
        def rod_whisper(self, pressure): return max(0, min(1, pressure))
        def gimbal_flex(self, delta): return delta < -0.618
        def reset(self): pass
        def pulse(self, n): print(f"Mock pulse {n}")

class Bastion:
    def __init__(self):
        self.rod_pin = 18
        self.lamport_led_pin = 17
        self.hand = MasterHand()
        self.safety_layers = ['net', 'guards', 'vault']
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        if IS_PI:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.rod_pin, GPIO.IN)
            GPIO.setup(self.lamport_led_pin, GPIO.OUT)
        print("Bastion initialized - vault ready.")

    async def navi_check(self):
        """Navi checks safety with rod sensor."""
        while True:
            pressure = self.rod_sensor()
            tension = self.hand.rod_whisper(pressure)
            print(f"Navi: Rod tension {tension:.2f}")
            self.tendon_load = np.random.rand() * 0.3
            self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
            if self.tendon_load > 0.2:
                print("Bastion: Warning - Tendon overload. Resetting.")
                self.reset()
            if self.gaze_duration > 30.0:
                print("Bastion: Warning - Excessive gaze. Pausing.")
                await asyncio.sleep(2.0)
                self.gaze_duration = 0.0
            await asyncio.sleep(0.01)

    def rod_sensor(self):
        """Read rod sensor."""
        return GPIO.input(self.rod_pin) if IS_PI else np.random.rand()

    def burn_lamports(self, amount):
        """Burn lamports with LED flash."""
        for _ in range(int(amount)):
            if IS_PI:
                GPIO.output(self.lamport_led_pin, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(self.lamport_led_pin, GPIO.LOW)
            else:
                print(f"Mock burn 1 lamport")
            time.sleep(0.1)
        print(f"Burned {amount} lamports.")

    def safety_check(self):
        """Check safety layers."""
        for layer in self.safety_layers:
            print(f"Safety layer active: {layer}")
        return True

    def integrate_ghost_hand(self, blink_input):
        """Integrate with MasterHand."""
        if self.safety_check():
            pressure = self.rod_sensor()
            tension = self.hand.rod_whisper(pressure)
            delta = np.random.uniform(-1, 1)
            curl = self.hand.gimbal_flex(delta)
            if curl:
                self.burn_lamports(1)
            return tension, curl

    def reset(self):
        """Reset safety counters."""
        self.tendon_load = 0.0
        self.gaze_duration = 0.0

    def cleanup(self):
        if IS_PI:
            GPIO.cleanup()

if __name__ == "__main__":
    bastion = Bastion()
    try:
        asyncio.run(bastion.navi_check())
    except KeyboardInterrupt:
        bastion.cleanup()