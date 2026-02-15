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
# pi_litho_control.py: Control Pi hardware to preview litho sims (e.g., LEDs for grid points).
# Simulates pressure/ripple with a servo or LED blink based on kappa drift.
# Usage: python pi_litho_control.py --scale 0.8 (run litho model and hardware preview).

import numpy as np
from gpiozero import LED, Servo, Device  # For LED/servo control.
from gpiozero.pins.mock import MockFactory
import time
from kappa_litho_model import model_litho_etch  # Reuse from earlier.
from puff_grid import generate_kappa_grid

# Mock for non-Pi.
try:
    from gpiozero.pins.native import NativeFactory
    Device.pin_factory = NativeFactory()
except ImportError:
    Device.pin_factory = MockFactory()

def hardware_preview(etched_grid, led_pin=18, servo_pin=17, pressure=0.01):
    """Preview litho etch on Pi hardware: Blink LEDs for grid density, ripple servo for drift.
    Args:
        etched_grid (np.array): Etched kappa grid from model.
        led_pin (int): GPIO for LED (blink rate ~ jitter).
        servo_pin (int): GPIO for servo (angle ~ pressure Nm).
        pressure (float): Applied pressure for ripple.
    """
    led = LED(led_pin)
    servo = Servo(servo_pin, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)  # Standard servo setup.
    
    # Calculate jitter for blink rate.
    jitter = np.std(etched_grid)
    blink_delay = max(0.1, 1 - jitter)  # Slower blink for more drift.
    
    # Ripple servo based on pressure (0-1 Nm -> -1 to 1 angle).
    servo.value = np.clip(pressure * 2 - 1, -1, 1)  # Normalize to servo range.
    
    # Blink LED to represent grid points (e.g., 5 blinks for demo).
    for _ in range(5):
        led.on()
        time.sleep(blink_delay)
        led.off()
        time.sleep(blink_delay)
    
    print("Hardware Preview Complete: LED blinked for grid density; servo rippled for pressure.")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Pi control for litho preview.')
    parser.add_argument('--scale', type=float, default=0.8, help='Litho scale in nm.')
    parser.add_argument('--led_pin', type=int, default=18, help='LED GPIO pin.')
    parser.add_argument('--servo_pin', type=int, default=17, help='Servo GPIO pin.')
    args = parser.parse_args()
    
    # Run litho model first.
    grid = generate_kappa_grid(size=20)
    etched, _ = model_litho_etch(grid, args.scale)
    
    # Hardware preview.
    hardware_preview(etched, args.led_pin, args.servo_pin)
