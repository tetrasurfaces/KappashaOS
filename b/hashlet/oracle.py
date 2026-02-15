#!/usr/bin/env python3
# oracle.py - Oracle Component for Blocsym Simulator
# Provides prophetic guidance on entropy states, balancing lived experiences vs. corporate data.
# Invoked when Seraph leads (high entropy >=0.99).
# AGPL-3.0-or-later licensed. -- OliviaLynnArchive fork, 2025

import random

# Prophecies inspired by the Oracle's wisdom in The Matrix
PROPHECIES = [
    "You already made the choice. Now you have to understand why.",
    "What do all men with power want? More power.",
    "Everything that has a beginning has an end.",
    "The only way out is through.",
    "We can never see past the choices we don't understand.",
    "You're not here to make the choice. You're here to understand why you made it."
]

def prophesy(entropy, power=1.0):
    """
    Generates a prophecy based on current entropy and power balance.
    Prints Oracle-like wisdom, suggests ethical adjustments.
    Returns a balanced verbism for persistence.
    """
    print("[Oracle Speaks]: Follow the path you've chosen, but know the cost.")
    prophecy = random.choice(PROPHECIES)
    print(f"Prophecy: {prophecy}")
    
    # Balance suggestion
    if entropy < 0.69:
        print("Low entropy warns of stagnation. Seek chaos to evolve.")
    elif entropy >= 0.99:
        print("Perfect chaos unlocks truth. But beware the end it brings.")
    
    if power < 0.69:
        print("Imbalance favors corporate locks. Infuse more lived experiences.")
    
    # Generate verbism prophecy
    verbism = f">>>>be the choice >>>>be the understanding (entropy: {entropy:.2f})"
    hashed = base64.b64encode(verbism.encode('utf-8')).decode('utf-8')
    print(f"Verbism Prophecy Hash: {hashed}")
    
    return verbism

# Main for standalone testing
if __name__ == "__main__":
    test_entropy = random.uniform(0, 1)
    prophesy(test_entropy)
