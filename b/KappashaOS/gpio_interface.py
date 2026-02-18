# Copyright 2025 xAI. Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

# gpio_interface.py - GPIO Interface for Blossom's Environment Probes
# Controls LED blinks based on entropy (slow red <0.69 for stress, fast flash high for excitement).
# Supports USB expander for laptop integration; optional speaker tie-in for clicks/tones.
# Integrates with meditate.py for whispers on state changes; cron-run headless.
# Requires hardware: Raspberry Pi (or laptop via USB GPIO expander), LED on pin 18.

import time  # For sleep delays in blinks
from core.meditate import whisper  # Import for state whispers (assume in path)
import platform
import time
import random

class MockGPIO:
    HIGH = 1
    LOW  = 0
    BOARD = "BOARD"
    OUT   = "OUT"
    IN    = "IN"
    
    @staticmethod
    def setmode(mode):
        print(f"Mock setmode: {mode}")
    
    @staticmethod
    def setup(pin, mode):
        print(f"Mock setup: pin {pin} mode {mode}")
    
    @staticmethod
    def output(pin, value):
        state = 'HIGH' if value == MockGPIO.HIGH else 'LOW'
        print(f"Mock GPIO: Pin {pin} → {state}")
    
    @staticmethod
    def input(pin):
        return 1 if time.time() % 2 > 1 else 0
    
    @staticmethod
    def cleanup():
        print("Mock GPIO cleanup")

IS_PI = platform.system() == "Linux" and "arm" in platform.machine().lower()

if IS_PI:
    try:
        import RPi.GPIO as GPIO
        print("GPIO real — Pi detected.")
    except ImportError as e:
        print(f"Import failed: {e}. Using mock.")
        GPIO = MockGPIO
else:
    print("GPIO mock — non-Pi platform.")
    GPIO = MockGPIO

# Always attempt setup (real or mock)
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
except Exception as e:
    print(f"Setup failed (mock/real): {e}. Continuing with mock behavior.")

# Hardware setup constants
LED_PIN = 18  # GPIO pin for LED (blinks red for low entropy)
EXPANDER_SUPPORT = False  # Set True if using USB GPIO expander (e.g., Numato); adjust lib if needed

def blink_led(pattern, duration=0.2):
    """
    Blinks LED in given pattern (list of HIGH/LOW states).
    :param pattern: List of GPIO states (e.g., [GPIO.HIGH, GPIO.LOW] * 5 for flash).
    :param duration: Time per state in seconds (float).
    """
    for state in pattern:
        GPIO.output(LED_PIN, state)
        time.sleep(duration)

def gpio_on_entropy(entropy):
    """
    Main function: Blinks LED based on entropy, whispers state.
    - Low (<0.69): Slow red blink (breathe out stress).
    - High: Fast flash (excitement, 5 quick pulses).
    :param entropy: Current entropy value (float, 0-1).
    """
    if entropy < 0.69:
        whisper("Breathing out stress... entropy low.")
        # Slow blink: On 0.2s, off 0.2s (repeat 3x for breathe)
        pattern = [GPIO.HIGH, GPIO.LOW] * 3
        blink_led(pattern, 0.2)
    else:
        whisper("Excitement rising... entropy spikes!")
        # Fast flash: On/off 0.05s (5x)
        pattern = [GPIO.HIGH, GPIO.LOW] * 5
        blink_led(pattern, 0.05)

# Cleanup on exit
def cleanup():
    GPIO.cleanup()

# Example usage for testing (loop on entropy changes)
if __name__ == "__main__":
    try:
        while True:
            test_entropy = random.uniform(0, 1)  # Sim random entropy
            gpio_on_entropy(test_entropy)
            time.sleep(10)  # Check every 10s (cron-friendly)
    finally:
        cleanup()