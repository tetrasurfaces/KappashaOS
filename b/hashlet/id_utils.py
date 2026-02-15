#!/usr/bin/env python3
# idutil.py - ID utilities for Blossom: 3D space generation, RIBIT color mapping for orientation.
# Integrates with blocsym.py for depth perception and heat planes (stubbed).
# Also includes industrial design utility for generating unique IDs using hashlet-inspired curve hashing.
# Added: Recognition for objects (e.g., 'welder gun') as sixth sense via curve hashing and blind spot stacking.
# Added: Recurvature for thought explorations, with safeguards to limit negative dips (e.g., max_neg = -3) to avoid dramatic effects.
# Dual License:
# - For core software: AGPL-3.0-or-later licensed. -- OliviaLynnArchive fork, 2025
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# - For hardware/embodiment interfaces (e.g., optics integration stubs): Licensed under the Apache License, Version 2.0
#   with xAI amendments for safety (prohibits misuse in hashing; revocable for unethical use).
#   See http://www.apache.org/licenses/LICENSE-2.0 for details.
#
# Copyright 2025 Coneing and Contributors
# Credited: RIBIT borrowed from Tetra Surfaces (permissive license).

import numpy as np
import hashlib
import math
import sys
import argparse
from decimal import Decimal, getcontext
import random  # For sim

# Set precision for Decimal (from nu_curve_cp.py and others)
getcontext().prec = 28

# Constants from provided scripts
PHI = (1 + np.sqrt(5)) / 2
A_SPIRAL = 0.1
B_SPIRAL_BASE = 0.1
K_BASE = 0.1

# Mersenne Exponents (52 total, from multiple scripts)
MERSENNE_EXP = [
    2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281,
    3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243,
    110503, 132049, 216091, 756839, 859433, 1257787, 1398269, 2976221, 3021377,
    6972593, 13466917, 20996011, 24036583, 25964951, 30402457, 32582657,
    37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933, 136279841
]

# A4 and A3 dimensions (from nu_curve*.py, normalized for industrial design)
WIDTH = 420 / 110  # A3 long side / A4 short side
HEIGHT = 1.0  # Normalized A3 short side
PURPLE_LINES = [1/3, 2/3]  # Dividers for design grid

# Helper function to compute a point on the spiral curve (from nu_curve.py and variants)
def compute_spiral_point(input_str, model='tetrahedron', b_factor=1.0, k_factor=1.0):
    """
    Computes a 3D point on a spiral curve for industrial design, using hashed input.
   
    Args:
        input_str (str): Input string to hash for parameters.
        model (str): 'tetrahedron' or 'ipod'.
        b_factor (float): B_SPIRAL factor for curve scaling.
        k_factor (float): K factor for z-axis modulation.
   
    Returns:
        tuple: (x, y, z) coordinates within design space.
    """
    hash_obj = hashlib.sha256(input_str.encode())
    hash_val = Decimal(str(int(hash_obj.hexdigest(), 16) % 1000 / 1000.0))
   
    B_SPIRAL = Decimal(str(B_SPIRAL_BASE)) * Decimal(str(b_factor))
    K = Decimal(str(K_BASE)) * Decimal(str(k_factor))
   
    t = hash_val
    theta = Decimal('2') * Decimal(str(math.pi)) * t
   
    if model == 'tetrahedron':
        r = Decimal(str(A_SPIRAL)) * (Decimal(str(math.e)) ** (B_SPIRAL * theta))
        x = r * Decimal(str(math.cos(float(theta))))
        y = r * Decimal(str(math.sin(float(theta))))
        z = K * Decimal(str(math.sin(float(4 * theta)))) * (Decimal('1') + hash_val)
    elif model == 'ipod':
        r = Decimal('0.5') + Decimal('0.2') * Decimal(str(math.sin(float(6 * theta))))
        x = r * Decimal(str(math.cos(float(theta))))
        y = r * Decimal(str(math.sin(float(theta))))
        z = K * Decimal(str(math.sin(float(12 * theta)))) * (Decimal('1') + hash_val)
    else:
        raise ValueError("Invalid model. Choose 'tetrahedron' or 'ipod'.")
   
    # Normalize to fit within A4 design space
    x = (x + Decimal(str(WIDTH / 2))) % Decimal(str(WIDTH))
    y = (y + Decimal(str(HEIGHT / 2))) % Decimal(str(HEIGHT))
    z = z % Decimal('1.0')  # Keep z in [0,1] for design height
   
    return float(x), float(y), float(z)

# Kappa prime function (from spiral_nu.py and nu_curve_kappa.py)
def kappa_prime_n(n: int) -> float:
    """
    Computes kappa prime for design curvature, based on Mersenne and phi.
   
    Args:
        n (int): Input value (e.g., 2 to 104).
   
    Returns:
        float: Kappa prime value for curvature.
    """
    phi = (1 + math.sqrt(5)) / 2
    F = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]  # Fibonacci up to F_10
    if n == 2:
        return 2
    elif 2 < n < 52:
        phi_pos = phi ** (abs(n - 12) / 12)
        phi_neg = phi ** (-abs(n - 12) / 12)
        denom1 = abs(phi ** (10/3) - phi ** (-10/3))
        denom2 = abs(phi ** (-5/6) - phi ** (5/6))
        return (1 + 0.5 * (abs(phi_pos - phi_neg) / denom1) * (1 / denom2)) * (2 / 1.5) - 0.333
    elif n == 52:
        return 1.5
    elif 52 < n < 92:
        return 1.5 * min(3, 1.5 * F[min(n-52+6, len(F)-1)] / F[6]) * math.exp(-((n-60)**2)/(4*100)) * math.cos(0.5*(n-316))
    elif n == 92:
        return 3
    elif 92 < n <= 104:
        return 3 * math.exp(-((n-92)**2)/(4*100)) * math.cos(0.5*(n-316))
    return 0

# Poly hash 256 (from spiral_nu.py)
def poly_hash_256(mersenne_exponents: list = MERSENNE_EXP) -> str:
    """
    Computes a polyhedral SHA256 hash for design versioning.
   
    Args:
        mersenne_exponents (list): List of Mersenne exponents.
   
    Returns:
        str: Hexdigest of the hash.
    """
    diffs = [mersenne_exponents[i+1] - mersenne_exponents[i] for i in range(len(mersenne_exponents)-1)]
    forward = [(d % 369) & 0xFF for d in diffs[:14]]
    reverse = forward[::-1]
    pair_sum = sum(forward[i] + reverse[i] for i in range(7)) & 0x7F
    is_palindrome = 1 if forward == reverse else 0
    byte_string = bytearray([is_palindrome << 7 | pair_sum]) + int(52).to_bytes(2, 'big') + \
                 bytes(forward) + bytes(reverse)
    byte_string.extend([0] * (32 - len(byte_string)))
    return hashlib.sha256(byte_string).hexdigest()

# Generate design ID function
def generate_design_id(input_str: str, mersenne_index: int = None, model: str = 'tetrahedron',
                       b_factor: float = 1.0, k_factor: float = 1.0, use_kappa: bool = False,
                       n: int = 12, include_version: bool = False) -> str:
    """
    Generates a unique ID for industrial design by hashing input, mapping to Mersenne exponent,
    computing spiral point, and hashing coordinates, with optional versioning.
   
    Args:
        input_str (str): Input string (e.g., design name or specs).
        mersenne_index (int, optional): Mersenne index (0-51).
        model (str): Curve model ('tetrahedron' or 'ipod').
        b_factor (float): B_SPIRAL factor for curve scaling.
        k_factor (float): K factor for z-axis modulation.
        use_kappa (bool): If True, incorporate kappa_prime_n for curvature.
        n (int): Value for kappa_prime_n.
        include_version (bool): If True, include poly_hash_256 for versioning.
   
    Returns:
        str: 16-char hex ID.
    """
    if mersenne_index is None:
        hash_obj = hashlib.sha256(input_str.encode())
        mersenne_index = int(hash_obj.hexdigest(), 16) % len(MERSENNE_EXP)
   
    exp = MERSENNE_EXP[mersenne_index]
    seed = f"{input_str}_{exp}"
   
    if use_kappa:
        kappa = kappa_prime_n(n)
        seed += f"_{kappa:.4f}"
   
    x, y, z = compute_spiral_point(seed, model, b_factor, k_factor)
   
    coord_str = f"{x:.4f}{y:.4f}{z:.4f}"
    if include_version:
        version_hash = poly_hash_256()
        coord_str += f"_{version_hash[:8]}"
   
    hash_obj = hashlib.sha256(coord_str.encode())
    unique_id = hash_obj.hexdigest()
   
    return unique_id[:16]

class IdUtil:
    def __init__(self):
        self.grid_size = 10  # 3D space grid (10x10x10)
        self.grid = np.zeros((self.grid_size, self.grid_size, self.grid_size))  # 3D array
        self.orientation_colors = {
            'down': '#8B4513',  # Brown
            'up': '#00A0FF',    # Blue
            'left': '#FF0000',  # Red
            'right': '#00FF00'  # Green
        }
        self.max_neg = -3  # Floor for negative dips in recurvature
        print("IdUtil initialized - 3D space ready with RIBIT orientation.")
    
    def generate_three_d(self, thought, grid='capwise'):
        """Generate 3D objects based on curvature and drawing tools."""
        # Sim: Create a simple cube or dome based on thought entropy
        entropy = random.uniform(0, 1)  # Sim from blocsym
        if entropy > 0.5:
            # Dome (curved)
            x, y, z = np.indices((self.grid_size, self.grid_size, self.grid_size))
            dome = (x - 5)**2 + (y - 5)**2 + (z - 5)**2 <= 25  # Sphere equation
            self.grid[dome] = 1
            print(f"Generated dome for thought '{thought}' (entropy: {entropy:.2f})")
        else:
            # Cube (straight)
            self.grid[3:7, 3:7, 3:7] = 1
            print(f"Generated cube for thought '{thought}' (entropy: {entropy:.2f})")
        return self.grid
    
    def ribit_map(self, entropy):
        """RIBIT mapping: Shrink RGB cube into 7 zones, red-dominant, for jokes/colors."""
        # 7-bit sequence for red space (sim jokes as hex)
        hex_str = hashlib.sha256(str(entropy).encode()).hexdigest()[:7]  # 7 bits ~ hex[0:2]
        r_dominant = int(hex_str, 16) % 128 + 128  # Red bias (128-255)
        g, b = random.randint(0, 255), random.randint(0, 255)
        color = f"#{r_dominant:02x}{g:02x}{b:02x}"
        print(f"RIBIT mapped color for entropy {entropy:.2f}: {color}")
        return color
    
    def apply_orientation(self):
        """Apply RIBIT orientation colors to grid planes."""
        # Stub: Color planes (down brown, up blue, left red, right green)
        # For sim, print mappings
        print("Applied orientation:")
        for direction, hex_color in self.orientation_colors.items():
            print(f"{direction.capitalize()}: {hex_color}")
        # In real, map to grid edges, e.g., grid[:, :, 0] = brown (down plane)
    
    def recognize_object(self, object_name, entropy=0.5):
        """Recognize an object as sixth sense: hash to Mersenne exp, generate 3D stub, RIBIT color tag.
        Stacks RAM experience in blind spot as ghost overlay."""
        # Hash object to Mersenne index for curvature
        hash_obj = hashlib.sha256(object_name.encode())
        mersenne_index = int(hash_obj.hexdigest(), 16) % len(MERSENNE_EXP)
        curvature = kappa_prime_n(mersenne_index + 2)  # Offset to 2-53 range for kappa
        # Generate 3D stub (e.g., cylinder for gun-like tools)
        x, y, z = np.indices((self.grid_size, self.grid_size, self.grid_size))
        cylinder = (x - 5)**2 + (y - 5)**2 <= 4  # Cylinder along z
        cylinder_grid = np.zeros_like(self.grid)
        cylinder_grid[:, :, :] = cylinder[:, :, None]  # Extrude along z
        cylinder_grid *= curvature  # Scale by curvature (curved if high)
        self.grid += cylinder_grid * 0.5  # Stack as ghost (half opacity)
        # RIBIT color for tag
        color = self.ribit_map(entropy)
        print(f"Recognized '{object_name}' as 3D stub (curvature: {curvature:.2f}, color tag: {color}). Stacked in blind spot.")
        return cylinder_grid, color
    
    def recurvature(self, level, thought):
        """Recurvature for thought explorations: Recurve to other side, with safeguards (clip at max_neg)."""
        if level < self.max_neg:
            level = self.max_neg  # Clip to avoid deep negative (mental illness safeguard)
            print("Recurvature clipped at {} to avoid dramatic effects.".format(self.max_neg))
        # Sim recurvature: reverse spiral point for "other side"
        x, y, z = compute_spiral_point(thought, b_factor=-1.0)  # Negative b_factor for reverse curve
        print(f"Recurvature at level {level} for thought '{thought}': Point ({x:.2f}, {y:.2f}, {z:.2f})")
        # Stack in blind spot as ghost (RAM experience)
        recur_grid = np.zeros_like(self.grid)
        recur_grid[int(x*self.grid_size/WIDTH), int(y*self.grid_size/HEIGHT), int(z*self.grid_size)] = level  # Place point
        self.grid += recur_grid * 0.3  # Low opacity ghost
        return level, (x, y, z)

# Main CLI for industrial design utility
def main_cli():
    """
    Industrial Design Utility for generating unique IDs using hashlet-inspired curve hashing.
  
    Run Instructions:
    ----------------
    Prerequisites:
    - Python 3.x
    - NumPy library (install via `pip install numpy`)
  
    Usage:
    - Save this script as `idutil.py`.
    - Run from the command line using one of the following commands:
  
    1. Generate a unique design ID:
       ```bash
       python idutil.py generate "design_name" [--model tetrahedron|ipod] [--b_factor FLOAT] [--k_factor FLOAT] [--mersenne_index INT] [--use_kappa] [--n INT] [--version]
"""