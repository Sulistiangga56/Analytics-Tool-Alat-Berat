import streamlit as st
import pandas as pd
from db_config import engine
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Ringkasan Kinerja Unit")
st.markdown("Menampilkan ringkasa metrik utama: jam kerja, konsumsi bahan bakar, dan jumlah breakdown.")

#LOAD DATA
@st.cache_data
def load_data():
    query = """
    SELECT
        um.unit_code,
        um.unit_type,
        SUM(el.hours_operated) AS total_hours_operated, 
        SUM(el.fuel_used) AS total_fuel, 
        COUNT(*) FILTER (WHERE el.breakdown = TRUE) AS total_breakdown
    FROM unit_master um
    LEFT JOIN equipment_logs el ON el.unit_id = um.unit_id
    GROUP BY um.unit_code, um.unit_type
    """

    df = pd.read_sql(query, engine)
    df["efficiency"] = df["total_hours_operated"] / df["total_fuel"]
    df = df.replace([float("inf"), -float("inf")], pd.NA).dropna()
    return df

df = load_data()

#Tabel Ringkasan
st.subheader("Tabel Ringkasan")
st.dataframe(df.rename(columns={
    "unit_code": "Kode Unit",
    "total_hours_operated": "Total Jam Operasi",
    "total_fuel": "Total Konsumsi BBM",
    "efficiency": "Efisiensi (Jam/Liter)",
    "total_breakdown": "Total Breakdown"
}), use_container_width=True)

#Visualisasi
st.subheader("Visualisasi Ringkasan per Unit")

fig, axs = plt.subplots(1, 3, figsize=(18, 5))

sns.barplot(data=df, x="unit_code", y="total_hours_operated", ax=axs[0], palette="Greens")
axs[0].set_title("Jam Kerja")
axs[0].set_ylabel("Jam")

sns.barplot(data=df, x="unit_code", y="total_fuel", ax=axs[1], palette="Oranges")
axs[1].set_title("Konsumsi Bahan Bakar")
axs[1].set_ylabel("Liter")

sns.barplot(data=df, x="unit_code", y="total_breakdown", ax=axs[2], palette="Reds")
axs[2].set_title("Breakdown")
axs[2].set_ylabel("Jumlah")

for ax in axs:
    ax.set_xlabel("Unit")

st.pyplot(fig)