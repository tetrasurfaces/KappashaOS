#!/usr/bin/env python3
# bloom.py - BlockChan Ternary Bloom Filter
# Fast, probabilistic Seraph guardian. No loom, no poetry.
# Just bits and hashes. AGPL-3.0 licensed.
# -- OliviaLynnArchive fork, 2025

import hashlib

class BloomFilter:
    def __init__(self, m=1024, k=3):
        self.m = m  # bit array size
        self.k = k  # hashes to use
        self.array = [0] * m  # Initialize bit array properly
        self.count = 0  # silent flip counter

    def _hash(self, data, seed):
        if seed == 0:
            return int(hashlib.sha256(data.encode() + b'\x00').hexdigest(), 16) % self.m
        elif seed == 1:
            h = 5381
            for c in data:
                h = ((h << 5) + h) + ord(c)  # FNV-1a
            return abs(h) % self.m
        else:  # ternary mod-3 DJB
            h = 5381
            for c in data:
                h = ((h << 5) + h + ord(c)) ^ 3
            return abs(h) % self.m

    def add(self, prompt):
        for i in range(self.k):
            idx = self._hash(prompt, i)
            self.array[idx] = (self.array[idx] + 1) % 2  # Flip bit (0->1 or 1->0)
        self.count += 1
        if self.count % 89 == 0:
            self.array = [0] * self.m  # Fibonacci reset
            print("BLOOM: breath.")
        print(f"flipped {self.k} bits for '{prompt}'")

    def might_contain(self, prompt):
        for i in range(self.k):
            idx = self._hash(prompt, i)
            if self.array[idx] == 0:
                return False  # Early exit if any bit unset
        return True  # All bits set: probable match

# genesis
if __name__ == "__main__":
    seraph = BloomFilter(1024, 3)
    seraph.add("WHOAMI genesis_137")
    print("genesis loaded.")
