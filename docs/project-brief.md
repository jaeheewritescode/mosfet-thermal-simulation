# Project Brief

## Problem

A power MOSFET in a buck converter dissipates conduction and switching losses. Junction-temperature rise increases `RDS(on)`, which can further increase conduction loss. A heat sink is therefore required, but an oversized or unnecessarily conductive design adds mass, raw-material cost and integration burden.

## Fixed Design Scope

- IRFZ44N MOSFET in a 24 V to 12 V buck converter
- 5 A, 10 A and 20 A electrically derived operating points
- Natural convection at 25°C ambient
- TGP5000 TIM fixed at 1.5 mm and 5 W/mK
- Aluminium 6061-T6 and copper C11000 screening
- 80 mm / 8-fin, 60 mm / 6-fin and 40 mm / 4-fin heat-sink candidates
- 10 W and 15 W imposed thermal-stress cases

TIM optimisation and aluminium/copper hybrid construction are outside the final scope.

## Design Requirement

**Tj <= 125°C at 15 W imposed thermal dissipation and 25°C ambient.**

The 175°C datasheet value is treated as an absolute limit, not the design target.

## Optimisation Objective

After material screening, select the **minimum-mass tested aluminium geometry** that satisfies the thermal requirement.

## Final Selection Logic

| Aluminium design | Tj at 15 W | Mass | Raw-material cost | Feasible? |
|---|---:|---:|---:|---|
| 80 mm / 8 fins | 103.595°C | 0.351 kg | £0.829 | Yes |
| **60 mm / 6 fins** | **111.831°C** | **0.263 kg** | **£0.622** | **Yes** |
| 40 mm / 4 fins | 129.400°C | 0.176 kg | £0.415 | No |

**Selected design: 60 mm / 6-fin aluminium heat sink with fixed TGP5000 TIM.**

It is the minimum-mass tested aluminium design that satisfies the 125°C / 15 W constraint.

## Scalability Question

The project then asks how close each design is to its thermal limit as electrical current, imposed heat dissipation or natural-convection conditions become more demanding. This is assessed through the 5/10/20 A coupled operating envelope, 10/15 W stress cases, effective thermal-capacity estimates and a convection-coefficient sensitivity.

## Remaining Finalisation Work

- refine analytical-versus-LTspice loss validation,
- add quantitative ANSYS mesh-independence and energy-balance evidence,
- add the ANSYS project/archive from the materials collaborator,
- refresh the final Streamlit dashboard after the data freeze.
