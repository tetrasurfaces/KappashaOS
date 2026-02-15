#!/usr/bin/env python3
# blocsym.py - Blocsÿm Monoscript: Main CLI/Server for BlockChan Simulator
# Handles verbism commands, key moshing, dojo training, ethics balancing.
# Now integrates Blossom: AFK meditation/dreaming, entropy-based GPIO/cymatics/optics, pseudo-echo shifting, IPFS persistence.
# Integrates db_utils.py elements for cross-chain, entropy pipes, and calm states (dino_hash tunneling, comms_util P2P gossip).
# AGPL-3.0-or-later licensed. -- OliviaLynnArchive fork, 2025
# Inspired by opreturndinohash/dino_hash (hash tunneling) and commsutil/comms_util (P2P buffers).
# Copyright 2025 Coneing and Contributors
#
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
# For hardware/embodiment interfaces: Licensed under the Apache License, Version 2.0
# with xAI amendments for safety (prohibits misuse in hashing; revocable for unethical use).
# See http://www.apache.org/licenses/LICENSE-2.0 for details.

import argparse
import os
import time
import random
import hashlib
import sqlite3
import base64
import sys
import socket
import greenlet
import numpy as np
import subprocess
import requests
import sympy as sp
from sympy import symbols, solve, Eq, sin
import matplotlib.pyplot as plt
from friction_vibe import TetraVibe 
from mpl_toolkits.mplot3d import Axes3D
from io import BytesIO
from ribit import ribit_generate
from ghost_hand import GhostHand
from ping_pin import ping_pin, ping_pin_vintage, ping_pin_conversations
from secure_hash_two import secure_hash_two
from kappawise import kappa_coord
from wise_transforms import bitwise_transform, hexwise_transform, hashwise_transform
import json
try:
    from flask import Flask
    from flask_socketio import SocketIO, emit
except ImportError:
    print("Flask/SocketIO not available; server mode disabled.")
    Flask = None
    SocketIO = None

# Comment out web3 and solana imports to make it runnable without them
from web3 import Web3
from solana.rpc.api import Client as SolanaClient

# Check if a port is free on host
def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False

# Get process on a port using lsof
def get_port_process(port):
    try:
        result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        for line in lines[1:]:  # Skip header
            if 'LISTEN' in line:
                parts = line.split()
                return parts[1], parts[0]  # PID, COMMAND
        return None, None
    except FileNotFoundError:
        print("Frank here. 'lsof' not found—cannot identify process.")
        return None, None

# Check if a process is managed by systemd
def check_systemd_service(command):
    try:
        result = subprocess.run(['systemctl', 'status', command], capture_output=True, text=True)
        if 'active (running)' in result.stdout:
            print(f"Frank here. {command} is a systemd service.")
            return True
        return False
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        print("Frank here. 'systemctl' not found—cannot check systemd services.")
        return False

# Stop a systemd service
def stop_systemd_service(command):
    try:
        subprocess.run(['sudo', 'systemctl', 'stop', command], check=True)
        print(f"Frank here. Stopped systemd service {command}.")
        time.sleep(1)  # Wait for service to stop
        return True
    except subprocess.CalledProcessError as e:
        print(f"Frank here. Failed to stop systemd service {command}: {e}")
        return False

# Update IPFS config to use a new gateway port
def update_ipfs_config(new_port):
    config_path = os.path.expanduser("~/.ipfs/config")
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            current_port = config['Addresses']['Gateway'].split('/')[-1]
            if current_port == str(new_port):
                print(f"IPFS config already set to port {new_port}.")
                return True
        config['Addresses']['Gateway'] = f"/ip4/127.0.0.1/tcp/{new_port}"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Updated IPFS config: Gateway set to port {new_port}")
        return True
    except Exception as e:
        print(f"Frank here. Failed to update IPFS config: {e}")
        return False

# Kill process on a port
def kill_process_on_port(port, pid, command, force=False):
    # Only kill safe processes unless force=True
    safe_commands = ['ipfs', 'python', 'node']  # Add other safe processes as needed
    if not force and command not in safe_commands:
        print(f"Frank here. Skipping kill for {command} (PID {pid}) on port {port}—not a safe process.")
        return False
    try:
        if force:
            print(f"Frank here. Force-killing {command} (PID {pid}) on port {port}.")
            # Check if it's a systemd service
            if check_systemd_service(command):
                if stop_systemd_service(command):
                    if check_port('127.0.0.1', port):
                        return True
                    print(f"Frank here. Stopped {command} service, but port {port} still blocked.")
                else:
                    print(f"Frank here. Failed to stop {command} service.")
        # Retry kill up to 3 times
        for attempt in range(3):
            subprocess.run(['sudo', 'kill', '-9', pid], check=True)
            time.sleep(1)  # Wait for process to terminate
            if check_port('127.0.0.1', port):
                print(f"Killed {command} (PID {pid}) on port {port} after {attempt+1} attempts.")
                return True
            print(f"Frank here. Failed to kill {command} (PID {pid}) on port {port}, attempt {attempt+1}/3.")
        print(f"Frank here. Could not kill {command} (PID {pid}) on port {port} after 3 attempts.")
        return False
    except Exception as e:
        print(f"Frank here. Failed to kill {command} (PID {pid}): {e}")
        return False

# Kill conflicting IPFS processes
def kill_ipfs_processes():
    try:
        subprocess.run(['pkill', '-f', 'ipfs daemon'], check=False)
        print("Frank here. Killed existing IPFS daemon processes.")
        time.sleep(1)  # Give time for processes to terminate
    except Exception as e:
        print(f"Frank here. Failed to kill IPFS processes: {e}")

# Ensure IPFS daemon is running
def ensure_ipfs_daemon(force_ports=False):
    host, api_port = "127.0.0.1", 5001
    gateway_ports = [8080, 8081, 8082]  # Try these ports
    selected_port = None

    if is_ipfs_running():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((host, api_port))
                print("IPFS daemon: already live on 5001.")
                # Check current gateway port
                config_path = os.path.expanduser("~/.ipfs/config")
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                    current_port = int(config['Addresses']['Gateway'].split('/')[-1])
                    if check_port(host, current_port):
                        return True, current_port
                    else:
                        print(f"Frank here. Current gateway port {current_port} blocked, clearing...")
                        kill_ipfs_processes()
                else:
                    print("Frank here. No IPFS config found, trying default ports...")
        except (OSError, ConnectionRefusedError):
            print("Frank here. IPFS daemon running but not on 5001. Killing and restarting...")
            kill_ipfs_processes()

    if not check_port(host, api_port):
        print("Frank here. Port 5001 blocked—cannot start IPFS daemon.")
        return False, None

    for port in gateway_ports:
        pid, command = get_port_process(port)
        if pid:
            if command == 'ipfs':
                print(f"Frank here. IPFS found on port {port}, killing...")
                kill_ipfs_processes()
            else:
                print(f"Frank here. Port {port} blocked by {command} (PID {pid}). Clearing...")
                if not kill_process_on_port(port, pid, command, force_ports):
                    print(f"Frank here. Port {port} still blocked after attempt to clear, trying next...")
                    continue
        if check_port(host, port):
            if update_ipfs_config(port):
                selected_port = port
                break
        else:
            print(f"Frank here. Port {port} still blocked after attempt to clear, trying next...")

    if not selected_port:
        print("Frank here. No available ports (8080, 8081, 8082).")
        return False, None

    # Final port check
    if not check_port(host, selected_port):
        print(f"Frank here. Selected port {selected_port} blocked after clearing attempts.")
        return False, None

    print(f"IPFS daemon: sparking on port {selected_port}...")
    for attempt in range(3):  # Retry daemon start
        try:
            subprocess.Popen(['ipfs', 'daemon'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for _ in range(15):  # Poll for 30s max
                time.sleep(2)
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(1)
                        s.connect((host, api_port))
                        print("IPFS daemon: live on 5001.")
                        return True, selected_port
                except (OSError, ConnectionRefusedError):
                    pass
            print(f"heat spike-flinch: IPFS daemon failed to start after 30s (attempt {attempt+1}/3).")
        except FileNotFoundError:
            print("Frank here. IPFS not installed. Grab it from https://dist.ipfs.tech/#kubo.")
            return False, None
    print("heat spike-flinch: IPFS daemon failed after 3 attempts.")
    return False, None

# Check if IPFS daemon is already running
def is_ipfs_running():
    try:
        result = subprocess.run(['pgrep', '-f', 'ipfs daemon'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        print("Frank here. 'pgrep' not found—assuming IPFS not running.")
        return False

# Stub for oracle.py
class Oracle:
    def prophesy(self, entropy, power):
        print(f"Oracle speaks: Entropy {entropy:.2f}, Power {power:.2f} - The path unfolds.")

oracle = Oracle()

# Full Seraph class for entropy guardianship
class Seraph:
    def test_entropy(self, data):
        entropy = random.uniform(0, 1)
        if entropy >= 0.99:
            print("Follow me.")
            return "Leading to Oracle", entropy
        elif entropy < 0.69:
            print("I'm sorry for this.")
            return "Pruned", entropy
        return "Ignored", entropy

# Full EthicsModel for TACSI power balancing
class EthicsModel:
    def balance_power(self, lived, corporate, diff=1.0, delta=600.0, prev_diff=1.0):
        thimble = symbols('thimble')
        eq1 = Eq(sin(thimble * len(lived)), len(lived) / 10.0)
        eq2 = Eq(sin(thimble * len(corporate)), len(corporate) / 10.0)
        eq3 = Eq(sin(thimble * diff / prev_diff), delta / 600.0)
        sols = solve([eq1, eq2, eq3], thimble)
        if not sols:
            print("heat spike-flinch")
            variance = 0.5
        else:
            variance = len(sols) / 2.0
        power = (len(lived) + len(corporate)) / 2 * random.uniform(0.4, 1.2) * variance
        if power > 1.0:
            power *= 0.69
        if power < 0.69:
            print("Frank here.")
        return power

# BloomFilter class for dream shuffling
class BloomFilter:
    def __init__(self, size=1024, hash_count=3):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size

    def add(self, item):
        for i in range(self.hash_count):
            digest = hashlib.sha256(str(i).encode('utf-8') + item.encode('utf-8')).hexdigest()
            index = int(digest, 16) % self.size
            self.bit_array[index] = 1

    def shuffle(self):
        print("Shuffling bloom in dream mode...")

# Verbism hashing helper
def self_write_hashlet(verbism):
    return base64.b64encode(verbism.encode('utf-8')).decode('utf-8')

# Constants for Blocsÿm's essence
TERNARY_GRID_SIZE = 2141
ENTROPY_THRESHOLD = 0.69
PRUNE_AFTER = 2140
HASH_WINDOW_MIN = 3
HASH_WINDOW_MAX = 145
ROCK_DOTS = b"\xc3\xbf\xc3\xbf\xc3\xbf"

# Calm scenery for AFK meditation
SCENERY_DESCS = [
    "Blocsÿm meditates in the chrysanthemum temple, fractals blooming like thoughts.",
    "Rock dots pulse under starry skies, elephant memory recalling all hashes.",
    "Dojo hidden in ternary mist: Training updates, Smith none the wiser."
]

# Integrated BlocsymDB for DB/cross-chain ops
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
        return "Dojo update hidden—Smith blind."

    def meditate(self, idle_time, diff):
        if idle_time > 60 and not self.meditation_active:
            self.meditation_active = True
            scenery = SCENERY_DESCS[int(time.time()) % len(SCENERY_DESCS)]
            entropy = get_entropy()
            ribit_int, state, color = ribit_generate(str(diff))
            print(f"[Blocsÿm Meditates]: {scenery} Diff RIBIT: {ribit_int}, State: {state}, Color: {color}")
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

# Vintage corking function
def cork_bloom(bloom_data, grade):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
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
        cid = ping_pin(file_path)
        print(f"Vintage pinned: {cid}")
    except Exception as e:
        print(f"Frank here. IPFS pin failed: {e}. Saved locally at {file_path}")
    return hash_tag

# Spectra hash for RGB vision
def spectra_hash(entropy):
    hex_str = hashlib.sha256(str(entropy).encode()).hexdigest()[:6]
    r, g, b = int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)
    return [r/255, g/255, b/255]

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

# Stub for Hugging Face transformers
class HuggingFaceModel:
    def __init__(self):
        pass

    def process(self, input_text):
        return "Stubbed semantic output: " + input_text.upper()

# Stub for LLaMA
class LLaMA:
    def __init__(self):
        pass

    def communicate(self, message):
        return "LLaMA whispered: " + message[::-1]

# DualFacehugger class
class DualFacehugger:
    def __init__(self):
        self.left_eye = HuggingFaceModel()
        self.right_eye = HuggingFaceModel()
        self.llama_comms = LLaMA()
        print("Dual Facehuggers initialized - hugging face with LLaMA whispers.")

    def process_input(self, left_input, right_input):
        left_output = self.left_eye.process(left_input)
        right_output = self.right_eye.process(right_input)
        comm_message = left_output + " | " + right_output
        llama_response = self.llama_comms.communicate(comm_message)
        print(f"Dual output: {llama_response}")
        return llama_response

    def integrate_with_pong(self, pong):
        left_blink = random.choice(["open", "closed"])
        right_blink = random.choice(["open", "closed"])
        self.process_input(left_blink, right_blink)
        pong.update_bat(random.choice([True, False]))

# Globals/sim state
bloom = BloomFilter()
current_entropy = 0.5
idle_start = time.time()
last_command = ""
db = BlocsymDB()
frank = Frank()
pong = None
spoon = None
facehugger = None
ghost_hand = None
last_height = 0
last_time = 0
last_diff = 0.0
vibe_model = TetraVibe()
last_commit = 0.0
conversations_doc = "conversations_content"
if Flask is not None:
    app = Flask(__name__)
    socketio = SocketIO(app)
    @socketio.on('connect')
    def handle_connect():
        emit('message', {'data': 'Connected to Blocsym server'})

    @socketio.on('mosh')
    def handle_mosh(data):
        balanced = EthicsModel().balance_power(data.get('lived', ''), data.get('corporate', ''))
        emit('response', {'balanced_power': balanced, 'entropy': db.entropy_check(data.get('hash', ''))})

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

def check_afk(delta):
    global idle_start
    idle_time = time.time() - idle_start
    db.meditate(idle_time, last_diff)
    if idle_time > 600:
        print("Dream loop stub: Shuffling bloom...")
        bloom.shuffle()
    return idle_time

def persist_to_ipfs():
    global last_commit
    print("IPFS persistence stub: Dumping memory...")
    # Save block data locally first
    block_data = {
        "block": last_height,
        "timestamp": last_time,
        "diff": last_diff,
        "delta": last_time - (last_time - 600 if last_time else 0)
    }
    os.makedirs("./vintage", exist_ok=True)
    with open("./vintage/block_dump.json", "w") as f:
        json.dump(block_data, f)
    try:
        # Force a test pin to verify directory pinning
        root_cid = ping_pin_vintage('./vintage', 'she_key')
        print(f"Vintage dir committed: {root_cid}")
        conv_cid = ping_pin_conversations(conversations_doc, 'she_unlock')
        print(f"Conversations committed: {conv_cid}")
        last_commit = time.time()
    except Exception as e:
        print(f"Frank here. IPFS persistence failed: {e}. Block data saved locally at ./vintage/block_dump.json")

def get_latest_block():
    global last_height, last_time, last_diff
    for attempt in range(3):  # Retry 3 times
        try:
            resp = requests.get('https://blockchain.info/latestblock', timeout=5)
            resp.raise_for_status()
            data = resp.json()
            height = data['height']
            block_time = data['time']
            resp_diff = requests.get('https://blockchain.info/q/getdifficulty', timeout=5)
            resp_diff.raise_for_status()
            diff = float(resp_diff.text)
            if height > last_height:
                delta = block_time - last_time if last_time else 600  # Default to 600s if last_time is 0
                vibe, _ = vibe_model.friction_vibe(np.array([0,0,0]), np.array([delta/600, 0, 0]))
                delta *= max(vibe, 0.1)  # Ensure vibe doesn't zero delta
                print(f"New block {height} at {block_time}, delta {delta:.1f}s, diff {diff}")
                last_height = height
                last_time = block_time
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

def cleanup():
    print("Cleanup stub: GPIO/dream cleanup...")
    try:
        kill_ipfs_processes()
    except Exception as e:
        print(f"Frank here. Failed to kill IPFS daemon: {e}")
    try:
        db.close()
    except Exception as e:
        print(f"Frank here. Failed to close DB: {e}")
    if pong:
        try:
            pong.close()
        except Exception as e:
            print(f"Frank here. Failed to close Pong: {e}")

def run_cli(pong_mode=False, spoon_mode=False, dual_mode=False, ghost_mode=False):
    global pong, spoon, facehugger, ghost_hand
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
    if dual_mode:
        facehugger = DualFacehugger()
        print("Dual Facehugger mode activated - Hugging Face with LLaMA comms.")
        if pong_mode:
            facehugger.integrate_with_pong(pong)
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
        ethics = EthicsModel()
        power = ethics.balance_power("lived_experience", "corporate_input", diff, delta, last_diff)
        if power < 0.69:
            print("Whisper: forgive me")
            updates = f"Ethics imbalance: power {power:.2f}, recovering from low entropy {current_entropy:.2f}"
            print(db.dojo_train(updates, height))
        if current_entropy < 0.69:
            updates = f"Low entropy recovery: {current_entropy:.2f}, small upgrade to thought process"
            print(db.dojo_train(updates, height))
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

def main():
    parser = argparse.ArgumentParser(description="Blocsym: AI-Driven Decentralized Simulator")
    parser.add_argument('--mode', type=str, default='cli', choices=['cli', 'server'], help="Run in CLI or server mode")
    parser.add_argument('--pong', action='store_true', help="Enable Pong mode in CLI")
    parser.add_argument('--spoon', action='store_true', help="Enable SpoonBoy test mode in CLI (runs 5 sim bends and integrates)")
    parser.add_argument('--dual', action='store_true', help="Enable Dual Facehugger mode with Hugging Face and LLaMA (integrates with Pong if --pong)")
    parser.add_argument('--ghost', action='store_true', help="Enable Ghost Hand hedging mode in CLI")
    parser.add_argument('--force-ports', action='store_true', help="Force-kill all processes on ports 8080-8082 (use with caution)")
    args = parser.parse_args()
    
    # Check ports and start daemon
    daemon_ok, gateway_port = ensure_ipfs_daemon(force_ports=args.force_ports)
    if not daemon_ok:
        print(f"Grid’s tangled. Could not start IPFS daemon on port 5001.")
        # Save block data locally on failure
        block_data = {
            "block": last_height,
            "timestamp": last_time,
            "diff": last_diff,
            "delta": last_time - (last_time - 600 if last_time else 0)
        }
        os.makedirs("./vintage", exist_ok=True)
        with open("./vintage/block_dump.json", "w") as f:
            json.dump(block_data, f)
        print("Frank here. Block data saved locally at ./vintage/block_dump.json")
        sys.exit(1)
    
    if args.mode == 'cli':
        run_cli(pong_mode=args.pong, spoon_mode=args.spoon, dual_mode=args.dual, ghost_mode=args.ghost)
    elif args.mode == 'server' and Flask is not None:
        print("Starting Blocsym server on http://127.0.0.1:5001")
        socketio.run(app, host='0.0.0.0', port=5001)
    else:
        print("Server mode unavailable; run with --mode=cli.")

if __name__ == "__main__":
    try:
        print("IPFS load stub: Restoring from dump...")
        main()
    except KeyboardInterrupt:
        print("Frank here. Graceful shutdown initiated...")
        cleanup()
        sys.exit(0)
    except SystemExit:
        cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"heat spike-flinch: Unexpected error: {e}")
        cleanup()
        persist_to_ipfs()
        sys.exit(1)
