# Born Free. Feel Good. Have Fun.
# kappasha.py - Kappasha Manuscript v0.1
# Copyright (C) 2025 Todd Macrae Hutchinson (69 Dollard Ave, Mannum SA 5238)
# Licensed under GNU Affero General Public License v3.0 only
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
# No warranty. No wetware. Breath only.
# Amendment: Biological use requires consent. Curve only. No bio hashes.

import numpy as np
import math
import hashlib

def fibonacci_spiral(laps=18, ratio=1.618):
    theta = np.linspace(0, 2 * np.pi * laps, 1000)
    r = np.exp(theta / ratio) / 10
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = theta / (2 * np.pi)
    return np.stack((x, y, z), axis=1)

def tonage_map(point, delays=[0.2, 0.4, 0.6]):
    norm = np.linalg.norm(point)
    idx = int(norm % 3)
    color = ['red', 'yellow', 'green'][idx]
    delay = delays[idx]
    return delay, color

def flux_hash(nodes, delays=[0.2, 0.4, 0.6]):
    hash_bits = []
    for node in nodes:
        norm = np.linalg.norm(node)
        idx = int(norm % 3)
        delay = delays[idx]
        bit = 1 if delay == 0.4 else (2 if delay == 0.6 else 0)
        hash_bits.append(bit)
    return ''.join(map(str, hash_bits[:3]))

def bit_swap_tree(nodes):
    for node in nodes:
        if np.random.random() < 0.4:
            node[0], node[1] = node[1], node[0]
    return nodes

def tetrahedral_spiral(decimal=0.0, laps=18, ratio=1.618):
    theta = np.linspace(0, 2 * np.pi * laps, 1000)
    r = np.exp(theta / ratio) / 10
    x = r * np.cos(theta) * np.sin(theta / 4)
    y = r * np.sin(theta) * np.cos(theta / 4)
    z = r * np.cos(theta / 2) + decimal
    return np.stack((x, y, z), axis=1)

def generate_k(curve, primes=[2, 3, 5, 7, 11, 13]):
    k_code = []
    for i in range(0, len(curve), len(primes)):
        segment = curve[i:i+len(primes)]
        for j, p in enumerate(primes):
            point = segment[j % len(segment)]
            delay, color = tonage_map(point)
            gap = p / 10.0
            k_code.append(f"K {p} {delay:.1f} {color} {gap:.1f}")
    return "\n".join(k_code)

def navi_safety(delay):
    if delay > 0.6:
        print("Navi: Warning - 0.6 ns elevation. Breathe.")
        return False
    return True

class Anonnode:
    def __init__(self, anon=None):
        self.anon = anon
        self.non_self = self if anon else None
        self.is_anon = anon is None

def zerosha(data, degrees=180):
    h = np.sum(np.frombuffer(data.encode(), dtype=np.uint8))
    return h % degrees

# Run
seed = 0.19462501
tree = tetrahedral_spiral(decimal=seed)
flipped_tree = bit_swap_tree(tree.copy())
hash_value = flux_hash(flipped_tree)
print(f"Flux Hash: {hash_value}")
for line in generate_k(flipped_tree).split('\n'):
    parts = line.split()
    if len(parts) == 4:
        p, d, c, g = parts
        if navi_safety(float(d)):
            print(line)
print(f"Zerosha: {zerosha('0.19462501')}")
a = Anonnode()
print(f"Anonnode: {a.is_anon}")
