import streamlit as st
import pandas as pd
from db_config import engine
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.title("Analisis Breakdown Unit")
st.markdown("Menampilkan jumlah dan distribusi breakdown alat berat.")

#LOAD DATA
@st.cache_data
def load_data():
    query = """
    SELECT em.log_date, um.unit_code, em.breakdown
    FROM equipment_logs em
    JOIN unit_master um ON em.unit_id = um.unit_id
    """
    return pd.read_sql(query, engine)

df = load_data()

#FILTER UNIT
unit_list = df["unit_code"].unique()
selected_units = st.multiselect("Pilih Unit", unit_list, default=unit_list)

filtered_df = df[df["unit_code"].isin(selected_units)]

#BREAKDOWN count per unit
breakddown_counts = (filtered_df.groupby("unit_code")["breakdown"].sum().reset_index())

#VISUALISASI MENGGUNAKAN PLOTLY
st.subheader("Jumlah Breakdown per Unit")

# Bar chart dengan plotly
fig = px.bar(breakddown_counts, 
             x="unit_code", 
             y="breakdown",
             labels={"unit_code": "Unit Code", "breakdown": "Jumlah Breakdown"},
             color="breakdown",
             color_continuous_scale="Reds")
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

#TIMELINE BREAKDOWN DENGAN PLOTLY
st.subheader("Timeline Breakdown Harian")

timeline = filtered_df.groupby(["log_date"])["breakdown"].sum().reset_index()

fig2 = px.line(timeline, 
               x="log_date", 
               y="breakdown",
               markers=True,
               labels={"log_date": "Tanggal", "breakdown": "Total Breakdown"})
fig2.update_layout(height=500)
fig2.update_traces(line_color="red")
st.plotly_chart(fig2, use_container_width=True)