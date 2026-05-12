
# Model Card - Credit Card Fraud Detection Classifier

## Model Details
- **Version:** 1.0
- **Date:** 2026-05-12
- **Developed by:** Amaan Najmi
- **Model type:** Supervised Binary Classification (Random Forest)
- **Language/Framework:** Python (Scikit-learn)

## Intended Use
- **Primary use:** Detect fraudulent credit card transactions in real time
- **Intended users:** Financial crime compliance teams and fraud analysts
- **Out of scope:** Not suitable for credit scoring, identity verification, or non-card payment fraud

## Training Data
Kaggle ULB Credit Card Fraud Detection dataset — 284,807 real transactions, 492 fraud cases (0.17% fraud rate). Features V1-V28 are PCA-transformed for confidentiality.

## Performance Metrics
| Metric | Score |
|--------|-------|
| Accuracy | 0.9996 |
| Precision | 0.9524 |
| Recall | 0.8163 |
| F1 Score | 0.8791 |
| ROC AUC | 0.9482 |

## Limitations
Recall of 0.8163 means approximately 18% of fraud cases are missed. Model trained on European cardholders — may not generalise globally.

## Ethical Considerations
Risk of bias against certain spending patterns. High precision reduces false accusations but missed fraud cases may disproportionately affect vulnerable customers. Fairness audit recommended.

## Contact
amaannajmi@gmail.com