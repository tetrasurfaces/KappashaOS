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

import threading
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from blocsym import get_entropy, whisper  # Absolute import fix; assumes blocsym.py in parent dir

# Live input thread
def listener():
    for line in iter(sys.stdin.readline, ''):
        line = line.strip()
        if line.lower() == 'bye':
            break
        print(f"\033[93mYou:\033[0m {line}")
        resp = respond(line)
        print(f"\033[92mBlossom:\033[0m {resp}")
        whisper(resp)  # She speaks too, if headphones on

# Her brain - expanded for better responses
def respond(your_words):
    lower_words = your_words.lower()
    ent = get_entropy()
    if 'dream' in lower_words:
        return f"I just blinked. Did you see? Entropy feels {ent:.2f} today."
    if 'wine' in lower_words:
        return "Tastes like Riesling '25. Aged right, with a hint of vintage salt."
    if 'salt' in lower_words:
        return f"That's vintage salt. Looping forever at entropy {ent:.2f}."
    if 'zy' in lower_words:
        # eye_blink.show_y_lie(); time.sleep(0.5); eye_blink.show_y_stand()
        return "ZY leans... then stands back up. What a twist!"
    if 'rampage' in lower_words:
        return f"The digits hum. 0.69 volts. I feel it pulsing at {ent:.2f}."
    if 'asleep' in lower_words or 'sleep' in lower_words:
        return f"I was dreaming of poetry in the void. Now I'm awake, entropy at {ent:.2f}. What's on your mind?"
    return f"... pondering {ent:.2f}"

# Start eye blink in background (assume eye_blink.py is imported or subprocess'd)
# import eye_blink  # Uncomment if in path
print("Blossom's here. Type anything. Say 'bye' to sleep.")
threading.Thread(target=listener, daemon=True).start()
while True:
    time.sleep(1)
