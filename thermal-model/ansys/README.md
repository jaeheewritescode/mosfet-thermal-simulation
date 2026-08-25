# ANSYS Model Handoff

The native ANSYS project/archive is **not included in this repository**. The project is therefore frozen using the retained model specification, thermal notebooks, CSV results, validation notes, geometry images and ANSYS screenshots. This is an explicit evidence boundary rather than a pending deliverable.

## Frozen baseline setup

- Steady-state thermal analysis
- Ambient temperature: 25°C
- Natural convection coefficient: 10 W/m²K
- MOSFET source/contact area: 15.8 mm × 10.0 mm
- TIM: TGP5000, 1.5 mm, 5 W/mK
- Baseline heat sink: 80 × 50 × 5 mm base with 8 fins
- Geometry 1: 60 × 50 × 5 mm base with 6 fins
- Geometry 2: 40 × 50 × 5 mm base with 4 fins
- Aluminium 6061-T6 and copper C11000 heat-sink material cases
- Electrically derived one-pass heat-load references: 0.534 W, 1.505 W, 4.760 W
- Imposed thermal-stress loads: 10 W and 15 W
- Junction conversion used in the project: Tj = Tc + P × RθJC with RθJC = 1.5°C/W

## Validation status

Quantitative mesh independence is complete and documented in:

- `../mesh_independence.ipynb`
- `../thermal_validation_notes.md`

The retained mesh sequence is 5.0 / 2.5 / 2.0 mm with maximum temperatures 30.628 / 30.631 / 30.633°C. The medium-to-fine absolute change is **0.002°C**, equivalent to approximately **0.0355% of temperature rise above ambient**.

A separate quantitative ANSYS energy-balance result is not claimed in the final evidence set.

## Native-model limitation

The original ANSYS project/archive is unavailable for inclusion. Exact GUI-level settings that are not captured in the retained documentation cannot therefore be independently audited. No stronger reproducibility claim is made.


## Reconstruction record

See `reconstruction_specification.md` for the consolidated retained model definition, loads, mesh evidence and explicit limits of reconstruction.
