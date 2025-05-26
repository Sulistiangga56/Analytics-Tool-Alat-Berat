import streamlit as st
import pandas as pd
from db_config import engine
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard Efisiensi Unit")
st.markdown("Perbandingan antara jam kerja dan konsumsi bahan bakar (BBM).")

#LOAD DATA
@st.cache_data
def load_data():
    query = """
    SELECT em.log_date, um.unit_code, um.unit_type, em.hours_operated, em.fuel_used
    FROM equipment_logs em
    JOIN unit_master um ON em.unit_id = um.unit_id
    """
    return pd.read_sql(query, engine)

df = load_data()

#FILTER UNIT
unit_list = df["unit_code"].unique()
selected_units = st.multiselect("Pilih Unit", unit_list, default=unit_list)

filtered_df = df[df["unit_code"].isin(selected_units)]

#HITUNG EFISIENSI JAM KERJA / LITER BBM
filtered_df["efficiency"] = filtered_df["hours_operated"] / filtered_df["fuel_used"]
filtered_df = filtered_df.replace([float("inf"), -float("inf")], pd.NA).dropna()

st.subheader("Distribusi Efisiensi Operasi")

fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=filtered_df, x="unit_code", y="efficiency", ax=ax, palette="Blues")
ax.set_ylabel("Efisiensi (Jam Kerja / Liter BBM)")
ax.set_xlabel("Unit Code")
st.pyplot(fig)

#RATA-RATA EFISIENSI PER UNIT
st.subheader("Rata-rata Efisiensi per Unit")
avg_eff = (filtered_df.groupby("unit_code")["efficiency"].mean().sort_values(ascending=False).reset_index())

st.dataframe(avg_eff.rename(columns={"efficiency": "avg_efficiency (jam/liter)" }), use_container_width=True)