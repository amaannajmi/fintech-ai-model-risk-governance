# -*- coding: utf-8 -*-
# This script generates a Model Card using REAL metrics
# pulled automatically from the trained fraud detection model

import os
import json
from datetime import datetime
from jinja2 import Template

# ── STEP 1: LOAD REAL METRICS FROM JSON FILE ───────────────────────
# This reads the metrics that were saved when we trained the model
# Instead of typing numbers manually, we pull them straight from the model output
with open("data/model_metrics.json", "r") as f:
    metrics = json.load(f)

print("Real metrics loaded:")
for metric, value in metrics.items():
    print(f"  {metric}: {value}")

# ── STEP 2: BUILD THE MODEL INFORMATION ───────────────────────────
# Now we plug the real metrics into our model info dictionary
model_info = {
    "model_name": "Credit Card Fraud Detection Classifier",
    "version": "1.0",
    "date": datetime.today().strftime("%Y-%m-%d"),
    "developed_by": "Amaan Najmi",
    "model_type": "Supervised Binary Classification (Random Forest)",
    "language": "Python (Scikit-learn)",

    "intended_use": "Detect fraudulent credit card transactions in real time",
    "intended_users": "Financial crime compliance teams and fraud analysts",
    "training_data": "Kaggle ULB Credit Card Fraud Detection dataset — 284,807 real transactions, 492 fraud cases (0.17% fraud rate). Features V1-V28 are PCA-transformed for confidentiality.",

    # These are now REAL numbers pulled from the model automatically
    "performance": {
        "accuracy": str(metrics["accuracy"]),
        "precision": str(metrics["precision"]),
        "recall": str(metrics["recall"]),
        "f1_score": str(metrics["f1_score"]),
        "roc_auc": str(metrics["roc_auc"])
    },

    "out_of_scope": "Not suitable for credit scoring, identity verification, or non-card payment fraud",
    "limitations": "Recall of 0.8163 means approximately 18% of fraud cases are missed. Model trained on European cardholders — may not generalise globally.",
    "ethical_concerns": "Risk of bias against certain spending patterns. High precision reduces false accusations but missed fraud cases may disproportionately affect vulnerable customers. Fairness audit recommended.",
    "contact": "amaannajmi@gmail.com"
}

# ── STEP 3: TEMPLATE ───────────────────────────────────────────────
template_text = """
# Model Card - {{ model_name }}

## Model Details
- **Version:** {{ version }}
- **Date:** {{ date }}
- **Developed by:** {{ developed_by }}
- **Model type:** {{ model_type }}
- **Language/Framework:** {{ language }}

## Intended Use
- **Primary use:** {{ intended_use }}
- **Intended users:** {{ intended_users }}
- **Out of scope:** {{ out_of_scope }}

## Training Data
{{ training_data }}

## Performance Metrics
| Metric | Score |
|--------|-------|
| Accuracy | {{ performance.accuracy }} |
| Precision | {{ performance.precision }} |
| Recall | {{ performance.recall }} |
| F1 Score | {{ performance.f1_score }} |
| ROC AUC | {{ performance.roc_auc }} |

## Limitations
{{ limitations }}

## Ethical Considerations
{{ ethical_concerns }}

## Contact
{{ contact }}
"""

# ── STEP 4: GENERATE AND SAVE ──────────────────────────────────────
template = Template(template_text)
output = template.render(**model_info)

output_path = os.path.join("outputs", "model_card.md")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(output)

print("\nModel card generated successfully with real metrics!")
print(f"Saved to: {output_path}")