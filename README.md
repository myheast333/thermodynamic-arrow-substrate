📄 最新 README.md 内容

How to Contribute
Run python clock_comparison.py 
Compare output with NASA GRACE data
Report residuals at frequency 1.7e-4 Hz

Thermodynamic Arrow from a Discrete Substrate

This repository contains simulation code accompanying the manuscript:

"The Geometric Origin of the Second Law of Thermodynamics: Irreducible Residual Deficits in a Discrete Substrate"  Jingsong Zhou (2026)

Overview

The code reproduces the key experimental prediction of the paper: a residual periodic signal in atomic clock comparisons at the orbital frequency of a satellite (1.7 times 10^{-4} Hz), arising from the discrete sampling of the substrate's global refresh rate.

Repository Contents
File   Description
clock_comparison.py   Simulates ground vs. space clock comparison and generates residual time series

power_spectrum.py   Computes power spectral density of the residual and plots the result

validation_protocol.md   Step-by-step guide for experimental labs to replicate the proposed test

substrate_sim.py   (Optional) Discrete substrate evolution simulator for pedagogical validation

Quick Start

Requirements: Python 3.8+ with numpy and matplotlib.

bash
pip install numpy matplotlib

Run the simulation:
bash
python clock_comparison.py
python power_spectrum.py

Key Features

Atomic Clock Comparison Simulation
Simulates ground-based vs. space-based atomic clocks
Models relativistic effects (special and general relativity)
Includes discrete substrate refresh rate effects
Generates realistic residual time series

Power Spectrum Analysis
Computes power spectral density using Welch's method
Identifies the characteristic frequency at 1.7e-4 Hz
Compares with theoretical predictions
Produces publication-quality plots

Experimental Validation Ready
Output format compatible with NASA GRACE data
Standardized residual reporting at 1.7e-4 Hz
Community review ready validation protocol
Reproducible experimental setup

Theoretical Background

Discrete Substrate Framework
The model is based on a discrete substrate where:
Global refresh rate creates irreducible deficits
Orbital motion samples this refresh rate periodically
Results in measurable residual signals in precision timing

Predicted Signal Characteristics
Frequency: 1.7 times 10^{-4} Hz (orbital frequency)
Amplitude: ~10^{-19} seconds (relative time deviation)
Periodicity: Matches satellite orbital period (~97 minutes)
Persistence: Irreducible due to fundamental substrate discreteness

Validation Protocol

The repository includes a comprehensive validation protocol that enables experimental laboratories to:

Replicate the simulation with their own parameters
Compare with real data from atomic clock networks
Analyze residuals at the predicted frequency
Contribute findings to the community review process

Expected Output

When running the simulation, you should see:

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

How to Validate Against Real Data

Obtain NASA GRACE or similar satellite clock data
Extract time residuals between ground and space clocks
Compute power spectrum of your residuals
Look for peak at 1.7e-4 Hz
Compare amplitude with simulation predictions
Report findings to the community

Citation

If you use this code in your research, please cite:

@article{zhou2026geometric,
  title={The Geometric Origin of the Second Law of Thermodynamics: Irreducible Residual Deficits in a Discrete Substrate},
  author={Zhou, Jingsong},
  year={2026},
  doi={10.5281/zenodo.19537142}
}

License

MIT License - see LICENSE for details.

Contact

For questions about the theoretical framework or experimental validation:
Author: Jingsong Zhou
Email: myheast@gmail.com
Institution: Independent Researcher

Note: This repository represents cutting-edge theoretical physics with testable experimental predictions. Community validation is essential for scientific progress!
