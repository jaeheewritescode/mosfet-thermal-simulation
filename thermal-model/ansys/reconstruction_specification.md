# ANSYS Reconstruction Specification and Evidence Boundary

The native ANSYS project/archive is unavailable. This document records the final model information that **is** supported by the retained project evidence so that the FEA setup is auditable without implying exact native-file reproducibility.

## Analysis definition

- Analysis: **ANSYS Mechanical Steady-State Thermal**
- Ambient temperature: **25°C**
- Baseline prescribed convection coefficient: **10 W/m²K**
- Cooling representation: natural convection represented by a **prescribed film coefficient**; room airflow is not solved with CFD
- Heat-source/contact face: **15.8 mm × 10.0 mm = 158 mm²**
- TIM: **TGP5000**, fixed at **1.5 mm**, **5 W/mK**
- Junction conversion used after the simplified package/case result: **Tj = Tc + P × RθJC**, with **RθJC = 1.5°C/W**

## Heat-sink candidates

| Design | Base | Fins | Fin dimensions |
|---|---|---:|---|
| Original | 80 × 50 × 5 mm | 8 | 5.5 × 50 × 50 mm |
| Geometry 1 | 60 × 50 × 5 mm | 6 | 5.5 × 50 × 50 mm |
| Geometry 2 | 40 × 50 × 5 mm | 4 | 5.5 × 50 × 50 mm |

Materials compared: **Aluminium 6061-T6** and **Copper C11000**. The fixed numerical properties used by the repository are recorded in `../../data/material-properties.csv`.

## Thermal loads

Electrically derived one-pass references:

- 5 A: **0.534 W**
- 10 A: **1.505 W**
- 20 A: **4.760 W**

Separate imposed stress cases:

- **10 W**
- **15 W**

The 10 W and 15 W values are not assigned to converter current unless the electrical model independently produces those losses.

## Mesh evidence

The retained baseline aluminium mesh study uses global element sizes:

- 5.0 mm → 30.628°C
- 2.5 mm → 30.631°C
- 2.0 mm → 30.633°C

The medium-to-fine change is **0.002°C**, approximately **0.0355% of the temperature rise above 25°C ambient**. The 2.5 mm mesh is retained as the converged project compromise. A 1.25 mm attempt exceeded the ANSYS Student node/element limit.

## Retained FEA evidence

- `../geometry_variation.ipynb`
- `../thermal_resistance_estimate_cleaned.ipynb`
- `../mesh_independence.ipynb`
- `../thermal_validation_notes.md`
- `../images/Ansys_1.png`
- `../images/geometry_80mm.png`
- `../images/geometry_60mm.png`
- `../images/geometry_40mm.png`
- `../../data/thermal_response_aluminium.csv`
- `../../data/thermal_response_copper.csv`
- `../../results/master_results.csv`

## What cannot be reconstructed exactly

Without the native archive, exact GUI-level details that are not visible in the retained evidence—such as every Mechanical object setting, solver metadata or selection identifier—cannot be independently verified. The repository does not invent those settings and does not claim exact native-model reproducibility.
