import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db_config import engine

st.title("Exploratory Data Analysis")
st.markdown("Halaman interaktif untuk eksplorasi data operasional alat berat.")

@st.cache_data
def load_data():
    query = """
    SELECT em.log_date, um.unit_code, um.unit_type, em.hours_operated, em.fuel_used, em.breakdown
    FROM equipment_logs em
    JOIN unit_master um ON em.unit_id = um.unit_id
    """
    return pd.read_sql(query, engine)

# Load
df = load_data()

# Sidebar Controls
st.sidebar.header("Filter Data")
units = df["unit_code"].unique()
selected_units = st.sidebar.multiselect("Pilih Unit", units, default=list(units))
df_filtered = df[df["unit_code"].isin(selected_units)]

# Date Range
if not df_filtered.empty:
    min_date = pd.to_datetime(df_filtered["log_date"]).min().date()
    max_date = pd.to_datetime(df_filtered["log_date"]).max().date()
    start_date, end_date = st.sidebar.date_input("Rentang Tanggal", [min_date, max_date])
    df_filtered = df_filtered[(pd.to_datetime(df_filtered["log_date"]).dt.date >= start_date) & (pd.to_datetime(df_filtered["log_date"]).dt.date <= end_date)]
else:
    st.warning("No data available for the selected filters")

# Main EDA Sections
st.subheader("Preview Data")
st.dataframe(df_filtered, use_container_width=True)

# Distribution Plots
st.subheader("Distribusi Jam Operasi dan Konsumsi BBM")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Jam Operasi**")
    fig1, ax1 = plt.subplots()
    sns.histplot(df_filtered["hours_operated"], kde=True, ax=ax1)
    ax1.set_xlabel("Jam Operasi")
    st.pyplot(fig1)
with col2:
    st.markdown("**Konsumsi BBM**")
    fig2, ax2 = plt.subplots()
    sns.histplot(df_filtered["fuel_used"], kde=True, ax=ax2)
    ax2.set_xlabel("BBM (liter)")
    st.pyplot(fig2)

# Correlation Heatmap
st.subheader("Heatmap Korelasi")
fig3, ax3 = plt.subplots(figsize=(6, 4))
corr = df_filtered[["hours_operated", "fuel_used", "breakdown"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax3)
st.pyplot(fig3)

# Scatter Plot
st.subheader("Scatter Plot: Jam Operasi vs BBM")
fig4, ax4 = plt.subplots()
sns.scatterplot(data=df_filtered, x="hours_operated", y="fuel_used", hue="unit_code", ax=ax4)
ax4.set_xlabel("Jam Operasi")
ax4.set_ylabel("BBM (liter)")
st.pyplot(fig4)

# Breakdown over time
st.subheader("Breakdown Over Time")
fig5, ax5 = plt.subplots()
time_series = df_filtered.groupby("log_date")["breakdown"].sum().reset_index()
sns.lineplot(data=time_series, x="log_date", y="breakdown", ax=ax5)
ax5.set_xlabel("Tanggal")
ax5.set_ylabel("Jumlah Breakdown")
st.pyplot(fig5)