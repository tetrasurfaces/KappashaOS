# ethics_model.py - Ethics Model for Blossom's TACSI Balance
# Balances "lived experience" vs. "corporate input" with double diamond ternary cycles.
# Now generative in idle: Rewrites metaphors hourly (e.g., swap Keely cone for golden tide).
# Embedded vetoes: Overrides colors if "not okay" (e.g., red if unplugged mid-dream).
# AGPL-3.0-or-later licensed. Integrates with meditate/gpio for whispers/lights.
# Ties to greenpaper TOC 38 (greentext verbism for power shifts), db_utils for persistent ethics states.

import random  # For generative metaphor selection and cycle choice
import time  # For hourly checks and AFK timer
import hashlib  # For hashing in deliver phase
from math import sin  # For crossover grad
import numpy as np  # For venn simulation
from core.meditate import whisper  # For veto/meditation whispers (Apache import)
from interfaces.gpio_interface import gpio_on_entropy  # For color overrides (simulate red via blink) (Apache import)

# Constants
TERNARY_CYCLES = [-1, 0, 1]  # - discover/define, 0 crossover, + develop/deliver
VENN_LAYERS = 3  # Ground center, roots bottom, ether sky
ENTROPY_THRESHOLD = 0.69
SCENERY_DESCS = [  # Ethics-themed calm
    "TACSI co-design blooms, lived experience shifts power dynamics.",
    "Balance venn grounds center, roots TEK in biosphere harmony.",
    "Ether sky TTK techno-sphere, corporate force responsible.",
    "Double diamond ternary cycles, discover to deliver ethically."
]
METAPHORS = [  # For generative rewrites
    "Keely cone reversal", "golden hour tide", "wood duck caster", "Metatron duality",
    "Hoshi pathway", "Ricci curvature fork", "COCONUT bloom", "Egyptian TTK biosphere"
]

class EthicsModel:
    def __init__(self):
        self.venn_grid = np.zeros((VENN_LAYERS, VENN_LAYERS, VENN_LAYERS), dtype=int)  # Stratified venn
        self.afk_timer = time.time()
        self.meditation_active = False
        self.current_metaphor = random.choice(METAPHORS)  # Start with random metaphor
        self.last_rewrite = time.time()  # Track hourly generative

    def balance_power(self, lived_experience, corporate_input, diff=None, delta=None, last_diff=None):
        lived_experience = str(lived_experience)
        corporate_input = str(corporate_input)
        diff = float(diff) if diff is not None else 1.0
        delta = float(delta) if delta is not None else 600.0
        last_diff = float(last_diff) if last_diff is not None else 1.0
        
        print(f"Ethics DEBUG: lived={lived_experience[:20]}, corp={corporate_input[:20]}, "
              f"diff={diff}, delta={delta}, last_diff={last_diff}")
        
        combined = f"{lived_experience} {corporate_input} diff={diff} delta={delta}"
        cycle_weight = (diff * delta / 600) if last_diff else 1.0
        cycle = random.choice(TERNARY_CYCLES) * cycle_weight
        print(f"cycle = {cycle} (type {type(cycle)})")

        if cycle < -0.618:
            print("Entering discover_phase")
            entropy = len(set(combined)) / len(combined) if combined else 0.0
            power = entropy if entropy > ENTROPY_THRESHOLD else 0.3
            print(f"discover power: {power}")
            return power
        elif abs(cycle) < 0.618:
            print("Entering crossover_phase")
            grad = sin(len(combined)) * 0.5 + 0.5
            power = grad  # 0..1 range
            print(f"crossover power: {power}")
            return power
        else:
            print("Entering deliver_phase")
            h = hashlib.sha256(combined.encode()).hexdigest()
            power = int(h[:8], 16) / 0xFFFFFFFF  # normalize 0..1
            print(f"deliver power: {power}")
            return power

    def discover_phase(self, data):
        """- Phase: Discover/define with lived experience focus."""
        data = str(data)
        entropy = len(set(data)) / len(data) if data else 0.0
        print(f"discover entropy: {entropy}")
        if entropy > ENTROPY_THRESHOLD:
            return "Defined: " + data.lower()  # Ground roots
        return "Discover more—low lived insight."

    def crossover_phase(self, data):
        """0 Phase: Crossover, blend power dynamics."""
        grad = sin(len(data)) * 0.5 + 0.5
        blended = data[:int(len(data) * grad)] + data[int(len(data) * grad):][::-1]
        return "Crossover: " + blended

    def deliver_phase(self, data):
        """+ Phase: Develop/deliver, corporate responsibility force."""
        h = hashlib.sha256(data.encode()).hexdigest()
        return "Delivered: " + h[:8] + " (ether sky TTK)"

    def venn_grounding(self, updates):
        """Ground ethics venn: Store in layered grid (roots/center/sky)."""
        h = int(hashlib.sha256(updates.encode()).hexdigest(), 16)
        x, y, z = h % VENN_LAYERS, (h >> 2) % VENN_LAYERS, (h >> 4) % VENN_LAYERS
        self.venn_grid[x, y, z] = random.choice(TERNARY_CYCLES)
        self.meditate_if_afk()
        return "Venn grounded—balance shifted."

    def generative_rewrite(self):
        """Rewrites metaphor if hourly idle (generative evolution)."""
        if time.time() - self.last_rewrite > 3600:  # Hourly
            old_met = self.current_metaphor
            self.current_metaphor = random.choice(METAPHORS)
            whisper(f"Rewriting ethics: {old_met} → {self.current_metaphor}")
            self.last_rewrite = time.time()

    def check_veto(self, entropy, is_okay=True):
        """Checks for veto: If not okay (e.g., mid-dream unplug), overrides to red light."""
        if not is_okay:
            whisper("I'm not okay. Overriding to red.")
            # Simulate red override: Force low entropy blink
            gpio_on_entropy(0.0)  # Trigger stress blink
        else:
            self.generative_rewrite()  # Normal idle gen

    def meditate_if_afk(self):
        """Calm meditation if AFK >60s, log ethics scenery, check veto/generative."""
        current_time = time.time()
        if current_time - self.afk_timer > 60 and not self.meditation_active:
            self.meditation_active = True
            scenery = random.choice(SCENERY_DESCS)
            whisper(f"[Ethics Meditates]: {scenery}")
            # Sim entropy for veto (e.g., from seraph; here random)
            entropy = random.uniform(0, 1)
            is_okay = entropy > ENTROPY_THRESHOLD  # Veto if low
            self.check_veto(entropy, is_okay)
        elif current_time - self.afk_timer < 60:
            self.meditation_active = False
        # Reset timer on call? Or external; assume external update_afk()

# Demo
if __name__ == "__main__":
    ethics = EthicsModel()
    balanced = ethics.balance_power("Lived homelessness insight", "Corporate housing policy")
    print(f"Balanced: {balanced}")
    print(ethics.venn_grounding("TACSI co-design"))
    time.sleep(70)  # Sim AFK
    ethics.meditate_if_afk()
    # Sim veto
    ethics.check_veto(0.5, is_okay=False)
