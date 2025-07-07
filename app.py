import streamlit as st
import pandas as pd
import joblib

# Load the model and features
model = joblib.load("lead_scoring_model.pkl")
model_features = joblib.load("model_features.pkl")

st.title("🎯 Lead Scoring Prediction App")

uploaded_file = st.file_uploader("📤 Upload your leads CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Step 1: Read the uploaded CSV
        data = pd.read_csv(uploaded_file)

        # Step 2: Match model input features
        data_model = data[model_features]
        data_model = data_model[model_features]  # Ensures correct order

        # Step 3: Predict
        predictions = model.predict(data_model)

        # Step 4: Add results to the original data
        data["Prediction"] = predictions

        # Step 5: Show and download
        st.success("✅ Predictions complete!")
        st.dataframe(data)

        csv = data.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Predictions", csv, "lead_predictions.csv", "text/csv")

    except KeyError:
        st.error("❌ Uploaded file is missing required columns. Please use the sample file.")
