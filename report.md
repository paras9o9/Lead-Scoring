# Lead Scoring Tool — Project Report

## Objective

Develop a machine learning–based lead scoring model to predict whether a marketing lead will convert (`Converted = 1`).  
Wrap the model in a user-friendly web app to help marketing teams **prioritize high-quality leads** and improve sales efficiency.

---

## Approach

### 1. Problem Framing
- **Type**: Binary Classification
- **Target Variable**: `Converted`
- **Goal**: Predict lead conversion likelihood using behavioral and profile data

---

### 2. Data Preprocessing
- Dropped identifier columns: `Prospect ID`, `Lead Number`
- Handled missing values using median/mode imputation and category placeholders
- Transformed binary columns (`Yes`/`No`) into numeric (`1`/`0`)
- Applied **One-Hot Encoding** for categorical features like `City`, `Lead Source`, `Country`
- Normalized continuous features (e.g., `TotalVisits`, `Page Views Per Visit`)

---

### 3. Model Development
- Trained and evaluated:
  - Logistic Regression
  - Random Forest
  - **XGBoost**
- XGBoost selected for its superior performance and ability to handle mixed feature types
- Model saved using `joblib` for portability and integration into the app

---

### 4. Evaluation Metrics
- Used: **Accuracy**, **Precision**, **Recall**, **F1-Score**, and **Confusion Matrix**
- Stratified data splitting to handle slight class imbalance

---

## Results

| Model               | Accuracy | F1-Score |
|--------------------|----------|----------|
| Logistic Regression | ~87%  | ~85%  |
| Random Forest       | ~90%  | ~89%  |
| **XGBoost (Final)** | ~92%  | ~91%  |

> The XGBoost model demonstrated the best overall performance with a strong balance of accuracy and generalization.

---

## Streamlit App Interface

The final app allows users to:
- Upload new lead data as CSV
- Predict conversion likelihood
- Download the results with a `Prediction` column appended

The model automatically processes the input, applies necessary encoding, and returns predictions in real time.

---

## Real-World Value

This tool directly supports:
- **Targeted sales outreach** (focus on high-probability leads)
- **Time efficiency** (reduce low-quality lead handling)
- **Improved conversion rates** via data-driven decision-making

It’s especially valuable in B2C and ed-tech-style businesses with high lead inflow.

---

## Deployment Note

The app was **successfully deployed locally** and is fully functional.

It allows users to:
- Upload a leads CSV
- Automatically preprocess the data
- Generate predictions on conversion likelihood
- Download the output — all from a browser-based UI

> The tool is also ready for cloud deployment via:
> - Streamlit Sharing
> - Hugging Face Spaces
> - Docker-based cloud platforms

With minimal configuration, it can be publicly hosted and shared.

---

## Author

**Paras Sharma**  
This project was developed as part of the **Caprae Capital AI Readiness Pre-Screening Challenge**.  
🔗 [LinkedIn Profile]([https://linkedin.com/in/your-link](https://www.linkedin.com/in/paras-sharma-938b701a2/)) *(Add your link here)*

---
