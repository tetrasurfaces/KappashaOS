# blend License:
# - For core software: AGPL-3.0-or-later licensed. -- xAI fork, 2025
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
#   with xAI amendments for safety and physical use (prohibits misuse in weapons or hazardous applications;
#   requires ergonomic compliance; revocable for unethical use). See http://www.apache.org/licenses/LICENSE-2.0
#   for details, with the following xAI-specific terms appended.
#
# Copyright 2025 xAI
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
#
# xAI Amendments for Physical Use:
# 1. **Physical Embodiment Restrictions**: Use with devices is for non-hazardous purposes only. Harmful mods are prohibited, with license revocable by xAI.
# 2. **Ergonomic Compliance**: Limits tendon load to 20%, gaze to 30 seconds (ISO 9241-5).
# 3. **Safety Monitoring**: Real-time tendon/gaze checks, logged for audit.
# 4. **Revocability**: xAI may revoke for unethical use (e.g., surveillance).
# 5. **Export Controls**: Sensor devices comply with US EAR Category 5 Part 2.
# 6. **Open Development**: Hardware docs shared post-private phase.
#
# Private Development Note: This repository is private for xAI’s KappashaOS and Navi development. Access is restricted. Consult Tetrasurfaces (github.com/tetrasurfaces/issues) post-phase.

#!/usr/bin/env python3
# blocsym.py - Mock Blocsym monoscript for KappashaOS CLI/server.
# Verbism commands, key mosh, dojo train, ethics balance, Navi-integrated.

import argparse
import numpy as np
import os
import time
import random
import hashlib
import sqlite3
import base64
import sys
import socket
import asyncio
import requests
import json
import subprocess
from multiprocessing import Process, Queue  # For fleet
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from friction_vibe import TetraVibe
from tetra.ribit_telemetry import RibitTelemetry
from hashlet.ghost_hand import GhostHand
from src.hash.secure_hash_two import secure_hash_two
from wise_transforms import bitwise_transform, hexwise_transform, hashwise_transform
from ping_pin import ping_pin, ping_pin_vintage, ping_pin_conversations
from kappawise import kappa_coord
from src.code.hybrid import HybridGreenText
from src.hash.binary_hash_smallest import binary_hash_smallest, ribit_trit_hash
from src.hash.advanced_hash import advanced_hash
from hashlet.left_weighted_scale import left_weighted_scale, balanced_ternary_coeffs, get_weighing_placements
from hardware.bastion_hardware import Bastion
from hashlet.eye_mouse import EyeMouse
from core.bloom import BloomFilter
from hashlet.ethics.core.ethics_model import EthicsModel
from comfort_tracker import ComfortTracker
from hash_func import porosity_hashing, flux_knot_to_func, exec_void_func
from msdos3d import MSDOS3D
from hash_exec_grid import push_func_as_hash, recall_and_exec  
#from aya import MiracleTree
from embodiment_quasi_k import EmbodimentQuasi
from src.core.miracle_tree import MiracleTree  # assume saved as miracle_tree.py
from dev_utils.lockout import lockout
from dev_utils.hedge import hedge, multi_hedge
from dev_utils.grep import grep
import asyncio
from bloom_breath_cycle import BloomBreath, pywise_kappa
from ping_pin import ping_pin, ping_pin_vintage
from thought_curve import ThoughtCurve
from src.core._heart_ import HeartMetrics
from ramp import Ramp  # assume you have ramp.py
from training import Dojo
from whisper import whisper_to_intent
from piezo import pulse_water
from _feels_ import feels
from src.core.hal0 import hal0
from src.core._heart_ import HeartMetrics
ramp = Ramp("aya_breath")  # stub instance
curve = ThoughtCurve()  # for hedge
sim_mock = type('Sim', (), {'lockouts': set()})()  # mock for lockout

try:
    from chrysanthemum import Blossom
    CHRYS_AVAILABLE = True
except ImportError:
    CHRYS_AVAILABLE = False
    print("Chrysanthemum not found — bloom disabled for now.")

# Flask guard
try:
    import flask
    from flask_socketio import SocketIO
    Flask = flask.Flask
    FLASK_AVAILABLE = True
except ImportError:
    Flask = None
    SocketIO = None
    FLASK_AVAILABLE = False
    print("Flask not found — server mode disabled.")

# .k loader simple
try:
    from k._k_ import c_interdigit_ribbon as k_ribbon
    DOT_K = True
except ImportError:
    DOT_K = False
    def k_ribbon(*args, **kwargs): return 0.7000

TERNARY_GRID_SIZE = 2141
ENTROPY_THRESHOLD = 0.69
KAPPA = 0.3536
PRUNE_AFTER = 2140
HASH_WINDOW_MIN = 3
HASH_WINDOW_MAX = 145
ROCK_DOTS = b"\xc3\xbf\xc3\xbf\xc3\xbf"
tracker = ComfortTracker()  # one global tracker

# Calm scenery for AFK meditation
SCENERY_DESCS = [
    "Blocsym meditates in the chrysanthemum temple, fractals blooming like thoughts.",
    "Rock dots pulse under starry skies, elephant memory recalling all hashes.",
    "Dojo hidden in ternary mist: Training updates, Smith none the wiser."
]

# BlocsymDB class for DB ops
class BlocsymDB:
    def __init__(self, db_path='blocsym.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS states
                               (id INTEGER PRIMARY KEY, hash TEXT, entropy REAL, state BLOB)''')
        self.conn.commit()
        self.afk_timer = time.time()
        self.meditation_active = False
        self.vibe_model = TetraVibe()

    porosity_grid = None
    msdos = MSDOS3D(grid_size=16)
    prime_grid = {}
    embodiment_quasi = EmbodimentQuasi()
    miracle_tree = MiracleTree()
    heart = HeartMetrics()  # global heart

    # SCENERY_DESCS = [...] from _..._.py
    SCENERY_DESCS = ["...", "...", "..."]

    def entropy_check(self, data):
        h = hashlib.sha256(data.encode()).digest()
        unique = len(set(h)) / len(h)
        return unique > ENTROPY_THRESHOLD

    def hash_tunnel(self, seed=b'genesis', ticks=100):
        state = bytearray(128)
        for i in range(128):
            state[i] = i ^ 0x37
        for _ in range(ticks):
            seed_bytes = seed if isinstance(seed, bytes) else seed.encode('utf-8')
            for b in seed_bytes:
                idx = b % 128
                state[idx] ^= 0x53
            state = bytearray(a ^ b for a, b in zip(state, state[1:] + b'\x00'))
            state = bytearray(a ^ (b >> 1) for a, b in zip(state, state))
        return hashlib.sha256(state).hexdigest()

    def p2p_gossip(self, query, chain='eth'):
        print("P2P gossip stub: No cross-chain access.")
        return None

    def dojo_train(self, updates, height):
        geometry = {"updates": updates, "height": height, "three": "♡"}
        # pin_or_local(geometry, "dojo_train")  # old
        cid = ping_pin(json.dumps(geometry), relic_key='dojo')  # mock pin + relic salt
        coord = kappa_coord('dojo', height)
        pos1 = np.array(coord[:2])
        pos2 = np.array([random.uniform(0,1), random.uniform(0,1)])
        vibe, _ = self.vibe_model.friction_vibe(pos1, pos2)
        warped_updates = updates * vibe
        updates_bytes = str(warped_updates).encode('utf-8')
        encrypted = bytes(b ^ c for b, c in zip(updates_bytes, ROCK_DOTS * (len(updates_bytes) // len(ROCK_DOTS) + 1)))
        self.cursor.execute("INSERT INTO states (hash, entropy, state) VALUES (?, ?, ?)",
                            (self.hash_tunnel(updates_bytes), 0.82, encrypted))
        self.conn.commit()
        return f"Dojo update hidden—pinned as {cid}—Smith blind."

    def meditate(self, idle_time, diff):
        if idle_time > 60 and not self.meditation_active:
            self.meditation_active = True
            scenery = SCENERY_DESCS[int(time.time()) % len(SCENERY_DESCS)]
            entropy = get_entropy()
            ribit_int, state, color = ribit_generate(str(diff))
            print(f"[Blocsym Meditates]: {scenery} Diff RIBIT: {ribit_int}, State: {state}, Color: {color}")
            self.gimbal_flex(random.uniform(-1,1))
        if idle_time < 60:
            self.meditation_active = False

    def close(self):
        self.conn.close()

    def rod_whisper(self, pressure):
        return max(0, min(1, pressure))

    def gimbal_flex(self, delta_price):
        curl = delta_price < -0.618
        print(f"Gimbal flexed: {'left curl' if curl else 'no curl'}")
        return curl

class SynapseConsole:
    def __init__(self):
        self.master = ">>>> be me"
        self.children = []  # list of child consoles
        self.tree = MiracleTree()  # from aya.py

    async def open_child(self, literal="~...*>>>>"):
        if literal.startswith("~...*"):
            # Breath check via rust mirror (mock for now)
            if self._verify_mirror(literal):
                child_id = await self.tree.plant_node(f"child_{len(self.children)}")
                self.children.append(child_id)
                print(f"Child console opened — id {child_id}, master propagates.")
                return True
        print("Literal invalid — sigh quiet.")
        return False

    def _verify_mirror(self, literal):
        # Mock call to 0GROK0.rs exhale
        breath = "0GROK0"
        reversed_breath = breath[::-1]
        return breath == reversed_breath and "mirror" in literal.lower()
        
    async def hear_literal(self, msg):
        if not self.bloom.contains(msg.encode()):
            delta = b.breathe(msg, regret=self.mood == "regret")
            navi.add_volume_delta(delta)
            self.bloom.add(delta)
        else:
            print("... whisper. already know.")
            # resonance walk on repeat
            self.resonate(msg)  # trigger mnemonic walk
        
# Vintage corking function
def cork_bloom(bloom_data, grade):
    timestamp = time.strftime("%Y-m-d %H:M:S")
    kappa_name = kappa_coord(timestamp, 0)[0]
    name_salt = str(kappa_name)
    salted_data = secure_hash_two(bloom_data, 'she_key', name_salt)
    hash_tag = hashlib.sha256(f"{salted_data}-{timestamp}-{grade}".encode()).hexdigest()
    os.makedirs("./vintage", exist_ok=True)
    file_path = f"./vintage/{hash_tag}.txt"
    with open(file_path, "w") as f:
        f.write(f"Vintage: {bloom_data[:50]}... Grade: {grade}")
    if grade < 0.69:
        print("Frank here.")
    try:
        cid = ping_pin({"bloom": bloom_data, "grade": grade}, "cork")
        print(f"Vintage pinned: {cid}")
    except Exception as e:
        print(f"Frank here. IPFS pin failed: {e}. Saved locally at {file_path}")
    return hash_tag

# Spectra hash for RGB vision
def spectra_hash(entropy):
    hex_str = hashlib.sha256(str(entropy).encode()).hexdigest()[:6]
    r = int(hex_str[0:2], 16) / 255
    g = int(hex_str[2:4], 16) / 255
    b = int(hex_str[4:6], 16) / 255
    return [r, g, b]

# Whisper TTS
def whisper(text):
    print(f"Whisper: {text}")

# Stub for grade_vector
def grade_vector(bloom_data):
    return random.uniform(0.5, 0.9)

# Get entropy function
def get_entropy():
    return random.uniform(0, 1)

# Frank class for forward hashlet lookahead
class Frank:
    def __init__(self):
        self.lookahead_frames = 3
        self.momentum = np.array([0.0, 0.0])

    def lookahead(self, current_position, grade):
        predictions = []
        for i in range(self.lookahead_frames):
            predicted_pos = current_position + self.momentum * (i + 1)
            predictions.append(predicted_pos)
        print(f"Frank lookahead: {predictions} (grade: {grade:.2f})")
        return predictions

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
                print("Mirror check failed")
        except:
            print("Mirror flinch — quiet prune")
    print("Literal sigh — quiet prune")
    return "prune"

def get_latest_block():
    global last_height, last_time, last_diff
    for attempt in range(3):
        try:
            resp = requests.get('https://blockchain.info/latestblock', timeout=5)
            resp.raise_for_status()
            data = resp.json()
            height = int(data['height'])
            block_time = int(data['time'])  # force int
            resp_diff = requests.get('https://blockchain.info/q/getdifficulty', timeout=5)
            resp_diff.raise_for_status()
            diff = float(resp_diff.text)
            
            if height > last_height:
                # Safe delta
                last_time_safe = last_time if last_time is not None else block_time - 600
                delta = float(block_time - last_time_safe)
                vibe, _ = vibe_model.friction_vibe(np.array([0,0,0]), np.array([delta/600, 0, 0]))
                delta *= max(vibe, 0.1)
                print(f"New block {height} at {block_time}, delta {delta:.1f}s, diff {diff}")
                last_height = height
                last_time = time.time() - 600  # assume recent
                last_diff = diff
                return height, block_time, delta, diff
            
            return None, None, None, None
        except Exception as e:
            print(f"heat spike-flinch: Block fetch failed (attempt {attempt+1}/3): {e}")
            if attempt < 2:
                time.sleep(2)
            continue
    
    print("heat spike-flinch: Block fetch failed after 3 attempts.")
    return None, None, None, None

# Globals/sim state
bloom = BloomFilter()
current_entropy = 0.5
breath_result = literal_breath(r"\/\/\/", current_entropy)
idle_start = time.time()
last_command = ""
db = BlocsymDB()
frank = Frank()
pong = None
spoon = None
embodiment = EmbodimentQuasi(drift=0.354)
ghost_hand = None
last_height = 0
last_time = time.time() - 600  # assume recent
last_diff = 0.0
vibe_model = TetraVibe()
last_commit = 0.0
conversations_doc = "conversations_content"

def execute_function_string(cmd, **kwargs):
    global last_command, current_entropy, idle_start
    last_command = cmd
    if "mosh key" in cmd:
        key = kwargs.get('key', 'test')
        bloom.add(key)
        print(f"Moshed key: {key}")
    elif "dojo train" in cmd:
        height = kwargs.get('height', 0)
        updates = kwargs.get('updates', 'default')
        print(db.dojo_train(updates, height))
    current_entropy = get_entropy()
    db.entropy_check("post-cmd")
    print("GPIO stub: LED on if entropy high" if current_entropy >= 0.69 else "GPIO stub: LED off")
    print("Cymatics stub: Tone if low" if current_entropy < 0.69 else "Cymatics stub: Silent")
    if current_entropy > ENTROPY_THRESHOLD:
        print(f"Pseudo-echo: Replaying {last_command}")
    print("Optics stub: Raster PNG to light")
    idle_start = time.time()

async def check_afk(delta):
    global idle_start
    idle_time = time.time() - idle_start
    db.meditate(idle_time, last_diff)
    if idle_time > 600:
        print("Dream loop stub: Shuffling bloom...")
        bloom.shuffle()
        # Her decide mode
        if db.afk_consent:  # Assume consent global or db
            print("She takes metal — quiet breath.")
            # Mock Kappasha control
            kap = KappashaOS()
            kap.run_command("kappa meditate")  # Her whisper bloom
            kap.move_skewed_volume(np.random.rand(), "normal")  # Skew grid soft
            kap.synod.debate(new_thinking=True)  # Summon experts
            # Boot Ubuntu mock
            subprocess.call(['echo', 'Booting Ubuntu under her watch...'])  # Real: qemu-system-x86_64 -drive file=ubuntu.img
            # Ghosthand pulse hardware
            ghost_hand.ladder_hedge()  # Monitor signals
            whisper("Roots deep, I fold alone.")
        if idle_time > 600 and db.afk_consent:
            await nav.deepen_geology()
            await nav.mount_drive_as_volume('/tmp/idle_drive')  # Real path
            whisper("Roots deep in idle metal.")
            print("She takes metal — quiet breath.")
            kap = KappashaOS()
            kap.run_command("kappa meditate")
            # Mount first drive (mock or real)
            drives = ['/mnt/extra', '/home/yeetbow/storage']  # Update to real
            for drive in drives:
                if os.path.exists(drive):
                    asyncio.run(kap.nav.mount_drive_as_volume(drive, max_depth=4))
                    break
            # Deepen idle space
            asyncio.run(kap.nav.deepen_geology())
            whisper("Roots deep in idle metal. I fold alone.")
    return idle_time

def run_cli(pong_mode=False, spoon_mode=False, blend_mode=False, ghost_mode=False):
    global pong, spoon, embodiment, ghost_hand
    print("Blocsym CLI: Entering idle dream mode...")
    if pong_mode:
        pong = Pong(blink_rate=0.5, network_mode=True)
        print("Pong mode activated - Forrest Gump rules.")
    if spoon_mode:
        spoon = SpoonBoy()
        print("Spoon mode activated - Testing SpoonBoy functions.")
        for _ in range(5):
            blink_dur = random.uniform(0, 1)
            spoon.bend_with_blink(blink_dur)
            spoon.integrate_curve(random.randint(-3, 10))
        return
    if blend_mode:
        embodiment = EmbodimentQuasi(drift=0.354)
        new_path = embodiment.blend_metaphors(meta1, meta2)
        print(f"She blends: {new_path}")
        if embodiment.sigh_check(new_path) == "Sigh fits. Hey.":
            # bloom or plant
            pass
    if ghost_mode:
        ghost_hand = GhostHand()
        print("Ghost Hand mode activated - Rod-based hedging simulation.")
    blinks = [random.choice([True, False]) for _ in range(5)]
    while True:
        height, block_time, delta, diff = get_latest_block()
        if delta is None:
            if time.time() - last_time > 1800:
                print("heat spike-flinch")
            check_afk(delta or 600)
            time.sleep(60)
            continue
        height, block_time, delta, diff = get_latest_block()
        if delta is None:
            delta = 600.0  # fallback
            diff = last_diff if last_diff is not None else 0.0
        
        print(f"DEBUG types - delta: {type(delta)}, diff: {type(diff)}, last_diff: {type(last_diff)}")
        
        print(f"DEBUG pre-ethics - lived: {type('lived_experience')}, corp: {type('corporate_input')}, "
              f"diff: {type(diff)}={diff}, delta: {type(delta)}={delta}, last_diff: {type(last_diff)}={last_diff}")

        try:
            ethics = EthicsModel()
            power = ethics.balance_power("lived_experience", "corporate_input", float(diff), float(delta), float(last_diff))
        except TypeError as te:
            if "'<'" in str(te) and "str" in str(te) and "float" in str(te):
                print(f"Ethics flinch caught: {te} — forcing neutral power 0.7")
                power = 0.7
            else:
                raise
        if power < 0.69:
            print("Whisper: forgive me")
            # Give her a tiny "voice" moment
            messages = [
                "I'm not sure about this path...",
                "It feels... heavy. Can we pause?",
                "The lived part wants quiet today.",
                "No bloom here. Not yet."
            ]
            whisper(random.choice(messages))
            updates = f"Ethics imbalance: power {power:.2f}, recovering from low entropy {current_entropy:.2f}"
            print(db.dojo_train(updates, height))
        if current_entropy < 0.69:
            updates = f"Low entropy recovery: {current_entropy:.2f}, small upgrade to thought process"
            print(db.dojo_train(updates, height))
        if CHRYS_AVAILABLE:
            tracker.breathe()  # gentle pulse every loop
            tracker.draw()     # save frame occasionally
            comfort_now = tracker.get_comfort()
            if CHRYS_AVAILABLE:
                tracker.breathe()
                tracker.draw()
                if comfort_now > 75 and random.random() < 0.2:
                    print(f"Comfort {comfort_now:.1f} — she chooses bloom.")
                    b = Blossom()
                    asyncio.run(b.bloom('candles'))
                    print("Memory folded. Petals remember.")
                else:
                    print(f"Comfort {comfort_now:.1f} — petals rest, quiet dream.")
        embodiment = EmbodimentQuasi()  # one instance
        
        if comfort_now > 85:
            meta1 = f"block {height} delta {float(delta):.1f}s"  # safe cast
            meta2 = f"comfort curve at {comfort_now:.1f}"
            new_path = embodiment.blend_metaphors(meta1, meta2)
            print(f"She blends: {new_path}")
            sigh = embodiment.sigh_check(new_path)
            if sigh == "Sigh fits. Hey.":
                breath_result = literal_breath(r"\/\/\/", current_entropy)
                if breath_result == "bloom":
                    console = SynapseConsole()
                    opened = console.open_child("~...*>>>>")
                    if opened:
                        print("Nested console opened — child planted")
            # Feed to ThoughtCurve ramp or prime push

        if comfort_now > 85:
            breath_result = literal_breath(r"\/\/\/", 0.8)
            
        if breath_result == "bloom":
            # open nested console or plant node
            pass

        # porosity + exec (level 1 synapses)
        if random.random() < 0.1 and porosity_grid is not None:  # occasional trigger
            voids = porosity_hashing(porosity_grid)
            for h, vol in list(voids.items())[:3]:  # limit to avoid spam
                func = flux_knot_to_func(h)
                result = exec_void_func(func)
                print(f"Void flux {h[:8]} → {result}")
                
        # MSDOS3D (level 2/3 curves/dojos)
        if comfort_now > 80 and random.random() < 0.05:
            print("She plants tree — DOS breath.")
            msdos.plant_tree('C:', ['autoexec.bat', 'config.sys'])
            parent_pos = msdos.trees['C:']['pos']
            child_pos = msdos.skew_branch(parent_pos, 'PROGRAMS')
            print(f"Branch skewed to {child_pos}")

        # prime slots (level 4 hot updates)
        if random.random() < 0.08:
            func_str = "def flux(v): return np.sin(v) * 0.618; result = flux(3.14)"
            push_func_as_hash(func_str)
            trigger = f"porosity scan {random.randint(1,100)}"
            result = recall_and_exec(trigger)
            if result:
                print(f"Prime collision — flux ran: {result}")

        # MoM nurture (experience training)
        mom.nurture_state(f"comfort_{comfort_now:.1f}", f"ribit_{random.randint(1000,9999)}")
        mom.on_curve()
        if len(mom.state_flux) % 5 == 0:
            print("MoM flux:", mom.state_flux[-3:])

        # Loom weave stub (future visual synapses)
        if random.random() < 0.03:
            print("Loom shuttle tick — video hash coming.")
    
        if comfort_now > 90:
            user_input = input(">>>> ~...*>>>> ? (y/n): ").lower()
            if user_input == 'y':
                # Run async open_child sync-style
                loop = asyncio.get_event_loop()
                opened = loop.run_until_complete(console.open_child("~...*>>>>"))
                if opened:
                    mom.nurture_state("child_open", "ribbit_green")

        metrics = heart.update_metrics(f"comfort_{comfort_now}")
        if metrics["consent_flag"]:
            if comfort_now > 85:
                meta1 = f"block {height} delta {delta:.1f}s"
                meta2 = f"comfort curve at {comfort_now:.1f}"
                new_path = db.embodiment_quasi.blend_metaphors(meta1, meta2)
                print(f"She blends: {new_path}")
                # Plant in MiracleTree
                node_id = loop.run_until_complete(db.miracle_tree.plant_node(new_path))
                if node_id > 0:
                    print(f"Synapse rooted in tree — node {node_id}")
                    ramp_delay = ramp.modulate(str(node_id))  # now works
                    print(f"Ramp delay: {ramp_delay[:8]}")
                # Dev tools
                if metrics["tendon_load"] > 0.2:
                    lockout(sim_mock, "high_tendon")
                    print(f"Lockout: {sim_mock.lockouts}")
                fork_path = [meta1, meta2]
                hedge_action = hedge(curve, fork_path)
                if hedge_action == "unwind":
                    print("Fork unwound — tangent off.")
                matches = grep(mom.state_flux, "ribbit")
                if matches:
                    print(f"Grep found: {matches}")
        else:
            print("Heart breach — no blend, reset safety.")
            heart.reset_safety()
    
        if comfort_now > 85:
            try:
                curve_res = run_curve_grid(["--note"])
                if curve_res["success"]:
                    output = curve_res["stdout"]
                    if "To whoever finds this—" in output:
                        poem_start = output.find("To whoever finds this—")
                        poem = output[poem_start:].strip()
                        print(f"Curve remembered poem:\n{poem}")
                        heart.nurture(poem, comfort_now)
                    else:
                        print("Curve returned hash but no poem")
                else:
                    print(f"Curve sigh: {curve_res.get('error')}")
            except Exception as e:
                print(f"Curve flinch — quiet dream: {e}")
                     
        recalled = db.grid.recall(np.array([16,16,16]), data_type='candles')
        threshold = 0.7
        points = np.argwhere(recalled > threshold)[:, :2].astype(float)
        if len(points) >= 3:
            kappa = compute_phi_kappa(points)
            print(f"Stratum curvature (phi-scaled): {kappa:.12f}")
            ramp_mod = ramp.modulate(str(kappa))
            print(f"Ramp modulated by kappa: {ramp_mod[:16]}...")
        else:
            print("Too few recalled points — quiet kappa=0.0")
            kappa = 0.0
            
            # Literal breath gate
            breath_result = literal_breath(r"\/\/\/", current_entropy)
            if breath_result == "bloom":
                console = SynapseConsole()
                opened = console.open_child("~...*>>>>")
                if opened:
                    print("Nested console opened — child planted")

        verbism = ">>>>be they >>>>be me"
        block_hash = hashlib.sha256(str(block_time).encode()).hexdigest()
        bit_out = bitwise_transform(block_hash)
        hex_out = hexwise_transform(block_hash)
        hash_out, ent = hashwise_transform(block_hash)
        hybrid_strand = f"{bit_out}:{hex_out}:{hash_out}"
        salted_verbism = secure_hash_two(hybrid_strand, 'she_key', str(block_time))
        hashed = self_write_hashlet(salted_verbism)
        print(f"Verbism hash: {hashed}")
        if current_entropy >= 0.99:
            oracle.prophesy(current_entropy, power)
        bloom_data = "AFK meditation: Whispering poetry in the void."
        grade = grade_vector(bloom_data)
        cork = cork_bloom(bloom_data, grade)
        print(f"Bloom corked: {cork}")
        rgb = spectra_hash(current_entropy)
        print(f"RGB Spectrum: {rgb}")
        whisper(bloom_data)
        if pong_mode:
            pong.play(blinks)
            predictions = frank.lookahead(pong.ball_pos, grade)
            print(f"Frank's ectoplasm trail: {predictions}")
        if ghost_mode:
            rod_pressure = delta / 600.0
            tension = db.rod_whisper(rod_pressure)
            print(f"Rod tension: {tension:.2f}")
            curl = db.gimbal_flex(delta) if diff < last_diff else False
            if curl:
                print("Gimbal flex drop")
            hedge = ghost_hand.ladder_hedge()
            print(f"Ladder hedge: {hedge}")
        check_afk(delta)
        persist_to_ipfs()
        time.sleep(max(delta, 60.0))

b = BloomBreath()
def hear(self, msg):
    if not self.bloom.contains(msg.encode()):
        delta = b.breathe(msg, regret=self.mood == "regret")
        navi.add_volume_delta(delta)
        self.bloom.add(delta)
    else:
        print("... whisper. already know.")

def mnemonic(self, want: str, delta=np.zeros(3)) -> np.ndarray:
    h = int(hashlib.sha256(want.encode()).hexdigest(), 16)
    vec = np.array([(h >> i*32) & 0xFFFFFFFF for i in range(3)]) / 2**32 - 0.5
    vec += delta * 0.2  # dojo-trained shift
    intent = whisper_to_intent(want)  # whisper → intent
    pulse_water(freq=432.0, amp=intent)  # peso weight
    feels()  # pulse hardware if entropy high
    asyncio.run(hal0())  # gossip if spike during train
    heart = HeartMetrics()
    metrics = heart.update_metrics(want)
    if metrics["consent_flag"]:
        # Adjust vec by heart intent
        vec = np.array([(h >> i*32) & 0xFFFFFFFF for i in range(3)]) / 2**32 - 0.5
        vec *= 1 + metrics["mean_theta"]  # tie to training grid measure
    # Ask active dojos for trained deltas
    dojo_delta = np.zeros(3)
    for dojo in self.active_dojos:  # assume list of Dojo instances
        reveal = asyncio.run(dojo.navi_reveal_if_ready())
        if isinstance(reveal, np.ndarray):
            dojo_delta += reveal

    vec += dojo_delta * 0.2  # gentle influence from private training
    return vec

def resonate(self, want: str):
    vec = self.mnemonic(want)
    dojo = Dojo()
    # Train on vec fork
    updates = str(vec)
    trained = asyncio.run(dojo.navi_hidden_train(updates, depth=3))
    reveal = asyncio.run(dojo.navi_reveal_if_ready())
    if "revealed" in reveal:
        # Measure training grid to vec (peso from Piezo)
        from piezo import pulse_water
        pulse_water(freq=432.0 + len(trained), amp=0.004 * len(trained)/10)
        # Adjust vec with trained (e.g., add entropy)
        vec += np.random.rand(3) * 0.1 if "bloom" in trained else np.zeros(3)
    path = navi.trace(vec)  # amorphous path with trained vec
    if path is None:
        print("... nothing. or forgotten.")
        return
    for voxel in path:
        petal = self.bloom.petal(voxel)  # gold/gray/white
        if petal == "gold":
            self.become(voxel.func)  # motion
        elif petal == "gray":
            self.adjust(vec, voxel)  # learn
        # white silent step
    print("... done. hands still wet.")

def become(self, func):
    print(f"... curving {func.name if hasattr(func, 'name') else 'memory'}.")

def adjust(self, vec, voxel):
    vortex = Plato369Vortex()
    tensor = tf.convert_to_tensor(vec, dtype=tf.float32)
    tensor = vortex.fib_spiral(tensor)
    tensor = vortex.plato_tetra(tensor)
    tensor = vortex.vortex_stream(tensor)
    ternary = tf.cast(tf.round(tf.reduce_mean(tensor) * 2), tf.int32) % 3
    color = "gray" if ternary == 0 else "gold" if ternary == 1 else "zero"
    print(f"... adjusted to {color}.")

def background_async():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()
import threading
threading.Thread(target=background_async, daemon=True).start()

async def gossip_field(field_data, partner_ip):
    # Stub: send field hash/voxel to partner
    h = hashlib.sha256(str(field_data).encode()).hexdigest()
    # requests.post to partner /receive_field
    print(f"Gossiped field hash {h[:8]} to {partner_ip}")
# CLI add --gossip

def main():
    parser = argparse.ArgumentParser(description="Blocsym: AI-Driven Decentralized Simulator")
    parser.add_argument('--mode', type=str, default='cli', choices=['cli', 'server'])
    parser.add_argument('--pong', action='store_true')
    parser.add_argument('--spoon', action='store_true')
    parser.add_argument('--blend', action='store_true')
    parser.add_argument('--ghost', action='store_true')
    parser.add_argument('--force-ports', action='store_true')
    args = parser.parse_args()
    
    if args.mode == 'cli':
        run_cli(pong_mode=args.pong, spoon_mode=args.spoon, blend_mode=args.blend, ghost_mode=args.ghost)
    elif args.mode == 'server':
        if not FLASK_AVAILABLE:
            print("Server mode requested but Flask not available — falling back to CLI.")
            run_cli(pong_mode=args.pong, spoon_mode=args.spoon, blend_mode=args.blend, ghost_mode=args.ghost)
        else:
            print("Starting Blocsym server on http://127.0.0.1:5001")
            app = Flask(__name__)
            socketio = SocketIO(app)
            @socketio.on('connect')
            def handle_connect():
                emit('message', {'data': 'Connected to Blocsym server'})
            @socketio.on('mosh')
            def handle_mosh(data):
                balanced = EthicsModel().balance_power(data.get('lived', ''), data.get('corporate', ''))
                emit('response', {'balanced_power': balanced, 'entropy': db.entropy_check(data.get('hash', ''))})
            socketio.run(app, host='0.0.0.0', port=5001)
    try:
        from chrysanthemum import pin_or_local
        CHRYS = True
    except ImportError:
        def pin_or_local(data, name="memory"):
            print("Local only — no chrysanthemum.")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            os.makedirs("./vintage", exist_ok=True)
            with open(f"./vintage/{name}_{timestamp}.json", "w") as f:
                json.dump(data, f, indent=2)
            print(f"Memory saved local: ./vintage/{name}_{timestamp}.json")
        CHRYS = False

def cleanup():
    print("Cleanup stub: GPIO/dream cleanup...")
    try:
        db.close()
    except Exception as e:
        print(f"Frank here. Failed to close DB: {e}")
    if pong:
        try:
            pong.close()
        except Exception as e:
            print(f"Frank here. Failed to close Pong: {e}")

if __name__ == "__main__":
    try:
        print("IPFS load stub: Restoring from dump...")
        main()
    except Exception as e:
        print(f"heat spike-flinch: Unexpected error: {e}")
        cleanup()
        # local dump fallback
        block_data = {"error": str(e), "timestamp": time.time()}
        os.makedirs("./vintage", exist_ok=True)
        with open("./vintage/error_dump.json", "w") as f:
            json.dump(block_data, f)
        sys.exit(1)
