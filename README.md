# Electro-Thermal Optimisation of a Power MOSFET Cooling System

## Engineering Problem

This project investigates the cooling of an **IRFZ44N power MOSFET** in a **24 V to 12 V non-synchronous buck converter**. MOSFET conduction and switching losses become heat; as junction temperature rises, `RDS(on)` also rises, which increases conduction loss and creates positive electro-thermal feedback.

The engineering problem is therefore not simply to produce the lowest possible temperature. A larger or more conductive heat sink can improve thermal performance, but it can also increase **mass, raw-material cost, packaging burden and manufacturing complexity**.

The project asks:

> **Which passive heat-sink material and tested geometry provide the most practical solution while maintaining the required thermal margin?**

### Why dedicated cooling is required

Under the **conservative datasheet-based junction-to-ambient no-heat-sink reference**, the 10 A coupled case exceeds the **175°C absolute device limit**, while the baseline aluminium heat sink holds the coupled 10 A junction temperature to approximately **33.1°C**.

| 10 A cooling configuration | Junction temperature | Result |
|---|---:|---|
| No heat sink | 183.84°C | Exceeds 175°C device limit |
| 80 mm aluminium heat sink | 33.11°C | Large thermal margin |
| 80 mm copper heat sink | 32.90°C | Large thermal margin |

This establishes the problem before optimisation: **a heat sink is necessary, but unnecessary heat-sink material should be avoided.**

## Fixed Scope

The final project deliberately keeps the thermal interface fixed so that heat-sink material and geometry can be compared cleanly.

- Converter: 24 V to 12 V non-synchronous buck converter
- MOSFET: IRFZ44N
- Electrical operating points: 5 A, 10 A and 20 A
- Cooling mode: passive natural convection
- Ambient temperature: 25°C
- TIM: **TGP5000, 1.5 mm, 5 W/mK - fixed for all heat-sink comparisons**
- Heat-sink materials: aluminium 6061-T6 and copper C11000
- Tested aluminium/copper geometries: 80 mm / 8 fins, 60 mm / 6 fins and 40 mm / 4 fins
- Thermal-stress loads: imposed 10 W and 15 W cases

**Not investigated:** TIM optimisation, aluminium/copper hybrid construction, forced-air CFD, liquid cooling, physical hardware, detailed semiconductor-chip modelling or continuous topology optimisation.

## Design Requirement and Optimisation Objective

The final design decision is formulated as a **discrete constrained optimisation** rather than a subjective "best compromise".

### Thermal design requirement

> **Maintain MOSFET junction temperature `Tj <= 125°C` at 15 W imposed thermal dissipation and 25°C ambient temperature.**

- **125°C** is a project-defined engineering target selected to retain a **50°C margin** below the 175°C absolute maximum; it is not presented as an Infineon-recommended continuous operating temperature.
- **175°C** is treated as the absolute IRFZ44N junction-temperature limit, not a recommended operating target.
- **15 W** is a deliberately demanding imposed thermal-stress design point, above the electrically derived loss envelope in this project, used to expose cooling headroom and distinguish the candidate geometries. It is not assigned to a converter current unless independently produced by the electrical model.

### Optimisation objective

> **Among the tested aluminium heat-sink geometries, minimise heat-sink mass and raw-material use subject to the 125°C thermal constraint.**

This is a **discrete parametric optimisation across three tested candidates**, not a continuous fin/topology optimisation.

## Simulation Workflow

The project follows one connected engineering chain:

**Electrical operating condition -> MOSFET loss -> temperature-dependent RDS(on) -> thermal response -> updated junction temperature -> design screening -> constrained geometry selection -> scalability assessment**

Tools used:

- **LTspice** - buck-converter electrical simulation
- **Python** - analytical loss model, electro-thermal coupling and engineering assessment
- **ANSYS Steady-State Thermal** - heat-sink thermal simulations

The electrically derived 5 A / 10 A / 20 A cases are kept separate from the imposed 10 W / 15 W thermal-stress cases.

## Simulation Models

#### LTspice Electrical Model

![alt text](/electrical-model/images/LTSpice.png)

The 24 V to 12 V non-synchronous buck converter was modelled in LTspice at
5 A, 10 A and 20 A operating points. MOSFET voltage and current waveforms
were used to validate the analytical electrical-loss model.

#### ANSYS Thermal Model

![alt text](/thermal-model/images/Ansys_1.png)

A steady-state thermal model was used to predict the MOSFET and heat-sink
temperature response under prescribed natural-convection conditions.
Electrical MOSFET losses and imposed thermal-stress loads were applied as
heat inputs to the thermal model.



## Quick Start

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run results/app.py
```

Run notebooks from their own repository directories so that the documented relative CSV paths resolve correctly. To check the frozen data and decision logic without opening any notebook, run:

```bash
python scripts/validate_repository.py
```

The expected final line is `ALL REPOSITORY CHECKS PASSED`.

## Electrical Operating Envelope

For the baseline aluminium heat sink, the final coupled results are:

| Current | One-pass loss | Coupled loss | Coupled Tj | Margin to 125°C |
|---:|---:|---:|---:|---:|
| 5 A | 0.534 W | 0.537 W | 27.82°C | 97.18°C |
| 10 A | 1.505 W | 1.548 W | 33.11°C | 91.89°C |
| 20 A | 4.760 W | 5.371 W | 53.14°C | 71.86°C |

Electro-thermal feedback becomes increasingly important as current rises. At 20 A, the coupled loss is approximately **12.8% higher** than the one-pass 25°C estimate.

The reported efficiency is **MOSFET-loss-based efficiency**, not full converter efficiency.

## Coupling Robustness

The 20 A aluminium coupled case was also started from three different initial junction-temperature guesses. All converged to essentially the same solution:

| Initial Tj | Final Tj | Final MOSFET loss | Iterations |
|---:|---:|---:|---:|
| 25°C | 53.141°C | 5.371 W | 4 |
| 75°C | 53.161°C | 5.375 W | 4 |
| 125°C | 53.156°C | 5.374 W | 5 |

The final temperatures differ by less than **0.02°C**, supporting numerical robustness of the coupled fixed-point solution to the initial temperature guess.

## Material Screening

Material selection is treated as a **screening step before geometry optimisation**.

At the 15 W baseline geometry:

| Material | Tj | Equal-geometry mass | Raw-material cost |
|---|---:|---:|---:|
| Aluminium | 103.595°C | 0.351 kg | £0.829 |
| Copper | 101.624°C | 1.158 kg | £11.725 |

Copper improves junction temperature by only **1.97°C**, while the same geometry is approximately **3.30x heavier** and has a much larger benchmark raw-material cost. Aluminium is therefore selected as the default system-level material for the geometry optimisation.

## Discrete Constrained Geometry Optimisation

The three aluminium candidates are evaluated against the 15 W / 125°C design requirement:

| Candidate | Tj at 15 W | Margin to 125°C | Mass | Mass reduction | Raw-material cost | Feasible? |
|---|---:|---:|---:|---:|---:|---|
| Original - 80 mm / 8 fins | 103.595°C | +21.405°C | 0.351 kg | 0% | £0.829 | Yes |
| **Geometry 1 - 60 mm / 6 fins** | **111.831°C** | **+13.169°C** | **0.263 kg** | **25%** | **£0.622** | **Yes** |
| Geometry 2 - 40 mm / 4 fins | 129.400°C | -4.400°C | 0.176 kg | 50% | £0.415 | No |

### Optimisation result

**Geometry 1 (60 mm aluminium) is the minimum-mass tested aluminium design that satisfies the 125°C requirement at 15 W.**

- The 80 mm design passes, but uses 33% more mass than Geometry 1.
- The 40 mm design is lighter, but violates the thermal requirement.
- The 60 mm design therefore has a clear engineering justification rather than being selected from temperature alone.

At the controlled **1.505 W fixed heat load**, the original / 60 mm / 40 mm aluminium temperatures are **32.885°C / 33.713°C / 35.475°C**. Reducing the sink from 80 mm to 60 mm therefore removes **25% of the mass for only about 0.83°C temperature penalty** at the baseline heat load.

## Scalability

### Electrical scalability

The 5 A -> 10 A -> 20 A study shows that increasing current raises MOSFET loss nonlinearly and makes temperature-dependent `RDS(on)` feedback more important. This defines the electrically derived operating envelope without inventing additional current cases.

### Cooling-system scalability

At approximately steady, fixed-property conditions, geometry differences are best interpreted through thermal resistance: as heat load increases, the same resistance difference produces a larger **absolute temperature penalty**, so geometry selection becomes more consequential as the design approaches its thermal constraint.

Using each aluminium design's 15 W FEA temperature to estimate effective thermal resistance:

| Geometry | Effective Rth from 15 W result | Estimated heat load at 125°C |
|---|---:|---:|
| 80 mm | 5.240°C/W | 19.09 W |
| 60 mm | 5.789°C/W | 17.27 W |
| 40 mm | 6.960°C/W | 14.37 W |

These are **estimated thermal-capacity thresholds**, not experimentally verified limits. They show the order in which the designs lose compliance as required heat dissipation increases.

## Natural-Convection Uncertainty

Natural convection is a major uncertainty in passive cooling. A first-order analytical sensitivity uses the documented geometry, fixed TIM and aluminium properties while varying the convection coefficient `h`.

| Aluminium geometry | Tj at h=5 W/m²K | Tj at h=10 W/m²K | Tj at h=15 W/m²K |
|---|---:|---:|---:|
| 80 mm | 134.6°C | 106.7°C | 97.4°C |
| 60 mm | 153.0°C | 115.9°C | 103.5°C |
| 40 mm | 189.5°C | 134.1°C | 115.7°C |

This sensitivity is intentionally conservative and first-order; it is not a replacement for ANSYS. It shows that the final recommendation is **conditional on the natural-convection environment**. At the baseline project assumption `h = 10 W/m²K`, the 60 mm design remains feasible while the 40 mm design does not. Under weak convection (`h = 5 W/m²K`), none of the tested passive designs meets the 125°C / 15 W requirement.

## Manufacturability and Industrial Scalability

The heat sinks use straight fins and are compatible with an extrusion-led aluminium manufacturing route. However, the 80 / 60 / 40 mm dimension is the dimension **across which the fins are distributed**, and the fin count changes 8 -> 6 -> 4. The three candidates therefore do **not** represent one identical extrusion cross-section simply cut to different lengths.

A realistic manufacturing interpretation is:

- a custom extruded profile can be used for a selected production design,
- changing base width and fin count changes the cross-section and can require a different die/profile,
- low-volume prototypes may be produced by machining or trimming suitable standard stock,
- high production volume can justify a dedicated extrusion die for the final selected geometry,
- the lower mass of the 60 mm aluminium design reduces material use, handling and mounting burden compared with the 80 mm baseline.

Copper remains technically viable when a small extra temperature reduction is worth the mass and material-cost penalty, but it is not the preferred material for this application.

## Estimated Current Thresholds

The repository also estimates the current at which each aluminium geometry reaches 125°C or 175°C using the coupled electrical model and interpolation/extrapolation of available thermal data.

These results are intentionally labelled **estimated current thresholds**, not "safe current limits", because the 60 mm and 40 mm models have fewer ANSYS heat-load points and values above the simulated range require extrapolation.

See `results/engineering_assessment.ipynb` for the calculation and limitations.

## Validation Status

Completed checks include:

- analytical thermal-resistance estimate versus ANSYS baseline: **0.34°C absolute difference**, approximately **4.2% of the ANSYS temperature rise above ambient**,
- analytical-versus-LTspice electrical comparison, including waveform decomposition showing about **4% difference** in the 10 A conduction-loss component,
- quantitative three-level mesh-independence study: **30.628°C / 30.631°C / 30.633°C** for 5.0 / 2.5 / 2.0 mm global element sizes; medium-to-fine absolute change **0.002°C**, approximately **0.0355% of temperature rise above ambient**,
- coupled 5 A / 10 A / 20 A operating solutions,
- convergence robustness from multiple starting temperatures,
- controlled material and geometry comparisons,
- natural-convection sensitivity, and
- separation of electrically derived and imposed thermal-stress cases.

The repository does **not** claim experimental hardware validation or a quantitative ANSYS energy-balance result. The native ANSYS project/archive is **not available for inclusion**, so the final FEA evidence is intentionally limited to the documented setup, result tables, screenshots and mesh study. This is a stated reproducibility limitation, not a pending project task.

## Reproducibility

The repository contains:

- the LTspice schematic: `electrical-model/BUCK_converter.asc`,
- LTspice run provenance: `electrical-model/LTspice_run_notes.md`,
- analytical and electro-thermal Python notebooks,
- frozen CSV input/result datasets,
- ANSYS result screenshots and documented boundary conditions,
- quantitative mesh-independence evidence in `thermal-model/mesh_independence.ipynb`, and
- a `requirements.txt` file for the Python environment.

The committed LTspice schematic preserves the **10 A baseline** load (`R1 = 1.2 ohm`). The recorded 5 A and 20 A LTspice results were obtained from the same schematic by changing only the load resistance to the corresponding operating-point value and recording the MOSFET average loss; separate `.asc` copies were not retained.

### Master-results data semantics

`results/master_results.csv` intentionally separates electrical and thermal quantities:

- for `Electrical` rows, `Heat_Load_W` is the conservative one-pass 25°C heat-load reference used to define the thermal-response point, while `MOSFET_Loss_W` is the final converged electro-thermal MOSFET loss;
- for `Thermal_Stress` and `Geometry` rows, `Heat_Load_W` is an imposed/fixed thermal load and `MOSFET_Loss_W` is therefore left blank;
- the fixed 1.505 W geometry-comparison rows have `Load_Current_A` left blank because they are **not coupled 10 A operating cases**, even though 1.505 W originates from the conservative 10 A one-pass reference.

The native ANSYS archive is unavailable. `thermal-model/ansys/README.md` records the retained model specification and the exact evidence boundary so the repository does not overstate FEA reproducibility.

## Final Recommendation

For the defined project conditions:

> **Use aluminium 6061-T6 with the 60 mm / 6-fin geometry and the fixed TGP5000 interface.**

The recommendation is based on the following engineering chain:

1. Under the conservative datasheet-based no-heat-sink reference, the 10 A case is thermally unacceptable.
2. Copper provides only a small thermal improvement relative to its mass/cost penalty, so aluminium is screened in.
3. The 40 mm aluminium design fails the 125°C requirement at 15 W.
4. The 80 mm aluminium design passes but uses more material than required.
5. The **60 mm aluminium design is the minimum-mass tested feasible design** at the defined 15 W stress requirement.
6. Thermal-capacity and convection-sensitivity results define where that recommendation stops being valid as demand or ambient cooling conditions worsen.

## Repository Structure

- `electrical-model/` - LTspice schematic, analytical MOSFET loss calculations and electrical evidence
- `thermal-model/` - thermal-resistance validation, geometry study, ANSYS evidence and model handoff notes
- `coupled-simulation/` - iterative electro-thermal coupling model and convergence robustness check
- `materials/` - mass, raw-material cost and manufacturability analysis
- `data/` - frozen inputs, case matrix and design data
- `results/` - master results and final engineering assessment
- `references/` - BibTeX bibliography
- `docs/` - project brief, engineering evidence matrix and traceable sources

`results/master_results.csv` is the final numerical source of truth for reported simulation cases.

## Cost Basis

World Bank July 2026 monthly-average commodity prices are **US$3,161/metric tonne aluminium** and **US$13,543/metric tonne copper**. The Bank of England July 2026 monthly-average exchange rate is **£1 = US$1.3379**.

The resulting benchmark raw-material values used in this repository are:

- Aluminium: **£2.363/kg**
- Copper: **£10.123/kg**

These are raw-material comparison values only; they exclude extrusion, machining, tooling, finishing, labour, scrap, transport, supplier margin and production-volume effects.

## References

See:

- `docs/engineering-evidence-matrix.md` for the verification/validation evidence and limitations,
- `docs/sources.md` for a readable source register,
- `references/references.bib` for the BibTeX bibliography.
