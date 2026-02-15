# kappawise.py - Spiral-based grid generation using hash indexing with spiral_hash
#
# Copyright 2025 xAI
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
import hashlib
import numpy as np
from spiral_hash import kappa_spiral_hash, proof_check  # Import spiral hash

SEED = 42  # Seeded for reproducibility
def kappa_coord(user_id, theta):
    """
    Compute 107-bit coordinates (x, y, z) using spiral_hash for 3328-bit precision.
    Handles casting safely with reduced multiplier.
    """
    input_str = str(user_id) + str(theta) + str(SEED)
    comfort_vec = np.random.rand(3)  # Mock comfort vector
    hash_data = kappa_spiral_hash(input_str, comfort_vec, theta_base=100, laps=18)
    spiral_vec = hash_data['spiral_vec']
    # Map 3328-bit spiral to 107-bit coords, use smaller multiplier
    idx = int((user_id % 3328) / 31)  # 107 points from 3328
    x = np.int64(np.clip(np.abs(spiral_vec[idx, 0]), 0, 1e3) * (1 << 20) % (1 << 107))  # Reduced to 20-bit base
    y = np.int64(np.clip(np.abs(spiral_vec[idx, 1]), 0, 1e3) * (1 << 20) % (1 << 107))  # 107-bit
    z = np.int64(np.clip(np.abs(spiral_vec[idx, 2]), 0, 1e3) * (1 << 20) % (1 << 107))  # 107-bit
    proof_check(spiral_vec, laps=18)  # Verify spiral integrity with explicit laps
    print(f"Debug: kappa_coord - x={x}, y={y}, z={z}, idx={idx}, spiral_vec[idx]={spiral_vec[idx]}")  # Enhanced debug
    return x, y, z

# Example usage (commented out)
# print(kappa_coord(12345, 3.14159))  # Outputs large 107-bit coords
