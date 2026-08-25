# Sources

This file lists the main external sources used to support the electrical, thermal, manufacturability, and raw-material cost assumptions in the MOSFET electro-thermal simulation project.

Project-generated results such as ANSYS temperatures, calculated junction temperatures, heat-sink volumes, masses, mass reductions, and final engineering recommendations are not external references and therefore are not listed here as source material.

## MOSFET and Electrical Modelling

1. **Infineon Technologies / International Rectifier — IRFZ44NPbF Product Data Sheet**  
   Used for MOSFET electrical and thermal parameters including on-state resistance, switching characteristics, maximum junction temperature, and junction-to-case thermal resistance.  
   https://www.infineon.com/assets/row/public/documents/24/49/infineon-irfz44n-datasheet-en.pdf

2. **Analog Devices — AN-140: Basic Concepts of Linear Regulator and Switching Mode Power Supplies**  
   Used to support the ideal buck-converter relationship between input voltage, output voltage, and duty cycle.  
   https://www.analog.com/en/resources/app-notes/an-140.html

3. **Texas Instruments — Power MOSFET Gate Driver Bias Optimization, SLUA958**  
   Used to support the MOSFET conduction-loss and switching-loss equations used in the analytical electrical model.  
   https://www.ti.com/lit/ug/slua958/slua958.pdf

4. **Analog Devices — LTspice Simulator**  
   Used as the official reference for the LTspice electrical simulation environment.  
   https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html

## Thermal Modelling

5. **Ansys — Getting Started with Mechanical: Steady-State Thermal Solution – Heat Sink**  
   Used to support the steady-state thermal modelling approach and heat-sink simulation methodology in Ansys Mechanical.  
   https://ansyshelp.ansys.com/

6. **Ansys — Convection Heat Transfer**  
   Used to support convection boundary-condition concepts and the convection thermal-resistance relationship.  
   https://ansyshelp.ansys.com/

7. **Infineon Technologies — Recommendations for Assembly of Infineon TO Packages**  
   Used to support the series thermal-resistance network from semiconductor junction through the package, interface, heat sink, and ambient environment.  
   https://www.infineon.com/assets/row/public/documents/24/42/infineon-applicationnote-package-recommendations-assembly-topackages-applicationnotes-en.pdf

8. **Infineon Technologies — Infineon Small Signal MOSFETs: General Information**  
   Used to support the relationship between dissipated power, thermal resistance, and junction-temperature rise.  
   https://www.infineon.com/assets/row/public/documents/24/42/infineon-small-signal-products-applicationnotes-en.pdf

## Material and Thermal-Interface Properties

9. **Henkel — BERGQUIST GAP PAD TGP 5000**  
   Used for the fixed TIM conductivity of **5.0 W/mK** and to confirm that 1.5 mm lies within the published standard-thickness range.  
   https://next.henkel-adhesives.com/us/en/products/thermal-management-materials/central-pdp.html/bergquist-gap-pad-tgp-5000/112226IB.html

10. **Copper Development Association — C11000 Alloy**  
    Used for grade-specific C11000 physical properties. The project uses **8.91 g/cm³** density. The thermal-conductivity input is retained as **390 W/mK**, a rounded project value close to the CDA grade data.  
    https://alloys.copper.org/alloy/C11000

## Manufacturability and Industrial Use

11. **Hydro — 6061-T6 Aluminum Properties**  
   Used to support aluminium 6061-T6 numerical properties and manufacturability. Hydro reports specific gravity **2.70** and typical thermal conductivity of approximately **167 W/mK**; the project uses **170 W/mK** as a rounded engineering input. The source also supports extrusion and machining suitability.  
   https://www.hydro.com/us/us/aluminum/products/extruded-profiles/north-america-resources/extruded-aluminum-products/aluminum-extrusion-alloys/6061-t6-aluminum-properties/

## Raw-Material Cost Data

12. **World Bank — World Bank Commodities Price Data (The Pink Sheet), August 2026**  
    Used for the July 2026 aluminium and copper monthly-average benchmark commodity prices: **US$3,161/metric tonne aluminium** and **US$13,543/metric tonne copper**.  
    https://www.worldbank.org/en/research/commodity-markets

13. **Bank of England — Exchange rates against Sterling, July 2026 monthly average**  
    Used to convert the World Bank US-dollar commodity prices into pounds sterling. The July 2026 monthly average is **£1 = US$1.3379**.  
    https://www.bankofengland.co.uk/boeapps/database/Rates.asp?into=GBP&rateview=A

The repository converts the benchmark prices using:

**GBP/kg = (USD/metric tonne ÷ 1000) ÷ 1.3379**

This gives approximately **£2.363/kg aluminium** and **£10.123/kg copper**.

## Cost-Model Caveat

The project estimates only:

**Raw-material cost = heat-sink mass × benchmark material price per kg**

The calculated values are intended for comparative engineering analysis only. They do **not** represent finished heat-sink purchase prices and exclude extrusion, machining, cutting, tooling, surface finishing, scrap, labour, transport, supplier margin, taxes, and production-volume effects.

## Notes on Project-Derived Results

The following values are outputs of this project and therefore do not require external references:

- ANSYS case-temperature results
- calculated MOSFET junction temperatures
- calculated heat-sink volumes
- aluminium and copper heat-sink masses
- 25% and 50% geometry mass reductions
- raw-material cost calculations after applying the sourced benchmark price
- thermal-margin comparisons
- final geometry and material engineering recommendation
