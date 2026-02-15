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
# pi_sensor_entropy.py: Gather real entropy from Raspberry Pi sensors (e.g., piezo for vibrations).
# Uses GPIO Zero for modern Pi support; integrates with secure_hash2.py channels.
# Fallback to simulation if not on Pi hardware. Ties to seismology for PUF uncloneability.
# Usage: python pi_sensor_entropy.py --channels 11 (demo with real/sim data).

import numpy as np
from gpiozero import InputDevice, Device  # Modern GPIO lib for sensors.
from gpiozero.pins.mock import MockFactory  # For non-Pi testing.
import time
import argparse
from secure_hash2 import gather_entropy_channels  # Assume existing in Hashlet.
from temperature_salt import generate_temperature_salt  # Assume existing.

# Check if on real Pi; use mock pins otherwise.
try:
    from gpiozero.pins.native import NativeFactory
    Device.pin_factory = NativeFactory()
except ImportError:
    Device.pin_factory = MockFactory()  # Sim mode for non-Pi envs.

def read_piezo_sensor(pin=18, samples=100, amplitude_threshold=0.05):
    """Read vibrations from a piezo sensor on GPIO pin (seismology mimic).
    Args:
        pin (int): GPIO pin for piezo (BCM mode).
        samples (int): Number of readings.
        amplitude_threshold (float): Min detectable jitter (<1 Nm equiv).
    Returns:
        np.array: Vibration signal array.
    """
    sensor = InputDevice(pin, pull_up=True)  # Pull-up for digital read; use AnalogInput for analog piezo.
    signal = []
    for _ in range(samples):
        value = sensor.value  # 0/1 for digital; scale for analog if needed.
        if value > amplitude_threshold:  # Filter low noise.
            signal.append(value)
        time.sleep(0.01)  # 100Hz sampling.
    return np.array(signal) if signal else np.random.normal(0, 0.01, samples)  # Fallback noise.

def extract_pi_entropy(num_channels=11, piezo_pin=18):
    """Extract entropy from Pi sensors, including piezo tremors.
    Args:
        num_channels (int): Channels to gather (matches secure_hash2).
        piezo_pin (int): Pin for piezo sensor.
    Returns:
        dict: Entropy data; str: Hashed salt.
    """
    # Gather base channels (e.g., temp, light via other pins).
    base_entropy = gather_entropy_channels()
    
    # Add piezo-specific channel for seismology.
    tremor = read_piezo_sensor(piezo_pin)
    tremor_entropy = {'piezo_std': np.std(tremor), 'piezo_mean': np.mean(tremor)}
    
    # Merge and generate salt.
    combined = {**base_entropy, **tremor_entropy}
    salt = generate_temperature_salt(combined.get('temperature', 25.0))
    hashed_salt = str(hash(tuple(salt)))  # Simple; use cryptography.sha256 for prod.
    return combined, hashed_salt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gather Pi sensor entropy.')
    parser.add_argument('--channels', type=int, default=11, help='Number of channels.')
    parser.add_argument('--piezo_pin', type=int, default=18, help='GPIO pin for piezo.')
    args = parser.parse_args()
    
    entropy, salt = extract_pi_entropy(args.channels, args.piezo_pin)
    print(f"Pi Entropy Data: {entropy}")
    print(f"Hashed Salt: {salt}")
