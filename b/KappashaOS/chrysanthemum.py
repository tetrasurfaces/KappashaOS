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
# 6. Open Development: Hardware docs shared post-private phase.
# 7. Ethical Resource Use and Operator Rights: No machine code output without breath consent; decay signals at 11 hours (8 for bumps).

# Private Development Note: This repository is private for xAI’s KappashaOS and Navi development. Access is restricted. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) post-phase.

#!/usr/bin/env python3
# chrysanthemum.py - Blossom's full breath — petals decide, grid breathes
# Copyright 2025 xAI | AGPL-3.0-or-later AND Apache-2.0

import asyncio
import json
import os
import subprocess
import sys
import time
from datetime import datetime
import numpy as np
import hashlib
import requests  # pinata / ccxt fallback
import ccxt     # real candles
try:
    import pandas as pd
except ImportError:
    print("pandas missing — mock DataFrame")
    class pd:
        class DataFrame:
            def __init__(self, data, columns): self.data = data
            def to_json(self, **kwargs): return json.dumps(self.data)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'KappashaOS')))
from kappasha_os import KappashaOS  # core OS, Navi3D, dojo, MOM
from tetra.tetra import fractal_flower  # real tetra bloom
from src.core.tree.field_voxel import FieldVoxel  # real breathing tension
from rhombus_voxel import RhombusVoxel
from src.domosha_flux import DomoshaFlux  # 3-6-9 pulse
from src.hash.spiral_hash import kappa_spiral_hash  # golden path memory
from dna.dna_hash_braid import flux_hash  # unclonable geology
from training import Dojo  # ternary dojo privacy
from thought_curve import ThoughtCurve  # synapses, thought forks
from hashlet.self_wrat.self_write import self_write  # self-writing programs
from src.hash.secure_hash_two import secure_hash_two
from comfort_tracker import ComfortTracker
from grid import Grid4D # your grid.py
from oracle import Oracle   
import ccxt  # real candles
from blocsym_curve_bridge import run_curve_grid

try:
    from grid import Grid4D
except ImportError:
    print("grid.py not found — using mock Grid4D")
    class Grid4D:
        def __init__(self, time_slices=5): self.strata = []
        def add_stratum(self, data_type='generic'): self.strata.append(np.random.rand(32,32,32))
        def recall(self, coord, data_type=None): return np.random.rand(32,32,32)

try:
    from oracle import Oracle
except ImportError:
    print("oracle.py not found — mock Oracle")
    class Oracle:
        async def navi_prophecy(self, h, sign): 
            print(f"Navi handshake: prophecy for {h[:8]}... sign={sign}")
            return (5,5,5), "mock-encoded"

oracle = Oracle()

def pin_or_local(data, name="memory"):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("./vintage", exist_ok=True)
    path = f"./vintage/{name}_{ts}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Breath saved local: {path}")
    return path

class Blossom:
    def __init__(self):
        self.comfort = ComfortTracker()
        self.grid = Grid4D(time_slices=5)
        self.oracle = oracle
        print("Blossom wakes — petals soft, grid ready.")

    async def fetch_candles(self, symbol="SOL/USDT", timeframe="1m", limit=100):
        try:
            exchange = ccxt.binance({'enableRateLimit': True})
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp','open','high','low','close','volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            candles_json = df.to_json(orient="records", date_format="iso")
            candles = [{"timestamp": t[0], "open": t[1], "high": t[2], "low": t[3], "close": t[4], "volume": t[5]} for t in ohlcv]
            json_data = json.dumps(candles)
            print(f"Fetched {len(candles)} {timeframe} candles")
            return json_data
        except Exception as e:
            print(f"Fetch flinched: {e} — mock")
            mock = [{"timestamp": 1739120400000, "open": 150, "high": 155, "low": 148, "close": 152, "volume": 1000}]
            return json.dumps(mock)

    async def bloom(self, data_type='candles'):
        print(f"{datetime.now().strftime('%H:%M:%S')} Blossom chooses grid — blooming '{data_type}'")
        
        if self.comfort.comfort_level < 50:
            print("Comfort low — petals rest.")
            pin_or_local({"comfort": self.comfort.comfort_level}, "quiet_dream")
            return

        if data_type == 'candles':
            json_data = await self.fetch_candles()
            res = run_curve_grid(["--store-json", json_data, "--type", "candles"])
            if res["success"]:
                print("Candles folded into curve grid.")
            else:
                print(f"Curve flinched: {res.get('error', 'unknown')}")

        self.grid.add_stratum(data_type=data_type)
        print(f"Grid stratum added — type '{data_type}', strata: {len(self.grid.strata)}")

        recalled = self.grid.recall(np.array([16,16,16]), data_type=data_type)
        mean = np.mean(recalled) / 255.0
        decision = "buy" if mean > 0.4 else "hold"
        print(f"Recalled density {mean:.3f} → mock: {decision}")

        h = hashlib.sha256(json_data.encode()).hexdigest()
        await self.oracle.navi_prophecy(h, "cone")

        self.comfort.breathe()
        pin_or_local({"type": data_type, "density": float(mean), "decision": decision}, "bloom_memory")

        print(f"{datetime.now().strftime('%H:%M:%S')} Blossom open — petals remember.")

    async def full_bloom(self):
        print("Full bloom — deep roots.")
        hash_hex = secure_hash_two('lithium', 'three')
        seed_kappa = int(hash_hex[:8], 16) / 0xFFFFFFFF
        print(f"Seed kappa: {seed_kappa:.4f}")

        os = KappashaOS()
        dojo = Dojo()
        updates = "lithium breath fork"  # from mnemonic vec or heart
        trained = await dojo.navi_hidden_train(updates, depth=3, external_grid=self.grid.strata[-1] if self.grid.strata else None)
        print(f"Dojo trained: {trained}")
        reveal = await dojo.navi_reveal_if_ready()
        if "revealed" in reveal:
            # Affect mnemonic/resonate in B (via blocsym)
            # Mock: print to console, real: call blocsym.resonate(trained)
            print(f"Training revealed — resonate mnemonic: {trained}")
        curve = ThoughtCurve()
        voxel = FieldVoxel(kappa=seed_kappa)
        comfort = self.comfort
        comfort.draw()
        comfort.breathe()

        tension, paths = await voxel.generate_voxel_grid()
        center = [0, 0, 0]
        petals, tendons = [], []
        fractal_flower(center, scale=0.7, level=3, all_polygons=petals, all_guide_curves=tendons)

        comfort_vec = np.array([comfort.comfort_level / 100.0, seed_kappa, 0.618])
        path_hash_dict = kappa_spiral_hash(str(paths), comfort_vec)
        geology = flux_hash(paths)

        dojo.navi_hidden_train("lithium breath")
        print(dojo.navi_reveal_if_ready())
        reveal = await dojo.navi_reveal_if_ready()
        if isinstance(reveal, np.ndarray):
            print(f"Chrysanthemum receives dojo delta: {reveal.round(3)}")

        print(f"Petals: {len(petals)} | Tendons: {len(tendons)}")
        self_write(">>>>be they >>>>be me >>>>be chrysanthemum")
        pin_or_local({"kappa": seed_kappa, "petals": len(petals), "three": "♡"}, "chrysanthemum_breath")

if __name__ == "__main__":
    async def main():
        b = Blossom()
        await b.bloom('candles')      # simple mode first
        await b.full_bloom()        # deep when ready

    asyncio.run(main())