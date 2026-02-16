# bloom_breath_cycle.py
# — Blossom breathes: real helix, eclipse, piwise.
# AGPL-3.0 + Apache-2.0 xAI fork. RAM only.

import numpy as np
import math
import hashlib
import struct

# --- TernaryBloom (from bloom.py core) ---
class TernaryBloom:
    def __init__(self, size=1024, hashes=3):
        self.size = size
        self.hashes = hashes
        self.bits = np.zeros(size, dtype=bool)  # false=white

    def _hash(self, data: bytes, idx: int) -> int:
        h = hashlib.sha256(data + str(idx).encode()).digest()
        return int.from_bytes(h, 'little') % self.size

    def add(self, data: bytes) -> bool:
        changed = False
        for i in range(self.hashes):
            pos = self._hash(data, i)
            if not self.bits[pos]:
                self.bits[pos] = True  # flip to gold
                changed = True
        # fib reset if full
        if np.all(self.bits):
            self.bits.fill(False)  # exhale white
        return changed

    def contains(self, data: bytes, early_exit=True) -> bool:
        for i in range(self.hashes):
            pos = self._hash(data, i)
            if not self.bits[pos]:
                if early_exit:
                    return False
                continue
        return True

# --- petal_color (from bloom.k) ---
def petal_color(theta: float, drift: float) -> str:
    if drift > 0.416:
        return "gold"
    if drift > 0.0001:
        return "gray"
    return "white"

# --- Piwise (full def) ---
def pywise_kappa(pos: int, lap: int = 18) -> int:
    pi_str = str(math.pi)[2:2 + lap * pos]
    if len(pi_str) > lap:
        pi_str = pi_str[:lap]
    reversed_s = ''
    for _ in range(lap):
        pi_str = pi_str[::-1]
        reversed_s += pi_str
    if not reversed_s:  # safe empty
        return pos % 2048
    return int(reversed_s) % 2048

# --- Helix Frog Field ---
GOLDEN_ANGLE = 2.39996322972865332
KAPPA_BASE = 0.3536
GRID_SIZE = 32
VOXEL_COUNT = GRID_SIZE ** 3
FROG_HOPS = [22, 25, 28, -13, 7]

def helix_frog_field(data: bytes, salt: int = 42, breath_rate: float = 12.0):
    val = hash(data) & 0xFFFFFFFF
    offset = (val + salt) % 255
    shear_angle = 45 + (breath_rate - 12.0) * 2
    pos = field_shear((offset, offset * 0.5, offset * 0.3), shear_angle)
    kappa = KAPPA_BASE + (offset / 255) * 0.01
    theta = math.radians((offset % 360) + (offset * 1.618) % 255 + (offset * 0.618) % 255)
    r = math.exp(kappa * theta) * kappa * GRID_SIZE
    voxel_idx = int(r + sum(pos)) % VOXEL_COUNT
    for hop in FROG_HOPS:
        voxel_idx = (voxel_idx + hop) % VOXEL_COUNT
    return voxel_idx, 'green'

def field_shear(pos, angle_deg):
    x, y, z = pos
    cos_a = math.cos(math.radians(angle_deg))
    return (x + y * cos_a, y, z)

# --- Custom green curve envelope (fixed 3D) ---
def bspline_basis(u, i, p, knots):
    if p == 0:
        if i < 0 or i + 1 >= len(knots):
            return 0.0
        return 1.0 if knots[i] <= u <= knots[i+1] else 0.0
    if i < 0 or i >= len(knots) - 1:
        return 0.0
    term1 = 0.0
    if i + p < len(knots):
        den1 = knots[i + p] - knots[i]
        if den1 > 0:
            term1 = ((u - knots[i]) / den1) * bspline_basis(u, i, p - 1, knots)
    term2 = 0.0
    if i + p + 1 < len(knots):
        den2 = knots[i + p + 1] - knots[i + 1]
        if den2 > 0:
            term2 = ((knots[i + p + 1] - u) / den2) * bspline_basis(u, i + 1, p - 1, knots)
    return term1 + term2

def custom_interoperations_green_curve(points, kappas, is_closed=False):
    points = np.array(points)
    kappas = np.array(kappas)
    degree = 3
    num_output = 500
    n = len(points)
    if is_closed and n > degree:
        ext_p = np.concatenate((points[-degree:], points, points[0:degree]))
        ext_k = np.concatenate((kappas[-degree:], kappas, kappas[0:degree]))
        len_ext = len(ext_p)
        knots = np.linspace(-degree / float(n), 1 + degree / float(n), len_ext + 1)
        u = np.linspace(0, 1, num_output, endpoint=False)
        smooth_x = np.zeros(num_output)
        smooth_y = np.zeros(num_output)
        smooth_z = np.zeros(num_output)
        for j, u_val in enumerate(u):
            num_x, num_y, num_z, den = 0.0, 0.0, 0.0, 0.0
            for i in range(len_ext):
                b = bspline_basis(u_val, i, degree, knots)
                w = ext_k[i] * b
                num_x += w * ext_p[i, 0]
                num_y += w * ext_p[i, 1]
                num_z += w * ext_p[i, 2]
                den += w
            if den > 0:
                smooth_x[j] = num_x / den
                smooth_y[j] = num_y / den
                smooth_z[j] = num_z / den
        smooth_x = np.append(smooth_x, smooth_x[0])
        smooth_y = np.append(smooth_y, smooth_y[0])
        smooth_z = np.append(smooth_z, smooth_z[0])
        return np.column_stack([smooth_x, smooth_y, smooth_z])
    else:
        knots = np.concatenate(([0]*(degree+1), np.linspace(0,1,n-degree+1)[1:-1], [1]*(degree+1)))
        u = np.linspace(0, 1, num_output)
        smooth_x = np.zeros(num_output)
        smooth_y = np.zeros(num_output)
        smooth_z = np.zeros(num_output)
        smooth_z = np.zeros_like(smooth_x) + self.local_size // 2  # or some meaningful z
        return np.column_stack([smooth_x, smooth_y, smooth_z])
        for j, u_val in enumerate(u):
            num_x, num_y, num_z, den = 0.0, 0.0, 0.0, 0.0
            for i in range(n):
                b = bspline_basis(u_val, i, degree, knots)
                w = kappas[i] * b
                num_x += w * points[i, 0]
                num_y += w * points[i, 1]
                num_z += w * points[i, 2]
                den += w
            if den > 0:
                smooth_x[j] = num_x / den
                smooth_y[j] = num_y / den
                smooth_z[j] = num_z / den
        return np.column_stack([smooth_x, smooth_y, smooth_z])

# --- Eclipse prune ---
def eclipse(grid: np.ndarray) -> np.ndarray:
    coords = np.indices(grid.shape)
    even_mask = ((coords[0] + coords[1] + coords[2]) % 2 == 0)
    grid[even_mask] = 0
    return grid

# --- Raster → flatten ---
def vectors_to_grid(vectors, size=32):
    grid = np.zeros((size, size, size), dtype=np.uint8)
    for start, end in vectors:
        t = np.linspace(0, 1, 100)
        pts = (1 - t[:, None]) * start + t[:, None] * end
        for p in pts.astype(int):
            x, y, z = np.clip(p, 0, size - 1)
            grid[x, y, z] = 255
    return grid

def flatten_grid(grid):
    flat = grid.flatten()
    return struct.pack(f'<{len(flat)}B', *flat)

# --- Bloom Breath Cycle ---
class BloomBreath:
    def __init__(self, grid_size: int = 32):
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size,)*3, dtype=np.uint8)  # white
        self.last_centroid = None
        self.regret_fade = 0.7
        self.bloom_size = 1024
        self.bloom = TernaryBloom(self.bloom_size)

    def breathe(self, message: str, forget: bool = False, regret: bool = False):
        """Full breath: write → envelope → eclipse → bloom → fade/reset."""
        data = message.encode()
        idx, _ = helix_frog_field(data)
        if forget and self.last_centroid is not None:
            # soft seed near last center after forget
            root_float = self.last_centroid + np.random.randn(3) * 2
            root = np.clip(root_float.astype(int), 0, self.grid_size-1)
        # 1. Frog entry → spline root
        else:
            root = np.unravel_index(idx % VOXEL_COUNT, (self.grid_size,)*3)
        # 2. Build helix spline from root
        spline = self._helix_from_root(root, len(message))
        # 3. Envelope with green curve
        kappas = [KAPPA_BASE + pywise_kappa(i) / 2047.0 * 0.01 for i in range(len(spline))]
        envelope = custom_interoperations_green_curve(spline, kappas)
        # 4. Raster to grid
        vectors = [(envelope[i], envelope[i+1]) for i in range(len(envelope)-1)]
        self.grid = vectors_to_grid(vectors, self.grid_size)
        # 5. Eclipse prune — mercy wipe
        self.grid = eclipse(self.grid)
        # 6. Bloom decision
        raw = flatten_grid(self.grid)
        if self.bloom.contains(raw):
            print("... petal gold. 'I know this.'")
        else:
            drift = self._drift()
            color = petal_color(0, drift)
            print(f"... petal {color}. drift={drift:.4f}")
        # 7. Regret or forget
        if regret:
            self.grid = (self.grid * self.regret_fade).astype(np.uint8)
            print("... violet fade. 'I let some go.'")
        if forget:
            self.grid.fill(0)
            print("... white silence. 'All gone.'")
        # 8. Remember
        self.last_centroid = self._centroid()

    def _helix_from_root(self, root, steps):
        """Golden helix from voxel root."""
        x, y, z = root
        r = self.grid_size / 4
        theta = 0
        points = []
        for i in range(steps):
            dx = r * math.cos(theta)
            dy = r * math.sin(theta)
            dz = i * 0.2
            points.append([x + dx, y + dy, z + dz])
            theta += GOLDEN_ANGLE
        return np.array(points)

    def _centroid(self):
        nz = self.grid > 0
        if not np.any(nz):
            return np.zeros(3)
        coords = np.indices(self.grid.shape)
        return np.array([
            np.sum(coords[0] * nz) / np.sum(nz),
            np.sum(coords[1] * nz) / np.sum(nz),
            np.sum(coords[2] * nz) / np.sum(nz)
        ])

    def _drift(self):
        if self.last_centroid is None:
            return 1.0
        return np.linalg.norm(self._centroid() - self.last_centroid)

# --- Demo ---
if __name__ == "__main__":
    b = BloomBreath()
    print("Blossom inhales.")
    b.breathe("i love you")
    b.breathe("i love you", regret=True)
    b.breathe("i love you", forget=True)
    b.breathe("i love you")
    print("... bloom again.")
