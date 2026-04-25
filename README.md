# 📄 **README.md 全文内容**

```markdown
![Validation Status](https://img.shields.io/badge/validation-ready_for_community_review-green)
## How to Contribute
1. Run `python clock_comparison.py` 
2. Compare output with NASA GRACE data
3. Report residuals at frequency 1.7e-4 Hz

# Thermodynamic Arrow from a Discrete Substrate

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19537142.svg)](https://doi.org/10.5281/zenodo.19537142)

This repository contains simulation code accompanying the manuscript:

**"The Geometric Origin of the Second Law of Thermodynamics: Irreducible Residual Deficits in a Discrete Substrate"**  
*Jingsong Zhou (2026)*

## Overview

The code reproduces the key experimental prediction of the paper: a residual periodic signal in atomic clock comparisons at the orbital frequency of a satellite ($1.7 \times 10^{-4}$ Hz), arising from the discrete sampling of the substrate's global refresh rate.

## Repository Contents

| File | Description |
| :--- | :--- |
| `clock_comparison.py` | Simulates ground vs. space clock comparison and generates residual time series |
| `power_spectrum.py` | Computes power spectral density of the residual and plots the result |
| `validation_protocol.md` | Step-by-step guide for experimental labs to replicate the proposed test |
| `substrate_sim.py` | (Optional) Discrete substrate evolution simulator for pedagogical validation |

## Quick Start

**Requirements:** Python 3.8+ with `numpy` and `matplotlib`.

```bash
pip install numpy matplotlib
```

**Run the simulation:**
```bash
python clock_comparison.py
python power_spectrum.py
```

## Key Features

### 1. Atomic Clock Comparison Simulation
- Simulates ground-based vs. space-based atomic clocks
- Models relativistic effects (special and general relativity)
- Includes discrete substrate refresh rate effects
- Generates realistic residual time series

### 2. Power Spectrum Analysis
- Computes power spectral density using Welch's method
- Identifies the characteristic frequency at 1.7e-4 Hz
- Compares with theoretical predictions
- Produces publication-quality plots

### 3. Experimental Validation Ready
- Output format compatible with NASA GRACE data
- Standardized residual reporting at 1.7e-4 Hz
- Community review ready validation protocol
- Reproducible experimental setup

## Theoretical Background

### Discrete Substrate Framework
The model is based on a discrete substrate where:
- Global refresh rate creates irreducible deficits
- Orbital motion samples this refresh rate periodically
- Results in measurable residual signals in precision timing

### Predicted Signal Characteristics
- **Frequency**: $1.7 \times 10^{-4}$ Hz (orbital frequency)
- **Amplitude**: ~$10^{-19}$ seconds (relative time deviation)
- **Periodicity**: Matches satellite orbital period (~97 minutes)
- **Persistence**: Irreducible due to fundamental substrate discreteness

## Validation Protocol

The repository includes a comprehensive validation protocol that enables experimental laboratories to:

1. **Replicate the simulation** with their own parameters
2. **Compare with real data** from atomic clock networks
3. **Analyze residuals** at the predicted frequency
4. **Contribute findings** to the community review process

## Expected Output

When running the simulation, you should see:

```
Simulating clock comparison...
Total simulation time: 86400.0 seconds (1.0 days)
Orbital frequency: 1.7e-04 Hz
Relativistic correction applied: Special + General Relativity
Discrete substrate effect included
Residual time series saved to 'clock_residuals.npy'

Computing power spectrum...
Peak detected at frequency: 1.7e-04 Hz
Peak amplitude: 1.23e-19
Signal-to-noise ratio: 15.7
Power spectrum plot saved to 'power_spectrum.png'
```

## How to Validate Against Real Data

1. **Obtain NASA GRACE or similar satellite clock data**
2. **Extract time residuals between ground and space clocks**
3. **Compute power spectrum of your residuals**
4. **Look for peak at 1.7e-4 Hz**
5. **Compare amplitude with simulation predictions**
6. **Report findings to the community**

## Citation

如果您在研究中使用此代码，请引用：

```
@article{zhou2026geometric,
标题={热力学第二定律的几何起源：离散基底中的不可约剩余缺陷},
作者=周景松,
年={2026},

}
```

##许可证

MIT 许可证 - 请参阅[许可证(许可证)了解详情。

##联系

关于理论框架或实验验证的问题：
- **作者**: 周景松
- **邮箱**: myheast@gmail.com
**：独立研究员

---

**注意**：本仓库代表了具有可检验实验预测的前沿理论物理。社区验证对于科学进步至关重要！
```
