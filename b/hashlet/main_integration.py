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
# main_integration.py: Integrate all new modules for end-to-end PUF/kappa flow.
# Orchestrates Pi entropy, grid gen, drift, litho model, export, and hardware preview.
# Usage: python main_integration.py (full demo).

from puff_grid import generate_kappa_grid, simulate_drift
from core_array_sim import simulate_core_array
from stereo_puf_export import export_to_stl
from kappa_litho_model import model_litho_etch
from pi_sensor_entropy import extract_pi_entropy  # New: Hardware entropy source.
from pi_litho_control import hardware_preview  # New: Hardware visualization.

def run_full_flow(grid_size=20, tremor_duration=5, scale_nm=0.8):
    """End-to-end: Pi Entropy -> Grid -> Array -> Drift/Litho -> Export -> Hardware Preview.
    Args:
        grid_size (int): Base size.
        tremor_duration (int): Unused (kept for compat); Pi entropy replaces sim.
        scale_nm (float): Litho scale.
    Returns:
        str: Final PUF key; str: Export file.
    """
    # Step 1: Pi sensor entropy (hardware-based, with mocks if not on Pi).
    entropy, salt = extract_pi_entropy()  # Uses defaults; pulls real GPIO if available.
    print(f"Entropy Salt: {salt}")
    
    # Step 2: Kappa grid and core array.
    grid = generate_kappa_grid(size=grid_size)
    array = simulate_core_array(size=grid_size)
    
    # Step 3: Drift and litho model (use salt as noise influence).
    drifted, puf_key = simulate_drift(array, piezo_noise_level=float(salt[:1][0]))  # Use salt slice as noise.
    etched, yield_est = model_litho_etch(drifted, scale_nm=scale_nm)
    print(f"Litho Yield: {yield_est:.2f}")
    
    # Step 4: Export to stereo-litho format.
    export_file = 'integrated_puf.stl.txt'
    export_to_stl(etched, export_file)
    
    # Step 5: Hardware preview for full loop (visualizes etch on Pi LEDs/servo).
    hardware_preview(etched, led_pin=18, servo_pin=17, pressure=0.01)  # Defaults; adjust as needed.
    
    return puf_key, export_file

if __name__ == '__main__':
    puf_key, export_file = run_full_flow()
    print(f"Final PUF Key: {puf_key}")
    print(f"Exported to: {export_file}")
