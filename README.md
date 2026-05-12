# FinTech AI Model Risk Governance Framework

An open-source Python toolkit for AI model risk governance in financial services.

Built against a real fraud detection model trained on the Kaggle ULB Credit Card Fraud dataset (284,807 transactions).

## What This Project Does

This framework automates the complete AI model governance lifecycle for financial services — from documentation and explainability through to regulatory classification and ongoing monitoring. A single pipeline command runs everything end to end.

## Modules

| # | Module | Purpose | Status |
|---|--------|---------|--------|
| 1 | Model Card Generator | Automated model documentation | ✅ Complete |
| 2 | SHAP Explainability Report | Feature-level decision explanation | ✅ Complete |
| 3 | Bias & Fairness Audit | Performance equity across transaction groups | ✅ Complete |
| 4 | Data Drift Monitor | Statistical detection of input distribution shift | ✅ Complete |
| 5 | EU AI Act Risk Classifier | Regulatory classification and compliance status | ✅ Complete |
| — | Governance Pipeline Agent | Runs all 5 modules in one command | ✅ Complete |

## Run the Full Governance Pipeline

```bash
python run_governance_pipeline.py
```

One command runs all 5 modules, checks all outputs, and generates a final governance health report at `outputs/governance_summary.md`.

Example output: 
============================================================
FinTech AI Model Risk Governance Framework
Pipeline Agent v1.0
Overall Health:     HEALTHY
Modules Passed:     5/5
Drift Alerts:       0
Bias Concerns:      0
EU AI Act Status:   COMPLIANT
EU AI Act Risk:     HIGH

## EU AI Act Classification

This fraud detection model is classified as **HIGH RISK** under the EU AI Act (Annex III — Financial Services). All five modules directly address the legal obligations that classification creates.

| Obligation | Addressed By | Status |
|------------|-------------|--------|
| Technical documentation | Module 1 — Model Card | ✅ |
| Explainability | Module 2 — SHAP Report | ✅ |
| Bias and fairness testing | Module 3 — Fairness Audit | ✅ |
| Post-deployment monitoring | Module 4 — Drift Monitor | ✅ |
| Risk classification | Module 5 — EU AI Act Classifier | ✅ |

## Model Performance

Trained on the Kaggle ULB Credit Card Fraud Detection dataset:

| Metric | Score |
|--------|-------|
| Accuracy | 0.9996 |
| Precision | 0.9524 |
| Recall | 0.8163 |
| F1 Score | 0.8791 |
| ROC AUC | 0.9482 |

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

For full results, download the complete dataset from [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud), place it at `data/creditcard.csv`, then run:
```bash
python data/train_model.py
```

**4. Run the full pipeline**
```bash
python run_governance_pipeline.py
```

Or run individual modules:
```bash
python module_1_model_card/generate_model_card.py
python module_2_shap_explainability/generate_shap_report.py
python module_3_bias_fairness/bias_audit.py
python module_4_data_drift/drift_monitor.py
python module_5_eu_ai_act/eu_ai_classifier.py
```

All outputs are saved to the `outputs/` folder.

## About
Built by Amaan Najmi — 6+ years in financial crime compliance (AML, KYC, fraud) at PayPal,
MSc Business Analytics, UCD Dublin 2025.

## Licence
MIT