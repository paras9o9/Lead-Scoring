import streamlit as st
import pandas as pd
import joblib

# Load model and features
model = joblib.load("lead_scoring_model.pkl")
model_features = joblib.load("model_features.pkl")

st.title("🎯 Lead Scoring Prediction App")
uploaded_file = st.file_uploader("📤 Upload your leads CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the uploaded file
        data = pd.read_csv(uploaded_file)

        # Show expected vs actual columns
        st.subheader("🧪 Debug: Feature Check")
        st.write("✅ Model expects:", model_features)
        st.write("📤 Your file has:", list(data.columns))

        # Add missing columns as 0s
        for col in model_features:
            if col not in data.columns:
                data[col] = 0

        # Reorder columns to match model
        data_model = data[model_features]

        # Predict
        predictions = model.predict(data_model)
        data["Prediction"] = predictions

        # Display and allow download
        st.success("✅ Predictions complete!")
        st.dataframe(data)

        csv = data.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Predictions", csv, "lead_predictions.csv", "text/csv")

    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")
