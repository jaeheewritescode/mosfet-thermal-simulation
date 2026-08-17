import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="MOSFET Electro-Thermal Dashboard",
    layout="wide"
)

st.title("MOSFET Electro-Thermal Simulation Dashboard")
st.write(
    "Final electrical and thermal outputs generated from the validated "
    "master_results.csv dataset."
)

# Load validated project results
df = pd.read_csv("master_results.csv")

# Use only electrically derived operating points
electrical = df[df["Scenario_Type"] == "Electrical"].copy()

st.sidebar.header("Operating Point")

current = st.sidebar.selectbox(
    "Load Current",
    [5.0, 10.0, 20.0]
)

material = st.sidebar.selectbox(
    "Heat Sink Material",
    ["Aluminium", "Copper"]
)

# Select matching validated case
result = electrical[
    (electrical["Load_Current_A"] == current) &
    (electrical["Material"] == material)
]

if result.empty:
    st.error("No validated result found for this configuration.")

else:
    row = result.iloc[0]

    tj = row["Junction_Temperature_C"]
    loss = row["MOSFET_Loss_W"]
    efficiency = row["Efficiency_pct"]
    margin_125 = row["Margin_to_125C_C"]
    margin_175 = row["Margin_to_175C_C"]

    st.subheader("Electrical and Thermal Outputs")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "MOSFET Loss",
        f"{loss:.3f} W"
    )

    col2.metric(
        "MOSFET-Loss-Based Efficiency",
        f"{efficiency:.2f}%"
    )

    col3.metric(
        "Junction Temperature",
        f"{tj:.2f} °C"
    )

    st.subheader("Thermal Safety")

    col4, col5 = st.columns(2)

    col4.metric(
        "Margin to 125°C Target",
        f"{margin_125:.2f} °C"
    )

    col5.metric(
        "Margin to 175°C Limit",
        f"{margin_175:.2f} °C"
    )

    if tj < 125:
        st.success(
            "SAFE: Junction temperature is below the 125°C project target."
        )
    elif tj < 175:
        st.warning(
            "CAUTION: Above the 125°C project target but below the "
            "175°C absolute device limit."
        )
    else:
        st.error(
            "UNSAFE: Junction temperature exceeds the 175°C device limit."
        )

st.divider()

st.subheader("Cooling Design Recommendation")

st.write(
    "**Recommended design strategy: Aluminium heat sink with geometry "
    "optimisation and TGP5000 TIM.**"
)

st.write(
    "Copper provides slightly lower junction temperatures, but the improvement "
    "is small compared with the effect of heat-sink geometry. Aluminium is "
    "therefore preferred as the baseline material, with geometry optimisation "
    "prioritised when additional thermal performance is required."
)

st.divider()

st.subheader("Validated Electrical Results")

display_columns = [
    "Load_Current_A",
    "Material",
    "Junction_Temperature_C",
    "MOSFET_Loss_W",
    "Efficiency_pct",
    "Margin_to_125C_C",
    "Margin_to_175C_C"
]

st.dataframe(
    electrical[display_columns],
    use_container_width=True,
    hide_index=True
)