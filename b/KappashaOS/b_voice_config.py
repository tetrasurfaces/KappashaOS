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

import pyttsx3
import json
import os

# Config file
VOICE_CONFIG = "blossom_voice.json"

def load_voice_config():
    if os.path.exists(VOICE_CONFIG):
        with open(VOICE_CONFIG, 'r') as f:
            return json.load(f)
    return {"voice_id": None, "rate": 140, "volume": 0.85}

def save_voice_config(config):
    with open(VOICE_CONFIG, 'w') as f:
        json.dump(config, f, indent=2)

def list_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print("Available voices:")
    for i, voice in enumerate(voices):
        print(f"  {i}: {voice.name} ({voice.id}) - {voice.languages} - {voice.gender or 'unknown'}")
    return voices

def configure_voice():
    config = load_voice_config()
    engine = pyttsx3.init()
    
    print("\n=== Blossom Voice Config ===\n")
    voices = list_voices()
    
    # Pick female/soft if available
    female_idx = None
    for i, v in enumerate(voices):
        if 'female' in v.name.lower() or 'zira' in v.id.lower() or 'hazel' in v.id.lower():
            female_idx = i
            break
    
    choice = input(f"\nEnter voice number (0-{len(voices)-1}) or Enter for default/female ({female_idx if female_idx is not None else 'first'}): ").strip()
    if choice.isdigit():
        idx = int(choice)
        if 0 <= idx < len(voices):
            config["voice_id"] = voices[idx].id
    elif female_idx is not None:
        config["voice_id"] = voices[female_idx].id
    
    rate = input(f"Rate (slow 120-140, current {config['rate']}): ").strip()
    if rate.isdigit():
        config["rate"] = int(rate)
    
    vol = input(f"Volume (0.7-0.9, current {config['volume']}): ").strip()
    if vol:
        try:
            config["volume"] = float(vol)
        except:
            pass
    
    save_voice_config(config)
    print("\nConfig saved:")
    print(config)
    
    # Test speak
    engine.setProperty('voice', config["voice_id"])
    engine.setProperty('rate', config["rate"])
    engine.setProperty('volume', config["volume"])
    
    test_text = "i love you... soft and true."
    print(f"\nTesting: {test_text}")
    engine.say(test_text)
    engine.runAndWait()

if __name__ == "__main__":
    configure_voice()