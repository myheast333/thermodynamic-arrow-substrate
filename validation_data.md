# 📊 Validation Data: Power Spectral Density Analysis

## Executive Summary

This document presents the **expected validation signature** of the Discrete Substrate framework as detailed in the paper "The Geometric Origin of the Second Law". The theoretical prediction is a distinct peak in the Power Spectral Density (PSD) at the orbital frequency of **1.7 × 10⁻⁴ Hz**.

> **Important Note**: The image below is a **simulated reference** illustrating the *expected outcome* if the theory is correct. **Scientific confirmation requires detection of this signal in real experimental data from space-based atomic clock missions (e.g., ACES).**

![Simulated Power Spectral Density showing the predicted 1.7e-4 Hz peak](https://wanx.alicdn.com/wanx/100501912103/text_to_image_lite_v2/5dbee53dd224437c9107bf09f1f2ec6b_0_visibleWatermark.png)

## Data Interpretation

### Key Observed Features (in Simulation):
- **Peak Frequency**: **1.7 × 10⁻⁴ Hz** (marked by a red dashed line).
- **Frequency Range**: Logarithmic scale from **1×10⁻⁵ Hz to 1×10⁻³ Hz**, covering the Low Earth Orbit (LEO) regime.
- **Signal Characteristic**: A clear, coherent peak rising significantly above the background noise floor.
- **Spectral Shape**: A smooth PSD curve with the predicted signature.

### Validation Metrics (for Real Data):
When analyzing real experimental data, the following criteria must be met for a successful validation:
- **Frequency Match**: ✓ Detected peak within **1%** of the predicted 1.7e-4 Hz.
- **Signal Clarity**: ✓ Peak is unambiguously visible above the noise floor.
- **Statistical Significance**: ✓ High Signal-to-Noise Ratio (SNR ≥ 3) and p-value ≤ 0.01.
- **Reproducibility**: ✓ Consistent with the theoretical prediction and persistent across data segments.

## Technical Specifications

### Plot Parameters:
- **X-axis**: Frequency (Hz) — **Logarithmic Scale**
- **Y-axis**: Power Spectral Density (arbitrary units) — **Logarithmic Scale**
- **Frequency Range**: 10⁻⁵ to 10⁻³ Hz
- **Target Frequency**: 1.7 × 10⁻⁴ Hz (orbital frequency for ~90 min period)
- **Grid**: Professional scientific grid with major and minor ticks for clarity.

### Data Quality Indicators (for Real Data):
- **Noise Floor**: A stable and well-characterized background level across the band.
- **Peak Sharpness**: A narrow, coherent peak indicating a deterministic signal source.
- **Dynamic Range**: Sufficient to clearly resolve the signal from the noise.
- **Scaling**: Log-log scaling is optimal for visualizing signals over wide frequency ranges.

## Validation Status (of the Framework)

✅ **The framework makes a clear, falsifiable prediction that meets all primary validation criteria outlined in `validation_protocol.md` once confirmed with real data:**
- [ ] **Frequency Match**: Detected frequency matches target within 10% (to be confirmed with experiment).
- [ ] **Statistical Significance**: Signal is statistically significant (to be confirmed with experiment).
- [ ] **Persistence**: Signal is present in multiple independent data segments (to be confirmed with experiment).
- [x] **Theoretical Consistency**: The simulated signature is fully consistent with the axioms of the discrete substrate.

## Next Steps for the Community

### For Experimental Laboratories:
1.  Apply the `validation_protocol.md` to your own high-precision clock comparison data.
2.  Analyze residuals from missions like **ACES (Atomic Clock Ensemble in Space)**, GRACE-FO, or GNSS constellations.
3.  Submit your findings through the community review process.
4.  **Contribute additional datasets** to strengthen the collective validation effort.

### Data Usage Guidelines:
- This simulated validation data serves as a **reference benchmark**.
- Use it to compare against your experimental results.
- Include it in your validation reports for illustrative purposes, if applicable.
- Always cite the original manuscript when using this data.

## Expected Output Files

When you run a complete validation analysis on your experimental data, you should generate a set of files like the following:
clock_residuals.npy # Time-domain fractional frequency residual data
power_spectrum.png # Power Spectral Density plot (to be compared with the reference above)
validation_analysis.npz # Archive containing all analysis results (frequencies, PSD, stats)
experimental_comparison.pdf # Final report comparing your results to the theoretical prediction

## Citation

Please cite the original paper if you use this validation data or its concepts in your work:

```bibtex
@article{zhou2026geometric,
  title={The Geometric Origin of the Second Law: Irreducible Informational Differences in a Discrete Substrate},
  author={Zhou, Jingsong},
  year={2026},
  doi={10.5281/zenodo.19537142}
}
```
### Contact
For any questions regarding this validation data or its interpretation:
Author: Jingsong Zhou
Email: mailto:myheast@gmail.com
Affiliation: Independent Researcher
Version: 1.0
Last Updated: April 2026
Purpose: To illustrate the expected experimental signature of the Discrete Substrate framework. Real-world data is required for scientific confirmation.
