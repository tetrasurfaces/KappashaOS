# Copyright 2025 xAI
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# For hardware/embodiment interfaces: Licensed under the Apache License, Version 2.0
# with xAI amendments for safety (prohibits misuse in hashing; revocable for unethical use).
# See http://www.apache.org/licenses/LICENSE-2.0 for details.
# core_array_sim.py: Simulate a kappa grid core array with piezo ripple.
# Builds on puff_grid; for chip modeling under torque/pressure.
# Usage: python core_array_sim.py --size 20 --ripple 0.05

import argparse
import numpy as np
from puff_grid import generate_kappa_grid, simulate_drift  # Reuse from new file.

def simulate_core_array(size=20, ripple_factor=0.05):
    """Model a 3D-stacked kappa array with ripple (flex under piezo).
    Args:
        size (int): Base grid size.
        ripple_factor (float): Flex amount (<1 Nm torque simulation).
    Returns:
        np.array: Rippled 3D array.
    """
    base_grid = generate_kappa_grid(size)
    # Stack layers with offset (golden ratio for minimal crosstalk).
    golden_ratio = (1 + np.sqrt(5)) / 2
    layers = [base_grid + i * golden_ratio * ripple_factor for i in range(3)]  # 3-layer stack.
    stacked = np.stack(layers, axis=0)
    # Apply drift to whole stack (seismology/pressure influence).
    rippled, _ = simulate_drift(stacked, ripple_factor)
    return rippled

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulate kappa core array.')
    parser.add_argument('--size', type=int, default=20, help='Grid size.')
    parser.add_argument('--ripple', type=float, default=0.05, help='Ripple factor.')
    args = parser.parse_args()
    
    array = simulate_core_array(args.size, args.ripple)
    print(f"Rippled Core Array Shape: {array.shape}")
    print(f"Sample Layer: {array[0][:5]}")  # Preview.
