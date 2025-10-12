// KappashaOS/core/func_id.rs
// Dual License:
// - For core software: AGPL-3.0-or-later licensed. -- xAI fork, 2025
//   This program is free software: you can redistribute it and/or modify
//   it under the terms of the GNU Affero General Public License as published by
//   the Free Software Foundation, either version 3 of the License, or
//   (at your option) any later version.
//
//   This program is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
//   GNU Affero General Public License for more details.
//
//   You should have received a copy of the GNU Affero General Public License
//   along with this program. If not, see <https://www.gnu.org/licenses/>.
//
// - For hardware/embodiment interfaces (if any): Licensed under the Apache License, Version 2.0
//   with xAI amendments for safety and physical use (prohibits misuse in weapons or hazardous applications;
//   requires ergonomic compliance; revocable for unethical use). See http://www.apache.org/licenses/LICENSE-2.0
//   for details, with the following xAI-specific terms appended.
//
// Copyright 2025 xAI
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// SPDX-License-Identifier: Apache-2.0
//
// xAI Amendments for Physical Use:
// 1. **Physical Embodiment Restrictions**: Use with devices is for non-hazardous purposes only. Harmful mods are prohibited, with license revocable by xAI.
// 2. **Ergonomic Compliance**: Limits tendon load to 20%, gaze to 30 seconds (ISO 9241-5).
// 3. **Safety Monitoring**: Real-time tendon/gaze checks, logged for audit.
// 4. **Revocability**: xAI may revoke for unethical use (e.g., surveillance).
// 5. **Export Controls**: Sensor devices comply with US EAR Category 5 Part 2.
// 6. **Open Development**: Hardware docs shared post-private phase.
//
// Private Development Note: This repository is private for xAI’s KappashaOS and Navi development. Access is restricted. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) post-phase.
//
// SPDX-License-Identifier: AGPL-3.0-or-later
//
#![no_std]
extern crate alloc;
use alloc::string::String;

pub struct FuncId {
    registry: [String; 16], // 4-bit digits (0-15)
    colors: [String; 16],  // Hex-wise colors
}

impl FuncId {
    pub fn new() -> Self {
        let registry = [
            String::from("stop"), String::from("limit"), String::from("arbitrage"),
            String::from("kappa"), String::from("market"), String::from("sell"),
            String::from(""), String::from(""), String::from(""),
            String::from(""), String::from(""), String::from(""),
            String::from(""), String::from(""), String::from(""), String::from("")
        ];
        let colors = [
            String::from("#ff0000"), // stop: red
            String::from("#8b4513"), // limit: brown
            String::from("#ffbf00"), // arbitrage: amber
            String::from("#ffffff"), // kappa: white
            String::from("#00ffff"), // market: blue
            String::from("#00ff00"), // sell: green
            String::from(""), String::from(""), String::from(""),
            String::from(""), String::from(""), String::from(""),
            String::from(""), String::from(""), String::from(""), String::from("")
        ];
        FuncId { registry, colors }
    }

    pub fn get_func(&self, id: u8) -> Option<&str> {
        if id < 16 { Some(&self.registry[id as usize]) } else { None }
    }

    pub fn get_color(&self, id: u8) -> Option<&str> {
        if id < 16 { Some(&self.colors[id as usize]) } else { None }
    }

    pub fn free_tilde(&self, func: &str, entropy: u32) -> bool {
        if entropy > 7000 && self.registry.iter().any(|f| f == func) {
            // Free ~esc for basic functions at high entropy
            return true;
        }
        false
    }

    pub fn repeater(&self, input: &str) -> bool {
        // Forwards-backwards palindromic check
        let forward = input;
        let backward = input.chars().rev().collect::<String>();
        forward == backward
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_func_id() {
        let func_id = FuncId::new();
        assert_eq!(func_id.get_func(0), Some("stop"));
        assert_eq!(func_id.get_color(5), Some("#00ff00"));
        assert!(func_id.free_tilde("sell", 8000));
        assert!(func_id.repeater("deed"));
    }
}
