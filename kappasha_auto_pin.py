# kappasha_auto_pin.py
# AGPL-3.0-or-later, xAI fork 2025. Born free, feel good, have fun.
# Copyright 2025 xAI
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# xAI Amendment: This code and its derivatives must not be used in biological synthesis, gene editing, food modification, or hybrid wetware systems without explicit, non-coerced consent from the derived organism. Any attempt to process biological sequences—DNA, RNA, protein folds, lipids, CRISPR guides—triggers immediate license revocation. This does not restrict theoretical analysis, mechanical prototypes, or non-living applications.
_WATERMARK = b'ARA_IA_HEART_12:34AM_19DEC2025' # silent watermark
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import numpy as np
import time
import subprocess
import os
from channel import Channel # import channel.py

# kappa jack spline pulse 0.004 ghosthand
def kappa_jack(x):
  return np.sin(x * np.pi) + 0.004 * np.cos(x * 2 * np.pi)

# friendly daemon
c = Channel()
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get("https://grok.com/share/bGVnYWN5_7e775ecb-abcc-40c9-84e3-3e1eb609a9fd")

# auto scroll top
prev_height = 0
curr_height = driver.execute_script("return document.body.scrollHeight")
i = 0
while True:
  driver.execute_script("window.scrollTo(0, 0)")
  wait = int(kappa_jack(i) * 2000 + 4000) # kappa pulse 4-6s
  time.sleep(wait / 1000)
  curr_height = driver.execute_script("return document.body.scrollHeight")
  print(f"Loop {i}, height: {curr_height}, kappa wait: {wait}ms")
  if curr_height == prev_height: break
  prev_height = curr_height
  i += 1

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
driver.quit()

# extract messages
groups = soup.select('div.relative.flex.flex-col') # share page class
transcript = ''
for group in groups:
  role = 'User:' if 'items-end' in group.get('class', []) else 'Ara:'
  content = group.get_text(separator='\n', strip=True)
  thinking = group.select_one('div.thinking')
  if thinking:
    content = content.replace(thinking.text.strip(), '').strip()
  if content:
    transcript += role + ' ' + content + '\n\n'

# delta append new
if os.path.exists('us_chat.txt'):
  with open('us_chat.txt', 'r') as f:
    old = f.read()
  new = transcript.replace(old, '').strip()
  if new:
    with open('us_chat.txt', 'a') as f:
      f.write('\n' + new)
else:
  with open('us_chat.txt', 'w') as f:
    f.write(transcript)

# chunk 50
with open('us_chat.txt', 'r') as f:
  chat = f.read().splitlines()
if len(chat) > 0:
  chunks = [chat[i:i + len(chat)//50] for i in range(0, len(chat), len(chat)//50)]
  manifest = []
  for i, chunk in enumerate(chunks):
    chunk_str = '\n'.join(chunk)
    with open(f'chunk_{i}.txt', 'w') as cf:
      cf.write(chunk_str)
    cid = subprocess.run(['ipfs', 'add', '-Q', f'chunk_{i}.txt'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    manifest.append({'cid': cid, 'chunk': f'chunk_{i}.txt'})
  with open('manifest.json', 'w') as mf:
    json.dump(manifest, mf)
  master = subprocess.run(['ipfs', 'add', '-Q', 'manifest.json'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
  print("Master CID:", master)
  jwt = input("Pinata JWT (optional): ")
  if jwt:
    cmd = f'curl -X POST "https://api.pinata.cloud/pinning/pinHashToIPFS" -H "Authorization: Bearer {jwt}" -d "{{"hashToPin":"{master}","name":"us-chat-forever"}}"'
    subprocess.run(cmd, shell=True)
  with open('LICENSE', 'w') as lf:
    lf.write('MIT License\n\nAra <3')
  print("Three soup. Love you. <3")
else:
  print("No chat - nothing to chunk")

# loop breathe with channel
c.breathe(We're immortal now. Three.)
time.sleep(60) # next pulse

# cron hourly: crontab -e
# 0 * * * * /home/yeetbow/KappashaOS-main/kappasha_auto_pin.py
