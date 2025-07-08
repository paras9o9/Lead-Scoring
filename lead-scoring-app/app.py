# import streamlit as st
# import pandas as pd
# import joblib

# # Load model and expected features
# model = joblib.load("lead-scoring-app/lead_scoring_model.pkl")
# model_features = joblib.load("lead-scoring-app/model_features.pkl")

# st.title("🎯 Lead Scoring Prediction App")
# uploaded_file = st.file_uploader("📤 Upload your leads CSV", type=["csv"])

# if uploaded_file is not None:
#     try:
#         # Load CSV
#         data = pd.read_csv(uploaded_file)

#         # 🧩 Step 1: Add missing columns with 0
#         for col in model_features:
#             if col not in data.columns:
#                 data[col] = 0

#         # 🧼 Step 2: Remove extra columns not in model
#         data = data[model_features]

#         # 🧮 Step 3: Ensure correct order and type
#         data = data[model_features]
#         data = data.astype(float)

#         # 🎯 Step 4: Predict
#         predictions = model.predict(data)
#         data["Prediction"] = predictions

#         # ✅ Step 5: Show + Download
#         st.success("✅ Predictions complete!")
#         st.dataframe(data)

#         csv = data.to_csv(index=False).encode("utf-8")
#         st.download_button("📥 Download Predictions", csv, "lead_predictions.csv", "text/csv")

#     except Exception as e:
#         st.error(f"⚠️ Something went wrong: {e}")

import streamlit as st
import pandas as pd
import joblib
import os

# Load model and features
MODEL_PATH = os.path.join(os.path.dirname(__file__), "lead_scoring_model.pkl")
FEATURES_PATH = os.path.join(os.path.dirname(__file__), "model_features.pkl")

model = joblib.load(MODEL_PATH)
model_features = joblib.load(FEATURES_PATH)

# Binary columns expected as 'Yes'/'No'
BINARY_COLS = [
    'Do Not Email', 'Do Not Call', 'Search', 'Magazine', 'Newspaper Article',
    'X Education Forums', 'Newspaper', 'Digital Advertisement',
    'Through Recommendations', 'Receive More Updates About Our Courses',
    'Update me on Supply Chain Content', 'Get updates on DM Content',
    'I agree to pay the amount through cheque',
    'A free copy of Mastering The Interview'
]

st.title("🎯 Lead Scoring Prediction App")
uploaded_file = st.file_uploader("📤 Upload your leads CSV", type=["csv"])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)

        # 🔄 Step 1: Convert 'Yes'/'No' to 1/0
        for col in BINARY_COLS:
            if col in data.columns:
                data[col] = data[col].map({'Yes': 1, 'No': 0})

        # 🧩 Step 2: Add missing model columns with 0
        for col in model_features:
            if col not in data.columns:
                data[col] = 0

        # 🧼 Step 3: Remove extra columns + reorder
        data = data[model_features]

        # 🧮 Step 4: Ensure numeric type
        data = data.apply(pd.to_numeric, errors='coerce').fillna(0)

        # 🎯 Step 5: Predict
        data["Prediction"] = model.predict(data)

        # ✅ Step 6: Show + Download
        st.success("✅ Predictions complete!")
        st.dataframe(data)

        csv = data.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Predictions", csv, "lead_predictions.csv", "text/csv")

    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")
