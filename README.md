# Electro-Thermal Optimisation of a Power MOSFET Cooling System

## Project Overview

This project investigates the electro-thermal behaviour and cooling requirements of an IRFZ44N power MOSFET used in a 24 V to 12 V buck converter.

The project combines:

- analytical MOSFET loss calculations,
- LTspice electrical simulation,
- ANSYS steady-state thermal simulation,
- temperature-dependent MOSFET resistance,
- iterative electro-thermal coupling,
- heat-sink material comparison,
- heat-sink geometry comparison,
- thermal-stress analysis, and
- a Streamlit dashboard for presenting the final validated results.

The main engineering objective is to determine how electrical loading, MOSFET power loss, heat-sink material and heat-sink geometry affect junction temperature and thermal safety.

## Key Findings

- Cooling is essential: the 10 A no-heat-sink case exceeds the **175°C device limit**.
- All cooled **5 A, 10 A and 20 A** operating points remain below the **125°C project target**.
- Electro-thermal feedback becomes increasingly significant at higher current.
- Copper provides only a modest junction-temperature improvement over aluminium, while the same geometry is approximately **3.32× heavier**.
- The 60 mm aluminium geometry reduces heat-sink mass by **25%** relative to the original while remaining below the 125°C target at 15 W.
- The 40 mm aluminium geometry reduces mass by **50%**, but exceeds the 125°C project target at 15 W.
- Heat-sink geometry has a stronger influence than material under high thermal demand.
- At 20 A, the aluminium MOSFET loss increases from approximately **4.760 W one-pass** to **5.371 W coupled**, showing a feedback increase of about **12.8%**.
- Under a 15 W thermal-stress load, the 60 mm geometry is approximately **17.6–17.9°C cooler** than the 40 mm geometry.
- The current preferred design strategy is **aluminium + geometry optimisation + fixed TGP5000 TIM**.

## Electrical Operating Conditions

The electrically derived converter operating points are:

| Parameter | Value |
|---|---:|
| Input voltage | 24 V |
| Output voltage | 12 V |
| Switching frequency | 50 kHz |
| Duty cycle | 0.5 |
| MOSFET | IRFZ44N |
| Gate voltage | 10 V |
| Rise time | 60 ns |
| Fall time | 45 ns |
| Inductor | 40 µH |
| Electrical load currents | 5 A, 10 A, 20 A |

Two values of MOSFET Rds(on) are intentionally used:

- **0.0139 Ω** for direct analytical comparison with the LTspice MOSFET model.
- **0.0175 Ω** as the conservative datasheet maximum at 25°C for thermal and electro-thermal analysis.

## Modelling Workflow

The project follows the modelling chain:

**Converter operating point → MOSFET electrical loss → temperature-dependent Rds(on) → thermal model → junction temperature → updated MOSFET loss**

MOSFET conduction loss is estimated using:

**Pcond = I² × Rds(on) × D**

Switching loss is estimated using:

**Psw = 0.5 × Vin × I × (tr + tf) × fs**

The electrical and thermal models are coupled iteratively so that increased junction temperature raises Rds(on), which increases conduction loss and therefore produces additional heat.

The coupling continues until the junction-temperature change between iterations is below **0.1°C**.

## Final Electrical Results

The final coupled electrical results for the baseline heat-sink geometry are:

| Current | Material | MOSFET loss (W) | Junction temperature (°C) | MOSFET-loss-based efficiency (%) | Margin to 125°C (°C) |
|---:|---|---:|---:|---:|---:|
| 5 A | Aluminium | 0.537 | 27.82 | 99.11 | 97.18 |
| 10 A | Aluminium | 1.548 | 33.11 | 98.73 | 91.89 |
| 20 A | Aluminium | 5.371 | 53.14 | 97.81 | 71.86 |
| 5 A | Copper | 0.537 | 27.75 | 99.11 | 97.26 |
| 10 A | Copper | 1.546 | 32.90 | 98.73 | 92.10 |
| 20 A | Copper | 5.349 | 52.32 | 97.82 | 72.68 |

All cooled electrical operating points remain below the **125°C project junction-temperature target**.

The efficiency values reported here include MOSFET loss only and therefore should not be interpreted as complete converter efficiency.

## Thermal-Stress Cases

Two additional heat loads were imposed directly in the thermal model:

- **10 W**
- **15 W**

These cases are intentionally separate from the electrically derived 5 A, 10 A and 20 A converter operating points.

### Why the Thermal-Stress Cases Are Separate

The 10 W and 15 W values are **not calculated MOSFET losses corresponding to specific converter currents**.

They are imposed thermal loads used to investigate how the cooling system behaves when heat generation becomes substantially greater than the validated electrical operating range.

They therefore provide evidence of:

- cooling-system scalability,
- reduced thermal margin at high heat load,
- increasing importance of heat-sink geometry, and
- increasing relevance of material thermal conductivity.

They should not be interpreted as statements such as "10 W corresponds to a particular converter current".

### Baseline Thermal-Stress Results

| Heat load | Aluminium Tj (°C) | Copper Tj (°C) | Aluminium margin to 125°C | Copper margin to 125°C |
|---:|---:|---:|---:|---:|
| 10 W | 77.390 | 76.082 | 47.610°C | 48.918°C |
| 15 W | 103.595 | 101.624 | 21.405°C | 23.376°C |

Copper consistently reduces junction temperature, but the improvement remains relatively small compared with the effect produced by changing heat-sink geometry.

## Heat-Sink Geometry Study

Three heat-sink sizes were considered:

- **80 mm baseline geometry**
- **60 mm reduced geometry**
- **40 mm reduced geometry**

The reduced geometries were introduced to investigate whether the original heat sink was oversized for the normal electrical operating conditions.

At the 1.505 W baseline heat load, the temperature difference between the reduced geometries is relatively small.

Under the 15 W thermal-stress condition, however, the effect of geometry becomes much stronger.

| Geometry | Aluminium Tj at 15 W | Copper Tj at 15 W |
|---|---:|---:|
| 60 mm | 111.831°C | 110.259°C |
| 40 mm | 129.400°C | 128.140°C |

The 60 mm heat sink therefore gives approximately **17.6–17.9°C lower junction temperature** than the 40 mm heat sink at 15 W.

This demonstrates that geometry becomes increasingly important as thermal demand increases.

## Mass, Cost and Manufacturability

The thermal comparison was extended using the actual solid dimensions of the heat-sink base and fins. Each fin is **5.5 × 50 × 50 mm**. The original, Geometry 1 and Geometry 2 designs use **8, 6 and 4 fins**, respectively.

| Geometry | Total volume | Aluminium mass | Copper mass | Reduction vs original |
|---|---:|---:|---:|---:|
| Original — 80 mm | 130 cm³ | 0.351 kg | 1.165 kg | 0% |
| Geometry 1 — 60 mm | 97.5 cm³ | 0.263 kg | 0.874 kg | 25% |
| Geometry 2 — 40 mm | 65 cm³ | 0.176 kg | 0.582 kg | 50% |

For the same geometry, copper is approximately **3.32× heavier** than aluminium. The repository also includes a raw-material cost estimate based on an August 2026 benchmark snapshot (**£2.31/kg aluminium; £9.89/kg copper**). These values are used only for relative material comparison and do not represent finished heat-sink procurement cost. Manufacturing cost would additionally depend on extrusion/machining, tooling, finishing, labour, scrap, supplier margin and production volume.

Mass materially changes the geometry decision. Geometry 2 is 50% lighter than the original aluminium design, but at 15 W it reaches **129.400°C**, above the 125°C project target. Geometry 1 is 25% lighter than the original and remains at **111.831°C** at 15 W, making it the stronger balanced design when both mass and high-load thermal margin matter.

### Manufacturability and Industrial Use

Aluminium 6061-T6 is compatible with extrusion and secondary machining. Because the investigated designs retain a similar straight-fin cross-section, an industrial implementation could use an extruded heat-sink profile, cut it to the required length, machine mounting/contact features, apply any required finish, and assemble the MOSFET/TIM. This supports scalable production while reducing material use in the 60 mm and 40 mm variants.

Copper remains technically viable where its higher conductivity is valuable, but its substantially greater mass and raw-material cost make it harder to justify for this application given the comparatively small thermal improvement.

## Final Case Matrix

| Case group | Electrical current | Heat load | Material | Geometry | Purpose |
|---|---|---|---|---|---|
| Electrical | 5 A | Electrically derived | Aluminium / Copper | 80 mm baseline | Low-load coupled operation |
| Electrical | 10 A | Electrically derived | Aluminium / Copper | 80 mm baseline | Baseline coupled operation |
| Electrical | 20 A | Electrically derived | Aluminium / Copper | 80 mm baseline | High-load coupled operation |
| No heat sink | 10 A | Electrically derived | None | None | Demonstrate cooling requirement |
| Thermal stress | N/A | 10 W | Aluminium / Copper | 80 mm baseline | Cooling scalability |
| Thermal stress | N/A | 15 W | Aluminium / Copper | 80 mm baseline | Extreme thermal demand |
| Geometry | N/A | 1.505 W | Aluminium / Copper | 60 mm / 40 mm | Geometry comparison at baseline heat load |
| Geometry stress | N/A | 15 W | Aluminium / Copper | 60 mm / 40 mm | Geometry comparison at high thermal demand |

The matrix deliberately separates electrically derived operating points from imposed thermal-stress cases.

## Repository Structure

- `electrical-model/` — analytical MOSFET loss calculations and LTspice validation
- `thermal-model/` — thermal-resistance validation, geometry studies and ANSYS-related analysis
- `coupled-simulation/` — iterative electro-thermal coupling model
- `data/` — validated electrical and thermal input datasets
- `results/` — engineering assessment, master results CSV and Streamlit dashboard
- `references/` — datasheets and supporting engineering sources

The final validated project outputs are consolidated in:

`results/master_results.csv`

The Streamlit dashboard also uses this frozen dataset so that the displayed outputs remain consistent with the final engineering assessment.

## Engineering Recommendation

Considering **thermal performance, mass, raw-material cost and manufacturability together**, the preferred general-purpose design is **Geometry 1: a 60 mm aluminium 6061-T6 heat sink with the fixed TGP5000 TIM**.

The 60 mm aluminium design reduces heat-sink mass by **25%** relative to the original 80 mm geometry (**0.263 kg vs 0.351 kg**) while maintaining an estimated junction temperature of **111.831°C at the imposed 15 W stress load**, leaving approximately **13.17°C margin** to the 125°C project target.

The 40 mm Geometry 2 design is the strongest lightweight/compact option, reducing aluminium mass by **50%** to approximately **0.176 kg**. Its baseline thermal penalty is small, but its junction temperature reaches **129.400°C at 15 W**, so it is not the preferred design if the 125°C stress target must be maintained.

Copper produces slightly lower junction temperatures, but the same geometry is approximately **3.32× heavier** and has a much larger benchmark raw-material cost. The thermal improvement is therefore insufficient to justify copper as the default material for this design.

From a manufacturing perspective, aluminium provides a practical extrusion-led route and easier integration due to its lower mass. The final strategy is therefore:

**60 mm aluminium heat sink → fixed TGP5000 TIM → extrusion/cut-to-length manufacturing route → use 40 mm only for mass/volume-constrained normal-load applications → use copper only if a small additional thermal margin is worth the mass and cost penalty.**

## Assumptions

The principal assumptions used in the project are:

- Ambient temperature is fixed at **25°C**.
- Natural convection is represented using **h = 10 W/m²K**.
- TGP5000 TIM is fixed at **1.5 mm thickness** and **5 W/mK thermal conductivity**.
- MOSFET RθJC is taken as **1.5°C/W** for junction-temperature correction.
- Electrical switching loss is estimated using a simplified linear switching-overlap equation.
- Temperature dependence is represented primarily through MOSFET Rds(on).
- LTspice uses an idealised gate-drive source.
- ANSYS steady-state thermal analysis is used rather than transient thermal simulation.
- Validated ANSYS thermal-response data are interpolated during electro-thermal coupling instead of rerunning ANSYS at every iteration.
- The 10 W and 15 W cases are imposed thermal loads rather than electrically derived MOSFET losses.

## Limitations

The main limitations are:

- No physical hardware testing was performed.
- Analytical switching-loss equations simplify real switching behaviour.
- LTspice and analytical loss estimates do not match exactly because they model MOSFET switching differently.
- MOSFET-loss-based efficiency excludes diode, inductor, capacitor, PCB and gate-driver losses.
- The thermal model simplifies some package and contact details.
- Natural convection is represented using a fixed heat-transfer coefficient.
- Current-sweep results become less certain where thermal-response extrapolation is required.
- Cost, mass and manufacturability are not yet fully quantified.
- The results should therefore be interpreted as engineering simulation estimates rather than experimentally verified device ratings.

## Reproducibility

The project is structured so that the main downstream analysis can be regenerated using the saved validated datasets.

The main Python workflow consists of:

1. MOSFET loss equations and assumptions
2. Temperature-dependent MOSFET resistance
3. Analytical and LTspice electrical-loss comparison
4. Analytical thermal-resistance validation
5. Electro-thermal coupling
6. Engineering assessment
7. Streamlit results dashboard

Validated ANSYS results are stored as project data and are used as inputs to the coupling model.

The Streamlit dashboard reads the frozen `master_results.csv` dataset and presents:

- MOSFET loss
- MOSFET-loss-based efficiency
- junction temperature
- margin to the 125°C project target
- margin to the 175°C absolute device limit
- final cooling recommendation

## Sources

The project uses the following main engineering sources:

- **Infineon IRFZ44N datasheet** — MOSFET electrical parameters, maximum junction temperature, Rds(on), switching times and temperature dependence.
- **LTspice IRFZ44N model** — waveform-based electrical simulation and MOSFET power-loss comparison.
- **ANSYS steady-state thermal simulations** — heat-sink material, geometry and thermal-response results.
- **TGP5000 thermal-interface material data** — TIM thermal conductivity and thickness.
- Project-generated CSV datasets and Jupyter notebooks contain the frozen numerical inputs and validated simulation outputs.

Where datasheet curves are used, values extracted from graphical relationships are treated as engineering approximations rather than exact manufacturer-tabulated values.