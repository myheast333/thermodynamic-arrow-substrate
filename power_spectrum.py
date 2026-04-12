#!/usr/bin/env python3
"""
Power spectrum analysis for clock comparison residual.
Generates Figure 1 from the manuscript.
"""

import numpy as np
import matplotlib.pyplot as plt

# Orbital frequency (Hz)
ORBITAL_FREQ = 1.7e-4

def compute_psd(filename='residual.txt'):
    """Load residual data and compute power spectral density."""
    data = np.loadtxt(filename, skiprows=1)
    t = data[:, 0]
    residual = data[:, 1]
    
    # Sampling interval
    dt = t[1] - t[0]
    fs = 1.0 / dt
    
    # Compute PSD using Welch's method
    from scipy import signal
    f, psd = signal.welch(residual, fs, nperseg=min(1024, len(residual)//4))
    
    return f, psd

def plot_psd(f, psd, savefig=True):
    """Plot power spectral density with orbital frequency marker."""
    plt.figure(figsize=(8, 5))
    plt.loglog(f, psd, 'b-', linewidth=1, label='Simulated residual')
    
    # Mark orbital frequency
    plt.axvline(x=ORBITAL_FREQ, color='r', linestyle='--', 
                label=f'Orbital frequency ({ORBITAL_FREQ:.1e} Hz)')
    
    # 1/f reference line
    f_ref = np.array([1e-5, 1e-2])
    psd_ref = 1e-36 * (f_ref[0] / f_ref)**1
    plt.loglog(f_ref, psd_ref, 'k:', label='$1/f$ reference')
    
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power Spectral Density (fractional frequency)$^2$/Hz')
    plt.title('Clock Comparison Residual Power Spectrum (6 months integration)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if savefig:
        plt.savefig('power_spectrum.png', dpi=150, bbox_inches='tight')
        print("Figure saved to power_spectrum.png")
    plt.show()

def main():
    try:
        f, psd = compute_psd()
    except FileNotFoundError:
        print("Error: residual.txt not found. Run clock_comparison.py first.")
        return
    
    plot_psd(f, psd)

if __name__ == '__main__':
    main()
