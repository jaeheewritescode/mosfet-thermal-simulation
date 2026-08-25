## Frozen Thermal Model Settings

The thermal-model settings below are reused for controlled comparisons unless a specific sensitivity study intentionally changes one of them.

- Analysis type: steady-state thermal
- Ambient temperature: 25°C
- Natural-convection coefficient: 10 W/m²K for the baseline ANSYS model
- MOSFET heat-source area: 15.8 mm × 10.0 mm = 0.000158 m²
- TIM: TGP5000, fixed at 1.5 mm and 5 W/mK
- Reference heat sink: 80 mm × 50 mm × 5 mm aluminium baseline geometry with 8 fins
- Heat input method: total heat flow or equivalent heat flux applied to the MOSFET source/contact face; only one method is used at a time
- Contact treatment: retained consistently between controlled cases
- Junction-temperature interpretation: ANSYS package/case temperature plus junction-to-case temperature rise where required

## Completed Validation Evidence

- The 1.505 W aluminium baseline was compared with an independent thermal-resistance network.
- Analytical Tj ≈ 33.22°C and ANSYS-derived Tj ≈ 32.88°C, a difference of about 1%.
- A three-level mesh-independence study was completed using global element sizes of **5.0 mm, 2.5 mm and 2.0 mm**.
- The corresponding maximum temperatures were **30.628°C, 30.631°C and 30.633°C**.
- The medium-to-fine change was approximately **0.0065%**, and the coarse-to-fine change approximately **0.0163%**, both far below the project criterion of 2%.
- A 1.25 mm refinement was attempted but exceeded the ANSYS Student node/element limit; the already stabilised 5.0/2.5/2.0 mm sequence provides the retained mesh-convergence evidence.
- The **2.5 mm medium mesh** is retained as the project compromise between computation and numerical accuracy.
- Electrically derived and imposed/fixed thermal loads are kept separate in the data files.

The quantitative calculation and plot are stored in `mesh_independence.ipynb`.

## Evidence Boundary

A separate quantitative ANSYS energy-balance result is **not included or claimed** in the final validation evidence. The remaining repository artifact is the full archived ANSYS project/model file held by the materials collaborator.

## Controlled-Comparison Rule

For material and geometry comparisons, the TIM and other boundary conditions are held fixed. Only the intended heat-sink variable is changed. The first-order convection-coefficient sensitivity in `results/engineering_assessment.ipynb` is explicitly labelled as a separate uncertainty study rather than part of the frozen ANSYS comparison.
