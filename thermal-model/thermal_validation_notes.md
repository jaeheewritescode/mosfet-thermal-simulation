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
- Electrically derived and imposed thermal-stress loads are kept separate in the data files.

## Validation Evidence Still To Be Added

The following items are intentionally **not claimed as complete in the repository yet**:

- quantitative three-level mesh-independence table,
- ANSYS energy-balance check,
- final archived ANSYS project/model file from the materials collaborator.

These will be added during the final validation stage. Until then, the repository should not describe mesh independence or energy balance as quantitatively demonstrated.

## Controlled-Comparison Rule

For material and geometry comparisons, the TIM and other boundary conditions are held fixed. Only the intended heat-sink variable is changed. The first-order convection-coefficient sensitivity in `results/engineering_assessment.ipynb` is explicitly labelled as a separate uncertainty study rather than part of the frozen ANSYS comparison.
