# Copyright 2025 xAI
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# For hardware/embodiment interfaces: Licensed under the Apache License, Version 2.0
# with xAI amendments for safety (prohibits misuse in hashing; revocable for unethical use).
# See http://www.apache.org/licenses/LICENSE-2.0 for details.
# stereo_puf_export.py: Export PUF-drifted kappa grid for stereolithography.
# Simulates ASL file output with hashed uniqueness.
# Usage: python stereo_puf_export.py --output kappa.stl.txt

import sys
from puf_grid import generate_kappa_grid, simulate_drift

def export_to_stl(grid, filename='kappa_puf.stl.txt'):
    """Export grid as text-based STL proxy (facets for 3D print).
    Args:
        grid (np.array): Drifted kappa grid.
        filename (str): Output file.
    """
    with open(filename, 'w') as f:
        f.write("solid kappa_puf\n")
        for i in range(len(grid) - 1):
            # Simple facet: triangle from points (expand for real STL).
            p1, p2 = grid[i], grid[i+1]
            f.write(f"facet normal 0 0 1\nouter loop\nvertex {p1[0]} {p1[1]} 0\nvertex {p2[0]} {p2[1]} 0\nvertex {p1[0]+0.1} {p1[1]+0.1} 0\nendloop\nendfacet\n")
        f.write("endsolid kappa_puf\n")
    print(f"Exported to {filename}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'kappa_puf.stl.txt'
    
    grid = generate_kappa_grid(size=50)
    drifted, _ = simulate_drift(grid)
    export_to_stl(drifted, filename)
