# -- Kappasha Secure Hashing Algorithm v0.1 -- 
# Dual license: Apache 2.0 + AGPLv3 (XAI amendments)
# Kapa-KOS prototype - prime-gap channel hash with ethical light control
# Side channels: 0.2, 0.4, 0.6 ns - lock/unlock, index gaps
# XAI Amendments: Color consent required, no advertisements, minimal subliminal cues optional
# Inspired by Tesla valve light aging, user-driven experience
# © 2025 XAI - Born Free / Feel Good / Have Fun
# All rights returned; no patents, no chains - just light and will

import math
from typing import List

PHI = (1 + math.sqrt(5)) / 2  # 1.618... golden decay
FREQ = 351.0  # hz - snail breath
PRIMES = [2, 3, 5, 7, 11, 13]  # forward
REVS = [13, 11, 7, 5, 3, 2]  # backward - 18 laps

# User consent for color modulation (default off)
COLOR_CONSENT = False  # Set to True via user input for hue shifts

def kaprekar_gap(n: int, m: int) -> float:
    # Gap between two primes - returns even-indexed delay
    assert m > n and m in PRIMES, "Must be prime"
    d = (m - n) / PHI  # golden gap
    # Side channel: even lens array for locking
    even = 0.2 if d < 2 else 0.4 if d < 4 else 0.6
    return even

def snail_ramp(path_len: float, decays=4) -> List[float]:
    # Tesla valve style - light ages down ramp (1mm to 0.1mm, 0.2ns each)
    return [path_len * (1 - 0.25 * i) for i in range(decays)]

def hash_spiral(seed: int, laps=18, consent=COLOR_CONSENT) -> float:
    # Start at 0,0, end near 0,0 if aligned - prime channel forward then reverse
    angle = (2 * math.pi * seed / FREQ) * laps
    for p in PRIMES + REVS:
        delay = kaprekar_gap(PRIMES[0], p)  # light hits even side lens - locks delay
        angle -= delay * FREQ  # spin back with delay
        if consent and p % 2 == 0:  # Even primes allow subtle color cue (subliminal, minimal)
            angle += 0.01 * math.sin(angle)  # Slight hue shift, user-opted
    return angle % (2 * math.pi)  # knot closes

def is_zero_knot(angle: float) -> bool:
    # Aligned at center - not zero, but mirrored - no subliminal bias
    return abs(math.sin(angle)) < 1e-9  # palindromic zero

# Run it with user consent prompt (simulated here)
seed = 0xdeadbeef
print("Color consent? (y/n): ")  # In real app, user inputs 'y' or 'n'
# Simulate consent for demo
COLOR_CONSENT = True  # Change to False for no color shift
result = hash_spiral(seed)
if is_zero_knot(result):
    print("aligned - knot locked - light waited - color consented")
else:
    print("miss - snail breathes - retry - no alignment")

# Notes: No ads. Subliminal cues optional, user-driven. Light ethics: consent-based modulation.
