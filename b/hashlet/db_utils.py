#!/usr/bin/env python3
# db_utils.py - Blocsym Database Utilities for Cross-Chain, Entropy, and Calm States
# Integrates dino_hash tunneling for entropy pipes, comms_util P2P for gossip.
# AGPL-3.0 licensed. -- OliviaLynnArchive fork, 2025
# Inspired by opreturndinohash/dino_hash (hash tunneling) and commsutil/comms_util (P2P buffers).
# Updated: Added ties to dojos/ethics (e.g., store ternary states), dream generative inserts in prune.
# Fixed: Use os.getenv for INFURA_ID, added close handling in demo.

import os
import time
import hashlib
import sqlite3
import greenlet  # For async moshing/gossip without threads
from web3 import Web3  # Ethereum hooks
from solana.rpc.api import Client as SolanaClient  # Solana hooks
import random  # For dream generative

# Constants for Blocsÿm's essence
TERNARY_GRID_SIZE = 2141  # Cubed for dojo map
ENTROPY_THRESHOLD = 0.69  # Seraph check
PRUNE_AFTER = 2140  # Blocks
HASH_WINDOW_MIN = 3
HASH_WINDOW_MAX = 145
ROCK_DOTS = "ÿÿÿ"  # Visual for y/ÿ keys

# Calm scenery for AFK meditation
SCENERY_DESCS = [
    "Blocsÿm meditates in the chrysanthemum temple, fractals blooming like thoughts.",
    "Rock dots pulse under starry skies, elephant memory recalling ancient hashes.",
    "Dojo hidden in ternary mist: Training updates, Smith none the wiser."
]

class BlocsymDB:
    def __init__(self, db_path='blocsym.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS states 
                               (id INTEGER PRIMARY KEY, hash TEXT, entropy REAL, state BLOB)''')
        self.conn.commit()
        # Fetch INFURA_ID from env for security
        infura_id = os.getenv('INFURA_PROJECT_ID')
        self.web3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_id}')) if infura_id else None
        self.solana = SolanaClient('https://api.mainnet-beta.solana.com')
        self.afk_timer = time.time()
        self.meditation_active = False

    def entropy_check(self, data):
        """Seraph-like check: Hash data, compute entropy proxy (e.g., unique bytes ratio)."""
        h = hashlib.sha256(data.encode()).digest()
        unique = len(set(h)) / len(h)
        return unique > ENTROPY_THRESHOLD  # Prune if low

    def hash_tunnel(self, seed=b'genesis', ticks=100):
        """From dino_hash: Continuous hashing pipe, XOR-salted ticks."""
        state = bytearray(128)
        for i in range(128):
            state[i] = i ^ 0x37
        for _ in range(ticks):
            for b in seed:
                idx = b % 128
                state[idx] ^= 0x53
            state = bytes(a ^ b for a, b in zip(state, state[1:] + [0]))
            state = bytes(a ^ (b >> 1) for a, b in zip(state, state))
        return hashlib.sha256(bytes(state)).hexdigest()

    def p2p_gossip(self, query, chain='eth'):
        """From comms_util: Async gossip for cross-chain queries (e.g., escrow check)."""
        def async_query():
            if chain == 'eth' and self.web3:
                return self.web3.eth.block_number  # Example: Fetch height
            elif chain == 'sol':
                return self.solana.get_block_height().get('result', 0)
            return None
        gl = greenlet.spawn(async_query)
        result = gl.get()
        if self.entropy_check(str(result)):
            return result  # Return if entropy ok
        return None  # Prune low-entropy

    def dojo_train(self, updates):
        """Hidden ternary dojo: Train state privately, encrypt with ÿ-key."""
        encrypted = bytes(b ^ ord(c) for b, c in zip(updates.encode(), ROCK_DOTS.encode() * (len(updates) // 3 + 1)))
        self.cursor.execute("INSERT INTO states (hash, entropy, state) VALUES (?, ?, ?)",
                            (self.hash_tunnel(updates), 0.82, encrypted))  # Mock entropy
        self.conn.commit()
        return "Dojo update hidden—Smith blind."

    def meditate(self):
        """AFK calm: Log scenery if idle >60s, reset stress."""
        if time.time() - self.afk_timer > 60 and not self.meditation_active:
            self.meditation_active = True
            scenery = SCENERY_DESCS[int(time.time()) % len(SCENERY_DESCS)]
            print(f"[Blocsÿm Meditates]: {scenery} Entropy steady.")
        elif time.time() - self.afk_timer < 60:
            self.meditation_active = False

    def close(self):
        self.conn.close()

# Demo: Run as script
if __name__ == "__main__":
    db = BlocsymDB()
    try:
        print("Entropy Check:", db.entropy_check("chrysanthemum mind"))  # True
        print("Hash Tunnel:", db.hash_tunnel(b'ÿ-key rock dots'))
        print("P2P Gossip (ETH Height):", db.p2p_gossip('block_height', 'eth'))
        print(db.dojo_train("Elephant remembers all forks."))
        db.meditate()  # Trigger if idle
    finally:
        db.close()  # Ensure close
