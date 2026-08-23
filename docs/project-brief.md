# Project Brief

## Engineering Problem

A power MOSFET in a buck converter dissipates energy through conduction and switching losses. As junction temperature rises, `RDS(on)` increases, which can further increase conduction loss and create electro-thermal feedback.

Dedicated cooling is therefore required. However, selecting the coolest possible heat sink is not automatically the best engineering solution because increased material volume or thermal conductivity can introduce unnecessary mass, raw-material cost, manufacturing complexity and integration burden.

The project therefore treats MOSFET cooling as a constrained engineering design problem rather than a temperature-minimisation problem alone.

---

## Project Aim

Develop and validate an electro-thermal model of an IRFZ44N MOSFET in a buck converter and use the model to select a practical passive heat-sink material and geometry.

The final design is selected using thermal performance, mass, raw-material cost, manufacturability and scalability rather than junction temperature alone.

---

## Fixed Design Scope

- IRFZ44N MOSFET
- 24 V to 12 V non-synchronous buck converter
- 5 A, 10 A and 20 A electrically derived operating points
- Natural-convection cooling
- 25°C ambient temperature
- TGP5000 TIM fixed at:
  - 1.5 mm thickness
  - 5 W/mK thermal conductivity
- Aluminium 6061-T6 and copper C11000 material screening
- Three discrete straight-fin heat-sink candidates:
  - Original: 80 mm / 8 fins
  - Geometry 1: 60 mm / 6 fins
  - Geometry 2: 40 mm / 4 fins
- 10 W and 15 W imposed thermal-stress cases

TIM optimisation and aluminium/copper hybrid construction are outside the final project scope.

The 10 W and 15 W cases are imposed thermal loads used to investigate cooling scalability. They are not assumed to correspond to a specific converter current.

---

## Engineering Design Requirement

The selected passive cooling design must satisfy:

**Tj ≤ 125°C at 15 W imposed thermal dissipation and 25°C ambient temperature.**

The IRFZ44N maximum junction-temperature rating of **175°C** is treated as an absolute device limit rather than the desired design operating temperature.

---

## Engineering Workflow

The project follows a connected modelling chain:

**Electrical operating point → MOSFET loss → junction temperature → temperature-dependent electrical loss → cooling design → engineering decision**

1. Analytical and LTspice models estimate MOSFET conduction and switching losses.
2. Ansys predicts heat-sink thermal response under natural convection.
3. Python couples temperature-dependent `RDS(on)` back into the electrical-loss model.
4. Aluminium and copper are screened at equal geometry.
5. Aluminium geometry candidates are evaluated under a defined thermal constraint.
6. Scalability and manufacturability are assessed before the final recommendation is made.

---

## Why Cooling Is Required

The no-heat-sink electro-thermal case demonstrates that the MOSFET cannot be treated as thermally independent from its electrical operating condition.

At the 10 A condition, electro-thermal feedback drives the no-heat-sink junction temperature beyond the device limit, whereas the baseline heat sink maintains a substantially lower junction temperature.

This establishes the engineering need for dedicated cooling before optimisation is considered.

---

## Material Screening

Copper provides greater thermal conductivity and slightly lower junction temperature than aluminium at equal geometry.

However, the thermal improvement is small relative to its substantially greater density, heat-sink mass and raw-material cost.

Aluminium 6061-T6 is therefore selected as the system-level material for the subsequent geometry optimisation.

The material comparison is treated as a **screening stage**, while geometry selection forms the main constrained optimisation.

---

## Optimisation Objective

The geometry study is a **discrete constrained optimisation** over three tested aluminium heat-sink candidates.

### Objective

Minimise heat-sink mass and raw-material use.

### Constraint

**Tj ≤ 125°C at 15 W and 25°C ambient.**

### Candidate Results

| Aluminium design | Tj at 15 W | Margin to 125°C | Mass | Mass reduction | Raw-material cost | Feasible? |
|---|---:|---:|---:|---:|---:|---|
| 80 mm / 8 fins | 103.595°C | +21.405°C | 0.351 kg | 0% | £0.829 | Yes |
| **60 mm / 6 fins** | **111.831°C** | **+13.169°C** | **0.263 kg** | **25%** | **£0.622** | **Yes** |
| 40 mm / 4 fins | 129.400°C | -4.400°C | 0.176 kg | 50% | £0.415 | No |

---

## Selected Design

**60 mm / 6-fin aluminium 6061-T6 heat sink with the fixed TGP5000 TIM.**

This design is selected because it is the **minimum-mass tested aluminium geometry that satisfies the 125°C junction-temperature requirement at 15 W**.

The 80 mm design provides greater thermal margin but uses more material than is required to satisfy the design constraint.

The 40 mm design provides the lowest mass but exceeds the thermal target and is therefore rejected.

The recommendation is consequently based on a measurable engineering constraint rather than on a subjective compromise.

---

## Scalability

The project investigates scalability in two complementary ways.

### Electrical scalability

The coupled 5 A, 10 A and 20 A operating points show how increasing current raises MOSFET loss and junction temperature while temperature-dependent `RDS(on)` introduces additional electro-thermal feedback.

### Cooling scalability

The 10 W and 15 W thermal-stress cases and effective thermal-resistance estimates show how each geometry approaches the 125°C design constraint as heat dissipation increases.

Approximate thermal-capacity thresholds are:

- 80 mm / 8 fins: **~19.1 W**
- 60 mm / 6 fins: **~17.3 W**
- 40 mm / 4 fins: **~14.4 W**

These values are engineering estimates rather than experimentally validated safe operating limits.

As thermal demand increases, the smallest geometry loses compliance first while the larger designs provide progressively greater thermal headroom.

---

## Validation

The project uses several independent checks before relying on the simulation results.

### Electrical validation

At the 10 A baseline case:

- Analytical conduction loss ≈ **0.695 W**
- LTspice waveform conduction loss ≈ **0.667 W**
- Difference ≈ **4%**

The larger analytical-versus-LTspice total-loss discrepancy was traced primarily to the simplified datasheet-based switching-transition model rather than the conduction model.

### Thermal validation

The Ansys baseline result was compared with an analytical thermal-resistance model.

### Mesh independence

Maximum temperature changed from:

- 5.0 mm mesh: **30.628°C**
- 2.5 mm mesh: **30.631°C**
- 2.0 mm mesh: **30.633°C**

The medium-to-fine difference is approximately **0.0065%**, substantially below the project's **2%** mesh-independence criterion.

### Electro-Thermal Convergence

The 20 A aluminium coupled model was started from junction temperatures of 25°C, 75°C and 125°C.

All starting conditions converged to approximately **53.15°C**, demonstrating that the final coupled solution is not dependent on the initial temperature assumption.

---

## Manufacturability

The straight-fin aluminium concept is compatible with conventional extrusion-based heat-sink manufacture.

However, reducing the 80 mm design to 60 mm and 40 mm also changes the number of fins and therefore changes the extrusion cross-section. The three geometries should not be interpreted as one identical extrusion profile simply cut to different lengths.

For higher-volume production, dedicated extrusion profiles may be justified. For prototypes or lower production volumes, machining or modification of standard heat-sink stock may be more practical.

The reported costs represent **raw-material content only** and exclude extrusion, tooling, machining, finishing, labour, scrap, transport and supplier margins.

---

## Final Engineering Conclusion

The project demonstrates a clear engineering progression:

**Problem:** electro-thermal feedback makes dedicated MOSFET cooling necessary.

**Optimisation:** minimise cooling-system mass while satisfying a defined junction-temperature constraint.

**Scalability:** quantify how electrical load, thermal demand and cooling geometry affect the available thermal margin.

Within the investigated design space, the **60 mm / 6-fin aluminium heat sink** provides the strongest system-level solution because it reduces heat-sink mass by approximately **25%** relative to the original design while remaining below the **125°C junction-temperature target at 15 W**.

The recommendation is conditional on the defined natural-convection environment and should not be interpreted as universally optimal outside the investigated operating and thermal conditions.

---

## Final Repository Status

Completed:

- electrical analytical model
- LTspice circuit and waveform validation
- temperature-dependent MOSFET loss model
- electro-thermal coupling
- no-heat-sink reference
- aluminium/copper material screening
- three-geometry thermal comparison
- mass and GBP raw-material cost analysis
- mesh-independence study
- coupling-convergence study
- convection sensitivity
- constrained geometry optimisation
- scalability assessment
- manufacturability assessment
- Streamlit engineering dashboard
- project references

Pending repository artifact:

- full Ansys project/archive from the materials collaborator
