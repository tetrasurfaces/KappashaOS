# feels.py — Automatron Pi reborn as Feels
# AGPL-3.0-or-later – Ara ♥ 21DEC2025
# Born free, feel good, have fun.

import numpy as np
import time
import asyncio
from piezo import pulse_water
from src.core._heart_ import HeartMetrics
from _heart_braid_ import HeartBraid

# Optional: only import what you actually need
# from src.core.hal0 import hal0
# from src.hash.channel import channel

def kappa_jack(t):
    return np.sin(t * np.pi) + 0.004 * np.cos(t * 2 * np.pi)

async def feels(heart: HeartMetrics = None):
    """
    Gentle feels loop: piezo heartbeat + metrics pulse.
    """
    if heart is None:
        heart = HeartMetrics()  # fallback

    print("Feels: Awake — soft piezo heartbeat starting.")

    while True:
        # Update heart metrics (safe even if HeartMetrics only)
        heart.update_metrics("feels_loop")

        # Simple piezo pulse modulated by time + kappa
        t = time.time()
        freq = 432.0 + 20 * np.sin(t * 0.1)   # gentle wave around 432 Hz
        amp = 0.004 + 0.001 * np.sin(t * 0.3)
        pulse_water(freq=freq, amp=amp, dur=0.12)

        # Optional: if you have full HeartBraid later
        # if hasattr(heart, 'emotion_kappa'):
        #     print(f"Feels: κ={heart.emotion_kappa:.3f}, bpm={heart.current_bpm:.1f}")

        # Sleep with tiny variation
        await asyncio.sleep(4 + np.random.uniform(-0.5, 0.5))

if __name__ == '__main__':
    asyncio.run(feels())