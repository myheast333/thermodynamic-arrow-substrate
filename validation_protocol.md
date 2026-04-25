# 🔬 Experimental Validation Protocol: The Geometric Origin of the Second Law

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19537142.svg)](https://doi.org/10.5281/zenodo.19537142)

## 1. Overview

This protocol provides a standardized, step-by-step guide for experimental physics laboratories to test the central, falsifiable prediction of the discrete substrate framework presented in the paper:

> **"The Geometric Origin of the Second Law: Irreducible Informational Differences in a Discrete Substrate"**  
> Jingsong Zhou (2026)

The core prediction is that **high-precision comparisons between a ground-based atomic clock and a satellite-borne atomic clock will reveal an irreducible residual periodic signal at the satellite's orbital frequency (f<sub>orb</sub> ≈ 1.7 × 10<sup>-4</sup> Hz).** This signal arises from the intrinsic symmetry breaking of continuous rotations on a discrete substrate during periodic motion.

This protocol is designed to be reproducible, compatible with existing and upcoming space missions (e.g., ACES), and to facilitate community-driven scientific validation.

## 2. Theoretical Prediction Summary

### 2.1 Core Prediction
- **Frequency**: **f<sub>orb</sub> = 1 / T<sub>orb</sub> ≈ 1.7 × 10<sup>-4</sup> Hz**
    - Where T<sub>orb</sub> is the orbital period of the satellite (~90 minutes for Low Earth Orbit).
- **Physical Origin**: The discrete substrate cannot perfectly realize the continuous rotational symmetry of the satellite's orbit. This "closure informational difference" manifests as a persistent modulation in the clock's sampling of the substrate's fundamental update rate.
- **Signal Type**: An irreducible residual in the fractional frequency comparison data (y(t) = (ν<sub>S</sub> - ν<sub>G</sub>) / ν<sub>G</sub>).
- **Expected Amplitude**: Δy ∼ τ<sub>min</sub> / τ<sub>clock</sub> ≈ 10<sup>-29</sup>. While this amplitude is below current single-shot sensitivity, it is detectable through long-term integration (months to years) of high-stability clock data.

### 2.2 Why This Test is Falsifiable
The absence of a statistically significant peak at f<sub>orb</sub> in the power spectrum of properly corrected clock comparison data, after reaching the required integration time and accounting for all known systematics, would directly contradict the core mechanism of the discrete substrate framework.

## 3. Prerequisites

### 3.1 Data Requirements
- **Type**: Time series of fractional frequency residuals (y(t)) from a comparison between a ground clock (G) and a space clock (S).
- **Source**: Existing or future missions with high-precision clocks, such as:
    - **ACES (Atomic Clock Ensemble in Space)** on the ISS (operational ~2026-2027)
    - GPS/Galileo navigation satellite clock residuals
    - Dedicated future missions with optical clocks in space
- **Duration**: **Minimum of 6 months** of continuous or near-continuous data is recommended to allow sufficient integration for signal emergence above the 1/f noise floor.
- **Quality**: Data must have undergone standard relativistic corrections (Special and General Relativity).

### 3.2 Software Requirements
- Python 3.8 or higher
- Required packages: `numpy`, `matplotlib`, `scipy`
    ```bash
    pip install numpy matplotlib scipy
    ```

## 4. Validation Procedure

### Step 1: Understand the Simulation Baseline (Contextual)
The repository contains `substrate_sim.py`, which simulates the **cosmological evolution** of the dynamic precision horizon and entropy increase. While it does not generate the 1.7e-4 Hz signal itself, it validates the foundational axioms (finite information, minimal scale, intrinsic symmetry breaking) that lead to the prediction. Running it provides essential context for the geometric origin of irreversibility.

> **Note on Atomic Clock Simulation Code**: The specific scripts (`clock_comparison.py`, `power_spectrum.py`) referenced in the paper for generating the 1.7e-4 Hz signal are part of the complete validation suite. They are archived with the paper's DOI and will be released publicly to coincide with the analysis of ACES mission data. This protocol describes the method to validate the prediction using **real experimental data**.

### Step 2: Prepare Your Experimental Data
1.  Obtain the fractional frequency residual time series `y(t)` from your chosen mission.
2.  Ensure all standard relativistic corrections have been applied.
3.  Format the data as a 1D NumPy array of residuals with a corresponding time vector (or uniform sampling rate).

### Step 3: Compute the Power Spectral Density (PSD)
Use Welch's method or another appropriate spectral estimation technique to compute the PSD of `y(t)`.

**Example Analysis Script (`analyze_residuals.py`):**
```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# --- USER INPUT ---
# Load your experimental residual data (y(t))
time, y_residuals = np.loadtxt('your_residual_data.txt', unpack=True)
sampling_rate = 1.0 / np.mean(np.diff(time)) # Calculate from your time vector

# Define the target frequency and region of interest (ROI)
target_freq = 1.7e-4 # Hz
roi_min, roi_max = 1e-5, 1e-3 # Hz

# --- ANALYSIS ---
# Compute Power Spectral Density
frequencies, psd = signal.welch(
    y_residuals,
    fs=sampling_rate,
    nperseg=min(16384, len(y_residuals)//4), # Adjust segment length as needed
    noverlap=min(8192, len(y_residuals)//8),
    scaling='density'
)

# Focus on the Region of Interest
roi_mask = (frequencies >= roi_min) & (frequencies <= roi_max)
f_roi, psd_roi = frequencies[roi_mask], psd[roi_mask]

# Find the peak within a window around the target frequency
window_mask = (frequencies >= 1.5e-4) & (frequencies <= 1.9e-4)
if np.any(window_mask):
    peak_idx = np.argmax(psd[window_mask])
    detected_freq = frequencies[window_mask][peak_idx]
    peak_psd = psd[window_mask][peak_idx]
else:
    detected_freq, peak_psd = None, None

# --- OUTPUT ---
print(f"Target Frequency: {target_freq:.2e} Hz")
print(f"Detected Peak: {detected_freq:.2e} Hz")
if detected_freq:
    print(f"Relative Deviation: {abs(detected_freq - target_freq)/target_freq:.2%}")

# Plot the result
plt.figure(figsize=(10, 6))
plt.loglog(frequencies, psd, label='Experimental PSD')
plt.axvline(target_freq, color='red', linestyle='--', label=f'Target: {target_freq:.1e} Hz')
if detected_freq:
    plt.axvline(detected_freq, color='green', linestyle=':', label=f'Detected: {detected_freq:.1e} Hz')
plt.xlim(roi_min, roi_max)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectral Density')
plt.title('Clock Comparison Residual Power Spectrum')
plt.legend()
plt.grid(True, which="both", ls="-")
plt.savefig('experimental_psd.png', dpi=150)
plt.show()


###Step 4: Statistical Significance Testing
To claim a detection, the peak must meet stringent statistical criteria:
Frequency Match: The detected peak must be within 10% of the expected orbital frequency (i.e., |fdetected - forb| / forb ≤ 0.1).
Signal-to-Noise Ratio (SNR): Calculate the SNR by dividing the peak PSD value by the median noise floor in a nearby frequency band (e.g., 1e-4 to 3e-4 Hz). SNR ≥ 3 is a minimum threshold.
p-value: Perform a statistical test (e.g., based on the Chi-square distribution for Welch's PSD) to ensure the probability of the peak being a noise fluctuation is p ≤ 0.01.

###Step 5: Multi-Day and Cross-Validation
Persistence: The signal should be present consistently across multiple, non-overlapping segments of the data (e.g., weekly or monthly chunks).
Orbital Correlation: For missions with variable orbits, the signal frequency should correlate with the actual, instantaneous orbital frequency.
. Validation Criteria
表格
Criterion	Threshold	Method
Primary: Frequency Match	Within 10% of forb	Peak detection in PSD
Primary: Statistical Significance	p-value ≤ 0.01	Chi-square or equivalent test
Primary: Signal Persistence	Present in ≥ 3 independent data segments	Multi-segment analysis
Secondary: Amplitude Consistency	Matches theoretical scaling	Comparison with simulation (when available)
Secondary: Orbital Correlation	fsignal tracks forb(t)	For variable-orbit missions
A successful validation requires meeting all Primary criteria.
. Reporting Guidelines
When submitting your results for community review (e.g., via a GitHub issue or scientific publication), please include:
Mission Details: Name, clock types, data period, and orbital parameters.
Data Processing: Description of all corrections applied (especially relativistic).
Analysis Results: Detected frequency, SNR, p-value, and the PSD plot.
Data & Code: Share your processed data and the exact analysis script used (if possible).
. Expected Timeline & Feasibility
Data Availability: The ACES mission is scheduled to provide the ideal dataset starting in 2026-2027.
Analysis: Once data is available, the analysis outlined in this protocol can be completed within 1-2 weeks.
Feasibility: The experiment leverages existing and planned space infrastructure, making it a realistic near-term test of a foundational theory of physics.
. Contact
For questions regarding this validation protocol or the theoretical framework:
Author: Jingsong Zhou
Affiliation: Independent Researcher
Email: mailto:myheast@gmail.com
Version: 1.0
Last Updated: April 2026
Compatible with: Discrete Substrate Framework V5.5
DOI: 10.5281/zenodo.19537142
This validation protocol represents a community-driven effort to empirically test a profound claim about the origin of time's arrow. Your contribution is vital to the scientific process.
```
