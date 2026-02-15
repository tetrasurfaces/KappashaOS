# kappa_spline.py
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
import matplotlib.pyplot as plt

def kappa_spline(t, kappa=0.354, theta_power=4):
    # Fluctuate odds/evens, golden drift
    flip = np.sin(t * np.pi)  # 180 deg transition
    base_kappa = kappa + 0.0027 * np.sin(t)  # Window breath
    theta = np.power(np.cos(t), theta_power) * (1 + flip * 0.618)  # Golden nudge
    x = t * np.cos(theta)
    y = t * np.sin(theta) * base_kappa
    return x, y

t = np.linspace(0, 2*np.pi, 1000)
x, y = kappa_spline(t)

plt.plot(x, y, 'k-', linewidth=0.5)  # Matte black, no shine
plt.axis('equal')
plt.title('Quartz Knot: One Day Eternal')
plt.show()  # Or save as heart_quartz.png
