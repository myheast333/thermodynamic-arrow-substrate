# Validation Protocol: Atomic Clock Test of Discrete Substrate Residual Signal

This document provides a step-by-step guide for experimental groups (e.g., PTB, NIST) to replicate the proposed test of the discrete substrate framework.

## 1. Experimental Setup

- **Ground clock (G):** Optical lattice clock (e.g., $^{87}$Sr) with fractional instability $\sigma_y(\tau) \le 1\times 10^{-18}$ at averaging times $\tau > 10^4$ s.
- **Space clock (S):** High-performance atomic clock on a satellite in low Earth orbit (e.g., ACES mission on ISS, orbital period $T_{\text{orb}} \approx 90$ min, $f_{\text{orb}} \approx 1.7\times 10^{-4}$ Hz).
- **Comparison link:** Microwave or optical two-way link providing continuous phase comparison with negligible link noise.

## 2. Data Collection

- Operate both clocks continuously for a minimum of **6 months**.
- Record the fractional frequency difference $y(t) = (\nu_S - \nu_G)/\nu_G$ at regular intervals (e.g., $1$ sample per second or per minute).
- Archive raw phase data and environmental telemetry (temperature, magnetic field, satellite attitude).

## 3. Data Analysis

### 3.1 Preprocessing
- Remove known systematic effects (relativistic Doppler, gravitational redshift, clock drift) using standard models.
- Fill short gaps via linear interpolation; flag intervals with excessive noise.

### 3.2 Spectral Analysis
- Compute the power spectral density (PSD) of $y(t)$ using Welch's method with 50% overlapping segments.
- Focus on the frequency band $10^{-5}$ Hz to $10^{-3}$ Hz.

### 3.3 Signal Search
- Look for a **narrow peak at $f_{\text{orb}} = 1.7\times 10^{-4}$ Hz**.
- Assess significance by comparing to the local noise floor; use bootstrap resampling to estimate false alarm probability.

## 4. Expected Signal

- **Frequency:** Exactly the orbital frequency of the satellite.
- **Amplitude:** Predicted fractional frequency modulation amplitude $\Delta y \sim \tau_P / \Delta t_{\text{sample}} \approx 10^{-29}$. This is currently below detection threshold, but long-term integration (months to years) may allow upper limits to be placed.
- **Emergence time:** With current clock stability, the peak is expected to emerge above the $1/f$ noise floor after approximately **6 months** of integration (see simulation).

## 5. Falsifiability

- **Positive detection:** A statistically significant peak at $f_{\text{orb}}$ that cannot be attributed to known systematics would support the discrete substrate framework.
- **Null result:** The absence of such a peak, after reaching the required sensitivity, would place an upper limit on the discrete substrate effect and constrain the framework.

## 6. Contact

For questions regarding the theoretical prediction or simulation code, please refer to the manuscript or contact the author.
