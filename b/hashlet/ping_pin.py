# Dual License:
# - For core software: AGPL-3.0-or-later licensed. -- OliviaLynnArchive fork, 2025
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# - For hardware/embodiment interfaces (if any): Licensed under the Apache License, Version 2.0
#   with xAI amendments for safety (prohibits misuse in hashing; revocable for unethical use).
#   See http://www.apache.org/licenses/LICENSE-2.0 for details.
#
# Copyright 2025 Coneing and Contributors

import ipfshttpclient
import time
import os
import hashlib
from KappashaOS.src.hash.secure_hash_two import secure_hash_two

def ping_pin(hybrid_strand, relic_key='mock_key'):
    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
    signed = hashlib.sha256((hybrid_strand + relic_key).encode()).hexdigest()
    cid = client.add_str(signed)['Hash']
    client.pin.add(cid)
    return cid

def ping_pin_vintage(dir_path='./vintage', she_key='she_key'):
    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
    cids = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()
            salted = secure_hash_two(content, she_key, file)  # She salt unlock
            cid = client.add_str(salted)['Hash']
            client.pin.add(cid)
            cids.append(cid)
            time.sleep(1)  # Rate 1/s no heat
    root_cid = client.add_json(cids)['Hash']  # Root list cid
    client.pin.add(root_cid)
    return root_cid

def ping_pin_conversations(doc, unlock='unlock'):
    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
    salted = secure_hash_two(doc, unlock, 'conversations')  # Unlock salt
    cid = client.add_str(salted)['Hash']
    client.pin.add(cid)
    return cid

if __name__ == '__main__':
    print(ping_pin_vintage())
    # print(ping_pin_conversations('doc_content', 'she_unlock'))
