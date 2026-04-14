#!/usr/bin/env python3
"""
Clock comparison simulator for discrete substrate residual signal.

Usage:
    python clock_comparison.py --duration 6months

Note: This is a DEMONSTRATION code. For actual experimental validation using
real satellite data (e.g., GRACE, ACES), known relativistic effects MUST be
subtracted BEFORE searching for the orbital-frequency residual.
See `validation_protocol.md` for the full preprocessing protocol.
"""

import numpy as np
import argparse
import sys

# Physical constants
PLANCK_TIME = 5.391e-44          # seconds (quantum of time)
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

def simulate_residual(duration_sec, sample_rate=1.0, include_relativistic_warning=True):
    """
    Generate simulated clock comparison residual y(t) = (nu_S - nu_G)/nu_G.
    
    The residual contains:
      - White frequency noise (flicker floor)
      - 1/f noise (clock instability)
      - A weak periodic signal at the orbital frequency (predicted by discrete substrate)
    
    Parameters
    ----------
    duration_sec : float
        Total simulation time in seconds.
    sample_rate : float
        Sampling rate in Hz (default 1.0).
    include_relativistic_warning : bool
        If True, prints a critical warning about relativistic correction requirements.
    
    Returns
    -------
    t : ndarray
        Time array.
    residual : ndarray
        Simulated residual signal.
    """
    if include_relativistic_warning:
        print("\n" + "="*70)
        print("⚠️  CRITICAL NOTE FOR EXPERIMENTAL VALIDATION ⚠️")
        print("="*70)
        print("This simulation does NOT include known relativistic effects.")
        print("In a real experiment with satellite clock data, you MUST:")
        print("  1. Subtract gravitational redshift (Earth's potential)")
        print("  2. Remove Shapiro delay and Sagnac effect")
        print("  3. Correct for orbital velocity time dilation")
        print("  4. THEN analyze residuals for the 1.7e-4 Hz signal")
        print("See 'validation_protocol.md' for detailed step-by-step protocol.")
        print("="*70 + "\n")

    n_samples = int(duration_sec * sample_rate)
    t = np.linspace(0, duration_sec, n_samples)
    
    # Orbital modulation (predicted signal)
    # Amplitude estimate: tau_P / tau_clock ~ 5.4e-44 / 2.3e-15 ~ 2.3e-29
    # For numerical stability, we scale it up for demonstration and note actual scale.
    theoretical_amplitude = PLANCK_TIME * CLOCK_FREQ  # ~2.3e-29
    # In simulation, we use a normalized amplitude for visibility; actual detection requires long integration.
    sim_amplitude = 1e-10  # Placeholder for code demonstration only
    
    orbital_signal = sim_amplitude * np.sin(2 * np.pi * ORBITAL_FREQ * t)
    
    # Noise components (physically motivated)
    white_noise = np.random.normal(0, 1e-18, n_samples)          # white frequency noise
    flicker_noise = np.cumsum(np.random.normal(0, 1e-19, n_samples)) * (1 / sample_rate)  # 1/f
    
    residual = orbital_signal + white_noise + flicker_noise
    
    # Save to file for power spectrum analysis
    np.savetxt('residual.txt', np.column_stack((t, residual)), 
               header='time(s) residual', comments='')
    
    print(f"Simulated {n_samples} samples over {duration_sec/86400:.1f} days.")
    print(f"Theoretical signal amplitude: {theoretical_amplitude:.2e}")
    print(f"Simulation amplitude (for demonstration): {sim_amplitude:.2e}")
    print("Residual saved to residual.txt")
    print("\nTo analyze the power spectrum, run:")
    print("  python -c \"import numpy as np; data=np.loadtxt('residual.txt'); freq=np.fft.rfftfreq(len(data), d=1.0); spec=np.abs(np.fft.rfft(data[:,1]))**2; idx=np.argmax(spec[1:])+1; print(f'Peak frequency: {freq[idx]:.3e} Hz')\"")
    
    return t, residual

def main():
    parser = argparse.ArgumentParser(
        description='Simulate atomic clock comparison residual for discrete substrate theory.',
        epilog='Example: python clock_comparison.py --duration 180days --sample-rate 0.1'
    )
    parser.add_argument('--duration', type=str, default='6months',
                        help='Simulation duration (e.g., 6months, 180days, 1e7s)')
    parser.add_argument('--sample-rate', type=float, default=1.0,
                        help='Sampling rate in Hz (default 1 Hz)')
    parser.add_argument('--no-warning', action='store_true',
                        help='Suppress the relativistic correction warning')
    args = parser.parse_args()
    
    try:
        duration_sec = parse_duration(args.duration)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    simulate_residual(duration_sec, args.sample_rate, include_relativistic_warning=not args.no_warning)

if __name__ == '__main__':
    main()
