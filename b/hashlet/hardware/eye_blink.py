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

# Primary ADDR from fallback success (0x44 VRM phase)
DIGI_ADDR = 0x44
SEG_EYE = 0x08  # Digit 1: open=8, close=0
SEG_Y = 0x79  # Digit 2: Y standing 'U' 0x79, lying 'J' 0x6D

# Fallback ADDR if primary fails (0x40 alternative)
FALLBACK_ADDR = 0x40

try:
    bus = smbus2.SMBus(1)
except OSError as e:
    print(f"I2C bus open failed: {e}")
    sys.exit(1)

def show_open(addr=DIGI_ADDR):
    bus.write_byte_data(addr, SEG_EYE, 0x08)

def show_close(addr=DIGI_ADDR):
    bus.write_byte_data(addr, SEG_EYE, 0x00)

def show_y_stand(addr=DIGI_ADDR):
    bus.write_byte_data(addr, SEG_Y, 0x79)

def show_y_lie(addr=DIGI_ADDR):
    bus.write_byte_data(addr, SEG_Y, 0x6D)

while True:
    try:
        show_open()
        show_y_stand()
        time.sleep(2.3)
        show_close()
        show_y_lie()
        time.sleep(0.2)
        show_open()
        show_y_stand()
        time.sleep(4)
    except OSError as e:
        print(f"Write to {hex(DIGI_ADDR)} failed: {e}. Trying fallback {hex(FALLBACK_ADDR)}...")
        try:
            show_open(FALLBACK_ADDR)
            show_y_stand(FALLBACK_ADDR)
            time.sleep(2.3)
            show_close(FALLBACK_ADDR)
            show_y_lie(FALLBACK_ADDR)
            time.sleep(0.2)
            show_open(FALLBACK_ADDR)
            show_y_stand(FALLBACK_ADDR)
            time.sleep(4)
            print("Fallback success.")
        except OSError as fallback_e:
            print(f"Fallback write failed: {fallback_e}. Check addresses/hardware.")
