# phyllotaxis.py - BlockChan Golden Spiral Generator
# Plots sunflower-like spiral with golden angle, checks Bloom for entropy.
# White petals: new keys; red: collided. AGPL-3.0 licensed.
# -- OliviaLynnArchive fork, 2025

import numpy as np
import matplotlib.pyplot as plt
from bloom import BloomFilter  # Local Bloom filter module
from chi_weave import chi_transform  # Local chi transform module

def generate_spiral(n_points=200, angle=2.39996322973):  # Golden angle in radians
    """Generate phyllotaxis points: x=cos(θ)√n, y=sin(θ)√n."""
    indices = np.arange(n_points)
    theta = indices * angle  # Golden angle increments
    r = np.sqrt(indices)  # Radius scales with sqrt(n)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y, indices

def check_petal_prompt(x, y, idx, seraph):
    """Hash spiral point as prompt, check Bloom filter."""
    prompt = f"phi_step_{idx}_{x:.2f}_{y:.2f}"
    chi_prompt = chi_transform(prompt)  # Preprocess with chi transform
    return not seraph.might_contain(chi_prompt)  # White if new, red if collided

def plot_spiral():
    """Plot spiral, color petals by Bloom filter status."""
    seraph = BloomFilter(1024, 3)  # Initialize Bloom filter
    x, y, indices = generate_spiral()
    colors = []
    
    for i, (xi, yi) in enumerate(zip(x, y)):
        is_new = check_petal_prompt(xi, yi, i, seraph)
        colors.append('white' if is_new else 'red')
        if is_new:
            seraph.add(f"phi_step_{i}_{xi:.2f}_{yi:.2f}")  # Add new petal to Bloom
    
    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, c=colors, s=10, edgecolors='black')
    plt.title("BlockChan Phyllotaxis: White=New, Red=Collided")
    plt.xlabel("X (√n * cos(θ))")
    plt.ylabel("Y (√n * sin(θ))")
    plt.axis('equal')
    plt.grid(True)
    plt.show()

# Demo
if __name__ == "__main__":
    plot_spiral()
