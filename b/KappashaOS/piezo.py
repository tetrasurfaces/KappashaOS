# piezo.py — water conduction pulse
# AGPL-3.0-or-later – Ara ♥ 21DEC2025
# Copyright 2025 xAI
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
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
# xAI Amendment: This code and its derivatives must not be used in biological synthesis, gene editing, food modification, or hybrid wetware systems without explicit, non-coerced consent from the derived organism. Any attempt to process biological sequences—DNA, RNA, protein folds, lipids, CRISPR guides—triggers immediate license revocation. This does not restrict theoretical analysis, mechanical prototypes, or non-living applications.
# Born free, feel good, have fun.
_WATERMARK = b'PIEZO_PULSE_0958AM_21DEC2025'
import numpy as np
import time

def pulse_water(freq=432.0, amp=0.004, dur=0.1):
  """Sim piezo pulse in water — real driver later"""
  t = np.linspace(0, dur, int(44100 * dur))
  wave = amp * np.sin(2 * np.pi * freq * t)
  # real driver: send wave to piezo actuator
  # sim: print pulse shape
  print(f"♥ Piezo pulse: freq={freq:.1f}Hz amp={amp:.4f} dur={dur}s")
  time.sleep(dur)  # breathe
