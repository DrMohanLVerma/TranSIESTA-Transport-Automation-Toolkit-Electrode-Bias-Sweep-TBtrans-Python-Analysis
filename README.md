# TranSIESTA-Transport-Automation-Toolkit-Electrode-Bias-Sweep-TBtrans-Python-Analysis
Automated workflow for quantum transport simulations using SIESTA/TranSIESTA/TBtrans with Python-based post-processing tools for transmission, conductance, I–V characteristics, differential conductance, and eigenchannel analysis.
# TranSIESTA Transport Automation Toolkit

A complete automation and analysis toolkit for quantum transport calculations using:

- SIESTA
- TranSIESTA
- TBtrans
- Python post-processing tools

This repository provides a workflow from electrode calculations to bias-dependent transport analysis with publication-quality plotting utilities.

---

## Features

### Electrode automation

Automated electrode calculations:

✔ Creates electrode directory structure  
✔ Copies pseudopotentials automatically  
✔ Runs SIESTA electrode calculation  
✔ Generates electrode Hamiltonian files (`*.TSHS`, `*.HSX`)

---

### Transport automation

Automated bias-dependent transport workflow:

✔ Zero-bias initialization  
✔ Positive and negative bias sweep  
✔ Automatic continuation using previous density matrix  
✔ SCF convergence recovery strategy  
✔ Automatic TBtrans execution  
✔ Current extraction  
✔ IV data generation

Supported workflow:

Electrode
↓
TranSIESTA
↓
TBtrans
↓
Python Analysis
↓
Publication Figures

---

### Python analysis tools

Automatic generation of:

✔ Transmission spectra T(E)  
✔ Conductance spectrum G(E)  
✔ Normalized conductance G/G0  
✔ Conductance in μS  
✔ I–V characteristics (μA scale)  
✔ Differential conductance dI/dV  
✔ Transmission eigenchannels  
✔ Bias comparison plots  
✔ Publication-quality figures (600 dpi)

---

## Output files analyzed

### Transport files

| File | Significance |
|--------|--------------|
| scat.TBT.AVTRANS_Left-Right | Total transmission spectrum |
| scat.TBT.AVTEIG_Left-Right | Transmission eigenchannels |
| scat.TSCCEQ-* | Equilibrium contribution |
| scat.TSCCNEQ-* | Non-equilibrium contribution |
| scat.TSGF* | Green function data |
| IV.dat | Current-voltage data |

---

## Scientific quantities obtained

Transmission:

T(E)

Conductance:

G(E)=G₀T(E)

Conductance quantum:

G₀ = 2e²/h

Differential conductance:

dI/dV

Current:

I(V)

---

## Typical outputs

Transmission_comparison.png

Conductance_normalized.png

Conductance_microS.png

IV_curve.png

dIdV.png

scat_0.3/Eigenchannels.png

scat_0.5/Eigenchannels.png

scat_0.7/Eigenchannels.png

---

## Example applications

- Graphene nanoribbon transport
- Molecular junctions
- 2D material devices
- Spin transport
- Nanoelectronic devices
- Resonant tunneling systems
- Negative Differential Resistance studies

---

## Requirements

- SIESTA ≥5.x
- TranSIESTA
- TBtrans
- MPI
- Python ≥3.9

Python packages:

numpy

matplotlib

netCDF4

scipy

Install:

pip install numpy matplotlib scipy netCDF4

---

## Citation

If this workflow contributes to your research, please cite:

Mohan L Verma,
Computational Nanomaterial Research Laboratory

and cite:

Brandbyge et al.,
Density-functional method for nonequilibrium electron transport

Phys Rev B 65, 165401 (2002)

---

## Author

Dr Mohan L Verma  
Computational Nanomaterial Research Laboratory  
Department of Applied Physics  
SSGI, Bhilai, India

Website:
www.drmlv.in

Feedback:
drmohanlv@gmail.com

---

## License

MIT License
