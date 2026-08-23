import streamlit as st
import pandas as pd
from pathlib import Path

# ------------------------------------------------------------
# Page setup
# ------------------------------------------------------------
st.set_page_config(
    page_title="MOSFET Cooling Optimisation Dashboard",
    layout="wide",
)

st.title("MOSFET Electro-Thermal Cooling Optimisation")
st.caption(
    "Problem → constrained optimisation → scalability for a passively cooled "
    "IRFZ44N buck-converter MOSFET."
)

# ------------------------------------------------------------
# Load project data
# ------------------------------------------------------------
HERE = Path(__file__).resolve().parent
POSSIBLE_PATHS = [
    HERE / "master_results.csv",
    HERE.parent / "results" / "master_results.csv",
    Path("results/master_results.csv"),
    Path("master_results.csv"),
]

RESULTS_PATH = next((p for p in POSSIBLE_PATHS if p.exists()), None)

if RESULTS_PATH is None:
    st.error(
        "Could not find master_results.csv. Run the app from the repository root "
        "with `streamlit run results/app.py`, or keep app.py beside master_results.csv."
    )
    st.stop()

df = pd.read_csv(RESULTS_PATH)

electrical = df[df["Scenario_Type"] == "Electrical"].copy()
thermal_stress = df[df["Scenario_Type"] == "Thermal_Stress"].copy()
geometry_results = df[df["Scenario_Type"] == "Geometry"].copy()
reference_results = df[df["Scenario_Type"] == "Reference"].copy()

TARGET_TJ = 125.0
ABSOLUTE_TJ_LIMIT = 175.0
AMBIENT_C = 25.0
BASELINE_GEOMETRY_LOAD_W = 1.505
DESIGN_STRESS_W = 15.0

GEOMETRY_INFO = {
    "Baseline": {
        "display": "Original",
        "label": "Original — 80 mm / 8 fins",
        "base_length_mm": 80,
        "fins": 8,
    },
    "Geometry_1": {
        "display": "Geometry 1",
        "label": "Geometry 1 — 60 mm / 6 fins",
        "base_length_mm": 60,
        "fins": 6,
    },
    "Geometry_2": {
        "display": "Geometry 2",
        "label": "Geometry 2 — 40 mm / 4 fins",
        "base_length_mm": 40,
        "fins": 4,
    },
}

LABEL_TO_GEOMETRY = {
    info["label"]: key for key, info in GEOMETRY_INFO.items()
}


def get_geometry_case(material_name, geometry_key, heat_load_w):
    """Return one controlled thermal geometry/material case, if available."""
    if geometry_key == "Baseline":
        # At 15 W the baseline case is stored as Thermal_Stress.
        if abs(heat_load_w - DESIGN_STRESS_W) < 1e-9:
            rows = thermal_stress[
                (thermal_stress["Material"] == material_name)
                & (thermal_stress["Heat_Load_W"] == heat_load_w)
                & (thermal_stress["Geometry"] == "Baseline")
            ]
        else:
            # The fixed 1.505 W baseline geometry comparison is stored as Geometry.
            rows = geometry_results[
                (geometry_results["Material"] == material_name)
                & (geometry_results["Geometry"] == "Baseline")
                & (geometry_results["Heat_Load_W"] == heat_load_w)
            ]
    else:
        rows = geometry_results[
            (geometry_results["Material"] == material_name)
            & (geometry_results["Geometry"] == geometry_key)
            & (geometry_results["Heat_Load_W"] == heat_load_w)
        ]

    if rows.empty:
        return None
    return rows.iloc[0]


# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
st.sidebar.header("Explore the Design")

current = st.sidebar.selectbox(
    "Electrical load current",
    [5.0, 10.0, 20.0],
    index=1,
)

material = st.sidebar.selectbox(
    "Heat-sink material",
    ["Aluminium", "Copper"],
)

geometry_label = st.sidebar.selectbox(
    "Heat-sink geometry",
    list(LABEL_TO_GEOMETRY.keys()),
    index=1,
)

selected_geometry = LABEL_TO_GEOMETRY[geometry_label]
selected_geometry_info = GEOMETRY_INFO[selected_geometry]

st.sidebar.caption(
    "Current and material control the coupled electrical operating-point view. "
    "Geometry controls the controlled thermal-design comparison. The reduced "
    "geometries were not simulated as fully coupled 5 A / 10 A / 20 A cases, "
    "so the dashboard keeps those datasets separate."
)

# ------------------------------------------------------------
# 1. Engineering problem
# ------------------------------------------------------------
st.header("1. Engineering Problem")

st.markdown(
    """
MOSFET conduction and switching losses generate heat. As junction temperature rises,
the device on-resistance increases, which can further increase electrical loss.
Dedicated cooling is therefore required, but an oversized heat sink adds unnecessary
mass, raw-material cost and integration burden.

**Design requirement**

> Select the minimum-mass tested passive heat-sink design that maintains
> **Tj ≤ 125°C at 15 W imposed thermal dissipation and 25°C ambient**.

The **175°C** value is treated as the absolute device limit rather than the desired
design operating temperature. The 15 W case is an imposed thermal-stress condition
and is not mapped to a converter current.
"""
)

st.subheader("Why dedicated cooling is required")

baseline_10a = electrical[
    (electrical["Load_Current_A"] == 10.0)
    & (electrical["Material"] == "Aluminium")
]

no_sink = reference_results[
    reference_results["Load_Point"].astype(str).str.lower() == "no heat sink"
]

if not baseline_10a.empty and not no_sink.empty:
    sink_tj = float(baseline_10a.iloc[0]["Junction_Temperature_C"])
    no_sink_tj = float(no_sink.iloc[0]["Junction_Temperature_C"])
    no_sink_loss = float(no_sink.iloc[0]["MOSFET_Loss_W"])

    c1, c2, c3 = st.columns(3)
    c1.metric("10 A with baseline Al heat sink", f"{sink_tj:.1f} °C")
    c2.metric("10 A no-heat-sink reference", f"{no_sink_tj:.1f} °C")
    c3.metric("No-heat-sink coupled loss", f"{no_sink_loss:.3f} W")

    if no_sink_tj > ABSOLUTE_TJ_LIMIT:
        st.error(
            "The coupled no-heat-sink case exceeds the 175°C device limit. "
            "Dedicated cooling is therefore required before optimisation."
        )

st.divider()

# ------------------------------------------------------------
# 2. Electrical operating envelope
# ------------------------------------------------------------
st.header("2. Electrical Operating Envelope")

selected_electrical = electrical[
    (electrical["Load_Current_A"] == current)
    & (electrical["Material"] == material)
]

if selected_electrical.empty:
    st.warning("No coupled electrical result is available for this current/material selection.")
else:
    row = selected_electrical.iloc[0]

    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Coupled MOSFET loss", f'{row["MOSFET_Loss_W"]:.3f} W')
    e2.metric("Junction temperature", f'{row["Junction_Temperature_C"]:.2f} °C')
    e3.metric("MOSFET-loss-based efficiency", f'{row["Efficiency_pct"]:.2f}%')
    e4.metric("Margin to 125°C target", f'{row["Margin_to_125C_C"]:.2f} °C')

    if row["Junction_Temperature_C"] <= TARGET_TJ:
        st.success("This electrically derived operating point is below the 125°C project target.")
    elif row["Junction_Temperature_C"] <= ABSOLUTE_TJ_LIMIT:
        st.warning(
            "This case exceeds the 125°C design target but remains below the "
            "175°C absolute device limit."
        )
    else:
        st.error("This case exceeds the 175°C absolute device limit.")

st.caption(
    "The 5 A / 10 A / 20 A results are electrically derived coupled cases for the "
    "baseline heat-sink geometry. Geometry variants are assessed separately under "
    "controlled thermal loads."
)

st.divider()

# ------------------------------------------------------------
# 3. Selected geometry snapshot
# ------------------------------------------------------------
st.header("3. Selected Geometry Snapshot")

g_base = get_geometry_case(
    material,
    selected_geometry,
    BASELINE_GEOMETRY_LOAD_W,
)
g_stress = get_geometry_case(
    material,
    selected_geometry,
    DESIGN_STRESS_W,
)

g1, g2, g3, g4 = st.columns(4)
g1.metric("Selected geometry", selected_geometry_info["display"])
g2.metric("Base length", f'{selected_geometry_info["base_length_mm"]} mm')
g3.metric("Number of fins", f'{selected_geometry_info["fins"]}')
if g_stress is not None:
    g4.metric("Mass", f'{float(g_stress["Mass_kg"]):.3f} kg')
elif g_base is not None:
    g4.metric("Mass", f'{float(g_base["Mass_kg"]):.3f} kg')
else:
    g4.metric("Mass", "N/A")

if g_base is not None or g_stress is not None:
    source_for_cost = g_stress if g_stress is not None else g_base

    s1, s2, s3, s4 = st.columns(4)

    if g_base is not None:
        s1.metric(
            f"Tj at {BASELINE_GEOMETRY_LOAD_W:.3f} W",
            f'{float(g_base["Junction_Temperature_C"]):.2f} °C',
        )
    else:
        s1.metric(f"Tj at {BASELINE_GEOMETRY_LOAD_W:.3f} W", "Not simulated")

    if g_stress is not None:
        stress_tj = float(g_stress["Junction_Temperature_C"])
        stress_margin = TARGET_TJ - stress_tj

        s2.metric("Tj at 15 W", f"{stress_tj:.2f} °C")
        s3.metric("Margin to 125°C", f"{stress_margin:.2f} °C")
        s4.metric(
            "Raw-material cost",
            f'£{float(source_for_cost["Estimated_Cost"]):.3f}',
        )

        if stress_tj <= TARGET_TJ:
            st.success(
                f"{geometry_label} in {material.lower()} satisfies the "
                "125°C / 15 W project constraint."
            )
        else:
            st.error(
                f"{geometry_label} in {material.lower()} does not satisfy the "
                "125°C / 15 W project constraint."
            )
    else:
        s2.metric("Tj at 15 W", "Not simulated")
        s3.metric("Margin to 125°C", "N/A")
        s4.metric(
            "Raw-material cost",
            f'£{float(source_for_cost["Estimated_Cost"]):.3f}',
        )
else:
    st.warning("No controlled geometry result was found for this selection.")

st.caption(
    "Raw-material cost represents material content only; it excludes extrusion, "
    "tooling, machining, finishing, labour, transport and supplier margin."
)

st.divider()

# ------------------------------------------------------------
# 4. Material screening
# ------------------------------------------------------------
st.header("4. Material Screening")

material_15w = thermal_stress[
    thermal_stress["Heat_Load_W"] == DESIGN_STRESS_W
].copy()

if {"Aluminium", "Copper"}.issubset(set(material_15w["Material"].dropna())):
    al = material_15w[material_15w["Material"] == "Aluminium"].iloc[0]
    cu = material_15w[material_15w["Material"] == "Copper"].iloc[0]

    thermal_gain = float(
        al["Junction_Temperature_C"] - cu["Junction_Temperature_C"]
    )
    mass_ratio = float(cu["Mass_kg"] / al["Mass_kg"])
    cost_ratio = float(cu["Estimated_Cost"] / al["Estimated_Cost"])

    m1, m2, m3 = st.columns(3)
    m1.metric("Copper thermal advantage @ 15 W", f"{thermal_gain:.2f} °C")
    m2.metric("Copper / aluminium mass ratio", f"{mass_ratio:.2f}×")
    m3.metric("Copper / aluminium raw-cost ratio", f"{cost_ratio:.1f}×")

    material_table = pd.DataFrame(
        {
            "Material": ["Aluminium", "Copper"],
            "Tj at 15 W (°C)": [
                float(al["Junction_Temperature_C"]),
                float(cu["Junction_Temperature_C"]),
            ],
            "Mass (kg)": [
                float(al["Mass_kg"]),
                float(cu["Mass_kg"]),
            ],
            "Raw-material cost (GBP)": [
                float(al["Estimated_Cost"]),
                float(cu["Estimated_Cost"]),
            ],
        }
    )

    st.dataframe(
        material_table.round(
            {
                "Tj at 15 W (°C)": 3,
                "Mass (kg)": 3,
                "Raw-material cost (GBP)": 3,
            }
        ),
        width="stretch",
        hide_index=True,
    )

    st.info(
        "Material screening selects aluminium for the system-level optimisation: "
        "the copper temperature improvement is small relative to its mass and "
        "raw-material-cost penalties."
    )

st.divider()

# ------------------------------------------------------------
# 5. Constrained geometry optimisation
# ------------------------------------------------------------
st.header("5. Constrained Geometry Optimisation")

st.markdown(
    """
**Objective:** minimise heat-sink mass and raw-material use.

**Constraint:** `Tj ≤ 125°C` at `15 W` and `25°C ambient`.

**Candidate set:** three discrete straight-fin aluminium designs.
"""
)

candidate_rows = []

for geometry_key in ["Baseline", "Geometry_1", "Geometry_2"]:
    source = get_geometry_case(
        "Aluminium",
        geometry_key,
        DESIGN_STRESS_W,
    )

    if source is None:
        continue

    info = GEOMETRY_INFO[geometry_key]
    tj = float(source["Junction_Temperature_C"])
    mass = float(source["Mass_kg"])
    cost = float(source["Estimated_Cost"])

    candidate_rows.append(
        {
            "Design": info["display"],
            "Base length (mm)": info["base_length_mm"],
            "Fins": info["fins"],
            "Tj @ 15 W (°C)": tj,
            "Margin to 125°C (°C)": TARGET_TJ - tj,
            "Mass (kg)": mass,
            "Raw-material cost (GBP)": cost,
            "Feasible": tj <= TARGET_TJ,
        }
    )

optimisation = pd.DataFrame(candidate_rows)

if not optimisation.empty:
    original_mass = float(
        optimisation.loc[
            optimisation["Design"] == "Original",
            "Mass (kg)",
        ].iloc[0]
    )

    optimisation["Mass reduction vs Original (%)"] = (
        (original_mass - optimisation["Mass (kg)"])
        / original_mass
        * 100
    )

    optimisation["Feasible?"] = optimisation["Feasible"].map(
        {True: "YES", False: "NO"}
    )

    display_cols = [
        "Design",
        "Base length (mm)",
        "Fins",
        "Tj @ 15 W (°C)",
        "Margin to 125°C (°C)",
        "Mass (kg)",
        "Mass reduction vs Original (%)",
        "Raw-material cost (GBP)",
        "Feasible?",
    ]

    st.dataframe(
        optimisation[display_cols].round(
            {
                "Tj @ 15 W (°C)": 3,
                "Margin to 125°C (°C)": 3,
                "Mass (kg)": 3,
                "Mass reduction vs Original (%)": 1,
                "Raw-material cost (GBP)": 3,
            }
        ),
        width="stretch",
        hide_index=True,
    )

    feasible = optimisation[optimisation["Feasible"]].copy()

    if not feasible.empty:
        recommended = feasible.sort_values("Mass (kg)").iloc[0]

        st.success(
            f'**Optimised tested design: {recommended["Design"]} '
            f'({int(recommended["Base length (mm)"])} mm, '
            f'{int(recommended["Fins"])} fins) in aluminium.** '
            "It is the minimum-mass tested candidate that satisfies the "
            "125°C / 15 W constraint."
        )

        o1, o2, o3, o4 = st.columns(4)
        o1.metric("Recommended mass", f'{recommended["Mass (kg)"]:.3f} kg')
        o2.metric(
            "Mass reduction",
            f'{recommended["Mass reduction vs Original (%)"]:.0f}%',
            delta="vs Original",
        )
        o3.metric(
            "Tj at 15 W",
            f'{recommended["Tj @ 15 W (°C)"]:.2f} °C',
        )
        o4.metric(
            "Thermal margin",
            f'{recommended["Margin to 125°C (°C)"]:.2f} °C',
        )

    st.write("**15 W junction-temperature comparison**")
    st.bar_chart(
        optimisation.set_index("Design")[["Tj @ 15 W (°C)"]]
    )

st.divider()

# ------------------------------------------------------------
# 6. Thermal scalability
# ------------------------------------------------------------
st.header("6. Thermal Scalability")

st.markdown(
    """
An effective thermal resistance is estimated from each aluminium 15 W result:

`Rθ,eff ≈ (Tj - Ta) / P`

The corresponding heat load at which the model reaches the 125°C design target is:

`P125 ≈ (125 - Ta) / Rθ,eff`

These values are **estimated thermal-capacity thresholds**, not experimentally
validated safe operating limits.
"""
)

if not optimisation.empty:
    scalability = optimisation.copy()

    scalability["Effective thermal resistance (°C/W)"] = (
        scalability["Tj @ 15 W (°C)"] - AMBIENT_C
    ) / DESIGN_STRESS_W

    scalability["Estimated heat load at 125°C (W)"] = (
        TARGET_TJ - AMBIENT_C
    ) / scalability["Effective thermal resistance (°C/W)"]

    scalability_display = scalability[
        [
            "Design",
            "Effective thermal resistance (°C/W)",
            "Estimated heat load at 125°C (W)",
        ]
    ].copy()

    st.dataframe(
        scalability_display.round(3),
        width="stretch",
        hide_index=True,
    )

    st.bar_chart(
        scalability.set_index("Design")[
            ["Estimated heat load at 125°C (W)"]
        ]
    )

    st.markdown(
        """
**Interpretation:** the 40 mm design reaches the project temperature constraint
first as heat dissipation increases. The 60 mm design provides an intermediate
lightweight operating range, while the 80 mm design provides the greatest thermal
headroom.

Under the approximately linear steady-state model, higher thermal demand amplifies
the absolute junction-temperature penalty associated with higher thermal resistance.
"""
    )

st.divider()

# ------------------------------------------------------------
# 7. Manufacturability
# ------------------------------------------------------------
st.header("7. Manufacturability and Industrial Use")

st.markdown(
    """
- Aluminium 6061-T6 provides a large mass advantage over copper and is suitable
  for conventional heat-sink manufacture.
- The straight-fin concept is compatible with extrusion.
- The 80 / 60 / 40 mm designs do **not** represent one identical extrusion simply
  cut to different lengths: changing base width and fin count changes the extrusion
  cross-section.
- At higher production volume, dedicated extrusion profiles/dies may be justified.
- For prototype or low-volume production, machining or modifying standard heat-sink
  stock may be more practical.
- Secondary machining may still be required for MOSFET contact, mounting and assembly
  features.

The raw-material cost values are comparative material-content estimates only.
"""
)

st.divider()

# ------------------------------------------------------------
# 8. Validation summary
# ------------------------------------------------------------
st.header("8. Validation Summary")

v1, v2, v3 = st.columns(3)

with v1:
    st.markdown(
        """
**Electrical cross-check**

At the 10 A baseline, waveform-separated LTspice conduction loss is approximately
**0.667 W** versus **0.695 W** analytically (about **4% difference**).

The larger total-loss discrepancy is dominated by the simplified datasheet-based
switching-transition estimate.
"""
    )

with v2:
    st.markdown(
        """
**Mesh independence**

- 5.0 mm: **30.628°C**
- 2.5 mm: **30.631°C**
- 2.0 mm: **30.633°C**

Medium-to-fine change ≈ **0.0065%**, well below the **2%** project criterion.
"""
    )

with v3:
    st.markdown(
        """
**Coupling convergence**

The 20 A aluminium coupled model was started from **25°C, 75°C and 125°C**.

All runs converged to approximately **53.15°C**, with a final spread below **0.02°C**.
"""
    )

st.caption(
    "Detailed derivations, waveform analysis, mesh calculations and convergence "
    "histories remain documented in the repository notebooks."
)

st.divider()

# ------------------------------------------------------------
# 9. Final recommendation
# ------------------------------------------------------------
st.header("9. Final Engineering Recommendation")

st.success(
    """
**Select Geometry 1: 60 mm base length, 6 fins, aluminium 6061-T6, with the
fixed TGP5000 interface.**

It is the **minimum-mass tested design that satisfies the 125°C junction-temperature
target at 15 W** under the baseline natural-convection assumption.
"""
)

st.markdown(
    """
The recommendation is conditional on the defined passive-cooling environment.
The project does not claim that the 60 mm design is universally optimal under all
convection conditions or beyond the validated modelling range.

**Problem:** electro-thermal feedback makes dedicated cooling necessary.  
**Optimisation:** minimise heat-sink mass subject to the 125°C / 15 W constraint.  
**Scalability:** quantify how the three candidate geometries approach the thermal
constraint as heat demand increases.
"""
)

with st.expander("Show master results"):
    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
    )
