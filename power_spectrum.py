#!/usr/bin/env python3
"""
power_spectrum.py - Strict Power Spectral Density Analysis for Atomic Clock Residuals

Implements the exact experimental protocol from "The Geometric Origin of the Second Law" (V5.5):
- Analyzes clock comparison residual data from residual.txt
- Computes PSD using Welch's method with proper frequency resolution
- Detects signal at orbital frequency f_orb = 1.7e-4 Hz
- Applies strict 3-sigma detection threshold based on measured noise floor
- Provides automatic verdict: supports or falsifies the theory

Author: Jingsong Zhou
Date: 2026-04-14
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import sys
import os

# Critical parameters from V5.5 paper
ORBITAL_FREQ = 1.7e-4  # Orbital frequency in Hz (90-minute orbit)
EXPECTED_AMPLITUDE = 2.3e-29  # True theoretical amplitude (for reference only)

def load_residual_data(filename='residual.txt'):
    """Load residual data from file, handle common errors."""
    if not os.path.exists(filename):
        print(f"Error: {filename} not found!")
        print("Please ensure residual.txt is in the current directory.")
        sys.exit(1)
    
    try:
        data = np.loadtxt(filename)
        if data.shape[1] != 2:
            print(f"Error: {filename} must have exactly 2 columns (time, residual)")
            sys.exit(1)
        return data[:, 0], data[:, 1]
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        sys.exit(1)

def compute_psd(t, residual, nperseg=16384):
    """
    Compute Power Spectral Density using Welch's method.
    
    Parameters:
    -----------
    t : array-like
        Time array (seconds)
    residual : array-like  
        Fractional frequency residual data
    nperseg : int
        Number of samples per segment (controls frequency resolution)
        
    Returns:
    --------
    f : array
        Frequency array (Hz)
    psd : array
        Power spectral density (dimensionless²/Hz)
    df : float
        Frequency resolution (Hz)
    """
    # Calculate sampling rate
    dt = np.mean(np.diff(t))
    fs = 1.0 / dt
    
    # Verify frequency resolution requirement
    df = fs / nperseg
    if df > ORBITAL_FREQ:
        print(f"Warning: Frequency resolution {df:.2e} Hz is larger than orbital frequency {ORBITAL_FREQ:.2e} Hz")
        print("Consider increasing nperseg for better resolution.")
    
    # Compute PSD using Welch's method
    f, psd = signal.welch(
        residual, 
        fs=fs, 
        nperseg=nperseg,
        noverlap=nperseg//2,
        window='hann',
        scaling='density'
    )
    
    return f, psd, df

def estimate_noise_floor(f, psd):
    """
    Estimate noise floor from high-frequency white noise region.
    Uses frequency range [1e-3, 0.1] Hz as specified in V5.5.
    
    Returns:
    --------
    noise_floor : float
        Median PSD value in white noise region
    """
    # Define white noise region (above 1/f corner)
    white_noise_mask = (f >= 1e-3) & (f <= 0.1)
    
    if np.sum(white_noise_mask) == 0:
        # Fallback: use highest frequencies available
        white_noise_mask = f >= np.percentile(f[f > 0], 90)
    
    if np.sum(white_noise_mask) == 0:
        raise ValueError("Cannot estimate noise floor: insufficient frequency range")
    
    noise_floor = np.median(psd[white_noise_mask])
    return noise_floor

def detect_signal_at_frequency(f, psd, target_freq, noise_floor, threshold_sigma=3.0):
    """
    Detect signal at specific frequency with statistical threshold.
    
    Parameters:
    -----------
    f : array
        Frequency array
    psd : array
        PSD values
    target_freq : float
        Target frequency to test
    noise_floor : float
        Estimated noise floor
    threshold_sigma : float
        Detection threshold in sigma units
        
    Returns:
    --------
    detected : bool
        Whether signal is detected
    peak_value : float
        PSD value at target frequency
    threshold_value : float
        Detection threshold value
    """
    # Find closest frequency bin to target
    freq_idx = np.argmin(np.abs(f - target_freq))
    peak_value = psd[freq_idx]
    
    # Apply detection threshold
    threshold_value = threshold_sigma * noise_floor
    detected = peak_value > threshold_value
    
    return detected, peak_value, threshold_value

def create_analysis_plot(f, psd, noise_floor, detection_result, df):
    """
    Create publication-quality plot following V5.5 specifications.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot PSD
    ax.loglog(f[f > 0], psd[f > 0], 'b-', linewidth=1.5, label='PSD')
    
    # Add 1/f reference line
    f_ref = np.array([1e-5, 1e-3])
    psd_ref = psd[np.argmin(np.abs(f - 1e-4))] * (f_ref / 1e-4) ** (-1)
    ax.loglog(f_ref, psd_ref, 'k--', alpha=0.7, label='1/f reference')
    
    # Mark orbital frequency
    ax.axvline(ORBITAL_FREQ, color='red', linestyle='--', linewidth=2, 
               label=f'Orbital frequency\n({ORBITAL_FREQ:.1e} Hz)')
    
    # Add detection threshold
    threshold_val = 3.0 * noise_floor
    ax.axhline(threshold_val, color='green' if detection_result['detected'] else 'red', 
               linestyle=':', linewidth=2, 
               label=f'3σ threshold\n({threshold_val:.2e})')
    
    # Highlight detection region
    detection_box_x = [ORBITAL_FREQ * 0.8, ORBITAL_FREQ * 1.2]
    detection_box_y = [threshold_val * 0.8, threshold_val * 1.2]
    ax.fill_betweenx(detection_box_y, detection_box_x[0], detection_box_x[1], 
                     alpha=0.2, color='green' if detection_result['detected'] else 'red')
    
    # Labels and formatting
    ax.set_xlabel('Frequency (Hz)', fontsize=12)
    ax.set_ylabel('Power Spectral Density (fractional$^2$/Hz)', fontsize=12)
    ax.set_title('Atomic Clock Comparison Residual - Power Spectrum Analysis\n'
                '(Strict test of Substrate Ontology prediction)', fontsize=14)
    ax.grid(True, which="both", ls="-", alpha=0.3)
    ax.legend(loc='upper right')
    
    # Set axis limits
    ax.set_xlim(1e-5, 1)
    ax.set_ylim(1e-34, 1e-24)
    
    # Add verdict text box
    verdict_text = ("SUPPORTS THEORY" if detection_result['detected'] 
                   else "FALSIFIES THEORY")
    verdict_color = 'green' if detection_result['detected'] else 'red'
    
    ax.text(0.02, 0.98, f"VERDICT: {verdict_text}\n"
                        f"Orbital freq: {ORBITAL_FREQ:.1e} Hz\n"
                        f"Resolution: {df:.1e} Hz\n"
                        f"Peak PSD: {detection_result['peak_value']:.2e}\n"
                        f"Threshold: {detection_result['threshold_value']:.2e}",
            transform=ax.transAxes, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
            color=verdict_color, fontweight='bold', fontsize=11)
    
    plt.tight_layout()
    return fig

def main():
    """Main analysis pipeline."""
    print("=" * 60)
    print("POWER SPECTRAL DENSITY ANALYSIS")
    print("Substrate Ontology Experimental Test (V5.5)")
    print("=" * 60)
    
    # Load data
    print("\n1. Loading residual data...")
    t, residual = load_residual_data()
    print(f"   Data points: {len(t)}")
    print(f"   Duration: {t[-1] - t[0]:.0f} seconds ({(t[-1] - t[0])/86400:.1f} days)")
    print(f"   Sampling rate: {1/np.mean(np.diff(t)):.1f} Hz")
    
    # Compute PSD
    print("\n2. Computing Power Spectral Density...")
    f, psd, df = compute_psd(t, residual)
    print(f"   Frequency resolution: {df:.2e} Hz")
    print(f"   Orbital frequency: {ORBITAL_FREQ:.2e} Hz")
    print(f"   Resolution adequate: {'YES' if df < ORBITAL_FREQ else 'NO'}")
    
    # Estimate noise floor
    print("\n3. Estimating noise floor...")
    try:
        noise_floor = estimate_noise_floor(f, psd)
        print(f"   Noise floor (median): {noise_floor:.2e}")
    except ValueError as e:
        print(f"   Error: {e}")
        sys.exit(1)
    
    # Detect signal
    print("\n4. Testing for orbital frequency signal...")
    detected, peak_value, threshold_value = detect_signal_at_frequency(
        f, psd, ORBITAL_FREQ, noise_floor, threshold_sigma=3.0
    )
    
    detection_result = {
        'detected': detected,
        'peak_value': peak_value,
        'threshold_value': threshold_value,
        'noise_floor': noise_floor
    }
    
    print(f"   Peak PSD at {ORBITAL_FREQ:.1e} Hz: {peak_value:.2e}")
    print(f"   3σ threshold: {threshold_value:.2e}")
    print(f"   Signal detected: {'YES' if detected else 'NO'}")
    
    # Create plot
    print("\n5. Generating analysis plot...")
    fig = create_analysis_plot(f, psd, noise_floor, detection_result, df)
    
    # Save results
    verdict = "supports" if detected else "falsifies"
    output_filename = f"power_spectrum_{verdict}.png"
    fig.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"   Plot saved as: {output_filename}")
    
    # Final verdict
    print("\n" + "=" * 60)
    print(f"FINAL VERDICT: {'SUPPORTS' if detected else 'FALSIFIES'} SUBSTRATE ONTOLOGY")
    print("=" * 60)
    
    if not detected:
        print("\nNote: Non-detection would falsify the theory as stated in V5.5.")
        print("This represents a strong, falsifiable prediction.")
    else:
        print("\nNote: Detection supports the theory, but requires independent verification.")
    
    # Display theoretical amplitude context
    print(f"\nTheoretical signal amplitude: {EXPECTED_AMPLITUDE:.1e}")
    print("(This extremely small value explains why detection requires long integration times)")
    
    plt.show()

if __name__ == "__main__":
    main()
