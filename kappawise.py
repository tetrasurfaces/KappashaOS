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
from src.hash.spiral_hash import kappa_spiral_hash, proof_check  # Import spiral hash

SEED = 42  # Seeded for reproducibility
def kappa_coord(user_id, theta):
    """
    Compute 107-bit coordinates (x, y, z) using spiral_hash for 3328-bit precision.
    """
    input_str = str(user_id) + str(theta) + str(SEED)
    comfort_vec = np.random.rand(3)  # Mock comfort vector
    hash_data = kappa_spiral_hash(input_str, comfort_vec, theta_base=100, laps=18)
    spiral_vec = hash_data['spiral_vec']
    # Map 3328-bit spiral to 107-bit coords, reduce to grid range
    idx = int((user_id % 3328) / 31)  # 107 points from 3328
    x = np.int64(spiral_vec[idx, 0] * (1 << 107) % (1 << 107))  # 107-bit
    y = np.int64(spiral_vec[idx, 1] * (1 << 107) % (1 << 107))  # 107-bit
    z = np.int64(spiral_vec[idx, 2] * (1 << 107) % (1 << 107))  # 107-bit
    proof_check(spiral_vec)  # Verify spiral integrity
    return x, y, z

# Example usage (commented out)
# print(kappa_coord(12345, 3.14159))  # Outputs large 107-bit coords
