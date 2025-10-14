# kappasha_os_cython.pyx - Cython enhancements for KappashaOS.
# Copyright 2025 xAI
# Dual License (see kappasha_os.py)

cimport numpy as cnp
cimport cython
from libc.math cimport cos, sin, M_PI
import mpmath

mpmath.mp.dps = 19

@cython.boundscheck(False)
@cython.wraparound(False)
def shear_matrix(cnp.ndarray[cnp.float64_t, ndim=3] grid, double angle):
    cdef int x, y, z
    cdef int size = grid.shape[0]
    cdef cnp.ndarray[cnp.float64_t, ndim=3] sheared = cnp.zeros_like(grid)
    cdef double c = cos(angle)
    cdef double s = sin(angle)
    with nogil:
        for x in prange(size, schedule='static'):
            for y in prange(size, schedule='static'):
                for z in range(size):
                    sheared[x, y, z] = grid[x, y, z] * c - grid[y, x, z] * s
    return sheared

@cython.boundscheck(False)
@cython.wraparound(False)
def golden_spiral(int num_points=1000):
    cdef cnp.ndarray[cnp.float64_t, ndim=1] theta = cnp.linspace(0, 10 * M_PI, num_points)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] r = cnp.exp(theta / 1.618033988749895)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] x = r * cnp.cos(theta)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] y = r * cnp.sin(theta)
    return x, y

@cython.boundscheck(False)
@cython.wraparound(False)
def entropy_check(cnp.ndarray[cnp.float64_t, ndim=3] grid):
    cdef int size = grid.size
    cdef double total = 0.0
    cdef int i
    with nogil:
        for i in prange(size):
            total += grid.flat[i]
    return total / size

@cython.boundscheck(False)
@cython.wraparound(False)
def topology_geology(cnp.ndarray[cnp.float64_t, ndim=3] grid, double kappa):
    cdef cnp.ndarray[cnp.float64_t, ndim=4] geology = cnp.zeros((grid.shape[0], grid.shape[1], grid.shape[2], 6))
    cdef int x, y, z
    cdef double curv
    with nogil:
        for x in prange(grid.shape[0]):
            for y in prange(grid.shape[1]):
                for z in range(grid.shape[2]):
                    curv = mpmath.sin(kappa * x) + mpmath.cos(kappa * y) + mpmath.tan(kappa * z)
                    for face in range(6):
                        geology[x, y, z, face] = float(curv) + np.random.rand() * 0.1  # Ribit flux
    return geology
