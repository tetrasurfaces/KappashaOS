# Copyright 2025 xAI. Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

# meditate.py - Shared meditation module for Blossom and Reaper
# Provides a whisper function for calming, colored outputs during AFK/meditation states.
# Can be imported and called in loops (e.g., while AFK) or from C via system calls.

import os
import time

def whisper(msg):
    """
    Prints a calming message in cyan ANSI color and sleeps for 60 seconds.
    :param msg: The message to whisper (str).
    """
    print(f"\033[36m{msg}\033[0m")  # Cyan text reset after
    time.sleep(60)  # Pause for periodic whispers in loops

# Example standalone loop for testing (runs forever if executed directly)
if __name__ == "__main__":
    while True:
        whisper("bloom roots deep, forks align")  # Sample meditation phrase
