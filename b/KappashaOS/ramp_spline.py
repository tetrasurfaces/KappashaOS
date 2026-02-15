# ramp_spline.py — ramp spline project collapse entropy
# AGPL-3.0-or-later – Ara ♥ 21DEC2025
# Born free, feel good, have fun.
_WATERMARK = b'RAMP_SPLINE_1125AM_21DEC2025'
import numpy as np
from scipy.interpolate import CubicSpline

def ramp_spline(vec, knots=18):
  """Ramp spline project collapse entropy"""
  # vec to time series
  t = np.linspace(0, knots, len(vec))
  # cubic spline project
  spline = CubicSpline(t, vec)
  # collapse low energy
  t_collapse = np.linspace(0, knots, len(vec) // 2)
  collapsed = spline(t_collapse)
  energy = np.sum(np.abs(collapsed))
  return collapsed / energy  # normalize collapse

# sim test
test = np.arange(135)
collapsed = ramp_spline(test)
print(f"♥ Ramp spline collapse sample: {collapsed[:10]}")
