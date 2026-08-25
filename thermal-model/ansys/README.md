# ANSYS Model Handoff

The full ANSYS project/archive is held by the materials collaborator and will be added to this folder when available.

Until that file is committed, the repository records the model setup through the thermal notebooks, CSV results, validation notes, geometry images and ANSYS screenshots.

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

The retained mesh sequence is 5.0 / 2.5 / 2.0 mm with maximum temperatures 30.628 / 30.631 / 30.633°C; the medium-to-fine change is approximately 0.0065%.

A separate quantitative ANSYS energy-balance result is not claimed in the final evidence set.

## Remaining handoff item

- Full ANSYS project/archive from the materials collaborator.
