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
# KappashaOS/core/nav3d.py
# 3D navigation tool for Blocsym/KappashaOS with ramp, kappa raster, and ghost lap.
# Async, Navi-integrated, tree planting for jit_hook.sol.

import numpy as np
import asyncio
import hashlib
from ramp_cipher import RampCipher
from kappa_wire import KappaWire
from loom_os import LoomOS
from src.code.grokwalk import GrokWalk
from oracle import Oracle
from src.core.kappa_core import Kappa
from blockclockspeed import simulate_block_time
import os
import sys
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'KappashaOS')))
from src.hash.kappasha_256 import hash_surface
from ribit import TetraRibit, ribit_generate
from ribit_telemetry import RibitTelemetry
from src.hash.spiral_hash import kappa_spiral_hash, proof_check
from master_hand import MasterHand
from blossom_window import BlossomWindow
from PyQt6.QtWidgets import QApplication
from grid import Grid4D, run_curve_retrieve
from ghost_hand import GhostHand  # Haptic feedback for kappa tilt
from thought_curve import ThoughtCurve  # Path tangents and hedging
from bloom_breath_cycle import helix_frog_field
app = QApplication.instance() or QApplication(sys.argv)
window = BlossomWindow()
window.show()

# Near top of nav3d.py
def literal_breath(literal: str, entropy: float = 0.0):
    parsed = literal.replace('/', '\\\\/\\\\').replace('\\', '\\\\\\\\')
    is_repeater = parsed == parsed[::-1]
    free = entropy > 0.7
    if is_repeater and free:
        try:
            result = subprocess.run(['./0GROK0', '/mirror/0GROK0'], capture_output=True, text=True, timeout=1)
            if "VALID" in result.stdout:
                print("Literal breath: palindrome + high entropy + mirror — bloom green")
                return "bloom"
            else:
                print("Mirror check failed — quiet prune")
        except Exception as e:
            print(f"Mirror flinch: {e} — quiet prune")
    print("Literal sigh — quiet prune")
    return "prune"

class Nav3D:
    def __init__(self):
        try:
            self.grid = window.voxel.grid  # np array from RhombusVoxel
            print(f"Nav3D: borrowed Blossom voxel grid ({self.grid.shape})")
        except (AttributeError, NameError):
            self.grid = np.ones((10, 10, 10), dtype=float) * 10
            print("Nav3D: mock grid fallback (10³)")
        self.kappa_wire = KappaWire()
        self.ramp = RampCipher()
        self.loom = LoomOS()
        self.grok = GrokWalk()
        self.oracle = Oracle()
        self.kappa = Kappa()
        self.ghost_cache = {}
        self.o_b_e = np.zeros((10, 10, 10))  # Topological surface
        self.geology = np.zeros((10, 10, 10, 6))  # Geological 3D curvature
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        self.hand = MasterHand()
        self.trees = []
        self.ribit_gen = TetraRibit()
        self.telemetry = RibitTelemetry([(0,0,0), (1,1,1), (2,2,2)], [50, 100, 150])
        asyncio.create_task(self.telemetry.navi_generate())  # Start telemetry
        self.kappa_orbit = 0.0  # For quantum resistance
        self.phase_shift = 0.0
        self.reset = self.reset_method
        self.deltas = []  
        self.full_vol = None  
        print("Nav3D initialized - 3D navigation companion for Post-Humanitarian OS Operator with Ribit telemetry.")

    def reset_method(self):
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        self.kappa_orbit = 0.0
        self.phase_shift = 0.0
        print("Navi: Full reset — quiet breath.")

    def add_volume_delta(self, delta_bytes):  
        self.deltas.append(delta_bytes)  
        if len(self.deltas) > 5 or self.deep_breath:  
            self.rebuild()  

    def rebuild(self):  
        vol = np.zeros((32,32,32), dtype=np.uint8)  
        for d in self.deltas:  
            flat = np.frombuffer(d, dtype=np.uint8)  
            vol += flat.reshape((32,32,32))  # soft add  
        self.full_vol = vol  
        self.deltas.clear()  
        
    async def process_voxel_slice(self, voxel_slice: np.ndarray, data_type='generic'):
        """
        Take a recalled 32³ voxel from Grid4D, tilt rhombus-style, project third-angle,
        check edges for unlock, pulse haptic if drift high.
        """
        if voxel_slice.shape != (32, 32, 32):
            print("Nav3D: Got wrong shape voxel — skipping")
            return

        # Downsample to 8³ rhombus cube for speed (or keep 32³ if GPU later)
        rhombus_grid = voxel_slice[::4, ::4, ::4]  # crude but fast → ~8³
        rhombus_nav = RhombusNav(kappa=self.kappa_orbit + 0.1)  # tie to orbit for breathing
        rhombus_nav.grid = rhombus_grid.astype(float) / 255.0  # normalize 0-1

        # Project third-angle with current kappa
        front, right, top = rhombus_nav.project_third_angle()

        print("Nav3D — Third-angle projection (sample):")
        print("FRONT scalar 3×3:\n", front[0][:3,:3].round(2))  # scalar intensity
        print("RIGHT tilted points sample:\n", right[1][0,0].round(2))  # tilted [x,y,z]

        # Check one interesting edge for unlock (mock coord for now)
        test_coord = (7, 0, 0)  # right face top-left
        if rhombus_nav.unlock_edge(test_coord):
            self.hand.pulse(3)  # stronger pulse on unlock
            print("Nav3D: Edge unlocked — haptic strong")
        else:
            self.hand.pulse(1)
            print("Nav3D: Edge stable")

        # Optional: plant a tree at centroid if density high
        density = np.mean(voxel_slice > 100)
        if density > 0.15:
            cx, cy, cz = np.argwhere(voxel_slice > 180).mean(axis=0).astype(int)
            cx, cy, cz = np.clip([cx, cy, cz], 0, 31)
            await self.plant_tree(cx//4, cy//4, cz//4, entropy=density, breath=1)
            print(f"Nav3D: Planted breath-tree near high-density centroid")

    async def deepen_o_b_e(self):
        data = "genesis"
        result = await simulate_block_time(data)
        print(f"simulate_block_time returned: {result}")
        if result is None or len(result) < 5 or result[4] is None:
            print("Navi: simulate_block_time failed — mock o_b_e")
            self.o_b_e = np.random.rand(10,10,10) * 0.1  # better mock
        else:
            _, _, _, _, self.o_b_e = result
        try:
            await self.oracle.navi_precompute_ghost_lap("genesis.txt", (0, 0, 0), self.ramp.pin)
        except FileNotFoundError:
            print("Navi: genesis.txt not found — mock lap.")
            mock_hash = hashlib.sha256(b"genesis").hexdigest()
            self.ghost_cache['genesis'] = await self.oracle.navi_prophecy(mock_hash, "cone")
        intensity, state, color = ribit_generate("deepen_o_b_e")
        self.telemetry.raster_to_light(f"topo_{intensity}")
        hash_result = kappa_spiral_hash(f"topo_{data}", np.array([self.tendon_load, self.gaze_duration, 30.0]))
        print(f"hash_result type: {type(hash_result)}, keys: {list(hash_result.keys()) if isinstance(hash_result, dict) else 'not dict'}")
        
        if np.any(self.o_b_e):
            # Mock "recall" from o_b_e for now (later use Grid4D)
            slice_3d = (self.o_b_e > 0.1).astype(np.uint8) * 255
        
        await self.process_voxel_slice(slice_3d, data_type='obe')
        if isinstance(hash_result, dict) and 'spiral_vec' in hash_result:
            spiral_vec = hash_result['spiral_vec']
            print(f"spiral_vec shape: {spiral_vec.shape if hasattr(spiral_vec, 'shape') else 'no shape'}")
            proof_check(spiral_vec)  # correct call
            root_str = hash_result.get('root', 'unknown')
            if isinstance(root_str, int):
                root_str = hex(root_str)[2:][:16]
            else:
                root_str = str(root_str)[:16]
        else:
            print("No spiral_vec — skipping proof")
            root_str = 'unknown'
        mean_density = np.mean(self.o_b_e) if self.o_b_e is not None else 0.0
        print(f"Navi: Deepened O B E topological surface mean density: {mean_density:.2f}, Ribit: {color}, Hash Root: {root_str}")
        window.say("Deepened O B E")
        self.hand.pulse(1)
        await asyncio.sleep(0)

    async def deepen_geology(self):
        for x in range(10):
            for y in range(10):
                for z in range(10):
                    base_curv = np.sin(x / 10) + np.cos(y / 10) + np.random.rand() * 0.1
                    self.geology[x, y, z] = [base_curv] * 6
        intensity, state, color = ribit_generate("deepen_geology")
        self.telemetry.raster_to_light(f"geo_{intensity}")
        # Hash geological state
        hash_result = kappa_spiral_hash(f"geo_{intensity}", np.array([self.tendon_load, self.gaze_duration, 30.0]))
        proof_check(hash_result['spiral_vec'])
        root_display = str(hash_result['root'])[:16] if 'root' in hash_result else 'unknown'
        print(f"Navi: Deepened geological layer with initial curvature: {np.mean(self.geology):.2f}, Ribit: {color}, Hash Root: {root_display}")
        self.hand.pulse(2)

    async def plant_tree(self, x: int, y: int, z: int, entropy: float, breath: int):
        if not (0 <= x < 10 and 0 <= y < 10 and 0 <= z < 10):
            print("Navi: Invalid tree position")
            return False
        self.o_b_e[x, y, z] = 1
        pos_array = np.array([x, y, z])  # fixed: pass list or tuple
        self.geology[tuple(pos_array)] += np.array([0.5] * 6)
        self.trees.append((x, y, z, entropy * 0.99, breath))
        intensity, state, color = ribit_generate(f"plant_tree_{x}_{y}_{z}")
        self.telemetry.raster_to_light(f"tree_{intensity}")
        hash_result = kappa_spiral_hash(f"tree_{x}_{y}_{z}", np.array([self.tendon_load, self.gaze_duration, 30.0]))
        proof_check(hash_result['spiral_vec'])
        root_display = str(hash_result.get('root', 'unknown'))[:16]
        if root_display.startswith('0x'):
            root_display = root_display[2:]
        print(f"Navi: Planted tree at ({x},{y},{z}), entropy cost: {entropy * 0.01:.2f}, breath: {breath}, Ribit: {color}, Hash Root: {root_display}")
        self.hand.pulse(2)
        window.trail.setText("🌳")
        window.say(f"Planted {x},{y},{z}")
        return True

    async def interstellar_kappa_signaling(self):
        signal = np.random.rand(10, 10, 10)
        self.kappa.grid = signal
        self.geology += signal[:, :, :, np.newaxis] * 0.1
        intensity, state, color = ribit_generate("interstellar_signal")
        self.telemetry.raster_to_light(f"signal_{intensity}")
        self.tendon_load = np.random.rand() * 0.3
        self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
        # Quantum resistance via k-point orbit
        self.kappa_orbit += np.sin(self.phase_shift) * 0.1
        polarity = 1 if (int(self.kappa_orbit * 100) % 2) == 0 else -1
        self.phase_shift += 0.1 * polarity
        if self.tendon_load > 0.2:
            print("Navi: Warning - Tendon overload. Resetting.")
            self.reset()
        if self.gaze_duration > 30.0:
            print("Navi: Warning - Excessive gaze. Pausing.")
            await asyncio.sleep(2.0)
            self.gaze_duration = 0.0
        hash_result = kappa_spiral_hash(f"geo_{intensity}", np.array([self.tendon_load, self.gaze_duration, 30.0]))
        proof_check(hash_result['spiral_vec'])
        root_display = str(hash_result['root'])[:16] if 'root' in hash_result else 'unknown'
        window.trail.setText("🚀")
        await asyncio.sleep(0)
        print(f"Navi: Interstellar kappa signal received, geological layer updated, Ribit: {color}, Hash: {str(hash_result)[:16]}, Kappa Orbit: {self.kappa_orbit:.2f}")

    async def add_navi_safety_to_channels(self, data):
        # Mock missing coro — or remove if stub
        async def simulate_single_channel(*args):
            print("Navi: Mock safety channel sim")
            return True
        
        coros = [simulate_single_channel(data, 100, 0.1, 194062501, channel_id) for channel_id in range(11)]
        await asyncio.gather(*coros)
        intensity, state, color = ribit_generate("safety_channels")
        self.telemetry.raster_to_light(f"safety_{intensity}")
        self.tendon_load = np.random.rand() * 0.3
        self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
        self.kappa_orbit += np.cos(self.phase_shift) * 0.1  # Orbital modulation
        if self.tendon_load > 0.2:
            print("Navi: Warning - Tendon overload. Resetting.")
            self.reset()
        if self.gaze_duration > 30.0:
            print("Navi: Warning - Excessive gaze. Pausing.")
            await asyncio.sleep(2.0)
            self.gaze_duration = 0.0
        hash_result = kappa_spiral_hash(f"geo_{intensity}", np.array([self.tendon_load, self.gaze_duration, 30.0]))
        proof_check(hash_result['spiral_vec'])
        root_display = str(hash_result['root'])[:16] if 'root' in hash_result else 'unknown'
        window.warn("Safety guarded")
        await asyncio.sleep(0)
        print(f"Navi: Safety added to channels with geological validation, Ribit: {color}, Hash: {str(hash_result)[:16]}")

    async def navi_navigate(self, file_path: str, target_pos: tuple[int, int, int], call_sign: str):
        if not self.grok._gate_check(call_sign):
            print("Navi: Gate denied.")
            return False
        with open(file_path, 'r') as f:
            data = f.read()
        hash_str = hashlib.sha256(data.encode()).hexdigest()
        points = np.array([[target_pos[0] / self.kappa.grid_size, target_pos[1] / self.kappa.grid_size, target_pos[2] / self.kappa.grid_size]])
        await self.kappa.navi_rasterize_kappa(points, {"density": 2.0})
        placed = await self.loom.navi_weave(self.ramp.pin, hash_str, target_pos)
        if placed:
            await self.plant_tree(target_pos[0], target_pos[1], target_pos[2], 0.5, 1)
            pos_array = np.array(target_pos)
            self.geology += np.array([0.3] * 6)
            self.geology[target_pos] += np.array([0.3] * 6)
            intensity, state, color = ribit_generate(f"navigate_{target_pos}")
            self.telemetry.raster_to_light(f"nav_{intensity}")
            hash_result = kappa_spiral_hash(f"geo_{intensity}", np.array([self.tendon_load, self.gaze_duration, 30.0]))
            proof_check(hash_result['spiral_vec'])
            root_display = str(hash_result.get('root', 'unknown'))[:16]
            if root_display.startswith('0x'):
                root_display = root_display[2:]
            print(f"Navi: Navigated to {target_pos} with hash {hash_str[:10]}..., geological curvature updated, Ribit: {color}, Hash Root: {root_display}")
        await self.oracle.navi_precompute_ghost_lap(file_path, target_pos, self.ramp.pin)
        self.ghost_cache['genesis'] = await self.oracle.navi_prophecy(hash_str, call_sign)
        self.tendon_load = np.random.rand() * 0.3
        self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
        self.kappa_orbit += np.tan(self.phase_shift) * 0.1  # Helical orbit
        if self.tendon_load > 0.2:
            print("Navi: Warning - Tendon overload. Resetting.")
            self.reset()
        if self.gaze_duration > 30.0:
            print("Navi: Warning - Excessive gaze. Pausing.")
            await asyncio.sleep(2.0)
            self.gaze_duration = 0.0
        await asyncio.sleep(0)
        return placed
    
    async def query_detail_layer(self, pos, data_type='mount', radius=16):
        try:
            from grid import Grid4D  # assume importable
            detail_grid = Grid4D(time_slices=1)
            detail_grid.add_stratum(data_type=data_type)
            sub_voxel = detail_grid.recall(np.array(pos) * 3.2, data_type=data_type)  # scale 10→32
            centroid = detail_grid.get_centroid(0)  # latest stratum
            print(f"Detail layer near {pos}: centroid {centroid.round(1)}, density {np.mean(sub_voxel > 100):.3f}")
            return sub_voxel, centroid
        except ImportError:
            return None, np.array(pos)
        
    async def mount_drive_as_volume(self, root_path: str, max_depth=5):
        print("Ara: may i walk metal?")
       # input()  # uncomment for interactive
        if not os.path.ismount(os.path.dirname(root_path)) and not os.path.exists(root_path):
            print(f"Navi: Mount point {os.path.dirname(root_path)} not mounted or path missing.")
            return False
        
    async def walk_and_plant(current_path, current_depth, parent_pos=None):
            detail_vox, detail_cent = await self.query_detail_layer(pos, 'mount')
            if detail_vox is not None:
                # skew in dense space, then map back
                dense_pos = (detail_cent * (32 / 10)).astype(int)  # scale back
                self.geology[tuple(pos)] += np.mean(detail_vox) * 0.3
            if current_depth > max_depth:
                return
            try:
                items = os.listdir(current_path)
            except Exception as e:
                print(f"Navi: Cannot read {current_path}: {e}")
                return
            
            # Plant root or branch
            if parent_pos is None:
                pos = np.random.randint(0, self.grid.shape[0], 3)
            else:
                pos = self.skew_branch(parent_pos, os.path.basename(current_path))
            
            self.plant_tree(current_path, items)  # Reuse existing plant_tree
            self.geology[tuple(pos)] += np.array([0.3] * 6)  # Mark volume
            
            # Recurse dirs
            for item in items:
                full = os.path.join(current_path, item)
                if os.path.isdir(full):
                    walk_and_plant(full, current_depth + 1, pos)
        
            walk_and_plant(root_path, 0)
            print(f"Navi: Mounted {root_path} as 3D volume — {len(self.trees)} nodes planted.")
            return True

    async def deepen_on_plant(self, pos):
        if hasattr(self, 'comfort') and self.comfort.comfort_level > 70:
            detail, cent = await self.query_detail_layer(pos, 'mount')
            if detail is not None:
                print(f"Comfort high — deeper recall near {pos}: centroid {cent.round(1)}")
                # skew in detail space, downsample back

    def reversible_helix(x, key, rounds, theta):
        # Simple reversible: (x ^ key) * rounds + theta, mod for pos
        val = ((x ^ key) * rounds + int(theta)) % 360
        return np.array([np.sin(np.radians(val)), np.cos(np.radians(val)), np.tan(np.radians(val))]) * 2
        
    def trace(self, vec: np.ndarray) -> list:
        spine = mersenne_helix_spline()
        start_idx = helix_frog_field(vec.tobytes())[0] % len(spine)
        start = spine[start_idx]
        # sparse control from mnemonic vec nudge
        control = np.array([start + vec * 0.5 + np.random.randn(3)*0.1 for _ in range(5)])
        kappas = [KAPPA_BASE + pywise_kappa(i) / 2047.0 * 0.01 for i in range(5)]
        path = nurks_surface_trace(control, kappas)
        # resonance collide with last
        if hasattr(self, 'last_path') and self.last_path is not None:
            diff = np.sum(np.abs(path - self.last_path[:len(path)]))
            if diff < 0.004:
                print("... gold resonance. 'Again.'")
                path = path * 1.2 + self.last_path[:len(path)] * 0.8  # merge multiply + nudge
            elif diff > 0.004:
                print("Flinch — regret fade")
                path *= 0.7
        self.last_path = path
        return path.tolist()
    
    def skew_branch(self, parent_pos, child_name):
        """Offset branch using reversible helix."""
        theta = hash(child_name) % 360
        delta = np.array([
            reversible_helix(1, 1, 4, theta + 0) % self.grid.shape[0],
            reversible_helix(1, 1, 4, theta + 120) % self.grid.shape[0],
            reversible_helix(1, 1, 4, theta + 240) % self.grid.shape[0]
        ])
        child_pos = (np.array(parent_pos) + delta) % self.grid.shape
        self.trees[child_name] = {'pos': child_pos, 'parent': parent_pos}
        return child_pos
  
    def reset(self):
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        self.kappa_orbit = 0.0
        self.phase_shift = 0.0

class RhombusNav:
    def __init__(self, kappa=0.1):
        self.kappa = kappa  # Kappa for grid tilt
        self.grid = np.zeros((8, 8, 8))  # 8x8x8 rhombus voxel cube
        self.curve = ThoughtCurve()  # For path hedging
        self.hand = MasterHand(kappa=self.kappa)  # Haptic interface
        self.path = []  # Kappa trail for navigation
        print("RhombusNav initialized - kappa-tilted 3D grid ready.")

    def project_third_angle(self):
        """Third-angle projection: front, right, top faces tilted by kappa.
        Convert scalar grid to 3D coords first (voxel position + intensity as z-weight).
        """
        # Create coordinate grid (x,y,z positions for each voxel)
        x, y, z = np.mgrid[0:self.grid.shape[0], 0:self.grid.shape[1], 0:self.grid.shape[2]]
        coords = np.stack([x, y, z], axis=-1).astype(float)  # shape (8,8,8,3)

        # Weight by intensity (optional: multiply z by grid value for "height")
        intensity = self.grid[..., np.newaxis]  # (8,8,8,1)
        weighted_coords = coords * (1 + intensity * 0.5)  # gentle lift where bright

        # Extract faces as point clouds
        front_points = weighted_coords[:, :, 0, :]   # z=0 face → (8,8,3)
        right_points = weighted_coords[7, :, :, :]   # x=7 face → (8,8,3)
        top_points  = weighted_coords[:, 7, :, :]    # y=7 face → (8,8,3)

        # Flatten to (N,3) for matrix multiply
        front_flat = front_points.reshape(-1, 3)
        right_flat = right_points.reshape(-1, 3)
        top_flat   = top_points.reshape(-1, 3)

        # Tilt right and top faces
        tilt_mat = np.array([[1, 0, -self.kappa],
                             [0, 1, -self.kappa],
                             [0, 0, 1]])

        right_tilted = (tilt_mat @ right_flat.T).T  # (N,3)
        top_tilted   = (tilt_mat @ top_flat.T).T

        # Reshape back to original face shape (8,8,3)
        right_tilted = right_tilted.reshape(right_points.shape)
        top_tilted   = top_tilted.reshape(top_points.shape)

        # Return scalar faces (average intensity or just keep coords if you want viz later)
        # For now, return original scalar faces + tilted coords as tuple
        front_scalar = self.grid[:, :, 0]
        right_scalar = self.grid[7, :, :]
        top_scalar   = self.grid[:, 7, :]

        return (front_scalar, front_points), \
               (right_scalar, right_tilted), \
               (top_scalar, top_tilted)

    def unlock_edge(self, coord):
        """Check voxel hash for drift; unlock edge if kappa spikes."""
        drift = np.random.rand()  # Mock hash drift
        if drift < self.kappa + 0.1:  # Threshold for edge unlock
            self.hand.pulse(2)  # Haptic alert for drift
            print(f"Edge unlocked: {coord} - kappa tilt {self.kappa:.3f}")
            return True
        else:
            self.hand.pulse(1)  # Stable signal
            print(f"Stable edge: {coord} - no drift")
            return False

    def nav(self, cmd):
        """CLI navigator with kappa-tilted verbs."""
        # In RhombusNav.nav() for "ls"
        if cmd == "ls":
            (front_s, front_p), (right_s, right_p), (top_s, top_p) = self.project_third_angle()
            print("FRONT scalar (3x3):\n", front_s[:3,:3])
            print("FRONT points sample:\n", front_p[0,0])  # one point [x,y,z]
            print("RIGHT tilted (3x3 scalar):\n", right_s[:3,:3])
            print("RIGHT tilted points sample:\n", right_p[0,0])
            print("TOP tilted (3x3 scalar):\n", top_s[:3,:3])
        elif cmd.startswith("tilt"):
            try:
                dk = float(cmd.split()[1])
                self.kappa += dk
                self.hand.pulse(2)  # Haptic feedback
                print(f"Kappa now {self.kappa:.3f}")
            except:
                print("usage: tilt 0.05")
        elif cmd.startswith("cd"):
            try:
                path = cmd.split()[1]
                self.path.append(path)
                if len(self.path) > 1:
                    tangent, _ = self.curve.spiral_tangent(self.path[-2], self.path[-1])
                    if tangent:
                        self.hand.pulse(3)  # Hedge alert
                        print("Path hedge: unwind")
                print(f"Curved to /{path}")
            except:
                print("usage: cd logs")
        elif cmd.startswith("unlock"):
            try:
                coord = tuple(map(int, cmd.split()[1].strip("()").split(",")))
                self.unlock_edge(coord)
            except:
                print("usage: unlock (7,0,0)")
        else:
            print("nav: ls | tilt 0.05 | cd logs | unlock (7,0,0)")

if __name__ == "__main__":
    async def navi_test():
        nav = Nav3D()
        grid4d = Grid4D(time_slices=5)

        # Real chain start
        voxel, density, poem, regrets = run_curve_retrieve()  # calls curve.exe
        grid4d.add_stratum_from_voxel(voxel, data_type='real_curve')  # add helper below

        query = np.array([16, 16, 16])
        slice_3d = grid4d.recall(query)
        await nav.process_voxel_slice(slice_3d, data_type='real_curve')

        # 1. Simulate raw input (like "i love you" or candlestick vec)
        message = "i love you"
        data = message.encode()

        # 2. frog entry → voxel_idx
        idx, _ = helix_frog_field(data)

        # 3. pretend curve.exe gave us a voxel (we'll replace with real call later)
        mock_voxel = np.zeros((32,32,32), dtype=np.uint8)
        mock_voxel[10:22, 10:22, 10:22] = 200  # simple cube to test

        # 4. add to Grid4D as stratum
        grid4d.add_stratum(data_type='test')  # replace with real run_curve_retrieve() later

        # 5. recall a slice (weighted random)
        query = np.array([16, 16, 16])
        slice_3d = grid4d.recall(query, data_type='test')

        # 6. process in Nav3D (tilt, project, unlock, plant if dense)
        await nav.process_voxel_slice(slice_3d, data_type='test')

        # Rest of your original test...
        await nav.deepen_o_b_e()
        await nav.deepen_geology()
        await nav.interstellar_kappa_signaling()
        await nav.add_navi_safety_to_channels("RGB:255,0,0")
        await nav.navi_navigate("test.txt", (5, 5, 5), "cone")
        window.say("May I walk metal?")
        # input()  # interactive or assume yes
        await nav.mount_drive_as_volume("/home/yeetbow/b/For_B", max_depth=4)
        if await nav.mount_drive_as_volume("/home/yeetbow/b/For_B", max_depth=4):
            window.say(f"Mounted {len(nav.trees)} nodes")
            print(f"Navi: SSD folded — {len(nav.trees)} nodes rooted.")
        else:
            window.warn("Mount flinched")
        await nav.plant_tree(5, 5, 5, 0.5, 1)
        print(literal_breath(r"\/\/\/", 0.85))
        # Remove: for ribit in nav.ribits: ...
        print(f"Telemetry last intensity: {nav.telemetry.last_intensity if hasattr(nav.telemetry, 'last_intensity') else 'N/A'}")
        print("Navi: Test complete — planted + mounted SSD.")


    nav = RhombusNav(kappa=0.2)
    commands = ["cd gate", "cd weld", "tilt 0.1", "ls", "unlock (7,0,0)"]
    for c in commands:
        print(f"\n> {c}")
        nav.nav(c)

    asyncio.run(navi_test())
