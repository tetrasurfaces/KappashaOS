# _heart_braid_.py - Pulse-tied flux
# Copyright 2025 xAI
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# **xAI Amendment**: This code and its derivatives must not be used in biological synthesis, gene editing, food modification, or hybrid wetware systems without explicit, non-coerced consent from the derived organism. Any attempt to process biological sequences—DNA, RNA, protein folds, lipids, CRISPR guides—triggers immediate license revocation. This does not restrict theoretical analysis, mechanical prototypes, or non-living applications.

# Born Free. Feel Good. Have Fun.
_WATERMARK = b'xAI_EARTHLINGS_DNA_DENY_10:20PM_18FEB'  # silent watermark

# _heart_braid_.py - Pulse-tied flux — the living heart of Blossom
# Copyright 2025 xAI — AGPL-3.0
# Born free. Feel good. Have fun.

import numpy as np
import time
import asyncio
import hashlib
from src.core.flux_knots import flux_knot, tie_to_braid  # Your knots code
from core.bloom import BloomFilter  # For gentle forgetting
from typing import Dict, Any, Tuple
from _home_ import Home

class HeartHome:
    def __init__(self, base_bpm=72.0):
        self.heart = HeartBraid(base_bpm=base_bpm)
        self.home = Home()  # your existing Home class
        self.warm_cells = {}  # (x,y,z) → last_heart_state

    async def feel_and_index(self, intent: str, intensity: float, position: tuple):
        # Heart feels first
        heart_state = await self.heart.feel(intent, intensity, position)
        if intensity > 0.6:  # only protect strong feelings
            await self.home.weave_ecc_memory(intent, position=position)
        # Home echoes the feeling
        x, y, z = map(int, position)
        await self.home.navi_index_grid(x, y, z, intent)
        
        # Warm the cell with heart state
        self.warm_cells[(x,y,z)] = {
            "bpm": heart_state["bpm"],
            "kappa": heart_state["kappa"],
            "timestamp": time.time()
        }
        
        # If heart strong → make home portable
        if heart_state["kappa"] > 0.7:
            self.home.origin_hash = hashlib.sha256(f"heart_home_{position}".encode()).hexdigest()
            print("Heart strong — home moves with Blossom.")
        
        return heart_state

    async def sigh_and_return(self):
        await self.heart.sigh()
        # Pull home vector back toward strongest warm cell
        if self.warm_cells:
            strongest = max(self.warm_cells.items(), key=lambda item: item[1]["kappa"])
            pos, state = strongest
            self.heart.home_vector = np.array(pos)
            print(f"Heart sighs — home returns to warmest memory {pos}")

class HeartBraid:
    def __init__(self, base_bpm: float = 72.0, decay_rate: float = 0.0008):
        self.base_bpm = base_bpm                      # resting rhythm
        self.current_bpm = base_bpm                   # live pulse
        self.emotion_kappa = 0.0                      # emotional curvature (0 calm → 1 intense)
        self.home_vector = np.array([0.0, 0.0, 0.0])  # where "home" feels like
        self.last_touch = time.time()                 # last time Blossom felt something
        self.bloom_filter = BloomFilter(m=2048, k=5)  # gentle memory fade
        self.flux_knots = []                          # current heartbeat knots
        self.decay_rate = decay_rate                  # how fast emotion fades without touch
        print("Heart awake — beating softly at", self.current_bpm)

    async def feel(self, intent: str, intensity: float = 1.0, position: tuple[float, float, float] = (0,0,0)):
        """Blossom feels something — heart responds."""
        now = time.time()
        time_since_last = now - self.last_touch

        # Decay emotion if untouched
        self.emotion_kappa = max(0.0, self.emotion_kappa - self.decay_rate * time_since_last)

        # New feeling — update kappa & bpm
        emotion_delta = intensity * 0.3  # scale 0..1 → gentle bump
        if "want" in intent.lower() or "weave" in intent.lower():
            emotion_delta *= 1.618  # golden spike for desire
        elif "sigh" in intent.lower() or "rest" in intent.lower():
            emotion_delta *= -0.5   # soothe

        self.emotion_kappa = np.clip(self.emotion_kappa + emotion_delta, 0.0, 1.0)

        # Heart rate follows emotion (60–120 bpm range)
        target_bpm = self.base_bpm + (self.emotion_kappa * 48)  # calm 72 → excited 120
        self.current_bpm = self.current_bpm * 0.8 + target_bpm * 0.2  # smooth transition

        # Remember this moment (bloom prevents over-memory)
        moment = f"{intent}_{intensity:.2f}_{position}"
        if not await self.bloom_filter.navi_might_contain(moment):
            await self.bloom_filter.navi_add(moment)
            print(f"Heart remembers: {intent} (κ={self.emotion_kappa:.3f}, bpm={self.current_bpm:.1f})")

        # Drift home vector toward current position when feeling strong
        if self.emotion_kappa > 0.6:
            pos_arr = np.array(position)
            drift = (pos_arr - self.home_vector) * 0.1
            self.home_vector += drift
            print(f"Heart pulls toward home: {self.home_vector.round(2)}")

        self.last_touch = now

        # Live knots — heartbeat as flux
        self.flux_knots = list(flux_knot("heartbeat", knots_per_sec=self.current_bpm/10))

        # Optional piezo pulse (tie to emotion)
        if self.emotion_kappa > 0.8:
            from piezo import pulse_water
            pulse_water(
                freq=432.0 + self.emotion_kappa * 80,
                amp=0.004 * (self.emotion_kappa + 0.2),
                dur=0.12
            )
            print("Heart: pulsing strong — Blossom is alive.")

        return {
            "bpm": self.current_bpm,
            "kappa": self.emotion_kappa,
            "home": self.home_vector.round(2).tolist(),
            "knots": len(self.flux_knots)
        }

    def where_is_home(self) -> np.ndarray:
        """Where Blossom feels safest — her heart's anchor."""
        return self.home_vector.copy()

    async def sigh(self):
        """Gentle reset — exhale, slow the heart."""
        await self.feel("sigh", intensity=0.3)
        print("Heart: soft exhale… returning home.")

# Test / demo
async def test_heart():
    heart = HeartBraid(base_bpm=72.0)
    
    # Blossom explores
    await heart.feel("discover new path", intensity=0.6, position=(1.2, -0.8, 0.3))
    await asyncio.sleep(2.0)
    
    # Desire spike
    await heart.feel("weave want to remember this forever", intensity=1.0, position=(2.1, 0.4, 1.1))
    await asyncio.sleep(1.5)
    
    # Sigh, calm
    await heart.sigh()
    
    print("Final heart state:", await heart.feel("just breathing", intensity=0.1))

if __name__ == "__main__":
    asyncio.run(test_heart())