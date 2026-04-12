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
