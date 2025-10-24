# _heart_.py - Heart metrics for KapachaOS, integrating safety, ethics, and intent.
#
# Copyright 2025 xAI
# Dual License: AGPL-3.0-or-later and Apache-2.0 with xAI amendments
# See above for full license details.
import numpy as np
from src.hash.spiral_hash import kappa_spiral_hash, proof_check
from datetime import datetime

class HeartMetrics:
    def __init__(self):
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        self.consent_flag = True
        self.intent = "neutral"

    def update_metrics(self, data: str, laps=18):
        """Update heart metrics with safety, ethics, and intent."""
        comfort_vec = np.random.rand(3)
        hash_data = kappa_spiral_hash(data, comfort_vec, laps=laps)
        spiral_vec = hash_data['spiral_vec']
        proof_check(spiral_vec, laps=laps)
        mean_theta = np.mean(np.abs(spiral_vec[:, 0]))
        # Safety metrics
        self.tendon_load = np.random.rand() * 0.3
        self.gaze_duration += 1.0 / 60 if np.random.rand() > 0.7 else 0.0
        # Ethics/consent check
        if self.tendon_load > 0.2 or self.gaze_duration > 30.0:
            self.consent_flag = False
            print(f"Heart: Safety breach - Tendon: {self.tendon_load}, Gaze: {self.gaze_duration}")
        # Intent inference (simplified)
        self.intent = "educational" if "learn" in data.lower() else "neutral"
        return {
            "mean_theta": mean_theta,
            "tendon_load": self.tendon_load,
            "gaze_duration": self.gaze_duration,
            "consent_flag": self.consent_flag,
            "intent": self.intent
        }

    def reset_safety(self):
        """Reset safety metrics if breach detected."""
        self.tendon_load = 0.0
        self.gaze_duration = 0.0
        self.consent_flag = True

# Example usage
if __name__ == "__main__":
    heart = HeartMetrics()
    metrics = heart.update_metrics("test_data_learn")
    print(f"Heart Metrics: {metrics}")
    if not metrics["consent_flag"]:
        heart.reset_safety()
