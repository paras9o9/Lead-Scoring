# Lead Conversion Scoring Tool

A machine learning-powered web tool that predicts whether a marketing lead is likely to convert or not.  
This project demonstrates the **end-to-end ML pipeline** — from real-world data cleaning and feature engineering, to model training, evaluation, and deployment in a **Streamlit web app**.

---

## Project Overview

Sales and marketing teams often waste time on leads that never convert.  
This tool solves that problem by assigning a **conversion score** to each lead, enabling smarter prioritization and improved sales efficiency.

The model is trained on a real-world lead generation dataset. Users upload a `.csv` file of leads, and the app predicts whether each lead is likely to convert (`Converted = 1`) or not (`Converted = 0`).

---

## Problem Type

- **Type**: Supervised Learning – Binary Classification  
- **Target Variable**: `Converted`  
- **Objective**: Predict the likelihood of conversion for each lead

---

## Key Features

| Feature | Description |
|---------|-------------|
| Data Cleaning | Removed IDs, handled missing values, and cleaned categorical values |
| Model Training | Trained Logistic Regression, Random Forest, and XGBoost classifiers |
| Evaluation | Compared models using Accuracy, Precision, Recall, and F1-score |
| Feature Engineering | Applied One-Hot Encoding and selected the best predictors |
| Model Export | Best model saved using `joblib` with matching feature set |
| Streamlit App | Upload CSV → Run Prediction → View & Download Results |
| Local Deployment | Fully functional offline tool with step-by-step setup guide |

---

## 🏁 Model Performance Summary

| Model               | Accuracy | Precision | Recall | F1-Score |
|--------------------|----------|-----------|--------|----------|
| Logistic Regression | ~87%     | Good      | Good   | Good     |
| Random Forest       | ~90%     | Better    | Better | Better   |
| **XGBoost (Final)** |  Best  | Highest   | High   | High     |

> The final model (XGBoost) was selected for its strong balance of accuracy, generalization, and robustness on unseen data.

---

## How to Run Locally

```bash
# 1️Clone the repository
git clone https://github.com/your-username/lead-scoring-app.git
cd lead-scoring-app

# 2️(Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

# 3️Install required packages
pip install -r requirements.txt

# 4️Launch the Streamlit app
streamlit run app.py
