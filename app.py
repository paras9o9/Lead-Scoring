import streamlit as st
import pandas as pd
import joblib

model = joblib.load("lead_scoring_model.pkl")
model_features = joblib.load("model_features.pkl")

st.title("🎯 Lead Scoring Prediction Tool")
st.markdown("Upload your leads data (CSV) to get conversion predictions.")

uploaded_file = st.file_uploader("📁 Upload CSV File", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    if not set(model_features).issubset(set(data.columns)):
        st.error("❌ Uploaded file is missing required columns.")
    else:
        data_model = data[model_features]
        predictions = model.predict(data_model)
        data['Prediction'] = predictions
        
        st.success("✅ Predictions complete!")
        st.dataframe(data)

        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Predictions", csv, "lead_predictions.csv", "text/csv")

with open("sample_leads.csv", "rb") as file:
    st.download_button(
        label="📥 Download Sample Leads CSV",
        data=file,
        file_name="sample_leads.csv",
        mime="text/csv"
    )

data_model = data[model_features]
data_model = data_model[model_features]

try:
    data_model = data[model_features]
    data_model = data_model[model_features]  # Ensure column order
    predictions = model.predict(data_model)
    data['Prediction'] = predictions

    st.success("✅ Predictions complete!")
    st.dataframe(data)

    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Predictions", csv, "lead_predictions.csv", "text/csv")

except KeyError as e:
    st.error("❌ Uploaded file is missing required columns. Please use the sample file.")
    st.stop()

st.write("Model expects:", model_features)
st.write("Uploaded file has:", list(data.columns))


