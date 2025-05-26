import streamlit as st
import pandas as pd
from db_config import engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Prediksi Breakdown Unit")
st.markdown("Model Machine Learning untuk memprediksi apakah unit akan mengalami breakdown.")

@st.cache_data
def load_and_prepare_data():
    query = """
    SELECT el.unit_id, el.hours_operated, el.fuel_used, COUNT(br.breakdown_id) AS breakdowns
    FROM equipment_logs el
    LEFT JOIN breakdown br ON el.unit_id = br.unit_id
    GROUP BY el.unit_id, el.hours_operated, el.fuel_used
    """
    df = pd.read_sql(query, engine)
    df["is_breakdown"] = df["breakdowns"].apply(lambda x: 1 if x > 0 else 0)
    return df

df = load_and_prepare_data()

# Split data
X = df[["hours_operated", "fuel_used"]]
y = df["is_breakdown"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
preds = model.predict(X_test)

# Evaluation
st.subheader("Evaluasi Model")
st.text(classification_report(y_test, preds))

cm = confusion_matrix(y_test, preds)
fig, ax = plt.subplots()
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["No Breakdown", "Breakdown"], yticklabels=["No Breakdown", "Breakdown"])
ax.set_xlabel("Prediksi")
ax.set_ylabel("Aktual")
st.pyplot(fig)

# Predict secara interaktif
st.subheader("Prediksi Interaktif")
op_hour = st.number_input("Masukkan jam kerja", min_value=0.0)
fuel_used = st.number_input("Masukkan konsumsi BBM (liter)", min_value=0.0)

if st.button("Prediksi"):
    pred_input = pd.DataFrame([[op_hour, fuel_used]], columns=["hours_operated", "fuel_used"])
    result = model.predict(pred_input)[0]
    if result == 1:
        st.error("Unit berisiko mengalami breakdown.")
    else:
        st.success("Unit cenderung tidak mengalami breakdown.")