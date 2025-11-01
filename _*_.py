#!/usr/bin/env python3
# _*_.py - Postcard Def Cmd for KappashaOS
# AGPL-3.0-or-later, xAI fork 2025
# Goal: Def cmd for sig-curve postcards, mocking frag gaze logic. Wildcard for bloom.
# Usage: python _*_.py --sig-curve [kappa|purple|green] --gaze [0.99] --keyed [0/1] [--output frag|png]
# Outputs GLSL snippet or matplotlib PNG mock.
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
# Born Free. Feel Good. Have Fun.
#
# **xAI Amendment**: This code and its derivatives must not be used in biological synthesis, gene editing, food modification, or hybrid wetware systems without explicit, non-coerced consent from the derived organism. Any attempt to process biological sequences—DNA, RNA, protein folds, lipids, CRISPR guides—triggers immediate license revocation. This does not restrict theoretical analysis, mechanical prototypes, or non-living applications.
_WATERMARK = b'xAI_TODD_DNA_DENY_09:35PM_19OCT'  # silent watermark

import argparse
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from typing import Optional

# Constants from postcard.frag
GAZE_THRESHOLD = 0.99

def generate_sig_curve(curve_type: str = 'kappa', num_points: int = 1000) -> np.ndarray:
    """Generate sig curve (kappa spiral or color variant)."""
    t = np.linspace(0, 2 * np.pi, num_points)
    if curve_type == 'kappa':
        kappa_base = 0.3536
        r = np.exp(kappa_base * t) / 10
        x = r * np.cos(t)
        y = r * np.sin(t)
    elif curve_type == 'purple':
        # Purple twist: sin modulation for that 'us' glow
        r = np.sin(t * 1.618) + 1
        x = r * np.cos(t + np.pi / 4)
        y = r * np.sin(t + np.pi / 4)
    else:  # green
        r = np.sin(t * 2)
        x = r * np.cos(t)
        y = r * np.sin(t)
    return np.column_stack([x, y])

def mock_frag_logic(curve: np.ndarray, gaze: np.ndarray, keyed: int) -> np.ndarray:
    """Mock postcard.frag: green if keyed gaze hits, red otherwise."""
    # Simulate uv coords as curve params
    uv = curve / np.max(np.abs(curve), axis=0)  # Normalize to [0,1]
    # Gaze dot product
    dot_prod = np.dot(uv, gaze)
    # Frag logic
    color = np.where(dot_prod > GAZE_THRESHOLD and keyed == 1, [0, 1, 0], [1, 0, 0])
    return color  # RGBA-ish, alpha=1

def render_postcard(curve: np.ndarray, gaze: np.ndarray, keyed: int, output: str = 'frag') -> Optional[str]:
    """Render postcard: frag snippet or PNG base64."""
    if output == 'frag':
        # Emit GLSL mock
        frag_code = f"""
uniform vec2 gaze = vec2({gaze[0]}, {gaze[1]}); // Your gaze
uniform int keyed = {keyed}; // Bloom if true
void main() {{
    vec2 uv = gl_FragCoord.xy / resolution; // Curve norm
    if (dot(gaze, uv) > {GAZE_THRESHOLD} && keyed == 1) {{
        gl_FragColor = vec4(0, 1, 0, 1); // Green bloom
    }} else {{
        gl_FragColor = vec4(1, 0, 0, 1); // Red unread
    }}
}}
"""
        return frag_code
    else:  # png
        # Matplotlib mock: plot curve, color points per frag logic
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(curve[:, 0], curve[:, 1], 'k-', alpha=0.5)
        colors = mock_frag_logic(curve, gaze, keyed)
        scatter = ax.scatter(curve[:, 0], curve[:, 1], c=colors, s=10, alpha=0.8)
        ax.set_title('Coning Postcard Bloom')
        ax.axis('off')
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', facecolor='black', edgecolor='none')
        buf.seek(0)
        img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close(fig)
        return f"data:image/png;base64,{img_b64}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coning Postcard Def Cmd")
    parser.add_argument('--sig-curve', default='kappa', choices=['kappa', 'purple', 'green'], help="Curve type")
    parser.add_argument('--gaze', nargs=2, type=float, default=[0.99, 0.99], help="Gaze vector [x y]")
    parser.add_argument('--keyed', type=int, default=1, choices=[0, 1], help="Keyed state (1=bloom)")
    parser.add_argument('--output', default='frag', choices=['frag', 'png'], help="Output type")
    args = parser.parse_args()

    curve = generate_sig_curve(args.sig_curve)
    gaze_vec = np.array(args.gaze)
    result = render_postcard(curve, gaze_vec, args.keyed, args.output)

    if args.output == 'frag':
        print(result)
    else:
        print(result)  # Base64 PNG - copy to browser

    print("Coning postcard rendered. Blooming for you <3")
