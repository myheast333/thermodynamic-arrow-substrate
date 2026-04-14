# Validation Protocol: Atomic Clock Test of Discrete Substrate Residual Signal

**Version:** 2.0 (with relativistic preprocessing)  
**Date:** 2026-04-14  
**Target experiments:** ACES (ISS), GRACE-FO, or any satellite‑based clock comparison with fractional frequency instability ≤1×10⁻¹⁸ at 10⁴ s.

---

## 1. Scientific Objective

Test the prediction of a **discrete substrate framework** (quantum‑geometric origin of thermodynamic arrow) that a clock comparison residual between a ground clock and a satellite clock should contain a **narrow periodic component at the satellite’s orbital frequency**  
\( f_{\text{orb}} \approx 1.7\times 10^{-4}~\text{Hz} \) (90‑min orbit).  
The signal amplitude is predicted to be  
\( \Delta y \sim \tau_P / \Delta t_{\text{sample}} \approx 2.3\times 10^{-29} \) (fractional frequency),  
which is currently below direct detection but can be integrated over months to years to set upper limits or achieve significance via matched filtering.

---

## 2. Experimental Setup Requirements

| Component | Requirement | Example |
|-----------|-------------|---------|
| Ground clock (G) | Optical lattice clock, \( \sigma_y(\tau) \le 1\times10^{-18} \) for \( \tau > 10^4 \) s | PTB’s \(^{87}\)Sr clock, NIST’s Yb clock |
| Space clock (S) | High‑stability clock on LEO satellite, orbital period \( T_{\text{orb}} = 90\pm5 \) min | ACES (PHARAO on ISS), GRACE‑FO (USO) |
| Comparison link | Two‑way microwave or optical link, link noise below clock noise | MWL (ACES), or laser link (future) |
| Data duration | Minimum 6 months continuous | ≥180 days |
| Sampling rate | ≥0.1 Hz (recommended 1 Hz) | 1 Hz |

**Critical:** Satellite position & velocity vectors (ECI frame) must be recorded simultaneously with clock data for relativistic correction.

---

## 3. Data Collection Protocol

1. **Start both clocks** and synchronise time tags to a common reference (e.g., TAI or GPS time).
2. **Record continuously**:
   - Fractional frequency difference \( y(t) = (\nu_S - \nu_G)/\nu_G \)
   - Satellite ephemeris (position, velocity, attitude)
   - Environmental data (temperature, magnetic field, radiation)
3. **Log metadata** for every data gap, outlier, or calibration manoeuvre.

---

## 4. Critical Preprocessing: Removal of Known Relativistic Effects

> **⚠️ This step is mandatory before any search for the orbital‑frequency signal.**  
> Failure to subtract these effects will produce spurious peaks at orbital harmonics due to gravitational redshift and Sagnac effect.

### 4.1 Required Corrections (Standard GR)

| Effect | Formula (simplified) | Reference |
|--------|----------------------|-----------|
| Gravitational redshift | \( \frac{\Delta f}{f} = \frac{GM}{c^2}\left(\frac{1}{r_G} - \frac{1}{r_S}\right) \) | IERS 2010 |
| Shapiro delay | \( \Delta t = \frac{2GM}{c^3}\ln\left(\frac{r_G + r_S + d}{R_E}\right) \) | Shapiro (1964) |
| Sagnac effect | \( \Delta t_{\text{Sagnac}} = \frac{2\omega_E \cdot \vec{A}}{c^2} \) | Ashby (2003) |
| Orbital velocity time dilation | \( \frac{\Delta f}{f} = \sqrt{1-v_S^2/c^2} - \sqrt{1-v_G^2/c^2} \) | Special relativity |

### 4.2 Step‑by‑Step Preprocessing Pipeline

1. **Load raw data** \( y_{\text{raw}}(t) \), satellite positions \( \vec{r}_S(t) \), ground station position \( \vec{r}_G \) (fixed in ECEF, convert to ECI).
2. **Compute gravitational redshift correction**  
   \( \delta_{\text{grav}}(t) = \frac{GM}{c^2}\left(1/|\vec{r}_G(t)| - 1/|\vec{r}_S(t)|\right) \)  
   Subtract from \( y_{\text{raw}}(t) \).
3. **Compute Shapiro delay** (convert to fractional frequency via time derivative) and subtract.
4. **Compute Sagnac correction** using the signed area of the light path; subtract from time stamps.
5. **Compute velocity time dilation** \( \delta_{\text{vel}}(t) = \sqrt{1-v_S^2/c^2} - \sqrt{1-v_G^2/c^2} \) and subtract.
6. **Form the corrected residual**  
   \( y_{\text{corr}}(t) = y_{\text{raw}}(t) - \delta_{\text{grav}}(t) - \delta_{\text{vel}}(t) - \text{(Shapiro & Sagnac time converted to frequency)} \)
7. **Validate correction quality**: Compute Allan deviation of \( y_{\text{corr}}(t) \); it should show white + flicker noise without low‑frequency drift. Also verify no spectral peaks at 12‑hour or 24‑hour harmonics (known GR artefacts).

**Reference implementation:** See `relativistic_corrections.py` in the accompanying repository.

---

## 5. Spectral Analysis & Signal Search

### 5.1 Power Spectral Density (PSD) Estimation

- Use **Welch’s method** with 50% overlapping Hann windows.
- Segment length: \( \approx 2^{20} \) samples (about 12 days at 1 Hz) to resolve \( 10^{-5} \) Hz.
- Frequency range of interest: \( 10^{-5}~\text{Hz} \) to \( 10^{-3}~\text{Hz} \).

### 5.2 Detection Criterion

- Look for a **narrow peak** at \( f_{\text{orb}} = 1/T_{\text{orb}} \), where \( T_{\text{orb}} \) is the satellite’s mean orbital period (known from ephemeris).
- **Significance assessment**:
  - Compute local noise floor in a 10‑bin window around \( f_{\text{orb}} \) (excluding the candidate bin).
  - Define \( \text{SNR} = P_{\text{peak}} / \langle P_{\text{noise}} \rangle \).
  - Use bootstrap (shuffle residuals while preserving noise structure) to estimate false alarm probability.

### 5.3 Integration Time & Sensitivity

- With current clock stability (\( \sigma_y \approx 10^{-18} \) at \( 10^4 \) s), the **expected signal amplitude** \( \Delta y \approx 2.3\times 10^{-29} \) requires an integration time \( T_{\text{int}} \) such that \( \sigma_y(T_{\text{int}}) \approx \Delta y \).
- For white phase noise, \( \sigma_y(\tau) \propto 1/\sqrt{\tau} \). To reach \( 2.3\times 10^{-29} \), we need \( \tau \approx 10^{20} \) seconds — impossible.
- **However**: The signal is not white but **coherent at a known frequency**. Using matched filtering (or simply FFT with long integration), the signal‑to‑noise ratio scales as \( \sqrt{T_{\text{int}}} \) for white noise, but for \( 1/f \) noise the scaling is slower. Still, a **null result after 6 months** can place an upper limit on the effect at the level of \( \sim 10^{-16} \) in fractional frequency (PSD amplitude), which would rule out the simplest version of the model if the predicted amplitude were many orders larger.  
  *Practical conclusion:* The direct signal is too small for current clocks, but the framework remains falsifiable because it predicts **exactly zero** signal if discrete time does not exist. Any positive detection above \( 10^{-18} \) at \( f_{\text{orb}} \) would be revolutionary.

---

## 6. Expected Outcome & Falsifiability

| Scenario | Interpretation |
|----------|----------------|
| **Statistically significant peak at \( f_{\text{orb}} \)** (SNR ≥ 5 after 6‑12 months) | Supports discrete substrate framework; rules out all known noise sources (must be reproduced in independent missions). |
| **No peak above noise floor** after reaching a sensitivity of \( 10^{-18} \) in fractional frequency amplitude at \( f_{\text{orb}} \) | Disfavours the simplest discrete substrate prediction; the model would need revision (e.g., much smaller amplitude or different frequency scaling). |
| **Peak at a different frequency** (e.g., half the orbital frequency) | Points to a systematic effect (e.g., gravitational tidal aliasing) and would not confirm the theory. |

**Key falsifiability statement:**  
> The discrete substrate framework predicts **a single, isolated frequency** exactly equal to the satellite’s orbital period, with **no free parameters**. If after correcting for all known relativistic effects and noise, no such peak is found at a level that the experimental sensitivity could have detected (given the integration time), the theory is empirically ruled out.

---

## 7. Simulation & Code Repository

The accompanying repository contains:

- `clock_comparison.py` – Simulates the expected residual with realistic noise (white + flicker) and an injected orbital signal.
- `relativistic_corrections.py` – Implements all GR corrections for GRACE‑like data.
- `power_spectrum_analysis.py` – Computes PSD and searches for the orbital peak.
- `validation_protocol.md` – This document.

**To run the demonstration simulation:**  
```bash
python clock_comparison.py --duration 6months
