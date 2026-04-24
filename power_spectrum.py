============================================================
POWER SPECTRAL DENSITY ANALYSIS
Substrate Ontology Experimental Test (V5.5)
============================================================

1. Loading residual data...
   ✅ Loaded 15,552,000 samples using pandas
   Time span: 180.0 days
   Sampling rate: 1.0 Hz
   Data range: -1.00e-10 to 1.00e-10
   DataFrame shape: (15552000, 2)
   Columns: ['time(s)', 'residual']

2. Computing power spectral density...
   Using Welch method with 8192-point segments
   Frequency resolution: 1.22e-04 Hz
   Frequency range: 0.00e+00 to 5.00e-01 Hz

3. Analyzing spectrum...
   Expected frequency: 1.700e-04 Hz
   Power at expected freq: 2.450e-17
   Peak frequency (1e-5-1e-3 Hz): 1.221e-04 Hz
   Peak power: 2.450e-17
   Frequency match: ✅ YES

4. Signal-to-Noise Ratio (SNR) analysis...
   Peak power: 2.450e-17
   Noise floor (median): 9.376e-21
   SNR: 34.17 dB
   Detection threshold: 3.0 dB
   Signal detected: ✅ YES

5. Generating visualization...
   ✅ Plot saved: power_spectrum_supports.png

6. Saving analysis results...
   ✅ Results saved: spectrum_analysis.txt

============================================================
ANALYSIS COMPLETE
============================================================

🎯 CONCLUSION: The simulated data supports the discrete substrate
   framework (V5.5) prediction with a clear signal at 1.7e-4 Hz.

📊 Output files:
   - power_spectrum_supports.png
   - spectrum_analysis.txt

⚠️  REMINDER FOR REAL EXPERIMENTS:
   Real satellite clock data requires relativistic corrections!
   See 'validation_protocol.md' for the complete 7-step protocol.
