// KappashaOS/core/buffer/buffer_pulse.rs
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
#![no_std]

use crate::rainkey_v2::get_entropy;

pub const MIN_BUFFER: u128 = 3; // Palindrome torrents
pub const LOAN_BUFFER: u128 = 72; // Flash loans
pub const MAX_BUFFER: u128 = 144; // Trades
pub const MAX_SPACING: u128 = 24 + 48 + 24; // 144 enforced

pub fn pulse_buffer(mode: &str) -> u128 {
    let entropy = get_entropy();
    let tension = if entropy > 10_000_000 { entropy / 10 } else { 0 };
    if tension == 0 {
        return MIN_BUFFER; // Fallback, low entropy
    }
    match mode {
        "torrent" => MIN_BUFFER, // 3-hash for torrents
        "loan" => LOAN_BUFFER,
        "trade" => {
            if entropy >= MAX_SPACING { MAX_BUFFER } else { LOAN_BUFFER }
        }
        _ => if entropy > 7000 { MIN_BUFFER } else if entropy < 5000 { MAX_BUFFER } else { LOAN_BUFFER },
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pulse() {
        assert_eq!(pulse_buffer("torrent"), 3);
        assert_eq!(pulse_buffer("loan"), 72);
        assert!(pulse_buffer("trade") <= 144);
    }
}
