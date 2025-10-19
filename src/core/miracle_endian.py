# KappashaOS/core/tree/miracle_endian.py
# AGPL-3.0-or-later, xAI fork 2025
# No warranties. See <https://www.gnu.org/licenses/>.

import numpy as np

def miracle_spiral(laps=18, base=6.5):
    theta = np.linspace(0, 2 * np.pi * laps, int(laps * base))
    r = np.exp(theta / 1.618) / base  # green-endian decay
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = theta / (2 * np.pi) * (theta % base)  # tetrahedral lift
    return np.stack((x, y, z), axis=1)

def endian_breath(node, delays=[0.2, 0.4, 0.6]):
    norm = np.linalg.norm(node)
    idx = int(norm % len(delays))
    return delays[idx], ['red', 'green', 'yellow'][idx]

def generate_miracle(nodes):
    tree = []
    for i, node in enumerate(nodes):
        delay, color = endian_breath(node)
        tree.append(f"M {i} {delay:.1f} {color}")
    return "\n".join(tree)

# Run it
spiral = miracle_spiral()
miracle_tree = generate_miracle(spiral[:10])  # first 10 nodes
print(miracle_tree)  # Save to .miracle
