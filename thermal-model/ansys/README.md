# ANSYS Model Handoff

The full ANSYS project/archive is held by the materials collaborator and will be added to this folder when available.

Until that file is committed, the repository records the model setup through the thermal notebooks, CSV results, validation notes and screenshots.

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
- Electrically derived heat loads: 0.534 W, 1.505 W, 4.760 W
- Imposed thermal-stress loads: 10 W and 15 W
- Junction conversion used in the project: Tj = Tc + P × RθJC with RθJC = 1.5°C/W

## Pending validation evidence

The archived model should eventually be accompanied by the quantitative mesh-independence and energy-balance evidence planned for the final validation pass.
