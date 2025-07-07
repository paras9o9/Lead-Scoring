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
           # Load uploaded CSV
           data = pd.read_csv(uploaded_file)

          # Ensure all model features are present
          for col in model_features:
              if col not in data.columns:
                  data[col] = 0

          # Drop any extra columns not used in training
          data = data[model_features]

          # Reorder to match model
          data = data[model_features]

          # Optional: ensure numeric dtype
          data = data.astype(float)

          # Predict
          predictions = model.predict(data)
          data["Prediction"] = predictions

          # Show results
          st.success("✅ Predictions complete!")
          st.dataframe(data)

          # Download button
          csv = data.to_csv(index=False).encode("utf-8")
          st.download_button("📥 Download Predictions", csv, "lead_predictions.csv", "text/csv")

       except Exception as e:
           st.error(f"⚠️ Something went wrong: {e}")

