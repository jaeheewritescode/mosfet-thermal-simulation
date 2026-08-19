# Sources

The mass/cost/manufacturability extension uses the following engineering references. Prices are benchmark snapshots used only for relative material comparison, not supplier quotations.

- Aluminum Association — Alloy 6061 density / general 6xxx-series properties: https://www.aluminum.org/sites/default/files/2021-10/6061CombustibilityReport.pdf
- Aluminum Association — 6xxx-series extrusion/industry information: https://www.aluminum.org/standards
- Copper Development Association — C11000 high-conductivity copper properties: https://alloys.copper.org/alloy/C11000
- Hydro — 6061-T6 extrudability and machinability: https://www.hydro.com/us/us/aluminum/products/extruded-profiles/north-america-resources/extruded-aluminum-products/aluminum-extrusion-alloys/6061-t6-aluminum-properties/
- London Metal Exchange — official-price methodology/reference data: https://www.lme.com/market-data/reports-and-data/lme-official-prices
- Reuters, 18 Aug 2026 — aluminium three-month benchmark around $3,270/t, used as the aluminium price snapshot: https://www.reuters.com/commentary/reuters-open-interest/china-eases-iran-war-aluminium-shock-cost-2026-08-18/
- Reuters, 19 Aug 2026 — copper cash price $14,912/t, used as the copper price snapshot: https://www.reuters.com/commentary/reuters-open-interest/lme-gripped-by-flash-squeeze-copper-tensions-boil-over-2026-08-19/

## Cost-model caveat

The project calculates only **raw material content cost = mass × benchmark price per kg**. It excludes extrusion/machining conversion cost, tooling, cutting, finishing, scrap, labour, overhead, transport, supplier margin, minimum-order effects and taxes.
