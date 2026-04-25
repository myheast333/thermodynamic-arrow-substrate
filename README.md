# The Geometric Origin of the Second Law: A Discrete Substrate Framework

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19537142.svg)](https://doi.org/10.5281/zenodo.19537142)

This repository provides the simulation code and validation protocol supporting the theoretical framework presented in the paper:

> **"The Geometric Origin of the Second Law: Irreducible Informational Differences in a Discrete Substrate"**  
> Jingsong Zhou  
> April 2026

The work derives the Second Law of Thermodynamics from three minimal axioms of a discrete substrate, offering a first-principles explanation for the thermodynamic arrow of time without invoking special initial conditions.

## Core Theoretical Framework

Our framework is built upon three foundational axioms:

1.  **Finite Information**: Any finite spacetime region contains a finite amount of information.
2.  **Minimal Scale**: Physical reality is composed of indivisible minimal units (Planck scale).
3.  **Intrinsic Symmetry Breaking**: Continuous symmetries (e.g., rotation, translation) cannot be perfectly realized on a discrete substrate, leaving behind an irreducible **closure informational difference** (δ).

From these axioms, we prove that entropy, defined as the macroscopic sum of accumulated informational differences (S = k<sub>B</sub>∑δ<sub>i</sub>), must increase monotonically (dS/dt ≥ 0). This is a *geometric necessity*, not a statistical contingency, resolving Loschmidt's reversibility paradox.

## Repository Contents

This repository contains two main components:

### 1. Cosmic Evolution Simulator (`substrate_sim.py`)
This script implements the **cosmological implications** of the discrete substrate framework, specifically simulating the growth of the **Dynamic Precision Horizon** D(t) = ⌊log<sub>b</sub>(t/τ<sub>min</sub>)⌋.

- **Functionality**: It models the continuous decay of energy level differences (ΔE(t) ∝ 1/t) and the concurrent, monotonic increase of entropy (S(t) ∝ ln t) across cosmic history.
- **Output**: Generates a comprehensive figure with 8 subplots that:
    - Visualize the dynamic precision horizon K(t) vs. cosmic age.
    - Demonstrate the continuous decay of ΔE(t).
    - Verify the mathematical relation b<sup>-K(t)</sup> ≈ τ<sub>0</sub>/t.
    - Provide three independent numerical verifications of the Second Law (thermal, information, and phase-space entropy).
    - Resolve the "complexity paradox" by showing how increasing resolution enables the emergence of structure while total entropy still increases.

This simulator serves as a powerful pedagogical and theoretical tool to explore the long-term, universe-scale consequences of the discrete substrate axioms.

### 2. Atomic Clock Validation Protocol (`validation_protocol.md`)
This document details the **experimental test** proposed in the paper to falsify the framework.

- **Prediction**: High-precision comparisons between a ground-based atomic clock and a satellite-borne clock will reveal a residual periodic signal at the satellite's orbital frequency (**f<sub>orb</sub> ≈ 1.7 × 10<sup>-4</sup> Hz**).
- **Protocol**: The protocol outlines the steps for data collection, spectral analysis, and noise modeling required to detect this signature, which arises from the intrinsic symmetry breaking of the discrete substrate during periodic motion.

> **Note on Atomic Clock Simulation Code**: The paper references specific scripts (`clock_comparison.py`, `power_spectrum.py`) for generating the predicted 1.7e-4 Hz signal. These files are part of the complete validation suite but are not included in this initial release. The core theoretical engine (`substrate_sim.py`) and the experimental protocol (`validation_protocol.md`) are provided here to establish the foundation. The full atomic clock simulation package will be released in conjunction with the ACES mission data analysis timeline.

## Quick Start

To run the cosmic evolution simulator:

1.  Ensure you have Python 3.8 or higher installed.
2.  Install the required dependencies:
    ```bash
    git clone https://github.com/myheast333/thermodynamic-arrow-substrate.git
    cd thermodynamic-arrow-substrate
    python -m venv substrate_env
    pip install numpy numpy matplotlib pandas scipy
    ```
3.  Execute the simulation:
    ```bash
    python substrate_sim.py
    ```
    This will generate a high-resolution plot (`cosmic_dynamic_precision.png`) and print a detailed summary of the simulation results and key conclusions.

## Key Features

*   **First-Principles Derivation**: Provides a geometric, non-statistical origin for the Second Law.
*   **Falsifiable Prediction**: Offers a concrete, testable signature (1.7e-4 Hz peak) for experimental physics.
*   **Paradox Resolution**: Naturally resolves Loschmidt's reversibility paradox.
*   **Cosmological Consistency**: Links the thermodynamic arrow to a growing dynamic precision horizon, aligning with cosmic evolution.
*   **Open & Reproducible**: All core simulation code is open-source and requires only standard scientific Python libraries.

## Citation

If you use this work in your research, please cite the original paper:

```bibtex
@article{Zhou2026GeometricOrigin,
  title={The Geometric Origin of the Second Law: Irreducible Informational Differences in a Discrete Substrate},
  author={Zhou, Jingsong},
  journal={In Preparation for IPI Letters},
  year={2026}
}
