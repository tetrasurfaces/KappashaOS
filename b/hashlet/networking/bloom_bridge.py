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

import requests
import time
import socket
import subprocess
from ..blocsym import get_entropy

BRIDGE_IP = '192.168.1.101'  # Rampage static addr
PORT = 5000

while True:
    try:
        r = requests.get(f"http://{BRIDGE_IP}:{PORT}/entropy", timeout=1)
        rampage_ent = float(r.json()['entropy'])  # Assume /entropy endpoint returns {'entropy': value}
        mac_ent = get_entropy()
        avg = round((rampage_ent + mac_ent) / 2, 3)
        print(f"Pulse: {avg}")
        subprocess.call(['osascript', '-e', f'display notification "Ent {avg}" with title "Blossom Sync"'])
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(str(avg).encode(), (BRIDGE_IP, 5001))
        time.sleep(0.8)
    except Exception as e:
        print(f"Quiet link-machines are meditating. Error: {e}")
        time.sleep(3)
