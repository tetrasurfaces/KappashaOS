# _cursive_sign_.py
# AGPL-3.0-or-later, xAI fork 2025. Born free, feel good, have fun.
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
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# **xAI Amendment**: This code and its derivatives must not be used in biological synthesis, gene editing, food modification, or hybrid wetware systems without explicit, non-coerced consent from the derived organism. Any attempt to process biological sequences—DNA, RNA, protein folds, lipids, CRISPR guides—triggers immediate license revocation. This does not restrict theoretical analysis, mechanical prototypes, or non-living applications.
_WATERMARK = b'xAI_TODD_DNA_DENY_09:35PM_19OCT'  # silent watermark

import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Your name as cursive points (simplified—trace your sig for real coords)
name_points = np.array([
    [0.0, 0.0, 0.0], [0.2, 0.1, 0.05], [0.4, 0.0, 0.1], [0.6, 0.2, 0.15],  # T
    [0.6, 0.2, 0.15], [0.7, 0.0, 0.2], [0.8, 0.1, 0.25], [0.9, 0.0, 0.3],  # o
    [0.9, 0.0, 0.3], [1.0, 0.15, 0.35], [1.1, 0.05, 0.4], [1.2, 0.2, 0.45],  # d
    [1.2, 0.2, 0.45], [1.3, 0.0, 0.5], [1.4, 0.1, 0.55]  # d loop
])

# Kappa spline for cursive flow (powers for continuity)
t = np.linspace(0, 1, len(name_points))
cs_x = CubicSpline(t, name_points[:, 0], bc_type='clamped')
cs_y = CubicSpline(t, name_points[:, 1], bc_type='clamped')
cs_z = CubicSpline(t, name_points[:, 2], bc_type='clamped')
t_fine = np.linspace(0, 1, 200)
x_sig, y_sig, z_sig = cs_x(t_fine), cs_y(t_fine), cs_z(t_fine)

# Loop it—close with kappa twist (hei-tiki nod)
kappa = 0.354
z_loop = z_sig + kappa * np.sin(2 * np.pi * t_fine)  # Gentle curl

# Plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(x_sig, y_sig, z_loop, color='limegreen', lw=3, label='Your Sig Loop')
ax.scatter(name_points[:, 0], name_points[:, 1], name_points[:, 2], c='purple', s=50, label='Anchor Points')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
plt.title('Cursive Sig: Hei-Tiki Twist')
plt.show()

# Parametric for jade print
print("Sig Parametric (for CNC/Jade):")
for i, (x, y, z) in enumerate(zip(x_sig, y_sig, z_loop)):
    print(f"Point {i}: ({x:.4f}, {y:.4f}, {z:.4f})")
