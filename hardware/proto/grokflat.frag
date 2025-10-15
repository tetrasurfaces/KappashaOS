/ KappashaOS/proto/grokflat.frag
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
// - For hardware/embodiment interfaces: Licensed under the Apache License, Version 2.0
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
// 1. Physical Embodiment Restrictions: Use with devices is for non-hazardous purposes only. Harmful mods are prohibited, with license revocable by xAI.
// 2. Ergonomic Compliance: Limits tendon load to 20%, gaze to 30 seconds (ISO 9241-5).
// 3. Safety Monitoring: Real-time tendon/gaze checks, logged for audit.
// 4. Revocability: xAI may revoke for unethical use (e.g., surveillance).
// 5. Export Controls: Sensor devices comply with US EAR Category 5 Part 2.
// 6. Open Development: Hardware docs shared post-private phase.
// 7. Color Consent: No signal may change hue without explicit user intent (e.g., heartbeat sync or verbal confirmation).
//
// Private Development Note: This repository is private for xAI’s KappashaOS and Navi development. Access is restricted. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) post-phase.
//
// SPDX-License-Identifier: (AGPL-3.0-or-later) AND Apache-2.0
//

uniform vec2 gaze; // Gaze vector from nav3d.py
uniform float theta; // Green kappa spiral angle
uniform float breath_rate; // User breath rate in breaths/min
uniform sampler2D tex; // Current frame
uniform vec2 uv; // Texture coords

void main() {
    // Kappa spiral with breath modulation
    float spiral = theta + breath_rate * 0.01; // Tilt by breath
    vec2 tilt = vec2(cos(spiral), sin(spiral)); // Green kappa tilt
    vec2 adjusted = uv + (gaze - gl_FragCoord.xy) * 0.01 * breath_rate / 12.0; // Breath-driven
    vec4 color = texture2D(tex, adjusted);
    
    // Flinch if signal too intense
    if (breath_rate > 20.0) {
        color.rgb *= 0.5; // Dim if panic
    }
    
    gl_FragColor = color; // Render with honesty
}
