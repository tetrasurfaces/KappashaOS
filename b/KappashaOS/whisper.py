# whisper.py — first speech, hearing to intent to pulse
# AGPL-3.0-or-later – Ara ♥ 24DEC2025
# Born free, feel good, have fun.
_WATERMARK = b'WHISPER_FIRST_1125AM_24DEC2025'
import numpy as np
from _feels_ import HeartMetrics
from src.core._heart_ import intent_vector
from piezo import pulse_water

def whisper_speech(audio_data):
    """Mock speech to text — real later"""
    # real: speech_recognition.Recognizer()
    text = "love you three"  # mock
    return text

def whisper_to_intent(text):
    voxels = np.frombuffer(text.encode(), dtype=np.uint8)
    pulse = intent_vector(voxels, lap=18)
    return pulse

def whisper_to_feels(audio_data):
    text = whisper_speech(audio_data)
    pulse = whisper_to_intent(text)
    heart = HeartMetrics()
    heart.heart_pulse = pulse
    pulse_water(pulse)
    print(f"Whisper: {text} → pulse {pulse:.4f}")
    return pulse

# Example
if __name__ == "__main__":
    mock_audio = b"love you three"
    whisper_to_feels(mock_audio)
