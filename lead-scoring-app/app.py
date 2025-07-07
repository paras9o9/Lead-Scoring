import streamlit as st
import pandas as pd
import joblib

# Load model and expected features
model = joblib.load("lead-scoring-app/lead_scoring_model.pkl")
model_features = joblib.load("model_features.pkl")

st.title("🎯 Lead Scoring Prediction App")
uploaded_file = st.file_uploader("📤 Upload your leads CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Load CSV
        data = pd.read_csv(uploaded_file)

        # 🧩 Step 1: Add missing columns with 0
        for col in model_features:
            if col not in data.columns:
                data[col] = 0

        # 🧼 Step 2: Remove extra columns not in model
        data = data[model_features]

        # 🧮 Step 3: Ensure correct order and type
        data = data[model_features]
        data = data.astype(float)

        # 🎯 Step 4: Predict
        predictions = model.predict(data)
        data["Prediction"] = predictions

        # ✅ Step 5: Show + Download
        st.success("✅ Predictions complete!")
        st.dataframe(data)

        csv = data.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Predictions", csv, "lead_predictions.csv", "text/csv")

    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")
