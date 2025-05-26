import streamlit as st
import pandas as pd
from db_config import engine

st.set_page_config(page_title="Analytics Dashboard", page_icon=":bar_chart:", layout="wide")

st.title("Unit Performance Dashboard")
st.markdown("Analisis data operasional alat berat.")

#Load data dari database
@st.cache_data
def load_data():
    query = """
    SELECT em.log_date, um.unit_code, um.unit_type, em.hours_operated, em.fuel_used, em.breakdown
    FROM equipment_logs em
    JOIN unit_master um ON em.unit_id = um.unit_id
    """
    return pd.read_sql(query, engine)

df = load_data()

#FILTER
unit_options = df['unit_code'].unique()
selected_units = st.multiselect("Pilih Unit", unit_options, default=unit_options)

filtered_df = df[df['unit_code'].isin(selected_units)]

#METRICS
col1, col2, col3 = st.columns(3)
col1.metric("Total Jam Operasi", f"{filtered_df['hours_operated'].sum():,.2f} jam")
col2.metric("Total Konsumsi Digunakan", f"{filtered_df['fuel_used'].sum():,.2f} liter")
col3.metric("Total Breakdown", f"{filtered_df['breakdown'].sum()} kali")

#CHARTS
st.subheader("Grafik Operasional Harian")

import matplotlib.pyplot as plt

daily_summary = filtered_df.groupby('log_date').agg({'hours_operated': 'sum', 'fuel_used': 'sum'}).reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(daily_summary['log_date'], daily_summary['hours_operated'], label='Jam Operasi', marker='o')
ax.plot(daily_summary['log_date'], daily_summary['fuel_used'], label='Konsumsi Bahan Bakar', marker='o')

# Improve date formatting
plt.xticks(rotation=45)
ax.grid(True, linestyle='--', alpha=0.7)

# Format axes
ax.set_xlabel('Tanggal', fontsize=10)
ax.set_ylabel('Total Harian', fontsize=10)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Adjust layout to prevent label cutoff
plt.tight_layout()

st.pyplot(fig)