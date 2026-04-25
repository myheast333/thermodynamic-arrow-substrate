#!/usr/bin/env python3
"""
Clock Comparison Simulation for Substrate Ontology Experimental Test (V5.5)

Simulates the comparison between two clocks to detect the predicted
1.7e-4 Hz signal from the discrete substrate framework.

Author: Jingsong Zhou
Based on: "The Geometric Origin of the Second Law" (2026)
DOI: 10.5281/zenodo.19537142
"""

import numpy as np
import argparse
import sys

def simulate_residual(duration_sec, sample_rate=1.0, include_relativistic_warning=True):
    """Simulate clock comparison residual with substrate ontology signal"""
    
    if include_relativistic_warning:
        print("=" * 70)
        print("⚠️  CRITICAL NOTE FOR EXPERIMENTAL VALIDATION ⚠️")
        print("=" * 70)
        print("This simulation does NOT include known relativistic effects.")
        print("In a real experiment with satellite clock data, you MUST:")
        print("  1. Subtract gravitational redshift (Earth's potential)")
        print("  2. Remove Shapiro delay and Sagnac effect")
        print("  3. Correct for orbital velocity time dilation")
        print("  4. THEN analyze residuals for the 1.7e-4 Hz signal")
        print("See 'validation_protocol.md' for detailed step-by-step protocol.")
        print("=" * 70)
        print()
    
    # Simulation parameters
    n_samples = int(duration_sec * sample_rate)
    
    # Time array
    t = np.linspace(0, duration_sec, n_samples, dtype=np.float64)
    
    # Theoretical signal parameters (V5.5)
    # Orbital frequency for ~90 minute orbit: f = 1/(90*60) ≈ 1.85e-4 Hz
    # Adjusted to 1.7e-4 Hz for specific orbital configuration
    signal_freq = 1.7e-4  # Hz
    
    # Theoretical amplitude (extremely small, 2.32e-29 seconds)
    theoretical_amplitude = 2.32e-29
    
    # For demonstration purposes, use larger amplitude to be visible
    # In real experiment, this would be at the noise floor
    demonstration_amplitude = 1.0e-10
    
    # Generate signal (using demonstration amplitude)
    signal = demonstration_amplitude * np.sin(2 * np.pi * signal_freq * t)
    
    # Add small noise (white noise)
    noise_amplitude = 5.0e-11
    noise = noise_amplitude * np.random.randn(n_samples)
    
    # Total residual
    residual = signal + noise
    
    print(f"Simulated {n_samples:,} samples over {duration_sec/86400:.1f} days.")
    print(f"Theoretical signal amplitude: {theoretical_amplitude:.2e}")
    print(f"Simulation amplitude (for demonstration): {demonstration_amplitude:.2e}")
    
    # Save to .npy format (FASTEST - takes 2-3 seconds)
    data = np.column_stack((t, residual))
    np.save('residual.npy', data)
    print(f"Residual saved to residual.npy (binary format, {data.nbytes/1e6:.1f} MB)")
    
    # Also save small text sample for inspection (1000 rows only)
    sample_size = 1000
    sample_data = data[:sample_size]
    np.savetxt('residual_sample.txt', sample_data, 
               header='time(s) residual', 
               comments='',
               fmt='%.18e %.18e')
    print(f"Sample saved to residual_sample.txt ({sample_size} rows)")
    
    print(f"\nTo analyze the power spectrum, run:")
    print(f"  python power_spectrum.py")
    
    return data

def main():
    parser = argparse.ArgumentParser(description='Clock Comparison Simulation')
    parser.add_argument('--duration', type=float, default=180.0,
                        help='Simulation duration in days (default: 180.0)')
    parser.add_argument('--sample-rate', type=float, default=1.0,
                        help='Sampling rate in Hz (default: 1.0)')
    parser.add_argument('--no-warning', action='store_true',
                        help='Suppress relativistic warning message')
    
    args = parser.parse_args()
    
    duration_sec = args.duration * 86400.0
    
    simulate_residual(duration_sec, args.sample_rate, 
                     include_relativistic_warning=not args.no_warning)

if __name__ == "__main__":
    main()
