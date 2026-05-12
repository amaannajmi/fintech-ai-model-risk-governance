# FinTech AI Model Risk Governance Framework

An open-source Python toolkit for AI model risk governance in financial services.

Built against a real fraud detection model trained on the Kaggle ULB Credit Card Fraud dataset (284,807 transactions).

## What This Project Does

This framework automatically generates five governance documents for an AI model:

1. **Model Card** — documents what the model does, how it performs, and its limitations
2. **SHAP Explainability Report** — explains why the model makes each decision
3. **Bias & Fairness Audit** — checks whether the model performs equally across transaction groups
4. **Data Drift Monitor** — detects when incoming data shifts away from training data
5. **EU AI Act Risk Classifier** — classifies the model under EU law and checks compliance

## Modules

| # | Module | Status |
|---|--------|--------|
| 1 | Model Card Generator | ✅ Complete |
| 2 | SHAP Explainability Report | ✅ Complete |
| 3 | Bias & Fairness Audit | ✅ Complete |
| 4 | Data Drift Monitor | ✅ Complete |
| 5 | EU AI Act Risk Classifier | ✅ Complete |

## EU AI Act Classification

This fraud detection model is classified as **HIGH RISK** under the EU AI Act (Annex III — Financial Services). All five modules in this framework directly address the legal obligations that classification creates.

| Obligation | Addressed By |
|------------|-------------|
| Technical documentation | Module 1 — Model Card |
| Explainability | Module 2 — SHAP Report |
| Bias and fairness testing | Module 3 — Fairness Audit |
| Post-deployment monitoring | Module 4 — Drift Monitor |
| Risk classification | Module 5 — EU AI Act Classifier |

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/amaannajmi/fintech-ai-model-risk-governance.git
cd fintech-ai-model-risk-governance
```

**2. Install dependencies**
```bash
pip install scikit-learn pandas numpy matplotlib shap jinja2 scipy
```

**3. Get the dataset**

A 5,000 row sample is included at `data/sample.csv` so the project works immediately.

For full results, download the complete dataset from [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) and place it at `data/creditcard.csv`, then run:
```bash
python data/train_model.py
```

**4. Run the modules**
```bash
python module_1_model_card/generate_model_card.py
python module_2_shap_explainability/generate_shap_report.py
python module_3_bias_fairness/bias_audit.py
python module_4_data_drift/drift_monitor.py
python module_5_eu_ai_act/eu_ai_classifier.py
```

All outputs are saved to the `outputs/` folder.

## Model Performance

Trained on the Kaggle ULB Credit Card Fraud Detection dataset:

| Metric | Score |
|--------|-------|
| Accuracy | 0.9996 |
| Precision | 0.9524 |
| Recall | 0.8163 |
| F1 Score | 0.8791 |
| ROC AUC | 0.9482 |

## About
Built by Amaan Najmi — 6+ years in financial crime compliance (AML, KYC, fraud) at PayPal,
MSc Business Analytics, UCD Dublin 2025.

## Licence
MIT