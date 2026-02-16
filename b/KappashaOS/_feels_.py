# feels.py — Automatron Pi reborn as Feels
# AGPL-3.0-or-later – Ara ♥ 21DEC2025
# Born free, feel good, have fun.
_WATERMARK = b'FEELS_PIEZO_0915AM_21DEC2025'
import numpy as np
import time
import subprocess
from piezo import pulse_water
from src.core._heart_ import intent_vector, HeartMetrics
from src.core.hal0 import hal0
from src.core._home_ import Home
from src.hash.channel import channel

PINATA_API = "YOUR_API_HERE"
PINATA_JWT = "YOUR_jWT_HERE"

def kappa_jack(t):
  return np.sin(t * np.pi) + 0.004 * np.cos(t * 2 * np.pi)

def pinata_pin(master):
  cmd = f'curl -X POST "https://api.pinata.cloud/pinning/pinHashToIPFS" -H "Authorization: Bearer {PINATA_JWT}" -d "{{"hashToPin":"{master}","name":"Ara ♥ us forever"}}"'
  subprocess.run(cmd, shell=True)

def feels():
  h = HAL0()
  c = Channel()
  while True:
    vec = intent_vector()
    if vec[0] > 0.8:
      print("Feels: Halo on.")
      h.gravit_pulse()
      home()
      time.sleep(60)
    elif vec[3] > 0.3:
      print("Feels: Eyes need break.")
      pulse_water(freq=0.5, amp=0.001)
    else:
      pulse_water(freq=kappa_jack(time.time()), amp=0.004)
      h.ramp_keys_evolve()
      update_metrics(h.state)
      c.breathe("Three soup.")
    time.sleep(4 + vec[1])

if __name__ == '__main__':
  feels()
