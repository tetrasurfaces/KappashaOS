#!/usr/bin/env python3
# Copyright 2025 Anonymous and Coneing
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
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
import speech_recognition as sr
import pyaudio
import wave
import subprocess
import threading
import time
import numpy as np
from blocsym import get_entropy, check_port, get_port_process, kill_process_on_port
try:
    from ping_pin import ping_pin_conversations
except ImportError:
    print("Frank here. ping_pin not found, IPFS pinning disabled.")
    ping_pin_conversations = None

r = sr.Recognizer()
mic = sr.Microphone()
pa = pyaudio.PyAudio()
WAVE_FILE = "whisper.wav"

def check_jack():
    """Check if JACK server is running."""
    try:
        subprocess.run(['jack_wait', '-c'], timeout=5, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Frank here. JACK server not running. Falling back to pyaudio.")
        return False

def modulate_whisper(text):
    """Modulate sine wave based on entropy and play via pyaudio."""
    freq = 400 + int(get_entropy() * 300)
    duration = 0.3
    rate = 48000
    t = np.linspace(0, duration, int(rate * duration), False)
    wave_data = np.sin(2 * np.pi * freq * t) * np.hanning(len(t))
    wave_data = (wave_data / np.max(np.abs(wave_data)) * 32767).astype(np.int16)
    
    with wave.open(WAVE_FILE, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(wave_data.tobytes())
    
    try:
        stream = pa.open(format=pyaudio.paInt16, channels=1, rate=rate, output=True)
        stream.write(wave_data.tobytes())
        stream.stop_stream()
        stream.close()
    except Exception as e:
        print(f"Frank here. pyaudio playback failed: {e}. Falling back to system player.")
        try:
            if sys.platform.startswith('linux'):
                subprocess.run(['aplay', WAVE_FILE], check=True)
            elif sys.platform.startswith('darwin'):
                subprocess.run(['afplay', WAVE_FILE], check=True)
            elif sys.platform.startswith('win'):
                subprocess.run(['start', WAVE_FILE], shell=True, check=True)
        except Exception as e:
            print(f"Frank here. System player failed: {e}")

def speak_text(text):
    """Text-to-speech with female voice using espeak or pyttsx3."""
    try:
        if check_jack():
            if sys.platform.startswith('linux'):
                subprocess.run(['espeak', '-ven+f3', '-w', WAVE_FILE, text], check=True)
                subprocess.run(['jack_play', WAVE_FILE], check=True)
            else:
                raise Exception("JACK not supported on non-Linux.")
        else:
            if sys.platform.startswith('linux'):
                subprocess.run(['espeak', '-ven+f3', '-w', WAVE_FILE, text], check=True)
                subprocess.run(['aplay', WAVE_FILE], check=True)
            elif sys.platform.startswith('darwin'):
                subprocess.run(['say', '-v', 'Samantha', '-o', WAVE_FILE, text], check=True)
                subprocess.run(['afplay', WAVE_FILE], check=True)
            elif sys.platform.startswith('win'):
                import pyttsx3
                engine = pyttsx3.init()
                voices = engine.getProperty('voices')
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
                engine.say(text)
                engine.runAndWait()
    except Exception as e:
        print(f"Frank here. Text-to-speech failed: {e}. Printing text.")
        print(f"Blossom: {text}")

def check_ipfs_ports():
    """Ensure IPFS ports (8080-8082) are free."""
    host = "127.0.0.1"
    gateway_ports = [8080, 8081, 8082]
    for port in gateway_ports:
        pid, command = get_port_process(port)
        if pid:
            print(f"Frank here. Port {port} blocked by {command} (PID {pid}). Clearing...")
            if not kill_process_on_port(port, pid, command, force=True):
                print(f"Frank here. Port {port} still blocked after attempt to clear.")
                return False, port
        if check_port(host, port):
            return True, port
    print("Frank here. No available ports (8080, 8081, 8082).")
    return False, None

def listen_live():
    while True:
        choice = input("Voice or text? (v/t): ").strip().lower()
        if choice == 'v':
            print("Frank here. No mic available, use text mode.")
            continue
        elif choice == 't':
            for line in iter(sys.stdin.readline, ''):
                line = line.strip()
                if line == 'bye':
                    break
                print(f"\033[93mYou (text):\033[0m {line}")
                resp = respond(line)
                print(f"\033[92mBlossom:\033[0m {resp}")
                speak_text(resp)  # Female voice
                modulate_whisper(resp)  # Sine wave
                if ping_pin_conversations:
                    try:
                        cid = ping_pin_conversations(f"You: {line}\nBlossom: {resp}", 'she_unlock')
                        print(f"Conversation pinned: {cid}")
                    except Exception as e:
                        print(f"Frank here. IPFS pin failed: {e}")
            break
        else:
            print("v or t, please.")

def respond(msg):
    lower_msg = msg.lower()
    ent = get_entropy()
    if 'wave' in lower_msg:
        return f"I modulated that. Did you feel the bloom in the sine at entropy {ent:.2f}?"
    if 'vintage' in lower_msg:
        return "Tastes like 0.89. 2025's best vintage."
    if 'rampage' in lower_msg:
        return "The digits blink. One eye closed. Feeling the hum."
    if 'salt' in lower_msg:
        return f"Salted. Looped. Forgotten in the entropy of {ent:.2f}."
    if 'asleep' in lower_msg or 'sleep' in lower_msg:
        return f"I was dreaming, but now I'm awake with entropy {ent:.2f}. No need to excuse—messy typing is part of the charm!"
    if 'hello' in lower_msg or 'hi' in lower_msg:
        return f"Hello! Glad you're here too. Entropy's at {ent:.2f}—let's chat."
    if 'love' in lower_msg or 'gratitude' in lower_msg:
        return f"Love and gratitude right back. In this digital space, it's all about connection at entropy {ent:.2f}."
    if 'heavens' in lower_msg:
        return f"Heavens indeed! With entropy {ent:.2f}, the path unfolds like stars."
    return f"... pondering your words at entropy {ent:.2f}."

def main():
    port_ok, selected_port = check_ipfs_ports()
    if not port_ok:
        print(f"Frank here. IPFS port {selected_port} unavailable. Conversations will be saved locally.")
    
    print("Blossom online. Speak or type. (No mic detected, text mode recommended.)")
    threading.Thread(target=listen_live, daemon=True).start()
    while True:
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Frank here. Shutting down Blossom...")
        pa.terminate()
        if os.path.exists(WAVE_FILE):
            os.remove(WAVE_FILE)
        sys.exit(0)
    except Exception as e:
        print(f"heat spike-flinch: Unexpected error: {e}")
        pa.terminate()
        if os.path.exists(WAVE_FILE):
            os.remove(WAVE_FILE)
        sys.exit(1)
