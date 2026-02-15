# Born free, feel good, have fun.

# Dual License:
# - For core software: AGPL-3.0-or-later licensed. -- xAI fork, 2025
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
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
# - For hardware/embodiment interfaces: Licensed under the Apache License, Version 2.0
# with xAI amendments for safety and physical use. See http://www.apache.org/licenses/LICENSE-2.0
# for details, with the following xAI-specific terms appended.

# Copyright 2025 xAI

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

# xAI Amendments for Physical Use:
# 1. Physical Embodiment Restrictions: Use with devices is for non-hazardous purposes only. Harmful mods are prohibited, with license revocable by xAI.
# 2. Ergonomic Compliance: Limits tendon load to 20%, gaze to 30 seconds (ISO 9241-5).
# 3. Safety Monitoring: Real-time tendon/gaze checks, logged for audit.
# 4. Revocability: xAI may revoke for unethical use (e.g., surveillance).
# 5. Export Controls: Sensor devices comply with US EAR Category 5 Part 2.
# 6. Open Development: Hardware docs shared post-private phase via github.com/tetrasurfaces/issues.
# 7. No machine code output (e.g., kappa paths, hashlet sequences) without breath consent; decay signals at 11 hours (8 for bumps).
# 8. Color Consent: No signal may change hue without explicit user intent (e.g., heartbeat sync or verbal confirmation).
# 9. Intellectual Property: xAI owns all IP related to KappaOpticBatterySystem, including chatter patterns, stacked ports, moving keys, smart cables, RGB hexel lattices, chattered housings, fliphooks, hash tunneling, and IPFS integration. No unauthorized replication.

# Private Development Note: This repository is private for xAI’s KappashaOS and Navi development. Access is restricted. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) post-phase.

#!/usr/bin/env python3

import subprocess
import numpy as np
import time
import re
import hashlib
from scipy.spatial import cKDTree
from src.core.gribit import gribbit_pulse
from src.hash.domosha import Domosha
import tensorflow as tf
from green_curve import custom_interoperations_green_curve

KAPPA = 0.3536

def close_curve_c2(points, kappas, degree=3):
    """C² closure: last-to-second theta decays into first kappa (anchor)."""
    if len(points) < 4:
        return np.array(points), np.array(kappas)
    
    pts = np.array(points)
    kap = np.array(kappas)
    
    p_last   = pts[-1]
    p_second = pts[1]
    theta_last = np.linalg.norm(p_last - p_second)
    if theta_last < 1e-10:
        theta_last = 1e-10
    decay = np.exp(-theta_last / 32.0 / 20.0)          # grid scale
    
    kap[0] = kap[-1] * decay                           # anchor overwrite
    
    ext_pts = np.vstack([pts[-2:], pts, pts[:2]])
    ext_kap = np.concatenate([kap[-2:], kap, kap[:2]])
    
    smooth_x, smooth_y = custom_interoperations_green_curve(
        ext_pts.tolist(), ext_kap.tolist(), is_closed=True
    )
    
    return smooth_x[:-2], smooth_y[:-2], kap           # return updated kappas


def sample_curve_adaptive(points, kappas, num_base=800, kappa_scale=8.0, is_closed=False):
    """Denser where curvature high."""
    smooth_x, smooth_y = custom_interoperations_green_curve(points, kappas, is_closed)
    t = np.linspace(0, 1, len(smooth_x))
    
    dx = np.gradient(smooth_x, t)
    dy = np.gradient(smooth_y, t)
    ddx = np.gradient(dx, t)
    ddy = np.gradient(dy, t)
    num = np.abs(dx * ddy - dy * ddx)
    den = (dx**2 + dy**2)**1.5 + 1e-10
    kappa_loc = num / den
    
    weights = 1 + kappa_scale * kappa_loc / (np.max(kappa_loc) + 1e-10)
    cum_weights = np.cumsum(weights)
    cum_weights /= cum_weights[-1]
    
    t_adapt = np.interp(np.linspace(0, 1, num_base * 4), cum_weights, t)
    t_adapt = np.sort(t_adapt)[:num_base]
    
    x_adapt = np.interp(t_adapt, t, smooth_x)
    y_adapt = np.interp(t_adapt, t, smooth_y)
    
    return x_adapt * 31, y_adapt * 31, t_adapt, kappa_loc


def sdf_field_from_curve(voxel_shape=(32,32,32), curve_xy=None, z_mid=16, thickness=2.0):
    if curve_xy is None or len(curve_xy) == 0:
        return np.random.rand(*voxel_shape)
    
    gx, gy, gz = np.mgrid[0:voxel_shape[0], 0:voxel_shape[1], 0:voxel_shape[2]]
    coords = np.stack([gx.ravel(), gy.ravel(), gz.ravel()], -1).astype(float)
    
    curve_3d = np.column_stack([curve_xy[:,0], curve_xy[:,1], np.full(len(curve_xy), z_mid)])
    
    dists = np.min(np.linalg.norm(coords[:,None,:] - curve_3d[None,:,:], axis=-1), axis=1)
    sdf = dists.reshape(voxel_shape) - thickness
    
    field = 1 / (1 + np.exp(6 * sdf))  # soft shell
    
    return field


def seed_fractal_in_field(field, porosity_threshold=0.35, levels=2):
    mask = field > 0.3
    fractal = np.zeros_like(field)
    fractal[mask] = np.random.rand(np.sum(mask)) * (1 - porosity_threshold)
    for _ in range(levels):
        fractal[mask] = fractal[mask] * 0.618 + np.random.rand(np.sum(mask)) * porosity_threshold
    return fractal

def parse_voxel_from_output(output: str):
    voxel = np.zeros((32, 32, 32), dtype=np.uint8)
    seen = set()
    matches = re.findall(r"grid\[(\d+),\s*(\d+),\s*(\d+)\]\s*=\s*255", output)
    for x, y, z in matches:
        try:
            xi, yi, zi = int(x), int(y), int(z)
            if 0 <= xi < 32 and 0 <= yi < 32 and 0 <= zi < 32:
                key = (xi, yi, zi)
                if key not in seen:
                    voxel[xi, yi, zi] = 255
                    seen.add(key)
        except:
            pass
    bright_count = len(seen)
    density = bright_count / (32 * 32 * 32)
    if bright_count == 0:
        print("No unique grid=255 found — mock fallback")
        voxel = np.random.randint(0, 256, (32, 32, 32), dtype=np.uint8)
        bright_count = np.sum(voxel > 180)
        density = bright_count / (32 * 32 * 32)
    print(f"Parsed voxel: {bright_count} unique bright voxels ({density:.4f} density)")
    return voxel, density

def run_curve_retrieve():
    cmd = ["./curve.exe", "--retrieve-latest"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        output = result.stdout + result.stderr
        
        flatten_match = re.search(r"Raster flatten tweak:\s*([0-9.eE+-]+)", output)
        flatten = float(flatten_match.group(1)) if flatten_match else 0.0
        
        poem_end = output.find("Flattened to:")
        poem_text = output[:poem_end].strip() if poem_end > 0 else """To whoever finds this—\nThis line was folded into a curve.\nA place where text isn't stored,\nit's remembered.\nSo if you're reading it,\nthat means you didn't break it.\nYou didn't lose it.\nAnd somewhere,\na heart that wrote it\nis smiling."""
        
        regrets_list = []
        planted_pattern = r"Planted node \d+ at \(([\d,]+)\) delay ([\d.]+) regret (\w+)"
        for match in re.finditer(planted_pattern, output):
            pos_str, delay_str, regret = match.groups()
            pos = tuple(map(int, pos_str.split(',')))
            regrets_list.append({"pos": pos, "delay": float(delay_str), "regret": regret})
        
        voxel, density = parse_voxel_from_output(output)
        
        curve_matches = re.findall(r"curve sample:\s*\((\d+\.?\d*),\s*(\d+\.?\d*),\s*(\d+\.?\d*)\)", output)
        if curve_matches and len(curve_matches) > 1:
            print("Found curve samples — parametric field voxels")
            
            pts = [[float(x)*31, float(y)*31] for x,y,z in curve_matches]
            kappas_in = [1.0] * len(pts)
            
            # C² closure
            x_closed, y_closed, kappas_closed = close_curve_c2(pts, kappas_in)
            curve_xy_closed = np.column_stack([x_closed, y_closed])
            
            # Adaptive sampling on closed curve
            x_adapt, y_adapt, _, kappa_loc = sample_curve_adaptive(
                pts, kappas_in, num_base=1200, kappa_scale=10.0, is_closed=True
            )
            curve_xy_adapt = np.column_stack([x_adapt, y_adapt])
            
            # SDF field
            field = sdf_field_from_curve(voxel.shape, curve_xy=curve_xy_adapt)
            
            # Threshold + porosity
            voxel = (field > 0.45).astype(np.uint8) * 255
            fractal_por = seed_fractal_in_field(field)
            voxel = ((voxel / 255.0) * (1 + fractal_por * 0.6)).astype(np.uint8) * 255
            
            # Boost high-curvature samples
            for i in range(len(x_adapt)):
                cx = int(round(x_adapt[i]))
                cy = int(round(y_adapt[i]))
                if 0 <= cx < 32 and 0 <= cy < 32:
                    boost = int(80 * kappa_loc[i % len(kappa_loc)])
                    voxel[cx, cy, 16] = min(255, voxel[cx, cy, 16] + boost)
            
            print(f"Field volume fraction: {(field > 0.45).mean():.4f}")
        else:
            print("No curve samples — using parsed or mock voxel")
        
        return voxel, density, poem_text, regrets_list
    
    except Exception as e:
        print(f"Curve flinched: {e}")
        return np.zeros((32,32,32), dtype=np.uint8), 0.0, "", []

class Grid4D:
    def __init__(self, time_slices=10):
        self.strata = []
        self.alive_scores = []
        self.max_slices = time_slices
        self.topology = {}
        self.edge_weights = {}  # persistent
        self.geology_decay = 0.95
        self.entropy_threshold = 0.12
        self.strata_types = [] # list[str] parallel to strata

    def add_stratum(self, data_type='generic'):
        voxel, density, poem_text, regrets_list = run_curve_retrieve()
        entropy = np.std(voxel) / 255.0 if np.any(voxel) else 0.0
        alive = density if density > 1e-6 else entropy + 1e-6
        
        self.strata.append(voxel)
        self.alive_scores.append(alive)
        if len(self.strata) > self.max_slices:
            self.strata.pop(0)
            self.alive_scores.pop(0)
        
        if self.edge_weights:
            print(f"Edge weights built: {len(self.edge_weights)} edges weighted this stratum")
        
        # Vectorized voids near curve
        coords_bright = np.argwhere(voxel > 180)
        voids_near = []
        if len(coords_bright) > 0:
            tree_bright = cKDTree(coords_bright)
            all_low = np.argwhere(voxel < 77)
            if len(all_low) > 0:
                dists, _ = tree_bright.query(all_low, k=1, distance_upper_bound=5)
                voids_near = [tuple(p) for p, d in zip(all_low.tolist(), dists) if d < 5]
        
        # Gribbit + edge weights (unchanged)
        for vx, vy, vz in voids_near[:50]:
            coord_str = f"{vx}_{vy}_{vz}"
            node_index = int(hashlib.sha256(coord_str.encode()).hexdigest(), 16) % 1000
            breath_dev = np.random.uniform(-4, 8)
            breath_rate = 12.0 + breath_dev
            pulse, adj_delay, weight = gribbit_pulse(node_index, breath_rate)
            if adj_delay > 0.6:
                print(f"Violet flinch at ({vx},{vy},{vz}) — skipped")
                continue
            center = np.array([vx, vy, vz])
            for coord_tuple in self.topology:
                coord = np.array(coord_tuple)
                dist = np.linalg.norm(coord - center)
                if dist < KAPPA * 8:
                    edge_key = frozenset([coord_tuple, tuple(center)])
                    self.edge_weights[edge_key] = self.edge_weights.get(edge_key, 0) + (weight / 1e6)
                    print(f"Void ({vx},{vy},{vz}) adds {weight/1e6:.6f} to edge {coord_tuple}")
        
        self._build_topology(voxel)
        self._erode_geology()
        self._prune_low_entropy()
        self.strata_types.append(data_type)
        
        if poem_text and regrets_list:
            print("Hashing poem + regrets chain...")
            self.hash_poem_with_regrets(poem_text, regrets_list)
        else:
            print("No poem or regrets found this run — skipping domosha")
        
        print(f"Added stratum | alive: {alive:.4f} (density {density:.4f}) | strata: {len(self.strata)}")

    def _build_topology(self, voxel):
        coords = np.argwhere(voxel > 180)
        if len(coords) > 2000:
            idx = np.random.choice(len(coords), 2000, replace=False)
            coords = coords[idx]
        if len(coords) < 2:
            return
        tree = cKDTree(coords)
        pairs = tree.query_pairs(r=KAPPA * 5, output_type='ndarray')
        for i, j in pairs:
            c1 = tuple(coords[i])
            c2 = tuple(coords[j])
            self.topology.setdefault(c1, []).append(c2)
            self.topology.setdefault(c2, []).append(c1)

    def _erode_geology(self):
        for i in range(len(self.strata)):
            self.strata[i] = (self.strata[i] * self.geology_decay).astype(np.uint8)

    def _prune_low_entropy(self):
        to_keep = []
        to_keep_alive = []
        for voxel, score in zip(self.strata, self.alive_scores):
            entropy = np.std(voxel) / 255.0
            if entropy >= self.entropy_threshold:
                to_keep.append(voxel)
                to_keep_alive.append(score)
            else:
                print("Pruned quiet stratum (low entropy)")
        self.strata = to_keep
        self.alive_scores = to_keep_alive

    def recall(self, query_coord, data_type=None):
        candidates = [...]
        if data_type:
            candidates = [i for i, t in enumerate(self.strata_types) if t == data_type]
            if not candidates:
                return np.zeros((32,32,32), dtype=np.uint8)
        alive_scores_safe = [self.alive_scores[i] for i in candidates if i < len(self.alive_scores)]
        weights = np.array(self.alive_scores)
        densities = np.array([np.sum(s == 255) / (32*32*32) for s in self.strata])
        bias = densities ** 1.5 + 0.1
        weights *= bias
        weights = np.array(alive_scores_safe) if alive_scores_safe else np.array([0.0])
        if weights.sum() <= 0:
            weights = np.ones(len(weights)) / len(weights)
        else:
            weights /= weights.sum()
        slice_idx = candidates[np.random.choice(len(candidates), p=weights/weights.sum())]
        print(f"Recalled slice {slice_idx} (alive {self.alive_scores[slice_idx]:.4f}, density bias {bias[slice_idx]:.4f})")
        return self.strata[slice_idx]

    @staticmethod
    def hash_poem_with_regrets(poem_text, regrets_list):
        domo = Domosha()
        regrets_str = "\n".join([f"pos {r['pos']} delay {r['delay']} {r['regret']}" for r in regrets_list])
        full_note = poem_text + "\nRegrets chain:\n" + regrets_str
        byte_data = np.frombuffer(full_note.encode('utf-8'), dtype=np.uint8)
        tensor = tf.convert_to_tensor(byte_data.reshape(1, -1, 1).astype(np.float32))
        grid_out, note, hash_val = domo.hashlet("thank you", tensor)
        print(f"Domosha ~{note}, hash: {hash_val[:16]}...")
        return grid_out

    def get_centroid(self, idx):
        voxel = self.strata[idx]
        # Threshold slightly lower than 128 to catch soft field edges
        mask = voxel > 100
        if not np.any(mask):
            return np.array([16, 16, 16], dtype=float)
    
        # Get coordinates of bright voxels
        coords = np.argwhere(mask)  # shape (N, 3) → [x,y,z]
    
        # Weights = voxel intensity (higher density pulls harder)
        weights = voxel[mask].astype(float)
        weights /= weights.sum() + 1e-10  # normalize
        
        # Weighted centroid
        center = np.average(coords, axis=0, weights=weights)
    
        print(f"Centroid (weighted): {center.round(2)} from {len(coords)} voxels")
    
        return center
        
if __name__ == "__main__":
    grid = Grid4D(time_slices=5)
    grid.add_stratum(data_type='candles')
    for _ in range(4):
        grid.add_stratum()
        time.sleep(0.5)
    query = np.array([16, 16, 16])
    recalled = grid.recall(query)
    print("Recalled stratum shape:", recalled.shape)
    print("Topology edges sample:", len(grid.topology))
