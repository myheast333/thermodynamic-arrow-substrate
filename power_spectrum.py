#!/usr/bin/env python3
"""
Power Spectral Density Analysis for Substrate Ontology Experimental Test
Version 5.5 (Fixed - 2D Array Support)

This script analyzes the residual time series from clock_comparison.py
and computes the power spectral density to detect the characteristic
frequency at 1.7e-4 Hz.

FIXED: Now correctly handles 2D array format (time, residual)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import sys
import os

# Set matplotlib style for scientific plots
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 10

def load_residual_data():
    """Load residual data from residual.npy and extract residual values"""
    print("1. Loading residual data...")
    
    if not os.path.exists('residual.npy'):
        print("   Error: residual.npy not found!")
        print("   Please run 'python clock_comparison.py' first")
        sys.exit(1)
    
    try:
        data = np.load('residual.npy')
        print("   [OK] Loaded data array with shape: {}".format(data.shape))
        
        # Handle different data formats
        if data.ndim == 2:
            # Format: (samples, 2) where column 0 = residual, column 1 = time (or vice versa)
            print("   Data is 2D array - extracting residual column...")
            
            # Check which column has smaller values (likely the residual)
            col0_range = np.max(np.abs(data[:, 0]))
            col1_range = np.max(np.abs(data[:, 1]))
            
            print("   Column 0 range: {:.2e}".format(col0_range))
            print("   Column 1 range: {:.2e}".format(col1_range))
            
            # The residual should have much smaller values than timestamps
            if col0_range < col1_range:
                residuals = data[:, 0]
                print("   [OK] Using column 0 as residuals (smaller range)")
            else:
                residuals = data[:, 1]
                print("   [OK] Using column 1 as residuals (smaller range)")
        elif data.ndim == 1:
            # Format: (samples,) - already the residual values
            residuals = data
            print("   [OK] Data is 1D array - using directly as residuals")
        else:
            print("   Error: Unexpected data dimensions: {}".format(data.ndim))
            sys.exit(1)
        
        print("   Residuals shape: {}".format(residuals.shape))
        print("   Data type: {}".format(residuals.dtype))
        print("   Min: {:.2e}, Max: {:.2e}".format(np.min(residuals), np.max(residuals)))
        print("   Mean: {:.2e}, Std: {:.2e}".format(np.mean(residuals), np.std(residuals)))
        
        return residuals
    except Exception as e:
        print("   Error loading residual.npy: {}".format(e))
        import traceback
        traceback.print_exc()
        sys.exit(1)

def compute_power_spectrum(residuals, sampling_rate=1.0):
    """Compute power spectral density using Welch's method"""
    print("\n2. Computing power spectral density...")
    
    # Welch's method parameters
    # Use smaller segment size for very large datasets
    max_nperseg = 32768  # Maximum segment size
    nperseg = min(max_nperseg, len(residuals) // 100)  # Use 1% of data or max
    nperseg = max(nperseg, 1024)  # Minimum segment size
    
    noverlap = nperseg // 2  # 50% overlap
    
    print("   Total samples: {:,}".format(len(residuals)))
    print("   Sampling rate: {} Hz".format(sampling_rate))
    print("   Segment length: {} samples".format(nperseg))
    print("   Overlap: {} samples".format(noverlap))
    print("   Number of segments: {}".format((len(residuals) - noverlap) // (nperseg - noverlap)))
    
    try:
        frequencies, psd = signal.welch(
            residuals,
            fs=sampling_rate,
            window='hann',
            nperseg=nperseg,
            noverlap=noverlap,
            scaling='density',
            detrend='linear',
            average='mean'
        )
        
        print("   [OK] Computed PSD with {} frequency bins".format(len(frequencies)))
        print("   Frequency range: {:.2e} to {:.2e} Hz".format(frequencies[0], frequencies[-1]))
        print("   Frequency resolution: {:.2e} Hz".format(frequencies[1] - frequencies[0]))
        
        return frequencies, psd
    except Exception as e:
        print("   Error computing PSD: {}".format(e))
        import traceback
        traceback.print_exc()
        sys.exit(1)

def detect_peak(frequencies, psd, target_freq=1.7e-4):
    """Detect peak near the target frequency"""
    print("\n3. Detecting peak near target frequency: {:.2e} Hz".format(target_freq))
    
    # Define search window around target frequency (±50% to be safe)
    freq_min = target_freq * 0.5
    freq_max = target_freq * 1.5
    
    # Find indices in the search window
    window_mask = (frequencies >= freq_min) & (frequencies <= freq_max)
    window_freqs = frequencies[window_mask]
    window_psd = psd[window_mask]
    
    if len(window_psd) == 0:
        print("   [FAIL] No data in frequency window [{:.2e}, {:.2e}] Hz".format(freq_min, freq_max))
        print("   Available frequency range: [{:.2e}, {:.2e}] Hz".format(frequencies[0], frequencies[-1]))
        return None, None, None
    
    # Find peak in window
    peak_idx = np.argmax(window_psd)
    peak_freq = window_freqs[peak_idx]
    peak_psd = window_psd[peak_idx]
    
    # Calculate SNR
    # Use median of surrounding region as noise floor (excluding the peak window)
    lower_mask = (frequencies >= frequencies[0]) & (frequencies < freq_min)
    upper_mask = (frequencies > freq_max) & (frequencies <= frequencies[-1])
    
    if np.any(lower_mask) or np.any(upper_mask):
        noise_data = np.concatenate([
            psd[lower_mask] if np.any(lower_mask) else np.array([]),
            psd[upper_mask] if np.any(upper_mask) else np.array([])
        ])
        noise_floor = np.median(noise_data)
    else:
        noise_floor = np.median(psd)
    
    snr = peak_psd / noise_floor if noise_floor > 0 else 0
    
    print("   [OK] Peak detected at: {:.2e} Hz".format(peak_freq))
    print("   Peak PSD: {:.2e}".format(peak_psd))
    print("   Noise floor: {:.2e}".format(noise_floor))
    print("   Signal-to-Noise Ratio: {:.2f}".format(snr))
    print("   Frequency deviation: {:.2f}%".format(abs(peak_freq - target_freq) / target_freq * 100))
    
    return peak_freq, peak_psd, snr

def plot_power_spectrum(frequencies, psd, peak_freq, peak_psd, snr, target_freq=1.7e-4):
    """Create publication-quality power spectrum plot"""
    print("\n4. Generating power spectrum plot...")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot PSD on log-log scale
    ax.loglog(frequencies, psd, 'b-', linewidth=1.5, alpha=0.8, label='Power Spectral Density')
    
    # Mark target frequency
    ax.axvline(x=target_freq, color='r', linestyle='--', linewidth=2, 
               label='Target: {:.1e} Hz'.format(target_freq), alpha=0.7)
    
    # Mark detected peak
    if peak_freq is not None:
        ax.axvline(x=peak_freq, color='g', linestyle='-', linewidth=2,
                   label='Detected Peak: {:.1e} Hz\nSNR: {:.1f}'.format(peak_freq, snr), alpha=0.7)
        ax.plot(peak_freq, peak_psd, 'go', markersize=10, markeredgecolor='k')
    
    # Labels and title
    ax.set_xlabel('Frequency (Hz)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Power Spectral Density', fontsize=12, fontweight='bold')
    ax.set_title('Power Spectral Density Analysis\nSubstrate Ontology Experimental Test (V5.5)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Grid and legend
    ax.grid(True, which="both", ls="-", alpha=0.2)
    ax.legend(loc='best', fontsize=10, framealpha=0.9)
    
    # Add annotation box
    if peak_freq is not None:
        annotation_text = 'Peak Detection Results:\n' \
                         'Frequency: {:.2e} Hz\n' \
                         'Target: {:.2e} Hz\n' \
                         'Deviation: {:.2f}%\n' \
                         'SNR: {:.2f}'.format(peak_freq, target_freq, 
                                            abs(peak_freq - target_freq) / target_freq * 100, 
                                            snr)
        ax.text(0.02, 0.98, annotation_text, transform=ax.transAxes,
                fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Adjust layout
    plt.tight_layout()
    
    # Save plot
    output_file = 'power_spectrum.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print("   [OK] Plot saved to: {}".format(output_file))
    
    # Also save as PDF for publication quality
    pdf_file = 'power_spectrum.pdf'
    plt.savefig(pdf_file, dpi=300, bbox_inches='tight')
    print("   [OK] PDF saved to: {}".format(pdf_file))
    
    plt.show()

def save_results(frequencies, psd, peak_freq, peak_psd, snr):
    """Save analysis results to file"""
    print("\n5. Saving analysis results...")
    
    results = {
        'frequencies': frequencies,
        'psd': psd,
        'peak_freq': peak_freq,
        'peak_psd': peak_psd,
        'snr': snr,
        'target_freq': 1.7e-4
    }
    
    np.savez('power_spectrum_analysis.npz', **results)
    print("   [OK] Results saved to: power_spectrum_analysis.npz")
    
    # Also save CSV for easy viewing
    with open('power_spectrum_data.csv', 'w') as f:
        f.write('Frequency (Hz),PSD\n')
        for freq, power in zip(frequencies, psd):
            f.write('{:.6e},{:.6e}\n'.format(freq, power))
    print("   [OK] CSV data saved to: power_spectrum_data.csv")

def main():
    """Main analysis pipeline"""
    print("=" * 60)
    print("POWER SPECTRAL DENSITY ANALYSIS")
    print("Substrate Ontology Experimental Test (V5.5 - FIXED)")
    print("=" * 60)
    print()
    
    # Step 1: Load data
    residuals = load_residual_data()
    
    # Step 2: Compute PSD
    frequencies, psd = compute_power_spectrum(residuals)
    
    # Step 3: Detect peak
    peak_freq, peak_psd, snr = detect_peak(frequencies, psd)
    
    # Step 4: Plot results
    plot_power_spectrum(frequencies, psd, peak_freq, peak_psd, snr)
    
    # Step 5: Save results
    save_results(frequencies, psd, peak_freq, peak_psd, snr)
    
    print("\n" + "=" * 60)
    print("[OK] Analysis complete!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - power_spectrum.png (plot)")
    print("  - power_spectrum.pdf (publication quality)")
    print("  - power_spectrum_analysis.npz (full results)")
    print("  - power_spectrum_data.csv (frequency data)")
    print("\nTo validate against real data, see 'validation_protocol.md'")

if __name__ == '__main__':
    main()
