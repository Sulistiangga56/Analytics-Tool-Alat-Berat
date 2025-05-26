import streamlit as st
import pandas as pd
from db_config import engine
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Prediksi Efisiensi BBM (Fuel Efficiency)")
st.markdown("Model regresi untuk memprediksi efisiensi konsumsi BBM per jam kerja.")

@st.cache_data
def load_data():
    query = """
    SELECT unit_id, hours_operated, fuel_used
    FROM equipment_logs
    WHERE hours_operated > 0 AND fuel_used > 0
    """
    df = pd.read_sql(query, engine)
    df["fuel_efficiency"] = df["fuel_used"] / df["hours_operated"]
    return df

df = load_data()

X = df[["hours_operated", "fuel_used"]]
y = df["fuel_efficiency"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

st.subheader("Evaluasi Model")
st.markdown(f"**MSE:** {mse:.2f}")
st.markdown(f"**R² Score:** {r2:.2f}")

# Visualisasi hasil prediksi vs aktual
st.subheader("Visualisasi Prediksi vs Aktual")
fig, ax = plt.subplots()
sns.scatterplot(x=y_test, y=y_pred, ax=ax)
ax.set_xlabel("Efisiensi Aktual")
ax.set_ylabel("Efisiensi Prediksi")
ax.set_title("Prediksi vs Aktual Efisiensi BBM")
st.pyplot(fig)

# Prediksi Interaktif
st.subheader("Prediksi Interaktif")
op_hour = st.number_input("Jam Kerja", min_value=1.0)
fuel_used = st.number_input("Total BBM yang Digunakan (liter)", min_value=1.0)

if st.button("Prediksi Efisiensi"):
    input_data = pd.DataFrame([[op_hour, fuel_used]], columns=["hours_operated", "fuel_used"])
    efficiency = model.predict(input_data)[0]
    st.success(f"Efisiensi Perkiraan: {efficiency:.2f} liter/jam")