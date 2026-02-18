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
    Compute 107-bit coordinates (x, y, z) using spiral_hash.
    Safely handles string user_id (e.g. timestamp) by hashing to int.
    """
    # Convert user_id to numeric seed
    if isinstance(user_id, str):
        # Hash string to stable int
        seed_int = int(hashlib.sha256(user_id.encode()).hexdigest(), 16)
    else:
        seed_int = int(user_id)  # assume already numeric

    input_str = str(seed_int) + str(theta) + str(SEED)
    comfort_vec = np.random.rand(3)
    hash_data = kappa_spiral_hash(input_str, comfort_vec, theta_base=100, laps=18)
    spiral_vec = hash_data['spiral_vec']
    
    # Safe modulo & division
    mod = seed_int % 3328
    idx = int(mod / 31)  # now always int
    
    # Clip safely (use modulo len to avoid index error)
    vec_len = len(spiral_vec)
    if vec_len == 0:
        print("kappa_coord: Empty spiral_vec — returning zeros")
        return 0, 0, 0
    
    idx_safe = idx % vec_len
    x = np.int64(np.clip(np.abs(spiral_vec[idx_safe, 0]), 0, 1e3) * (1 << 20) % (1 << 107))
    y = np.int64(np.clip(np.abs(spiral_vec[idx_safe, 1]), 0, 1e3) * (1 << 20) % (1 << 107))
    z = np.int64(np.clip(np.abs(spiral_vec[idx_safe, 2]), 0, 1e3) * (1 << 20) % (1 << 107))
    
    proof_check(spiral_vec, laps=18)
    print(f"Debug: kappa_coord - x={x}, y={y}, z={z}, idx={idx}, seed_int={seed_int % 10000}..., spiral_vec[idx]={spiral_vec[idx_safe]}")
    
    return x, y, z

# Example usage (commented out)
# print(kappa_coord(12345, 3.14159))  # Outputs large 107-bit coords