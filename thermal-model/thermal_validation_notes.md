## Frozen Thermal Model Settings

The validated thermal-model settings below will be reused for all later design comparisons unless a specific comparison or sensitivity study intentionally changes one of them.

- Analysis type: Steady-state thermal
- Ambient temperature: 25°C
- Natural-convection coefficient: 10 W/m²K
- MOSFET heat-source area: 15.8 mm × 10.0 mm = 0.000158 m²
- TIM thickness: 1.5 mm
- TIM thermal conductivity: 5 W/mK
- Reference heat sink: current validated baseline geometry
- Reference material: aluminium
- Heat input method: total heat flow or equivalent heat flux applied to the MOSFET source/contact face
- Contact treatment: keep identical to the validated baseline model
- Mesh: ANSYS default mesh, validated through a mesh-independence check; further refinement produced negligible change in maximum temperature
- Junction-temperature interpretation: Ansys package/case temperature plus junction-to-case temperature rise where required

These settings define the validated reference model. For controlled comparisons, only the intended design variable is changed while the remaining settings are kept consistent.