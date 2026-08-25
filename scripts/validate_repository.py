from pathlib import Path
import math
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "results" / "master_results.csv"
CASE_MATRIX = ROOT / "data" / "simulation_case_matrix.csv"
MATERIALS = ROOT / "data" / "material-properties.csv"
MASS = ROOT / "data" / "heatsink_mass_comparison.csv"


def close(a, b, tol=1e-6):
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=tol)


def require(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


master = pd.read_csv(MASTER)
cases = pd.read_csv(CASE_MATRIX)
materials = pd.read_csv(MATERIALS)
mass = pd.read_csv(MASS)

require(master["Case_ID"].is_unique, "master_results Case_ID values are unique")
require(cases["Case_ID"].is_unique, "simulation_case_matrix Case_ID values are unique")
require(set(master["Case_ID"]) == set(cases["Case_ID"]), "master results and case matrix contain the same case IDs")
require(len(master) == 21, "final master result contains the expected 21 cases")

# Shared case-definition fields should agree exactly (NaNs treated as blank).
shared = [
    "Scenario_Type", "Load_Point", "Load_Current_A", "Heat_Load_W",
    "Material", "TIM_Config", "Geometry", "Ambient_Temperature_C",
]
a = master.set_index("Case_ID")[shared].fillna("").astype(str).sort_index()
b = cases.set_index("Case_ID")[shared].fillna("").astype(str).sort_index()
require(a.equals(b), "shared case-definition fields match between master results and case matrix")

# Temperature margins.
for _, row in master.dropna(subset=["Junction_Temperature_C"]).iterrows():
    tj = row["Junction_Temperature_C"]
    require(close(row["Margin_to_125C_C"], 125.0 - tj), f"{row['Case_ID']} margin to 125°C is correct")
    require(close(row["Margin_to_175C_C"], 175.0 - tj), f"{row['Case_ID']} margin to 175°C is correct")

# Geometry-only fixed-load rows must not masquerade as current cases.
geom = master[master["Scenario_Type"] == "Geometry"]
require(geom["Load_Current_A"].isna().all(), "geometry-only rows have blank Load_Current_A")
require(set(geom["TIM_Config"].dropna()) == {"TGP5000"}, "geometry rows use one consistent TGP5000 category")

# Material density / mass / cost traceability.
al_density = float(materials.loc[materials["Material"] == "Aluminium 6061-T6", "Density_g_cm3"].iloc[0])
cu_density = float(materials.loc[materials["Material"] == "Copper C11000", "Density_g_cm3"].iloc[0])
al_price = float(materials.loc[materials["Material"] == "Aluminium 6061-T6", "Benchmark_Raw_Metal_Price_GBP_per_kg"].iloc[0])
cu_price = float(materials.loc[materials["Material"] == "Copper C11000", "Benchmark_Raw_Metal_Price_GBP_per_kg"].iloc[0])
require(close(al_density, 2.70), "aluminium density is frozen at 2.70 g/cm³")
require(close(cu_density, 8.91), "C11000 density is frozen at 8.91 g/cm³")

for _, row in mass.iterrows():
    volume = float(row["Total_Volume_cm3"])
    exp_al_mass = volume * al_density / 1000.0
    exp_cu_mass = volume * cu_density / 1000.0
    require(close(row["Aluminium_Mass_kg"], exp_al_mass), f"{row['Geometry']} aluminium mass reproduces from volume and density")
    require(close(row["Copper_Mass_kg"], exp_cu_mass), f"{row['Geometry']} copper mass reproduces from volume and density")
    require(close(row["Aluminium_Raw_Material_Cost_GBP"], exp_al_mass * al_price, 2e-6), f"{row['Geometry']} aluminium raw-material cost reproduces")
    require(close(row["Copper_Raw_Material_Cost_GBP"], exp_cu_mass * cu_price, 2e-6), f"{row['Geometry']} copper raw-material cost reproduces")

# Final discrete optimisation decision.
def get_tj(case_id):
    return float(master.loc[master["Case_ID"] == case_id, "Junction_Temperature_C"].iloc[0])

candidates = pd.DataFrame([
    {"Design":"Original", "Tj":get_tj("C09"), "Mass":float(mass.loc[mass["Geometry"]=="Original","Aluminium_Mass_kg"].iloc[0])},
    {"Design":"Geometry 1", "Tj":get_tj("C18"), "Mass":float(mass.loc[mass["Geometry"]=="Geometry 1","Aluminium_Mass_kg"].iloc[0])},
    {"Design":"Geometry 2", "Tj":get_tj("C16"), "Mass":float(mass.loc[mass["Geometry"]=="Geometry 2","Aluminium_Mass_kg"].iloc[0])},
])
candidates["Feasible"] = candidates["Tj"] <= 125.0
winner = candidates[candidates["Feasible"]].sort_values("Mass").iloc[0]
require(winner["Design"] == "Geometry 1", "Geometry 1 is the minimum-mass tested feasible aluminium design at 15 W")
require(not bool(candidates.loc[candidates["Design"]=="Geometry 2","Feasible"].iloc[0]), "Geometry 2 correctly fails the 125°C / 15 W constraint")

# Core repository artifacts.
for rel in [
    "electrical-model/BUCK_converter.asc",
    "electrical-model/LTspice_run_notes.md",
    "thermal-model/mesh_independence.ipynb",
    "thermal-model/ansys/reconstruction_specification.md",
    "results/engineering_assessment.ipynb",
    "results/app.py",
    "docs/engineering-evidence-matrix.md",
]:
    require((ROOT / rel).exists(), f"required artifact exists: {rel}")

print("\nALL REPOSITORY CHECKS PASSED")
