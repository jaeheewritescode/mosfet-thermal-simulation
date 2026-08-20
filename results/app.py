import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="MOSFET Electro-Thermal Dashboard", layout="wide")

st.title("MOSFET Electro-Thermal Simulation Dashboard")
st.write(
    "Interactive summary of the validated electrical, thermal, geometry, mass, "
    "cost and manufacturability results."
)

# Load results
possible_paths = [Path("master_results.csv"), Path("results/master_results.csv")]
results_path = next((p for p in possible_paths if p.exists()), None)

if results_path is None:
    st.error("master_results.csv could not be found.")
    st.stop()

df = pd.read_csv(results_path)
electrical = df[df["Scenario_Type"] == "Electrical"].copy()
geometry_results = df[df["Scenario_Type"] == "Geometry"].copy()

# Geometry + material data
geometry_data = pd.DataFrame({
    "Geometry": ["Original", "Geometry 1", "Geometry 2"],
    "Base length (mm)": [80, 60, 40],
    "Number of fins": [8, 6, 4],
    "Volume (cm³)": [130.0, 97.5, 65.0],
    "Aluminium mass (kg)": [0.3510, 0.26325, 0.1755],
    "Copper mass (kg)": [1.1648, 0.8736, 0.5824],
    "Mass reduction vs Original (%)": [0, 25, 50],
})

AL_PRICE_PER_KG = 3.270
CU_PRICE_PER_KG = 14.912

geometry_data["Aluminium raw material cost (USD)"] = geometry_data["Aluminium mass (kg)"] * AL_PRICE_PER_KG
geometry_data["Copper raw material cost (USD)"] = geometry_data["Copper mass (kg)"] * CU_PRICE_PER_KG

# Sidebar
st.sidebar.header("Operating Point")
current = st.sidebar.selectbox("Load Current", [5.0, 10.0, 20.0])
material = st.sidebar.selectbox("Heat Sink Material", ["Aluminium", "Copper"])
selected_geometry = st.sidebar.selectbox("Heat Sink Geometry", ["Original", "Geometry 1", "Geometry 2"])

# Electrical / thermal result
result = electrical[
    (electrical["Load_Current_A"] == current) &
    (electrical["Material"] == material)
]

st.subheader("Electrical and Thermal Outputs")

if result.empty:
    st.warning("No validated electrical result was found for this configuration.")
else:
    row = result.iloc[0]
    tj = row["Junction_Temperature_C"]
    loss = row["MOSFET_Loss_W"]
    efficiency = row["Efficiency_pct"]
    margin_125 = row["Margin_to_125C_C"]
    margin_175 = row["Margin_to_175C_C"]

    c1, c2, c3 = st.columns(3)
    c1.metric("MOSFET Loss", f"{loss:.3f} W")
    c2.metric("MOSFET-Loss-Based Efficiency", f"{efficiency:.2f}%")
    c3.metric("Junction Temperature", f"{tj:.2f} °C")

    st.subheader("Thermal Safety")
    c4, c5 = st.columns(2)
    c4.metric("Margin to 125°C Target", f"{margin_125:.2f} °C")
    c5.metric("Margin to 175°C Limit", f"{margin_175:.2f} °C")

    if tj < 125:
        st.success("SAFE: Junction temperature is below the 125°C project target.")
    elif tj < 175:
        st.warning("CAUTION: Above the 125°C project target but below the 175°C absolute device limit.")
    else:
        st.error("UNSAFE: Junction temperature exceeds the 175°C device limit.")

st.divider()

# Geometry, mass and cost
st.subheader("Geometry, Mass and Raw-Material Cost")

selected_geo_row = geometry_data[geometry_data["Geometry"] == selected_geometry].iloc[0]

if material == "Aluminium":
    selected_mass = selected_geo_row["Aluminium mass (kg)"]
    selected_cost = selected_geo_row["Aluminium raw material cost (USD)"]
else:
    selected_mass = selected_geo_row["Copper mass (kg)"]
    selected_cost = selected_geo_row["Copper raw material cost (USD)"]

g1, g2, g3, g4 = st.columns(4)
g1.metric("Base Length", f'{selected_geo_row["Base length (mm)"]:.0f} mm')
g2.metric("Number of Fins", f'{selected_geo_row["Number of fins"]:.0f}')
g3.metric("Heat-Sink Mass", f"{selected_mass:.3f} kg")
g4.metric("Estimated Raw-Material Cost", f"${selected_cost:.2f}")

st.caption(
    "Raw-material cost only. This excludes extrusion, machining, surface finishing, "
    "labour, tooling, scrap, transport and supplier margin."
)

st.write("**Mass comparison**")
st.bar_chart(
    geometry_data.set_index("Geometry")[["Aluminium mass (kg)", "Copper mass (kg)"]]
)

st.write("**Raw-material cost comparison**")
st.bar_chart(
    geometry_data.set_index("Geometry")[[
        "Aluminium raw material cost (USD)",
        "Copper raw material cost (USD)"
    ]]
)

st.dataframe(geometry_data.round(3), use_container_width=True, hide_index=True)

st.divider()

# Geometry thermal performance
st.subheader("Geometry Thermal Performance")

if geometry_results.empty:
    st.info("No geometry rows were found in master_results.csv.")
else:
    geometry_display_cols = [
        c for c in [
            "Load_Point",
            "Heat_Load_W",
            "Material",
            "Geometry",
            "Junction_Temperature_C",
            "Margin_to_125C_C",
            "Margin_to_175C_C",
            "Mass_kg",
            "Estimated_Cost",
            "Manufacturability",
            "Status"
        ] if c in geometry_results.columns
    ]
    st.dataframe(
        geometry_results[geometry_display_cols],
        use_container_width=True,
        hide_index=True
    )

    completed_geometry = geometry_results.dropna(subset=["Junction_Temperature_C"]).copy()
    if not completed_geometry.empty:
        completed_geometry["Case"] = (
            completed_geometry["Geometry"].astype(str)
            + " | "
            + completed_geometry["Heat_Load_W"].astype(str)
            + " W"
        )
        st.write("**Validated geometry junction temperatures**")
        st.bar_chart(
            completed_geometry.set_index("Case")[["Junction_Temperature_C"]]
        )

st.divider()

# Manufacturability
st.subheader("Manufacturability and Industrial Use")

m1, m2 = st.columns(2)

with m1:
    st.markdown("""
**Aluminium 6061-T6**
- Low density reduces component and system mass.
- Well suited to heat-sink extrusion and secondary machining.
- Straight-fin geometry is compatible with scalable profile-based manufacture.
- Lower mass improves handling, mounting, transport and converter integration.
""")

with m2:
    st.markdown("""
**Copper C11000**
- Higher thermal conductivity can reduce junction temperature.
- Approximately 3.32× denser than aluminium for the same geometry.
- Significantly higher raw-material cost in this comparison.
- Higher mass increases mounting and integration demands.
- Most attractive where thermal constraints justify the penalty.
""")

st.write(
    "**Likely industrial route for the recommended aluminium design:** "
    "aluminium extrusion → cut to required length → secondary machining of "
    "mounting/contact features → optional surface finishing → TIM and MOSFET assembly."
)

st.divider()

# Recommendation
st.subheader("Engineering Recommendation")

st.success(
    "**Recommended overall design: Geometry 1 (60 mm, 6 fins) in aluminium "
    "with TGP5000 TIM.**"
)

r1, r2, r3 = st.columns(3)
r1.metric("Geometry 1 Aluminium Mass", "0.263 kg", delta="-25% vs Original")
r2.metric("Geometry 1 Material Volume", "97.5 cm³", delta="-25% vs Original")

geometry_1_stress = pd.DataFrame()
if not geometry_results.empty:
    geometry_1_stress = geometry_results[
        geometry_results["Geometry"].astype(str).str.contains("Geometry_1|Geometry 1", regex=True) &
        (geometry_results["Heat_Load_W"] == 15.0)
    ]

if not geometry_1_stress.empty and pd.notna(geometry_1_stress.iloc[0]["Junction_Temperature_C"]):
    g1_stress_tj = float(geometry_1_stress.iloc[0]["Junction_Temperature_C"])
else:
    g1_stress_tj = 111.831

r3.metric(
    "Geometry 1 at 15 W",
    f"{g1_stress_tj:.2f} °C",
    delta=f"{125 - g1_stress_tj:.2f} °C margin to 125°C"
)

st.markdown("""
The final recommendation is based on a **multi-objective engineering trade-off**
rather than the lowest temperature alone:

- **Thermal performance:** Geometry 1 retains useful margin to the 125°C project target at the 15 W stress case.
- **Mass:** moving from the 80 mm Original geometry to the 60 mm Geometry 1 reduces heat-sink mass by **25%**.
- **Material:** aluminium is approximately **3.32× lighter than copper** for the same geometry.
- **Cost:** aluminium has a substantially lower raw-material-content cost than copper.
- **Manufacturability:** the straight-fin aluminium design is suitable for extrusion, cut-to-length production and secondary machining.
- **Industrial integration:** lower mass and a shorter heat sink reduce packaging, mounting and handling demands.

**Geometry 2 (40 mm, 4 fins)** achieves the greatest mass reduction at **50% below
the Original design**, but its 15 W thermal result exceeds the 125°C project target.
It is therefore better suited to lower thermal-demand applications.

**Copper** remains a useful alternative where maximum heat spreading or tight
thermal constraints justify its higher mass and cost.
""")

st.divider()

# Validated electrical results
st.subheader("Validated Electrical Results")

display_columns = [
    c for c in [
        "Load_Current_A",
        "Material",
        "Junction_Temperature_C",
        "MOSFET_Loss_W",
        "Efficiency_pct",
        "Margin_to_125C_C",
        "Margin_to_175C_C",
        "Mass_kg",
        "Estimated_Cost",
        "Manufacturability"
    ] if c in electrical.columns
]

st.dataframe(
    electrical[display_columns],
    use_container_width=True,
    hide_index=True
)
