# FinTech AI Model Risk Governance Framework

An open-source Python toolkit for AI model risk governance in financial services.

Built against a real fraud detection model trained on the Kaggle ULB Credit Card Fraud dataset.

## Modules

| # | Module | Status |
|---|--------|--------|
| 1 | Model Card Generator | ✅ Complete |
| 2 | SHAP Explainability Report | 🔧 In Progress |
| 3 | Bias & Fairness Audit | ⏳ Planned |
| 4 | Data Drift Monitor | ⏳ Planned |
| 5 | EU AI Act Risk Classifier | ⏳ Planned |

## Dataset

This project uses the [Kaggle ULB Credit Card Fraud Detection dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud).

A 5,000 row sample (`data/sample.csv`) is included so the project works out of the box.

For full results, download the complete dataset from Kaggle and place it at `data/creditcard.csv`, then run `python data/train_model.py`.

## About
Built by Amaan Najmi — 6+ years in financial crime compliance (AML, KYC, fraud) at PayPal,
MSc Business Analytics, UCD Dublin 2025.

## Licence
MIT