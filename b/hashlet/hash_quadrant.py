# hash_quadrant.py - Hash Quadrant Generator for Blossom's Optics Prep
# Formerly greenpaper.py: Generates 11-layer cell PNGs from simulated data via Matplotlib.
# Computes 3 orthographic views (front/top/right) + third-angle projection with 40% overlap.
# Integrates with optics_view.py for direct raster-to-light post-generation; expandable TOC demos.
# AGPL-3.0-or-later licensed. -- OliviaLynnArchive fork, 2025

import matplotlib.pyplot as plt  # For PNG generation
import numpy as np  # For grid/layer data
import os  # For file paths
from optics_view import raster_to_light  # Apache import for post-gen light scan (optional)

# Constants
NUM_LAYERS = 11  # Total layers for Hash Quadrant
OVERLAP = 0.4  # 40% overlap for projections
GRID_SIZE = 100  # Sample size for cell grid (e.g., 100x100 per view)

# Sample TOC sections (placeholder; expand to 50 with real demos)
TOC = [
    "1. Intro to BlockChan",
    "38. Greentext Verbism for Power Shifts",
    # ... add more
]

class HashQuadrant:
    def __init__(self):
        self.cell_data = np.random.randint(0, 256, (NUM_LAYERS, GRID_SIZE, GRID_SIZE))  # Sample 3D data

    def run_demos(self):
        """Run TOC demos; generate PNGs for each layer."""
        print("Running Hash Quadrant TOC demos...")
        for section in TOC:
            print(f"Demo: {section}")
        self.generate_pngs()

    def generate_pngs(self, output_dir="layers"):
        """Generates 11 grayscale PNGs: 3 orthos (front/top/right averages) + third-angle + overlaps."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Compute views
        front = np.mean(self.cell_data[0:3], axis=0)  # Layers 0-2: Front ortho
        top = np.mean(self.cell_data[3:6], axis=0)  # 3-5: Top
        right = np.mean(self.cell_data[6:9], axis=0)  # 6-8: Right
        third_angle = np.mean(self.cell_data[9:11], axis=0)  # 9-10: Third-angle proj
        
        # Apply overlap (simple alpha blend sim; adjust for real)
        overlap_front_top = front * (1 - OVERLAP) + top * OVERLAP
        # ... expand for all pairs if needed
        
        # Save as grayscale PNGs
        views = [front, top, right, third_angle, overlap_front_top]  # Expand to 11 with more blends
        png_paths = []
        for i, view in enumerate(views * (NUM_LAYERS // len(views) + 1))[:NUM_LAYERS]:  # Pad to 11
            path = os.path.join(output_dir, f"layer_{i}.png")
            plt.imshow(view, cmap='gray')
            plt.axis('off')
            plt.savefig(path, bbox_inches='tight', pad_inches=0)
            plt.close()
            png_paths.append(path)
        
        print(f"Generated {NUM_LAYERS} PNG layers in {output_dir}")
        return png_paths

# Demo
if __name__ == "__main__":
    hq = HashQuadrant()
    hq.run_demos()
    # Optional: Raster to light post-gen
    png_paths = hq.generate_pngs()
    result = raster_to_light(png_paths)
    print("Optics result:", result)
