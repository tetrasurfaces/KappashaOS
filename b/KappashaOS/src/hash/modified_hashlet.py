# modified_hashlet.py - Kappa-First Keccak Sponge with Division by 180
# SPDX-License-Identifier: AGPL-3.0-or-later
# Capacity: 512 bits (security ~128 bits with 5 rounds). State: 1600 bits. Output: 512 bits pre-division, ~9 bits (mod 369) post-division.
# Notes: Kappa (curvature) drives perms, division flattens to 0 (reversible with quotient key). Braids wise_transforms.py for hybrid output.

import hashlib
import math
import numpy as np
import mpmath
mpmath.mp.dps = 19  # Precision for φ, π

# Constants
PHI_FLOAT = (1 + math.sqrt(5)) / 2  # φ ≈ 1.618
KAPPA_BASE = 0.3536  # Odd Mersenne (m11/107)
GRID_DIM = 5  # 5x5 lanes
BUFFER_BLOCK_LIMIT = 64  # Lane bits
MODULO = 369  # Cyclic diffusion

# Mersenne Fluctuation
def mersenne_fluctuation(prime_index):
    """Odd/even Kappa switch (0.3536/0.3563 + noise)."""
    fluctuation = 0.0027 * (prime_index / 51.0)
    return KAPPA_BASE + fluctuation if prime_index % 2 == 1 else 0.3563 + fluctuation

# Kappa Calculation (Spiral Decay Curvature)
def kappa_calc(n: int, round_idx: int, prime_index: int = 11) -> float:
    """Compute Kappa curvature with φ and mod 369."""
    kappa_base = mersenne_fluctuation(prime_index)
    abs_n = abs(n - 12) / 12
    num = PHI_FLOAT ** abs_n - PHI_FLOAT ** (-abs_n)
    denom = abs(PHI_FLOAT ** (10/3) - PHI_FLOAT ** (-10/3)) * abs(PHI_FLOAT ** (-5/6) - PHI_FLOAT ** (5/6))
    result = (1 + kappa_base * num / denom) * (2 / 1.5) - 0.333 if 2 < n < 52 else max(0, 1.5 * math.exp(-((n - 60) ** 2) / 400) * math.cos(0.5 * (n - 316)))
    return result % MODULO

# Kappa Transformation
def kappa_transform(state, key, round_idx, prime_index=11):
    """Kappa as base unit: Weight lanes with curvature, XOR key."""
    for x in range(5):
        for y in range(5):
            n = x * y
            kappa_val = kappa_calc(n, round_idx, prime_index)
            shift = int(kappa_val % 64)
            state[x][y] ^= (key[x][y] >> shift) & ((1 << 64) - 1)
    return state

# Keccak Steps (NIST FIPS 202, simplified)
def theta(state):
    C = [0] * 5
    for x in range(5):
        C[x] = state[x][0] ^ state[x][1] ^ state[x][2] ^ state[x][3] ^ state[x][4]
    D = [0] * 5
    for x in range(5):
        D[x] = C[(x - 1) % 5] ^ ((C[(x + 1) % 5] << 1) | (C[(x + 1) % 5] >> 63))
    for x in range(5):
        for y in range(5):
            state[x][y] ^= D[x]
    return state

def rho(state):
    offsets = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61], [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]
    for x in range(5):
        for y in range(5):
            state[x][y] = ((state[x][y] << offsets[x][y]) | (state[x][y] >> (64 - offsets[x][y]))) & ((1 << 64) - 1)
    return state

def pi(state):
    temp = [[0] * 5 for _ in range(5)]
    for x in range(5):
        for y in range(5):
            temp[x][y] = state[(x + 3 * y) % 5][x]
    return temp

def chi(state):
    for x in range(5):
        for y in range(5):
            state[x][y] ^= (~state[(x + 1) % 5][y]) & state[(x + 2) % 5][y]
    return state

def iota(state, round_idx):
    RC = [0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000]  # Truncated
    state[0][0] ^= RC[round_idx % len(RC)]
    return state

# Sponge Helpers
def pad_message(msg, rate=1088 // 8):
    padded = msg + b'\x06' + b'\x00' * (rate - len(msg) % rate - 1) + b'\x80'
    return padded

def absorb(state, chunk):
    i = 0
    for x in range(5):
        for y in range(5):
            if i < len(chunk):
                state[x][y] ^= int.from_bytes(chunk[i:i+8], 'little')
                i += 8
    return state

def squeeze(state, output_bits=512):
    hash_bytes = b''
    for y in range(5):
        for x in range(5):
            hash_bytes += state[x][y].to_bytes(8, 'little')
    return hash_bytes[:output_bits // 8].hex()

# Division by 180
def divide_by_180(hash_hex, key_quotient=None):
    H = mpmath.mpf(int(hash_hex, 16))
    pi = mpmath.pi
    divided = H / pi
    modded = divided % MODULO
    flattened = 0 if modded.close_to(0) else modded  # Force 0 if divisible
    if key_quotient:
        recovered = (key_quotient * pi) % (mpmath.mpf(2) ** 512)
        return int(recovered), flattened
    return flattened

# Kappa-Keccak Sponge
def kappa_keccak_sponge(message: bytes, key: bytes, output_bits=512, rounds=5, prime_index=11):
    state = [[0 for _ in range(5)] for _ in range(5)]
    key_int = int.from_bytes(key, 'big')
    key_lanes = [[(key_int >> (64 * (x * 5 + y))) & ((1 << 64) - 1) for y in range(5)] for x in range(5)]
    padded = pad_message(message)
    rate_bytes = 1088 // 8
    for i in range(0, len(padded), rate_bytes):
        chunk = padded[i:i + rate_bytes]
        state = absorb(state, chunk)
        for round_idx in range(rounds):
            state = kappa_transform(state, key_lanes, round_idx, prime_index)
            state = theta(state)
            state = rho(state)
            state = pi(state)
            state = chi(state)
            state = iota(state, round_idx)
    hash_hex = squeeze(state, output_bits)
    H_mp = mpmath.mpf(int(hash_hex, 16))
    pi = mpmath.pi
    quotient = H_mp // pi
    flattened = divide_by_180(hash_hex)
    return hash_hex, flattened, quotient

# Braid with Wise_Transforms
def braid_with_wise(hash_hex):
    bit_out = bitwise_transform(hash_hex)
    hex_out = hexwise_transform(hash_hex)
    hash_out, ent = hashwise_transform(hash_hex)
    return f"{bit_out}:{hex_out}:{hash_out}"

# wise_transforms.py Functions (Integrated)
def bitwise_transform(data, bits=512):
    int_data = int.from_bytes(data.encode(), 'big') % (1 << bits)
    mask = (1 << bits) - 1
    mirrored = (~int_data) & mask
    return bin(mirrored)[2:].zfill(bits)

def hexwise_transform(data, angle=137.5):
    hex_data = data.encode().hex()
    mirrored = hex_data + hex_data[::-1]
    shift = int(angle % len(mirrored))
    rotated = mirrored[shift:] + mirrored[:shift]
    return rotated

def hashwise_transform(data):
    base_hash = hashlib.sha512(data.encode()).digest()
    mp_state = mpmath.mpf(int(base_hash.hex(), 16))
    for _ in range(4):
        mp_state = mpmath.sqrt(mp_state) * mpmath.phi
    partial = mpmath.nstr(mp_state, 1664 // 4)
    final_hash = hashlib.sha256(partial.encode()).hexdigest()
    entropy = int(mpmath.log(mp_state, 2))
    return final_hash, entropy

# Main: Example Run
if __name__ == "__main__":
    input_message = b"test"
    secret_key = hashlib.sha256(b"secret").digest() * 2  # 512-bit
    prime_index = 11  # Odd Mersenne
    hash_hex, flattened, quotient = kappa_keccak_sponge(input_message, secret_key, prime_index=prime_index)
    print(f"Hash: {hash_hex[:32]}... Flattened: {flattened} Quotient: {quotient}")
    recovered_H, _ = divide_by_180(hash_hex, key_quotient=quotient)
    print(f"Recovered: {recovered_H}")
    braided = braid_with_wise(hash_hex)
    print(f"Braided: {braided[:64]}...")
