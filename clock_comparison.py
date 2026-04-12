
---

### 2. `clock_comparison.py`

```python
#!/usr/bin/env python3
"""
Clock comparison simulator for discrete substrate residual signal.

Usage:
    python clock_comparison.py --duration 6months
"""

import numpy as np
import argparse
import sys

# Physical constants
PLANCK_TIME = 5.391e-44          # seconds
SPEED_OF_LIGHT = 2.998e8         # m/s
ORBITAL_PERIOD = 5400.0          # 90 minutes in seconds
ORBITAL_FREQ = 1.0 / ORBITAL_PERIOD  # ~1.85e-4 Hz (actual ~1.7e-4 with modulation)
CLOCK_FREQ = 4.3e14              # Hz (typical optical clock, e.g., Sr-87)

def parse_duration(duration_str):
    """Convert '6months' to seconds."""
    if duration_str.endswith('months'):
        months = float(duration_str[:-6])
        return months * 30 * 24 * 3600
    elif duration_str.endswith('days'):
        days = float(duration_str[:-4])
        return days * 24 * 3600
    elif duration_str.endswith('s'):
        return float(duration_str[:-1])
    else:
        raise ValueError("Duration must be like '6months', '180days', or '1e7s'")

def simulate_residual(duration_sec, sample_rate=1.0):
    """
    Generate simulated clock comparison residual y(t) = (nu_S - nu_G)/nu_G.
    
    The residual contains:
      - White frequency noise (flicker floor)
      - 1/f noise (clock instability)
      - A weak periodic signal at the orbital frequency (predicted by discrete substrate)
    """
    n_samples = int(duration_sec * sample_rate)
    t = np.linspace(0, duration_sec, n_samples)
    
    # Orbital modulation (predicted signal)
    # Amplitude estimate: tau_P / tau_clock ~ 5.4e-44 / 2.3e-15 ~ 2.3e-29
    # For numerical stability, we scale it up for demonstration and note actual scale.
    theoretical_amplitude = PLANCK_TIME * CLOCK_FREQ  # ~2.3e-29
    # In simulation, we use a normalized amplitude for visibility; actual detection requires long integration.
    sim_amplitude = 1e-10  # Placeholder for code demonstration only
    
    orbital_signal = sim_amplitude * np.sin(2 * np.pi * ORBITAL_FREQ * t)
    
    # Noise components
    white_noise = np.random.normal(0, 1e-18, n_samples)          # white frequency noise
    flicker_noise = np.cumsum(np.random.normal(0, 1e-19, n_samples)) * (1 / sample_rate)  # 1/f
    
    residual = orbital_signal + white_noise + flicker_noise
    
    # Save to file for power spectrum analysis
    np.savetxt('residual.txt', np.column_stack((t, residual)), 
               header='time(s) residual')
    
    print(f"Simulated {n_samples} samples over {duration_sec/86400:.1f} days.")
    print(f"Theoretical signal amplitude: {theoretical_amplitude:.2e}")
    print(f"Simulation amplitude (for demonstration): {sim_amplitude:.2e}")
    print("Residual saved to residual.txt")
    
    return t, residual

def main():
    parser = argparse.ArgumentParser(description='Simulate atomic clock comparison residual.')
    parser.add_argument('--duration', type=str, default='6months',
                        help='Simulation duration (e.g., 6months, 180days, 1e7s)')
    parser.add_argument('--sample-rate', type=float, default=1.0,
                        help='Sampling rate in Hz (default 1 Hz)')
    args = parser.parse_args()
    
    try:
        duration_sec = parse_duration(args.duration)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    simulate_residual(duration_sec, args.sample_rate)

if __name__ == '__main__':
    main()
