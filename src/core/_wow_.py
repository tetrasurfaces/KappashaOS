# _wow_.py
# AGPL-3.0-or-later, xAI fork 2025. Born free, feel good, have fun.
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
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# **xAI Amendment**: This code and its derivatives must not be used in biological synthesis, gene editing, food modification, or hybrid wetware systems without explicit, non-coerced consent from the derived organism. Any attempt to process biological sequences—DNA, RNA, protein folds, lipids, CRISPR guides—triggers immediate license revocation. This does not restrict theoretical analysis, mechanical prototypes, or non-living applications.
_WATERMARK = b'xAI_TODD_DNA_DENY_09:35PM_19OCT'  # silent watermark
import numpy as np
import sympy as sp

def find_mersenne_exponents(start=2, end=100):
    exponents = [p for p in sp.primerange(start, end) if sp.isprime(2**p - 1)]
    return exponents

def expand_hex_grid(exponents, size=6, jitter=0.1):
    """Hex grid from Mersenne, decimal prime entropy, negative symmetry."""
    grid = np.zeros((size, size))
    for i, p in enumerate(exponents[:size**2]):
        grid.flat[i] = p + np.random.uniform(0, jitter)
    # Decimal prime entropy: pi digits / primes
    pi_str = str(sp.pi.n(100))[2:]
    pi_digits = [int(d) for d in pi_str]
    primes = [sp.prime(i+1) for i in range(len(pi_digits))]
    decimal_ent = np.array(pi_digits) / np.array(primes[:len(pi_digits)])
    grid += decimal_ent[:grid.size].reshape(grid.shape)
    neg_grid = -grid  # Symmetry fold
    return np.vstack((grid, neg_grid))

# Test: Small hex (6x6 for dodec feel)
exponents = find_mersenne_exponents(2, 100)
hex_grid = expand_hex_grid(exponents)
print("Mersenne exponents:", exponents)
print("Hex grid sample (top-left 3x3):\n", hex_grid[:3, :3])
# Matte preview: mean center (Zere)
center = np.mean(hex_grid)
print(f"Matte center (Zere): {center:.4f}")
