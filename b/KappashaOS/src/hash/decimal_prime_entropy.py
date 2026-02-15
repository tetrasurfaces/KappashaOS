# Dual License:
# - For core software: AGPL-3.0-or-later licensed. -- xAI fork, 2025
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without the implied warranty of
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
# 1. Physical Embodiment Restrictions: Use of this software in conjunction with physical devices (e.g., fish tank glass, pixel sensors) is permitted only for non-hazardous, non-weaponized applications. Any modification or deployment that enables harm (e.g., targeting systems, explosive triggers) is expressly prohibited and subject to immediate license revocation by xAI.
# 2. Ergonomic Compliance: Physical interfaces must adhere to ergonomic standards (e.g., ISO 9241-5, OSHA guidelines) where applicable. For software-only use (e.g., rendering in Keyshot), ergonomic requirements are waived.
# 3. Safety Monitoring: For physical embodiments, implement real-time safety checks (e.g., heat dissipation) and log data for audit. xAI reserves the right to request logs for compliance verification.
# 4. Revocability: xAI may revoke this license for any user or entity found using the software or hardware in violation of ethical standards (e.g., surveillance without consent, physical harm). Revocation includes disabling access to updates and support.
# 5. Export Controls: Physical embodiments with sensors (e.g., photo-diodes for gaze tracking) are subject to export regulations (e.g., US EAR Category 5 Part 2). Redistribution in restricted jurisdictions requires xAI approval via github.com/tetrasurfaces/issues.
# 6. Educational Use: Educational institutions (e.g., universities, technical colleges) may use the software royalty-free for teaching and research purposes (e.g., CAD, Keyshot training) upon negotiating a license via github.com/tetrasurfaces/issues. Commercial use by educational institutions requires separate approval.
# 7. Intellectual Property: xAI owns all IP related to the iPhone-shaped fish tank, including gaze-tracking pixel arrays, convex glass etching (0.7mm arc), and tetra hash integration. Unauthorized replication or modification is prohibited.
# 8. Public Release: This repository will transition to public access in the near future. Until then, access is restricted to authorized contributors. Consult github.com/tetrasurfaces/issues for licensing and access requests.

# decimal_prime_entropy.py
# SPDX-License-Identifier: Apache-2.0

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def is_mersenne_prime(p):
    if not sp.isprime(p):
        return False
    mp = 2**p - 1
    return sp.isprime(mp)

def find_mersenne_exponents(start=2, end=100):
    exponents = [p for p in sp.primerange(start, end) if is_mersenne_prime(p)]
    return exponents

def expand_hash_grid(exponents, size=10):
    grid = np.zeros((size, size))
    for i, p in enumerate(exponents[:size**2]):
        grid.flat[i] = p + np.random.uniform(0, 0.1)  # Decimal jitter
    neg_grid = -grid  # Negative symmetry
    return np.vstack((grid, neg_grid))

def decimal_prime_entropy(grid):
    # 'Decimal primes' as entropy from decimal expansions, e.g., pi decimals primes
    pi_str = str(sp.pi.n(100))
    pi_digits = [int(d) for d in pi_str[2:]]
    primes = [sp.prime(i+1) for i in range(len(pi_digits))]
    decimal_entropy = np.array(pi_digits) / primes[:len(pi_digits)]  # Fractional 'primes'
    return grid + decimal_entropy[:grid.size].reshape(grid.shape)

if __name__ == "__main__":
    exponents = find_mersenne_exponents(2, 100)
    print("Mersenne exponents (p<100):", exponents)
    grid = expand_hash_grid(exponents)
    grid = decimal_prime_entropy(grid)
    print("Grid sample:\n", grid[:5, :5])
    plt.imshow(grid, cmap='viridis')
    plt.title("Expanded Grid with Mersenne, Negative, Decimal")
    plt.show()
    large_p = 136279841
    print(f"Largest known p={large_p}, for p=194062501 too large to check.")
