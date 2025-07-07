# Lead Scoring Tool Report

## Objective
Build a machine learning-based lead scoring model that predicts whether a lead will convert (`Converted = 1`) and wrap it into a simple, user-friendly tool. The goal is to support marketing teams in prioritizing high-quality leads.

---

## Approach

1. **Problem Framing**  
   - Binary Classification: Predict whether a lead will convert.
   - Target: `Converted`

2. **Data Preprocessing**
   - Dropped ID columns (`Lead Number`, `Prospect ID`)
   - Imputed missing values using statistical techniques
   - Encoded categorical features using Label and OneHot Encoding
   - Normalized numeric columns for scaling

3. **Model Development**
   - Trained Logistic Regression, Random Forest, and XGBoost
   - Selected **XGBoost** based on highest performance (accuracy, F1)
   - Saved model with `joblib` for deployment

4. **Evaluation**
   - Used Accuracy, Precision, Recall, F1, and Confusion Matrix
   - Handled class imbalance using stratified splitting

---

## Results

| Model             | Accuracy | F1-Score |
|------------------|----------|----------|
| Logistic Regression | ~87%   | ~85%     |
| Random Forest       | ~90%   | ~89%     |
| **XGBoost**         | ~92%   | ~91%     |

---

## Streamlit App

A clean UI allows users to:
- Upload CSV files with leads
- Get predictions (Converted = 1 or 0)
- Download the result CSV with added `Lead Score`

---

## Real-World Value

This tool supports:
- Smarter sales prioritization
- Time-efficient outreach
- Improved conversion strategy

---

## Note on Deployment

Due to environment mismatches, live deployment wasn’t completed. However, the full app runs locally and is deployment-ready with minor tweaks.

