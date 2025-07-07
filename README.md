# Lead Conversion Scoring Tool

A machine learning-powered web tool to predict whether a marketing lead is likely to convert or not. This project demonstrates the end-to-end process of solving a real-world business problem — from data cleaning to model deployment.

---

## Project Overview

Sales and marketing teams often spend resources on leads that never convert. This tool solves that problem by assigning a **conversion score** to each lead using machine learning — helping prioritize follow-ups and optimize outreach.

The model was trained on real-world lead data and wrapped in an easy-to-use **Streamlit web app**. Users can upload a CSV of new leads, and the tool will return predictions on whether each lead is likely to convert (`Converted = 1`) or not (`Converted = 0`).

---

## Problem Type

- **Task**: Binary Classification  
- **Target Variable**: `Converted`  
- **Goal**: Predict if a lead will convert (1) or not (0)

---

## Features

| Feature | Description |
|---------|-------------|
| 📊 Data Cleaning | Removed IDs, handled missing values, and encoded categorical features |
| ⚙️ Model Training | Trained Logistic Regression, Random Forest, and XGBoost models |
| 📈 Evaluation | Compared models using Accuracy, Precision, Recall, F1-Score |
| 🧪 Feature Selection | Applied techniques to reduce noise and improve generalization |
| 🧠 Model Export | Saved best model using `joblib` |
| 💻 Streamlit App | Simple UI for CSV upload → Prediction → CSV download |
| 📎 Deployment-Ready | Designed for local or cloud deployment (minor packaging step pending) |

---

## Model Performance

| Model             | Accuracy | Precision | Recall | F1-Score |
|------------------|----------|-----------|--------|----------|
| Logistic Regression | ~87%   |   Good    |  Good  |  Good    |
| Random Forest       | ~90%   |  Better   | Better | Better   |
| XGBoost (Final)     | Best |  Highest  | High   | High     |

The final model was selected for its balance of **accuracy**, **interpretability**, and **scalability**.
