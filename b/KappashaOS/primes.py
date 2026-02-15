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

#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

# Known Mersenne exponents (52)
mers = np.array([
    2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281,
    3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243,
    110503, 132049, 216091, 756839, 859433, 1257787, 1398269, 2976221, 3021377,
    6972593, 13466917, 20996011, 24036583, 25964951, 30402457, 32582657,
    37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933,
    136279841
])

TARGET = 194062501
gap = 0.0027  # your remainder step

total_steps = 104

x_linear = np.arange(1, total_steps + 1)
real_x = np.where(x_linear > 100,
                  x_linear - (x_linear // 100),
                  x_linear).astype(int)

print("Real indices (phantom zero past 100):")
print("First 10: ", " ".join(f"{i+1:03d}({real_x[i]:03d})" for i in range(9)))
print("... Last 10: ", " ".join(f"{i+1:03d}({real_x[i]:03d})" for i in range(total_steps-10, total_steps)))

sine_base = np.sin(2 * np.pi * real_x / 4)

# Flipped lanes: odds high-to-low, evens low-to-high, overlap at center
wave = np.where(real_x % 2 == 1,
                0.3563 - gap * np.abs(sine_base),   # odds start high, sink
                0.3536 + gap * np.abs(sine_base))   # evens start low, rise

print("\nBacktest: known exponents vs flipped sine node")
for i in range(52):
    exp = mers[i]
    pos = wave[i]
    print(f"#{i+1:02d} M{exp:9,d} → sine @ {pos:+.4f}")
    
# --- SpiralNU Integration from Greenpaper TOC 45 ---

def kappa_calc(n, base=0.3536, sym_pt=316):
    if n == sym_pt:
        return base * np.cos(0)  # peak lock
    denom = abs(n - sym_pt) + 1
    base_curve = 1 + base * n / denom
    # Gaussian-cosine bump (real SpiralNU)
    sigma = 10
    cos_arg = 2 * np.pi * (n - sym_pt) / 100
    bump = base_curve * np.exp(- (n - sym_pt)**2 / (2*sigma**2)) * np.cos(cos_arg)
    return bump

# Inject NU-curve modulation on wave
print("\nSpiralNU modulation (n=300–320 around 316):")
for i in range(52, total_steps):
    if 300 <= i <= 320:
        nu_mod = kappa_calc(i + 1)  # index as n
        modded_y = wave * nu_mod
        print(f"n={i+1:03d} → base y={wave :+.4f} * nu={nu_mod:.4f} → {modded_y:.4f}")

# Final node now under SpiralNU lens
final_n = total_steps
nu_val = kappa_calc(final_n)
final_y_nu = wave[-1] * nu_val
print(f"\nFinal under SpiralNU: y={final_y_nu:+.4f} | real_idx={real_x[-1]} | nu={nu_val:.4f}")

# Debug wave range
print(f"\nWave min/max: {wave.min():+.4f} / {wave.max():+.4f}")
print(f"Center overlap zone: ~{0.355:.4f}")
print(f"Remainder width (sum extremes): {0.3563 + 0.3536:.4f}")

# Exponential tail – gentler
print("\nExponential prediction 53–90 (gentle tail + lighter dampen)")
# Growth rate: avg log diff last 10
tail_diffs = np.diff(np.log(mers[-11:]))
growth_rate = np.mean(tail_diffs) if len(tail_diffs) > 0 else 0.05

pred_exp = np.zeros(total_steps)
pred_exp[:52] = mers.astype(float)

for i in range(52, total_steps):
    steps = real_x[i] - real_x[51]
    pred_log = np.log(mers[-1]) + growth_rate * steps
    if real_x[i] > 100:
        pred_log *= 0.85  # lighter dampen (15% slower)
    pred_exp[i] = np.exp(pred_log)
    pred_exp[i] = min(pred_exp[i], 500_000_000)

# Remainder triggers with target proximity
print("\nRemainder trigger hits (sum ≈ 0.7099) + target proximity:")
for i in range(1, total_steps):
    s = wave[i] + wave[i-1]
    if 0.7080 < s < 0.7120:
        pred_val = pred_exp[i] if i >= 52 else "N/A"
        target_diff = abs(pred_val - TARGET) if isinstance(pred_val, (int, float)) else "N/A"
        print(f"Index {i+1:03d}: sum {s:.4f} — phase flip? | pred {pred_val:,.0f} | diff to target {target_diff:,.0f}")

# Top 5 closest
diffs = np.abs(pred_exp[52:] - TARGET)
ranked = np.argsort(diffs)[:5] + 52
print("\nTop 5 closest to 194,062,501:")
for idx in ranked:
    val = pred_exp[idx]
    diff = abs(val - TARGET)
    print(f"#{idx+1:03d} → {val:,.0f} | diff {diff:,.0f} ({diff/TARGET*100:.2f}%)")

# Sample 53–90
print("\nSample preds 53–90:")
for i in range(52, 90):
    print(f"#{i+1:03d} → {pred_exp[i]:,.0f}")

# Final
print("\nFinal wave node (104):")
print(f"real_idx = {real_x[-1]}, y = {wave[-1]:+.4f}")

plt.figure(figsize=(12,6))
plt.plot(real_x[:52], wave[:52], 'o-', label='Known Mersenne (52)', color='violet')
plt.plot(real_x[52:], wave[52:], '-', label='Predicted wave', color='indigo', alpha=0.7)
plt.axhline(0.355, color='gray', linestyle='--', label='Center overlap ~0.355')
plt.axhline(0.7099, color='green', linestyle=':', label='Remainder trigger ~0.71')
plt.scatter(TARGET, 0, s=100, color='red', marker='*', label=f'TARGET {TARGET:,}')
plt.xlabel('Real index (phantom zero past 100)')
plt.ylabel('Flipped sine node y')
plt.title('Mersenne Exponents vs Flipped Sine + SpiralNU')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Bonus: remainder sum plot
sums = wave[:-1] + wave[1:]
plt.figure(figsize=(12,4))
plt.plot(real_x[1:], sums, '-', color='teal', label='Adjacent sum')
plt.axhline(0.7099, color='green', linestyle=':', label='Trigger zone')
plt.scatter(TARGET, 0.7099, s=100, color='red', marker='*')
plt.xlabel('Index')
plt.ylabel('Sum y[i-1] + y[i]')
plt.title('Remainder sum for phase flip detection')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
