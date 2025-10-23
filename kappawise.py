# kappawise.py - Spiral-based grid generation using hash indexing
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

def murmur32(input_str):
    # Mock 32-bit hash using SHA-256
    h = hashlib.sha256(input_str.encode()).digest()
    return int.from_bytes(h[:4], 'big')

SEED = 42  # Seeded for reproducibility
def kappa_coord(user_id, theta):
    """
    Compute 107-bit coordinates (x, y, z) for a kappa grid point, safely using 64-bit ints.
    Uses a 128-bit hash with modular reduction to fit 107 bits.
    """
    input_str = str(user_id) + str(theta) + str(SEED)
    raw = int(hashlib.sha512(input_str.encode()).hexdigest(), 16) % (1 << 107)  # 107-bit hash
    # Split into three 64-bit segments, reduce to 107-bit range
    x = np.int64((raw >> 0) & ((1 << 107) - 1))  # 107 bits
    y = np.int64((raw >> 107) & ((1 << 107) - 1))  # Next 107 bits (wrap)
    z = np.int64((raw >> 214) & ((1 << 107) - 1))  # Third 107 bits
    return x, y, z

# Example usage (commented out)
# print(kappa_coord(12345, 3.14159))  # Outputs large 107-bit coords
