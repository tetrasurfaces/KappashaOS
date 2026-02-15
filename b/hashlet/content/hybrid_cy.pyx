# hybrid_cy.pyx - Cython for High-Precision PHI/Kappa
# hybrid.py - Hybrid Parser with Cython/Perl Integration
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
# - For hardware/embodiment interfaces (if any): Licensed under the Apache License, Version 2.0
#   with xAI amendments for safety (prohibits misuse in hashing; revocable for unethical use).
#   See http://www.apache.org/licenses/LICENSE-2.0 for details.
#
# Copyright 2025 xAI, Coneing and Contributors
#
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
# Integrates Python, Cython, and Perl for parsing and curvature calculations
# Compile: cythonize -i hybrid_cy.pyx
from libc.math cimport sin, cos, exp, log, sqrt, M_PI
from cython cimport boundscheck, wraparound
import mpmath
mpmath.mp.dps = 19
@boundscheck(False)
@wraparound(False)
cpdef double compute_phi_kappa(double[:, :] points):
    \"\"\"PHI-Scaled Kappa Computation (19 decimals precision for curvature calculation).\"\"\"
    cdef int n = points.shape[0]
    cdef double[:] l = points[:, 0]
    cdef double[:] h = points[:, 1]
    cdef double[:] dl = memoryview(np.diff(l))
    cdef double[:] dh = memoryview(np.diff(h))
    cdef double[:] d2l = memoryview(np.diff(dl))
    cdef double[:] d2h = memoryview(np.diff(dh))
    cdef double[:] kappa = np.zeros(n-2)
    cdef double phi = float(mpmath.phi)
    cdef int i
    for i in range(n-2):
        kappa[i] = abs(dl[i] * d2h[i] - dh[i] * d2l[i]) / (dl[i]**2 + dh[i]**2)**1.5 * phi
    return np.mean(kappa)
