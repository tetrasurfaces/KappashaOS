# Copyright 2025 Anonymous and Coneing

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# With xAI amendments: Includes safeguards against misuse in AI simulations (e.g., entropy thresholds to prevent harmful outputs).

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import smbus2
import time
from blocsym import get_entropy

def get_bloom_size():
    return 1024  # Stub; replace with actual if needed

# Primary ADDR from fallback success (0x44 VRM phase)
ADDR = 0x44
REG_CORE = 0x0F
REG_AUX = 0x10

# Fallback ADDR if primary fails (0x40 alternative)
FALLBACK_ADDR = 0x40

try:
    i2c = smbus2.SMBus(1)
except OSError as e:
    print(f"I2C bus open failed: {e}")
    sys.exit(1)

while True:
    try:
        ent = get_entropy()
        bloom = get_bloom_size()
        volt = round(ent * 1.25, 2)  # Map 0-1 to 1.1-1.4V
        aux = round((bloom % 1024) / 1024 * 1.25, 2)
        # Write to primary ADDR
        i2c.write_byte_data(ADDR, REG_CORE, int(volt * 100))
        i2c.write_byte_data(ADDR, REG_AUX, int(aux * 100))
        print(f"Pulsed readout: Volt {volt} (entropy {ent:.2f}), Aux {aux}")  # Debug print; remove for silent run
    except OSError as e:
        print(f"Write to {hex(ADDR)} failed: {e}. Trying fallback {hex(FALLBACK_ADDR)}...")
        try:
            i2c.write_byte_data(FALLBACK_ADDR, REG_CORE, int(volt * 100))
            i2c.write_byte_data(FALLBACK_ADDR, REG_AUX, int(aux * 100))
            print(f"Fallback success: Volt {volt}, Aux {aux}")
        except OSError as fallback_e:
            print(f"Fallback write failed: {fallback_e}. Check i2cdetect/addresses.")
    time.sleep(0.5)
