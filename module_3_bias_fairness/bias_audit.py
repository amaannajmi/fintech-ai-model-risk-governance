# -*- coding: utf-8 -*-
# This script runs a bias and fairness audit on the fraud detection model
# It checks whether the model performs equally well across different groups
# Groups are defined by transaction amount (low, medium, high)

import json
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import (precision_score, recall_score,
                             f1_score, confusion_matrix)

# ── STEP 1: LOAD THE MODEL ─────────────────────────────────────────
print("Loading model...")
with open("data/fraud_model.pkl", "rb") as f:
    model = pickle.load(f)

# ── STEP 2: LOAD THE SAMPLE DATA ──────────────────────────────────
print("Loading data...")
data = pd.read_csv("data/sample.csv")

# Separate features and label
X = data.drop(["Class", "Time"], axis=1)
y = data["Class"]

# ── STEP 3: GET MODEL PREDICTIONS ─────────────────────────────────
# Ask the model to predict fraud on the full sample
y_pred = model.predict(X)

# Add predictions back to the dataframe so we can slice by group
data["predicted"] = y_pred

# ── STEP 4: CREATE TRANSACTION AMOUNT GROUPS ──────────────────────
# We split transactions into three groups based on amount
# Low = bottom 33%, Medium = middle 33%, High = top 33%
# This lets us ask: does the model perform equally across all amount ranges?
data["amount_group"] = pd.qcut(
    data["Amount"],
    q=3,
    labels=["Low Amount", "Medium Amount", "High Amount"]
)

# ── STEP 5: CALCULATE FAIRNESS METRICS PER GROUP ──────────────────
# For each group we calculate:
# - Precision: when model says fraud, how often is it right?
# - Recall: out of all real fraud, how much did the model catch?
# - F1 Score: balance between precision and recall
# - Fraud Rate: what % of transactions in this group are actually fraud?

print("\nRunning fairness audit across transaction amount groups...")

results = []
groups = ["Low Amount", "Medium Amount", "High Amount"]

for group in groups:
    # Filter data to just this group
    group_data = data[data["amount_group"] == group]
    
    y_true_group = group_data["Class"]
    y_pred_group = group_data["predicted"]
    
    # Skip group if it has no fraud cases — metrics would be meaningless
    if y_true_group.sum() == 0:
        print(f"  {group}: No fraud cases found, skipping.")
        continue
    
    # Calculate metrics for this group
    precision = round(precision_score(y_true_group, y_pred_group, zero_division=0), 4)
    recall = round(recall_score(y_true_group, y_pred_group, zero_division=0), 4)
    f1 = round(f1_score(y_true_group, y_pred_group, zero_division=0), 4)
    fraud_rate = round(y_true_group.mean() * 100, 2)
    total = len(group_data)
    
    results.append({
        "group": group,
        "total_transactions": total,
        "fraud_rate_pct": fraud_rate,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    })
    
    print(f"  {group}: precision={precision}, recall={recall}, f1={f1}, fraud_rate={fraud_rate}%")

# ── STEP 6: SAVE RESULTS TO JSON ──────────────────────────────────
with open("data/bias_audit_results.json", "w") as f:
    json.dump(results, f, indent=4)
print("\nSaved: data/bias_audit_results.json")

# ── STEP 7: CREATE FAIRNESS CHART ─────────────────────────────────
# We create a bar chart comparing recall across groups
# Recall is the most important metric for fairness in fraud detection
# If recall is much lower for one group, the model is missing more fraud there

groups_labels = [r["group"] for r in results]
recalls = [r["recall"] for r in results]
f1_scores = [r["f1_score"] for r in results]

x = np.arange(len(groups_labels))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width/2, recalls, width, label="Recall", color="#2196F3")
bars2 = ax.bar(x + width/2, f1_scores, width, label="F1 Score", color="#FF5722")

# Add value labels on top of each bar
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=10)

for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=10)

ax.set_xlabel("Transaction Amount Group")
ax.set_ylabel("Score")
ax.set_title("Bias & Fairness Audit — Model Performance by Transaction Amount Group")
ax.set_xticks(x)
ax.set_xticklabels(groups_labels)
ax.set_ylim(0, 1.2)
ax.legend()
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("outputs/bias_audit.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: outputs/bias_audit.png")

# ── STEP 8: GENERATE TEXT SUMMARY ─────────────────────────────────
# This creates a simple written summary of the audit findings
# It flags any group where recall drops below 0.7 as a concern

print("\nGenerating audit summary...")

summary_lines = [
    "# Bias & Fairness Audit Report",
    "## Fraud Detection Model — Transaction Amount Analysis\n",
    "### Methodology",
    "Transactions were split into three equal groups by amount.",
    "Model performance was measured separately for each group.\n",
    "### Results\n",
    "| Group | Total | Fraud Rate | Precision | Recall | F1 Score |",
    "|-------|-------|------------|-----------|--------|----------|"
]

for r in results:
    summary_lines.append(
        f"| {r['group']} | {r['total_transactions']} | "
        f"{r['fraud_rate_pct']}% | {r['precision']} | "
        f"{r['recall']} | {r['f1_score']} |"
    )

summary_lines.append("\n### Findings")

# Automatically flag any group with recall below 0.7
concerns = [r for r in results if r["recall"] < 0.7]
if concerns:
    for c in concerns:
        summary_lines.append(
            f"- WARNING: Recall for {c['group']} is {c['recall']} "
            f"— model is missing fraud cases in this group."
        )
else:
    summary_lines.append(
        "- No major fairness concerns detected across amount groups."
    )

summary_lines.append("\n### Recommendation")
summary_lines.append(
    "- Continue monitoring performance across groups as new data arrives."
)
summary_lines.append(
    "- Consider retraining with stratified sampling if recall gaps widen."
)

summary_text = "\n".join(summary_lines)

with open("outputs/bias_audit_report.md", "w", encoding="utf-8") as f:
    f.write(summary_text)

print("Saved: outputs/bias_audit_report.md")
print("\nBias and fairness audit complete.")