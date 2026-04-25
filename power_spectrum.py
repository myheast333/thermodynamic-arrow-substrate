#!/usr/bin/env python3
"""
Power Spectral Density Analysis for Substrate Ontology Experimental Test (V5.5)

This script analyzes the residual time series data from clock_comparison.py
to detect the predicted 1.7e-4 Hz signal from the discrete substrate framework.

Author: Jingsong Zhou
Based on: "The Geometric Origin of the Second Law" (2026)
DOI: 10.5281/zenodo.19537142

CRITICAL NOTE FOR EXPERIMENTAL VALIDATION:
This simulation does NOT include known relativistic effects.
In a real experiment with satellite clock data, you MUST:
  1. Subtract gravitational redshift (Earth's potential)
  2. Remove Shapiro delay and Sagnac effect  
  3. Correct for orbital velocity time dilation
  4. THEN analyze residuals for the 1.7e-4 Hz signal
See 'validation_protocol.md' for detailed step-by-step protocol.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import os

def main():
    print("=" * 60)
    print("POWER SPECTRAL DENSITY ANALYSIS")
    print("Substrate Ontology Experimental Test (V5.5)")
    print("=" * 60)
    
    # 1. Load residual data using pandas
    print("\n1. Loading residual data...")
    try:
        # 使用 pandas 读取，自动处理标题行
        # 修复：delim_whitespace 已弃用，改用 sep='\s+'
        df = pd.read_csv('residual.txt', sep='\s+', comment='#', engine='python')
        
        # 提取数据
        time = df.iloc[:, 0].values
        residuals = df.iloc[:, 1].values
        
        n_samples = len(df)
        total_time = time[-1] - time[0]
        sampling_rate = 1.0  # Hz
        total_days = total_time / 86400.0
        
        print(f"   Loaded {n_samples:,} samples using pandas")
        print(f"   Time span: {total_days:.1f} days")
        print(f"   Sampling rate: {sampling_rate:.1f} Hz")
        print(f"   Data range: {residuals.min():.2e} to {residuals.max():.2e}")
        print(f"   DataFrame shape: {df.shape}")
        print(f"   Columns: {list(df.columns)}")
        
    except Exception as e:
        print(f"   Error loading residual.txt: {e}")
        print("   Make sure to run 'python clock_comparison.py' first")
        return
    
    # 2. Compute power spectral density using Welch method
    print("\n2. Computing power spectral density...")
    
    # Parameters for Welch method
    nperseg = 8192  # Number of points per segment
    noverlap = nperseg // 2  # 50% overlap
    
    # Compute PSD
    freq, psd = signal.welch(
        residuals, 
        fs=sampling_rate,
        window='hann',
        nperseg=nperseg,
        noverlap=noverlap,
        scaling='density',
        detrend='constant'
    )
    
    freq_resolution = freq[1] - freq[0]
    print(f"   Using Welch method with {nperseg}-point segments")
    print(f"   Frequency resolution: {freq_resolution:.2e} Hz")
    print(f"   Frequency range: {freq[0]:.2e} to {freq[-1]:.2e} Hz")
    
    # 3. Analyze spectrum for predicted signal
    print("\n3. Analyzing spectrum...")
    
    # Theoretical prediction from V5.5
    expected_freq = 1.7e-4  # Hz (orbital frequency for ~90 minute orbit)
    
    # Find the frequency bin closest to expected frequency
    freq_diff = np.abs(freq - expected_freq)
    expected_idx = np.argmin(freq_diff)
    actual_freq = freq[expected_idx]
    actual_power = psd[expected_idx]
    
    # Also find the global peak in the low-frequency region (1e-5 to 1e-3 Hz)
    low_freq_mask = (freq >= 1e-5) & (freq <= 1e-3)
    if np.any(low_freq_mask):
        peak_idx = np.argmax(psd[low_freq_mask])
        peak_freq = freq[low_freq_mask][peak_idx]
        peak_power = psd[low_freq_mask][peak_idx]
    else:
        peak_freq = actual_freq
        peak_power = actual_power
    
    print(f"   Expected frequency: {expected_freq:.3e} Hz")
    print(f"   Power at expected freq: {actual_power:.3e}")
    print(f"   Peak frequency (1e-5-1e-3 Hz): {peak_freq:.3e} Hz")
    print(f"   Peak power: {peak_power:.3e}")
    
    # Check if frequencies match within resolution
    freq_match = abs(peak_freq - expected_freq) < freq_resolution
    print(f"   Frequency match: {'YES' if freq_match else 'NO'}")
    
    # 4. Calculate Signal-to-Noise Ratio (SNR)
    print("\n4. Signal-to-Noise Ratio (SNR) analysis...")
    
    # Define noise floor as median of PSD in the low-frequency band
    noise_floor = np.median(psd[low_freq_mask])
    
    # SNR in dB
    snr_db = 10 * np.log10(peak_power / noise_floor)
    
    # Detection threshold (typically 3 dB for significant detection)
    detection_threshold = 3.0  # dB
    
    print(f"   Peak power: {peak_power:.3e}")
    print(f"   Noise floor (median): {noise_floor:.3e}")
    print(f"   SNR: {snr_db:.2f} dB")
    print(f"   Detection threshold: {detection_threshold:.1f} dB")
    print(f"   Signal detected: {'YES' if snr_db > detection_threshold else 'NO'}")
    
    # 5. Generate and save plot
    print("\n5. Generating visualization...")
    
    plt.figure(figsize=(14, 10))
    
    # Main plot - full spectrum
    plt.subplot(2, 1, 1)
    plt.loglog(freq, psd, 'b-', linewidth=1.0, alpha=0.8, label='Power Spectral Density')
    plt.axvline(x=expected_freq, color='red', linestyle='--', linewidth=2.0, 
                label=f'Expected: {expected_freq:.2e} Hz')
    plt.axvline(x=peak_freq, color='green', linestyle='--', linewidth=2.0,
                label=f'Peak: {peak_freq:.2e} Hz')
    
    plt.xlabel('Frequency (Hz)', fontsize=12)
    plt.ylabel('Power Spectral Density', fontsize=12)
    plt.title('Power Spectrum Analysis - Substrate Ontology Test (V5.5)', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, which='both')
    
    # Zoom plot - focus on orbital frequency region
    plt.subplot(2, 1, 2)
    zoom_mask = (freq >= 1e-5) & (freq <= 5e-4)
    if np.any(zoom_mask):
        plt.semilogy(freq[zoom_mask], psd[zoom_mask], 'b-', linewidth=1.5)
        plt.axvline(x=expected_freq, color='red', linestyle='--', linewidth=2.0)
        plt.axvline(x=peak_freq, color='green', linestyle='--', linewidth=2.0)
        
        plt.xlabel('Frequency (Hz)', fontsize=12)
        plt.ylabel('PSD (log scale)', fontsize=12)
        plt.title('Zoom: Orbital Frequency Region (1e-5 to 5e-4 Hz)', fontsize=12)
        plt.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    
    # Save the plot
    output_filename = 'power_spectrum_supports.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"   Plot saved: {output_filename}")
    
    # 6. Save analysis results to text file
    print("\n6. Saving analysis results...")
    results_filename = 'spectrum_analysis.txt'
    with open(results_filename, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("POWER SPECTRAL DENSITY ANALYSIS RESULTS\n")
        f.write("Substrate Ontology Experimental Test (V5.5)\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Input Data:\n")
        f.write(f"  File: residual.txt\n")
        f.write(f"  Samples: {n_samples:,}\n")
        f.write(f"  Duration: {total_days:.1f} days\n")
        f.write(f"  Sampling rate: {sampling_rate:.1f} Hz\n\n")
        
        f.write(f"Theoretical Prediction:\n")
        f.write(f"  Expected frequency: {expected_freq:.3e} Hz\n")
        f.write(f"  Reference: Jingsong Zhou (2026)\n")
        f.write(f"  DOI: 10.5281/zenodo.19537142\n\n")
        
        f.write(f"Spectral Analysis Results:\n")
        f.write(f"  Peak frequency: {peak_freq:.3e} Hz\n")
        f.write(f"  Peak power: {peak_power:.3e}\n")
        f.write(f"  Power at expected freq: {actual_power:.3e}\n")
        f.write(f"  Frequency resolution: {freq_resolution:.2e} Hz\n")
        f.write(f"  Noise floor (median): {noise_floor:.3e}\n")
        f.write(f"  SNR: {snr_db:.2f} dB\n\n")
        
        f.write(f"Detection Results:\n")
        f.write(f"  Frequency match: {freq_match}\n")
        f.write(f"  Signal detected: {snr_db > detection_threshold}\n")
        f.write(f"  Detection threshold: {detection_threshold:.1f} dB\n\n")
        
        f.write(f"Conclusion:\n")
        if freq_match and snr_db > detection_threshold:
            f.write("The simulated data shows a clear signal at the predicted orbital\n")
            f.write("frequency of 1.7e-4 Hz, consistent with the discrete substrate\n")
            f.write("framework (V5.5) prediction.\n")
        elif not freq_match and snr_db > detection_threshold:
            f.write("A significant signal was detected, but at a different frequency\n")
            f.write("than predicted. This may indicate an issue with the simulation\n")
            f.write("parameters or an unexpected physical effect.\n")
        else:
            f.write("No significant signal was detected at the expected frequency.\n")
            f.write("This could be due to insufficient simulation duration,\n")
            f.write("inadequate sampling rate, or the absence of the predicted effect.\n")
    
    print(f"   Results saved: {results_filename}")
    
    # 7. Final conclusion
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    
    if freq_match and snr_db > detection_threshold:
        print("\nCONCLUSION: The simulated data supports the discrete substrate")
        print("framework (V5.5) prediction with a clear signal at 1.7e-4 Hz.")
    else:
        print("\nCONCLUSION: The analysis did not confirm the V5.5 prediction.")
        print("Review simulation parameters and consider longer duration or")
        print("higher sampling rate for better sensitivity.")
    
    print(f"\nOutput files:")
    print(f"   - {output_filename}")
    print(f"   - {results_filename}")
    
    # Reminder about real experimental validation
    print(f"\nREMINDER FOR REAL EXPERIMENTS:")
    print(f"Real satellite clock data requires relativistic corrections!")
    print(f"See 'validation_protocol.md' for the complete 7-step protocol.")

if __name__ == "__main__":
    main()
