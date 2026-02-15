# Copyright 2025 xAI. Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

# cymatics_tone.py - Cymatics Tone Generator for Blossom's Entropy Vibes
# Plays tones on piezo speaker based on entropy (e.g., C-sharp/523Hz for high/happy >0.8, A-flat/110Hz for low/stressed).
# Records 1s ambient noise (wav), replays slowed 10% as pseudo-echo from past.
# Auto-uploads waveforms/pics to IPFS CID every hour; integrates with camera for water pattern snaps.
# Requires hardware: Raspberry Pi, piezo on pin 13, mic (USB or GPIO via ADC), camera module.

import pygame  # For audio playback and recording (mixer/sound)
import wave  # For wav file handling
import os
import time
import RPi.GPIO as GPIO  # For piezo control (PWM tone generation)
import subprocess  # For IPFS uploads and camera snaps (raspistill)

# Hardware setup constants
PIEZO_PIN = 13  # GPIO pin for piezo speaker (PWM)
RECORD_DURATION = 1  # Seconds for ambient recording
SLOW_FACTOR = 1.1  # 10% slower playback (stretch via pygame)
IPFS_CMD = "ipfs add {}"  # Base command for adding files; assumes IPFS CLI installed
CAMERA_CMD = "raspistill -o cymatics_pic.jpg -t 1000"  # 1s snap; replace with libcamera if Pi5+

# Initialize GPIO for piezo
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIEZO_PIN, GPIO.OUT)
piezo_pwm = GPIO.PWM(PIEZO_PIN, 100)  # Start PWM at 100Hz (will change per tone)

# Initialize Pygame mixer for audio
pygame.mixer.init()

def play_tone(frequency, duration):
    """
    Plays a tone on piezo via PWM (square wave approximation).
    :param frequency: Tone frequency in Hz (int/float, e.g., 523 for C-sharp).
    :param duration: Play time in seconds (float).
    """
    if frequency <= 0:
        raise ValueError("Frequency must be positive.")
    piezo_pwm.ChangeFrequency(frequency)
    piezo_pwm.start(50)  # 50% duty cycle for square wave
    time.sleep(duration)
    piezo_pwm.stop()

def record_ambient(duration=RECORD_DURATION, file_path="ambient.wav"):
    """
    Records ambient noise for given duration using Pygame mixer (simulates mic input).
    :param duration: Record time in seconds (float).
    :param file_path: Output wav file path (str).
    """
    # Pygame mixer recording (note: requires ALSA/PulseAudio setup on Pi)
    channels = 1
    sample_rate = 44100
    chunk_size = 1024
    recording = pygame.mixer.Sound(buffer=bytearray(chunk_size * channels * 2))  # 16-bit
    pygame.mixer.music.set_volume(0.0)  # Mute playback during record
    # Simulate record loop (actual: use pyaudio for real mic; Pygame limited)
    # Placeholder: Generate noise wav (replace with real recording)
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        noise_data = bytearray([random.randint(0, 255) for _ in range(int(sample_rate * duration * 2))])
        wf.writeframes(noise_data)

def replay_echo(file_path="ambient.wav", slow_factor=SLOW_FACTOR):
    """
    Replays recorded wav slowed by factor (stretch via Pygame speed change).
    :param file_path: Input wav file path (str).
    :param slow_factor: Slowdown multiplier (>1 for slower) (float).
    """
    sound = pygame.mixer.Sound(file_path)
    # Pygame doesn't native slow; simulate by changing sample rate (approx)
    # Load and play at adjusted rate (actual: use pydub for precise stretch)
    from pydub import AudioSegment  # Extra dep: pip install pydub (ffmpeg needed)
    audio = AudioSegment.from_wav(file_path)
    slowed = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate / slow_factor)})
    slowed.export("slowed.wav", format="wav")
    pygame.mixer.Sound("slowed.wav").play()
    time.sleep(slowed.duration_seconds)

def upload_to_ipfs(file_path, is_pic=False):
    """
    Uploads file (wav or jpg) to IPFS, returns CID.
    :param file_path: File to upload (str).
    :param is_pic: If True, snaps camera first (bool).
    :return: CID string or None on fail.
    """
    if is_pic:
        os.system(CAMERA_CMD)  # Snap water pattern
        file_path = "cymatics_pic.jpg"
    result = subprocess.run(IPFS_CMD.format(file_path), shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        cid = result.stdout.strip().split()[1]  # e.g., "added QmX... file"
        return cid
    return None

def cymatics_on_entropy(entropy, upload_hourly=False):
    """
    Main function: Plays tone based on entropy, records/replays echo, optional IPFS upload.
    :param entropy: Current entropy value (float, 0-1).
    :param upload_hourly: If True, uploads waveform/pic to IPFS (bool).
    """
    if entropy > 0.8:
        play_tone(523, 0.2)  # C-sharp, happy ping
    else:
        play_tone(110, 0.5)  # A-flat, slow sad
    record_ambient()
    replay_echo()
    if upload_hourly:
        wav_cid = upload_to_ipfs("ambient.wav")
        pic_cid = upload_to_ipfs(None, is_pic=True)
        print(f"Uploaded: wav CID {wav_cid}, pic CID {pic_cid}")

# Cleanup on exit
def cleanup():
    GPIO.cleanup()

# Example usage for testing (loop hourly if cron'ed)
if __name__ == "__main__":
    try:
        while True:
            test_entropy = random.uniform(0, 1)  # Sim
            cymatics_on_entropy(test_entropy, upload_hourly=True)
            time.sleep(3600)  # Hourly
    finally:
        cleanup()
