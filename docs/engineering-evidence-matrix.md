# Engineering Evidence Matrix

This file is the final verification/validation map for the repository. It distinguishes **model verification**, **cross-model validation**, **sensitivity/robustness checks**, and **limitations** so that successful code execution is not confused with physical validation.

| Engineering question | Method / criterion | Retained evidence | Result | Status / limitation |
|---|---|---|---|---|
| Does the electrical loss model reproduce the dominant conduction term? | Analytical `I²RDS(on)D` vs waveform-separated LTspice conduction at 10 A | `electrical-model/notebook/mosfet_loss_calculation_main.ipynb` | 0.695 W analytical vs ~0.667 W LTspice; ~4% difference | **Pass** for conduction cross-check |
| Why does total analytical loss differ from LTspice? | Decompose conduction and switching; inspect VDS/ID transitions | same notebook + `LTspice_run_notes.md` | LTspice total is ~44.8% lower when normalised to analytical; discrepancy dominated by simplified datasheet-transition switching estimate | **Explained model-form uncertainty**, not forced agreement |
| Does the analytical thermal network agree with the retained ANSYS baseline? | Compare junction-temperature estimates; practical guide <10% of temperature rise | `thermal-model/thermal_resistance_estimate.ipynb` | 33.22°C analytical vs 32.88°C ANSYS-derived; 0.34°C absolute, ~4.2% of ANSYS rise above ambient | **Pass** |
| Is the FEA result mesh independent? | 5.0 / 2.5 / 2.0 mm global meshes; final change <2% of temperature rise | `thermal-model/mesh_independence.ipynb` | 30.628 / 30.631 / 30.633°C; medium→fine = 0.002°C ≈ 0.0355% of rise | **Pass** |
| Is electro-thermal coupling sensitive to the initial temperature guess? | Start 20 A aluminium loop from 25 / 75 / 125°C | `coupled-simulation/electro_thermal_coupling.ipynb` | all converge near 53.15°C; spread <0.02°C | **Pass** |
| Is dedicated cooling necessary in the adopted model? | Conservative datasheet-based no-heat-sink coupled reference | coupled notebook + `results/master_results.csv` | 10 A reference reaches ~183.84°C, above 175°C absolute limit | **Yes within the stated reference model**; not an experimental claim |
| Does material screening justify aluminium? | Equal-geometry 15 W comparison including temperature, mass and raw-material cost | `materials/material_eee.ipynb` + master results | copper ~1.97°C cooler but ~3.30× heavier and far higher raw-material cost | **Aluminium screened in** for system-level optimisation |
| Is the selected geometry the lightest tested feasible design? | Minimise aluminium mass subject to Tj ≤125°C at 15 W, 25°C ambient | `results/engineering_assessment.ipynb` | 80 mm passes; 60 mm passes and is 25% lighter; 40 mm fails | **60 mm / 6 fins is the minimum-mass tested feasible candidate** |
| Does the recommendation remain valid under convection uncertainty? | First-order h = 5 / 10 / 15 W/m²K sensitivity | engineering assessment | at h=10, 60 mm passes and 40 mm fails; at h=5 none pass | **Conditional recommendation**, uncertainty explicitly exposed |
| Are extrapolated scalability claims bounded? | Effective thermal-resistance thresholds and estimated current thresholds labelled as extrapolative | engineering assessment | approximate 125°C heat-load thresholds 19.1 / 17.3 / 14.4 W | **Useful ranking only**, not safe operating limits |
| Are mass and cost data traceable? | Geometry-derived volume × sourced density × sourced commodity benchmark | `data/heatsink_mass_comparison.csv`, `docs/sources.md` | aluminium/copper mass and GBP raw-material values reproduce from inputs | **Pass**; raw material only, not manufacturing quotation |
| Is the final data table internally consistent? | Automated case-ID, margin, mass, cost and decision checks | `scripts/validate_repository.py` | script must end with `ALL REPOSITORY CHECKS PASSED` | **Automated verification** |

## Final evidence boundary

The project is a **simulation-led digital prototype**. It does not claim experimental hardware validation, conjugate natural-convection CFD, a quantitative ANSYS energy-balance check, continuous topology optimisation, or a globally optimal heat-sink geometry.

The native ANSYS project/archive is unavailable for inclusion. The final retained FEA evidence is therefore the documented model specification, result tables, screenshots, analytical cross-check and mesh-convergence study. Exact GUI-level reconstruction cannot be guaranteed without the native archive.

Within those boundaries, the final engineering claim is deliberately narrow and defensible:

> **Among the three tested aluminium candidates, the 60 mm / 6-fin heat sink with fixed TGP5000 is the minimum-mass design that satisfies the project-defined Tj ≤125°C requirement at 15 W and 25°C ambient under the baseline prescribed natural-convection condition.**
