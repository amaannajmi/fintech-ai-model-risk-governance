# Governance Pipeline Summary Report
**Run Date:** 2026-05-12 22:48:34
**Model:** Credit Card Fraud Detection Classifier v1.0
**Developer:** Amaan Najmi

---

## Overall Governance Health: HEALTHY

## Pipeline Execution Summary

| Module | Status |
|--------|--------|
| Module 1 — Model Card Generator | PASS |
| Module 2 — SHAP Explainability Report | PASS |
| Module 3 — Bias & Fairness Audit | PASS |
| Module 4 — Data Drift Monitor | PASS |
| Module 5 — EU AI Act Risk Classifier | PASS |

## Model Performance

| Metric | Score |
|--------|-------|
| accuracy | 0.9996 |
| precision | 0.9524 |
| recall | 0.8163 |
| f1_score | 0.8791 |
| roc_auc | 0.9482 |

## Key Governance Findings

- **Primary fraud signal:** V14 (SHAP analysis)
- **Bias concerns detected:** None
- **Data drift detected:** None
- **EU AI Act risk level:** HIGH
- **EU AI Act compliance status:** COMPLIANT

## Recommendations

- No drift detected. Schedule next drift check in 30 days.
- No fairness concerns detected. Continue monitoring.
- Ensure EU AI Act database registration before any EU deployment.

---
*Generated automatically by the FinTech AI Model Risk Governance Framework*